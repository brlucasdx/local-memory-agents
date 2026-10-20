# Phase 1 — TF-Engram reproducibility audit

**Paper:** Ma, Huang, Jiang, Shao. *TF-Engram: A Train-Free Engram with SSD-Backed Memory for Large Language Models.* arXiv 2607.07388 (Jul 2026). Local copy: `refs/2607.07388-tf-engram.pdf`.
**Known so far:** no public code (no link in the PDF, nothing on GitHub as of 2026-10-19); evaluated only on Qwen3-0.6B (avg 57.6 → 59.4).

## Pre-registered gate
- **CONTINUE** if every item marked ★ below is specified (or recoverable from cited work) and the RAM/disk/time estimate fits an RTX 3060 + 30 GB RAM.
- **STOP faithful reproduction** if any ★ item is missing and the authors don't answer within 2 weeks. Publish the gap list as the phase result.

## Extraction checklist
For each item: page/section, exact value or "not specified", and how decisive it is.

### Memory construction
- [ ] ★ Source corpus (which, size, preprocessing)
- [ ] ★ Key definition (phrase segmentation, n-gram order, tokenization handling)
- [ ] ★ Value definition (how the hidden-state vectors are computed offline, from which layer)
- [ ] Deduplication / collision handling (the paper criticizes hash collisions)
- [ ] Table size (entries, dimensions, dtype, bytes on disk)
- [ ] Offline build cost (time, hardware)

### Injection
- [ ] ★ Which layer(s) receive the memory
- [ ] ★ Injection operator (add, gate, projection, normalization)
- [ ] ★ Lookup at inference (how the current phrase is matched; exact vs fuzzy)
- [ ] Any learned parameters at all (train-free claim: confirm nothing is trained)

### Systems
- [ ] GPU–DRAM–SSD placement policy
- [ ] Early-exit guided predictive prefetching (which early layer, prediction rule, prefetch window)
- [ ] Reported throughput with and without prefetch

### Evaluation
- [ ] ★ Benchmarks list and the exact averaging behind 57.6 / 59.4
- [ ] ★ Prompting / few-shot / decoding settings
- [ ] Seeds, variance, confidence intervals (if any)
- [ ] LoRA baseline configuration (parameter-matched how?)

## Outputs of this phase
- `AUDIT.md`: filled checklist with page references.
- `QUESTIONS_FOR_AUTHORS.md`: concrete open questions (sent by e-mail; log date and reply).
- `ESTIMATE.md`: RAM/disk/time estimate for the 3060.

## Result (2026-10-20)
- **Gate: STOP faithful reproduction (pending authors).** 6 of 10 decisive items are unspecified, including the injection layer and how external embeddings become hidden-state updates without training. Internal inconsistency A1: the early-exit layer changes accuracy although the paper says the prefetch head cannot change outputs.
- Details: [AUDIT.md](AUDIT.md) · cost on our machine: [ESTIMATE.md](ESTIMATE.md) · questions: [QUESTIONS_FOR_AUTHORS.md](QUESTIONS_FOR_AUTHORS.md) (draft, not yet sent).
