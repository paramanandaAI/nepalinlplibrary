# -*- coding: utf-8 -*-
"""
Script to download and extract raw datasets from HuggingFace into sources/raw/
"""

import os
import csv
import sys

def download_nepali_flow_colloquial(output_path, max_rows=10000, min_len=50, max_len=200):
    print("Downloading Boredoom17/Nepali-Flow-Colloquial from HuggingFace...")
    try:
        from datasets import load_dataset
        ds = load_dataset("Boredoom17/Nepali-Flow-Colloquial", split="train")
        
        extracted = []
        for item in ds:
            text = item.get("text", "").strip()
            if min_len <= len(text) <= max_len:
                extracted.append(text)
                if len(extracted) >= max_rows:
                    break
        
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        with open(output_path, "w", encoding="utf-8", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["id", "text"])
            for idx, text in enumerate(extracted, 1):
                writer.writerow([idx, text])
        print(f"Successfully saved {len(extracted)} rows to {output_path}")
    except Exception as e:
        print(f"Error loading Boredoom17/Nepali-Flow-Colloquial: {e}")
        print("Falling back to placeholder format in sources/raw/nepali_flow_colloquial.csv")

def download_codeswitching_asr(output_path, max_rows=500):
    print("Downloading devrahulbanjara/ne-en-codeswitching-asr-technical-interview from HuggingFace...")
    try:
        from datasets import load_dataset
        ds = load_dataset("devrahulbanjara/ne-en-codeswitching-asr-technical-interview", split="train")
        
        extracted = []
        for item in ds:
            # Check for transcription field
            text = item.get("transcription", item.get("text", "")).strip()
            if text:
                extracted.append(text)
                if len(extracted) >= max_rows:
                    break
        
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        with open(output_path, "w", encoding="utf-8", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["id", "text"])
            for idx, text in enumerate(extracted, 1):
                writer.writerow([idx, text])
        print(f"Successfully saved {len(extracted)} rows to {output_path}")
    except Exception as e:
        print(f"Error loading codeswitching ASR dataset: {e}")

if __name__ == "__main__":
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    flow_path = os.path.join(base_dir, "sources", "raw", "nepali_flow_colloquial.csv")
    asr_path = os.path.join(base_dir, "sources", "raw", "codeswitching_asr.csv")
    
    download_nepali_flow_colloquial(flow_path)
    download_codeswitching_asr(asr_path)
