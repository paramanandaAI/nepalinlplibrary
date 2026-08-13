import os
import json
import time
import urllib.request
import sys

out_dir = r"d:\linguistic_adaptation\dataset\transformed\multimodal\document_ai_ocr"
os.makedirs(out_dir, exist_ok=True)
out_file = os.path.join(out_dir, "nepalipixel_ocr_benchmark.jsonl")

print("Starting download of himalaya-ai/nepalipixel-synthetic-ocr-benchmark...", flush=True)

offset = 0
length = 100
target_count = 5000
headers = {'User-Agent': 'Mozilla/5.0'}
saved_count = 0

with open(out_file, "w", encoding="utf-8") as f_out:
    while saved_count < target_count:
        url = f"https://datasets-server.huggingface.co/rows?dataset=himalaya-ai%2Fnepalipixel-synthetic-ocr-benchmark&config=default&split=train&offset={offset}&length={length}"
        req = urllib.request.Request(url, headers=headers)
        try:
            with urllib.request.urlopen(req) as resp:
                data = json.loads(resp.read().decode('utf-8'))
                fetched_rows = data.get('rows', [])
                if not fetched_rows:
                    print(f"No more rows returned at offset {offset}", flush=True)
                    break
                for r in fetched_rows:
                    row_data = r.get('row', {})
                    rec_id = row_data.get('id', f"nepali_ocr_{saved_count:07d}")
                    txt = row_data.get('text', '').strip()
                    font_name = row_data.get('font_name', '')
                    level = row_data.get('level', '')
                    size_px = row_data.get('size_px', 0)
                    aug = row_data.get('augmentations', [])
                    intensity = row_data.get('intensity', '')
                    w = row_data.get('image_w', 0)
                    h = row_data.get('image_h', 0)
                    
                    img_info = row_data.get('image', None)
                    img_url = ""
                    if isinstance(img_info, list) and len(img_info) > 0:
                        img_url = img_info[0].get('src', '')
                    elif isinstance(img_info, dict):
                        img_url = img_info.get('src', '') or img_info.get('path', '')
                    
                    if txt:
                        record = {
                            "id": rec_id,
                            "source": "himalaya-ai/nepalipixel-synthetic-ocr-benchmark",
                            "language": "ne",
                            "script": "Devanagari",
                            "task": "ocr_document_understanding",
                            "text": txt,
                            "font_name": font_name,
                            "level": level,
                            "size_px": size_px,
                            "augmentations": aug,
                            "intensity": intensity,
                            "image_dimensions": [w, h],
                            "image_url": img_url
                        }
                        f_out.write(json.dumps(record, ensure_ascii=False) + "\n")
                        f_out.flush()
                        saved_count += 1
                        if saved_count >= target_count:
                            break
                offset += len(fetched_rows)
                print(f"Downloaded & saved {saved_count} / {target_count} rows...", flush=True)
                time.sleep(0.15)
        except Exception as e:
            print(f"Fetch error at offset {offset}: {e}", flush=True)
            time.sleep(2)

print(f"Done! Successfully saved {saved_count} OCR benchmark JSONL records to {out_file}", flush=True)
