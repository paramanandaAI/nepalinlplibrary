from pathlib import Path

from ne_noise.denoise.pairs import make_pairs, make_pairs_from_records, write_jsonl, read_jsonl, NoisePair
from ne_noise.denoise.normalize import canonicalize_orthography, denoise_artifacts

SENTENCES = [
    "नेपालको राजधानी काठमाडौँ हो।",
    "उनले विद्यालयमा नयाँ किताब पढे।",
]


def test_make_pairs_count():
    pairs = make_pairs(SENTENCES, k=2, seed=1)
    assert len(pairs) == 4
    assert all(isinstance(p, NoisePair) for p in pairs)


def test_make_pairs_deterministic():
    a = make_pairs(SENTENCES, k=1, seed=9)
    b = make_pairs(SENTENCES, k=1, seed=9)
    assert [p.dict() for p in a] == [p.dict() for p in b]


def test_pairs_are_noised():
    pairs = make_pairs(SENTENCES, k=1, seed=3)
    changed = [p for p in pairs if p.noised != p.clean]
    assert len(changed) >= 1


def test_pair_has_id_and_ops():
    pairs = make_pairs(SENTENCES, k=1, seed=3)
    for p in pairs:
        assert p.id
        assert p.ops


def test_jsonl_round_trip(tmp_path: Path):
    pairs = make_pairs(SENTENCES, k=1, seed=2)
    path = tmp_path / "pairs.jsonl"
    write_jsonl(pairs, path)
    loaded = read_jsonl(path)
    assert len(loaded) == len(pairs)
    assert loaded[0]["clean"] == pairs[0].clean


def test_make_pairs_from_records():
    records = [{"id": "x", "text": t} for t in SENTENCES]
    pairs = make_pairs_from_records(records, text_field="text", k=1, seed=4)
    assert len(pairs) == 2


def test_canonicalize_orthography():
    assert canonicalize_orthography("नेपालको   राजधानी\tकाठमाडौँ।\u200b") == "नेपालको राजधानी काठमाडौँ।"


def test_denoise_artifacts():
    assert denoise_artifacts("राम\u200b\u200dसीता") == "रामसीता"
