"""Nepali text normalization: Unicode cleanup, whitespace, danda canonicalization."""

import re
import unicodedata

ZERO_WIDTH_CHARS = "\u200b\u200c\u200d\u200e\u200f\ufeff\u00ad"

_WS_RE = re.compile(r"[ \t]+")
_NEWLINE_RE = re.compile(r"\n{3,}")


def remove_zero_width(text: str) -> str:
    """Remove zero-width / bidi / soft-hyphen artifacts."""
    if not text:
        return text
    return "".join(ch for ch in text if ch not in ZERO_WIDTH_CHARS)


def collapse_whitespace(text: str) -> str:
    """Collapse runs of spaces/tabs to one and trim; limit blank lines."""
    text = _WS_RE.sub(" ", text)
    text = _NEWLINE_RE.sub("\n\n", text)
    return text.strip()


def normalize_danda(text: str) -> str:
    """Canonicalize punctuation: ASCII bar -> danda, common danda variants."""
    return text.replace("|", "।")


def to_nfc(text: str) -> str:
    """Unicode NFC normalization (composition)."""
    return unicodedata.normalize("NFC", text)


def normalize_nepali_text(text: str) -> str:
    """Canonical Nepali text normalization (superset of the legacy transformer).

    - zero-width / bidi / soft-hyphen artifacts removed
    - NFC composition
    - whitespace collapsed
    - ASCII bar folded to danda
    """
    if not isinstance(text, str):
        return str(text)
    return normalize_danda(collapse_whitespace(remove_zero_width(to_nfc(text))))
