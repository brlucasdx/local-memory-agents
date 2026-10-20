# Local Memory for Small Coding Agents

> **At home, the rules are different.** In the cloud, reading context is cheap, so the standard fix for "the model doesn't know this library" is RAG: paste the docs into the prompt. On a consumer GPU, reading context *is* the bottleneck. Every page of docs pasted into the prompt is paid again at every agent step.
>
> This project tests whether **conditional memory** (knowledge looked up from a table outside VRAM and injected into the hidden state, adding **zero tokens** to the context) beats RAG on the hardware most people actually own.

**Status:** research in progress. Nothing below is a result yet, except what is marked **[measured]**.
**Author:** Lucas Cruz · Brazil

---

## Why

Small open models can already run at home. What they can't do is run *fast enough to work*, and they invent APIs they never memorized.

- **[measured]** RTX 3060 12 GB (360 GB/s): Ornith 1.5 9B Q6_K decodes at **38 tok/s**, ~77% of the bandwidth ceiling. A better inference engine can win ~1.3× here, not 10×.
- **[published]** Akita's LLM coding benchmark v4: the same Qwen 3.8 27B scored **80.5** on a rented B300 and **80.0** on a home Strix Halo. Same quality, but **192 vs 706 minutes**. At home, intelligence fits; speed doesn't.
- An agent re-reads tens of thousands of tokens per step. On consumer hardware that prefill, not generation, is the wall, and RAG makes it worse.

## Thesis

1. **API memory instead of API context.** Version-pinned library knowledge (e.g. Rails 8, RubyLLM) lives in a conditional-memory table in RAM/SSD. The model reads a few rows per token instead of re-reading docs every step.
2. **Memory packages.** One memory file per library and version, generated from the real docs and pluggable into a small model without retraining. This also covers APIs released after the model's training cutoff, which is a problem frontier models have too.
3. **Project memory** (long-term, most speculative): the repository indexed as memory instead of re-read as context.

## Prior art (we are building on it, not claiming it)

The core mechanism is published: [DeepSeek Engram](https://arxiv.org/abs/2601.07372) (conditional memory beats an iso-parameter, iso-FLOPs MoE), [TF-Engram](https://arxiv.org/abs/2607.07388) (train-free, GPU–DRAM–SSD tables), [EngramEdit](https://arxiv.org/abs/2610.10533), [KOFF](https://arxiv.org/abs/2605.29075), [UltraMemV2](https://arxiv.org/abs/2508.18756). See [docs/RELATED_WORK.md](docs/RELATED_WORK.md).

**What we have not found:** conditional memory evaluated in **coding agents** on executable tasks, compared against RAG on **total wall time on a 12 GB GPU**, and distributed as versioned memory packages.

## Roadmap

| Phase | What | Gate |
|---|---|---|
| 0 | Local baseline (Ornith 9B, Pi harness) | done, see [experiments/00-baseline-local](experiments/00-baseline-local) |
| 1 | TF-Engram reproducibility audit | **done: 6 of 10 decisive details unspecified; questions drafted for the authors**, see [AUDIT](experiments/01-tf-engram-audit/AUDIT.md) |
| 2 | Minimal reimplementation (Qwen3-0.6B, table in RAM) | each component is verifiable and fits in 12 GB |
| 3 | Reproduce the published gain, with confidence intervals | confident gain at acceptable cost |
| 4 | **API memory vs RAG**: 72 executable tasks × 4 arms | API errors −30%, success +10 pp vs bare model; ≥ RAG success with ≥15% less wall time |
| 5 | Memory packages per library/version | — |
| 6 | Project memory | — |

Each phase is pre-registered in its `experiments/NN-*/README.md` before it runs.

## Honest outcomes

- **If it works:** *Train-free conditional memory for APIs in local coding agents: reproduction and evaluation on a 12 GB GPU.*
- **If it doesn't:** a validated reproduction that helps general benchmarks but **loses to RAG** on executable tasks or total time is still a useful, publishable boundary. An unvalidated reimplementation that fails proves nothing, and we won't claim otherwise.

## Repository layout

```
docs/            proposal, related work, decision log
experiments/     one folder per phase, each with README, config and RESULTS
bench/           executable tasks and hidden oracles (oracles never enter any memory)
src/             implementation (empty until phase 2)
refs/            papers (PDFs not versioned)
```

## License

To be defined. Until a license is added, all rights are reserved.
