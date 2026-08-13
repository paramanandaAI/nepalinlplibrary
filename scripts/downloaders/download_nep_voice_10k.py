import os
import json
import urllib.request
import pandas as pd
import io
import sys

out_dir = r"d:\linguistic_adaptation\dataset\transformed\multimodal\asr"
os.makedirs(out_dir, exist_ok=True)
out_file = os.path.join(out_dir, "nep_voice_compilation_10k.jsonl")

headers = {'User-Agent': 'Mozilla/5.0'}

# Fetch parquet URLs
parquet_api_url = "https://huggingface.co/api/datasets/himalaya-ai/nep-voice-tts-compilation/parquet/default/train"
req = urllib.request.Request(parquet_api_url, headers=headers)
p_urls = json.loads(urllib.request.urlopen(req).read().decode('utf-8'))

print(f"Total available parquet shards: {len(p_urls)}", flush=True)

instructions = [
    "तल दिइएको नेपाली आवाज (Audio) को उच्चारण सुनि त्यसको सही र शुद्ध Devanagari पाठ रूपान्तरण गर्नुहोस्।",
    "यो नेपाली श्रव्य सामग्री (Audio Recording) बाट बोलिएको वाक्य स्पष्ट रूपमा पहिचान गरी Devanagari लिपिका रूपमा लेख्नुहोस्।",
    "दिइएको Nepali Speech Sample को स्पष्ट उच्चारण सुनेर सही पाठप्रवाह प्रस्तुत गर्नुहोस्।"
]

target_count = 10000
saved_count = 0

with open(out_file, "w", encoding="utf-8") as f_out:
    for p_idx, p_url in enumerate(p_urls):
        if saved_count >= target_count:
            break
        print(f"Fetching parquet shard {p_idx+1}/{len(p_urls)}: {p_url}", flush=True)
        try:
            r_req = urllib.request.Request(p_url, headers=headers)
            with urllib.request.urlopen(r_req) as resp:
                content = resp.read()
                df = pd.read_parquet(io.BytesIO(content))
                print(f"Read shard {p_idx+1} with {len(df)} rows...", flush=True)
                for idx, row in df.iterrows():
                    if saved_count >= target_count:
                        break
                    
                    rec_id = str(row.get('id', f"nep_voice_{saved_count:07d}"))
                    raw_txt = str(row.get('text', '')).strip()
                    norm_txt = str(row.get('normalized_text', '')).strip() or raw_txt
                    source_id = str(row.get('source_id', 'google_fleurs'))
                    quality_tier = str(row.get('quality_tier', 'high'))
                    intended_use = str(row.get('intended_use', 'finetune'))
                    
                    if norm_txt:
                        instr = instructions[saved_count % len(instructions)]
                        input_text = f"<audio_id: {rec_id}> | स्रोत: {source_id} | गुणस्तर: {quality_tier} | उपयोग: {intended_use}"
                        
                        record = {
                            "id": rec_id,
                            "source": "himalaya-ai/nep-voice-tts-compilation",
                            "language": "ne",
                            "script": "Devanagari",
                            "task": "speech_recognition_transcription",
                            "instruction": instr,
                            "input": input_text,
                            "output": norm_txt,
                            "metadata": {
                                "source_id": source_id,
                                "quality_tier": quality_tier,
                                "intended_use": intended_use,
                                "raw_text": raw_txt
                            }
                        }
                        f_out.write(json.dumps(record, ensure_ascii=False) + "\n")
                        f_out.flush()
                        saved_count += 1
                print(f"Saved total: {saved_count} / {target_count} records.", flush=True)
        except Exception as e:
            print(f"Error reading {p_url}: {e}", flush=True)

print(f"Successfully saved {saved_count} clean SFT nep-voice records to {out_file}", flush=True)
