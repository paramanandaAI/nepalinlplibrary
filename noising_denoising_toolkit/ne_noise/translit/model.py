"""
Model-tier transliteration: optional lazy HuggingFace-backed wrapper.

Used for out-of-dictionary words and natural romanization when a transliteration
model is available. Falls back gracefully when models are not installed.

TODO (our_shared_notes/modules/transliteration/indictranslit):
- Integrate IndicTrans2 (ai4bharat/indictrans2-indic-indic) neural model pipeline
  with direction-specific src_lang="ne_Deva" / tgt_lang="ne_Latn" prompt prefixes.
"""

from typing import Optional

SUGGESTED_MODELS = [
    ("ai4bharat/indictrans2-indic-indic", "IndicTrans2: Indic script<->script translation/transliteration"),
    ("ai4bharat/indic-trans", "IndicTrans v1: Indic language translation/transliteration"),
    ("facebook/m2m100_418M", "M2M100: multilingual translation (can transliterate via script transfer)"),
]

INSTALL_HINT = (
    "The model tier requires 'transformers' (and a backend such as torch). "
    "Install with: pip install \"ne-noise[models]\". See ne_noise/models/README.md."
)


class TransliterationModel:
    """Lazy wrapper around a HuggingFace text-to-text transliteration model."""

    def __init__(self, model_id: Optional[str] = None, device: Optional[str] = None):
        self.model_id = model_id or SUGGESTED_MODELS[0][0]
        self.device = device
        self._pipeline = None

    def available(self) -> bool:
        """True if transformers is installed and the pipeline can be built."""
        try:
            import transformers  # noqa: F401
        except ImportError:
            return False
        try:
            self.load()
            return True
        except Exception:
            return False

    def load(self):
        if self._pipeline is not None:
            return self._pipeline
        try:
            from transformers import pipeline
        except ImportError as exc:
            raise ImportError(INSTALL_HINT) from exc
        self._pipeline = pipeline(
            "text2text-generation",
            model=self.model_id,
            device=self.device,
        )
        return self._pipeline

    def transliterate(self, text: str, direction: str = "auto") -> str:
        """Transliterate using the loaded model (direction currently model-dependent)."""
        pipe = self.load()
        out = pipe(
            text,
            max_length=512,
            do_sample=False,
        )
        if isinstance(out, list) and out and "generated_text" in out[0]:
            return out[0]["generated_text"]
        return str(out)
