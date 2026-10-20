"""B3b: library memory as a compiled KV package (llama-server slot snapshot) vs. RAG vs. bare.

Requires llama-server on 127.0.0.1:8080 started with --slot-save-path SLOT_DIR -np 1.
Standard library only. Usage:
  python3 -I experiments/03b-library-kv-packages/run.py --slot-dir ~/.cache/local-memory/slots
"""

from __future__ import annotations

import argparse
import json
import os
import re
import time
import urllib.request
from pathlib import Path

HOST = "http://127.0.0.1:8080"
ROOT = Path(__file__).resolve().parents[2]
SOURCE = ROOT / "packages/source/netkit-0.2/package.json"
TASKS = ROOT / "bench/tasks/netkit-0.1.json"
IDENT = re.compile(r"[A-Za-z_][A-Za-z0-9_]*")


def call(method: str, path: str, body: dict | None = None, timeout: int = 900) -> dict:
    data = json.dumps(body).encode() if body is not None else None
    req = urllib.request.Request(HOST + path, data=data, method=method, headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return json.load(r)


def evict(path: Path) -> None:
    fd = os.open(path, os.O_RDONLY)
    try:
        os.fsync(fd)
        os.posix_fadvise(fd, 0, 0, os.POSIX_FADV_DONTNEED)
    finally:
        os.close(fd)


def complete(prompt: str) -> tuple[dict, float]:
    t0 = time.perf_counter()
    r = call("POST", "/completion", {"prompt": prompt, "n_predict": 24, "temperature": 0, "seed": 0,
                                     "cache_prompt": True, "id_slot": 0})
    return r, time.perf_counter() - t0


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--slot-dir", type=Path, required=True)
    args = ap.parse_args()

    pkg = json.loads(SOURCE.read_text())
    lib, names = pkg["library"], {s["name"] for s in pkg["symbols"]}
    reference = "\n".join(f"{lib}.{s['name']}{s['signature']}  # {s['doc']}" for s in pkg["symbols"])
    system = f"You write Python using the {lib} library. Use ONLY functions from this API reference:\n{reference}"
    tasks = json.loads(TASKS.read_text())["tasks"]

    def render(task: str, with_reference: bool) -> str:
        msgs = ([{"role": "system", "content": system}] if with_reference else []) + [
            {"role": "user", "content": f"Task: {task}\nReply with only the {lib} function call, e.g. {lib}.function_name(...)."}]
        return call("POST", "/apply-template", {"messages": msgs, "chat_template_kwargs": {"enable_thinking": False}})["prompt"]

    # The package is the rendered prefix up to the end of the system message (stable part).
    sample = render("x", True)
    head_ref = sample[: sample.index("<|im_start|>user")]
    items = [(t["symbol"], t[split]) for t in tasks for split in ("dev", "test")]

    # Compile the package: process the reference once and snapshot the slot to the SSD.
    pkg_file = f"pkg-{lib}-{pkg['version']}.bin"
    call("POST", "/slots/0?action=erase", {})
    t0 = time.perf_counter()
    call("POST", "/completion", {"prompt": head_ref, "n_predict": 1, "temperature": 0, "cache_prompt": True, "id_slot": 0})
    compile_s = time.perf_counter() - t0
    saved = call("POST", "/slots/0?action=save", {"filename": pkg_file})
    pkg_gb = (args.slot_dir / pkg_file).stat().st_size / 1e9
    ref_tokens = len(call("POST", "/tokenize", {"content": head_ref})["tokens"])
    print(f"compiled package: {ref_tokens} reference tokens, {pkg_gb:.2f} GB, {compile_s:.1f} s ({saved.get('n_saved')} tokens saved)")

    rows = []
    for symbol, task in items:
        row = {"symbol": symbol, "task": task}
        for arm in ("bare", "rag", "kvpack"):
            prompt = render(task, arm != "bare")
            if arm != "bare":
                assert prompt.startswith(head_ref), "rendered prompt does not start with the package prefix"
            call("POST", "/slots/0?action=erase", {})
            restore_s = 0.0
            if arm == "kvpack":
                evict(args.slot_dir / pkg_file)
                t0 = time.perf_counter()
                call("POST", "/slots/0?action=restore", {"filename": pkg_file})
                restore_s = time.perf_counter() - t0
            r, wall = complete(prompt)
            m = re.search(rf"{lib}\.([A-Za-z_][A-Za-z0-9_]*)", r["content"])
            pred = m.group(1) if m else ""
            row[arm] = {"predicted": pred, "exact": pred == symbol, "invented": bool(pred) and pred not in names,
                        "content": r["content"], "prompt_n": r["timings"]["prompt_n"],
                        "prompt_s": r["timings"]["prompt_ms"] / 1000, "restore_s": restore_s,
                        "ttft_s": restore_s + r["timings"]["prompt_ms"] / 1000, "wall_s": wall + restore_s}
        rows.append(row)
        print(f"{symbol:12} bare={row['bare']['predicted']:<14} rag={row['rag']['predicted']:<14} "
              f"kv={row['kvpack']['predicted']:<14} ttft rag {row['rag']['ttft_s']:5.2f}s kv {row['kvpack']['ttft_s']:5.2f}s", flush=True)

    def agg(arm: str, key: str) -> float:
        return sum(r[arm][key] for r in rows) / len(rows)

    summary = {arm: {"exact_match": agg(arm, "exact"), "invented": agg(arm, "invented"), "ttft_s": agg(arm, "ttft_s"),
                     "prompt_n": agg(arm, "prompt_n")} for arm in ("bare", "rag", "kvpack")}
    summary["kvpack_identical_to_rag"] = sum(r["kvpack"]["content"] == r["rag"]["content"] for r in rows)
    summary["n"] = len(rows)
    summary["reference_tokens"], summary["package_gb"], summary["compile_s"] = ref_tokens, pkg_gb, compile_s
    out = Path(__file__).resolve().parent / "results"
    out.mkdir(exist_ok=True)
    (out / f"b3b-{int(time.time())}.json").write_text(json.dumps({"summary": summary, "rows": rows}, indent=1))
    print(json.dumps(summary, indent=1))


if __name__ == "__main__":
    main()
