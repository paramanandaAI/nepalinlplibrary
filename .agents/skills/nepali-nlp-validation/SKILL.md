---
name: nepali-nlp-validation
description: Validation rules and script checking heuristics for low-resource Nepali annotation tasks. Outlines rules for Devanagari validation, spelling-error checks, and postposition detacher validators.
---

# nepali-nlp-validation Skill

This skill provides validation rules and checks to ensure grammatical correctness and consistent formatting of Devanagari text annotations.

---

## 1. Script Validation Heuristics

When `language` tag is `ne`, `mai`, or `new`, the text must consist of native Devanagari characters:
- **Devanagari Unicode Block Range**: `U+0900` to `U+097F`.
- **Validation check**: If the caption contains Latin alphabetical characters (`[A-Za-z]`), trigger an inline warning card recommending Roman-to-Devanagari script transliteration or indicating that the text is code-mixed.

---

## 2. spelling-error & Matra-Halanta dropping checks

spelling errors in informal text (OCR transcriptions, social media posts) frequently drop or misplace markers:
- **Matra Drop**: Dropping vowels (e.g. `नेपाल` written as `नपाल`).
- **Halanta Drop**: Dropping the halanta vowel-suppressor (e.g. `महान्` written as `महान`).
- **Insertion check**: Highlight cases where non-standard characters (like independent vowels in place of Matras, e.g. `नेपाअल्`) are present.
- **Rule**: Emphasize checking word endings to ensure Halantas are preserved where linguistically appropriate.

---

## 3. Nepali Postpositions Attachment Validator

Nepali postpositions (such as `ले`, `लाई`, `बाट`, `को`, `मा`, `सङ्ग`) are syntactically attached directly to their host noun/pronoun:
- **Correct**: `रामले` (Ram-agent), `घरमा` (at home).
- **Incorrect (Split)**: `राम ले`, `घर मा`.
- **Validation logic**: Check captions for separated postposition tokens. If found, highlight the mismatch and suggest joining them to satisfy formal Nepali grammar standards.
- **ASR Post-correction**: Conversational speech (ASR) often introduces split pauses. Validating these joins is critical to ensure high-quality pre-training corpora.
