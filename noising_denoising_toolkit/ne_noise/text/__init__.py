"""Nepali text primitives (ne_noise.text)."""

from .normalize import (
    collapse_whitespace,
    normalize_danda,
    normalize_nepali_text,
    remove_zero_width,
    to_nfc,
)
from .scripts import (
    ANUSVARA,
    CHANDRABINDU,
    CONSONANTS,
    DANDA,
    DEPENDENT_MATRAS,
    HALANT,
    INDEPENDENT_VOWELS,
    VISARGA,
    char_category,
    contains_devanagari,
    devanagari_ratio,
    is_devanagari,
    is_devanagari_char,
    word_tokens,
)

__all__ = [
    "normalize_nepali_text",
    "normalize_danda",
    "collapse_whitespace",
    "remove_zero_width",
    "to_nfc",
    "is_devanagari",
    "is_devanagari_char",
    "contains_devanagari",
    "devanagari_ratio",
    "char_category",
    "word_tokens",
    "INDEPENDENT_VOWELS",
    "DEPENDENT_MATRAS",
    "CONSONANTS",
    "ANUSVARA",
    "CHANDRABINDU",
    "VISARGA",
    "HALANT",
    "DANDA",
]
