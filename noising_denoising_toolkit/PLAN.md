# PLAN — Nepali Noising & Denoising Toolkit (`ne_noise`)

> Companion to the working paper **"Nepali Noising and Denoising Methods"**.
> This document is the architecture plan: what the problem is, what already exists,
> how the toolkit is structured, and where it is going.

---

## 1. Vision

`ne_noise` is a **Nepali-first** Python library for creating and consuming noised text.
Its three jobs:

1. **Noise** — realistic Nepali degradation at every level (character, word, span,
   script, keyboard, homophone) so that anything can be turned into a
   `(clean → noised)` training signal.
2. **Denoise** — orthographic normalization plus the construction of denoising
   objectives/pairs used for pretraining (BART/T5-style) or fine-tuning.
3. **Transliterate** — a **word → character → model** mapping hierarchy for
   Devanagari ↔ Roman(ized) Nepali, usable both as a noising operator (code-mixing,
   romanization) and as a denoising target.

It is a **standalone library** (`pip install ne-noise`), deliberately free of:
- big data (datasets/artifacts live elsewhere),
- data acquisition (fetching/scraping/ingestion lives with data tooling),
- general-purpose utilities (the parent `library/` is reserved for those, later).

It is the successor to the legacy code, which has been fully refactored and integrated into `ne_noise`.

---

## 2. Problem Analysis — why a refactor

The previous folder (`noising_denoising_toolkit/`) was a grab-bag. Inventory:

| Piece | What it did | Verdict |
|-------|-------------|---------|
| `synthetic/` | Real, working noising functions (transliteration, homonym, noise engine, perturbations) | **Core asset** — refactored into `ne_noise` |
| `synthetic_tools/noising.py` | Scaffold with `raise NotImplementedError` TODOs | Refactored/wired into `ne_noise/noise/` |
| `synthetic_tools/transliterator.py` | Duplicate translit scaffold (TODO) | **Duplication** — replaced by `translit/` |
| `synthetic_tools/augment.py` | JSONL augmenter with hardcoded absolute Windows paths | Refactored into `pipelines/` |
| `fetch.py`, `transform.py`, `validate.py`, `manifest.py`, `pipelines/*`, `scrapers/*`, `ingest_*.py` | Data ingestion pipeline | **Out of scope** (data tooling) → `legacy/` |
| `transliterate/`, `augmentation/` | Empty scaffolds (pyproject only) | Absorbed into `ne_noise` |
| `chhanda/`, `autocomplete/`, `classify/`, `generator/`, `tabular/` | Unrelated tool scaffolds | Preserved in `legacy/` |
| `__init__.py`, `__main__.py` | Exported ingestion API + ingestion CLI | Replaced by `ne_noise` API + CLI |

**Concrete problems found:**
1. **Broken imports** — `pipelines/ingestion_pipeline.py` imported `toolkit.fetch`,
   a package that does not exist; `synthetic/word_transliteration.py` imported
   `synthetic.transliteration` assuming a top-level package.
2. **Triplicated transliteration** — `synthetic/transliteration.py` (working),
   `synthetic_tools/transliterator.py` (TODO), `transliterate/` (empty).
3. **Unexposed API** — `__init__.py` exported only data-ingestion functions, not the
   noising work that was the folder's actual purpose.
4. **Scaffolds not wired** — `noising.py` TODOs never connected to the working
   `synthetic/` implementations.
5. **No tests, no demo, no data** — despite the folder being intended as a module
   "with tests and demo data for testing hypotheses".
6. **Environment-coupled code** — `augment.py` hardcoded `D:/paramananda/...`.

---

## 3. Design Principles

1. **Nepali-first.** Devanagari realities drive everything: matras, halant
   conjuncts, anusvara/chandrabindu, danda punctuation, homophone confusions
   (श/ष/स, व/ब, इ/ई, ऋ/रि, ज्ञ/ग्य, क्ष/छ्य), postposition clitics, schwa
   deletion, and the Devanagari↔Roman script pair.
2. **Library-first.** Importable, documented, dependency-free core (stdlib only);
   heavy deps (pandas, torch, transformers) are optional and lazy.
3. **Deterministic & seedable.** Every noise op accepts `seed`/`rng` for
   reproducible experiments (essential for hypothesis testing).
4. **Composable.** Ops are registry entries usable alone, randomly, or as composed
   pipelines: `apply_noising` / `apply_random_noising` / `apply_composed_noising`.
5. **Tiered mapping.** Transliteration goes word → character → model, with graceful
   fallback down the hierarchy.
6. **Data-agnostic.** The library never owns big data; it accepts paths. The demo
   ships tiny sample data inside the folder for hypothesis testing.
7. **Everything preserved.** No legacy work is deleted — it all moves to `legacy/`.

---

## 4. Target Architecture

```
noising_denoising_toolkit/
├── pyproject.toml               # installable as `ne-noise` (import `ne_noise`)
├── PLAN.md                      # this document
├── README.md                    # quickstart
├── ne_noise/                    # THE library
│   ├── __init__.py              # public API
│   ├── __main__.py              # python -m ne_noise (demo | translit | pairs)
│   ├── text/                    # Nepali text primitives
│   │   ├── scripts.py           # Devanagari ranges, is_devanagari, ratio, char class
│   │   └── normalize.py         # ZWJ/ZWNJ cleanup, whitespace, danda, NFC
│   ├── translit/                # word -> character -> model
│   │   ├── rules.py             # character tier: rule-based Devanagari<->Roman
│   │   ├── lexicon.py           # word tier: dataset-backed dictionary (O(1))
│   │   ├── model.py             # model tier: lazy HF transliteration wrapper
│   │   ├── engine.py            # TransliterationEngine + default singleton
│   │   └── data/                # small sample lexicon (big dataset via scripts/)
│   ├── noise/                   # noising operators (the "support" transformations)
│   │   ├── char.py              # deletion/insertion/swap/substitution, inject_random_noise
│   │   ├── homophone.py         # Nepali homophone confusion pairs
│   │   ├── word.py              # dropout/permute/swap/clitic detachment/synonym
│   │   ├── script.py            # code-mix, transliterate_full / random words
│   │   ├── span.py              # BART/T5-style span corruption, masking, sentence permute
│   │   ├── keyboard.py          # phonetic-keyboard neighbor typos
│   │   └── engine.py            # NOISE_OPS registry + compose/random/apply API
│   ├── denoise/                 # the denoising side
│   │   ├── normalize.py         # orthographic canonicalization
│   │   └── pairs.py             # make (clean, noised) pairs, JSONL IO
│   ├── models/                  # pretrained-model wrappers + install guides
│   │   ├── base.py              # Noiser/Denoiser/Transliterator wrapper interface
│   │   ├── huggingface.py       # lazy HF loaders
│   │   └── README.md            # install guide + recommended models
│   ├── pipelines/               # pipelines have their own folder
│   │   └── noising_pipeline.py  # JSONL in -> noised pairs JSONL out + report
│   ├── scripts/                 # one-off downloads (2.4M translit dataset)
│   └── demo/                    # demo data path for testing hypotheses
│       ├── demo.py              # end-to-end demo (CLI or import)
│       └── data/sample_nepali.jsonl
├── tests/                       # pytest suite (stdlib-only, no network)
└── legacy/                      # every pre-refactor file, untouched
```

---

## 5. The Noising Taxonomy (for the paper)

| Level | Operator | Nepali detail |
|-------|----------|---------------|
| Character | deletion / insertion / swap / substitution | operate on Devanagari chars, keep spaces |
| Character | homophone substitution | श/ष/स, व/ब, इ/ई, उ/ऊ, ऋ/रि, ज्ञ/ग्य, क्ष/छ्य, ं/ँ… |
| Character | keyboard typo | phonetic-keyboard neighbor confusion (क↔ख↔ग…) |
| Word | dropout / permute / swap | sentence-level reordering |
| Word | clitic detachment | रामले → राम ले (postposition clitics) |
| Word | synonym replacement | small built-in Nepali synonym table (extensible) |
| Span | span corruption / infilling | BART/T5 pretraining objective with `<mask>` |
| Span | sentence permutation | discourse-level |
| Script | full transliteration | Devanagari → Roman (whole text) |
| Script | random-word transliteration | partial script shift |
| Script | code-mix | mixed Devanagari/Roman in one sentence |

Composition: `inject_random_noise`, `apply_random_noising`, `apply_composed_noising`.

**Why this taxonomy matters to the paper:** each level targets a distinct failure mode
of Nepali text — matra/char typos, homophonic misspellings, keyboard slips,
code-mixed social-media text, clitic-heavy morphology, and OCR/scan noise — and each
can be evaluated independently as a denoising task.

---

## 6. The Denoising Side

- **Rule-based normalization** (`denoise/normalize.py`): NFC, zero-width/bidi
  artifact removal, whitespace/danda canonicalization. (Unambiguous fixes only.)
- **Homophone ambiguity** (e.g., correcting श/स in the right word) is genuinely
  word-dependent, so:
- **Pair construction** (`denoise/pairs.py`): build `(id, clean, noised, ops)` from
  any noise recipe. These pairs are the supervised denoising/pretraining signal
  (T5-style text-to-text, BART-style span corruption, GEC-style spelling tasks).
- **Model-based denoising** (`models/huggingface.py`): wrapper around any HF
  seq2seq denoiser for inference/evaluation; install guide in `models/README.md`.

---

## 7. Transliteration Hierarchy — word → character → model

The user-requested core concept, and the trickiest Nepali-specific component:

1. **Word tier (`translit/lexicon.py`)** — O(1) dictionary lookup.
   - Full dataset: `Saugatkafley/Nepali-Roman-Transliteration` (~2.4M pairs),
     downloaded by `ne_noise/scripts/download_word_transliteration.py` (big data —
     not vendored).
   - Sample lexicon ships in `translit/data/` for demo/tests.
   - Handles real words rules can't: `काठमाडौँ → kathmandu`, `धन्यवाद → dhanyabaad`.
2. **Character tier (`translit/rules.py`)** — rule-based Devanagari↔Roman:
   - matra-aware syllable building (क+े→ke, क्+ष→ksha), anusvara/chandrabindu,
     nukta variants (क़, फ़), halant conjuncts;
   - two romanization styles: `"nepali"` (colloquial, ee/oo, schwa-deleted finals:
     राम→ram) and `"iast"` (scholarly, ii/uu, rāma);
   - reverse direction restores schwa (ram→राम) and is documented as ambiguous for
     ट/त, ड/द, ण/न — the inherent ambiguity of ASCII romanization.
3. **Model tier (`translit/model.py`)** — optional, lazy HF wrapper for OOV /
   natural romanization; used only when available (see `models/README.md`).

The engine falls back down the chain: `model → lexicon → rules`. Every noise op that
needs transliteration (`script.py`) uses the engine, so experiments can flip tiers
with one argument.

---

## 8. Model Integration & Install Guides

- `models/base.py` defines `BaseNoiser` / `BaseDenoiser` / `BaseTransliterator`
  so custom backends drop in cleanly.
- `models/huggingface.py` lazily loads HF pipelines (`text2text-generation`,
  translation) for kinds: `denoiser`, `transliterator`. No import cost until used.
- `models/README.md` documents: install steps (`pip install "ne-noise[models]"`),
  recommended model families (IndicTrans2/ai4bharat, M2M100, T5/BART for denoising,
  Romanized-Nepali fine-tunes), and how to register a custom wrapper.
- Parent-repo `models/` (currently empty) is the intended home for pretrained
  checkpoints; `ne_noise` stays wrapper-only.

---

## 9. Pipelines

Pipelines have their own folder (`ne_noise/pipelines/`) because noising is one thing,
pipelines are another. Currently one: `NoisingPipeline` — reads any JSONL, applies a
noise recipe per record, writes `(clean, noised)` pairs plus a small stats report.
Future pipeline candidates: denoising-eval loop, batch transliteration, corpus
augmentation at scale.

---

## 10. Relationship to the Rest of the Repo

| Where | Relationship |
|-------|--------------|
| `noising_denoising_toolkit/` | This library (active: `ne_noise/`, ref: `legacy/`). |
| `library/` | **Later** expansion for general/language-wide tools & utils. `ne_noise` stays lean; shared utilities may graduate here eventually. |
| data tooling (elsewhere) | `fetch/transform/validate/manifest/scrapers/ingest` are data-acquisition concerns → moved to `legacy/`, live outside the library. |
| `models/` (parent) | Pretrained checkpoints; `ne_noise/models/` are wrappers. |
| Big datasets | External; `ne_noise` only points at paths / downloads via `scripts/`. |

---

## 11. Testing Strategy

`tests/` is stdlib-only, offline, deterministic:

- `test_text.py` — normalization, Devanagari ratio, script detection.
- `test_translit.py` — known words both directions, styles, tier fallback, lexicon hit.
- `test_noise_char.py` / `test_noise_word.py` / `test_noise_script.py` /
  `test_noise_span.py` — each operator, seeded, boundary `p=0.0`/`p=1.0`.
- `test_noise_engine.py` — registry integrity, composed/random application, reproducibility.
- `test_denoise.py` — pair building, JSONL round-trip, orthographic normalization.
- `test_pipeline.py` — end-to-end JSONL → pairs → report.

Run with `python -m pytest`.

---

## 12. Demo & Hypothesis-Testing Workflow

`ne_noise/demo/demo.py` (+ `demo/data/sample_nepali.jsonl`) is the in-folder data path
for testing hypotheses. It prints and writes (to `demo/output/`):

1. normalization of raw Nepali;
2. all three transliteration tiers on the same words (showcasing word > char);
3. every noising operator on the demo sentences;
4. denoising pairs; and a small corruption report.

Because every op is seeded and composable, hypotheses like
"keyboard noise preserves more Devanagari ratio than random substitution" are testable
in a few lines:

```python
from ne_noise.text.scripts import devanagari_ratio
from ne_noise import apply_noising
r = devanagari_ratio(apply_noising(text, "keyboard_typo", seed=1))  # compare against "random_char_substitution"
```

---

## 13. Roadmap

- [x] **M0 — Restructure & preserve**: `legacy/` snapshot, `ne_noise` skeleton, packaging.
- [x] **M1 — Working core**: text primitives, translit tiers, full noise taxonomy,
      denoise pairs, pipeline, demo, tests.
- [ ] **M2 — Paper experiments**: corruption-level sweeps, per-op Devanagari-ratio /
      BLEU / denoising-recovery benchmarks in `demo/`; results feed the paper.
- [ ] **M3 — Models**: real HF denoiser/transliterator wrappers verified against a
      Nepali benchmark set; install guides finalized; checkpoints land in parent `models/`.
- [ ] **M4 — library/ graduation**: move battle-tested generic utilities into parent
      `library/`; keep `ne_noise` focused.

---

## 14. Decisions Log

- Package/import name: **`ne_noise`** (project `ne-noise`).
- Full restructure now; legacy preserved at `legacy/`.
- Core is stdlib-only; pandas/torch/transformers are optional extras.
- Romanization default style `"nepali"` (colloquial) to match existing conventions
  and real-world romanized Nepali data.
