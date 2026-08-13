"""
Nepali GEC Dataset Downloader and SFT JSONL Exporter
Downloads Hugging Face GEC datasets and formats them into standardized SFT JSONL format.
"""

import argparse
import json
from pathlib import Path
from typing import Optional
from datasets import load_dataset

SCRIPT_DIR = Path(__file__).resolve().parent


def generate_sumitaryal_gec_jsonl(output_path: Path, limit: Optional[int] = 100) -> None:
    """Generates SFT JSONL file for GEC from sumitaryal/nepali_grammatical_error_correction."""
    print("Loading 'sumitaryal/nepali_grammatical_error_correction'...")
    try:
        ds = load_dataset("sumitaryal/nepali_grammatical_error_correction", split="train")
    except Exception as e:
        print(f"Error loading sumitaryal GEC dataset: {e}")
        return

    records = []
    max_count = limit if limit else len(ds)
    for idx, sample in enumerate(ds):
        if idx >= max_count:
            break

        inp = sample.get("incorrect") or sample.get("input") or ""
        out = sample.get("correct") or sample.get("output") or ""

        if not inp or not out:
            continue

        records.append({
            "id": f"gec-sumitaryal-{idx+1}",
            "instruction": "तल दिइएको नेपाली वाक्यको व्याकरण सच्याउनुहोस्।",
            "input": str(inp).strip(),
            "output": str(out).strip(),
            "language": "ne",
            "script": "Devanagari",
            "task": "sft/gec/grammatical_error_correction",
            "source": "huggingface.co/datasets/sumitaryal/nepali_grammatical_error_correction",
            "license": "open"
        })

    print(f"Writing {len(records)} records to {output_path}...")
    with open(output_path, "w", encoding="utf-8") as f:
        for rec in records:
            f.write(json.dumps(rec, ensure_ascii=False) + "\n")
    print(f"Successfully generated {output_path}")


def generate_sumitaryal_detection_jsonl(output_path: Path, limit: Optional[int] = 100) -> None:
    """Generates SFT JSONL file for Error Detection from sumitaryal/nepali_grammatical_error_detection."""
    print("Loading 'sumitaryal/nepali_grammatical_error_detection'...")
    try:
        ds = load_dataset("sumitaryal/nepali_grammatical_error_detection", split="train")
    except Exception as e:
        print(f"Error loading sumitaryal detection dataset: {e}")
        return

    records = []
    max_count = limit if limit else len(ds)
    for idx, sample in enumerate(ds):
        if idx >= max_count:
            break

        sentence = sample.get("sentence") or sample.get("input") or ""
        has_error = sample.get("has_error") if "has_error" in sample else sample.get("label")

        if not sentence:
            continue

        status_str = "अशुद्ध (त्रुटिपूर्ण)" if has_error else "शुद्ध (त्रुटिरहित)"

        records.append({
            "id": f"gec-detect-{idx+1}",
            "instruction": "के यो नेपाली वाक्य व्याकरणिक रूपमा सही छ?",
            "input": str(sentence).strip(),
            "output": status_str,
            "has_error": bool(has_error),
            "language": "ne",
            "script": "Devanagari",
            "task": "sft/gec/error_detection",
            "source": "huggingface.co/datasets/sumitaryal/nepali_grammatical_error_detection",
            "license": "open"
        })

    print(f"Writing {len(records)} records to {output_path}...")
    with open(output_path, "w", encoding="utf-8") as f:
        for rec in records:
            f.write(json.dumps(rec, ensure_ascii=False) + "\n")
    print(f"Successfully generated {output_path}")


def generate_cfilt_ocr_jsonl(output_path: Path, limit: Optional[int] = 100) -> None:
    """Generates SFT JSONL file for OCR post-correction from cfilt/RoundTripOCR-nepali."""
    print("Loading 'cfilt/RoundTripOCR-nepali'...")
    try:
        ds = load_dataset("cfilt/RoundTripOCR-nepali", split="train")
    except Exception as e:
        print(f"Error loading cfilt dataset: {e}")
        return

    records = []
    max_count = limit if limit else len(ds)
    for idx, sample in enumerate(ds):
        if idx >= max_count:
            break

        inp = sample.get("noisy_text") or sample.get("input") or sample.get("ocr_text") or ""
        out = sample.get("clean_text") or sample.get("output") or sample.get("target_text") or ""

        if not inp or not out:
            continue

        records.append({
            "id": f"gec-ocr-{idx+1}",
            "instruction": "कृपया तलको OCR त्रुटियुक्त नेपाली पाठलाई शुद्ध बनाउनुहोस्।",
            "input": str(inp).strip(),
            "output": str(out).strip(),
            "language": "ne",
            "script": "Devanagari",
            "task": "sft/gec/ocr_correction",
            "source": "huggingface.co/datasets/cfilt/RoundTripOCR-nepali",
            "license": "apache-2.0"
        })

    print(f"Writing {len(records)} records to {output_path}...")
    with open(output_path, "w", encoding="utf-8") as f:
        for rec in records:
            f.write(json.dumps(rec, ensure_ascii=False) + "\n")
    print(f"Successfully generated {output_path}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Download and process Nepali GEC datasets into SFT JSONL format.")
    parser.add_argument("--limit", type=int, default=100, help="Maximum number of rows to export per dataset (default: 100). Set to 0 for unlimited.")
    args = parser.parse_args()

    limit_val = None if args.limit <= 0 else args.limit

    cfilt_file = SCRIPT_DIR / "cfilt_ocr_correction.jsonl"
    gec_file = SCRIPT_DIR / "sumitaryal_gec_10k.jsonl"
    detect_file = SCRIPT_DIR / "sumitaryal_error_detection_5k.jsonl"

    generate_sumitaryal_gec_jsonl(gec_file, limit=limit_val)
    generate_sumitaryal_detection_jsonl(detect_file, limit=limit_val)
    generate_cfilt_ocr_jsonl(cfilt_file, limit=limit_val)


if __name__ == "__main__":
    main()
