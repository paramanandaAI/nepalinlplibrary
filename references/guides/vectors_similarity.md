# Vectors, Embeddings & Semantic Similarity Guide

Architectures and methodologies for continuous vector representation, semantic search, and cross-lingual alignment in Nepali NLP.

---

## 1. Word & Subword Vectors
- **FastText & Skip-Gram with NCE Loss:** Captures subword n-gram character morphs for OOV (out-of-vocabulary) handling in highly inflected Devanagari words.
- **NpVec1:** Pretrained word embeddings for 500k+ Nepali vocabulary tokens (Koirala & Niraula, 2021).

---

## 2. Sentence Embeddings (Sentence-BERT & LaBSE)
- **Siamese Bi-Encoder Architecture:**
  - Forward pass encodes sentences $u = \text{Encoder}(s_1)$ and $v = \text{Encoder}(s_2)$.
  - Similarity metric: $\text{Cosine}(u, v) = \frac{u \cdot v}{\|u\| \|v\|}$.
- **Loss Functions:**
  - Multiple Negatives Ranking Loss (MNRL) over $(Q, P^+, P^-)$ triplets.
  - Cosine Similarity Loss on graded STS benchmarks (0.0 to 5.0 scale).

---

## 3. Cross-Lingual Vector Alignment
- **LaBSE (Language-Agnostic BERT Sentence Embeddings):** Maps Nepali sentences into the same shared representation space as English, Hindi, and 100+ languages for zero-shot cross-lingual retrieval.
