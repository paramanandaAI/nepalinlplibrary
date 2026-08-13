# -*- coding: utf-8 -*-
"""
Script to create batch translation instruction datasets (English <-> Nepali).
"""

import json
import os
import random
from pathlib import Path
from typing import Optional

def create_translation_instructions(
    csv_path: str,
    output_dir: str,
    source_lang: str,
    target_lang: str,
    sentences_per_input: int = 6,
    seed: int = 42
):
    random.seed(seed)
    
    import pandas as pd
    df = pd.read_csv(csv_path, encoding='utf-8')
    print(f"Loaded {len(df)} rows")
    
    if source_lang == 'en' and target_lang == 'ne':
        src_col, tgt_col = 'en', 'ne'
        task_name = 'english_to_nepali'
        instruction_ne = "तल दिइएको अंग्रेजी वाक्यहरूलाई नेपालीमा अनुवाद गर्नुहोस्।"
        instruction_en = "Translate the following English sentences to Nepali."
    else:
        src_col, tgt_col = 'ne', 'en'
        task_name = 'nepali_to_english'
        instruction_ne = "तल दिइएको नेपाली वाक्यहरूलाई अङ्ग्रेजीमा अनुवाद गर्नुहोस्।"
        instruction_en = "Translate the following Nepali sentences to English."
    
    pairs = list(zip(df[src_col].tolist(), df[tgt_col].tolist()))
    random.shuffle(pairs)
    
    output_path = Path(output_dir) / f"{task_name}.jsonl"
    os.makedirs(output_dir, exist_ok=True)
    
    with open(output_path, 'w', encoding='utf-8') as f:
        for i in range(0, len(pairs), sentences_per_input):
            batch = pairs[i:i + sentences_per_input]
            if len(batch) < sentences_per_input:
                continue
            
            src_sentences = [p[0] for p in batch]
            tgt_sentences = [p[1] for p in batch]
            
            input_text = "\n".join([f"{j+1}. {s}" for j, s in enumerate(src_sentences)])
            output_text = "\n".join([f"{j+1}. {s}" for j, s in enumerate(tgt_sentences)])
            
            record = {
                "id": f"{task_name}-{i//sentences_per_input + 1:06d}",
                "source": "kaggle:erparasrai/english-nepali-pair",
                "source_url": "https://www.kaggle.com/datasets/erparasrai/english-nepali-pair",
                "language": "ne" if target_lang == 'ne' else "en",
                "script": "Devanagari" if target_lang == 'ne' else "Latin",
                "task": "translation",
                "direction": f"{source_lang}2{target_lang}",
                "instruction": instruction_ne,
                "instruction_en": instruction_en,
                "input": input_text,
                "output": output_text
            }
            f.write(json.dumps(record, ensure_ascii=False) + '\n')
    
    print(f"Created {output_path} with {i//sentences_per_input + 1} examples")
