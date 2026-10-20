# Phase 4 — API memory vs RAG (main result)

One version-pinned library. 72 tasks (12 dev + 60 blind) over 20 APIs with hidden independent tests. Arms: bare core, lexical RAG (same docs), conditional memory, shuffled memory. Key metric: total wall time vs number of agent steps. Gate: API errors −30% and success +10 pp vs bare core; vs RAG, success ≥ with ≥15% less wall time.

**Pre-registration (fill before running):** configuration, metrics, CONTINUE/STOP gate. See `docs/pt/PLANO-DE-PESQUISA.md`.
