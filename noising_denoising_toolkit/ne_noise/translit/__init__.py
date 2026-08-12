"""Transliteration (ne_noise.translit): word -> character -> model tiers."""

from .engine import TransliterationEngine, get_default_engine
from .lexicon import Lexicon, DEFAULT_LEXICON_PATH, lexicon_deva_to_roman, lexicon_roman_to_deva
from .model import TransliterationModel, SUGGESTED_MODELS
from .rules import (
    CONSONANT_MAP,
    MATRA_MAP,
    NEPALI_MATRA_MAP,
    NEPALI_VOWEL_MAP,
    VOWEL_MAP,
    romanize,
    transliterate_devanagari_to_roman,
    transliterate_roman_to_devanagari,
)

__all__ = [
    "TransliterationEngine",
    "get_default_engine",
    "Lexicon",
    "DEFAULT_LEXICON_PATH",
    "lexicon_deva_to_roman",
    "lexicon_roman_to_deva",
    "TransliterationModel",
    "SUGGESTED_MODELS",
    "transliterate_devanagari_to_roman",
    "transliterate_roman_to_devanagari",
    "romanize",
    "VOWEL_MAP",
    "NEPALI_VOWEL_MAP",
    "MATRA_MAP",
    "NEPALI_MATRA_MAP",
    "CONSONANT_MAP",
]
