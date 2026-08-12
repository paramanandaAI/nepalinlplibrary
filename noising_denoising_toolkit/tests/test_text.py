import pytest

from ne_noise.text.normalize import normalize_nepali_text
from ne_noise.text.scripts import (
    devanagari_ratio,
    is_devanagari,
    is_devanagari_char,
    contains_devanagari,
    char_category,
)


def test_normalize_removes_zero_width():
    assert normalize_nepali_text("राम\u200bसिता") == "रामसिता"
    assert normalize_nepali_text("नेपाल\ufeff") == "नेपाल"


def test_normalize_collapses_whitespace():
    assert normalize_nepali_text("नेपालको   राजधानी\tकाठमाडौँ।") == "नेपालको राजधानी काठमाडौँ।"


def test_normalize_folds_bar_to_danda():
    assert normalize_nepali_text("एक| दुई।") == "एक। दुई।"


def test_normalize_nfc():
    assert normalize_nepali_text("\u0915\u093c") == "क़"


def test_devanagari_ratio():
    assert devanagari_ratio("नेपाल") == 1.0
    assert devanagari_ratio("namaste") == 0.0
    assert devanagari_ratio("") == 0.0
    assert 0.3 < devanagari_ratio("नेपाल namaste") < 0.6


def test_is_devanagari():
    assert is_devanagari("राम")
    assert is_devanagari("नेपालको राजधानी काठमाडौँ।")
    assert not is_devanagari("ram")
    assert not is_devanagari("")


def test_contains_and_char_category():
    assert contains_devanagari("a ने")
    assert not contains_devanagari("abc")
    assert char_category("क") == "consonant"
    assert char_category("ा") == "matra"
    assert char_category("अ") == "vowel"
    assert char_category("x") == "other"
