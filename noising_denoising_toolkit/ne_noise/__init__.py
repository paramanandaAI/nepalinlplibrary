"""
ne_noise — Nepali-first noising & denoising toolkit.

Public API: text primitives, transliteration (word -> character -> model tiers),
noising operators + engine, denoising pairs, pipelines, model wrappers.
"""

__version__ = "0.1.0"

from .text.normalize import (
    collapse_whitespace,
    normalize_danda,
    normalize_nepali_text,
    remove_zero_width,
    to_nfc,
)
from .text.scripts import (
    contains_devanagari,
    devanagari_ratio,
    is_devanagari,
    is_devanagari_char,
    word_tokens,
)
from .translit.engine import TransliterationEngine, get_default_engine
from .translit.lexicon import Lexicon, DEFAULT_LEXICON_PATH
from .translit.rules import (
    romanize,
    transliterate_devanagari_to_roman,
    transliterate_roman_to_devanagari,
)
from .noise.engine import (
    NOISE_OPS,
    apply_composed_noising,
    apply_noising,
    apply_random_noising,
    list_noise_ops,
    noise_variants,
)
from .noise.char import (
    inject_random_noise,
    random_char_deletion,
    random_char_insertion,
    random_char_substitution,
    random_char_swap,
)
from .noise.homophone import get_homophone_map, substitute_homophones
from .noise.keyboard import keyboard_typo
from .noise.word import (
    clitic_detachment,
    word_deletion,
    word_dropout,
    word_permute,
    word_replace_synonym,
    word_swap,
)
from .noise.script import code_mix, transliterate_full, transliterate_random_words
from .noise.span import random_mask, sentence_permutation, span_corruption
from .denoise.normalize import canonicalize_orthography, denoise_artifacts
from .denoise.pairs import (
    NoisePair,
    make_pairs,
    make_pairs_from_records,
    read_jsonl,
    write_jsonl,
)
from .pipelines.noising_pipeline import NoisingPipeline

__all__ = [
    # text
    "normalize_nepali_text",
    "collapse_whitespace",
    "normalize_danda",
    "remove_zero_width",
    "to_nfc",
    "is_devanagari",
    "is_devanagari_char",
    "contains_devanagari",
    "devanagari_ratio",
    "word_tokens",
    # translit
    "TransliterationEngine",
    "get_default_engine",
    "Lexicon",
    "DEFAULT_LEXICON_PATH",
    "transliterate_devanagari_to_roman",
    "transliterate_roman_to_devanagari",
    "romanize",
    # noise engine
    "NOISE_OPS",
    "list_noise_ops",
    "apply_noising",
    "apply_random_noising",
    "apply_composed_noising",
    "noise_variants",
    # noise char
    "random_char_deletion",
    "random_char_insertion",
    "random_char_swap",
    "random_char_substitution",
    "inject_random_noise",
    # noise word / homophone / keyboard / script / span
    "substitute_homophones",
    "get_homophone_map",
    "keyboard_typo",
    "word_dropout",
    "word_deletion",
    "word_permute",
    "word_swap",
    "word_replace_synonym",
    "clitic_detachment",
    "code_mix",
    "transliterate_full",
    "transliterate_random_words",
    "random_mask",
    "span_corruption",
    "sentence_permutation",
    # denoise
    "canonicalize_orthography",
    "denoise_artifacts",
    "NoisePair",
    "make_pairs",
    "make_pairs_from_records",
    "write_jsonl",
    "read_jsonl",
    # pipelines
    "NoisingPipeline",
]
