# Proposal: small reasoning core + sparse memory for coding agents on consumer GPUs

**Author:** Lucas Cruz · **Date:** 2026-10-19 · **Status:** untested proposal. Only items marked **[measured]** were measured.

## 1. Problem

At home, **intelligence already fits, speed does not**, and both are tied to the same resource: the weights read per token.

| Wall | Bound by | Why it hurts at home |
|---|---|---|
| Token generation (decode) | memory bandwidth: tok/s ≈ bandwidth ÷ bytes read per token | a dense 27B at Q4 reads ~16 GB per token |
| Context reading (prefill) | compute | an agent re-reads tens of thousands of tokens every step |

Idealized floors: a dense 35B at 100 tok/s needs ~1.75 TB/s at Q4. A 50k-token prefill in 5 s needs ~700 TFLOP/s effective.

**Evidence**
- **[measured]** RTX 3060 12 GB: Ornith 1.5 9B Q6_K at 38 tok/s (~77% of the 360 GB/s ÷ ~7.3 GB ceiling). Swift 1.5 27B Q4 with CPU offload: 7 tok/s.
- **[published]** akitaonrails LLM coding benchmark v4: Qwen 3.8 27B scored 80.5 on a B300 (192 min) and 80.0 on a home Strix Halo (706 min). The author's advice for consumer GPUs: don't even try.

**Ruled out during design review**
- A faster engine: llama.cpp already reaches ~77% of the physical ceiling, so the upside is ~1.3×.
- Stacking activation sparsity, hot-neuron offload, compression, megakernels and batching: they save the *same* bytes, so the gains don't multiply, and batching erodes sparsity (20% per sequence becomes ~83% across 8 independent sequences).
- MoE with VRAM as an expert cache: at 35 tok/s, PCIe allows ~0.7–0.86 GB per token, against ~1.5 GB read by a 3B-active MoE. Lookahead routing runs into causality.
- Composable per-file KV: a file's KV depends on preceding content, not just position.

## 2. Mechanism

**Separate reasoning from knowledge, and put each on the right hardware.**

- **Reasoning core in VRAM:** a 1–9B model with short reasoning. It thinks and writes code; it doesn't need to memorize APIs.
- **Sparse knowledge memory in RAM/SSD:** conditional-memory tables (Engram-style) or memory layers. Each token reads a few rows.

| | Bytes read per token for knowledge |
|---|---|
| Dense 27B (Q4) | ~16 GB |
| 3B-active MoE (Q4) | ~1.5 GB |
| Sparse memory lookup | ~hundreds of KB, independent of table size |

*(Orders of magnitude, not measurements. On SSD the risk is the p95 latency of many small dependent reads, not bandwidth.)*

## 3. The thesis that is specific to home hardware

On cloud GPUs, prompt tokens are cheap, so RAG is the rational way to inject library knowledge. On a consumer GPU, prefill is the wall, so **every RAG token is paid again at every agent step**. Memory injection adds zero context tokens.

> **Hypothesis:** at equal or better task success, conditional API memory has lower total wall time than RAG on a 12 GB GPU, and the advantage grows with the number of agent steps.

Practical form: **memory packages**, one per library and version (`rails-8.0`, `rubyllm-1.x`), built from the real docs and pluggable without retraining. This also covers APIs released after the training cutoff.

## 4. Where it can break

1. **Semantic integration:** retrieving the right row doesn't guarantee a frozen core will *use* it to emit the exact signature. Rare identifiers, fragmented tokenization, overloads and versions demand precision.
2. **Scale transfer:** TF-Engram was shown on Qwen3-0.6B. Nothing guarantees 9B.
3. **SSD latency:** many small random reads per token. Measure p95, cache misses and prefetch cost before claiming anything.
4. **No public code:** TF-Engram has no released implementation, and DeepSeek's Engram repo ships only a mocked demo, so this requires a careful reimplementation.
5. **Project memory** (a repository as editable memory) is not demonstrated by any technique we know. It starts as a symbol/AST index plus lexical search.

## 5. Evaluation design (summary)

- **Phase 3 (reproduction):** Qwen3-0.6B frozen; paired differences; stratified bootstrap confidence intervals. Detecting small effects needs many items (≈9,700 items for +0.9 pp at 80% power with 10% discordance).
- **Phase 4 (application):** 12 dev and 60 blind tasks over 20 APIs of one version-pinned library, with independent hidden tests. Tasks, solutions and tests never enter any memory. Four arms: bare core, lexical RAG over the same docs, conditional memory, shuffled memory (control). Metrics: test success, non-existent or incompatible API calls, total wall time, tok/s, VRAM/RAM, memory build cost.
- **Continue if:** API errors drop ≥30% relative and success rises ≥10 pp over the bare core; versus RAG, success is equal or better with ≥15% less total wall time.
