# Phase 0 — Local baseline (2026-10-19)

All numbers **[measured]** on the author's machine unless marked otherwise. n = 1 where noted; treat as exploratory.

## Hardware and software
- GPU: NVIDIA GeForce RTX 3060, 12 GB GDDR6, 192-bit, 360 GB/s (spec).
- RAM: 30 GB. OS: Debian 13 (Linux 6.12).
- Ollama 0.33.2 (llama.cpp backend). Harness: Pi 1.3.0 (`@earendil-works/pi-coding-agent`), Node 22.23.3.

## Models
| Model | Source | Quant | Fit | Decode |
|---|---|---|---|---|
| Ornith 1.5 9B (`ornith-code`) | `hf.co/ornith-ai/Ornith-1.5-9B-GGUF:Q6_K` | Q6_K, 8.5 GB file (~7.3 GB text weights, rest is vision projector) | 100% GPU, num_ctx 32768 | **38.0 tok/s** (400 tokens, think off); prompt ~282 tok/s on a short prompt |
| Swift 1.5 27B | `hf.co/ukisai/Swift-1.5-Qwen3.8-27B-GGUF:Q4_K_M` | Q4_K_M, 17.4 GB | GPU + CPU offload | **7.02–7.15 tok/s** (Ollama `--verbose`) |

Bandwidth ceiling for Ornith 9B: 360 GB/s ÷ ~7.3 GB ≈ 49 tok/s → measured 38 tok/s ≈ **77%** of the ceiling **[estimate]**.

Ornith settings (`ornith-code` Modelfile): temperature 0.6, top_p 0.95, top_k 20, min_p 0, num_ctx 32768 (the card's "precise coding" recommendation).

## Prefill (2026-10-20)
| Model | Prompt tokens | Prefill time | Rate |
|---|---|---|---|
| Ornith 1.5 9B Q6_K | 4,770 | 3.4 s | **1,413 tok/s** |
| Ornith 1.5 9B Q6_K | 19,134 | 11.2 s | **1,703 tok/s** |

Ollama `/api/generate`, `num_predict 1`, think off, num_ctx 32768, repeated Python code as the prompt.

## Storage (2026-10-20)
- NVMe sequential read: **3.2 GB/s** (4 GiB of random data, `dd bs=16M iflag=direct`, page cache bypassed).

## Swift 27B, chat (Ollama CLI, no harness)
| Task | Thinking | Total | Tokens | Result |
|---|---|---|---|---|
| Fix `media()` (5 constraints, 4 asserts) | on | 66.4 s | 452 | correct |
| same | off (`/set nothink`) | 18.1 s | 106 | correct |
| `agrupar_por()` (6 constraints) | off | 27.4 s | 186 | correct (order assert weak) |
| `calcular_sla()` simple (8 rules) | off | 71.6 s | 501 | correct on all 8 rules; dead code |
| `calcular_sla()` hard (maintenance, dependencies, TZ, cycles) | off | 4 min 3 s | 1673 | **truncated**: 2423 prompt + 1673 output = 4096 = num_ctx |

## Ornith 9B in the Pi harness: planted one-line bug
Target: a private network-automation codebase (Huawei VRP configuration parser), function that expands VLAN ranges such as `2 to 10`; one line changed from `range(start, end + 1)` to `range(start, end)`. The codebase is not public; the bug class (inclusive range off-by-one) is what matters. Symptom-only report ("`allow-pass vlan 100 to 110 200` arrives without VLAN 110"), asking to reproduce first, apply a minimal fix and prove it.

| Arm | Wall | Thinking chars | Outcome |
|---|---|---|---|
| Pi + `medium` (session `01a155bc…`) | ~4.5 min | ~15k | reproduced first ✅; **1st edit wrong** (line 202, a no-op equivalent condition, contradicting its own repro output); 2nd wrong guess (blamed `__pycache__`); then fixed correctly. +1 extra comment |
| Pi + `low` (session `01a155ca…`) | **2 min 13 s** | ~9.7k | reproduced first ✅; **fixed on first edit** ✅; 5 tool calls; +2 extra comments (one nonsensical) |

n = 1 per arm.

## Harness overhead
- Pi: system prompt ~22k chars; "oi" end-to-end **6.5 s**.
- OpenCode 1.18.34 with the same model: loaded 47 skills from `~/.claude/skills` + a 12 KB project CLAUDE.md; the user gave up before the first reply. Not measured further.
