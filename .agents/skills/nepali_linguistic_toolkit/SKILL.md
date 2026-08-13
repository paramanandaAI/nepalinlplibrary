---
name: nepali_linguistic_toolkit
description: Comprehensive NLP toolkit and linguistic guides for low-resource Nepali text processing, Devanagari transliteration (IAST/ASCII/SLP1), sentence segmentation, clitic tokenization, rule-based matching, polarity classification, and Trie-based n-gram autocomplete.
---

# Nepali Linguistic Toolkit & NLP Processing Guide

Provides production-ready algorithms, linguistic guides, and processing pipelines for the Nepali language and Devanagari script.

---

## 📚 Linguistic Architecture & Guides (`references/guides/`)

1. **Linguistic Features (`references/guides/linguistic_features.md`):**
   - 43-tag canonical Nepali Part-of-Speech tagset.
   - Inflectional agglutination, case postpositions (विभक्ति), and verbal conjugation.
   - Universal Dependencies (UD Nepali) and syntactic SOV graphs.
   - Named Entity Recognition (`PER`, `LOC`, `ORG`, `MISC`) and entity linking.

2. **Tokenization & Segmentation (`references/guides/tokenization_segmentation.md`):**
   - Sentence boundary segmentation respecting Danda (`।`) and abbreviations (*डा., प्रा., वि.सं.*).
   - Clitic splitting (*नेपालको $\to$ नेपाल + -को*), Sandhi merging, and NFC normalization.

3. **Vectors & Semantic Similarity (`references/guides/vectors_similarity.md`):**
   - FastText subword embeddings, NpVec1, and Sentence-BERT bi-encoders.
   - Cosine similarity ranking and LaBSE cross-lingual alignment.

4. **Language Data & Matchers (`references/guides/language_data_rules.md`):**
   - Rule-based regex matchers for Bikram Sambat dates and South Asian currency grouping (*लाख, करोड*).
   - Transformers & Large Language Models (`Gemma 4`, `NepBERTa`, `IndicTrans2`, `Whisper`).
   - Memory management, 4-bit NF4 quantization, and attention visualizers.

---

## 💻 Python API Usage

```python
import importlib.util
from pathlib import Path

# Load pipeline utilities
spec = importlib.util.spec_from_file_location(
    "pipeline_utils",
    ".agents/skills/nepali_linguistic_toolkit/scripts/pipeline_utils.py"
)
nlp = importlib.util.module_from_spec(spec)
spec.loader.exec_module(nlp)

# 1. Sentence Segmentation
sentences = nlp.segment_sentences("डा. राम काठमाडौँ गए। उनले भात खाए।")
print(sentences) # ['डा. राम काठमाडौँ गए।', 'उनले भात खाए।']

# 2. Clitic-Aware Tokenization
tokens = nlp.tokenize_words("रामले नेपालको इतिहास पढे।", split_clitics=True)
print(tokens) # ['राम', '-ले', 'नेपाल', '-को', 'इतिहास', 'पढे।']

# 3. Rule-Based Pattern Extraction
entities = nlp.extract_named_patterns("वि.सं. २०८१ बैशाख १५ मा रु. ५०,००० कारोबार भयो।")
print(entities) # {'dates': ['२०८१ बैशाख १५'], 'currency': ['रु. ५०,०००']}
```
