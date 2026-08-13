# Tokenization & Text Segmentation Guide

Principles and rules for text segmentation, token merging/splitting, sentence boundary detection, and Devanagari Unicode normalization.

---

## 1. Sentence Segmentation
- **Nepali Sentence Terminators:**
  - Pūrṇa Virāma / Danda: `।` (`\u0964`)
  - Double Danda: `॥` (`\u0965`)
  - Interrogative / Exclamatory: `?`, `!`
  - Ellipsis: `...`, `…`
- **Avoid False Boundaries:** Honorific and bureaucratic abbreviations (*डा.* for Doctor, *प्रा.* for Professor, *नं.* for Number, *ई.* for A.D., *वि.सं.* for B.S.) must not trigger sentence splits.

---

## 2. Tokenization, Merging & Splitting
- **Clitic Splitting (Postpositions):**
  - Syntactic analysis benefits from clitic decomposition: *नेपालको* $\to$ `["नेपाल", "-को"]`.
  - Generation benefits from subword BPE preservation: *नेपालको* as a unified subword cluster.
- **Compound Word Merging:**
  - Sandhi compounds (*विद्या + आलय = विद्यालय*)
  - Hyphenated / Conjunct pairs (*आना-सुकी, घर-बार*).

---

## 3. Devanagari Unicode Mappings & Exceptions
- **Zero-Width Normalization:**
  - Preserve `\u200d` (ZWJ) only when necessary for explicit half-letters (*र्‍*, eyelash-ra).
  - Strip orphan `\u200c` (ZWNJ) and corrupted null spaces.
- **NFC Canonical Decomposition:**
  - Always enforce `unicodedata.normalize('NFC', text)` to combine split vowel matras with their base glyphs.
