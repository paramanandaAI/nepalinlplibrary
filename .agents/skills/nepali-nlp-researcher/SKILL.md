---
name: nepali-nlp-researcher
description: Research methodology, data scaling (pre-training, SFT, RLHF), noising/denoising workflows, LLM-as-a-judge protocols, and grammatical evaluation frameworks tailored for Nepali NLP research.
---

# Nepali NLP Research & Evaluation Skill

This skill defines standard research methodologies, data scaling strategies, dataset generation workflows, and evaluation protocols for low-resource **Nepali NLP**, code-mixing, Romanization denoising, and LLM-assisted workflows.

---

## 1. Taxonomy of Nepali NLP Research & Datasets

### A. Academic & Research Context
- **Kathmandu University (KU ILPRL)** & **Tribhuvan University (Pulchowk/KEC)**: Focus on Devanagari script processing, ASR acoustic-language models, POS tagging, and BERT-based (NepBERTa) Grammatical Error Detection (GED).
- **Model Choice Matrix**:
  | Architecture | Model Family | Primary Use Case | Strengths in Nepali |
  |--------------|--------------|------------------|---------------------|
  | **Encoder Only** | NepBERTa, IndicBERT, XLM-R | Classification, GED, NER, Embedding Search | Excellent subword representations for Devanagari morphology |
  | **Seq2Seq** | mT5, IndicBART, NLLB-200 | Denoising, Transliteration, GEC, Summarization | Robust sequence mapping without autoregressive drift |
  | **Causal LLM** | Llama-3, Gemma-2, Mistral, GPT-4o | SFT, RLAIF, Reasoning, Zero-shot Evaluation | Strong high-level reasoning; requires prompt engineering for Devanagari grammar |

---

## 2. Multi-Stage Noising & Denoising Pipeline

### A. The 3-Stage Normalization Paradigm
To handle extreme code-mixing, Romanized Nepali, and social media informal text:

```
Noisy Source (Roman / Code-Mixed / Typos)
  │
  ├──▶ Stage 1: Devanagari Unaware (Script-level transliteration, exact word order preserved)
  │
  └──▶ Stage 2: Nepali Aware Final (Grammatically corrected Devanagari, English translated, postpositions attached)
```

### B. Agentic Multi-Model Verification Loop
To eliminate LLM hallucination during dataset creation:
1. **Generator**: Gemini 3.6 Flash — translates / normalizes noisy text into candidate Devanagari.
2. **Auditor**: DeepSeek v4 — performs pair-by-pair critique against source (checks for dropped clauses, altered verbs, or deleted slurs).
3. **Refiner**: Gemini 3.6 Flash (High) — executes targeted edits based on audit findings.

---

## 3. Data Scaling Strategy (Pre-training, SFT & RLAIF)

### A. Corpus Filtering & Quadgram Frequency Analysis
- **Removing Colloquial Bias**: Raw social media dumps contain high-frequency colloquial noise. Use **N-gram / Quadgram frequency distribution analysis** to identify and preserve rare, valid linguistic constructs while filtering out repetitive spam/bot patterns.
- **Context Preservation**: Avoid blind word-level random replacement. Synthetic noising must operate within full sentence structures to maintain SOV (Subject-Object-Verb) constraints.

### B. Synthetic Noiser Engine Categories
Organize synthetic noise generators under programmatic modules:
- **`typos_and_chars`**: Random character deletion/swap, matra/halanta dropping & insertion, homophone confusion (`ब/व`, `इ/ई`).
- **`grammar_and_morph`**: Postposition detachment (`सरकारले` → `सरकार ले`), compound splitting (`देशद्रोही` → `देश द्रोही`).
- **`substitutions_and_mixing`**: Transliteration replacement engine, English/Hindi code-switching, dictionary synonym substitution.
- **`structural_and_punctuation`**: Punctuation stripping (ASR speech style), missing space / extra space injection.

---

## 4. Evaluation Framework for Nepali LLMs & Denoising

### A. Automated Quantitative Metrics
- **Character Error Rate (CER)** & **Word Error Rate (WER)**: Essential for ASR transcripts and OCR scan correction.
- **chrF++ & BLEU**: Measures n-gram and subword overlap against clean reference texts.
- **Embedding Similarity (Word2Vec / LaBSE / IndicBERT)**: Evaluates semantic preservation between noisy query and denoised output.

### B. Rule-Based Grammatical Correctness Validation
1. **Postposition Suffix Check**: Verifies that postpositions (`ले`, `लाई`, `को`, `मा`, `बाट`, `देखि`, `सँग`) are correctly attached to stem nouns rather than floating as separate tokens.
2. **Halanta Verification**: Checks word-final consonants for required halantas (e.g., `हुन्छन्`, `छन्`).
3. **Homophone & Spelling Rules**: Audits common misspellings (`बधाई` vs `वधाई`, `ठिक` vs `थक`).
4. **Devanagari Syllable Validator**: Rule-based regex parser checking valid Devanagari consonant-matra combinations.

### C. LLM-as-a-Judge (Zero-Shot & Subjective Persona Evaluation)
Use structured prompts with persona skills for qualitative rating (1–5 scale):

```markdown
Role: Expert Nepali Linguist & Evaluator
Task: Evaluate the candidate Devanagari output against the original source across 3 dimensions:
1. Fluency & Naturalness (प्रवाहशीलता र सहजता): Is the sentence natural Devanagari Nepali?
2. Adequacy & Meaning (अर्थ संरक्षण): Is the original meaning, intent, and tone preserved?
3. Grammatical & Postposition Accuracy (व्याकरण र पदसंगति): Are postpositions attached and spellings accurate?
```

---

## 5. Sharing & Transparency Toolkit

Maintain a toolkit structure in the repository:
- **`sources/`**: Raw (`raw/`), Clean (`clean_corpora/`), Curated Synthetic (`synthetic/`), Factual External (`other_data/`).
- **`modules/`**: Noiser sub-engines (`noisers/`) and dataset builder (`generator/`).
- **`evaluation/`**: Benchmark metrics (`metrics.py`), IR retrieval tests, and human eval rubrics (`human_eval_rubric.md`).
- **`noisingexample.md`**: Transparent single-sentence comparative output for all noise modules.
