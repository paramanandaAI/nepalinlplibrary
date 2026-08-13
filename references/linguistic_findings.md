# Linguistic & Empirical Findings

## Key Observations in Nepali Social Media & Informal Text

1. **Postposition Detachment**:
   - Informal social media writers frequently detach grammatical postpositions from stem words (e.g. `sarkar le` / `सरकार ले` instead of `सरकारले`, `bhawan ko` / `भवन को` instead of `भवनको`).

2. **Compound Word Fragmentation**:
   - Compound words in Nepali break frequently in casual writing (e.g. `भूमि पुत्रहरु` instead of `भूमिपुत्रहरू`, `देश द्रोही` instead of `देशद्रोही`).

3. **Code-Mixing & Transliteration Heterogeneity**:
   - Text on digital platforms is rarely monolingual Devanagari. It is heavily mixed with Romanized Nepali (`bhrastachar`), English terms (`budget`, `police`, `ID`), and numeric variations (`19k` vs `१९ हजार`).

4. **Multi-Stage T5 Target Pipeline Strategy**:
   - Translating directly from noisy text to natural Nepali is hard for baseline models. Breaking the pipeline into two stages:
     - **Stage 1 (`devanagari_unaware`)**: Blind character/script-level transliteration.
     - **Stage 2 (`nepali_aware_final`)**: Grammar-aware normalization (postposition joining, halantas, English translation, spelling correction).
   - This 2-stage structure significantly improves model convergence and generation fluency.

5. **Data Quality & Verification**:
   - Automated LLM translation of noisy Nepali text often introduces hallucination (e.g. dropping clauses, changing violent verbs like `मारेका` to `घेरेका`).
   - A multi-model verification workflow (Gemini 3.6 Flash for translation → DeepSeek v4 for audit → Gemini 3.6 Flash High for final fixes) is essential to preserve ground truth integrity.
