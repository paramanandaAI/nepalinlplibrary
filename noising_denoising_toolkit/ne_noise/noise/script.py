"""Script-level noising: code-mixing and partial/full transliteration."""

import random
from typing import Optional

from ..translit.engine import TransliterationEngine, get_default_engine


def transliterate_full(
    text: str,
    direction: str = "auto",
    rng: Optional[random.Random] = None,
    engine: Optional[TransliterationEngine] = None,
) -> str:
    """Transliterate the entire text between Devanagari and Roman."""
    engine = engine or get_default_engine()
    return engine.transliterate(text, direction=direction)


def transliterate_random_words(
    text: str,
    ratio: float = 0.3,
    direction: str = "auto",
    rng: Optional[random.Random] = None,
    engine: Optional[TransliterationEngine] = None,
) -> str:
    """Transliterate a random subset of words (partial script shift)."""
    engine = engine or get_default_engine()
    r = rng if rng is not None else random
    words = text.split()
    if not words:
        return text
    for i, w in enumerate(words):
        if r.random() < ratio:
            words[i] = engine.transliterate(w, direction=direction)
    return " ".join(words)


def code_mix(
    text: str,
    ratio: float = 0.3,
    rng: Optional[random.Random] = None,
    engine: Optional[TransliterationEngine] = None,
) -> str:
    """Mix Devanagari with Romanized Nepali by transliterating a fraction of words."""
    engine = engine or get_default_engine()
    r = rng if rng is not None else random
    words = text.split()
    if not words:
        return text
    for i, w in enumerate(words):
        if r.random() < ratio:
            words[i] = engine.deva_to_roman(w)
    return " ".join(words)
