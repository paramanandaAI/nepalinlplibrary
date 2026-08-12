"""Nepali text primitives: Devanagari Unicode constants and script helpers."""

DEVANAGARI_START = 0x0900
DEVANAGARI_END = 0x097F
DEVANAGARI_EXT_START = 0xA8E0
DEVANAGARI_EXT_END = 0xA8FF

INDEPENDENT_VOWELS = "अआइईउऊऋएऐओऔ"
DEPENDENT_MATRAS = "ािीुूृेैोौ"
CONSONANTS = "कखगघङचछजझञटठडढणतथदधनपफबभमयरलवशषसह"
ANUSVARA = "ं"
CHANDRABINDU = "ँ"
VISARGA = "ः"
HALANT = "्"
NUKTA = "़"
DANDA = "।"
DOUBLE_DANDA = "॥"

NUKTA_BASE = "कखगजफडढ"

VOWEL_CHARS = set(INDEPENDENT_VOWELS)
MATRA_CHARS = set(DEPENDENT_MATRAS)
CONSONANT_CHARS = set(CONSONANTS)


def is_devanagari_char(ch: str) -> bool:
    """True if the character is inside the Devanagari Unicode block."""
    cp = ord(ch)
    return (
        DEVANAGARI_START <= cp <= DEVANAGARI_END
        or DEVANAGARI_EXT_START <= cp <= DEVANAGARI_EXT_END
    )


def contains_devanagari(text: str) -> bool:
    """True if the text contains at least one Devanagari character."""
    return any(is_devanagari_char(ch) for ch in text)


def is_devanagari(text: str) -> bool:
    """True if the text consists only of Devanagari letters, digits, spaces and punctuation."""
    if not text or not text.strip():
        return False
    return all(is_devanagari_char(ch) or ch.isspace() or ch in ".,!?;:।॥-–—()\"'%" for ch in text)


def devanagari_ratio(text: str) -> float:
    """Proportion of non-whitespace, non-digit characters that are Devanagari."""
    if not text:
        return 0.0
    deva = sum(1 for ch in text if is_devanagari_char(ch))
    alpha = sum(1 for ch in text if not ch.isspace() and not ch.isdigit())
    if alpha == 0:
        return 1.0 if deva > 0 else 0.0
    return deva / alpha


def char_category(ch: str) -> str:
    """Classify a Devanagari character: vowel, matra, consonant, nasal, other."""
    if ch in VOWEL_CHARS:
        return "vowel"
    if ch in MATRA_CHARS:
        return "matra"
    if ch in CONSONANT_CHARS:
        return "consonant"
    if ch in (ANUSVARA, CHANDRABINDU, VISARGA):
        return "nasal"
    if ch == HALANT:
        return "halant"
    return "other"


def word_tokens(text: str):
    """Split text into words (whitespace-separated), preserving order."""
    return text.split()
