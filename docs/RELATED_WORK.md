# Related work

Abstracts checked on arXiv on 2026-10-19. Full texts not yet read unless noted. Update this file as each paper is read in full.

## Conditional memory and memory layers (the mechanism)
| Paper | Date | Key claim | Code |
|---|---|---|---|
| [Conditional Memory via Scalable Lookup (DeepSeek Engram)](https://arxiv.org/abs/2601.07372) | Jan 2026, rev. Jul 2026 | O(1) n-gram embedding lookup as a second sparsity axis next to MoE; Engram-27B beats an iso-parameter, iso-FLOPs MoE; gains larger in reasoning/code (BBH +5.0, HumanEval +3.0) than knowledge (MMLU +3.4) | [deepseek-ai/Engram](https://github.com/deepseek-ai/Engram) (Apache-2.0): **mocked demo only**, no trained weights |
| [TF-Engram](https://arxiv.org/abs/2607.07388) ([our audit](../experiments/01-tf-engram-audit/AUDIT.md)) | Jul 2026 | Train-free Engram built offline from external corpora; tables across GPU–DRAM–SSD; early-exit guided predictive prefetching; Qwen3-0.6B avg 57.6 → 59.4, above a parameter-matched LoRA | **none found** (no link in PDF, nothing on GitHub) |
| [EngramEdit](https://arxiv.org/abs/2610.10533) | Oct 2026 | Factual edits done only in conditional memory, backbone fixed; near-perfect edit success | not checked |
| [Knowledge Offloading (KOFF)](https://arxiv.org/abs/2605.29075) | May 2026 | Decompose pretrained Llama/Qwen 3–8B into a sparse shared backbone + domain memories (LoRA + learned KV) | not checked |
| [UltraMemV2](https://arxiv.org/abs/2508.18756) | Aug 2025 | Memory layers reach parity with 8-expert MoE at equal compute/params with much lower memory access | not checked |
| [Ultra-Sparse Memory Network (UltraMem)](https://arxiv.org/abs/2411.12364) | Nov 2024 | Large ultra-sparse memory layers | — |
| Memory Layers at Scale (Meta FAIR) | Dec 2024 | Memory layers at scale; strong factual gains | to locate |
| Large Memory Layers with Product Keys (Lample et al.) | 2019 | Product-key memory | — |
| [Memory Grafting: Scaling LM Pre-training via Offline Conditional Memory](https://arxiv.org/abs/2605.20948) | 2026 | Cited by TF-Engram as its Engram-style base [5]; offline conditional memory | to read |
| [Memory Is Not Always Needed](https://arxiv.org/pdf/2608.23982) | Aug 2026 | Characterizes when conditional memory helps in scientific reasoning | to read |
| [re133/sparse-memory-lm](https://github.com/re133/sparse-memory-lm) | — | 21M LM + 16.8M-row product-key memory, table on SSD; unreviewed individual project | yes |

## Offloading and consumer-hardware inference (systems context)
- [PowerInfer](https://ipads.se.sjtu.edu.cn/_media/publications/powerinfer-20231219.pdf): neuron-aware GPU/CPU split based on activation locality.
- [PIPO](https://arxiv.org/pdf/2504.03664): pipelined offloading on consumer devices.
- [Endor](https://arxiv.org/pdf/2406.11674): hardware-friendly sparse format for offloaded inference.
- [SolidAttention (FAST '26)](https://www.usenix.org/system/files/fast26-zheng.pdf): KV cache on SSD for AI PCs.
- [I/O characterization of offloading to NVMe](https://atlarge-research.com/pdfs/2025-cheops-llm.pdf).
- [SSD offloading for MoE considered harmful in energy efficiency](https://arxiv.org/pdf/2508.06978).

## Coding agents and verification (evaluation context)
- [Teaching Agents to Code Reliably](https://arxiv.org/abs/2610.03984) (Oct 2026): self-written tests accept many wrong patches; score patches against their own reverted tree.
- [CARET](https://arxiv.org/abs/2610.04837) (Oct 2026): training-free test-time scaling for repository-level completion with 1–7B models.
- [akitaonrails LLM coding benchmark v4](https://github.com/akitaonrails/llm-coding-benchmark/tree/master/benchmark-v4) and [the B300 open-weights post](https://akitaonrails.com/2026/10/19/llm-benchmark-v4-os-top-llms-open-source-numa-b300/).

## Gap (search not exhaustive)
No work found that (a) evaluates conditional memory in coding agents on executable tasks, (b) compares it to RAG on total wall time on a 12 GB GPU, or (c) distributes it as versioned per-library memory packages.
