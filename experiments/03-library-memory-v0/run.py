"""B3: does self-encoded library memory let a frozen core name an unseen API?

Usage:
  .venv/bin/python experiments/03-library-memory-v0/run.py --model Qwen/Qwen3-0.6B --split dev
  .venv/bin/python experiments/03-library-memory-v0/run.py --model Qwen/Qwen3-0.6B --split test \
      --layer 12 --alpha 1 --value last
"""

from __future__ import annotations

import argparse
import json
import re
import sys
import time
from pathlib import Path

import torch
from transformers import AutoModelForCausalLM, AutoTokenizer

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src"))

from libmem.inject import injected, match_positions  # noqa: E402
from libmem.package import compile_package, load_compiled, load_source, save_compiled  # noqa: E402

SOURCE = ROOT / "packages/source/netkit-0.1/package.json"
TASKS = ROOT / "bench/tasks/netkit-0.1.json"
RESULTS = Path(__file__).resolve().parent / "results"
IDENT = re.compile(r"[A-Za-z_][A-Za-z0-9_]*")


def prompt(task: str, library: str, docs: str | None) -> str:
    ref = f"# {library} API reference:\n{docs}\n\n" if docs else ""
    return f"import {library}\n\n{ref}# {task}\nresult = {library}."


@torch.no_grad()
def run_one(model, tok, text: str, gold: str, layer: int | None, values, alpha: float, keys):
    ids = tok(text, return_tensors="pt").input_ids.to(model.device)
    positions = match_positions(ids[0].tolist(), tok, keys) if layer is not None else {}
    gold_ids = tok(gold, add_special_tokens=False, return_tensors="pt").input_ids.to(model.device)

    def forward_ctx():
        if layer is None or not positions:
            from contextlib import nullcontext
            return nullcontext()
        return injected(model, layer, positions, values, alpha)

    with forward_ctx():
        out = model.generate(ids, max_new_tokens=12, do_sample=False, pad_token_id=tok.eos_token_id)
    completion = tok.decode(out[0, ids.shape[1]:], skip_special_tokens=True)
    m = IDENT.match(completion)
    predicted = m.group(0) if m else ""

    full = torch.cat([ids, gold_ids], dim=1)
    with forward_ctx():
        logits = model(full).logits[0, ids.shape[1] - 1:-1].float()
    logp = torch.log_softmax(logits, dim=-1).gather(1, gold_ids[0].unsqueeze(1)).mean().item()
    return {"predicted": predicted, "exact": predicted == gold, "gold_logp": logp,
            "prompt_tokens": ids.shape[1], "matched_positions": len(positions)}


def evaluate(model, tok, source, compiled, tasks, split, arm, layer, alpha, value):
    names = [s.name for s in source.symbols]
    keys = {i: s.keys for i, s in enumerate(source.symbols)}
    docs = "\n".join("# " + s.doc_line(source.library) for s in source.symbols)
    vals = compiled[f"values_{value}"][:, layer, :] if layer is not None else None
    if arm == "mem_shuf" and vals is not None:
        vals = torch.roll(vals, shifts=7, dims=0)  # derangement: each symbol gets another's value
    rows = []
    for t in tasks:
        text = prompt(t[split], source.library, docs if arm == "rag" else None)
        use_layer = layer if arm in ("mem", "mem_shuf") else None
        r = run_one(model, tok, text, t["symbol"], use_layer, vals, alpha, keys)
        rows.append({"symbol": t["symbol"], **r})
    acc = sum(r["exact"] for r in rows) / len(rows)
    return {"arm": arm, "layer": layer, "alpha": alpha, "value": value, "exact_match": acc,
            "mean_gold_logp": sum(r["gold_logp"] for r in rows) / len(rows),
            "mean_prompt_tokens": sum(r["prompt_tokens"] for r in rows) / len(rows), "rows": rows}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--model", default="Qwen/Qwen3-0.6B")
    ap.add_argument("--split", choices=["dev", "test"], required=True)
    ap.add_argument("--layer", type=int)
    ap.add_argument("--alpha", type=float)
    ap.add_argument("--value", choices=["last", "mean"])
    ap.add_argument("--threads", type=int, default=6)
    args = ap.parse_args()
    torch.set_num_threads(args.threads)
    torch.manual_seed(0)

    source = load_source(SOURCE)
    tasks = json.loads(TASKS.read_text())["tasks"]
    tok = AutoTokenizer.from_pretrained(args.model)
    model = AutoModelForCausalLM.from_pretrained(args.model, dtype=torch.bfloat16, device_map="cuda").eval()

    slug = args.model.replace("/", "__")
    cpath = ROOT / f"packages/compiled/{source.library}-{source.version}/{slug}.pt"
    try:
        compiled = load_compiled(cpath, source, args.model)
    except (FileNotFoundError, ValueError):
        t0 = time.time()
        compiled = compile_package(source, model, tok, args.model)
        save_compiled(compiled, cpath)
        print(f"compiled {len(source.symbols)} symbols in {time.time() - t0:.1f}s -> {cpath.relative_to(ROOT)}")

    n_layers = compiled["values_last"].shape[1] - 1
    runs = [evaluate(model, tok, source, compiled, tasks, args.split, a, None, 0.0, "last") for a in ("bare", "rag")]
    if args.split == "dev":
        grid = [(l, a, v) for l in range(2, n_layers, 2) for a in (0.25, 0.5, 1, 2, 4) for v in ("last", "mean")]
    else:
        if None in (args.layer, args.alpha, args.value):
            sys.exit("test split needs the frozen --layer --alpha --value chosen on dev")
        grid = [(args.layer, args.alpha, args.value)]
    for layer, alpha, value in grid:
        for arm in ("mem", "mem_shuf"):
            runs.append(evaluate(model, tok, source, compiled, tasks, args.split, arm, layer, alpha, value))

    RESULTS.mkdir(exist_ok=True)
    out = RESULTS / f"{slug}-{args.split}.json"
    out.write_text(json.dumps({"model": args.model, "split": args.split, "n_layers": n_layers,
                               "torch": torch.__version__, "runs": runs}, indent=1))
    best = sorted((r for r in runs if r["arm"] == "mem"), key=lambda r: (r["exact_match"], r["mean_gold_logp"]), reverse=True)
    print(f"bare  EM={runs[0]['exact_match']:.2f} logp={runs[0]['mean_gold_logp']:.2f} tokens={runs[0]['mean_prompt_tokens']:.0f}")
    print(f"rag   EM={runs[1]['exact_match']:.2f} logp={runs[1]['mean_gold_logp']:.2f} tokens={runs[1]['mean_prompt_tokens']:.0f}")
    for r in best[:5]:
        shuf = next(s for s in runs if s["arm"] == "mem_shuf" and (s["layer"], s["alpha"], s["value"]) == (r["layer"], r["alpha"], r["value"]))
        print(f"mem   L={r['layer']:2} a={r['alpha']:<4} {r['value']:4} EM={r['exact_match']:.2f} logp={r['mean_gold_logp']:.2f} | shuf EM={shuf['exact_match']:.2f} logp={shuf['mean_gold_logp']:.2f}")
    print(f"-> {out.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
