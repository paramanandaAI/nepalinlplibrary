import os
import json
import random
import time
import urllib.request

out_dir = r"d:\linguistic_adaptation\dataset\transformed\instruction\nlp_tasks\gec"
os.makedirs(out_dir, exist_ok=True)

det_out_file = os.path.join(out_dir, "sumitaryal_error_detection_5k.jsonl")
pair_out_file = os.path.join(out_dir, "sumitaryal_pair_choice_5k.jsonl")

headers = {'User-Agent': 'Mozilla/5.0'}

print("Fetching dataset rows from HuggingFace (skipping first 10,000 records)...")

# Target 5,000 records each
target_count = 5000

# ---------------------------------------------------------
# TASK 1: Binary Error Detection (5,000 records)
# Fetching from offset 10,000+ of nepali_grammatical_error_detection
# ---------------------------------------------------------
print("\n--- Generating Task 1: Binary Error Detection (5,000 records) ---")

det_records = []
offset = 10000
length = 100

instructions_det = [
    "तल दिइएको नेपाली वाक्य व्याकरणिक रूपमा शुद्ध छ वा अशुद्ध? छुट्याउनुहोस्।",
    "निम्न वाक्यको व्याकरणिक शुद्धता जाँच गरी 'शुद्ध' वा 'अशुद्ध' के हो उत्तर दिनुहोस्।",
    "दिइएको नेपाली वाक्य व्याकरण र वर्णविन्यासका दृष्टिले सही छ कि छैन पत्ता लगाउनुहोस्।"
]

while len(det_records) < target_count:
    url = f"https://datasets-server.huggingface.co/rows?dataset=sumitaryal%2Fnepali_grammatical_error_detection&config=default&split=train&offset={offset}&length={length}"
    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req) as resp:
            data = json.loads(resp.read().decode('utf-8'))
            fetched_rows = data.get('rows', [])
            if not fetched_rows:
                print(f"No more rows returned for detection at offset {offset}")
                break
            for r in fetched_rows:
                row_data = r.get('row', {})
                sent = row_data.get('sentence', '').strip()
                label = row_data.get('label', 1)  # 1 = Correct, 0 = Incorrect
                if sent:
                    instr = instructions_det[len(det_records) % len(instructions_det)]
                    verdict = "शुद्ध" if label == 1 else "अशुद्ध"
                    explanation = "यो वाक्य व्याकरणिक रूपमा सही र शुद्ध छ।" if label == 1 else "यो वाक्यमा व्याकरणिक वा वर्णविन्यास सम्बन्धी त्रुटि छ।"
                    
                    det_records.append({
                        "id": f"sumitaryal-ged-{len(det_records)+1:06d}",
                        "source": "sumitaryal/nepali_grammatical_error_detection",
                        "language": "ne",
                        "script": "Devanagari",
                        "task": "grammatical_error_detection",
                        "instruction": instr,
                        "input": sent,
                        "output": f"{verdict}। ({explanation})"
                    })
                    if len(det_records) >= target_count:
                        break
            offset += len(fetched_rows)
            if len(det_records) % 1000 == 0 or len(det_records) >= target_count:
                print(f"Detection records collected: {len(det_records)} / {target_count}")
            time.sleep(0.2)
    except Exception as e:
        print(f"Detection fetch error at offset {offset}: {e}")
        time.sleep(3)

with open(det_out_file, "w", encoding="utf-8") as f:
    for item in det_records:
        f.write(json.dumps(item, ensure_ascii=False) + "\n")

print(f"Saved {len(det_records)} detection records to {det_out_file}")

# ---------------------------------------------------------
# TASK 2: Pairwise Preference / Choice (5,000 records)
# Fetching from offset 10,000+ of nepali_grammatical_error_correction
# ---------------------------------------------------------
print("\n--- Generating Task 2: Pairwise Choice (5,000 records) ---")

pair_records = []
offset = 10000
length = 100

instructions_pair = [
    "तल दिइएका दुई वाक्यहरू (विकल्प क र विकल्प ख) मध्ये कुन वाक्य व्याकरणिक रूपमा शुद्ध छ? सही विकल्प रोज्नुहोस्।",
    "निम्न दुई वाक्यहरूमध्ये कुन वाक्यमा कुनै व्याकरणिक अशुद्धि छैन? सही उत्तर चयन गर्नुहोस्।",
    "विकल्प (क) र विकल्प (ख) लाई ध्यानपूर्वक पढी व्याकरणिक रूपमा सही वाक्य कुन हो पहिचान गर्नुहोस्।"
]

random.seed(42)

while len(pair_records) < target_count:
    url = f"https://datasets-server.huggingface.co/rows?dataset=sumitaryal%2Fnepali_grammatical_error_correction&config=default&split=train&offset={offset}&length={length}"
    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req) as resp:
            data = json.loads(resp.read().decode('utf-8'))
            fetched_rows = data.get('rows', [])
            if not fetched_rows:
                print(f"No more rows returned for correction at offset {offset}")
                break
            for r in fetched_rows:
                row_data = r.get('row', {})
                incorrect = row_data.get('incorrect_sentence', '').strip()
                correct = row_data.get('correct_sentence', '').strip()
                if incorrect and correct and incorrect != correct:
                    instr = instructions_pair[len(pair_records) % len(instructions_pair)]
                    
                    # Randomize option A / option B
                    is_correct_a = random.choice([True, False])
                    if is_correct_a:
                        opt_a = correct
                        opt_b = incorrect
                        correct_opt_label = "विकल्प (क)"
                    else:
                        opt_a = incorrect
                        opt_b = correct
                        correct_opt_label = "विकल्प (ख)"
                    
                    input_text = f"विकल्प (क): {opt_a}\nविकल्प (ख): {opt_b}"
                    output_text = f"सही र शुद्ध वाक्य {correct_opt_label} हो।\nशुद्ध वाक्य: {correct}"
                    
                    pair_records.append({
                        "id": f"sumitaryal-pair-{len(pair_records)+1:06d}",
                        "source": "sumitaryal/nepali_grammatical_error_correction",
                        "language": "ne",
                        "script": "Devanagari",
                        "task": "grammatical_pair_choice",
                        "instruction": instr,
                        "input": input_text,
                        "output": output_text
                    })
                    if len(pair_records) >= target_count:
                        break
            offset += len(fetched_rows)
            if len(pair_records) % 1000 == 0 or len(pair_records) >= target_count:
                print(f"Pair choice records collected: {len(pair_records)} / {target_count}")
            time.sleep(0.2)
    except Exception as e:
        print(f"Pair choice fetch error at offset {offset}: {e}")
        time.sleep(3)

with open(pair_out_file, "w", encoding="utf-8") as f:
    for item in pair_records:
        f.write(json.dumps(item, ensure_ascii=False) + "\n")

print(f"Saved {len(pair_records)} pair choice records to {pair_out_file}")
print("\nBoth datasets generated successfully!")
