---
name: nltk_nepali_toolkit
description: Canonical NLTK-style low-resource NLP algorithms for Nepali and Indic languages including N-gram Language Modeling (Laplace/Lidstone), PMI Collocation Finders, Sequential POS Taggers, Regexp Chunkers, BLEU/chrF evaluation metrics, and Simplified Lesk WSD.
---

# NLTK Nepali Toolkit (`nltk_nepali_toolkit`)

A zero-dependency, pure Python implementation of canonical NLTK algorithms tailored specifically for Devanagari and low-resource Nepali language engineering.

---

## ⚡ Key Capabilities & Modules

1. **N-Gram Language Models (`NgramLanguageModel`):**
   - Maximum Likelihood Estimation (MLE) with Laplace ($\alpha=1$) and Lidstone smoothing.
   - Cross-entropy sentence perplexity estimation.

2. **Collocations & Association Measures (`CollocationFinder`):**
   - Pointwise Mutual Information (PMI) scoring for identifying idiomatic bigram/trigram compounds.

3. **Sequential POS Tagging (`SequentialPOSTagger`):**
   - Unigram frequency-based tagger backed by 43-tag Nepali morphological heuristics.

4. **Regex Phrase Chunking (`RegexpChunker`):**
   - Shallow parsing of Noun Phrases (`NP`) and Verb Groups (`VP`).

5. **Machine Translation Evaluation Metrics (`sentence_bleu`, `sentence_chrf`):**
   - Word-level BLEU with Brevity Penalty and character n-gram F-score (chrF).

6. **Word Sense Disambiguation (`nepali_lesk`):**
   - Overlap-based Lesk algorithm for IndoWordNet synset definitions.

---

## 💻 Python Usage

```python
import importlib.util

spec = importlib.util.spec_from_file_location(
    "nltk_engine",
    ".agents/skills/nltk_nepali_toolkit/scripts/nltk_engine.py"
)
nltk_ne = importlib.util.module_from_spec(spec)
spec.loader.exec_module(nltk_ne)

# 1. Tokenization
tokens = nltk_ne.word_tokenize("नेपाल एक सुन्दर देश हो।")
print(tokens) # ['नेपाल', 'एक', 'सुन्दर', 'देश', 'हो', '।']

# 2. Translation Evaluation (BLEU & chrF)
hyp = ["नेपाल", "सुन्दर", "छ"]
ref = ["नेपाल", "एक", "सुन्दर", "देश", "हो"]
bleu = nltk_ne.sentence_bleu(hyp, ref)
chrf = nltk_ne.sentence_chrf("नेपाल सुन्दर छ", "नेपाल एक सुन्दर देश हो")
print(f"BLEU: {bleu}, chrF: {chrf}")

# 3. Collocations (PMI)
finder = nltk_ne.CollocationFinder(["प्रधान", "मन्त्री", "काठमाडौँ", "गए", "प्रधान", "मन्त्री"])
print(finder.pmi_bigrams()) # [(('प्रधान', 'मन्त्री'), ...)]
```
