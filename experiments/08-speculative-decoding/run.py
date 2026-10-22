"""E8: measure decode speed and output identity for one speculative-decoding arm.

Run once per arm against a llama-server started with that arm's flags:
  python3 -I experiments/08-speculative-decoding/run.py --arm base
Standard library only. Writes results/<arm>.json.
"""

from __future__ import annotations

import argparse
import json
import statistics
import time
import urllib.request
from pathlib import Path

HERE = Path(__file__).resolve().parent
HOST = "http://127.0.0.1:8080"
REPS = 2


def call(path: str, body: dict) -> dict:
    req = urllib.request.Request(HOST + path, data=json.dumps(body).encode(), headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=900) as r:
        return json.load(r)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--arm", required=True)
    args = ap.parse_args()
    prompts = json.loads((HERE / "prompts.json").read_text())
    out = {}
    for name, text in prompts.items():
        prompt = call("/apply-template", {"messages": [{"role": "user", "content": text}],
                                          "chat_template_kwargs": {"enable_thinking": False}})["prompt"]
        runs = []
        for _ in range(REPS):
            t0 = time.perf_counter()
            r = call("/completion", {"prompt": prompt, "n_predict": 400, "temperature": 0, "seed": 0,
                                     "cache_prompt": False, "id_slot": 0})
            tm = r["timings"]
            runs.append({"decode_tok_s": tm["predicted_per_second"], "predicted_n": tm["predicted_n"],
                         "draft_n": tm.get("draft_n"), "draft_n_accepted": tm.get("draft_n_accepted"),
                         "wall_s": time.perf_counter() - t0, "content": r["content"]})
        out[name] = {"decode_tok_s": statistics.median(x["decode_tok_s"] for x in runs), "runs": runs,
                     "content": runs[0]["content"], "stable_across_reps": len({x["content"] for x in runs}) == 1}
        acc = runs[0]
        rate = f" accept {acc['draft_n_accepted']}/{acc['draft_n']}" if acc.get("draft_n") else ""
        print(f"{args.arm:12} {name:10} {out[name]['decode_tok_s']:6.1f} tok/s  ({acc['predicted_n']} tok){rate}", flush=True)
    (HERE / "results").mkdir(exist_ok=True)
    (HERE / "results" / f"{args.arm}.json").write_text(json.dumps(out, indent=1))


if __name__ == "__main__":
    main()
