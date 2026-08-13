# Modern NLP Ecosystem & Feature Mapping Guide: spaCy & Hugging Face for Nepali

This guide provides a comprehensive architectural mapping of modern NLP capabilities (from the spaCy Universe, Hugging Face transformers, and low-resource Indic toolkits) adapted for Nepali language processing.

---

## 🗺️ Capability & Tool Mapping

| Feature Category | spaCy / Universe Origin | Hugging Face & Nepali Adaptation | Key Nepali Task Subfolder |
|---|---|---|---|
| **Few-Shot Classification** | `SetFit`, `Classy Classification` | `setfit/setfit` with `NepBERTa` / `mDeBERTa-v3` | `data/datasets/candidate/sft/classification/` |
| **Span-Based NER** | `SpanMarker`, `GLiNER` | `tomaarsen/SpanMarkerNER` with BIO entity tagging | `data/datasets/candidate/sft/token_tagging/` |
| **Keyphrase Extraction** | `PyTextRank`, `KeyBERT` | `KeyBERT` over `NpVec1` / `Sentence-BERT` embeddings | `data/datasets/candidate/sft/summarization/` |
| **Entity Linking** | `spaCyOpenTapioca`, `spaCy fishing` | Dense retrieval over Devanagari Wikidata KB (`QIDs`) | `data/datasets/candidate/sft/structured_output/` |
| **Document & PDF Layout** | `spacy-layout`, `spacypdfreader` | `LayoutLMv3` / `Donut` / `NepaliPixel OCR` | `data/datasets/candidate/multimodal/ocr/` |
| **Grammar Correction** | `Contextual Spell Check` | `GECToR` / `IndicTrans2` / `mBART` Seq2Seq | `data/datasets/candidate/sft/gec/` |
| **WordNet & Polysemy** | `spacy-wordnet` | IndoWordNet Nepali Synset graphs & Lesk algorithm | `data/datasets/candidate/sft/wsd/` |
| **Coreference Resolution** | `Coreferee`, `neuralcoref` | Cross-lingual coreference with pronominal saliency | `data/datasets/candidate/sft/anaphora/` |
| **Speech-to-Text Pipeline** | `spaCy Whisper` | `openai/whisper-large-v3` + CTC ASR decoder | `data/datasets/candidate/multimodal/asr/` |
| **PII & Data Redaction** | `Presidio`, `scrubadub` | Rule-based & NER-based Nepali phone/ID redactor | `data/datasets/candidate/sft/instruction/` |
| **Readability & Metrics** | `spacy_readability`, `TextDescriptives` | Syllable-weight (Laghu/Guru) & Gunning-Fog metric | `nepalinlplibrary/.agents/skills/chhanda_agentic` |
| **Syntactic Dependency** | `displaCy`, `deplacy`, `spacy-udpipe` | Universal Dependencies (UD Nepali) treebanks | `data/datasets/candidate/sft/dependency_parsing/` |
| **Interactive Serving** | `spacy-streamlit`, `FastAPI` | Streamlit demo & FastAPI async endpoints | `demos/` |


---

## 🛠️ Hugging Face Native Implementations

### 1. Few-Shot Sentence Classification (SetFit)
```python
from setfit import SetFitModel, Trainer, TrainingArguments
from datasets import load_dataset

# Efficient few-shot training on 8-16 examples per class
model = SetFitModel.from_pretrained("Shushant/nepaliBERT")
# Trainer fine-tunes bi-encoder with Contrastive Loss
```

### 2. Zero-Shot Entity Extraction (GLiNER)
```python
from gliner import GLiNER

model = GLiNER.from_pretrained("urchade/gliner_multi-v2.1")
text = "डा. राम प्रसाद काठमाडौँको त्रिभुवन विश्वविद्यालयमा पढाउँछन्।"
labels = ["व्यक्ति (Person)", "स्थान (Location)", "संस्था (Organization)"]
entities = model.predict_entities(text, labels)
```

### 3. Keyphrase & Topic Extraction (KeyBERT)
```python
from keybert import KeyBERT

kw_model = KeyBERT(model="sentence-transformers/LaBSE")
keywords = kw_model.extract_keywords(
    "नेपालको कृषि क्षेत्रमा धान, मकै र गहुँको उत्पादन महत्त्वपूर्ण मानिन्छ।",
    keyphrase_ngram_range=(1, 2),
    stop_words=None
)
```
