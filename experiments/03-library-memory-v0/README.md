# B3 — Library memory v0

Source package format, compiler (self-encoded values from the frozen core) and injection `h'_ℓ = h_ℓ + α·‖h_ℓ‖·v/‖v‖`. See [docs/ARCHITECTURE.md](../../docs/ARCHITECTURE.md#2-library-memory).

## Pre-registration (written 2026-10-20, before any run)

**Question:** can a train-free, self-encoded hidden-state injection make a frozen core name an API it has never seen?

- **Library:** `netkit` 0.1.0, **fictional** (`packages/source/netkit-0.1/package.json`): 20 symbols with deliberately non-guessable names (e.g. `vrx_unfold`, `oui_owner`). No model can know them from training, so any success comes from the memory.
- **Tasks:** `bench/tasks/netkit-0.1.json`: 2 phrasings per symbol. `dev` (20) is used to choose the configuration; `test` (20) is run **once** with the frozen configuration. Each task contains one of the symbol's key phrases (TF-Engram-style phrase trigger).
- **Prompt (code completion, no chat template):**
  ```
  import netkit

  # <task>
  result = netkit.
  ```
- **Core models:** Qwen3-0.6B first (mechanism check), then a larger Qwen3 if it fits comfortably.
- **Arms:**
  | Arm | What the model sees |
  |---|---|
  | `bare` | the prompt only |
  | `rag` | the 20 doc lines as comments before the task (upper bound; costs prompt tokens) |
  | `mem` | the prompt only + injection of the matched symbol's value |
  | `mem_shuf` | same as `mem` but each symbol gets another symbol's value (control: injection without the right information) |
- **Metric:** exact match of the generated identifier after `netkit.` (greedy, 12 new tokens). Secondary: mean log-probability of the gold name tokens; prompt tokens per arm.
- **Tuned on dev only:** layer ℓ, scale α ∈ {0.25, 0.5, 1, 2, 4}, value type (last token / mean of the doc line).

### Gate
- **CONTINUE** (the mechanism carries information) if on **test**: `mem` exact match ≥ `bare` + 25 pp **and** `mem` − `mem_shuf` ≥ 20 pp.
- **STOP this variant** otherwise. A single additive vector per symbol is then insufficient, and the next variant is library memory as **precompiled KV blocks** (docs' KV cached on SSD and attended to: zero prefill cost, RAG-level information).
- `rag` is reported as the reference ceiling, not as a competitor in this micro-test.

## Results (2026-10-20) — gate FAILED: variant 1 stopped

**Core:** Qwen/Qwen3-0.6B, BF16, transformers 5.20.2, torch 2.14.1+cu130, RTX 3060. Compiling the package (20 symbols, all layers) took 0.4 s.

**Dev sweep** (13 layers × 5 scales × 2 value types = 130 configurations): no configuration produced a single exact match, and `mem` was indistinguishable from `mem_shuf` in every one.

| Split | Arm | Exact match | Mean gold log-prob | Prompt tokens |
|---|---|---|---|---|
| dev | bare | 0% | −8.26 | 24 |
| dev | rag | 15% | −2.88 | 625 |
| dev | mem (best: ℓ=4, α=1, mean) | 0% | −8.17 | 24 |
| dev | mem_shuf (same config) | 0% | −8.17 | 24 |
| **test** | bare | 0% | −7.90 | 22 |
| **test** | rag | 20% | −2.98 | 623 |
| **test** | **mem (frozen ℓ=4, α=1, mean)** | **0%** | **−7.90** | 22 |
| **test** | mem_shuf | 0% | −7.91 | 22 |

**The injection was active, not a bug:** every task matched 2–4 key-phrase positions, and larger scales moved the model (gold log-prob from −8.2 down to −10.1 at α=4; predictions changed to invented names such as `ctl` and `arp_query`). The added vector changes behavior but carries no recoverable information about *which identifier* to emit.

**Gate:** `mem` ≥ `bare` + 25 pp → 0 vs 0 ✗; `mem` − `mem_shuf` ≥ 20 pp → 0 ✗. **Variant 1 (one self-encoded additive vector per symbol) is stopped.**

**Caveats:**
- A 0.6B core is weak even with the docs in the prompt (RAG 15–20% exact match, although the gold log-prob jumps from −8 to −3). A larger core was not tested because `mem` showed **zero** signal over `mem_shuf`, even in log-probability, so there is nothing for scale to amplify.
- Interpretation (hypothesis): a single residual vector can nudge a concept, but an unseen identifier must be spelled token by token, and that needs token-level information (attention over the actual text), not a direction in hidden space.

**Next variant (as pre-registered):** library memory as **precompiled KV blocks**: the documentation's KV cache, built once per model and loaded from the SSD (the B2 mechanism, which passed). Information content equals RAG by construction; the claim to test becomes cost: RAG-level accuracy with near-zero prefill.
