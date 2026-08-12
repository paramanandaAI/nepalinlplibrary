"""
Lazy HuggingFace-backed model wrappers for denoising and transliteration.

Heavy dependencies (transformers, torch) are imported only on demand. Call
``available()`` before use, or catch the descriptive ImportError.
"""

from typing import Dict, Optional

from .base import BaseDenoiser, BaseTransliterator, OptionalModelMixin

INSTALL_HINT = (
    "The model tier requires 'transformers' and a backend (torch). "
    "Install with: pip install \"ne-noise[models]\". "
    "See ne_noise/models/README.md for the full guide."
)

DENOISER_DEFAULTS: Dict[str, str] = {
    "t5-small": "T5-small, general text-to-text (denoising/span corruption pretraining).",
    "t5-base": "T5-base, general text-to-text.",
    "facebook/bart-base": "BART-base, denoising pretraining family.",
}

TRANSLIT_DEFAULTS: Dict[str, str] = {
    "ai4bharat/indictrans2-indic-indic": "IndicTrans2 Indic<->Indic (script conversion).",
    "facebook/m2m100_418M": "M2M100 multilingual translation.",
}


class HFDenoiser(BaseDenoiser, OptionalModelMixin):
    """Text-to-text denoiser backed by a HuggingFace seq2seq model."""

    def __init__(self, model_id: str = "t5-small", device: Optional[str] = None):
        self.model_id = model_id
        self.device = device
        self._pipeline = None

    def _load(self):
        if self._pipeline is not None:
            return self._pipeline
        try:
            from transformers import pipeline
        except ImportError as exc:
            self._error = exc
            raise ImportError(INSTALL_HINT) from exc
        self._pipeline = pipeline(
            "text2text-generation", model=self.model_id, device=self.device
        )
        return self._pipeline

    def apply(self, noised_text: str) -> str:
        out = self._load()(noised_text, max_length=512, do_sample=False)
        if isinstance(out, list) and out and "generated_text" in out[0]:
            return out[0]["generated_text"]
        return str(out)


class HFTransliterator(BaseTransliterator, OptionalModelMixin):
    """Transliteration backend backed by a HuggingFace model."""

    def __init__(self, model_id: str = "ai4bharat/indictrans2-indic-indic", device: Optional[str] = None):
        self.model_id = model_id
        self.device = device
        self._model = None
        self._tokenizer = None

    def _load(self):
        if self._model is not None:
            return self._model, self._tokenizer
        try:
            from transformers import AutoModelForSeq2SeqLM, AutoTokenizer
        except ImportError as exc:
            self._error = exc
            raise ImportError(INSTALL_HINT) from exc
        self._tokenizer = AutoTokenizer.from_pretrained(self.model_id)
        self._model = AutoModelForSeq2SeqLM.from_pretrained(self.model_id)
        return self._model, self._tokenizer

    def _translate(self, text: str, src: str, tgt: str) -> str:
        model, tokenizer = self._load()
        prompt = f"<<2{tgt}>> {text}"
        encoded = tokenizer(prompt, return_tensors="pt")
        out = model.generate(**encoded, max_length=512)
        return tokenizer.decode(out[0], skip_special_tokens=True)

    def deva_to_roman(self, text: str) -> str:
        return self._translate(text, src="deva", tgt="latn")

    def roman_to_deva(self, text: str) -> str:
        return self._translate(text, src="latn", tgt="deva")


def load_hf_model(kind: str, model_id: Optional[str] = None, **kwargs):
    """Load a model wrapper by kind: ``denoiser`` or ``transliterator``."""
    if kind == "denoiser":
        return HFDenoiser(model_id or next(iter(DENOISER_DEFAULTS)), **kwargs)
    if kind == "transliterator":
        return HFTransliterator(model_id or next(iter(TRANSLIT_DEFAULTS)), **kwargs)
    raise ValueError(f"Unknown model kind '{kind}'. Choose from 'denoiser', 'transliterator'.")
