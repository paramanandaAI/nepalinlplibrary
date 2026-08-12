"""Span-level noising: BART/T5-style span corruption, masking, sentence permutation."""

import random
from typing import List, Optional

MASK_TOKEN = "<mask>"


def _rng(rng: Optional[random.Random]) -> random.Random:
    return rng if rng is not None else random


def random_mask(
    text: str,
    ratio: float = 0.15,
    mask_token: str = MASK_TOKEN,
    rng: Optional[random.Random] = None,
) -> str:
    """Replace a random subset of words with the mask token."""
    r = _rng(rng)
    words = text.split()
    if not words:
        return text
    out = [mask_token if r.random() < ratio else w for w in words]
    return " ".join(out)


def span_corruption(
    text: str,
    corruption_rate: float = 0.3,
    max_span_length: int = 3,
    mask_token: str = MASK_TOKEN,
    rng: Optional[random.Random] = None,
) -> str:
    """Replace contiguous word spans with a single mask token (BART/T5-style).

    Every corrupted span is collapsed into one ``mask_token``, so the output can
    be shorter than the input, matching the pretraining setup of BART/T5.
    """
    r = _rng(rng)
    words = text.split()
    if not words:
        return text

    corrupted = [False] * len(words)
    count = 0
    while count < len(words) and r.random() < corruption_rate:
        i = r.randrange(len(words))
        length = r.randint(1, max_span_length)
        for j in range(i, min(i + length, len(words))):
            if not corrupted[j]:
                corrupted[j] = True
                count += 1

    out: List[str] = []
    i = 0
    while i < len(words):
        if corrupted[i]:
            out.append(mask_token)
            while i < len(words) and corrupted[i]:
                i += 1
        else:
            out.append(words[i])
            i += 1
    return " ".join(out)


def sentence_permutation(
    text: str,
    p: float = 0.5,
    rng: Optional[random.Random] = None,
) -> str:
    """Randomly permute sentence order (split on danda/period)."""
    r = _rng(rng)
    parts = [s for s in text.replace("।", "।\n").replace(".", ".\n").split("\n") if s.strip()]
    if len(parts) < 2:
        return text
    if r.random() < p:
        r.shuffle(parts)
    return " ".join(parts)
