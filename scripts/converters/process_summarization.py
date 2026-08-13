import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
import json
from pathlib import Path

def main():
    print("Loading Kaggle Nepali news summaries dataset...")
    csv_path = Path(r"D:\linguistic_adaptation\lemmatization\other_sources\kaggle\nepali_news_summaries.csv")
    df = pd.read_csv(csv_path)
    
    # Drop any nulls
    df = df.dropna(subset=['article', 'summary'])
    df = df.reset_index(drop=True)
    
    print(f"Loaded {len(df)} articles. Computing TF-IDF...")
    # Use TF-IDF
    vectorizer = TfidfVectorizer(max_features=10000)
    tfidf_matrix = vectorizer.fit_transform(df['article'])
    
    num_samples = 1000
    print(f"Selecting {num_samples} most dissimilar articles using Greedy K-Center on TF-IDF...")
    
    # Greedy K-Center Initialization
    selected_indices = []
    
    # Start with a random index (or first one)
    np.random.seed(42)
    first_idx = np.random.randint(0, len(df))
    selected_indices.append(first_idx)
    
    # Track the maximum cosine similarity to the selected set for each point
    # We want to pick the point that has the MINIMUM max-similarity to the chosen ones
    # Initial similarities to the first selected point
    max_sims = linear_kernel(tfidf_matrix[first_idx], tfidf_matrix).flatten()
    
    for i in range(1, num_samples):
        # Find the point that is "farthest" from the currently selected set
        # i.e., the one with the smallest maximum similarity to the selected set
        next_idx = np.argmin(max_sims)
        selected_indices.append(next_idx)
        
        # Update max_sims with the new point
        new_sims = linear_kernel(tfidf_matrix[next_idx], tfidf_matrix).flatten()
        max_sims = np.maximum(max_sims, new_sims)
        
        if i % 100 == 0:
            print(f"Selected {i}/{num_samples} articles...")

    print(f"Selected {num_samples} articles. Saving to JSONL...")
    selected_df = df.iloc[selected_indices]
    
    # Create the output directory
    out_dir = Path(r"D:\linguistic_adaptation\lemmatization\sentence_data\summarization")
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / "nepali_news_summaries_dissimilar_1000.jsonl"
    
    records = []
    for idx, row in selected_df.iterrows():
        records.append({
            "id": f"news-summary-{idx}",
            "instruction": "तल दिइएको समाचार लेखको सारांश लेख्नुहोस्। (Summarize the given news article.)",
            "input": str(row['article']).strip(),
            "output": str(row['summary']).strip(),
            "language": "ne",
            "script": "Devanagari",
            "task": "sft/summarization",
            "source": "kaggle.com/datasets/adhikarykishan/nepali-news-summary",
            "license": "unknown"
        })
        
    with open(out_path, "w", encoding="utf-8") as f:
        for rec in records:
            f.write(json.dumps(rec, ensure_ascii=False) + "\n")
            
    print(f"Successfully saved {num_samples} dissimilar articles to {out_path}")

if __name__ == "__main__":
    main()
