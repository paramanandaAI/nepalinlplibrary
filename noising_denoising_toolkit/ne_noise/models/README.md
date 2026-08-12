# Models — Pretrained Wrappers & Install Guide

`ne_noise.models` provides **wrappers**, not weights. Pretrained checkpoints and
fine-tuned models live in the parent repo's `models/` directory; these wrappers
lazy-load them from HuggingFace on demand.

## Install

```bash
# Base library (no heavy deps)
pip install -e noising_denoising_toolkit

# Model wrappers (transformers + torch)
pip install -e "noising_denoising_toolkit[models]"
```

If you only need CPU inference on a small model, torch CPU wheels are enough:

```bash
pip install torch --index-url https://download.pytorch.org/whl/cpu
pip install transformers
```

## Recommended Model Families

### Transliteration (Devanagari <-> Roman)

| Model | Use |
|-------|-----|
| `ai4bharat/indic-trans` | Indic script transliteration/translation baseline |
| `ai4bharat/indictrans2-indic-indic` | Modern IndicTrans2, script conversion across Indic scripts |
| `facebook/m2m100_418M` | Multilingual seq2seq; script transfer via language pair |

> `ne_noise.translit` already provides deterministic word + character tiers; the
> model tier is for OOV words and natural romanization.

### Denoising

| Model | Use |
|-------|-----|
| `t5-small` / `t5-base` | Text-to-text denoising; span-corruption pretraining |
| `facebook/bart-base` | Denoising autoencoder pretraining family |
| Nepali fine-tunes (GEC / spelling) | Downstream denoising benchmarks |

## Usage

```python
from ne_noise.models import load_hf_model

denoiser = load_hf_model("denoiser")          # lazy; nothing downloaded yet
if denoiser.available():
    clean = denoiser.apply("नेपालक राजधानी काठमाडौँ ह")

translit = load_hf_model("transliterator")
if translit.available():
    roman = translit.deva_to_roman("काठमाडौँ")
```

## Adding a Custom Wrapper

Subclass one of the interfaces in `models/base.py`:

```python
from ne_noise.models import BaseDenoiser

class MyDenoiser(BaseDenoiser):
    def apply(self, noised_text: str) -> str:
        ...
        return clean_text
```

Then pass it wherever a backend is expected (e.g., as `noising_fn` in
`ne_noise.denoise.make_pairs`, or swap it into a `TransliterationEngine`).

## Roadmap Notes

- Verify each wrapper against a Nepali benchmark set (M2 experiments in PLAN.md).
- Fine-tuned Nepali checkpoints will be registered in the parent `models/` folder.
