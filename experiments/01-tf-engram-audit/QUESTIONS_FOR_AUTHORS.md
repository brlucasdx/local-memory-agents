# Questions for the TF-Engram authors

**Status:** draft, NOT sent. Log the send date and the reply here.
**To:** Yutang Ma (ytma2@cse.cuhk.edu.hk), cc Zili Shao (shao@cse.cuhk.edu.hk). Addresses are as printed on the arXiv v1 PDF.

---

**Subject:** Reproducing TF-Engram (arXiv:2607.07388) on a 12 GB consumer GPU: a few implementation questions

Dear Yutang Ma and co-authors,

I'm an independent engineer trying to reproduce TF-Engram on a consumer setup (RTX 3060 12 GB, 30 GB RAM) and then apply it to API knowledge in local coding agents. I read the paper closely and documented a reproducibility audit; a few details decide the result and I couldn't find them in the text:

1. **Injection point.** Which transformer layer(s) receive the memory vector?
2. **Space alignment.** The values are Qwen3-Embedding vectors and the backbone is Qwen3-0.6B. How is an embedding vector turned into the hidden-state update `g·m` without training? Is it a raw addition with a fixed scale, a fixed projection, or something else? Which Qwen3-Embedding size did you use, and what injection scale produced Table 3?
3. **Matching.** At position t, must the matched phrase end exactly at token t? How are the aggregation weights α computed when several phrases match?
4. **Prefetch misses and accuracy.** §4.4 says the early-exit head does not change the final token probabilities, but §5.4 reports different average scores for different early-exit layers. Is the memory injection skipped when an entry is not prefetched in time? If so, is accuracy timing-dependent?
5. **Prefetch head.** Did the experiments use the strictly train-free projection or the lightly calibrated `W_pref`?
6. **Phrase mining.** Which n-gram orders, frequency thresholds and filters, and how many tokens from each corpus?
7. **Evaluation.** Which harness, number of shots and metric variant (acc / acc_norm) produced Table 3? Were the Qwen3-0.6B numbers measured in your pipeline?
8. **LoRA baseline.** Rank, trainable parameter count, training data and steps.
9. **Code.** Do you plan to release code or the constructed tables?

I'll publish the audit and any reproduction openly, with full credit to your work, and I'm happy to share results before publishing.

Thank you for the paper. The GPU–DRAM–SSD design is exactly what makes this interesting for people running models at home.

Best regards,
Lucas Cruz
GitHub: https://github.com/brlucasdx
