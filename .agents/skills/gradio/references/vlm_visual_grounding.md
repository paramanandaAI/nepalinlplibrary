# VLM Visual Grounding & Quality Control

This guide documents the design of Automated Audit Loops and Multimodal Evaluation Frameworks (using Vision-Language Models) to verify dataset quality.

---

## 1. Multi-Model Ingestion & Audit Loop

Linguistic datasets for low-resource translation and image-captioning require automated audit checks before human review. We apply a **Multi-Model Pipeline** to prepare candidate inputs:

```
        +--------------------------------------------+
        | Ingestion: Upload Image & Raw Meta         |
        +--------------------------------------------+
                              │
                              ▼
  +--------------------------------------------------------+
  | Stage 1: Candidate Translation (Gemini 3.6 Flash)       |
  | Generates Devanagari translation from Romanized text.  |
  +--------------------------------------------------------+
                              │
                              ▼
  +--------------------------------------------------------+
  | Stage 2: Quality Audit (DeepSeek v4)                   |
  | Audits source-target meaning consistency, drops, or    |
  | grammatical inaccuracies.                              |
  +--------------------------------------------------------+
                              │
                              ▼
  +--------------------------------------------------------+
  | Stage 3: Refinement (Gemini 3.6 Flash High)            |
  | Generates corrected target text & feedback remarks.    |
  +--------------------------------------------------------+
                              │
                              ▼
        +--------------------------------------------+
        | Output: Write to localized YAML Sidecar    |
        +--------------------------------------------+
```

### Sidecar Mapping of Audit Logs
Audit loops write directly to the `llm_evaluation` block of the image's `.yml` sidecar:
```yaml
llm_evaluation:
  generator: "gemini-3.6-flash"
  auditor: "deepseek-v4"
  status: "flagged" # approved, flagged, pending
  clip_score: 0.285
  audit_critique: "The candidate translation dropped the word 'hill' (डाँडा)."
  corrected_candidate: "डाँडामाथि बादल मडारिएको मन्सुनको खेत।"
```

---

## 2. Multimodal Quality Metrics

To ensure captioned text matches the visual content of the image:
1. **CLIP Alignment Score**: Run a local CLIP model (e.g., `ViT-B/32`) on the image and candidate caption. Store the cosine similarity score in the metadata.
2. **Text Similarity (chrF / BLEU)**: Compare the LLM-generated translation against historical clean corpora.
3. **Human Rubric Validation**: Build a standard evaluation rubric inside the workbench.

---

## 3. Rendering Audit Comparisons in Gradio

To help linguists quickly verify LLM candidate caption quality, we design a **Pairwise Comparison Layout**:

- **Left Panel**: Target Image + Source Text.
- **Center Panel**: Multi-Model candidate translations and their audit critiques.
- **Right Panel**: A list of radio buttons for ratings (e.g., `1 - Poor (meaning changed)`, `2 - Fair (minor spelling/postposition error)`, `3 - Excellent (grammatically correct)`).
- **Behavior**: Clicking a rating automatically updates the YAML sidecar, increments the dashboard statistics, and advances the annotation queue.
