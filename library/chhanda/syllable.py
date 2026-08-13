"""
Devanagari Prosody & Syllabification Engine (`nepalinlplibrary.library.chhanda.syllable`)

Classifies syllables into Laghu (ह्रस्व / Light - 'L') and Guru (दीर्घ / Heavy - 'G').
"""

import re
from typing import List, Tuple

# Matras & Vowel Weights
SHORT_MATRAS = set("िु")
LONG_MATRAS = set("ाीूेैोौ")
SPECIAL_MODIFIERS = set("ंः")

DEPENDENT_MATRAS = set("ािीुूेैोौ")

def devanagari_syllabify(text: str) -> List[str]:
    """Break Devanagari text into prosodic syllables."""
    if not text:
        return []
    
    # Tokenize Devanagari words into phonetic syllables
    words = text.strip().split()
    syllables = []
    
    for word in words:
        chars = list(word)
        curr = ""
        for i, ch in enumerate(chars):
            curr += ch
            # Break boundary if next char is independent vowel or consonant without halanta
            if ch == "्":
                continue
            if i == len(chars) - 1 or chars[i + 1] not in DEPENDENT_MATRAS and chars[i + 1] != "्":
                syllables.append(curr)
                curr = ""
        if curr:
            syllables.append(curr)
            
    return [s for s in syllables if s.strip()]


def classify_weight(syllable: str) -> str:
    """
    Determines prosodic weight of a syllable:
    - 'L' (Laghu / ह्रस्व / Light)
    - 'G' (Guru / दीर्घ / Heavy)
    """
    s = syllable.strip()
    if not s:
        return "L"
        
    # Long matra or anusvara/visarga makes it Guru ('G')
    if any(m in s for m in LONG_MATRAS) or any(m in s for m in SPECIAL_MODIFIERS):
        return "G"
        
    # Conjunct ending or double consonant makes it Guru ('G')
    if "्" in s and not s.endswith("्"):
        return "G"
        
    return "L"


def scan_line(text: str) -> Tuple[List[str], str]:
    """Scan a Devanagari line returning (syllables, scan_pattern)."""
    syllables = devanagari_syllabify(text)
    pattern = "".join(classify_weight(s) for s in syllables)
    return syllables, pattern
