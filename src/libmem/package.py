"""Library memory packages: load a source package and compile it for one core model.

A *source package* is model-agnostic JSON written by people (library, version,
symbols with signature, doc and key phrases). A *compiled package* holds, for
every symbol, the hidden states the core model itself produces when it reads
that symbol's documentation line ("self-encoded values"), for every layer, so
the injection layer can be chosen later without recompiling.
"""

from __future__ import annotations

import hashlib
import json
import re
from dataclasses import dataclass
from pathlib import Path

import torch

SOURCE_FORMAT = "local-memory/source-package@0"
COMPILED_FORMAT = "local-memory/compiled-package@0"
_IDENTIFIER = re.compile(r"[A-Za-z_][A-Za-z0-9_]{0,63}")
_MAX_SYMBOLS = 10_000
_MAX_TEXT = 500


@dataclass(frozen=True)
class Symbol:
    name: str
    signature: str
    doc: str
    keys: tuple[str, ...]

    def doc_line(self, library: str) -> str:
        return f"{library}.{self.name}{self.signature}  # {self.doc}"


@dataclass(frozen=True)
class SourcePackage:
    library: str
    version: str
    symbols: tuple[Symbol, ...]

    @property
    def digest(self) -> str:
        payload = json.dumps(
            [self.library, self.version, [(s.name, s.signature, s.doc, s.keys) for s in self.symbols]],
            ensure_ascii=False,
        )
        return hashlib.sha256(payload.encode()).hexdigest()


def _text(value: object, field: str) -> str:
    if not isinstance(value, str) or not value.strip() or len(value) > _MAX_TEXT:
        raise ValueError(f"invalid {field!r}: must be a non-empty string up to {_MAX_TEXT} chars")
    return value.strip()


def load_source(path: Path) -> SourcePackage:
    """Load and validate a source package. Community packages are untrusted input."""
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    if data.get("format") != SOURCE_FORMAT:
        raise ValueError(f"unsupported format {data.get('format')!r}")
    library = _text(data.get("library"), "library")
    if not _IDENTIFIER.fullmatch(library):
        raise ValueError("library must be an identifier")
    raw = data.get("symbols")
    if not isinstance(raw, list) or not 0 < len(raw) <= _MAX_SYMBOLS:
        raise ValueError("symbols must be a non-empty list")
    symbols, seen = [], set()
    for item in raw:
        name = _text(item.get("name"), "name")
        if not _IDENTIFIER.fullmatch(name) or name in seen:
            raise ValueError(f"invalid or duplicate symbol name {name!r}")
        seen.add(name)
        keys = item.get("keys")
        if not isinstance(keys, list) or not keys:
            raise ValueError(f"symbol {name!r} needs at least one key phrase")
        symbols.append(Symbol(
            name=name,
            signature=_text(item.get("signature"), "signature"),
            doc=_text(item.get("doc"), "doc"),
            keys=tuple(_text(k, "key") for k in keys),
        ))
    return SourcePackage(library=library, version=_text(data.get("version"), "version"), symbols=tuple(symbols))


@torch.no_grad()
def compile_package(source: SourcePackage, model, tokenizer, model_id: str) -> dict:
    """Run every symbol's doc line through the frozen core and keep its hidden states.

    For each symbol and each layer we store two candidate values: the hidden
    state of the last token and the mean over the whole line. Shape of each
    tensor: [num_symbols, num_layers + 1, hidden_size] (index 0 = embeddings).
    """
    device = next(model.parameters()).device
    last, mean = [], []
    for sym in source.symbols:
        ids = tokenizer(sym.doc_line(source.library), return_tensors="pt").input_ids.to(device)
        hidden = model(ids, output_hidden_states=True).hidden_states  # tuple of [1, T, H]
        stack = torch.stack([h[0] for h in hidden])  # [L+1, T, H]
        last.append(stack[:, -1, :].float().cpu())
        mean.append(stack.mean(dim=1).float().cpu())
    return {
        "format": COMPILED_FORMAT,
        "library": source.library,
        "version": source.version,
        "source_digest": source.digest,
        "model_id": model_id,
        "symbols": [s.name for s in source.symbols],
        "values_last": torch.stack(last),
        "values_mean": torch.stack(mean),
    }


def save_compiled(compiled: dict, path: Path) -> None:
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    torch.save(compiled, path)


def load_compiled(path: Path, source: SourcePackage, model_id: str) -> dict:
    # weights_only=True: never unpickle arbitrary objects from a package file.
    compiled = torch.load(path, map_location="cpu", weights_only=True)
    if compiled.get("format") != COMPILED_FORMAT:
        raise ValueError("not a compiled package")
    if compiled["source_digest"] != source.digest or compiled["model_id"] != model_id:
        raise ValueError("compiled package does not match this source package or model; recompile")
    return compiled
