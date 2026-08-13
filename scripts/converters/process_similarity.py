"""
Nepali STS-B Sentence Similarity Data Exporter
Processes Kaggle STSB Multi-MT Nepali cleaned dataset into SFT JSONL format.
Supports batching 10 sentence pairs per instruction prompt as well as single-pair format,
using consistent Devanagari numerals and qualitative similarity descriptions.
"""

import argparse
import json
from pathlib import Path
import pandas as pd

SCRIPT_DIR = Path(__file__).resolve().parent
ROOT_DIR = SCRIPT_DIR.parent.parent
CSV_PATH = ROOT_DIR / "other_sources" / "kaggle" / "stsb_multi_mt_nepali_cleaned.csv"

# Digit translation table ASCII -> Devanagari
DEVA_DIGITS = str.maketrans("0123456789", "०१२३४५६७८९")


def to_deva_str(val) -> str:
    """Converts numbers/strings to Devanagari numeral representations."""
    return str(val).translate(DEVA_DIGITS)


def get_qualitative_label(score: float) -> str:
    """Returns qualitative Nepali similarity label based on STS-B score (0.0 to 5.0)."""
    if score >= 4.5:
        return "पूर्ण रूपमा समान"
    elif score >= 3.5:
        return "उच्च समानता"
    elif score >= 2.5:
        return "मध्यम समानता"
    elif score >= 1.2:
        return "न्यून समानता"
    else:
        return "असमान (भिन्न अर्थ)"


def generate_batched_10pairs_jsonl(df: pd.DataFrame, output_path: Path, num_records: int = 1000) -> None:
    """
    Groups sentence pairs into batches of 10 pairs per instruction prompt.
    Generates num_records batched JSONL entries with standardized Devanagari numerals.
    """
    print(f"Generating {num_records} batched 10-pair records with Devanagari numerals & qualitative labels...")
    total_pairs = len(df)
    records = []

    for record_idx in range(num_records):
        start_idx = (record_idx * 5) % (total_pairs - 10)
        batch_df = df.iloc[start_idx : start_idx + 10]

        prompt_lines = []
        target_lines = []
        pairs_meta = []

        for pair_idx, (_, row) in enumerate(batch_df.iterrows(), 1):
            s1 = str(row["sentence1"]).strip()
            s2 = str(row["sentence2"]).strip()
            score = round(float(row["score"]), 2)
            
            pair_num_deva = to_deva_str(pair_idx)
            score_deva = to_deva_str(f"{score:.1f}")
            qual_label = get_qualitative_label(score)

            prompt_lines.append(f"जोडी {pair_num_deva}:\nवाक्य १: {s1}\nवाक्य २: {s2}")
            target_lines.append(f"जोडी {pair_num_deva}: समानता अङ्क = {score_deva} / ५.० ({qual_label})")
            
            pairs_meta.append({
                "pair_num": pair_idx,
                "sentence1": s1,
                "sentence2": s2,
                "score": score,
                "score_deva": score_deva,
                "qualitative_label": qual_label
            })

        input_text = "\n\n".join(prompt_lines)
        output_text = "\n".join(target_lines)

        records.append({
            "id": f"stsb-batch10-{record_idx+1:04d}",
            "instruction": "तल दिइएका १० वटा नेपाली वाक्य जोडीहरूको अर्थगत समानता (Semantic Similarity) मूल्याङ्कन गरी प्रत्येक जोडीको समानता अङ्क (० देखि ५ सम्म) र समानताको स्थिति प्रदान गर्नुहोस्।",
            "input": input_text,
            "output": output_text,
            "num_pairs": 10,
            "pairs": pairs_meta,
            "language": "ne",
            "script": "Devanagari",
            "task": "sft/sentence_similarity/batched_10pairs",
            "source": "kaggle.com/datasets/yubraj11/sentence-similarity-nepali-dataset",
            "license": "cc-by-sa-4.0"
        })

    print(f"Writing {len(records)} batched records to '{output_path}'...")
    with open(output_path, "w", encoding="utf-8") as f:
        for rec in records:
            f.write(json.dumps(rec, ensure_ascii=False) + "\n")
    print(f"Successfully generated {output_path}")


def generate_single_pair_jsonl(df: pd.DataFrame, output_path: Path, num_records: int = 1000) -> None:
    """Generates single-pair similarity evaluation JSONL entries with Devanagari numerals."""
    print(f"Generating {num_records} single-pair records...")
    records = []

    for idx in range(min(num_records, len(df))):
        row = df.iloc[idx]
        s1 = str(row["sentence1"]).strip()
        s2 = str(row["sentence2"]).strip()
        score = round(float(row["score"]), 2)

        score_deva = to_deva_str(f"{score:.1f}")
        qual_label = get_qualitative_label(score)

        input_text = f"वाक्य १: {s1}\nवाक्य २: {s2}"
        output_text = f"समानता अङ्क = {score_deva} / ५.० ({qual_label})"

        records.append({
            "id": f"stsb-single-{idx+1:04d}",
            "instruction": "दिइएका दुई नेपाली वाक्यहरूको अर्थगत समानता (Semantic Similarity) मूल्याङ्कन गरी ० देखि ५ सम्मको समानता अङ्क र स्थिति प्रदान गर्नुहोस्।",
            "input": input_text,
            "output": output_text,
            "score": score,
            "score_deva": score_deva,
            "qualitative_label": qual_label,
            "language": "ne",
            "script": "Devanagari",
            "task": "sft/sentence_similarity/single_pair",
            "source": "kaggle.com/datasets/yubraj11/sentence-similarity-nepali-dataset",
            "license": "cc-by-sa-4.0"
        })

    print(f"Writing {len(records)} single-pair records to '{output_path}'...")
    with open(output_path, "w", encoding="utf-8") as f:
        for rec in records:
            f.write(json.dumps(rec, ensure_ascii=False) + "\n")
    print(f"Successfully generated {output_path}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Process Kaggle Nepali STS-B Dataset into SFT JSONL format.")
    parser.add_argument("--limit", type=int, default=1000, help="Number of SFT records to generate (default: 1000).")
    parser.add_argument("--csv_path", type=str, default=str(CSV_PATH), help="Path to cleaned input CSV file.")
    args = parser.parse_args()

    input_csv = Path(args.csv_path)
    if not input_csv.exists():
        raise FileNotFoundError(f"Input CSV file not found at '{input_csv}'.")

    print(f"Loading cleaned dataset from '{input_csv}'...")
    df = pd.read_csv(input_csv, encoding="utf-8")
    print(f"Loaded {len(df)} total sentence pairs.")

    batched_path = SCRIPT_DIR / "stsb_batched_similarity_1000.jsonl"
    single_path = SCRIPT_DIR / "stsb_single_similarity_1000.jsonl"

    generate_batched_10pairs_jsonl(df, batched_path, num_records=args.limit)
    generate_single_pair_jsonl(df, single_path, num_records=args.limit)


if __name__ == "__main__":
    main()
