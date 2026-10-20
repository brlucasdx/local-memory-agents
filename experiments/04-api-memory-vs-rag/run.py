"""B4: Pi agent on Polars 2.0 tasks — nolib vs rag vs pkg (KV snapshot of the official upgrade guide).

Requires llama-server on 127.0.0.1:8080 (--metrics, --slot-save-path) and the
local-llm-kv-cache proxy on 127.0.0.1:8081. Standard library only; grading runs
in the project venv. Usage: python3 -I experiments/04-api-memory-vs-rag/run.py
"""

from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import statistics
import subprocess
import time
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
TASKS = json.loads((ROOT / "bench/tasks/polars-2.0/tasks.json").read_text())
GUIDE = ROOT / "packages/source/polars-2.0.0/UPGRADE-2.md"
ORACLE_DIR = ROOT / "bench/oracles/polars-2.0"
VENV_BIN = ROOT / ".venv/bin"
WORK = Path.home() / ".cache/local-memory/agent-work"
LLAMA = "http://127.0.0.1:8080"
PI = str(Path.home() / ".local/bin/pi")
ARMS = {
    "nolib": {"provider": "localmem-direct", "erase": False, "pkg": False, "rag": False},
    "rag": {"provider": "localmem-direct", "erase": False, "pkg": False, "rag": True},
    "pkg": {"provider": "localmem-proxy", "erase": True, "pkg": True, "rag": False},
}
STOP = set("a an the of to in on and or is are be with for that this by as at it its from into than then each every "
           "returns return use used using polars function df column columns dtype value values exactly".split())


def http(method: str, url: str, body: dict | None = None) -> bytes:
    data = json.dumps(body).encode() if body is not None else None
    req = urllib.request.Request(url, data=data, method=method, headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=120) as r:
        return r.read()


def prompt_tokens_total() -> float:
    m = re.search(r"^llamacpp:prompt_tokens_total\s+([0-9.e+]+)", http("GET", f"{LLAMA}/metrics").decode(), re.M)
    return float(m.group(1)) if m else float("nan")


def words(text: str) -> set[str]:
    return {w for w in re.findall(r"[a-z_][a-z0-9_]+", text.lower()) if w not in STOP and len(w) > 2}


def rag_excerpts(task_text: str, k: int = 3) -> str:
    """Lexical RAG: the k '###' sections of the guide with the largest word overlap with the task."""
    sections = re.split(r"(?m)^(?=### )", GUIDE.read_text())
    q = words(task_text)
    ranked = sorted(sections, key=lambda s: len(q & words(s)), reverse=True)[:k]
    return "\n\n".join(s.strip() for s in ranked)


def task_text(t: dict) -> str:
    return TASKS["template"].format(signature=t["signature"], goal=t["goal"])


def reset_workdir() -> None:
    if WORK.exists():
        shutil.rmtree(WORK)  # fixed, script-owned path under ~/.cache/local-memory
    WORK.mkdir(parents=True)


def grade(t: dict) -> dict:
    if not (WORK / "solution.py").exists():
        return {"success": False, "reason": "no solution.py"}
    fname = t["signature"].split("(")[0]
    code = (f"import sys; sys.path[:0] = [{str(WORK)!r}, {str(ORACLE_DIR)!r}]\n"
            f"import warnings; warnings.simplefilter('ignore')\n"
            f"import oracle, solution\n"
            f"oracle.TESTS[{t['id']!r}](getattr(solution, {fname!r}))\nprint('PASS')")
    try:
        p = subprocess.run([str(VENV_BIN / "python"), "-I", "-c", code], cwd=WORK, capture_output=True, text=True, timeout=120)
    except subprocess.TimeoutExpired:
        return {"success": False, "reason": "grader timeout"}
    return {"success": p.returncode == 0 and "PASS" in p.stdout, "reason": p.stderr.strip().splitlines()[-1][:200] if p.returncode else ""}


def tool_calls(session_dir: Path) -> int:
    files = sorted(session_dir.rglob("*.jsonl"), key=lambda p: p.stat().st_mtime)
    return sum('"toolCall"' in line for line in files[-1].read_text().splitlines()) if files else -1


def run_session(arm: str, t: dict, sessions: Path) -> dict:
    cfg = ARMS[arm]
    reset_workdir()
    if cfg["erase"]:
        http("POST", f"{LLAMA}/slots/0?action=erase", {})
    text = task_text(t)
    if cfg["rag"]:
        text += "\n\nRelevant excerpts from the official Polars 2.0 upgrade guide:\n\n" + rag_excerpts(t["goal"] + " " + t["signature"])
    sdir = sessions / arm
    sdir.mkdir(parents=True, exist_ok=True)
    cmd = [PI, "-p", "-nc", "--model", f"{cfg['provider']}/ornith:low", "--session-dir", str(sdir)]
    if cfg["pkg"]:
        cmd += ["--append-system-prompt", str(GUIDE)]
    cmd.append(text)
    env = {**os.environ, "PATH": f"{VENV_BIN}:{os.environ['PATH']}"}
    before, t0 = prompt_tokens_total(), time.perf_counter()
    try:
        subprocess.run(cmd, cwd=WORK, capture_output=True, text=True, timeout=900, env=env)
        timed_out = False
    except subprocess.TimeoutExpired:
        timed_out = True
    wall = time.perf_counter() - t0
    tokens = prompt_tokens_total() - before
    return {"arm": arm, "task": t["id"], "kind": t["kind"], "wall_s": wall, "timed_out": timed_out,
            "prompt_tokens_processed": tokens, "tool_calls": tool_calls(sdir), **grade(t)}


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--arms", nargs="+", default=list(ARMS))
    args = ap.parse_args()
    out = HERE / "results" / str(int(time.time()))
    out.mkdir(parents=True)
    rows = []
    for arm in args.arms:
        if arm == "pkg":
            warm = {"id": "warmup", "kind": "-", "signature": "polars_version() -> str", "goal": "returns pl.__version__"}
            w = run_session("pkg", warm, out / "warmup-sessions")
            print(f"[warm-up pkg] {w['wall_s']:.0f}s, {w['prompt_tokens_processed']:.0f} prompt tokens; waiting for the golden snapshot", flush=True)
            time.sleep(30)
        for t in TASKS["tasks"]:
            r = run_session(arm, t, out / "sessions")
            rows.append(r)
            print(f"{arm:5} {t['id']:20} [{t['kind']:15}] {'OK  ' if r['success'] else 'FAIL'} wall {r['wall_s']:6.1f}s "
                  f"prefill {r['prompt_tokens_processed']:7.0f}  tools {r['tool_calls']:3}  {r.get('reason', '')[:70]}", flush=True)
        (out / "rows.json").write_text(json.dumps(rows, indent=1))
    summary = {}
    for arm in args.arms:
        rs = [r for r in rows if r["arm"] == arm]
        summary[arm] = {"success": sum(r["success"] for r in rs), "n": len(rs),
                        "by_kind": {k: f"{sum(r['success'] for r in rs if r['kind'] == k)}/{sum(r['kind'] == k for r in rs)}" for k in sorted({r['kind'] for r in rs})},
                        "median_wall_s": statistics.median(r["wall_s"] for r in rs),
                        "median_prompt_tokens": statistics.median(r["prompt_tokens_processed"] for r in rs),
                        "median_tool_calls": statistics.median(r["tool_calls"] for r in rs)}
    (out / "summary.json").write_text(json.dumps(summary, indent=1))
    print(json.dumps(summary, indent=1))


if __name__ == "__main__":
    main()
