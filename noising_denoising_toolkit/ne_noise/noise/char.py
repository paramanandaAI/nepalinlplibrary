"""Character-level noising: deletion, insertion, swap, substitution, composite noise."""

import random
from typing import Optional

from ..text.scripts import DEPENDENT_MATRAS, INDEPENDENT_VOWELS, NUKTA_BASE

DEVANAGARI_CHARS = [
    *list(INDEPENDENT_VOWELS),
    "क", "ख", "ग", "घ", "च", "छ", "ज", "झ", "त", "थ", "द", "ध", "न",
    "प", "फ", "ब", "भ", "म", "य", "र", "ल", "व", "स", "ह",
    *list(DEPENDENT_MATRAS),
    "ं", "्",
]

_INSERT_POOL = [c for c in DEVANAGARI_CHARS if c != "्"]
_SUBSTITUTE_POOL = [c for c in DEVANAGARI_CHARS if c not in NUKTA_BASE]


def _rng(rng: Optional[random.Random]) -> random.Random:
    return rng if rng is not None else random


def random_char_deletion(text: str, p: float = 0.05, rng: Optional[random.Random] = None) -> str:
    """Randomly delete non-space characters with probability ``p``."""
    if not text:
        return text
    r = _rng(rng)
    chars = [ch for ch in text if r.random() >= p or ch == " "]
    return "".join(chars) if chars else text


def random_char_insertion(text: str, p: float = 0.05, rng: Optional[random.Random] = None) -> str:
    """Randomly insert Devanagari characters after non-space characters with probability ``p``."""
    r = _rng(rng)
    out = []
    for ch in text:
        out.append(ch)
        if ch != " " and r.random() < p:
            out.append(r.choice(_INSERT_POOL))
    return "".join(out)


def random_char_swap(text: str, p: float = 0.05, rng: Optional[random.Random] = None) -> str:
    """Randomly transpose adjacent characters (skipping spaces) with probability ``p``."""
    r = _rng(rng)
    chars = list(text)
    for i in range(len(chars) - 1):
        if chars[i] != " " and chars[i + 1] != " " and r.random() < p:
            chars[i], chars[i + 1] = chars[i + 1], chars[i]
    return "".join(chars)


def random_char_substitution(text: str, p: float = 0.05, rng: Optional[random.Random] = None) -> str:
    """Replace random Devanagari characters with a random Devanagari character."""
    r = _rng(rng)
    chars = list(text)
    for i, ch in enumerate(chars):
        if ch != " " and r.random() < p:
            chars[i] = r.choice(_SUBSTITUTE_POOL)
    return "".join(chars)


def random_typo_injection(
    text: str,
    p: float = 0.05,
    rng: Optional[random.Random] = None,
    neighbors=None,
) -> str:
    """Keyboard-neighbor typo injection (uses noise.keyboard if available)."""
    if neighbors is None:
        from .keyboard import KEYBOARD_NEIGHBORS

        neighbors = KEYBOARD_NEIGHBORS
    r = _rng(rng)
    chars = list(text)
    for i, ch in enumerate(chars):
        if ch in neighbors and r.random() < p:
            chars[i] = r.choice(neighbors[ch])
    return "".join(chars)


def matra_drop(text: str, p: float = 0.1, rng: Optional[random.Random] = None) -> str:
    """Randomly drop Devanagari matras (vowel diacritics) with probability ``p``."""
    r = _rng(rng)
    matras = set(DEPENDENT_MATRAS)
    out = []
    for ch in text:
        if ch in matras and r.random() < p:
            continue
        out.append(ch)
    return "".join(out) if out else text


def halanta_drop(text: str, p: float = 0.1, rng: Optional[random.Random] = None) -> str:
    """Randomly drop Halanta ('्') from conjuncts with probability ``p``."""
    r = _rng(rng)
    out = []
    for ch in text:
        if ch == "्" and r.random() < p:
            continue
        out.append(ch)
    return "".join(out)


def inject_random_noise(
    text: str,
    noise_level: float = 0.1,
    rng: Optional[random.Random] = None,
) -> str:
    """Composite character noise: swap, delete, insert, then substitute.

    ``noise_level`` is clamped to [0.01, 0.3] internally.
    """
    r = _rng(rng)
    p = max(0.01, min(0.3, noise_level / 4.0))
    t = random_char_swap(text, p=p, rng=r)
    t = random_char_deletion(t, p=p, rng=r)
    t = random_char_insertion(t, p=p, rng=r)
    t = random_char_substitution(t, p=p, rng=r)
    return t

