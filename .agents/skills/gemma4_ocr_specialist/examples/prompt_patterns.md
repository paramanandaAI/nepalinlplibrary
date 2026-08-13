# Gemma 4 E2B OCR Prompt Patterns

These are standard prompt patterns used by the Gemma 4 OCR Specialist to achieve high-quality Nepali text extraction, translation, and validation.

## 1. Extract and Translate (Standard Document)
**Use Case:** Basic Nepali documents where both the native text and an English translation are required.
**Soft Tokens:** 280 (Default)
**Prompt:**
> "Extract all Nepali text exactly as it appears in the image, ensuring correct UTF-8 encoding. Following the extraction, provide a full English translation of the text."

## 2. Structured KYC Form Extraction
**Use Case:** Identity documents, application forms, and structured records.
**Soft Tokens:** 560 (Dense)
**Prompt:**
> "Extract all text from this KYC document. Identify form fields such as Name, Date of Birth, Address, and ID Number. Return the extracted data as a clean JSON object with English keys and the extracted Nepali values."

## 3. Two-Pass Verification (Confidence Estimation)
**Use Case:** High-stakes extraction where accuracy is critical.
**First Pass:** (Standard Extraction)
**Second Pass Prompt:**
> "I previously extracted this Nepali text from the image: <extracted_text>. Please compare this text to the image. Identify any missing words, misread characters, or ambiguous regions. Provide a confidence score from 0 to 100 for the overall extraction quality."

## 4. Adversarial / Anomaly Check
**Use Case:** Detecting tampered ID cards or forms.
**Soft Tokens:** 560 to 1120 (Max Detail)
**Prompt:**
> "Analyze this identity document. Extract the text, but also look for visual anomalies around the Name, Date of Birth, and ID Number fields that might indicate tampering or modification. Report any suspicious findings."
