import random

from ne_noise.noise.word import (
    clitic_detachment,
    word_deletion,
    word_dropout,
    word_permute,
    word_replace_synonym,
    word_swap,
)


def test_clitic_detachment():
    assert clitic_detachment("रामले काठमाडौँमा") == "राम ले काठमाडौँ मा"


def test_word_deletion_keeps_one_word():
    assert word_deletion("एक दुई तीन चार", p=1.0, rng=random.Random(0)) in ["एक", "दुई", "तीन", "चार"]


def test_word_dropout_p0_identity():
    assert word_dropout("एक दुई तीन", ratio=0.0, rng=random.Random(0)) == "एक दुई तीन"


def test_word_swap_changes_order():
    out = word_swap("एक दुई तीन चार", n=1, rng=random.Random(0))
    assert out != "एक दुई तीन चार"


def test_word_permute_deterministic():
    a = word_permute("एक दुई तीन चार पाँच", ratio=1.0, rng=random.Random(4))
    b = word_permute("एक दुई तीन चार पाँच", ratio=1.0, rng=random.Random(4))
    assert a == b


def test_word_replace_synonym():
    out = word_replace_synonym("घर पानी राम्रो", ratio=1.0, rng=random.Random(0))
    assert out != "घर पानी राम्रो"
    assert "गृह" in out or "जल" in out or "सुन्दर" in out


def test_word_swap_single_word_identity():
    assert word_swap("राम", n=1, rng=random.Random(0)) == "राम"
