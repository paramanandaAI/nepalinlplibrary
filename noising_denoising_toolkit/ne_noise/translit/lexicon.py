"""
Word-tier transliteration: dataset-backed Devanagari <-> Roman dictionary.

Provides O(1) word lookup. Falls back to the character tier for out-of-dictionary
words. A small sample lexicon ships in ``data/``; the full ~2.4M pair dataset is
downloaded via ``ne_noise/scripts/download_word_transliteration.py`` (big data is
kept outside the library).
"""

import csv
from pathlib import Path
from typing import Dict, Optional

from .rules import transliterate_devanagari_to_roman, transliterate_roman_to_devanagari

DEFAULT_LEXICON_PATH = Path(__file__).resolve().parent / "data" / "nepali_roman_word.csv"

_DEFAULT_CSV_HEADER = ("native word", "english word")


class Lexicon:
    """A bidirectional word-level transliteration dictionary."""

    def __init__(
        self,
        path: Path = DEFAULT_LEXICON_PATH,
        deva_col: str = "native word",
        roman_col: str = "english word",
    ):
        self.path = Path(path)
        self.deva_col = deva_col
        self.roman_col = roman_col
        self._deva_to_roman: Dict[str, str] = {}
        self._roman_to_deva: Dict[str, str] = {}
        self._loaded = False

    def load(self) -> "Lexicon":
        if self._loaded:
            return self
        if not self.path.exists():
            raise FileNotFoundError(
                f"Transliteration lexicon not found at '{self.path}'. "
                f"Run 'ne_noise/scripts/download_word_transliteration.py' or point "
                f"Lexicon(path=...) at an existing CSV."
            )
        with open(self.path, "r", encoding="utf-8", newline="") as f:
            reader = csv.DictReader(f)
            for row in reader:
                deva = (row.get(self.deva_col) or "").strip()
                roman = (row.get(self.roman_col) or "").strip()
                if not deva or not roman:
                    continue
                self._deva_to_roman[deva] = roman
                self._roman_to_deva.setdefault(roman.lower(), deva)
        self._loaded = True
        return self

    @property
    def loaded(self) -> bool:
        return self._loaded

    def __len__(self) -> int:
        return len(self._deva_to_roman)

    def has_deva(self, word: str) -> bool:
        return word.strip() in self._deva_to_roman

    def has_roman(self, word: str) -> bool:
        return word.strip().lower() in self._roman_to_deva

    def deva_to_roman(self, word: str) -> Optional[str]:
        """Look up a Devanagari word; None if not present."""
        return self._deva_to_roman.get(word.strip())

    def roman_to_deva(self, word: str) -> Optional[str]:
        """Look up a Romanized word; None if not present."""
        return self._roman_to_deva.get(word.strip().lower())


def lexicon_deva_to_roman(
    text: str,
    lexicon: Optional[Lexicon] = None,
    style: str = "nepali",
) -> str:
    """Word-level Devanagari -> Roman with character-tier fallback per word."""
    lexicon = lexicon or Lexicon()
    if not lexicon.loaded:
        try:
            lexicon.load()
        except FileNotFoundError:
            lexicon = None

    words = text.split()
    out = []
    for word in words:
        hit = lexicon.deva_to_roman(word) if lexicon else None
        out.append(hit if hit else transliterate_devanagari_to_roman(word, style=style))
    return " ".join(out)


def lexicon_roman_to_deva(
    text: str,
    lexicon: Optional[Lexicon] = None,
) -> str:
    """Word-level Roman -> Devanagari with character-tier fallback per word."""
    lexicon = lexicon or Lexicon()
    if not lexicon.loaded:
        try:
            lexicon.load()
        except FileNotFoundError:
            lexicon = None

    words = text.split()
    out = []
    for word in words:
        hit = lexicon.roman_to_deva(word) if lexicon else None
        out.append(hit if hit else transliterate_roman_to_devanagari(word))
    return " ".join(out)
