import random

from ne_noise.translit.rules import (
    transliterate_devanagari_to_roman,
    transliterate_roman_to_devanagari,
)
from ne_noise.translit.engine import TransliterationEngine, get_default_engine
from ne_noise.translit.lexicon import Lexicon


def test_deva_to_roman_nepali_style():
    assert transliterate_devanagari_to_roman("राम") == "raam"
    assert transliterate_devanagari_to_roman("नेपाल") == "nepaal"
    assert transliterate_devanagari_to_roman("काम") == "kaam"
    assert transliterate_devanagari_to_roman("नमस्ते") == "namaste"
    assert transliterate_devanagari_to_roman("रामले") == "raamale"


def test_deva_to_roman_conjuncts():
    assert transliterate_devanagari_to_roman("क्ष") == "ksha"
    assert transliterate_devanagari_to_roman("प्र") == "pra"


def test_deva_to_roman_iast_keeps_schwa():
    assert transliterate_devanagari_to_roman("राम", style="iast") == "raama"


def test_roman_to_deva_round_trips():
    assert transliterate_roman_to_devanagari("raam") == "राम"
    assert transliterate_roman_to_devanagari("nepaal") == "नेपाल"
    assert transliterate_roman_to_devanagari("kaam") == "काम"
    assert transliterate_roman_to_devanagari("namaste") == "नमस्ते"
    assert transliterate_roman_to_devanagari("raamale") == "रामले"


def test_engine_lexicon_hit_beats_rules():
    engine = TransliterationEngine()
    assert engine.deva_to_roman("काठमाडौँ") == "kathmandu"
    assert engine.deva_to_roman("नेपाल") == "nepal"


def test_engine_rules_fallback():
    engine = TransliterationEngine()
    assert engine.deva_to_roman("जीवन") == "jeewan"


def test_engine_default_singleton():
    assert get_default_engine() is get_default_engine()


def test_lexicon_bidirectional():
    lex = Lexicon()
    lex.load()
    assert lex.deva_to_roman("धन्यवाद") == "dhanyabaad"
    assert lex.roman_to_deva("pokhara") == "पोखरा"


def test_engine_roman_to_deva_lexicon():
    engine = TransliterationEngine()
    assert engine.roman_to_deva("kathmandu") == "काठमाडौँ"
