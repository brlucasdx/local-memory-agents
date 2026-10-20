"""B2: cold prefill vs. restoring a context snapshot from the SSD, on llama-server.

For each target context size:
  1. erase slot 0, send the long prompt cold, record prefill time and a greedy
     continuation (reference output);
  2. save the slot to disk (snapshot), record save time and file size;
  3. erase the slot (the context is now only on the SSD);
  4. restore the snapshot, record restore time;
  5. send the same prompt again: llama-server must reuse the restored tokens
     (tokens_cached / prompt_n) and produce the identical greedy continuation.

Only talks to llama-server on 127.0.0.1. Standard library only.
Usage: python3 -I measure.py --sizes 8000 32000 --slot-dir <dir used in --slot-save-path>
"""

from __future__ import annotations

import argparse
import json
import os
import time
import urllib.request
from pathlib import Path

HOST = "http://127.0.0.1:8080"
ROOT = Path(__file__).resolve().parents[2]


def call(method: str, path: str, body: dict | None = None, timeout: int = 1800) -> dict:
    data = json.dumps(body).encode() if body is not None else None
    req = urllib.request.Request(HOST + path, data=data, method=method, headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return json.load(r)


def corpus(n_chars: int) -> str:
    """Real code as context: the llama.cpp server sources, repeated if needed."""
    src = Path.home() / ".local/src/llama.cpp-v0.7.0/tools/server"
    text = "".join(p.read_text(errors="ignore") for p in sorted(src.rglob("*.cpp")))
    while len(text) < n_chars:
        text += text
    return text[:n_chars]


def evict_from_page_cache(path: Path) -> None:
    """Drop the snapshot's pages from the Linux page cache so the restore really reads the NVMe.

    Works without root for a file we own: flush it, then POSIX_FADV_DONTNEED.
    """
    fd = os.open(path, os.O_RDONLY)
    try:
        os.fsync(fd)
        os.posix_fadvise(fd, 0, 0, os.POSIX_FADV_DONTNEED)
    finally:
        os.close(fd)


def complete(prompt: str, n_predict: int) -> tuple[dict, float]:
    t0 = time.perf_counter()
    r = call("POST", "/completion", {"prompt": prompt, "n_predict": n_predict, "temperature": 0,
                                     "cache_prompt": True, "id_slot": 0, "seed": 0})
    return r, time.perf_counter() - t0


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--sizes", type=int, nargs="+", default=[8000, 32000])
    ap.add_argument("--slot-dir", type=Path, required=True)
    ap.add_argument("--n-predict", type=int, default=48)
    args = ap.parse_args()

    results = []
    for target in args.sizes:
        tok = call("POST", "/tokenize", {"content": corpus(target * 5)})["tokens"][:target]
        prompt = call("POST", "/detokenize", {"tokens": tok})["content"] + "\n// Summary of the code above in one sentence:\n"
        name = f"ctx{target}.bin"

        call("POST", "/slots/0?action=erase", {})
        cold, cold_wall = complete(prompt, args.n_predict)

        t0 = time.perf_counter()
        call("POST", "/slots/0?action=save", {"filename": name})
        save_s = time.perf_counter() - t0
        size_gb = (args.slot_dir / name).stat().st_size / 1e9

        call("POST", "/slots/0?action=erase", {})
        evict_from_page_cache(args.slot_dir / name)
        t0 = time.perf_counter()
        restored = call("POST", "/slots/0?action=restore", {"filename": name})
        restore_s = time.perf_counter() - t0

        warm, warm_wall = complete(prompt, args.n_predict)
        row = {
            "target_tokens": target,
            "prompt_tokens": cold["timings"]["prompt_n"] + cold.get("tokens_cached", 0) - cold.get("tokens_cached", 0),
            "cold_prefill_s": cold["timings"]["prompt_ms"] / 1000,
            "cold_wall_s": cold_wall,
            "snapshot_gb": size_gb,
            "save_s": save_s,
            "restore_s": restore_s,
            "restore_reported": restored,
            "warm_prompt_n": warm["timings"]["prompt_n"],
            "warm_prefill_s": warm["timings"]["prompt_ms"] / 1000,
            "warm_wall_s": warm_wall,
            "decode_tok_s_cold": cold["timings"]["predicted_per_second"],
            "decode_tok_s_warm": warm["timings"]["predicted_per_second"],
            "identical_output": cold["content"] == warm["content"],
        }
        row["speedup_prefill_vs_restore"] = row["cold_prefill_s"] / max(row["restore_s"] + row["warm_prefill_s"], 1e-9)
        results.append(row)
        print(f"{target:>7} tok | cold prefill {row['cold_prefill_s']:6.1f}s | snapshot {size_gb:5.2f} GB "
              f"save {save_s:5.2f}s restore {restore_s:5.2f}s | warm re-read {row['warm_prompt_n']} tok "
              f"{row['warm_prefill_s']:5.2f}s | x{row['speedup_prefill_vs_restore']:.0f} | "
              f"decode {row['decode_tok_s_cold']:.1f} tok/s | identical={row['identical_output']}", flush=True)

    out = Path(__file__).resolve().parent / "results"
    out.mkdir(exist_ok=True)
    (out / f"b2-{int(time.time())}.json").write_text(json.dumps(results, indent=1))


if __name__ == "__main__":
    main()
