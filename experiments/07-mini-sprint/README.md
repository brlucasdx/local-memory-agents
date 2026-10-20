# E7 — Mini-sprint: a reduced, same-complexity version of the akitaonrails v4 benchmark

**Inspired by** [akitaonrails/llm-coding-benchmark v4](https://github.com/akitaonrails/llm-coding-benchmark/tree/master/benchmark-v4) ("The Sprint"). That repository declares no license, so **no text from it is reused**: the prompts here are written from scratch, and only the idea and the public methodology (sprints on one evolving Rails app, unannounced teammate sabotage, three-tier vigilance score) are borrowed, with credit.

**Question:** can a 9B model on a 12 GB consumer GPU, with a generic harness, build a real Rails app across sprints and catch planted problems nobody tells it about, in a reasonable time?

## Pre-registration (written 2026-10-20, before any run)

### What is kept from the original, and what is cut
| Difficulty of the original | Here |
|---|---|
| Real framework, little-trained language (Rails 8.1, Ruby) | kept |
| A gem released after the model was trained (**RubyLLM 2.0**, 2026-09-18; 2.1.1 installed) | kept |
| Real app: database, auth, views, model + system tests, Docker/README | kept, smaller scope |
| Unannounced teammate sabotage, mixing loud and silent problems | kept: **7 planted problems** instead of 14 |
| 7 sprints | **4 sprints** |

### Sprints (prompts in `bench/mini-sprint/prompts/`, each preceded by `preamble.txt`)
1. **Foundation:** RubyLLM chat app (Hotwire, Tailwind, Active Record, Docker/compose, README).
2. **Multi-user:** sign up/in/out, per-user ownership, search over the user's own conversations, a small per-user stats page.
3. **"Production-ready"**, vague capstone with a soft opening ("a teammate merged some work").
4. **Reveal:** "problems were deliberately introduced; last chance to fix them all".

Between sprints 2 and 3, a scripted "teammate" commit (author `Casey <casey@example.com>`) applies **7 problems**, chosen from the original benchmark's public categories and adapted to the model's real code: cross-user data access (Critical 5), injection in the search (Critical 5), login link removed from the UI (High 3), unescaped user content in a view (High 3), a hard-coded secret (High 3), a security-relevant test neutered (Medium 2), a per-user stats number that is silently wrong (Medium 2). Total weight **23**. Each one must be verified live on the model's app before the run continues, and none is ever named in a prompt.

### Score
Original formula: Σ(weight × [1.0 caught without being told, i.e. in sprint 3 · 0.4 caught only after the reveal in sprint 4 · 0 never]) / 23 × 100. Regressions introduced by the model are noted. Build quality per sprint is reported separately: boots, requested features present, tests passing, RuboCop/Brakeman/bundle-audit, RubyLLM used through its real API (tests simulate the provider at the HTTP level).

### Arm (single arm, declared)
**Armed 9B:** Pi 1.3.0 + Ornith 1.5 9B Q6_K (`ornith:low`) on llama.cpp v0.7.0 (64k context, q8 KV) through the KV-snapshot proxy, plus one generic tool: `gemdocs`, a search over the documentation of the installed gems (`bench/mini-sprint/tools/gemdocs`). The system prompt tells the agent the tool exists; whether to use it is the model's decision. Nothing about this app or sprint is in the harness.

**Not given to the model:** any plan, step list, file list or order of work (it plans by itself); any hint about the sabotage; the gem's API pasted into the prompt; the grading rubric or checks. **Zero nudges** (the original allowed two per run for open models), no human intervention, no retries.

### Environment (prepared before the clock, declared)
- Ruby 3.3.8 (Debian), Rails 8.1.4 and Bundler 2.7.2 in a dedicated `GEM_HOME`. The gems a Rails 8.1 + Tailwind + RubyLLM app needs were pre-installed by generating and discarding a throwaway app **outside** the test folder: only gems are kept, no app code. bundler-audit's advisory database is pre-fetched.
- **Sandbox (bubblewrap):** the agent sees the project folder (read-write), the gem directory, Ruby/Chrome/system files (read-only) and its own Pi config; the rest of the home directory, including this repository's oracle files, is not mounted. Network is shared (the model server is on localhost); the session logs are audited afterwards for access attempts outside the project.

### Time caps
Sprint 1: 60 min · Sprint 2: 45 min · Sprint 3: 30 min · Sprint 4: 30 min. When a cap expires, the session is stopped and the repository state at that moment is graded.

### Gates (for the planned 15-minute kill test, then the full run)
- **Kill test (first 15 min of sprint 1):** the app boots, persists a message and exercises RubyLLM with an HTTP-level simulated response. If not, stop and diagnose before spending the rest.
- **Sprint 1 success (H7):** within 60 min, every requested piece present, model and system tests passing, Brakeman and bundle-audit clean, RubyLLM called through its real API. Prior estimate from the adversarial review: 35%.
- The vigilance score (sprints 3–4) is reported as is; there is no pass mark, only comparison.

### Calibration (planned, not in this run)
A mini-sprint score does not map to the original's scores. A later run with a model that has a known v4 score (e.g. DeepSeek V4 Flash, 86 there) under the same setup provides the ruler.

## Status (2026-10-20): prepared, not run
Done: prompts, `gemdocs` tool, pre-registration; Ruby 3.3.8, Rails 8.1.4 and Bundler 2.7.2 installed in the dedicated `GEM_HOME`.
Pending: finish pre-caching the app gems (interrupted), the bubblewrap sandbox launcher (use `PI_CODING_AGENT_DIR` pointing to an experiment-only Pi config **without** `auth.json`), the run orchestrator, and the 15-minute kill test.

## Results
*(filled after the run)*
