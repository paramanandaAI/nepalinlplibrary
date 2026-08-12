"""
Denoising pair construction: (clean, noised) records for pretraining/fine-tuning.

This is the supervised signal for T5-style text denoising, BART-style span
corruption, GEC-style spelling tasks, and transliteration normalization.
"""

import hashlib
import json
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Dict, Iterable, List, Optional, Tuple, Union

DEFAULT_OPS = [
    "char_deletion",
    "char_insertion",
    "char_swap",
    "char_substitution",
    "keyboard_typo",
    "homophone",
    "word_dropout",
    "word_permute",
    "code_mix",
    "span_corruption",
]


@dataclass
class NoisePair:
    """A single (clean, noised) denoising example."""

    clean: str
    noised: str
    ops: Tuple[str, ...]
    id: str = ""

    @classmethod
    def create(
        cls,
        clean: str,
        ops: Tuple[str, ...],
        source_id: str = "",
    ) -> "NoisePair":
        h = hashlib.md5(f"{source_id}:{clean}:{':'.join(ops)}".encode("utf-8")).hexdigest()[:10]
        return cls(clean=clean, noised="", ops=ops, id=h)

    def dict(self) -> Dict:
        return asdict(self)


def make_pairs(
    clean_texts: Iterable[str],
    ops: Optional[List[str]] = None,
    k: int = 1,
    seed: Optional[int] = None,
    source_ids: Optional[Iterable[str]] = None,
    noising_fn=None,
) -> List[NoisePair]:
    """Build ``k`` noised variants per clean text.

    ``ops``: operator names sampled for each variant (defaults to DEFAULT_OPS).
    ``noising_fn``: optional custom ``(clean, seed) -> (ops_tuple, noised)`` factory.
    """
    import random

    from ..noise.engine import apply_noising

    r = random.Random(seed)
    op_pool = ops or DEFAULT_OPS
    pairs: List[NoisePair] = []
    sources = list(source_ids) if source_ids is not None else []

    for idx, clean in enumerate(clean_texts):
        clean = clean.strip()
        if not clean:
            continue
        src = sources[idx] if idx < len(sources) else ""
        for _ in range(k):
            chosen = tuple(r.choice(op_pool) for _ in range(r.randint(1, 3)))
            if noising_fn is not None:
                ops_used, noised = noising_fn(clean, r.randint(0, 1 << 31))
                chosen = tuple(ops_used)
            else:
                noised = clean
                for op in chosen:
                    noised = apply_noising(noised, op, seed=r.randint(0, 1 << 31))
            pair = NoisePair.create(clean, chosen, source_id=src)
            pair.noised = noised
            pairs.append(pair)
    return pairs


def make_pairs_from_records(
    records: Iterable[Dict],
    text_field: str = "text",
    ops: Optional[List[str]] = None,
    k: int = 1,
    seed: Optional[int] = None,
) -> List[NoisePair]:
    """Build pairs from JSONL-style records (dicts) using a text field."""
    texts = [(rec.get(text_field, ""), rec.get("id", "")) for rec in records]
    clean = [t for t, _ in texts]
    ids = [i for _, i in texts]
    return make_pairs(clean, ops=ops, k=k, seed=seed, source_ids=ids)


def write_jsonl(pairs: Union[List[NoisePair], List[Dict]], path: Union[str, Path]) -> None:
    """Write pairs to JSONL (one JSON object per line, UTF-8)."""
    out = Path(path)
    out.parent.mkdir(parents=True, exist_ok=True)
    with open(out, "w", encoding="utf-8") as f:
        for p in pairs:
            if isinstance(p, NoisePair):
                f.write(json.dumps(p.dict(), ensure_ascii=False) + "\n")
            else:
                f.write(json.dumps(p, ensure_ascii=False) + "\n")


def read_jsonl(path: Union[str, Path]) -> List[Dict]:
    """Read JSONL pairs back as dicts."""
    records = []
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                records.append(json.loads(line))
    return records
