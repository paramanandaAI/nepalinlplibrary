import pytest

from ne_noise.noise.engine import (
    NOISE_OPS,
    apply_noising,
    apply_composed_noising,
    apply_random_noising,
    list_noise_ops,
    noise_variants,
)


def test_list_ops_nonempty():
    ops = list_noise_ops()
    assert len(ops) >= 15
    assert set(ops) == set(NOISE_OPS.keys())


def test_unknown_op_raises():
    with pytest.raises(KeyError):
        apply_noising("राम", op="not_an_op")


def test_apply_noising_deterministic():
    a = apply_noising("नेपालको राजधानी काठमाडौँ हो।", op="char_swap", seed=42)
    b = apply_noising("नेपालको राजधानी काठमाडौँ हो।", op="char_swap", seed=42)
    assert a == b


def test_apply_random_noising_returns_pairs():
    results = apply_random_noising("नेपालको राजधानी काठमाडौँ हो।", n=3, seed=42)
    assert len(results) == 3
    for op, text in results:
        assert op in NOISE_OPS
        assert isinstance(text, str)


def test_apply_composed_noising():
    out = apply_composed_noising("नेपालको राजधानी काठमाडौँ हो।", ops=["word_permute", "char_swap"], seed=1)
    assert isinstance(out, str)


def test_noise_variants_covers_all_ops():
    variants = noise_variants("राम")
    assert set(variants.keys()) == set(NOISE_OPS.keys())
