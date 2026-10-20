# B3b — Library memory v2: compiled KV packages

**Idea:** a library package is the documentation's **KV cache**, compiled once per model and loaded from the SSD at the stable top of the context (the B2 mechanism, which passed). The model attends to the real documentation text, so the information equals RAG **by construction**; what changes is the cost.

## Pre-registration (written 2026-10-20, before any run)

- **Core:** Ornith 1.5 9B Q6_K on llama.cpp v0.7.0 (RTX 3060), `-c 32768 -ctk q8_0 -ctv q8_0 -fa on -np 1`, greedy, 12 new tokens, raw completion (no chat template).
- **Library:** fictional `netkit` 0.2.0, 500 symbols (the 20 task symbols + 480 generated decoys from the same domain, `tools/gen_netkit_large.py`, seed 20261020), ~12k tokens of reference.
- **Tasks:** all 40 tasks of `bench/tasks/netkit-0.1.json` (dev + test). There are no hyperparameters to tune in this variant, so all 40 are evaluation.
- **Prompt:** the B3 code-completion prompt (`import netkit` → reference block as comments → `# <task>` → `result = netkit.`).
- **Arms:**
  | Arm | What happens per task |
  |---|---|
  | `bare` | prompt without the reference |
  | `rag` | reference in the prompt, **slot erased before each task** (full prefill: a new session with RAG) |
  | `kvpack` | slot erased, **compiled package restored from NVMe** (page cache evicted), then the same prompt; only the tokens after the reference are processed |
- **Metrics:** exact match of the identifier after `netkit.`; rate of invented names (predicted name not in the library); time to first token (restore + prompt processing); tokens actually processed.

### Gates
- **G1 correctness:** `kvpack` output byte-identical to `rag` for all 40 tasks.
- **G2 usefulness:** `rag` exact match ≥ `bare` + 50 pp.
- **G3 cost:** mean `kvpack` time to first token ≤ 10% of `rag`'s.

All three must hold to call the variant a success.

## Protocol amendment 1 (2026-10-20, after the first run, before the second)

**What changed:** the prompt format, from raw code completion (`result = netkit.`) to Ornith's own chat template: the reference goes in the system message, the task in the user message ("Reply with only the netkit function call"), thinking disabled, 24 new tokens. The KV package becomes the rendered prefix up to the end of the system message. Arms, metrics and gates are unchanged.

**Why:** in the first run the **RAG baseline itself failed**: 7.5% exact match with the 500-symbol reference, and a diagnostic with only the 20-symbol reference (~600 tokens) still gave **18%**. The model mostly emitted the **first function listed** (`arp_trace`, position 0 of 500), so the code-completion format does not make a chat/reasoning model consult a reference at all. That run measured the prompt format, not the memory. With the chat format, the same 20-symbol diagnostic gave **0/40 without the reference and 40/40 with it**.

**First-run numbers, kept as raw data** (`results/rejected-prompt-format/`): bare 0%; rag 7.5%; kvpack 10%; kvpack time to first token 0.34 s vs rag 9.40 s (×28) for a 14,673-token reference packaged in 0.41 GB; kvpack output byte-identical to rag in 32/40 tasks.

## Results (2026-10-20, chat format) — G2 and G3 PASSED, G1 failed strictly

Ornith 1.5 9B Q6_K, llama.cpp v0.7.0, RTX 3060, 32k context, q8 KV. Reference: 14,184 tokens (500 symbols). Compiled package: **0.41 GB, built in 8.9 s**. Raw data in `results/`.

| Arm | Exact match (40 tasks) | Invented names | Time to first token | Tokens processed |
|---|---|---|---|---|
| bare | 0% | 62.5% | 0.08 s | 45 |
| rag (reference in the prompt, new session) | **100%** | 0% | **9.04 s** | 14,229 |
| **kvpack (package restored from NVMe)** | **100%** | **0%** | **0.34 s** | 45 |

- **G2 usefulness: PASSED.** rag 100% vs bare 0% (+100 pp). Without the reference the model invents plausible names (`list_lldp_neighbors`, `find_vendor_by_mac`, `get_path_mtu`); with it, it picks the right function among 500, including near-duplicates (`vrx_audit`, `vrx_pin`, … around `vrx_unfold`).
- **G3 cost: PASSED.** kvpack time to first token = 3.8% of rag's (**×27**), with the same accuracy.
- **G1 byte-identical output: FAILED strictly (34/40).** The **function chosen is identical in 40/40**. The 6 differences are only in the arguments: quote style (`"…"` vs `'…'`), `switch="VLAN10"` vs `switch, vlan=10`, and an example IP. Hypothesis (not yet tested): llama.cpp is not batch-invariant. In rag the task tokens are computed in the same batch as the 14k-token reference; in kvpack they are computed alone after the restore, so near-tie decisions can flip. B2's identical outputs at every size do not contradict this, because that test had no near ties.

**Conclusion:** a library package as a compiled KV cache gives RAG's accuracy at ~4% of RAG's latency on a 12 GB GPU. Library memory and context memory turn out to be **the same mechanism** (persistent KV snapshots on NVMe) applied to two kinds of content.

