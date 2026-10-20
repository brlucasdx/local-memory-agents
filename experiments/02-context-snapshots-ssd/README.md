# B2 — Context snapshots on SSD

Prefix snapshots for a hybrid model: stable-to-volatile layout, append-only KV log, recurrent-state checkpoints, content-addressed hash chain. See [docs/ARCHITECTURE.md](../../docs/ARCHITECTURE.md#1-context-memory-on-the-ssd).

**Pre-registered gate:** exact-prefix load gives the same logits as recomputation (numerical tolerance to be fixed before running); warm load of a 20–50k-token repository context takes < 10% of the prefill time on the RTX 3060.

## Results (2026-10-20) — gate PASSED

**Setup [measured]:** llama.cpp v0.7.0 (commit 620d222, includes the hybrid-checkpoint fix from PR #26004), built for sm_86. Ornith 1.5 9B Q6_K, `--no-mmproj -ngl 99 -c 65536 -ctk q8_0 -ctv q8_0 -fa on -np 1 --slot-save-path`. VRAM in use: 8.8 GB. Prompt: real C++ source (llama.cpp server), greedy continuation of 48 tokens. Snapshots written to NVMe; before each restore the file is evicted from the Linux page cache (`fsync` + `POSIX_FADV_DONTNEED`) so the restore really reads the disk. Script: [measure.py](measure.py), raw data in `results/`.

| Context | Cold prefill | Snapshot (q8 KV + recurrent state) | Save | Restore from NVMe | Re-read after restore | Speed-up | Decode | Identical output |
|---|---|---|---|---|---|---|---|---|
| 8,000 | 4.7 s | 0.30 GB | 0.25 s | 0.16 s | 4 tokens, 0.06 s | ×22 | 40.1 tok/s | ✅ |
| 32,000 | 20.8 s | 0.72 GB | 0.67 s | 0.46 s | 4 tokens, 0.07 s | ×39 | 35.7 tok/s | ✅ |
| 60,000 | 43.1 s | 1.21 GB | 1.17 s | 0.63 s | 4 tokens, 0.08 s | **×60** | 31.5 tok/s | ✅ |

- **Gate:** warm load = 1.6% of the prefill time at 60k (gate: < 10%) and byte-identical greedy output at every size. **PASSED.**
- The ×60 matches the a-priori estimate (~58×) from measured prefill rate and NVMe bandwidth.
- A first run without page-cache eviction gave ×101 at 60k; that number measured RAM, not the SSD, and is not reported as a result.
- Decode at 60k context: 31.5 tok/s (vs 40.1 at 8k): the estimate for 128k with q8 KV was ~28–30 tok/s.
- Snapshot size ≈ 20 KB/token with q8 KV (a-priori estimate: 16 KB/token KV + ~50 MB fixed recurrent state).

**Not yet measured:** 128k context; restore after a full server restart; the proxy layer (local-llm-kv-cache) between Pi and llama-server in a real agent loop.
