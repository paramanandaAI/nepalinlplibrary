# Nepali NLP Library (`nepalinlplibrary`)

A collection of **Nepali-first** Natural Language Processing (NLP) toolkits, text perturbation engines, transliteration pipelines, and language adaptation utilities.

> Companion repository for the working paper **"Nepali Noising and Denoising Methods"**.

---

## Repository Architecture

```
nepalinlplibrary/
├── noising_denoising_toolkit/    # ne_noise: Nepali Noising, Denoising & Transliteration (Beta)
│   ├── ne_noise/                 # Core Python package
│   │   ├── text/                 # Devanagari primitives, NFC normalization, ratio math
│   │   ├── translit/             # Word -> Character -> Model 3-tier transliteration
│   │   ├── noise/                # 19 character, word, span, and script noising ops
│   │   ├── denoise/              # Supervised (clean, noised) pair construction
│   │   ├── models/               # Lazy HuggingFace & seq2seq wrappers
│   │   ├── pipelines/            # Batch JSONL noising pipelines
│   │   └── demo/                 # Interactive demo & hypothesis testing
│   ├── tests/                    # Pytest test suite (59 unit tests)
│   ├── pyproject.toml            # Package configuration (ne-noise)
│   └── PLAN.md                   # Architecture plan & roadmap
├── library/                      # General-purpose Nepali NLP modules (OCR, segmentation, etc.)
├── models/                       # Model architecture checkpoints & wrappers
└── test/                         # Experimental prompts, benchmarks, & MCP tools
```

---

## Toolkits Overview

### 1. `noising_denoising_toolkit` (`ne_noise`) — Beta
A comprehensive toolkit for generating realistic Nepali text degradation (typos, homophone confusions, clitic detachment, code-mixing, span masking) and constructing supervised denoising training pairs.

#### Quickstart Usage

```python
from ne_noise import (
    normalize_nepali_text,
    transliterate_devanagari_to_roman,
    TransliterationEngine,
    apply_noising,
    make_pairs,
)

# Text Normalization
clean = normalize_nepali_text("नेपालको   राजधानी\t काठमाडौँ।")

# Multi-Tier Transliteration (Lexicon -> Rules -> Model)
engine = TransliterationEngine()
print(engine.deva_to_roman("काठमाडौँ"))   # Output: "kathmandu" (lexicon)
print(engine.deva_to_roman("नमस्ते"))      # Output: "namaste" (lexicon)
print(engine.deva_to_roman("जीवन"))        # Output: "jeewan" (character rules)

# Seeded Noising Operators (19 operators available)
noised = apply_noising("नेपालको राजधानी काठमाडौँ हो।", op="code_mix", ratio=0.5, seed=42)

# Generate Denoising Pairs for Training (BART / T5 / GEC)
pairs = make_pairs(
    ["नेपालको राजधानी काठमाडौँ हो।"],
    ops=["word_dropout", "keyboard_typo", "code_mix"],
    k=2,
    seed=42,
)
```

#### Running Tests & Demo
```bash
# Run test suite
cd noising_denoising_toolkit
python -m pytest tests

# Run interactive demo
python -m ne_noise demo
```

---

## Design Principles

1. **Nepali-First Realities**: Devanagari matras, halant conjuncts, anusvara/chandrabindu, danda punctuation, and homophone confusions (श/ष/स, व/ब, इ/ई, ऋ/रि, ज्ञ/ग्य, क्ष/छ्य).
2. **Deterministic & Seedable**: Every perturbation function supports explicit random seeds for reproducible NLP experiments.
3. **Modular & Importable**: Pure Python stdlib core with zero required external dependencies (optional heavy dependencies like `pandas` or `transformers` are lazy-loaded).
4. **Standalone Modules**: Each toolkit can be imported locally or included directly in custom workflows without mandatory PyPI publishing.

---

## Citations & References

If you use this repository or `ne_noise` in your academic or applied research, please cite:

```bibtex
@article{nepali_noising_denoising_2026,
  title={Nepali Noising and Denoising Methods},
  author={Paramananda NLP Team},
  journal={Working Paper},
  year={2026}
}
```

### Acknowledgments & Data Sources
- **Nepali Roman Transliteration Dataset**: [Saugatkafley/Nepali-Roman-Transliteration](https://huggingface.co/datasets/Saugatkafley/Nepali-Roman-Transliteration) (~2.4M pairs).
- **IndicTrans2**: [AI4Bharat IndicTrans2](https://github.com/AI4Bharat/IndicTrans2).
- **Meta M2M100**: [facebook/m2m100_418M](https://huggingface.co/facebook/m2m100_418M).

---

## License

This project is licensed under the Apache 2.0 License - see the [LICENSE](LICENSE) file for details.
