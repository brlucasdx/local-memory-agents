"""Inject library-memory values into the hidden state of a frozen core model.

Matching is TF-Engram-style phrase matching on the token stream: when a
symbol's key phrase appears in the prompt, the symbol's value is added to the
residual stream at layer ℓ on the matched tokens:

    h'_ℓ[t] = h_ℓ[t] + α · ‖h_ℓ[t]‖ · v / ‖v‖

The value is rescaled to the norm of the hidden state it is added to, so α is
comparable across layers and models. Injection happens only in the prefill
pass; generated tokens read the injected states through attention.
"""

from __future__ import annotations

from contextlib import contextmanager

import torch


def _token_variants(tokenizer, phrase: str) -> list[list[int]]:
    """Token ids of a phrase as it may appear mid-sentence or at a line start."""
    variants = []
    for text in (" " + phrase, phrase, " " + phrase.lower(), phrase.lower()):
        ids = tokenizer(text, add_special_tokens=False).input_ids
        if ids and ids not in variants:
            variants.append(ids)
    return variants


def match_positions(input_ids: list[int], tokenizer, keys_by_symbol: dict[int, tuple[str, ...]]) -> dict[int, int]:
    """Map token position -> symbol index for every key-phrase occurrence (longest match wins)."""
    hits: dict[int, tuple[int, int]] = {}
    for sym_idx, keys in keys_by_symbol.items():
        for key in keys:
            for pattern in _token_variants(tokenizer, key):
                n = len(pattern)
                for start in range(len(input_ids) - n + 1):
                    if input_ids[start:start + n] == pattern:
                        for pos in range(start, start + n):
                            if pos not in hits or hits[pos][1] < n:
                                hits[pos] = (sym_idx, n)
    return {pos: sym for pos, (sym, _) in hits.items()}


@contextmanager
def injected(model, layer: int, positions: dict[int, int], values: torch.Tensor, alpha: float):
    """Context manager that adds memory values at `positions` in the output of decoder layer `layer`.

    `values` is [num_symbols, hidden] for the chosen layer. Only the prefill
    call (sequence longer than one token) is modified.
    """
    block = model.model.layers[layer - 1]  # hidden_states[ℓ] is the output of block ℓ-1
    pos_list = sorted(positions)
    sym_idx = torch.tensor([positions[p] for p in pos_list], dtype=torch.long)

    def hook(_module, _inputs, output):
        hidden = output[0] if isinstance(output, tuple) else output
        if hidden.shape[1] <= 1 or not pos_list:
            return output
        idx = torch.tensor(pos_list, device=hidden.device)
        h = hidden[0, idx, :]
        v = values[sym_idx].to(device=hidden.device, dtype=torch.float32)
        v = v / v.norm(dim=-1, keepdim=True).clamp_min(1e-6)
        delta = alpha * h.float().norm(dim=-1, keepdim=True) * v
        hidden = hidden.clone()
        hidden[0, idx, :] = (h.float() + delta).to(hidden.dtype)
        return (hidden, *output[1:]) if isinstance(output, tuple) else hidden

    handle = block.register_forward_hook(hook)
    try:
        yield
    finally:
        handle.remove()
