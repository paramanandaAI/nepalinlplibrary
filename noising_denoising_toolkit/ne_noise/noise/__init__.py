"""Noising operators (ne_noise.noise)."""

from .char import (
    inject_random_noise,
    random_char_deletion,
    random_char_insertion,
    random_char_substitution,
    random_char_swap,
    random_typo_injection,
)
from .engine import (
    NOISE_OPS,
    apply_composed_noising,
    apply_noising,
    apply_random_noising,
    list_noise_ops,
    noise_variants,
)
from .homophone import HOMOPHONE_MAP, get_homophone_map, substitute_homophones
from .keyboard import KEYBOARD_NEIGHBORS, keyboard_typo
from .script import code_mix, transliterate_full, transliterate_random_words
from .span import MASK_TOKEN, random_mask, sentence_permutation, span_corruption
from .word import (
    CLITICS,
    SYNONYM_MAP,
    clitic_detachment,
    word_deletion,
    word_dropout,
    word_permute,
    word_replace_synonym,
    word_swap,
)

__all__ = [
    "random_char_deletion",
    "random_char_insertion",
    "random_char_swap",
    "random_char_substitution",
    "random_typo_injection",
    "inject_random_noise",
    "substitute_homophones",
    "get_homophone_map",
    "HOMOPHONE_MAP",
    "keyboard_typo",
    "KEYBOARD_NEIGHBORS",
    "clitic_detachment",
    "word_swap",
    "word_deletion",
    "word_dropout",
    "word_permute",
    "word_replace_synonym",
    "CLITICS",
    "SYNONYM_MAP",
    "transliterate_full",
    "transliterate_random_words",
    "code_mix",
    "random_mask",
    "span_corruption",
    "sentence_permutation",
    "MASK_TOKEN",
    "NOISE_OPS",
    "list_noise_ops",
    "apply_noising",
    "apply_random_noising",
    "apply_composed_noising",
    "noise_variants",
]
