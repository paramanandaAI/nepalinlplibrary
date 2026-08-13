# Linguistic Features Guide: Nepali & Indic NLP

Comprehensive guide for linguistic analysis in low-resource Devanagari texts covering morphosyntax, sequence tagging, syntactic dependency graphs, and entity resolution.

---

## 1. Part-of-Speech (POS) Tagging
- **Standard 43-Tag Set:** Derived from the Prasain (2008) / Madan Puraskar Pustakalaya standard.
- **Key Categories:**
  - `NN` (Common Noun), `NNP` (Proper Noun)
  - `PRP` (Personal Pronoun), `DM` (Demonstrative)
  - `VF` (Finite Verb), `VNF` (Non-Finite Verb), `VAUX` (Auxiliary)
  - `PPO` (Postposition Clitics: *ले, लाई, मा, को, बाट*)
  - `JJ` (Adjective), `RB` (Adverb)
- **Hugging Face Modeling:** Token classification heads over `NepBERTa` / `mDeBERTa-v3` with BIO/Exact tagging.

---

## 2. Morphology & Lemmatization
- **Inflectional Agglutination:**
  - Case markers (विभक्ति): *घर + मा + बाट = घरबाट* (from home).
  - Plurality: *कलम + हरू = कलमहरू* (pens).
  - Verbal Conjugation: Root *खा* (eat) $\to$ *खान्छु* (1st sing pres), *खायो* (3rd sing past), *खानू* (infinitive).
- **Rule & BPE Lemmatization:**
  - Strip 128 canonical inflectional suffixes while checking against root lexicon to avoid over-stemming (*हात $\to$ हा* prevention).

---

## 3. Dependency Parsing
- **Universal Dependencies (UD Nepali):**
  - Root: Head verb of main clause (`root`).
  - Core Arguments: `nsubj` (nominal subject with ergative *ले*), `obj` (direct object), `iobj` (indirect object with dative *लाई*).
  - Non-Core Nominals: `obl` (oblique adverbial with locative *मा* / ablative *बाट*).
- **SOV Clausal Structure:** Verbs occur at clause termination; modifier dependents precede their head words.

---

## 4. Named Entities & Entity Linking
- **NER Categories:** `PER` (Person), `LOC` (Location), `ORG` (Organization), `MISC` (Miscellaneous), `DATE`, `MONEY`.
- **Entity Linking (Wikidata / KB):**
  - Resolving ambiguous mentions (*जनकपुर* $\to$ `Q287115` Janakpurdham) using Dense Retrieval (SBERT / LaBSE) over Nepali knowledge base embeddings.
