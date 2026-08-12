"""Wrapper interfaces for pretrained noising/denoising/transliteration backends."""

from abc import ABC, abstractmethod
from typing import Optional


class BaseNoiser(ABC):
    """A backend that adds noise to text (e.g., an LLM producing typos)."""

    @abstractmethod
    def apply(self, text: str) -> str:
        raise NotImplementedError

    def available(self) -> bool:
        return True


class BaseDenoiser(ABC):
    """A backend that recovers clean text from noised input."""

    @abstractmethod
    def apply(self, noised_text: str) -> str:
        raise NotImplementedError

    def available(self) -> bool:
        return True


class BaseTransliterator(ABC):
    """A backend that converts between Devanagari and Roman scripts."""

    @abstractmethod
    def deva_to_roman(self, text: str) -> str:
        raise NotImplementedError

    @abstractmethod
    def roman_to_deva(self, text: str) -> str:
        raise NotImplementedError

    def available(self) -> bool:
        return True


class OptionalModelMixin:
    """Mixin for backends that are not installed by default."""

    _error: Optional[Exception] = None

    def available(self) -> bool:
        return self._error is None
