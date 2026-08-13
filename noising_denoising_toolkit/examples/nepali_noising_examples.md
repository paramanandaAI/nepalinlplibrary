# Synthetic Noising Examples (Single Sentence Demo)

**Original Clean Reference Sentence**:
> `सरकारले आज स्थानीय निकायका कर्मचारी र प्राविधिकलाई नयाँ बजेटबाट प्रोत्साहन भत्ता दिने निर्णय गर्यो।`

---

## Noise Module Outputs

### 1. Postposition Detachment (`PostpositionSplitter`)
- **Noised Output**: `सरकार ले आज स्थानीय निकायका कर्मचारी र प्राविधिक लाई नयाँ बजेट बाट प्रोत्साहन भत्ता दिने निर्णय गर्यो।`
- **Noise Effect**: Detaches suffixes/postpositions (`ले`, `लाई`, `बाट`) from preceding nouns.

### 2. Matra & Halanta Removal (`MatraHalantaNoiser`)
- **Noised Output**: `सरकारले अज स्थानिय निकायका कर्मचारी र प्राविधकलाई नया बजेटबाट प्रोत्साहन भत्ता दिने निर्णय गर्यो।`
- **Noise Effect**: Simulates fast-typing or OCR errors by dropping vowel signs (*matraas*) and *halanta* diacritics.

### 3. Punctuation Stripping (`PunctuationNoiser`)
- **Noised Output**: `सरकारले आज स्थानीय निकायका कर्मचारी र प्राविधिकलाई नयाँ बजेटबाट प्रोत्साहन भत्ता दिने निर्णय गर्यो`
- **Noise Effect**: Removes sentence terminators (`।`, `?`) and punctuation marks to simulate raw ASR speech transcripts.

### 4. Transliteration & Romanization (`TransliterationEngine`)
- **Noised Output**: `sarkar le aaja sthaniye nikayeka karmachari ra prabidhik lai naya budget bata प्रोत्साहन भत्ता dine nirnaya garyo.`
- **Noise Effect**: Replaces Devanagari words with Romanized Nepali or English equivalents, creating code-mixed input.

### 5. Phonetic / Homophone Confusion (`PhoneticConfusionNoiser`)
- **Noised Output**: `सरकारले आज स्थानीय निकायका कर्मचारी र प्राबिधिकलाई नयाँ बजेटबाट प्रोत्साहन भत्ता दिने निरनय गरयो।`
- **Noise Effect**: Swaps phonetically similar letters (e.g. `व` ↔ `ब`, `इ` ↔ `ई`, `ण` ↔ `न`).

### 6. Composite Multi-Noise Pipeline (`DatasetBuilder`)
- **Noised Output**: `sarkar le aaja sthaniye nikayeka karmachari ra prabidhik lai naya budget bata bhatta dine nirnaya garyo`
- **Noise Effect**: Applies postposition detachment + transliteration replacement + punctuation stripping in sequence to produce real-world social media style text.
