# Low-Resource Nepali Dictionary Specifications

This document outlines the architectural and schema differences between **Unigram Frequency Dictionaries** (used for Autocomplete engines) and **DBPedia / Wikidata Entity Dictionaries** (used for Knowledge Graphs & Entity Linking).

---

## 1. Unigram Frequency Dictionary (`unigrams.jsonl` / `unigrams.csv`)

### Purpose
Used by the `toolkits/autocomplete` engine for prefix lookup, frequency learning, and heap-based top-$k$ word suggestions.

### Required Schema
```json
{
  "word": "नेपाल",
  "frequency": 154200,
  "pos_tag": "NNP" // optional
}
```

### Key Properties
- **Granularity**: Token / Word level.
- **Lookup Key**: Word prefix string (e.g. `ने`).
- **Ordering Metric**: Corpus frequency count (`frequency`).

---

## 2. DBPedia / Wikidata Entity Dictionary (`wikidata_nepali_dict.jsonl`)

### Purpose
Used for Named Entity Recognition (NER), Knowledge Graph Question Answering (KGQA), and Entity Linking in Nepalese NLP pipelines.

### Required Schema
```json
{
  "entity_id": "Q1544",
  "label": "सगरमाथा",
  "aliases": ["माउन्ट एभरेस्ट", "Mount Everest", "Sagarmatha"],
  "description": "संसारको सबैभन्दा अग्लो चुचुरो",
  "type": "Mountain",
  "dbpedia_uri": "http://dbpedia.org/resource/Mount_Everest",
  "wikidata_uri": "http://www.wikidata.org/entity/Q1544",
  "attributes": {
    "elevation_m": 8848.86,
    "location": "सोलुखुम्बु, नेपाल"
  }
}
```

### Key Properties
- **Granularity**: Concept / Entity level.
- **Lookup Key**: Entity ID, Label, or Aliases.
- **Ordering Metric**: Graph centrality / PageRank / Similarity score.
