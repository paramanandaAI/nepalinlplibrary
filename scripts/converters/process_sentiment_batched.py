import pandas as pd
import json
from pathlib import Path
import numpy as np

def label_to_str(label):
    label = str(label).strip()
    if label == '-1' or label == '-1.0':
        return 'नकारात्मक (Negative)'
    elif label == '0' or label == '0.0':
        return 'तटस्थ (Neutral)'
    elif label == '1' or label == '1.0':
        return 'सकारात्मक (Positive)'
    else:
        return 'अज्ञात (Unknown)'

def main():
    print("Loading Nepali Sentiment Analysis dataset...")
    csv_path = Path(r"D:\linguistic_adaptation\lemmatization\other_sources\kaggle\sentiment_analysis_nepali_final.csv")
    
    # Read the dataset. There are three columns: Index, Sentences, Sentiment
    try:
        df = pd.read_csv(csv_path)
    except Exception as e:
        print(f"Error reading CSV: {e}")
        return
        
    print(f"Original dataset size: {len(df)}")
    
    # Clean dataframe
    if 'Sentences' not in df.columns or 'Sentiment' not in df.columns:
        print("Columns 'Sentences' or 'Sentiment' not found.")
        print(f"Found columns: {df.columns}")
        return
        
    df = df.dropna(subset=['Sentences', 'Sentiment'])
    # Optional: shuffle dataset to ensure diverse batches
    df = df.sample(frac=1, random_state=42).reset_index(drop=True)
    
    records = []
    batch_size = 10
    total_batches = len(df) // batch_size
    
    for i in range(total_batches):
        batch = df.iloc[i*batch_size : (i+1)*batch_size]
        
        input_text = ""
        output_text = ""
        sentences_list = []
        
        for j in range(batch_size):
            row = batch.iloc[j]
            sentence = str(row['Sentences']).strip()
            sentiment_val = row['Sentiment']
            sentiment_str = label_to_str(sentiment_val)
            
            input_text += f"वाक्य {j+1}:\n{sentence}\n\n"
            output_text += f"वाक्य {j+1}: {sentiment_str}\n"
            
            sentences_list.append({
                "sentence_num": j+1,
                "sentence": sentence,
                "label": int(float(sentiment_val)),
                "sentiment_text": sentiment_str
            })
            
        input_text = input_text.strip()
        output_text = output_text.strip()
        
        records.append({
            "id": f"sentiment-batch10-{i+1:05d}",
            "instruction": "तल दिइएका १० वटा नेपाली वाक्यहरूको भावना (Sentiment) मूल्याङ्कन गरी प्रत्येक वाक्यको भावना (सकारात्मक, नकारात्मक, वा तटस्थ) प्रदान गर्नुहोस्। (Evaluate the sentiment of the following 10 Nepali sentences and provide whether each is Positive, Negative, or Neutral.)",
            "input": input_text,
            "output": output_text,
            "num_sentences": batch_size,
            "sentences": sentences_list,
            "language": "ne",
            "script": "Devanagari",
            "task": "sft/sentiment_analysis/batched_10",
            "source": "kaggle.com/datasets/Nepali-Sentiment-Analysis",
            "license": "unknown"
        })
        
    out_dir = Path(r"D:\linguistic_adaptation\lemmatization\sentence_data\sentiment")
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / "sentiment_batched_10.jsonl"
    
    print(f"Writing {len(records)} batched records to {out_path}...")
    with open(out_path, "w", encoding="utf-8") as f:
        for rec in records:
            f.write(json.dumps(rec, ensure_ascii=False) + "\n")
            
    print("Done!")

if __name__ == "__main__":
    main()
