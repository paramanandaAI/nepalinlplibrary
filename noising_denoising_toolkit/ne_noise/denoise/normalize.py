"""
Rule-based denoising / orthographic canonicalization.

Only unambiguous fixes are applied here (Unicode, artifacts, punctuation).
Homophone correction (श/स, व/ब ...) is word-dependent, so it is left to the
denoising *model* trained on pairs from ``ne_noise.denoise.pairs``.
"""

from ..text.normalize import normalize_nepali_text, remove_zero_width, to_nfc

_UNDO_HOMOPHONE_MAP = {
    "ऋ": "रि",
}


def canonicalize_orthography(text: str) -> str:
    """Best-effort orthographic canonicalization for clean Nepali text.

    - Unicode NFC
    - zero-width / bidi artifact removal
    - whitespace collapse and danda canonicalization
    - unambiguous digraph normalization (ऋ -> रि is left as-is; see notes)

    Example::
        "नेपालको   राजधानी\tकाठमाडौँ।" -> "नेपालको राजधानी काठमाडौँ।"
    """
    return normalize_nepali_text(text)


def denoise_artifacts(text: str) -> str:
    """Remove only machine-introduced artifacts; preserve everything else."""
    return remove_zero_width(to_nfc(text)).strip()
