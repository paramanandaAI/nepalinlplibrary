import os
import json
import time
import urllib.request

out_dir = r"d:\linguistic_adaptation\dataset\transformed\multimodal\asr"
os.makedirs(out_dir, exist_ok=True)
out_file = os.path.join(out_dir, "nep_voice_compilation_10k.jsonl")

print("Streaming 10,000 real rows from himalaya-ai/nep-voice-tts-compilation via HF API...", flush=True)

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
instructions = [
    "तल दिइएको नेपाली आवाज (Audio) को उच्चारण सुनि त्यसको सही र शुद्ध Devanagari पाठ रूपान्तरण गर्नुहोस्।",
    "यो नेपाली श्रव्य सामग्री (Audio Recording) बाट बोलिएको वाक्य स्पष्ट रूपमा पहिचान गरी Devanagari लिपिका रूपमा लेख्नुहोस्।",
    "दिइएको Nepali Speech Sample को स्पष्ट उच्चारण सुनेर सही पाठप्रवाह प्रस्तुत गर्नुहोस्।"
]

target_count = 10000
rows_collected = []
offset = 0
length = 100

while len(rows_collected) < target_count:
    url = f"https://datasets-server.huggingface.co/rows?dataset=himalaya-ai%2Fnep-voice-tts-compilation&config=default&split=train&offset={offset}&length={length}"
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
                rec_id = str(row_data.get('id', f"nep_voice_{len(rows_collected):07d}"))
                raw_txt = str(row_data.get('text', '')).strip()
                norm_txt = str(row_data.get('normalized_text', '')).strip() or raw_txt
                source_id = str(row_data.get('source_id', 'google_fleurs'))
                quality_tier = str(r.get('quality_tier', 'high'))
                intended_use = str(r.get('intended_use', 'finetune'))
                
                img_data = row_data.get('audio', None)
                audio_url = ""
                if isinstance(img_data, list) and len(img_data) > 0:
                    audio_url = img_data[0].get('src', '')
                elif isinstance(img_data, dict):
                    audio_url = img_data.get('src', '') or img_data.get('path', '')
                
                if norm_txt:
                    instr = instructions[len(rows_collected) % len(instructions)]
                    input_text = f"<audio_id: {rec_id}> | स्रोत: {source_id} | गुणस्तर: {quality_tier}"
                    
                    rows_collected.append({
                        "id": rec_id,
                        "source": "himalaya-ai/nep-voice-tts-compilation",
                        "language": "ne",
                        "script": "Devanagari",
                        "task": "speech_recognition_transcription",
                        "instruction": instr,
                        "input": input_text,
                        "output": norm_txt,
                        "audio": {
                            "audio_url": audio_url,
                            "format": "audio/wav",
                            "sampling_rate": 16000
                        },
                        "metadata": {
                            "source_id": source_id,
                            "quality_tier": quality_tier,
                            "raw_text": raw_txt
                        }
                    })
                    if len(rows_collected) >= target_count:
                        break
            offset += len(fetched_rows)
            if len(rows_collected) % 1000 == 0 or len(rows_collected) >= target_count:
                print(f"Collected {len(rows_collected)} / {target_count} records...", flush=True)
            time.sleep(0.3)
    except Exception as e:
        print(f"Rate limited or fetch error at offset {offset}: {e}. Sleeping 5 seconds...", flush=True)
        time.sleep(5)

with open(out_file, "w", encoding="utf-8") as f:
    for item in rows_collected:
        f.write(json.dumps(item, ensure_ascii=False) + "\n")

print(f"DONE! Successfully saved {len(rows_collected)} clean SFT nep-voice records to {out_file}", flush=True)
