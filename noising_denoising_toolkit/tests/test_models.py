import pytest
from ne_noise.models.base import BaseNoiser, BaseDenoiser, BaseTransliterator, OptionalModelMixin
from ne_noise.models.huggingface import HFDenoiser, HFTransliterator, load_hf_model, INSTALL_HINT


class DummyNoiser(BaseNoiser):
    def apply(self, text: str) -> str:
        return text + " [noised]"


class DummyDenoiser(BaseDenoiser):
    def apply(self, noised_text: str) -> str:
        return noised_text.replace(" [noised]", "")


def test_base_noiser_and_denoiser():
    noiser = DummyNoiser()
    denoiser = DummyDenoiser()
    assert noiser.available()
    assert denoiser.available()
    text = "नेपाल"
    noised = noiser.apply(text)
    assert noised == "नेपाल [noised]"
    cleaned = denoiser.apply(noised)
    assert cleaned == "नेपाल"


def test_load_hf_model_invalid_kind():
    with pytest.raises(ValueError, match="Unknown model kind"):
        load_hf_model("unknown_kind")


def test_hf_wrappers_instantiation():
    denoiser = HFDenoiser(model_id="t5-small")
    assert denoiser.model_id == "t5-small"
    transliterator = HFTransliterator()
    assert "indictrans2" in transliterator.model_id
