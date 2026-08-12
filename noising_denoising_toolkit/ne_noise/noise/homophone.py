"""Homophone / orthographic-confusion noising for Nepali (श/ष/स, व/ब, ...)."""

import random
from typing import Dict, List, Optional

HOMOPHONE_MAP: Dict[str, List[str]] = {
    "श": ["स", "ष"],
    "ष": ["स", "श"],
    "स": ["श", "ष"],
    "इ": ["ई"],
    "ई": ["इ"],
    "उ": ["ऊ"],
    "ऊ": ["उ"],
    "ि": ["ी"],
    "ी": ["ि"],
    "ु": ["ू"],
    "ू": ["ु"],
    "व": ["ब"],
    "ब": ["व"],
    "ऋ": ["रि"],
    "रि": ["ऋ"],
    "ज्ञ": ["ग्य"],
    "क्ष": ["छ्य"],
    "ं": ["ँ", "न्"],
    "ँ": ["ं"],
}


def get_homophone_map() -> Dict[str, List[str]]:
    """Return the Nepali homophone confusion pairs."""
    return dict(HOMOPHONE_MAP)


def substitute_homophones(
    text: str,
    p: float = 0.2,
    rng: Optional[random.Random] = None,
    homophone_map: Optional[Dict[str, List[str]]] = None,
) -> str:
    """Substitute homophone/orthographic confusable characters with probability ``p``.

    Example::
        "शहरी विकास" -> "सहरी बिकास"
    """
    hm = homophone_map or HOMOPHONE_MAP
    r = rng if rng is not None else random
    chars = list(text)
    for i, ch in enumerate(chars):
        if ch in hm and r.random() < p:
            chars[i] = r.choice(hm[ch])
    return "".join(chars)
