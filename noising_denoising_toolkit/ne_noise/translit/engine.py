"""
Transliteration engine: the word -> character -> model hierarchy.

Selection order (best first): model (if enabled/available) -> lexicon -> rules.
Every script-level noise operator should go through this engine so experiments can
flip tiers with one argument.
"""

from pathlib import Path
from typing import Optional

from ..text.scripts import contains_devanagari
from .lexicon import Lexicon, lexicon_deva_to_roman, lexicon_roman_to_deva
from .model import TransliterationModel
from .rules import transliterate_devanagari_to_roman, transliterate_roman_to_devanagari


class TransliterationEngine:
    """Tiered Devanagari <-> Roman transliteration."""

    def __init__(
        self,
        lexicon_path: Optional[Path] = None,
        use_model: bool = False,
        model: Optional[TransliterationModel] = None,
        style: str = "nepali",
    ):
        self.style = style
        self.use_model = use_model
        self.model = model or (TransliterationModel() if use_model else None)
        self._lexicon: Optional[Lexicon] = None
        if lexicon_path is not None:
            self._lexicon = Lexicon(path=Path(lexicon_path))
        else:
            self._lexicon = Lexicon()

    @property
    def lexicon(self) -> Optional[Lexicon]:
        if self._lexicon is None:
            return None
        if not self._lexicon.loaded:
            try:
                self._lexicon.load()
            except FileNotFoundError:
                return None
        return self._lexicon

    def deva_to_roman(self, text: str) -> str:
        if self.model_tier_active():
            try:
                return self.model.transliterate(text)
            except Exception:
                pass
        return lexicon_deva_to_roman(text, lexicon=self.lexicon, style=self.style)

    def roman_to_deva(self, text: str) -> str:
        if self.model_tier_active():
            try:
                return self.model.transliterate(text)
            except Exception:
                pass
        return lexicon_roman_to_deva(text, lexicon=self.lexicon)

    def transliterate(self, text: str, direction: str = "auto") -> str:
        """Transliterate text; direction 'dev2rom', 'rom2dev', or 'auto'."""
        if direction == "dev2rom":
            return self.deva_to_roman(text)
        if direction == "rom2dev":
            return self.roman_to_deva(text)
        if contains_devanagari(text):
            return self.deva_to_roman(text)
        return self.roman_to_deva(text)

    def model_tier_active(self) -> bool:
        return bool(self.use_model and self.model and self.model.available())


_engine: Optional[TransliterationEngine] = None


def get_default_engine() -> TransliterationEngine:
    """Process-wide singleton engine (character tier, lexicon if present)."""
    global _engine
    if _engine is None:
        _engine = TransliterationEngine()
    return _engine
