---
name: research-web-dump
description: Research methodology for web search dumping, domain-specific dataset trigger routing (Roboflow, HuggingFace, Kaggle, Google Scholar, Zenodo, GitHub Awesome lists), and converting raw search dumps into taxonomic hierarchical knowledge.
---

# Research Web Dump & Taxonomic Synthesis Skill

This skill defines the **"Research Web Dump"** methodology for conducting deep technical, dataset, and academic research. It provides guidelines for handling web searches, platform-specific dataset triggers, interactive user prompting, and converting raw web search dumps into structured hierarchical taxonomies.

---

## 1. Core Philosophy: Web Search vs. Raw Web Dumps

- **The Web Search Bottleneck**: Standard search engine summaries can be shallow or miss domain-specific details.
- **The Web Dump Solution**: When automated web search is inadequate, ingest raw text/HTML dumps from authoritative platforms (Roboflow Universe, Google Scholar, Kaggle, HuggingFace, GitHub, Zenodo) into text files (`.txt`) and programmatically synthesize them into **taxonomic, hierarchical markdown knowledge documents (`.md`)**.
- **Case Study Example**: Ingesting raw Roboflow Universe search output (`roboflow.txt`) and running an extraction pipeline to create a structured 300-dataset taxonomy (`roboflow.md`).

---

## 2. Dataset Design & Linguist Satisfaction (e.g., Nepali Multimodal/Image Datasets)

When researching or building multimodal datasets (e.g., Nepali image evaluation datasets):
1. **Industry Alignment**: Prioritize real-world deployment needs (e.g., edge compute, noisy camera inputs, social media image-text pairs).
2. **Linguistic Rigor**: Ensure native linguistic satisfaction by providing dedicated **image annotation tooling** (e.g., CVAT, Label Studio, Roboflow Annotate) tailored for native speakers and expert linguists.
3. **Dual Validation**: Combine automated vision-language metrics (CLIP score, BLEU/chrF) with native human annotator satisfaction scores.

---

## 3. Platform-Specific Search Triggers & Routing

When investigating a research topic, map the query to the correct specialized platform triggers:

| Domain / Resource Type | Target Platform Trigger | Optimal Search Directive |
|------------------------|-------------------------|--------------------------|
| **Computer Vision & Image Datasets** | **Roboflow Universe**, **Kaggle Vision** | Search by project type, downloads (>10), class labels, multi-label multi-class. |
| **NLP & Code-Mixed Corpora** | **HuggingFace Datasets**, **Kaggle**, **OPUS** | Search by language tag (`ne`, `hi-en`), code-switching, transliteration. |
| **Academic Papers & Preprints** | **Google Scholar**, **arXiv**, **ACL Anthology** | Filter top results by citations & data scale in the last 3 years (2023–2026). Ingest review pages. |
| **Open Source Repositories** | **GitHub Awesome Lists**, **GitHub Code Search** | Query `awesome-<topic>`, curated benchmark implementations, models. |
| **Archival & Open Research Data** | **Zenodo**, **OSF**, **PapersWithCode** | Query DOI-registered datasets, benchmark leaderboards. |

---

## 4. Academic Grounding & Interactive User Directives

When tackling advanced or ambiguous research topics:
1. **Grounding Check**: Actively check local notes and ask the user:
   > *"Have you reviewed foundational notes in this workspace? (e.g., `rl_notes.txt`, `flickr8k.md`, `roboflow.md`)"*
2. **Interactive Search Prompting**: If automated search is constrained, prompt the user with targeted parameters:
   - **Topic & Domain**: Exact research focus.
   - **Language & Region**: Script variants (Devanagari, Romanized), regional domain.
   - **Keywords & Boolean Operators**: Specific technical terms (`code-mixed`, `ASR post-correction`, `GEC`).
   - **Action**: Request the user to paste or save a raw search dump (`.txt`) for taxonomy processing.

---

## 5. Hierarchical Taxonomy Synthesis Workflow

When processing a raw search dump file (`<name>.txt`):

```
Raw Text Dump (.txt)
  │
  ├──▶ Step 1: Parse entities (Title, Creator, Scale, Models, Downloads, Class Labels)
  │
  ├──▶ Step 2: Categorize into logical high-level domain taxonomies
  │
  └──▶ Step 3: Generate structured Markdown Taxonomy (.md) with summary tables
```

### Standard Output Document Format (`.md`)
- **Title**: Taxonomy of `[Topic]`
- **Overview & Statistics**: Total entries, domain breakdown table.
- **Hierarchical Sections**: Category headings with bulleted metadata and sample class taxonomies.
