# Decision log

Newest first. Each entry: date, decision, why, what would change it.

## 2026-10-20 — Build our own architecture instead of reproducing TF-Engram
- **Decision:** the project builds two memories of its own: **context snapshots on the SSD** and **library memory with self-encoded values**. TF-Engram stops being a reproduction target and becomes prior art and a design reference; the authors' questions remain optional.
- **Why:** (1) the audit shows the paper cannot be reproduced faithfully; (2) self-encoded values (computed by the core model itself) close the gap TF-Engram leaves open, alignment between an external embedder and the backbone; (3) measured prefill on the RTX 3060 (~1,400–1,700 tok/s) against an estimated ~0.25–0.55 s to load a 50k-token context snapshot from NVMe makes context memory a candidate ~55–120× gain per agent step, the largest lever found so far.
- **Would change if:** B2 shows snapshot loads are not much faster than recomputation on real hardware, or that exact-prefix reuse does not reproduce the logits.

## 2026-10-20 — Phase 1 gate: stop faithful reproduction, ask the authors
- **Decision:** do not start a "reproduction" until the authors answer (2-week window). Questions drafted in `experiments/01-tf-engram-audit/QUESTIONS_FOR_AUTHORS.md`.
- **Why:** the audit found 6 of 10 decisive items unspecified (injection layer, embedding-to-hidden alignment, matching rule, phrase mining, evaluation protocol, LoRA baseline) and one internal inconsistency (accuracy varies with the early-exit layer).
- **Would change if:** the authors answer or release code. If not: either a best-effort reimplementation with every choice labeled as ours, or a systems-only reproduction.

## 2026-10-20 — What is public
- **Decision:** only the English material is published. Portuguese working notes, career planning and design-review transcripts stay local.

## 2026-10-20 — Project structure and public language
- **Decision:** public docs in English (`README.md`, `docs/*.md`); working docs in Portuguese (`docs/pt/`).
- **Why:** the project doubles as an international portfolio; the author's working language is Portuguese.

## 2026-10-19 — Reproduce TF-Engram (path R) instead of training memory (path T)
- **Decision:** reimplement TF-Engram from the paper on Qwen3-0.6B on the RTX 3060.
- **Why:** it answers the question that matters for off-the-shelf models (train-free) and needs no rented GPU. A failed reproduction does not kill the train-free line (it may be a spec, implementation or evaluation gap), and training answers a different question.
- **Would change if:** the audit (phase 1) shows the paper underspecifies decisive choices.

## 2026-10-19 — Position as application + measurement, not a new mechanism
- **Decision:** the claimed contribution is conditional memory in coding agents on a 12 GB GPU, against RAG on total wall time, plus versioned memory packages.
- **Why:** prior art (DeepSeek Engram, TF-Engram, EngramEdit, KOFF, UltraMemV2) already establishes the mechanism.

## 2026-10-19 — Ruled out as main track
- **Better inference engine in C++:** llama.cpp already reaches ~77% of the bandwidth ceiling on the 3060; upside ~1.3×.
- **Integrated sparsity/offload/compression/megakernel/batching engine:** the gains save the same bytes; batching erodes sparsity.
- **MoE with VRAM as an expert cache:** the PCIe budget (~0.7–0.86 GB/token at 35 tok/s) is below the ~1.5 GB/token read by a 3B-active MoE; lookahead routing runs into causality.
- **Composable per-file KV:** a file's KV depends on preceding content.
- These remain as side tracks in `docs/pt/PLANO-DE-PESQUISA.md` where a cheap measurement could still be informative.

## 2026-10-19 — Reasoning effort `low` as default for local agent runs
- **Why:** one bug, n = 1 per arm. `low` solved it on the first try in 2 min 13 s; `medium` took 4.5 min with two wrong attempts. Not yet statistically supported (see side track T-A).
