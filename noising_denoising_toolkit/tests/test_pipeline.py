import json
from pathlib import Path

from ne_noise.pipelines.noising_pipeline import NoisingPipeline


def test_pipeline_end_to_end(tmp_path: Path):
    src = tmp_path / "in.jsonl"
    dst = tmp_path / "out.jsonl"
    rows = [
        {"id": "1", "text": "नेपालको राजधानी काठमाडौँ हो।"},
        {"id": "2", "text": "उनले विद्यालयमा नयाँ किताब पढे।"},
    ]
    with open(src, "w", encoding="utf-8") as f:
        for r in rows:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")

    report = NoisingPipeline(k=2, seed=5).run(src, dst)

    assert report["status"] == "SUCCESS"
    assert report["input_records"] == 2
    assert report["output_pairs"] == 4

    with open(dst, "r", encoding="utf-8") as f:
        lines = [line for line in f if line.strip()]
    assert len(lines) == 4
    first = json.loads(lines[0])
    assert "clean" in first and "noised" in first and "ops" in first


def test_pipeline_sample_limit(tmp_path: Path):
    src = tmp_path / "in.jsonl"
    dst = tmp_path / "out.jsonl"
    with open(src, "w", encoding="utf-8") as f:
        for i in range(5):
            f.write(json.dumps({"id": str(i), "text": f"नेपालको राजधानी हो। {i}"}, ensure_ascii=False) + "\n")

    report = NoisingPipeline(k=1, seed=0).run(src, dst, sample=2)
    assert report["input_records"] == 2
