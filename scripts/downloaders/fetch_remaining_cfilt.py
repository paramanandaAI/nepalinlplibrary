import os
import json
import time
import urllib.request

out_dir = r"d:\linguistic_adaptation\dataset\transformed\instruction\nlp_tasks\gec"
os.makedirs(out_dir, exist_ok=True)
out_file = os.path.join(out_dir, "cfilt_ocr_correction.jsonl")

# Check existing rows count
existing_records = []
if os.path.exists(out_file):
    with open(out_file, "r", encoding="utf-8") as f:
        for line in f:
            if line.strip():
                existing_records.append(json.loads(line))

print(f"Already have {len(existing_records)} records.")

target_count = 10000
headers = {'User-Agent': 'Mozilla/5.0'}

# If we need more rows, fetch with sleep to avoid 429 rate limit
offset = len(existing_records)
while len(existing_records) < target_count:
    url = f"https://datasets-server.huggingface.co/rows?dataset=cfilt%2FRoundTripOCR-nepali&config=default&split=train&offset={offset}&length=100"
    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req) as resp:
            data = json.loads(resp.read().decode('utf-8'))
            fetched_rows = data.get('rows', [])
            if not fetched_rows:
                print(f"No more rows available at offset {offset}")
                break
            for r in fetched_rows:
                row_data = r.get('row', {})
                ocr_text = row_data.get('ocr', '')
                correct_text = row_data.get('correct', '')
                font_name = row_data.get('font', 'Unknown')
                if ocr_text and correct_text:
                    existing_records.append({
                        "id": f"cfilt-gec-{len(existing_records)+1:06d}",
                        "source": "cfilt/RoundTripOCR-nepali",
                        "language": "ne",
                        "script": "Devanagari",
                        "task": "post_ocr_correction",
                        "font": font_name,
                        "instruction": "तल दिइएको ओसीआर (OCR) त्रुटिपूर्ण नेपाली पाठलाई सच्याएर शुद्ध पाठ लेख्नुहोस्।",
                        "input": ocr_text,
                        "output": correct_text
                    })
                    if len(existing_records) >= target_count:
                        break
            offset += len(fetched_rows)
            if len(existing_records) % 1000 == 0 or len(existing_records) >= target_count:
                print(f"Total collected: {len(existing_records)} / {target_count}")
            time.sleep(0.3)  # Rate limiting prevention
    except Exception as e:
        print(f"Fetch error at offset {offset}: {e}")
        print("Sleeping 5 seconds before retry...")
        time.sleep(5)

# Save exact 10,000 JSONL records
with open(out_file, "w", encoding="utf-8") as f:
    for item in existing_records[:target_count]:
        f.write(json.dumps(item, ensure_ascii=False) + "\n")

print(f"Done! Saved exactly {min(len(existing_records), target_count)} records to {out_file}")
