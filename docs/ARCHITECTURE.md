# Architecture: two memories on the SSD

**Status:** design, not built. Markers: **[measured]**, **[published]**, **[estimate]**.

A small coding agent at home hits two walls (see [PROPOSAL.md](PROPOSAL.md)): it doesn't *know* the libraries, and it spends most of each step *re-reading* context. This project builds one memory for each wall, both living on cheap storage instead of VRAM.

| | Library memory | Context memory |
|---|---|---|
| Wall it attacks | invented / outdated APIs | re-reading the repository every agent step (prefill) |
| What is stored | per-symbol hidden-state vectors | the model's own processed context (KV cache + recurrent state) |
| How it is used | injected into the hidden state when a symbol appears; **zero extra tokens** | loaded instead of recomputed |
| Where it lives | RAM / NVMe, hot entries in VRAM | NVMe, current window in VRAM |
| Who builds it | the community (source packages) + the user's machine (compiled packages) | the user's machine, automatically |

---

## 1. Context memory on the SSD

### The numbers that motivate it
- **[measured]** RTX 3060, Ornith 1.5 9B Q6_K: prefill at **1,413 tok/s** (4,770-token prompt) and **1,703 tok/s** (19,134 tokens). A 50k-token agent context therefore costs **~30 s per step** to re-read **[estimate from measured rate]**.
- **[measured]** Ornith architecture (GGUF metadata): 33 blocks, full attention every 4th block (`full_attention_interval = 4`), 4 KV heads × 256-dim keys and values; the other blocks are linear-attention/SSM layers (`ssm.inner_size = 4096`, `ssm.state_size = 128`).
- **[estimate]** KV per token ≈ 8 full-attention layers × 4 heads × (256 + 256) × 2 bytes ≈ **32 KB/token**. Recurrent state ≈ 24 layers × 4096 × 128 × 4 bytes ≈ **~50 MB per snapshot, independent of length**.
- **[measured]** NVMe sequential read on the target machine: **3.2 GB/s** (4 GiB file, `dd` with `iflag=direct`, page cache bypassed).
- **[estimate]** 50k-token snapshot ≈ 1.6 GB KV + 0.05 GB state ≈ **1.65 GB** → **~0.52 s** to load at 3.2 GB/s, against **~30 s** to recompute: **~58× faster per agent step**, before PCIe transfer and deserialization overheads (to be measured in B2).

### Design
Hybrid models (attention + recurrent layers) cannot compose independent per-file blocks: the recurrent state depends on everything before it, in order. So the robust design is **prefix snapshots**, not composition:

1. **Stable-to-volatile layout.** The agent context is assembled in a fixed order: system prompt → library manifest → repository files sorted by stability (least recently edited first) → task and working set last. Typical edits then fall near the tail.
2. **Append-only KV log + periodic state checkpoints.** KV for a prefix is shared by every longer prefix, so it is stored once as an append-only log. Only the recurrent state needs checkpoints (~50 MB each, e.g. at every file boundary).
3. **Content-addressed chain.** Each checkpoint is keyed by a hash chain over the ordered chunks (like a Merkle chain). To resume, find the longest prefix whose hashes still match, load KV up to there plus the state checkpoint, and recompute only the rest.
4. **Persistence across sessions.** Snapshots survive restarts: opening the agent tomorrow on the same repository loads the context in under a second instead of re-reading it.
5. **Correctness check.** Loading an exact prefix must give the same logits as recomputing it (up to numerical tolerance). This is the first gate.

### Prior art to credit and compare against
Prefix caching exists in servers (vLLM, SGLang RadixAttention), with SSD offload in LMCache and in KV-on-SSD work such as SolidAttention (FAST '26). llama.cpp can save and restore a slot to disk. **Our contribution is the agent-aware layout, persistent snapshots for hybrid models on home hardware, and the end-to-end measurement** (time per agent step), not prefix caching itself.

### Research extension (not the first build)
Composable per-file KV with partial recomputation (CacheBlend-style) only works on pure-attention models, and code is less tolerant of approximation than RAG text. It is kept as a later experiment.

---

## 2. Library memory

### Design decision that closes the TF-Engram gap
Our audit found that TF-Engram never explains how a vector from an *external* embedding model becomes a hidden-state update in a *different* backbone without training (audit item ★ injection operator). We avoid the problem:

> **Self-encoded values.** Each API symbol's value is computed by **the core model itself**: run the symbol's documentation snippet (signature + short description) through the frozen core and take the hidden state at the injection layer ℓ. The value already lives in the core's own representation space. No training, no external embedder.

At inference, when the token stream matches a symbol's token prefix, the stored value is added at layer ℓ with a scale α: `h'_ℓ = h_ℓ + α · v_symbol`. ℓ and α are **our choices**, tuned on the development split only.

*(Related ideas: activation steering and hidden-state editing. This is a design hypothesis to be tested, not a claim.)*

### Packages: source and compiled
Self-encoded values are specific to one core model, so a package has two forms, like source and binary packages:

| Form | Contents | Model-specific? | Who makes it |
|---|---|---|---|
| **Source package** | `manifest` (library, version, license), symbol list, one doc snippet per symbol, provenance links | no | the community, reviewed like any open-source package |
| **Compiled package** | the vectors for one core model + layer ℓ, with the model's hash | yes | the user's machine, in minutes, from the source package |

This is what lets the community own it: anyone can write or fix the source package for `rails-8.0` or `rubyllm-1.x`, and everyone compiles it for the model they run.

### Storage
Per symbol: one 4096-dim vector for a 9B core ≈ 8 KB in FP16. A whole library (thousands of symbols) is tens of MB, so it fits in RAM or VRAM. The SSD tier matters only for many libraries or large documentation memories.

---

## 3. Build order and gates

| Step | What | Gate (pre-registered) |
|---|---|---|
| B0 | Measurements: prefill rate ✅, KV bytes/token ✅, NVMe read 3.2 GB/s ✅ | — |
| B1 | Research runtime in PyTorch (Hugging Face Transformers) with a small dense core first (Qwen3-0.6B) for hooks and KV I/O, then Ornith | layer hooks and KV save/load verified |
| B2 | **Context snapshots on SSD** | exact-prefix load gives the same logits; warm load of a 20–50k-token repo context takes **< 10%** of the prefill time |
| B3 | Library memory v0: source format, compiler, injection | on a small dev set, fewer non-existent API calls than the bare core, without lowering test success |
| B4 | API memory vs RAG (the main experiment, 72 tasks × 4 arms) | as in the README |
| B5 | Agent integration (OpenAI-compatible server for the Pi harness): time per agent step, end to end | — |
| B6 | Port to llama.cpp / Ollama | — |
