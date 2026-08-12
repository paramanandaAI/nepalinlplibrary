import random

from ne_noise.noise.char import (
    random_char_deletion,
    random_char_insertion,
    random_char_swap,
    random_char_substitution,
    inject_random_noise,
)
from ne_noise.noise.homophone import substitute_homophones, HOMOPHONE_MAP
from ne_noise.noise.keyboard import keyboard_typo


def test_deletion_p0_is_identity():
    assert random_char_deletion("राम सीता", p=0.0, rng=random.Random(0)) == "राम सीता"


def test_deletion_p1_keeps_only_spaces():
    assert random_char_deletion("राम हो", p=1.0, rng=random.Random(0)) == " "


def test_insertion_grows_text():
    out = random_char_insertion("राम", p=1.0, rng=random.Random(0))
    assert len(out) >= len("राम")


def test_swap_deterministic():
    a = random_char_swap("काठमाडौँ", p=0.5, rng=random.Random(3))
    b = random_char_swap("काठमाडौँ", p=0.5, rng=random.Random(3))
    assert a == b


def test_substitution_changes_some_chars():
    out = random_char_substitution("नेपालकी राजधानी", p=1.0, rng=random.Random(1))
    assert out != "नेपालकी राजधानी"


def test_inject_random_noise_deterministic():
    a = inject_random_noise("नेपालको राजधानी काठमाडौँ हो।", noise_level=0.1, rng=random.Random(5))
    b = inject_random_noise("नेपालको राजधानी काठमाडौँ हो।", noise_level=0.1, rng=random.Random(5))
    assert a == b


def test_homophone_substitution():
    assert substitute_homophones("शहर", p=1.0, rng=random.Random(0)) != "शहर"
    assert "स" in HOMOPHONE_MAP["श"]


def test_keyboard_typo_deterministic():
    a = keyboard_typo("काठमाडौँ", p=0.5, rng=random.Random(2))
    b = keyboard_typo("काठमाडौँ", p=0.5, rng=random.Random(2))
    assert a == b
