"""
Noising engine: operator registry plus single / random / composed application.

Every registered operator has the signature ``fn(text, **kwargs)`` and supports a
``rng`` kwarg for deterministic experiments.
"""

import random
from typing import Callable, Dict, List, Optional, Tuple

from .char import (
    inject_random_noise,
    random_char_deletion,
    random_char_insertion,
    random_char_substitution,
    random_char_swap,
)
from .homophone import substitute_homophones
from .keyboard import keyboard_typo
from .script import code_mix, transliterate_full, transliterate_random_words
from .span import random_mask, sentence_permutation, span_corruption
from .word import (
    clitic_detachment,
    word_deletion,
    word_dropout,
    word_permute,
    word_replace_synonym,
    word_swap,
)

NOISE_OPS: Dict[str, Dict] = {
    "char_deletion": {"fn": random_char_deletion, "defaults": {"p": 0.05}},
    "char_insertion": {"fn": random_char_insertion, "defaults": {"p": 0.05}},
    "char_swap": {"fn": random_char_swap, "defaults": {"p": 0.05}},
    "char_substitution": {"fn": random_char_substitution, "defaults": {"p": 0.05}},
    "keyboard_typo": {"fn": keyboard_typo, "defaults": {"p": 0.05}},
    "homophone": {"fn": substitute_homophones, "defaults": {"p": 0.2}},
    "word_dropout": {"fn": word_dropout, "defaults": {"ratio": 0.15}},
    "word_deletion": {"fn": word_deletion, "defaults": {"p": 0.1}},
    "word_permute": {"fn": word_permute, "defaults": {"ratio": 0.2}},
    "word_swap": {"fn": word_swap, "defaults": {"n": 1}},
    "clitic_detachment": {"fn": clitic_detachment, "defaults": {}},
    "word_replace_synonym": {"fn": word_replace_synonym, "defaults": {"ratio": 0.2}},
    "transliterate_full": {"fn": transliterate_full, "defaults": {}},
    "transliterate_random_words": {"fn": transliterate_random_words, "defaults": {"ratio": 0.3}},
    "code_mix": {"fn": code_mix, "defaults": {"ratio": 0.3}},
    "span_corruption": {"fn": span_corruption, "defaults": {"corruption_rate": 0.3}},
    "random_mask": {"fn": random_mask, "defaults": {"ratio": 0.15}},
    "sentence_permutation": {"fn": sentence_permutation, "defaults": {"p": 0.5}},
    "inject_random_noise": {"fn": inject_random_noise, "defaults": {"noise_level": 0.1}},
}


def list_noise_ops() -> List[str]:
    """Return the registered noising operator names."""
    return list(NOISE_OPS.keys())


def _make_rng(seed: Optional[int]) -> random.Random:
    return random.Random(seed)


def apply_noising(
    text: str,
    op: str,
    seed: Optional[int] = None,
    **overrides,
) -> str:
    """Apply a single registered noising operator by name."""
    if op not in NOISE_OPS:
        raise KeyError(
            f"Unknown noise op '{op}'. Available: {', '.join(NOISE_OPS)}"
        )
    spec = NOISE_OPS[op]
    kwargs = dict(spec["defaults"])
    kwargs.update(overrides)
    kwargs.setdefault("rng", _make_rng(seed))
    return spec["fn"](text, **kwargs)


def apply_random_noising(
    text: str,
    n: int = 1,
    ops: Optional[List[str]] = None,
    seed: Optional[int] = None,
) -> List[Tuple[str, str]]:
    """Apply ``n`` random noising operators, returning (op_name, noised_text)."""
    r = _make_rng(seed)
    pool = ops or list(NOISE_OPS.keys())
    if not pool:
        raise ValueError("No noising operators available.")
    results = []
    for _ in range(n):
        op = r.choice(pool)
        results.append((op, apply_noising(text, op, seed=r.randrange(1 << 31))))
    return results


def apply_composed_noising(
    text: str,
    ops: List[str],
    seed: Optional[int] = None,
    **overrides,
) -> str:
    """Apply a sequence of noising operators in order."""
    r = _make_rng(seed)
    result = text
    for op in ops:
        result = apply_noising(result, op, seed=r.randrange(1 << 31), **overrides)
    return result


def noise_variants(text: str, seed: Optional[int] = None) -> Dict[str, str]:
    """Apply every registered operator once; returns {op: noised_text}."""
    r = _make_rng(seed)
    variants = {}
    for op in NOISE_OPS:
        variants[op] = apply_noising(text, op, seed=r.randrange(1 << 31))
    return variants
