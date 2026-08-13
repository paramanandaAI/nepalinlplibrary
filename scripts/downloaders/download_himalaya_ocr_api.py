import os
import json
import time
import urllib.request

out_dir = r"d:\linguistic_adaptation\dataset\transformed\multimodal\document_ai_ocr"
os.makedirs(out_dir, exist_ok=True)
out_file = os.path.join(out_dir, "nepalipixel_ocr_benchmark.jsonl")

print("Streaming 5,000 real rows from himalaya-ai/nepalipixel-synthetic-ocr-benchmark via HF API...", flush=True)

headers = {'User-Agent': 'Mozilla/5.0'}
instructions = [
    "दिइएको मुद्रित नेपाली कागजात वा चित्रबाट ओसीआर (OCR) प्रविधिमार्फत शुद्ध Devanagari पाठ पहिचान गरी प्रस्तुत गर्नुहोस्।",
    "तल दिइएको ओसीआर (OCR) चित्रमा भएको नेपाली पाठलाई पढी सही र शुद्ध Devanagari पाठ रूपान्तरण गर्नुहोस्।",
    "यो मुद्रित नेपाली कागजात चित्र (Document Image) मा देखिएको शब्द वा वाक्यलाई शुद्ध पाठका रूपमा लेख्नुहोस्।"
]

target_count = 5000
rows_collected = []
offset = 0
length = 100

while len(rows_collected) < target_count:
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
                rec_id = str(row_data.get('id', f"nepali_ocr_{len(rows_collected):07d}"))
                text = str(row_data.get('text', '')).strip()
                font_name = str(row_data.get('font_name', ''))
                level = str(row_data.get('level', ''))
                size_px = str(row_data.get('size_px', ''))
                intensity = str(row_data.get('intensity', ''))
                w = str(row_data.get('image_w', ''))
                h = str(row_data.get('image_h', ''))
                
                img_data = row_data.get('image', None)
                img_url = ""
                if isinstance(img_data, list) and len(img_data) > 0:
                    img_url = img_data[0].get('src', '')
                elif isinstance(img_data, dict):
                    img_url = img_data.get('src', '') or img_data.get('path', '')
                
                if text:
                    instr = instructions[len(rows_collected) % len(instructions)]
                    input_text = f"<image_id: {rec_id}> | स्तर (Level): {level} | फन्ट (Font): {font_name} | आकार: {size_px}px ({w}x{h})"
                    
                    rows_collected.append({
                        "id": rec_id,
                        "source": "himalaya-ai/nepalipixel-synthetic-ocr-benchmark",
                        "language": "ne",
                        "script": "Devanagari",
                        "task": "ocr_document_understanding",
                        "instruction": instr,
                        "input": input_text,
                        "output": text,
                        "image": {
                            "image_url": img_url,
                            "width": w,
                            "height": h
                        },
                        "metadata": {
                            "font_name": font_name,
                            "level": level,
                            "size_px": size_px,
                            "intensity": intensity
                        }
                    })
                    if len(rows_collected) >= target_count:
                        break
            offset += len(fetched_rows)
            if len(rows_collected) % 1000 == 0 or len(rows_collected) >= target_count:
                print(f"Collected {len(rows_collected)} / {target_count} OCR records...", flush=True)
            time.sleep(0.15)
    except Exception as e:
        print(f"Fetch error at offset {offset}: {e}", flush=True)
        time.sleep(2)

with open(out_file, "w", encoding="utf-8") as f:
    for item in rows_collected:
        f.write(json.dumps(item, ensure_ascii=False) + "\n")

print(f"DONE! Successfully saved {len(rows_collected)} clean SFT OCR records to {out_file}", flush=True)
