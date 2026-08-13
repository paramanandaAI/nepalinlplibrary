import os
import json
import urllib.request
import pandas as pd
import io

out_dir = r"d:\linguistic_adaptation\dataset\transformed\multimodal\document_ai_ocr"
os.makedirs(out_dir, exist_ok=True)
out_file = os.path.join(out_dir, "nepalipixel_ocr_benchmark.jsonl")

parquet_urls = [
    'https://huggingface.co/api/datasets/himalaya-ai/nepalipixel-synthetic-ocr-benchmark/parquet/default/train/0.parquet',
    'https://huggingface.co/api/datasets/himalaya-ai/nepalipixel-synthetic-ocr-benchmark/parquet/default/train/1.parquet'
]

headers = {'User-Agent': 'Mozilla/5.0'}

instructions = [
    "दिइएको मुद्रित नेपाली कागजात वा चित्रबाट ओसीआर (OCR) प्रविधिमार्फत शुद्ध Devanagari पाठ पहिचान गरी प्रस्तुत गर्नुहोस्।",
    "तल दिइएको ओसीआर (OCR) चित्रमा भएको नेपाली पाठलाई पढी सही र शुद्ध Devanagari पाठ रूपान्तरण गर्नुहोस्।",
    "यो मुद्रित नेपाली कागजात चित्र (Document Image) मा देखिएको शब्द वा वाक्यलाई शुद्ध पाठका रूपमा लेख्नुहोस्।"
]

print("Downloading parquet shards for himalaya-ai/nepalipixel-synthetic-ocr-benchmark...")

rows_collected = []
target_count = 5000

for p_url in parquet_urls:
    if len(rows_collected) >= target_count:
        break
    print(f"Fetching parquet shard: {p_url}...")
    req = urllib.request.Request(p_url, headers=headers)
    try:
        with urllib.request.urlopen(req) as resp:
            content = resp.read()
            df = pd.read_parquet(io.BytesIO(content))
            print(f"Read shard with {len(df)} rows. Columns: {list(df.columns)}")
            
            for idx, row in df.iterrows():
                if len(rows_collected) >= target_count:
                    break
                rec_id = str(row.get('id', f"nepali_ocr_{len(rows_collected):07d}"))
                text = str(row.get('text', '')).strip()
                font_name = str(row.get('font_name', ''))
                level = str(row.get('level', ''))
                size_px = int(row.get('size_px', 0)) if pd.notnull(row.get('size_px')) else 0
                intensity = str(row.get('intensity', ''))
                w = int(row.get('image_w', 0)) if pd.notnull(row.get('image_w')) else 0
                h = int(row.get('image_h', 0)) if pd.notnull(row.get('image_h')) else 0
                
                # Extract image dict/url
                img_data = row.get('image', None)
                img_path = ""
                if isinstance(img_data, dict):
                    img_path = img_data.get('path', '') or img_data.get('bytes', '')
                
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
                        "metadata": {
                            "font_name": font_name,
                            "level": level,
                            "size_px": size_px,
                            "intensity": intensity,
                            "image_dimensions": [w, h]
                        }
                    })
    except Exception as e:
        print(f"Error reading shard {p_url}: {e}")

print(f"Collected {len(rows_collected)} transformed SFT OCR records.")

with open(out_file, "w", encoding="utf-8") as f:
    for item in rows_collected:
        f.write(json.dumps(item, ensure_ascii=False) + "\n")

print(f"Successfully saved {len(rows_collected)} clean SFT OCR records to {out_file}")
