# Bench

Executable coding tasks with hidden oracles, used in phase 4 (and reusable for the side tracks).

## Rules
1. **Oracles never enter any memory, RAG index or prompt.** `bench/oracles/` is read only by the grader.
2. Every task pins the library version it targets.
3. Tasks are written from the library's specification, never copied from its docs examples or tests.
4. Split is fixed before any run: `tasks/dev/` (12) and `tasks/blind/` (60). Blind tasks are not looked at while tuning.
5. Each task: `prompt.md`, `scaffold/` (starting code), `meta.json` (library, version, APIs exercised).
6. Each oracle: hidden tests + a check for non-existent / incompatible API calls (symbol resolution against the pinned version).
