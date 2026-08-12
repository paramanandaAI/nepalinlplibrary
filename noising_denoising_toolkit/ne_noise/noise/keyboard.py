"""Phonetic-keyboard neighbor typos for Devanagari (Nepali).

Simulates a user hitting a nearby key on a phonetic Nepali layout. The map below
is a curated set of the most common confusions; extend ``KEYBOARD_NEIGHBORS`` with
your keyboard layout if needed.
"""

from typing import Dict, List, Optional
import random

KEYBOARD_NEIGHBORS: Dict[str, List[str]] = {
    "क": ["ख", "ग", "च"],
    "ख": ["क", "ग", "घ"],
    "ग": ["क", "ख", "घ"],
    "घ": ["ग", "ख", "ङ"],
    "च": ["क", "छ", "ज"],
    "छ": ["च", "ज"],
    "ज": ["च", "छ", "झ", "ह"],
    "झ": ["ज", "छ"],
    "ट": ["ठ", "ड"],
    "ठ": ["ट", "ड", "ढ"],
    "ड": ["ट", "ठ", "ढ"],
    "ढ": ["ड", "ठ"],
    "त": ["थ", "द", "न"],
    "थ": ["त", "द"],
    "द": ["त", "थ", "ध", "न"],
    "ध": ["द", "थ"],
    "न": ["त", "द", "ण", "म"],
    "प": ["फ", "ब"],
    "फ": ["प", "भ", "ब"],
    "ब": ["प", "फ", "भ", "व"],
    "भ": ["ब", "फ", "म"],
    "म": ["न", "य", "भ"],
    "य": ["म", "र"],
    "र": ["य", "ल"],
    "ल": ["र", "व"],
    "व": ["ल", "ब", "स"],
    "स": ["श", "ष", "व"],
    "श": ["स", "ष"],
    "ष": ["स", "श"],
    "ह": ["ज", "य"],
    "ि": ["ी"],
    "ी": ["ि"],
    "ु": ["ू"],
    "ू": ["ु"],
    "े": ["ो"],
    "ो": ["े"],
    "ै": ["ौ"],
    "ौ": ["ै"],
}


def keyboard_typo(
    text: str,
    p: float = 0.05,
    rng: Optional[random.Random] = None,
) -> str:
    """Inject keyboard-neighbor substitution typos with probability ``p``."""
    from .char import random_typo_injection

    return random_typo_injection(text, p=p, rng=rng, neighbors=KEYBOARD_NEIGHBORS)
