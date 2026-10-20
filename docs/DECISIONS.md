# Decision log

Newest first. Each entry: date, decision, why, what would change it.

## 2026-10-20 — Library memory = compiled KV packages (v2 passes)
- **Result:** on Ornith 9B, a 14k-token library reference shipped as a KV snapshot on NVMe gave 100% exact match (bare 0%, RAG 100%) with time to first token 0.34 s vs 9.04 s for RAG (×27). Output byte-identical to RAG in 34/40 tasks; the chosen function was identical in 40/40.
- **Decision:** library memory continues as compiled KV packages. The two memories in ARCHITECTURE.md become one mechanism (persistent KV snapshots) with two content types: libraries (shared, community-built) and project context (local).
- **Lesson:** the first B3b run used a raw code-completion prompt in which even RAG failed (18% with a 20-symbol reference). Baselines must be validated before comparing arms.

## 2026-10-20 — Library memory v1 (additive self-encoded vectors) failed; move to KV-based library memory
- **Result:** on the fictional `netkit` library with Qwen3-0.6B, injecting one self-encoded vector per symbol gave 0% exact match on test, identical to the bare model and to the shuffled control, across a 130-configuration dev sweep. The hook was verified active.
- **Decision:** stop this variant. Next: library packages as precompiled KV blocks loaded from NVMe (reusing the B2 mechanism that passed), evaluated on the real core (Ornith 9B via llama.cpp) where RAG is a meaningful baseline.
- **Would change if:** a token-level variant (e.g. injecting at the generation position with retrieval by hidden-state similarity) shows signal over the shuffled control.

## 2026-10-20 — Context memory is prior art: use and measure, don't reinvent
- **Decision:** B2 starts by evaluating existing persistent-KV tools for llama.cpp on the RTX 3060 with Ornith 9B, and contributes upstream where hybrid-model support is broken. The project's original contribution is the library memory and the integration of both memories.
- **Why:** a search found active 2026 work on exactly this (KVMem, CachyLLama, local-llm-kv-cache, pi-kv-cache-manager, the "Agent Memory Below the Prompt" paper, LinearKV for hybrid models) and open llama.cpp issues on hybrid checkpoint persistence. An earlier claim that hybrid models cannot compose cached blocks was wrong (LinearKV).

## 2026-10-20 — Build our own architecture instead of reproducing TF-Engram
- **Decision:** the project builds two memories of its own: **context snapshots on the SSD** and **library memory with self-encoded values**. TF-Engram stops being a reproduction target and becomes prior art and a design reference; the authors' questions remain optional.
- **Why:** (1) the audit shows the paper cannot be reproduced faithfully; (2) self-encoded values (computed by the core model itself) close the gap TF-Engram leaves open, alignment between an external embedder and the backbone; (3) measured prefill on the RTX 3060 (~1,400–1,700 tok/s) against ~0.52 s to load a 50k-token context snapshot from the measured 3.2 GB/s NVMe makes context memory a candidate ~58× gain per agent step, the largest lever found so far.
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
