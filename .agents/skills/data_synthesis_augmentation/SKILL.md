---
name: data_synthesis_augmentation
description: Specialized data augmentation and text perturbation skill for expanding low-resource Nepali language datasets via orthographic noise injection, OCR confusion modeling, named entity substitution, and word-level perturbations.
---

# Low-Resource Nepali Data Synthesis & Augmentation Skill

This skill provides domain-tailored data synthesis and text perturbation techniques for low-resource Nepali NLP. It models phonological substitutions, orthographic ambiguities (e.g. `श/ष/स`, `व/ब`, `इ/ई`), and entity-preserving swaps.

---

## 💻 Python Library Usage

The augmentation engine is located in [`linguistic_adaptation/.agents/skills/data_synthesis_augmentation/scripts/augment.py`](file:///d:/linguistic_adaptation/.agents/skills/data_synthesis_augmentation/scripts/augment.py) and exposed via [`linguistic_adaptation/.agents/skills/data_synthesis_augmentation/scripts/__init__.py`](file:///d:/linguistic_adaptation/.agents/skills/data_synthesis_augmentation/scripts/__init__.py):

```python
from .agents.skills.data_synthesis_augmentation.scripts import NepaliTextAugmenter

text = "राम काठमाडौँमा नयाँ कामको खोजीमा छन्।"

# 1. Generate multi-strategy augmented variants
variants = NepaliTextAugmenter.augment(text)

# 2. Inject Devanagari orthographic / OCR noise
noisy_text = NepaliTextAugmenter.inject_orthographic_noise(text, p=0.25)
# Output: "राम काठमाण्डौमा नया कामको खोजिमा छन।"

# 3. Entity replacement (places and names from reference dictionaries)
swapped_entity = NepaliTextAugmenter.entity_replacement(text)
# Output: "श्याम पोखरामा नयाँ कामको खोजीमा छन्।"
```

---

## 📚 Academic & Low-Resource Citations

1. **Text Augmentation & Perturbation:**
   - **Wei, J., & Zou, K. (2019)**: *EDA: Easy Data Augmentation Techniques for Boosting Performance on Text Classification Tasks*, Proceedings of the 2019 Conference on Empirical Methods in Natural Language Processing (EMNLP).
2. **Indic Orthographic Normalization & Noise Modeling:**
   - **Kunchukuttan, A., et al. (2020)**: *The IndicNLP Library and Devanagari Noise Modeling*, AI4Bharat.
3. **Synthetic Expansion for Low-Resource MT & LLMs:**
   - **Sennrich, R., Haddow, B., & Birch, A. (2016)**: *Improving Neural Machine Translation Models with Monolingual Data*, ACL Anthology.
