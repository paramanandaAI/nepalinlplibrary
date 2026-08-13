# ACL SIG Domain Taxonomy & Quality Filtering Specifications

This reference document defines the complete ACL Anthology Special Interest Group (SIG) domain taxonomy, task categories, and quality filtering thresholds for Nepali NLP.

---

## 🏛️ ACL SIG Domain Taxonomy

- **SIGMORPHON / FSMNLP**: Morphological analysis, postposition splitting, matra/halanta diacritic normalization.
- **SIGLEX**: Lexicon building, WordNet synset mapping, bilingual word alignment (`word2word`).
- **ArgMining**: Legal argument mining, stance detection, case law QA (*G-LARA* framework).
- **DISRPT / CODI / CRAC**: Discourse processing, coreference resolution, sentence segmentation.
- **SIGPARSE**: Dependency parsing, constituent parsing, treebank annotation for Nepali.
- **LChange / LT4HALA**: Diachronic language change, ancient Nepal script (Ranjana/Prachalit) manuscript OCR.
- **ComputEL / BabyLM**: Sample-efficient low-resource pretraining & benchmark evaluation.
- **BEA / NLPerspectives**: Grammatical Error Correction (GEC), writing evaluation, proficiency feedback.
- **BioNLP / FinNLP / CrisisNLP**: Domain-specific SFT (healthcare, agriculture, financial markets, disaster response).

---

## 📏 Quality Tiers & Filtering Thresholds

| Quality Tier | Criteria | Metric Thresholds |
|---|---|---|
| **`gold`** | Human-annotated / Expert-reviewed | Accuracy = 100%, Devanagari Ratio $\ge 90\%$ |
| **`silver`** | High-precision synthetic NMT / LLM | chrF++ $> 45.0$, COMET $> 0.70$, Devanagari Ratio $\ge 80\%$ |
| **`bronze`** | Unfiltered web-scraped / Machine-translated | Devanagari Ratio $\ge 70\%$ |

---

## 🏷️ Provenance Tracking Fields

Every record carries provenance tracking fields:
```json
{
  "id": "task-source-000001",
  "source": "huggingface.co/datasets/...",
  "language": "ne",
  "script": "Devanagari",
  "task": "sft/gec",
  "quality_tier": "gold",
  "license": "cc-by-4.0"
}
```
