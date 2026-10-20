# B4 — Real library: Polars 2.0 (released after the core's training)

**Question:** when an agent's knowledge of a real library is out of date, does a library package (compiled KV snapshot of the official docs, restored from NVMe) raise its success, and how does it compare to RAG over the same docs?

## Pre-registration (written 2026-10-20, before any agent run)

**Scope change from the original plan (declared):** the original B4 plan was 72 tasks over 20 APIs × 4 arms with a fictional library. This run uses a **real** library and **10 tasks**. Fewer tasks, but real APIs, real breaking changes and executable grading; the result is reported per task and per change type.

- **Library:** Polars **2.0.0**, released **2026-10-06** (PyPI), after Ornith 1.5 (August 2026) was trained. Ornith is expected to know Polars 1.x.
- **Library package:** the official upgrade guide `docs/source/releases/upgrade/2.md` (pola-rs/polars, MIT), unmodified: `packages/source/polars-2.0.0/`. It goes into the system prompt via `--append-system-prompt`; the proxy snapshots it on NVMe.
- **Tasks:** `bench/tasks/polars-2.0/tasks.json`, 10 tasks, each targeting one documented 2.0 change. Validity check run **before** the agents (`bench/oracles/polars-2.0/oracle.py`): the reference solution passes every hidden test and the polars-1.x-style solution fails every one. 7 fail with an error (5 of those errors name the fix, e.g. "Use `str.to_date()` instead"), 3 change results **silently** (`explode` of empty lists, headerless CSV column numbering starting at 0).
- **Agent:** Pi 1.3.0, `ornith:low`, `-p -nc`; `python3` in the agent's PATH is the project venv (polars 2.0.0 installed). Grading imports `solution.py` and runs the hidden test; the oracle is never shown to the agent.
- **Arms:**
  | Arm | Docs | Path |
  |---|---|---|
  | `nolib` | none (the agent can still run code and read error messages) | Pi → llama-server, in-RAM prefix cache kept |
  | `rag` | the 3 guide sections with the highest word overlap with the task, appended to the user prompt | Pi → llama-server, in-RAM prefix cache kept |
  | `pkg` | the whole guide in the system prompt | Pi → proxy → llama-server, **slot erased before each session**, guide restored from NVMe |
  `pkg` gets one untimed warm-up session to publish the golden snapshot.
- **Metrics:** hidden-test success; wall time per session; prompt tokens processed; tool calls. One run per task and arm (n = 10 per arm).

### Gates
- **G1 knowledge helps:** success(`pkg`) ≥ success(`nolib`) + 3 tasks (30 pp).
- **G2 versus RAG:** success(`pkg`) ≥ success(`rag`) − 1 task **and** median wall time(`pkg`) ≤ median wall time(`rag`).
- Results are also reported by change type (silent / error / error-with-hint), where the expectation is that `nolib` can recover from hinted errors but not from silent changes.

## Results (2026-10-20) — G1 FAILED (by one task), G2 FAILED on time

30 graded sessions + 1 untimed warm-up. Raw data: `results/<run>/rows.json` and `summary.json` (Pi session transcripts stay local: they embed the local system prompt).

| Arm | Success | silent (2) | error (3) | error-with-hint (5) | Median wall time | Median prompt tokens processed | Median tool calls |
|---|---|---|---|---|---|---|---|
| `nolib` | 7/10 | 0/2 | 2/3 | 5/5 | 29.4 s | 1,497 | 5 |
| **`rag`** (3 sections in the user prompt) | **10/10** | **2/2** | 3/3 | 5/5 | **24.5 s** | 5,012 | 4.5 |
| `pkg` (whole 23,066-token guide in the system prompt, restored from NVMe) | 9/10 | 1/2 | 3/3 | 5/5 | 64.1 s | 927 | 7.5 |

- **G1 FAILED:** `pkg` 9/10 vs `nolib` 7/10 (+2, gate +3).
- **G2 FAILED:** accuracy within one task of `rag` (9 vs 10) ✓, but median wall time 64.1 s vs 24.5 s ✗.

### What the data says
- **The prediction about silent changes held for `nolib`:** it recovered from every error whose message names the fix (5/5) and failed both silent changes (0/2), where the code runs and returns a wrong result.
- **Lexical RAG was much stronger than expected:** 10/10, including the two CSV tasks where its retrieval returned the wrong sections (the agent recovered by running the code).
- **`pkg` lost on time, not on reading.** It processed the fewest prompt tokens (the SSD restore worked: 927 vs 5,012), but it made more tool calls (7.5 vs 4.5), and three sessions ran long (94 s, 108 s, 187 s). It also missed the `explode` silent change although the guide's section about it was in context.
- **Hypothesis (not tested yet):** a 9B model uses a long prose document in the system prompt worse than a few targeted excerpts placed next to the task (attention dilution / lost in the middle). Decode is also slower with a ~27k-token context. In B3b the package won because the task was a single lookup in a structured 500-line reference; an agent loop over a 23k-token prose guide is a different regime.
- n = 1 per task and arm; a few long sessions drive the medians. A rerun could move these numbers.

### Consequence for the architecture
For **library knowledge**, selection beats completeness on a 9B: delivering the *relevant* sections (RAG) worked better than the *whole* guide (package). The SSD snapshot keeps its value for **large stable prefixes** (agent instructions, project context, structured API references), as B2, B3b and E5 showed, but "put the whole library doc in the prefix" is not the right default for a small model.

