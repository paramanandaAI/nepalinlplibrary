import random

from ne_noise.noise.script import code_mix, transliterate_full, transliterate_random_words
from ne_noise.noise.span import span_corruption, random_mask, sentence_permutation
from ne_noise.text.scripts import contains_devanagari


def test_transliterate_full():
    out = transliterate_full("नेपाल")
    assert not contains_devanagari(out)


def test_transliterate_random_words_ratio1_all_roman():
    out = transliterate_random_words("नेपालको राजधानी काठमाडौँ हो", ratio=1.0, rng=random.Random(0))
    assert not contains_devanagari(out)


def test_code_mix_mixes_scripts():
    out = code_mix("नेपालको राजधानी काठमाडौँ हो", ratio=1.0, rng=random.Random(0))
    assert not contains_devanagari(out)


def test_code_mix_deterministic():
    a = code_mix("नेपालको राजधानी काठमाडौँ हो", ratio=0.5, rng=random.Random(7))
    b = code_mix("नेपालको राजधानी काठमाडौँ हो", ratio=0.5, rng=random.Random(7))
    assert a == b


def test_span_corruption_ratio0_identity():
    assert span_corruption("एक दुई तीन चार", corruption_rate=0.0, rng=random.Random(0)) == "एक दुई तीन चार"


def test_span_corruption_ratio1_all_masked():
    assert span_corruption("एक दुई तीन चार", corruption_rate=1.0, rng=random.Random(0)) == "<mask>"


def test_span_corruption_contains_mask():
    out = span_corruption("एक दुई तीन चार पाँच छ सात", corruption_rate=0.5, rng=random.Random(1))
    assert "<mask>" in out


def test_random_mask_ratio1():
    assert random_mask("एक दुई तीन", ratio=1.0, rng=random.Random(0)) == "<mask> <mask> <mask>"


def test_sentence_permutation():
    text = "एक। दुई। तीन।"
    out = sentence_permutation(text, p=1.0, rng=random.Random(0))
    assert set(out.split()) == set(text.split())
