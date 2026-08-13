import os
import json
import sys
import urllib.request

out_dir = r"d:\linguistic_adaptation\dataset\transformed\instruction\nlp_tasks\gec"
os.makedirs(out_dir, exist_ok=True)
out_file = os.path.join(out_dir, "cfilt_ocr_correction.jsonl")

print("Downloading 10,000 real rows from Hugging Face cfilt/RoundTripOCR-nepali...")

# Method 1: Try Hugging Face Datasets Server API (Paginated fetch of 10,000 rows)
target_count = 10000
rows_collected = []
offset = 0
length = 100

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
}

try:
    while len(rows_collected) < target_count:
        url = f"https://datasets-server.huggingface.co/rows?dataset=cfilt%2FRoundTripOCR-nepali&config=default&split=train&offset={offset}&length={length}"
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req) as resp:
            data = json.loads(resp.read().decode('utf-8'))
            fetched_rows = data.get('rows', [])
            if not fetched_rows:
                print(f"No more rows returned at offset {offset}")
                break
            for r in fetched_rows:
                row_data = r.get('row', {})
                ocr_text = row_data.get('ocr', '')
                correct_text = row_data.get('correct', '')
                font_name = row_data.get('font', 'Unknown')
                if ocr_text and correct_text:
                    rows_collected.append({
                        "id": f"cfilt-gec-{len(rows_collected)+1:06d}",
                        "source": "cfilt/RoundTripOCR-nepali",
                        "language": "ne",
                        "script": "Devanagari",
                        "task": "post_ocr_correction",
                        "font": font_name,
                        "instruction": "तल दिइएको ओसीआर (OCR) त्रुटिपूर्ण नेपाली पाठलाई सच्याएर शुद्ध पाठ लेख्नुहोस्।",
                        "input": ocr_text,
                        "output": correct_text
                    })
                    if len(rows_collected) >= target_count:
                        break
            offset += len(fetched_rows)
            if offset % 1000 == 0:
                print(f"Fetched {len(rows_collected)} / {target_count} rows...")
except Exception as e:
    print(f"HuggingFace Server API fetch error: {e}")

# If API fails or yields partial, check fallback method via pandas/pyarrow Parquet direct download
if len(rows_collected) < target_count:
    print(f"Server API yielded {len(rows_collected)} rows. Trying Direct Parquet download...")
    try:
        import pandas as pd
        parquet_url = "https://huggingface.co/datasets/cfilt/RoundTripOCR-nepali/resolve/main/data/train-00000-of-00001.parquet"
        df = pd.read_parquet(parquet_url)
        print(f"Loaded Parquet dataframe with shape: {df.shape}")
        rows_collected = []
        for i, row in df.head(target_count).iterrows():
            rows_collected.append({
                "id": f"cfilt-gec-{i+1:06d}",
                "source": "cfilt/RoundTripOCR-nepali",
                "language": "ne",
                "script": "Devanagari",
                "task": "post_ocr_correction",
                "font": str(row.get('font', '')),
                "instruction": "तल दिइएको ओसीआर (OCR) त्रुटिपूर्ण नेपाली पाठलाई सच्याएर शुद्ध पाठ लेख्नुहोस्।",
                "input": str(row.get('ocr', '')),
                "output": str(row.get('correct', ''))
            })
    except Exception as e:
        print(f"Parquet direct fetch error: {e}")

# Save collected JSONL
with open(out_file, "w", encoding="utf-8") as f:
    for item in rows_collected:
        f.write(json.dumps(item, ensure_ascii=False) + "\n")

print(f"Successfully saved {len(rows_collected)} real JSONL records to {out_file}")
