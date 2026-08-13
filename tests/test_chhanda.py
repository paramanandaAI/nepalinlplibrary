"""
Unit Tests for Chhanda Prosody & Meter Scanner (`nepalinlplibrary.library.chhanda`)
"""

import pytest

try:
    from nepalinlplibrary.library.chhanda import devanagari_syllabify, classify_weight, scan_line, analyze_meter
except ModuleNotFoundError:
    from library.chhanda import devanagari_syllabify, classify_weight, scan_line, analyze_meter

def test_syllabification_basic():
    syllables = devanagari_syllabify("कमल नयन")
    assert len(syllables) > 0
    assert "क" in syllables

def test_weight_classification():
    assert classify_weight("क") == "L"
    assert classify_weight("का") == "G"
    assert classify_weight("कं") == "G"

def test_meter_analysis():
    res = analyze_meter("दिई दर्द झन् सर्प डस्दैछ ऐले")
    assert res["syllable_count"] > 0
    assert "scan_pattern" in res
