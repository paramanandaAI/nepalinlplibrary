import os
import json
import time
import urllib.request

out_dir = r"d:\linguistic_adaptation\dataset\transformed\asr"
os.makedirs(out_dir, exist_ok=True)
out_file = os.path.join(out_dir, "nwacha_muna_newari_asr.jsonl")

print("Downloading Nwacha Muna Newari ASR dataset with audio metadata from Hugging Face...")

rows_collected = []
offset = 0
length = 100
headers = {'User-Agent': 'Mozilla/5.0'}

while True:
    url = f"https://datasets-server.huggingface.co/rows?dataset=ilprl-docse%2FNwacha_Muna_A_Newari_ASR_Dataset&config=default&split=train&offset={offset}&length={length}"
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
                utt_id = row_data.get('utterance_id', f"utt-{len(rows_collected)+1:04d}")
                sent = row_data.get('sentence', '').strip()
                audio_info = row_data.get('audio', None)
                
                # Extract audio URL or path if available
                audio_url = ""
                if isinstance(audio_info, list) and len(audio_info) > 0:
                    audio_url = audio_info[0].get('src', '')
                elif isinstance(audio_info, dict):
                    audio_url = audio_info.get('path', '') or audio_info.get('src', '')
                
                if sent:
                    rows_collected.append({
                        "id": utt_id,
                        "source": "ilprl-docse/Nwacha_Muna_A_Newari_ASR_Dataset",
                        "language": "new",
                        "language_name": "Nepal Bhasa / Newari",
                        "script": "Devanagari",
                        "task": "speech_recognition_transcription",
                        "utterance_id": utt_id,
                        "sentence": sent,
                        "audio": {
                            "utterance_id": utt_id,
                            "audio_url": audio_url,
                            "format": "audio/wav",
                            "sampling_rate": 16000
                        }
                    })
            offset += len(fetched_rows)
            print(f"Collected {len(rows_collected)} Newari ASR rows with audio metadata so far...")
            time.sleep(0.15)
    except Exception as e:
        print(f"Fetch error at offset {offset}: {e}")
        time.sleep(2)

with open(out_file, "w", encoding="utf-8") as f:
    for item in rows_collected:
        f.write(json.dumps(item, ensure_ascii=False) + "\n")

print(f"Successfully saved {len(rows_collected)} Newari ASR JSONL records with audio metadata to {out_file}")
