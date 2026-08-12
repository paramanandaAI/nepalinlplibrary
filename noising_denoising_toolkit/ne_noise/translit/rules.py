"""
Character-tier transliteration: rule-based Devanagari <-> Romanized Nepali.

This is the middle of the hierarchy:
    word (lexicon) -> character (rules) -> model (learned)

Two romanization styles are supported:
  * "nepali" (default): colloquial Nepali romanization, e.g. ई->ee, ऊ->oo,
    word-final inherent schwa dropped (राम -> ram, काम -> kaam).
  * "iast"            : scholarly transcription, ई->ii, ऊ->uu, final schwa kept
    (राम -> raama).

Reverse transliteration is greedy longest-match and restores word-final schwa
(ram -> राम). Ambiguities inherent to ASCII romanization are resolved toward the
more frequent letter (ट/त -> त, ड/द -> द, ण/न -> न); exact words should use the
word or model tier.
"""

import re
from typing import Dict, List, Tuple

from ..text.scripts import CONSONANT_CHARS, HALANT, NUKTA

VOWEL_MAP: Dict[str, str] = {
    "अ": "a", "आ": "aa", "इ": "i", "ई": "ii", "उ": "u", "ऊ": "uu",
    "ऋ": "ri", "ए": "e", "ऐ": "ai", "ओ": "o", "औ": "au",
}
NEPALI_VOWEL_MAP: Dict[str, str] = dict(VOWEL_MAP, **{"ई": "ee", "ऊ": "oo"})

MATRA_MAP: Dict[str, str] = {
    "ा": "aa", "ि": "i", "ी": "ii", "ु": "u", "ू": "uu", "ृ": "ri",
    "े": "e", "ै": "ai", "ो": "o", "ौ": "au",
}
NEPALI_MATRA_MAP: Dict[str, str] = dict(MATRA_MAP, **{"ी": "ee", "ू": "oo"})

NASAL_MAP: Dict[str, str] = {"ं": "n", "ँ": "n", "ः": "h"}

CONSONANT_MAP: Dict[str, str] = {
    "क": "ka", "ख": "kha", "ग": "ga", "घ": "gha", "ङ": "nga",
    "च": "cha", "छ": "chha", "ज": "ja", "झ": "jha", "ञ": "nya",
    "ट": "ta", "ठ": "tha", "ड": "da", "ढ": "dha", "ण": "na",
    "त": "ta", "थ": "tha", "द": "da", "ध": "dha", "न": "na",
    "प": "pa", "फ": "pha", "ब": "ba", "भ": "bha", "म": "ma",
    "य": "ya", "र": "ra", "ल": "la", "व": "wa", "श": "sha",
    "ष": "sha", "स": "sa", "ह": "ha",
}

NUKTA_CONSONANT_MAP: Dict[str, str] = {
    "क़": "qa", "ख़": "kha", "ग़": "ga", "ज़": "za", "फ़": "fa",
    "ड़": "da", "ढ़": "dha",
}

ROMAN_STYLES = ("nepali", "iast")


def _vowel_maps(style: str) -> Tuple[Dict[str, str], Dict[str, str]]:
    if style == "iast":
        return VOWEL_MAP, MATRA_MAP
    return NEPALI_VOWEL_MAP, NEPALI_MATRA_MAP


def _consonant_base(ch: str) -> str:
    """Consonant base sound without the inherent 'a' (क -> k)."""
    with_a = CONSONANT_MAP[ch]
    return with_a[:-1] if with_a.endswith("a") else with_a


# ---------------------------------------------------------------------------
# Devanagari -> Roman
# ---------------------------------------------------------------------------

_VOWEL_GROUP_RE = re.compile(r"[aeiou]{1,}")


def _drop_final_schwa(roman: str) -> str:
    """Colloquial Nepali: drop word-final inherent 'a' (but not 'aa').

    Only words with two or more vowel groups are affected, so single-syllable
    conjuncts like क्ष (ksha) keep their final vowel.
    """
    out = []
    for piece in re.split(r"(\s+)", roman):
        if (
            piece.strip()
            and piece.endswith("a")
            and not piece.endswith("aa")
            and len(_VOWEL_GROUP_RE.findall(piece)) > 1
        ):
            out.append(piece[:-1])
        else:
            out.append(piece)
    return "".join(out)


def transliterate_devanagari_to_roman(text: str, style: str = "nepali") -> str:
    """Convert Devanagari text to Romanized Nepali string (character tier).

    Examples::
        राम    -> raam
        नेपाल  -> nepaal
        काम    -> kaam
        रामले  -> raamale
        नमस्ते -> namaste
    """
    if style not in ROMAN_STYLES:
        style = "nepali"
    vowel_map, matra_map = _vowel_maps(style)

    out: List[str] = []
    i = 0
    n = len(text)
    while i < n:
        ch = text[i]

        if ch in vowel_map:
            out.append(vowel_map[ch])
            i += 1
            continue

        if ch in matra_map or ch in NASAL_MAP:
            out.append(matra_map.get(ch, NASAL_MAP[ch]))
            i += 1
            continue

        if ch in CONSONANT_CHARS:
            cluster: List[str] = []
            while i < n:
                ch2 = text[i]
                if ch2 == NUKTA and cluster:
                    key = text[i - 1] + NUKTA
                    nukta_roman = NUKTA_CONSONANT_MAP.get(key)
                    if nukta_roman:
                        base = nukta_roman[:-1] if nukta_roman.endswith("a") else nukta_roman
                        cluster[-1] = base
                    i += 1
                    continue
                if ch2 not in CONSONANT_CHARS:
                    break
                cluster.append(_consonant_base(ch2))
                i += 1
                if i < n and text[i] == HALANT:
                    i += 1
                    continue
                break

            vowel = ""
            if i < n and text[i] in matra_map:
                vowel = matra_map[text[i]]
                i += 1
            elif i < n and text[i] in NASAL_MAP:
                vowel = NASAL_MAP[text[i]]
                i += 1
            else:
                vowel = "a"

            out.append("".join(cluster) + vowel)
            continue

        out.append(ch)
        i += 1

    roman = "".join(out)
    if style == "nepali":
        roman = _drop_final_schwa(roman)
    return roman


def romanize(text: str, style: str = "nepali") -> str:
    """Convenience alias for transliterate_devanagari_to_roman."""
    return transliterate_devanagari_to_roman(text, style=style)


# ---------------------------------------------------------------------------
# Roman -> Devanagari
# ---------------------------------------------------------------------------

_CONSONANT_FULL: Dict[str, str] = {
    "ksha": "क्ष", "chha": "छ", "gha": "घ", "kha": "ख", "jha": "झ",
    "nya": "ञ", "nga": "ङ", "tra": "त्र", "gya": "ज्ञ", "sra": "श्र",
    "sha": "श", "pha": "फ", "bha": "भ", "tha": "थ", "dha": "ध",
    "ta": "त", "da": "द", "na": "न", "pa": "प", "ba": "ब", "ma": "म",
    "ya": "य", "ra": "र", "la": "ल", "va": "व", "wa": "व", "sa": "स",
    "ha": "ह", "ja": "ज", "cha": "च", "ga": "ग", "ka": "क",
    "qa": "क़", "za": "ज़", "fa": "फ़",
}

_CONSONANT_BARE: Dict[str, str] = {
    "ksh": "क्ष", "chh": "छ", "gh": "घ", "kh": "ख", "jh": "झ", "ny": "ञ",
    "ng": "ङ", "tr": "त्र", "gy": "ज्ञ", "sr": "श्र", "sh": "श", "ph": "फ",
    "bh": "भ", "th": "थ", "dh": "ध", "t": "त", "d": "द", "n": "न",
    "p": "प", "b": "ब", "m": "म", "y": "य", "r": "र", "l": "ल",
    "v": "व", "w": "व", "s": "स", "h": "ह", "j": "ज", "ch": "च",
    "g": "ग", "k": "क", "q": "क़", "z": "ज़", "f": "फ़",
}

# (roman, kind, independent_deva, matra_deva)
_VOWELS: List[Tuple[str, str, str, str]] = [
    ("ai", "V", "ऐ", "ै"), ("au", "V", "औ", "ौ"), ("ee", "V", "ई", "ी"),
    ("ii", "V", "ई", "ी"), ("oo", "V", "ऊ", "ू"), ("uu", "V", "ऊ", "ू"),
    ("aa", "V", "आ", "ा"), ("ri", "V", "ऋ", "ृ"), ("a", "V", "अ", ""),
    ("i", "V", "इ", "ि"), ("u", "V", "उ", "ु"), ("e", "V", "ए", "े"),
    ("o", "V", "ओ", "ो"),
]

_REVERSE_TOKENS: List[Tuple[str, str, str, str]] = []
for _r, _d in _CONSONANT_FULL.items():
    _REVERSE_TOKENS.append((_r, "C", _d, ""))
_REVERSE_TOKENS.extend(_VOWELS)
_REVERSE_TOKENS.sort(key=lambda t: -len(t[0]))

_BARE_TOKENS: List[Tuple[str, str, str, str]] = [
    (r, "C", d, "") for r, d in _CONSONANT_BARE.items()
]
_BARE_TOKENS.sort(key=lambda t: -len(t[0]))

_VOWEL_FINAL_LETTERS = "aeiou"

_ROMAN_WORD_RE = re.compile(r"[a-z]+|[^a-z]+")


def _restore_final_schwa(word: str) -> str:
    """Append a trailing 'a' when a roman word ends on a bare consonant."""
    if not word:
        return word
    if word[-1] in _VOWEL_FINAL_LETTERS:
        return word
    return word + "a"


def _word_roman_to_devanagari(word: str) -> str:
    w = _restore_final_schwa(word.lower())
    result: List[str] = []
    prev_consonant = False
    prev_bare = False
    i = 0
    n = len(w)
    while i < n:
        token = None
        for cand in _REVERSE_TOKENS:
            if w.startswith(cand[0], i):
                if cand[1] == "C":
                    nxt = w[i + len(cand[0]):i + len(cand[0]) + 1]
                    if nxt == "a":
                        continue
                token = cand
                break
        if token:
            kind = token[1]
            if kind == "C":
                result.append(token[2])
                prev_consonant, prev_bare = True, False
            elif kind == "V":
                if prev_consonant and token[3]:
                    result.append(token[3])
                elif not prev_consonant:
                    result.append(token[2])
                prev_consonant, prev_bare = False, False
            i += len(token[0])
            continue

        bare = None
        for cand in _BARE_TOKENS:
            if w.startswith(cand[0], i):
                bare = cand
                break
        if bare:
            if prev_bare:
                result.append(HALANT)
            result.append(bare[2])
            prev_consonant, prev_bare = True, True
            i += len(bare[0])
            continue

        result.append(w[i])
        prev_consonant, prev_bare = False, False
        i += 1

    return "".join(result)


def transliterate_roman_to_devanagari(text: str) -> str:
    """Convert Romanized Nepali text to Devanagari (greedy longest-match).

    Examples::
        ram      -> राम
        nepal    -> नेपाल
        kaam     -> काम
        namaste  -> नमस्ते
        ramale   -> रामले
    """
    out = []
    for piece in _ROMAN_WORD_RE.findall(text):
        if piece[0].isalpha():
            out.append(_word_roman_to_devanagari(piece))
        else:
            out.append(piece)
    return "".join(out)
