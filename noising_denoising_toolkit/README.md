# ne_noise — Nepali Noising & Denoising Toolkit (Beta)

`ne_noise` is a **Nepali-first** Python toolkit for text perturbation, orthographic normalization, synthetic data generation, and multi-tier Devanagari ↔ Roman transliteration.

Companion toolkit to the working paper **"Nepali Noising and Denoising Methods"**.

---

## Key Features

1. **Text Normalization (`ne_noise.text`)**: NFC normalization, zero-width joiner/non-joiner cleanup, whitespace collapsing, danda punctuation formatting, and Devanagari character ratio scoring.
2. **Multi-Tier Transliteration (`ne_noise.translit`)**:
   - **Word Tier (`Lexicon`)**: O(1) dictionary lookup backed by 2.4M Devanagari ↔ Roman pairs.
   - **Character Tier (`Rules`)**: Matra-aware, halant-aware, conjunct-aware rule engine supporting `"nepali"` (colloquial) and `"iast"` (scholarly) styles.
   - **Model Tier (`HuggingFace`)**: Lazy wrapper for deep learning transliteration models (e.g., IndicTrans2, M2M100).
3. **Noising Taxonomy (`ne_noise.noise`)**: 19 seedable, deterministic operators across 4 levels:
   - **Character**: deletion, insertion, swap, typo substitution, homophone confusion (श/ष/स, व/ब, इ/ई, ऋ/रि, ज्ञ/ग्य, क्ष/छ्य), phonetic keyboard typos.
   - **Word**: dropout, deletion, swap, permutation, postposition clitic detachment (रामले → राम ले), synonym replacement.
   - **Script**: full transliteration, random word script shift, code-mixing.
   - **Span / Discourse**: T5/BART-style span corruption, random masking, sentence permutation.
4. **Denoising Pair Generator (`ne_noise.denoise`)**: Construct `(clean, noised)` supervised training pairs and JSONL datasets for BART/T5 pretraining or fine-tuning.

---

## Installation & Usage Options

### Option A: Local Development Install (Recommended)
```bash
pip install -e noising_denoising_toolkit
```

Optional extras:
```bash
pip install -e "noising_denoising_toolkit[models]"    # HuggingFace seq2seq backends
pip install -e "noising_denoising_toolkit[lexicon]"   # pandas for 2.4M word dataset
pip install -e "noising_denoising_toolkit[dev]"       # pytest suite
```

### Option B: Direct Manual Import (No Installation Required)
Add the toolkit directory to your Python path:
```python
import sys
sys.path.append("path/to/nepalinlplibrary/noising_denoising_toolkit")

from ne_noise import (
    normalize_nepali_text,
    transliterate_devanagari_to_roman,
    TransliterationEngine,
    apply_noising,
    make_pairs,
)
```

---

## Quickstart Example

```python
from ne_noise import (
    normalize_nepali_text,
    transliterate_devanagari_to_roman,
    TransliterationEngine,
    apply_noising,
    make_pairs,
)

# 1. Normalize Nepali text
clean = normalize_nepali_text("नेपालको   राजधानी\t काठमाडौँ।\u200b")
# Output: "नेपालको राजधानी काठमाडौँ।"

# 2. Transliteration hierarchy: Word (lexicon) -> Character (rules) -> Model
engine = TransliterationEngine()
print(engine.deva_to_roman("काठमाडौँ"))   # Lexicon lookup -> "kathmandu"
print(engine.deva_to_roman("नमस्ते"))      # Lexicon lookup -> "namaste"
print(engine.deva_to_roman("जीवन"))        # Rule fallback -> "jeewan"

# 3. Apply seeded noising operators
noised_mix = apply_noising("नेपालको राजधानी काठमाडौँ हो।", op="code_mix", ratio=0.5, seed=42)
noised_typo = apply_noising("नेपालको राजधानी काठमाडौँ हो।", op="keyboard_typo", seed=42)

# 4. Generate (clean, noised) denoising pairs
pairs = make_pairs(
    ["नेपालको राजधानी काठमाडौँ हो।"],
    ops=["word_dropout", "char_swap", "code_mix"],
    k=2,
    seed=42,
)
for p in pairs:
    print(f"Clean : {p.clean}")
    print(f"Noised: {p.noised}  (ops: {p.ops})")
```

---

## CLI & Demo

Run the interactive demo suite directly:
```bash
python -m ne_noise demo
```

Run the unit test suite (59 tests):
```bash
python -m pytest tests
```

---

## Documentation

- **[PLAN.md](PLAN.md)** — Problem analysis, architecture design, operator taxonomy, transliteration tiers, and development roadmap.
- **`ne_noise/`** — Core library implementation.
- **`tests/`** — Pytest test suite (100% passing).

---

## Citations & References

If you use `ne_noise` or its data/methods in your research, please cite:

```bibtex
@article{nepali_noising_denoising_2026,
  title={Nepali Noising and Denoising Methods},
  author={Paramananda NLP Team},
  journal={Working Paper},
  year={2026}
}
```

### External Datasets & Backends
- **Nepali Roman Transliteration Dataset (~2.4M pairs)**: Saugat Karki (`Saugatkafley/Nepali-Roman-Transliteration`).
- **IndicTrans2**: AI4Bharat (`ai4bharat/indictrans2-indic-indic`).
- **M2M100**: Meta AI (`facebook/m2m100_418M`).
