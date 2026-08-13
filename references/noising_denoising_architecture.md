# Noising–Denoising Architecture Reference

With the rise of code-mixing, Romanized Nepali, and informal writing on digital platforms, this document outlines the architecture, pipeline design, and perturbation methods for Nepali text denoising, normalization, and Devanagari generation.

---

## Multi-Stage T5 Denoising Pipeline

```
noisy (raw social media / ASR / OCR)
  │
  ├──▶ Stage 1: Devanagari Unaware (script-only transliteration)
  │
  └──▶ Stage 2: Nepali Aware Final (grammar-corrected natural Nepali)
```

### Model Curation & Verification Workflow
- **Translation / Nepalification**: Gemini 3.6 Flash
- **Review & Auditing**: DeepSeek v4
- **Final Refinement & Quality Assurance**: Gemini 3.6 Flash (High)

---

## Noising Methods & Operators

- **Substitution**: Transliteration replacement, English/Hindi code-switching, synonyms
- **Typographical & Phonetic**: Matra deletion (`matra_drop`), halanta drop (`halanta_drop`), QWERTY typos (`keyboard_typo`), homophone & homonym confusion (`ब/व`, `छ/च`, `फूल/फुल`)
- **Morphological & Syntactic**: Postposition detachment (`clitic_detachment`: `सरकारले` → `सरकार ले`), compound splitting
- **Structural**: Punctuation stripping (`punctuation_strip`), space segmentation errors

---

## Data Sources

- **Rakshak: Toxic Content Benchmark** (Biraj Bhusal et al., 2024) — [HuggingFace](https://huggingface.co/datasets/biraj-bhusal/rakshak-nepali-toxicity-final)
- **Nepali Flow Colloquial Dataset** — `Boredoom17/Nepali-Flow-Colloquial`
- **Nepali-English Code-Switching ASR** — `devrahulbanjara/ne-en-codeswitching-asr-technical-interview`
- **RoundTrip OCR Nepali** — `cfilt/RoundTripOCR-nepali`

---

## Implications & Future Applications

- Safety alignment & toxicity detection for code-mixed multilingual LLMs
- Information Retrieval (IR) & semantic search robustness on noisy queries
- ASR transcript post-correction & Devanagari OCR error recovery
