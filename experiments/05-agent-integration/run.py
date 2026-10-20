"""E5: run the Pi agent on netkit tasks across the cold / ssd / ram / nolib arms and grade by execution.

Requires: llama-server on 127.0.0.1:8080 (with --metrics and --slot-save-path),
the local-llm-kv-cache proxy on 127.0.0.1:8081 (for the ssd arm), and Pi with the
`localmem-direct` / `localmem-proxy` providers. Standard library only.
Usage: python3 -I experiments/05-agent-integration/run.py [--arms cold ssd ram nolib]
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
TASKS = json.loads((ROOT / "bench/agent/tasks.json").read_text())
STUB = ROOT / "bench/agent/netkit_stub/netkit.py"
SOURCE = ROOT / "packages/source/netkit-0.2/package.json"
WORK = Path.home() / ".cache/local-memory/agent-work"  # fixed path: keeps the prompt prefix stable
LLAMA = "http://127.0.0.1:8080"
PI = str(Path.home() / ".local/bin/pi")
ARMS = {
    "cold": {"provider": "localmem-direct", "erase": True, "lib": True},
    "ssd": {"provider": "localmem-proxy", "erase": True, "lib": True},
    "ram": {"provider": "localmem-direct", "erase": False, "lib": True},
    "nolib": {"provider": "localmem-direct", "erase": False, "lib": False},
}


def http(method: str, url: str, body: dict | None = None) -> bytes:
    data = json.dumps(body).encode() if body is not None else None
    req = urllib.request.Request(url, data=data, method=method, headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=120) as r:
        return r.read()


def prompt_tokens_total() -> float:
    text = http("GET", f"{LLAMA}/metrics").decode()
    m = re.search(r"^llamacpp:prompt_tokens_total\s+([0-9.e+]+)", text, re.M)
    return float(m.group(1)) if m else float("nan")


def reference_file() -> Path:
    pkg = json.loads(SOURCE.read_text())
    lines = [f"{pkg['library']}.{s['name']}{s['signature']}  # {s['doc']}" for s in pkg["symbols"]]
    path = HERE / "netkit-0.2-reference.md"
    path.write_text(f"# {pkg['library']} {pkg['version']} API reference\nUse ONLY these functions when writing code that imports {pkg['library']}:\n\n" + "\n".join(lines) + "\n")
    return path


def reset_workdir() -> None:
    if WORK.exists():
        shutil.rmtree(WORK)  # fixed, script-owned path under ~/.cache/local-memory
    WORK.mkdir(parents=True)
    shutil.copy(STUB, WORK / "netkit.py")


def grade(symbol: str, log: Path) -> dict:
    script = WORK / "check.py"
    if not script.exists():
        return {"success": False, "exit": None, "called": [], "reason": "no check.py"}
    log.unlink(missing_ok=True)
    proc = subprocess.run(["python3", "-s", "check.py"], cwd=WORK, capture_output=True, text=True, timeout=60,
                          env={**os.environ, "NETKIT_CALL_LOG": str(log), "PYTHONPATH": str(WORK)})
    called = log.read_text().split() if log.exists() else []
    return {"success": proc.returncode == 0 and symbol in called, "exit": proc.returncode, "called": called,
            "stderr_tail": proc.stderr[-300:]}


def tool_calls(session_dir: Path) -> int:
    files = sorted(session_dir.rglob("*.jsonl"), key=lambda p: p.stat().st_mtime)
    if not files:
        return -1
    return sum('"toolCall"' in line for line in files[-1].read_text().splitlines())


def run_session(arm: str, symbol: str, goal: str, ref: Path, sessions: Path, logs: Path) -> dict:
    cfg = ARMS[arm]
    reset_workdir()
    if cfg["erase"]:
        http("POST", f"{LLAMA}/slots/0?action=erase", {})
    before = prompt_tokens_total()
    task = TASKS["template"].format(goal=goal)
    sdir = sessions / arm
    sdir.mkdir(parents=True, exist_ok=True)
    cmd = [PI, "-p", "-nc", "--model", f"{cfg['provider']}/ornith:low", "--session-dir", str(sdir)]
    if cfg["lib"]:
        cmd += ["--append-system-prompt", str(ref)]
    cmd.append(task)
    t0 = time.perf_counter()
    try:
        proc = subprocess.run(cmd, cwd=WORK, capture_output=True, text=True, timeout=900,
                              env={**os.environ, "NETKIT_CALL_LOG": str(logs / f"{arm}-{symbol}-agent.log")})
        timed_out = False
    except subprocess.TimeoutExpired:
        proc, timed_out = None, True
    wall = time.perf_counter() - t0
    after = prompt_tokens_total()
    result = grade(symbol, logs / f"{arm}-{symbol}-grade.log")
    return {"arm": arm, "symbol": symbol, "wall_s": wall, "timed_out": timed_out,
            "prompt_tokens_processed": after - before, "tool_calls": tool_calls(sdir),
            "agent_exit": None if proc is None else proc.returncode, **result}


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--arms", nargs="+", default=list(ARMS))
    args = ap.parse_args()
    ref = reference_file()
    stamp = int(time.time())
    out = HERE / "results" / str(stamp)
    sessions, logs = out / "sessions", out / "logs"
    logs.mkdir(parents=True)
    rows = []
    for arm in args.arms:
        if arm == "ssd":
            w = TASKS["warmup"]
            warm = run_session("ssd", w["symbol"], w["goal"], ref, out / "warmup-sessions", logs)
            print(f"[warm-up ssd] {warm['wall_s']:.0f}s, {warm['prompt_tokens_processed']:.0f} prompt tokens; waiting for the golden snapshot", flush=True)
            time.sleep(30)
        for t in TASKS["tasks"]:
            r = run_session(arm, t["symbol"], t["goal"], ref, sessions, logs)
            rows.append(r)
            print(f"{arm:6} {t['symbol']:10} {'OK ' if r['success'] else 'FAIL'} wall {r['wall_s']:6.1f}s "
                  f"prefill {r['prompt_tokens_processed']:7.0f} tok  tools {r['tool_calls']:3}  called {r['called'][:3]}", flush=True)
        (out / "rows.json").write_text(json.dumps(rows, indent=1))

    summary = {}
    for arm in args.arms:
        rs = [r for r in rows if r["arm"] == arm]
        summary[arm] = {"success": sum(r["success"] for r in rs), "n": len(rs),
                        "median_wall_s": statistics.median(r["wall_s"] for r in rs),
                        "median_prompt_tokens": statistics.median(r["prompt_tokens_processed"] for r in rs),
                        "median_tool_calls": statistics.median(r["tool_calls"] for r in rs)}
    (out / "summary.json").write_text(json.dumps(summary, indent=1))
    print(json.dumps(summary, indent=1))


if __name__ == "__main__":
    main()
