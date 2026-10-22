# E8 — Speculative decoding for Ornith 9B on the RTX 3060 (DFlash and n-gram)

**Question:** does speculative decoding raise Ornith 1.5 9B's generation speed on a 12 GB consumer GPU, on code, without changing the output?

## Pre-registration (written 2026-10-22, before any run)
- **Target:** Ornith 1.5 9B Q6_K (the same GGUF as every other experiment), llama.cpp v0.7.0 (commit 620d222), `-ngl 99 -c 16384 -fa on -np 1`, greedy (temperature 0), thinking disabled through the chat template, 400 new tokens.
- **Drafter:** [`audreyt/Ornith-1.5-9B-DFlash-GGUF`](https://huggingface.co/audreyt/Ornith-1.5-9B-DFlash-GGUF) `ornith1.5-9b-dflash-bf16-projection-Q4_K_M.gguf` (766 MB, SHA-256 `76ed0c5d…511f2` verified). Community drafter; its author reports +16.8% on a counting prompt and a slowdown on literary text (Apple M4, DS4 runtime), mean accepted length 2.77.
- **Arms:** `base` (no speculation) · `dflash-n4` and `dflash-n8` (`--spec-type draft-dflash`, `--spec-draft-n-max` 4 / 8) · `ngram-mod` and `ngram-cache` (llama.cpp's draft-free n-gram speculation, default parameters).
- **Workloads** (`prompts.json`): `code-py` (new Python module + tests), `code-rb` (Rails model + test), `code-edit` (return a given ~100-line file with a small change: copy-heavy), `prose` (control).
- **Metrics:** decode tok/s (`timings.predicted_per_second`), speed-up vs `base`, draft acceptance when reported, and **byte-identical output vs `base`** (greedy speculation must not change the text).

### Gate
- **Worth adopting** if an arm gives **≥ 1.3×** decode speed on the code workloads (median of `code-py`, `code-rb`, `code-edit`) with output identical to `base` on all of them.
- Any arm that changes greedy output is reported as **not lossless** regardless of speed.

## Results (2026-10-22) — no arm passes the gate; DFlash is fast but not byte-identical

Two repetitions per workload, 400 new tokens, greedy. Baseline: 39–41 tok/s. Raw data in `results/`.

**Repetition matters for `ngram-mod`:** llama.cpp keeps its n-gram table across requests, so the **second** run of the same prompt is predicted from the first run's output (code-py 272 tok/s, 6.65×). That is not a generation speed-up and is excluded. Only the first run counts.

| Arm | code-py | code-rb | code-edit | prose | Output identical to `base` |
|---|---|---|---|---|---|
| `dflash-n4` | 1.66× | 1.85× | 2.69× | 1.44× | only code-edit |
| **`dflash-n8`** | **2.04×** (84 tok/s) | **2.31×** (94 tok/s) | **4.62×** (183 tok/s) | 1.44× | only code-edit |
| `ngram-mod` (first run only) | 0.98× | 0.99× | 2.14× | 1.04× | yes |
| `ngram-cache` | 0.99× | 1.00× | 1.00× | 1.01× | yes |

- **DFlash** speeds up generation substantially on this 3060, deterministically (same acceptance in both repetitions; e.g. 298/807 drafted tokens accepted on code-py with n8), more than its author measured on an Apple M4 (+16.8%). But for newly generated code and prose, the greedy output **diverges from the baseline early** (code-py at character 13 with n8). On the copy-heavy edit it is byte-identical.
- **Hypothesis (not tested):** the divergence is numerical, not semantic. Verifying several drafted tokens in one batch uses a different kernel path than one-token decode, and near-tie argmax decisions flip, the same mechanism suspected in B3b (G1). It could also be an issue in llama.cpp's new DFlash path. A quality check (rerun B4's graded tasks with DFlash on) is needed before adopting it.
- **n-gram speculation** only helps when the output copies the input (edits: 2.1×), and is lossless there.
- **Gate:** `dflash-n8` passes the speed criterion (code median 2.31×) but fails "identical output"; `ngram-mod` keeps identical output but its code median is 0.99×. **No arm passes as pre-registered.**

