"""
Standalone Downloader & Processor for Universal Dependencies Nepali (ne_bk).
Generates two JSONL datasets:
1. train_surface_generation.jsonl (input: lemmas + upos + feats -> output: text)
2. train_lemmatization.jsonl (input: text -> output: lemma array)
"""

import json
import argparse
import requests
from pathlib import Path


def download_and_process_ud(limit: int = 50):
    dataset_name = "universal-dependencies/universal_dependencies"
    subset = "ne_bk"
    split = "test"
    
    out_dir = Path(__file__).resolve().parent
    gen_file = out_dir / "train_surface_generation.jsonl"
    lem_file = out_dir / "train_lemmatization.jsonl"
    
    raw_records = []

    # 1. Try Hugging Face datasets library
    try:
        from datasets import load_dataset
        ds = load_dataset(dataset_name, subset, split=split)
        for item in ds:
            raw_records.append({
                "sent_id": str(item.get("sent_id", "")),
                "text": str(item.get("text", "")).strip(),
                "tokens": list(item.get("tokens", [])),
                "lemmas": list(item.get("lemmas", [])),
                "upos": list(item.get("upos", [])),
                "feats": list(item.get("feats", [])) if item.get("feats") else [],
            })
            if len(raw_records) >= limit:
                break
    except Exception as e:
        print(f"HF datasets library fallback to REST API: {e}")

    # 2. Try REST API if library failed
    if not raw_records:
        url = f"https://datasets-server.huggingface.co/rows?dataset={dataset_name}&config={subset}&split={split}&offset=0&length={limit}"
        resp = requests.get(url, timeout=30)
        if resp.status_code == 200:
            data = resp.json()
            for row_obj in data.get("rows", []):
                row = row_obj.get("row", {})
                text = str(row.get("text", "")).strip()
                if text:
                    raw_records.append({
                        "sent_id": str(row.get("sent_id", "")),
                        "text": text,
                        "tokens": list(row.get("tokens", [])),
                        "lemmas": list(row.get("lemmas", [])),
                        "upos": list(row.get("upos", [])),
                        "feats": list(row.get("feats", [])) if row.get("feats") else [],
                    })
                    if len(raw_records) >= limit:
                        break

    gen_records = []
    lem_records = []

    for item in raw_records:
        sent_id = item["sent_id"]
        text = item["text"]
        lemmas = item["lemmas"]
        upos = item["upos"]
        feats = item["feats"]

        # Task 1: Surface Generation (input: lemmas + upos + feats -> output: text)
        input_gen = (
            f"Lemmas: {json.dumps(lemmas, ensure_ascii=False)}\n"
            f"UPOS: {json.dumps(upos, ensure_ascii=False)}\n"
            f"Features: {json.dumps(feats, ensure_ascii=False)}"
        )
        gen_records.append({
            "id": f"ud-gen-{subset}-{sent_id}",
            "instruction": "दिइएका मूल शब्दहरू (Lemmas), पदवर्ग (UPOS), र रूपीय गुणहरू (Features) को आधारमा सही नेपाली वाक्य निर्माण गर्नुहोस्।",
            "input": input_gen,
            "output": text,
            "sent_id": sent_id,
            "language": "ne",
            "script": "Devanagari",
            "task": "sft/surface_realization",
            "source": f"huggingface.co/datasets/{dataset_name}",
            "license": "cc-by-sa-4.0"
        })

        # Task 2: Sentence Lemmatization (input: text -> output: lemma array)
        lem_records.append({
            "id": f"ud-lem-{subset}-{sent_id}",
            "instruction": "दिइएको नेपाली वाक्यका शब्दहरूको मूल रूप (Lemma) को सूची (Array) पत्ता लगाउनुहोस्।",
            "input": text,
            "output": json.dumps(lemmas, ensure_ascii=False),
            "sent_id": sent_id,
            "language": "ne",
            "script": "Devanagari",
            "task": "sft/sentence_lemmatization",
            "source": f"huggingface.co/datasets/{dataset_name}",
            "license": "cc-by-sa-4.0"
        })

    # Write Task 1 JSONL
    with open(gen_file, "w", encoding="utf-8") as f:
        for r in gen_records:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")

    # Write Task 2 JSONL
    with open(lem_file, "w", encoding="utf-8") as f:
        for r in lem_records:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")

    print(f"Generated {len(gen_records)} records -> {gen_file.name}")
    print(f"Generated {len(lem_records)} records -> {lem_file.name}")
    return len(gen_records)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Download and process Universal Dependencies Nepali dataset.")
    parser.add_argument("--limit", type=int, default=50, help="Limit number of rows (default: 50)")
    args = parser.parse_args()
    download_and_process_ud(limit=args.limit)
