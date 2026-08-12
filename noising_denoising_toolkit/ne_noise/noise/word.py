"""Word-level noising: dropout, permute, swap, clitic detachment, synonym replacement."""

import random
from typing import Dict, Optional

CLITICS = ["ले", "मा", "बाट", "को", "का", "की", "लाई", "सँग", "हरू", "द्वारा", "भन्दा"]

SYNONYM_MAP: Dict[str, str] = {
    "मान्छे": "मानिस",
    "मानिस": "मान्छे",
    "पानी": "जल",
    "जल": "पानी",
    "घर": "गृह",
    "गृह": "घर",
    "राम्रो": "सुन्दर",
    "सुन्दर": "राम्रो",
    "ठूलो": "विशाल",
    "विशाल": "ठूलो",
    "नयाँ": "नवीन",
    "नवीन": "नयाँ",
    "छिटो": "तुरुन्त",
    "तुरुन्त": "छिटो",
}


def _rng(rng: Optional[random.Random]) -> random.Random:
    return rng if rng is not None else random


def clitic_detachment(text: str, rng: Optional[random.Random] = None) -> str:
    """Detach trailing postposition clitics from words with a space.

    Example::
        "रामले काठमाडौँमा" -> "राम ले काठमाडौँ मा"
    """
    words = text.split()
    res = []
    for w in words:
        detached = False
        for c in sorted(CLITICS, key=lambda x: -len(x)):
            if w.endswith(c) and len(w) > len(c) + 1:
                res.append(f"{w[:-len(c)]} {c}")
                detached = True
                break
        if not detached:
            res.append(w)
    return " ".join(res)


def word_swap(text: str, n: int = 1, rng: Optional[random.Random] = None) -> str:
    """Randomly swap ``n`` pairs of adjacent words."""
    words = text.split()
    if len(words) < 2:
        return text
    r = _rng(rng)
    for _ in range(n):
        idx = r.randint(0, len(words) - 2)
        words[idx], words[idx + 1] = words[idx + 1], words[idx]
    return " ".join(words)


def word_deletion(text: str, p: float = 0.1, rng: Optional[random.Random] = None) -> str:
    """Randomly delete words with probability ``p`` (keeps at least one word)."""
    words = text.split()
    if len(words) <= 1:
        return text
    r = _rng(rng)
    kept = [w for w in words if r.random() >= p]
    return " ".join(kept) if kept else words[0]


def word_dropout(text: str, ratio: float = 0.15, rng: Optional[random.Random] = None) -> str:
    """Word-level dropout (same behavior as word_deletion)."""
    return word_deletion(text, p=ratio, rng=rng)


def word_permute(text: str, ratio: float = 0.2, rng: Optional[random.Random] = None) -> str:
    """Swap adjacent word pairs, touching roughly ``ratio`` of positions."""
    words = text.split()
    if len(words) < 2:
        return text
    r = _rng(rng)
    for i in range(len(words) - 1):
        if r.random() < ratio:
            words[i], words[i + 1] = words[i + 1], words[i]
    return " ".join(words)


def word_replace_synonym(
    text: str,
    ratio: float = 0.2,
    rng: Optional[random.Random] = None,
    synonym_map: Optional[Dict[str, str]] = None,
) -> str:
    """Replace words with synonyms from a lookup table with probability ``ratio``."""
    sm = synonym_map or SYNONYM_MAP
    r = _rng(rng)
    words = text.split()
    for i, w in enumerate(words):
        if w in sm and r.random() < ratio:
            words[i] = sm[w]
    return " ".join(words)
