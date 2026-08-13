# Language Data, Rules & Processing Pipelines Guide

Scaffolding rule-based matchers, regex patterns, stopwords, and production Hugging Face pipelines for Nepali NLP.

---

## 1. Rule-Based Pattern Matching
- **Devanagari Regex Engine:**
  - Case marker extraction: `r"(\w+)(ले|लाई|मा|को|का|की|बाट|देखि)$"`
  - Currency & South Asian Numbering: `r"(रु\.|नेरू\s*)?(\d{1,3}(?:,\d{2})*(?:,\d{3})*(?:\.\d{1,2})?|\b[०-९]+(?:\.[०-९]+)?)\s*(हजार|लाख|करोड|अरब)?"`
  - Dates (बिक्रम संवत्): `r"(\d{4}|\b[०-९]{4})\s*(बैशाख|जेठ|असार|साउन|भदौ|असोज|कार्तिक|मंसिर|पुष|माघ|फागुन|चैत)\s*(\d{1,2}|[०-९]{1,2})?"`

---

## 2. Processing Pipelines & Transformer Architectures
- **End-to-End Pipeline Stages:**
  1. `Sanitization & NFC Normalization`
  2. `Sentence Boundary Segmentation`
  3. `Subword Tokenization (SentencePiece BPE)`
  4. `Encoder Embedding / Decoder Generation`
  5. `Post-Processing & Output Schema Validation`

- **Preferred Hugging Face Architectures:**
  - **Encoder (Discriminative / Embedding):** `NepBERTa`, `mDeBERTa-v3`, `IndicBERT`
  - **Seq2Seq (Translation / GEC):** `IndicTrans2`, `mBART-50`, `mT5`
  - **Generative LLM (Reasoning / Chat / RAG):** `Gemma 4`, `Llama 3 Indic-adapted`
  - **Multimodal (Vision & Audio):** `Whisper`, `Gemma 4 Vision`, `VITS / Parler-TTS`

---

## 3. Model Saving, Loading & Memory Management
- **Quantization & Batching:**
  - Utilize 4-bit / 8-bit NF4 quantization (`bitsandbytes`) for running 8B+ LLMs on standard GPUs.
  - Set `torch_dtype=torch.bfloat16` and use FlashAttention-2 for sequence lengths $> 2048$.
- **Attention Visualization:**
  - Export self-attention head matrices to visualize syntactic dependency focus (e.g. verb-to-subject attention weights).
