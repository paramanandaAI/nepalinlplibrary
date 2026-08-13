import os
import json
import time
import urllib.request

out_dir = r"d:\linguistic_adaptation\dataset\transformed\instruction\nlp_tasks\gec"
os.makedirs(out_dir, exist_ok=True)
out_file = os.path.join(out_dir, "sumitaryal_gec_10k.jsonl")

print("Downloading 10,000 real rows from Hugging Face sumitaryal/nepali_grammatical_error_correction...")

target_count = 10000
rows_collected = []
offset = 0
length = 100

headers = {'User-Agent': 'Mozilla/5.0'}

while len(rows_collected) < target_count:
    url = f"https://datasets-server.huggingface.co/rows?dataset=sumitaryal%2Fnepali_grammatical_error_correction&config=default&split=train&offset={offset}&length={length}"
    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req) as resp:
            data = json.loads(resp.read().decode('utf-8'))
            fetched_rows = data.get('rows', [])
            if not fetched_rows:
                print(f"No more rows returned at offset {offset}")
                break
            for r in fetched_rows:
                row_data = r.get('row', {})
                incorrect = row_data.get('incorrect_sentence', '')
                correct = row_data.get('correct_sentence', '')
                if incorrect and correct:
                    rows_collected.append({
                        "id": f"sumitaryal-gec-{len(rows_collected)+1:06d}",
                        "source": "sumitaryal/nepali_grammatical_error_correction",
                        "language": "ne",
                        "script": "Devanagari",
                        "task": "grammatical_error_correction",
                        "instruction": "तल दिइएको व्याकरणिक रूपमा त्रुटिपूर्ण नेपाली वाक्यलाई सच्याएर शुद्ध वाक्य लेख्नुहोस्।",
                        "input": incorrect,
                        "output": correct
                    })
                    if len(rows_collected) >= target_count:
                        break
            offset += len(fetched_rows)
            if len(rows_collected) % 1000 == 0 or len(rows_collected) >= target_count:
                print(f"Collected {len(rows_collected)} / {target_count} rows...")
            time.sleep(0.2)
    except Exception as e:
        print(f"Fetch error at offset {offset}: {e}")
        time.sleep(3)

# Save JSONL
with open(out_file, "w", encoding="utf-8") as f:
    for item in rows_collected:
        f.write(json.dumps(item, ensure_ascii=False) + "\n")

print(f"Successfully saved {len(rows_collected)} real JSONL records to {out_file}")
