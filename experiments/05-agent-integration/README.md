# E5 — Agent integration: library package + context snapshots in a real coding agent

**Question:** inside a real agent loop (Pi harness, Ornith 9B, RTX 3060), does the library reference make the agent write code that runs, and do SSD snapshots cut the cost of starting sessions?

## Pre-registration (written 2026-10-20, before any run)

- **Stack:** Pi 1.3.0 → (optional) `local-llm-kv-cache` proxy (golden shared prefix + session snapshots, `SAVE_POLICY=terminal`) → llama.cpp v0.7.0 `llama-server` (`-c 49152 -ctk q8_0 -ctv q8_0 -fa on -np 1 --metrics --slot-save-path`, same dir as the proxy cache) → Ornith 1.5 9B Q6_K. Pi model `…/ornith:low` (reasoning effort low), `-p -nc`.
- **Library:** fictional `netkit` 0.2.0 (500 symbols). The reference (~14k tokens) enters the **system prompt** through `--append-system-prompt`, so it is part of the stable prefix that gets snapshotted.
- **Executable grading:** `bench/agent/netkit_stub/netkit.py` (generated) implements every documented function and logs each call; any invented name raises `AttributeError`. After each session the grader runs `python3 check.py` itself.
- **Tasks:** 6 tasks in `bench/agent/tasks.json` ("write check.py that uses netkit to <goal> and run it"), one per gold function. Workdir is a fixed path, reset before every session (so the prompt prefix is stable).
- **Arms:**
  | Arm | Path | Before each session | Library in prompt |
  |---|---|---|---|
  | `cold` | Pi → llama-server | slot erased (fresh start: full prefill) | yes |
  | `ssd` | Pi → proxy → llama-server | slot erased; the proxy restores the golden prefix from NVMe | yes |
  | `ram` | Pi → llama-server | nothing (llama.cpp's own in-memory prefix reuse; best case while the server stays up) | yes |
  | `nolib` | Pi → llama-server | nothing | **no** (the agent may still inspect `netkit.py` with its tools) |
  `ssd` gets one untimed warm-up session (task `vrf_list`) to publish the golden snapshot.
- **Metrics per session:** success (grader run exits 0 **and** the gold function is called); wall time; prompt tokens actually processed by llama-server (`/metrics` counter delta); number of agent tool calls.

### Gates
- **G1 library helps the agent:** success(`ssd`) ≥ success(`nolib`) + 30 pp, *or* equal success with ≥ 30% less median wall time than `nolib`.
- **G2 snapshots cut session cost:** median prompt tokens processed per session in `ssd` ≤ 25% of `cold`, **and** median wall time `ssd` < `cold`.
- **G3 no quality loss:** success(`ssd`) ≥ success(`cold`) − 1 task.

## Protocol note
The first smoke-test session was graded as a failure by a grader bug (`python3 -I check.py` cannot import the `netkit.py` next to the script). The agent's code was correct; the grader was fixed to `python3 -s` before the real run. The smoke test is not part of the results.

## Results (2026-10-20) — G1, G2 and G3 PASSED

24 graded sessions (6 tasks × 4 arms) plus one untimed warm-up for `ssd`. Raw data: `results/1792504819/` (rows, summary, call logs; the Pi session transcripts stay local because they embed the local system prompt). The proxy log confirms one SSD restore per `ssd` session (6 `snapshot_restore`, 35 cache hits / 36 requests, 1 miss = the warm-up).

| Arm | Success (executed and graded) | Median wall time per session | Median prompt tokens processed | Median tool calls |
|---|---|---|---|---|
| `cold` | 6/6 | 23.1 s | 16,865 | 4 |
| **`ssd`** | **6/6** | **13.1 s** | **739** | 4.5 |
| `ram` (best case, server never restarted) | 6/6 | 11.8 s | 915 | 4 |
| `nolib` | 6/6 | 24.3 s | 3,155 (two sessions: ~20k) | 5.5 |

- **G2 PASSED:** `ssd` processes 4.4% of `cold`'s prompt tokens per session (gate ≤ 25%) and cuts the median session from 23.1 s to 13.1 s (−43%). Restoring from NVMe gets within ~1.3 s of keeping everything in RAM, while surviving server restarts and slot evictions.
- **G3 PASSED:** 6/6 in both `ssd` and `cold`: restoring the package from the SSD did not change the agent's success.
- **G1 PASSED through its time clause, not its success clause:** `nolib` also solved 6/6. Without the reference, the agent **read `netkit.py` with its tools** to discover the API (in two sessions it pulled ~20k tokens of source into the context) and needed more tool calls (5.5 vs 4.5). With the package, the same success took 13.1 s instead of 24.3 s (−46%).

**What this means:** when a library's source is small and readable, the library package buys **time and tokens**, not success. The success advantage measured in B3b (0% → 100% without tools) should appear where the agent cannot cheaply read the source (compiled modules, very large packages, network APIs, docs-only knowledge). That is a hypothesis for the next experiment, not a result.

