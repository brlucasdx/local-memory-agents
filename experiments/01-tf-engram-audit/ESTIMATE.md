# Cost estimate for our machine

All values are **[estimate]**, derived from the paper's numbers (RTX 5090 32 GB, i9-14900K 24c/32t, 64 GB RAM) scaled to ours. To be replaced by measurements in phase 2.

## Our machine
- GPU: RTX 3060 12 GB (360 GB/s).
- CPU: AMD Ryzen 7 7700, 8 cores / 16 threads.
- RAM: 30 GB (≈11 GB free during normal use).
- Disk: NVMe, ≈500 GB free.

## Table size and storage
Per entry: 1024-dim FP16 vector = 2 KB (+ metadata). Paper: 100M entries → 215.86 GB.

| Entries | Vectors | Fits where on our machine |
|---|---|---|
| 1M | ~2 GB | entirely in VRAM next to Qwen3-0.6B, or in RAM |
| 10M | ~21 GB | RAM only if almost everything else is closed; realistically SSD + RAM cache |
| 100M | ~216 GB | SSD only (fits in the ~500 GB free) |

Paper result: 1M → 100M moved the average from 58.21 to 59.41, so most of the gain is already present at 1M. **Start with 1M–10M**: it is cheaper and isolates the method from the storage system.

## Construction time (100M entries)
| Step | Paper | Our scaling assumption | Estimate |
|---|---|---|---|
| n-gram extraction (CPU-bound) | 1.612 h | 24c/32t → 8c/16t, ~2–3× slower | ~3–5 h |
| Embedding (GPU) | 0.231 h | 5090 → 3060, ~4–6× slower (A4: verify) | ~1–1.5 h |
| Index build | 0.157 h | CPU/IO | ~0.3–0.5 h |
| **Total** | **2.0 h** | | **~5–7 h** (one night) |

The corpus size is unknown (audit ★1), so these scale with whatever corpus we choose.

## Runtime
- Qwen3-0.6B (~1.2 GB in BF16) + a 1M-entry table fits in 12 GB with room for the KV cache.
- The paper's decode is 2.08 ms/token on a 5090. On a 3060 a 0.6B model is still fast (expect a few ms/token), so the window for hiding SSD latency is **larger** than theirs. For our 9B target (≈26 ms/token at 38 tok/s) it is larger still: favorable for the home-hardware thesis.

## Conclusion
Hardware is not the blocker. The blockers are the unspecified method details in `AUDIT.md`.
