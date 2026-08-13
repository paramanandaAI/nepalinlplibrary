---
name: skill_call_synthesizer
description: Synthetic data generation skill for synthesizing Nepali and English agent tool-calling dialogues, function-call arguments, and multi-turn interaction datasets.
---

# Skill Call Synthesizer

This skill generates structured function-calling and agent tool-calling training dialogues for Nepali NLP tasks, adhering to the canonical schema defined in [`linguistic_adaptation/DATA_SCHEMA.md`](file:///d:/linguistic_adaptation/DATA_SCHEMA.md).

---

## 💻 Python Library Usage

The generator library is located in [`linguistic_adaptation/.agents/skills/skill_call_synthesizer/scripts/synthesizer.py`](file:///d:/linguistic_adaptation/.agents/skills/skill_call_synthesizer/scripts/synthesizer.py) and exposed via [`linguistic_adaptation/.agents/skills/skill_call_synthesizer/scripts/__init__.py`](file:///d:/linguistic_adaptation/.agents/skills/skill_call_synthesizer/scripts/__init__.py):

```python
from .agents.skills.skill_call_synthesizer.scripts import SkillCallSynthesizer

# Generate a single tool-calling sample
sample = SkillCallSynthesizer.generate_single_turn(tool_name="get_nepse_quote")

# Generate a batch of training records
dataset = SkillCallSynthesizer.generate_dataset(num_samples=50)
```

---

## 🛠️ Tool Schema Citations

Synthesized function calls conform strictly to parameter definitions in [`linguistic_adaptation/.agents/skills/nepal_domain_tools/references/tool_schemas.json`](file:///d:/linguistic_adaptation/.agents/skills/nepal_domain_tools/references/tool_schemas.json).

- **Sample Records:** [`linguistic_adaptation/.agents/skills/skill_call_synthesizer/references/sample_calls.json`](file:///d:/linguistic_adaptation/.agents/skills/skill_call_synthesizer/references/sample_calls.json)
- **Target Schema:** [`linguistic_adaptation/DATA_SCHEMA.md`](file:///d:/linguistic_adaptation/DATA_SCHEMA.md)
