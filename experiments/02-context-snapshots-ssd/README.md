# B2 — Context snapshots on SSD

Prefix snapshots for a hybrid model: stable-to-volatile layout, append-only KV log, recurrent-state checkpoints, content-addressed hash chain. See [docs/ARCHITECTURE.md](../../docs/ARCHITECTURE.md#1-context-memory-on-the-ssd).

**Pre-registered gate:** exact-prefix load gives the same logits as recomputation (numerical tolerance to be fixed before running); warm load of a 20–50k-token repository context takes < 10% of the prefill time on the RTX 3060.
