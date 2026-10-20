# TF-Engram reproducibility audit

**Paper:** Yutang Ma, Kecheng Huang, Xikun Jiang, Zili Shao. *TF-Engram: A Train-Free Engram with SSD-Backed Memory for Large Language Models.* arXiv:2607.07388v1 [cs.CL], 8 Jul 2026, 13 pages.
**Audited:** 2026-10-20, full text (v1). **Code:** none public as of 2026-10-19 (no link in the PDF, no GitHub repository found).
**Auditor:** Lucas Cruz

Section references are to the arXiv v1 PDF. "Not specified" means the information is absent from the text; some may be in figures whose values did not survive text extraction, and those are marked as such.

---

## Verdict

**Faithful reproduction is not possible from the paper alone.** 6 of the 10 decisive (★) items are unspecified, including the two that define the method: **where** the memory is injected and **how** an external embedding vector becomes a hidden-state update without training.

There is also an **internal inconsistency** (A1 below): the paper states the prefetch head never changes the model's output, yet reports that the early-exit layer position changes the downstream accuracy.

**Gate outcome (pre-registered in README.md):** STOP faithful reproduction → send questions to the authors and wait 2 weeks. A *best-effort reimplementation*, explicitly labeled as such, remains possible, but its result would not confirm or refute the paper.

---

## Checklist

### Memory construction
| Item | Status | What the paper says | § |
|---|---|---|---|
| ★ Source corpus | **partial** | Mixture of FineWeb-Edu, Wikipedia, C4 English, arXiv and PubMed. **No sizes, proportions, versions or subsets.** | 5.1 |
| ★ Key definition (phrase mining) | **not specified** | Candidates are "bigrams, trigrams, named entities, technical terms…", which "can be selected using frequency thresholds, statistical association, named-entity recognition, or corpus-specific filters". A menu of options, not the method used: no n-gram order range, thresholds or NER model. | 4.2 |
| Tokenization filter | not specified | Filters "unstable tokenization, excessive length, or low corpus support". No thresholds. | 4.2 |
| ★ Value definition | **partial** | `e_i = E(φ_i)`, a frozen Qwen3-Embedding of the phrase string. **Model size not stated.** The storage figure (100M entries → 215.86 GB with 1024-dim FP16) implies 1024 dimensions, consistent with Qwen3-Embedding-0.6B *(our inference)*. | 4.2, 5.3 |
| Collision handling | specified | No hashing. One logical entry per phrase; two-level index `token prefix → phrase id → memory address`. | 4.2 |
| Table size | specified | 1M to 100M entries; 100M is the main configuration. | 5.3, 5.4 |
| Offline build cost | specified | 100M entries ≈ 2.0 h: n-gram extraction 1.612 h, embedding 0.231 h, indexing 0.157 h, on an i9-14900K + RTX 5090. | 5.3 |

### Injection (the core of the method)
| Item | Status | What the paper says | § |
|---|---|---|---|
| ★ Injection layer(s) | **not specified** | Nothing says which layer(s) receive the memory. | — |
| ★ Injection operator / space alignment | **not specified** | Only the generic `h' = h + g·m` of Engram-style memory, where the gate "may be a scalar, a vector, or a learned function". The values come from a **different model** (Qwen3-Embedding) than the backbone (Qwen3-0.6B). The paper never explains how a vector from that space becomes a meaningful update to the backbone's hidden state **without training**. Both happen to be 1024-dim, but equal dimensionality is not a shared space. A "memory injection scale" is varied in §5.4 (Fig. 6), but its value is not stated in the text. | 2.2, 4.1, 5.4 |
| ★ Lookup at inference | **not specified** | Longest match, with ties broken by "frequency, semantic confidence, or corpus priority". Whether the matched phrase must **end at** the current token or can extend past it is unclear ("token prefixes or suffix candidates"). Aggregation weights α are "determined by phrase length, frequency, or confidence", with no formula. | 4.2 |
| ★ Is anything trained? | **ambiguous** | The prefetch head is train-free (a "frozen projection derived from the backbone", presumably the LM head on an intermediate state) **or** "lightly calibrated" (`W_pref` trained on unlabeled text). **Which one the experiments use is not stated.** | 4.4 |

### Systems
| Item | Status | What the paper says | § |
|---|---|---|---|
| Placement policy | partial | GPU hot / DRAM warm / SSD full table; ranking by "access frequency, recency, phrase length, domain priority, and prefetch confidence". No policy, cache sizes or eviction rule. | 4.3, 5.1 |
| Prefetch head position | specified (with a contradiction) | Described as "near the end of the LLM" (layer L − r). The best result uses **layer 8**, which is roughly the first third of Qwen3-0.6B's 28 layers *(layer count from the Qwen3 report, not this paper)*. | 4.4, 5.4 |
| Prefetch budget | specified | Top-16 / 64 / 128 evaluated; Top-64 is the main setting. Priority `s = p·r·c`, but r and c are not defined numerically. | 4.4, 5.3 |
| Throughput / latency | specified | Baseline 2.08 ms/token. SSD without prefetch: 481.2 → 439.2 tok/s. Top-64: 460.3. Top-128: 462.4. GPU-resident 10M table: 24.03 GB VRAM. SSD-backed 100M table: 3.06 GB VRAM. | 5.3 |

### Evaluation
| Item | Status | What the paper says | § |
|---|---|---|---|
| ★ Benchmarks and averaging | **partial** | 10 benchmarks (MMLU, ARC-C, HellaSwag, PIQA, WinoGrande, BoolQ, OpenBookQA, SciQ, TruthfulQA-MC2, LAMBADA), unweighted mean. | 5.1, Table 3 |
| ★ Prompting / shots / harness / metric | **not specified** | No evaluation harness, few-shot count, prompt template or metric variant (e.g. acc vs acc_norm). | — |
| Seeds / variance / CIs | not specified | Single numbers; no variance reported. | Table 3 |
| ★ LoRA baseline | **not specified** | "Comparable trainable-parameter budget". TF-Engram is train-free, so what parameter count is matched is unclear. No LoRA rank, training data or steps. | 5.1, 5.2 |

---

## Anomalies

**A1 — Early-exit position changes accuracy, which the design says it cannot.**
§4.4: the early-exit head "affects only prefetch scheduling and does not change the final token probabilities". §5.4: varying the early-exit layer changes the **average score**, with layer 8 best at 59.4092. Both cannot be true unless a prefetch miss makes the system **skip** the memory injection, or some other undocumented timing-dependent path exists. If skipping on a miss is the behavior, accuracy depends on hardware speed and becomes non-deterministic across machines. **This is the single most important question for the authors.**

**A2 — "Near the end" vs layer 8.** The design motivates a head near the last layers (§3.2, §4.4), but the best configuration exits early in the network. Not necessarily wrong, but the latency-hiding argument changes: the hiding window becomes most of the forward pass.

**A3 — Backbone scores are suspiciously round.** 9 of the 10 Qwen3-0.6B scores in Table 3 end in ".0" (53.7 is the exception), while the LoRA and TF-Engram columns carry one non-zero decimal. This may be rounding or values copied from another source, but it matters for a 1.8-point claim.

**A4 — Embedding throughput.** 100M phrases embedded in 0.231 h implies ~120k phrases/s on one RTX 5090. Plausible only for very short inputs, a small encoder and large batches. Worth confirming when estimating our cost.

**A5 — Lost values.** Several percentages in §5.3 and §5.4 did not survive text extraction (e.g. "3.83", "9.57", "1.12", "3.20" without their units or context). Read them from the figures before citing.

---

## What *is* reproducible today
- The **systems** side (tiered storage, early-exit prefetch with Top-K, ms/token and VRAM measurements) can be rebuilt and measured independently of the quality claim.
- A **best-effort quality reimplementation** must choose: injection layer(s), the alignment from embedding space to hidden space (e.g. a fixed scale, or a train-free mapping), the matching rule and the evaluation harness. Each choice must be documented as **ours, not the paper's**.

## New related work found in the references
- [5] Runxi Cheng et al., *Memory Grafting: Scaling Language Model Pre-training via Offline Conditional Memory*, arXiv:2605.20948 (2026). Not yet in our RELATED_WORK, to read: "offline conditional memory" is close to our construction step.

## Next actions
1. Send `QUESTIONS_FOR_AUTHORS.md` (draft ready, **not sent**).
2. Read Fig. 6 values for the injection scale and early-exit sweeps.
3. If no answer in 2 weeks: decide between a documented best-effort reimplementation and the systems-only reproduction.
