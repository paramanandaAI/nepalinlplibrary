"""
Low-Resource Nepali Data Synthesis & Augmentation Library.
Provides domain-aware perturbation methods (orthographic noise, OCR typo simulation,
synonym/entity replacement, character swaps, deletion) tailored for low-resource Devanagari text.

Academic Citations:
- Wei, J., & Zou, K. (2019). EDA: Easy Data Augmentation Techniques for Boosting Performance on Text Classification Tasks (EMNLP).
- Kunchukuttan, A. et al. (2020). AI4Bharat IndicNLP Corpus and Noise Modeling.
- Sennrich, R. et al. (2016). Improving NMT with Monolingual Data (ACL).
"""

import json
import random
from pathlib import Path
from typing import List, Dict, Any, Optional

DATA_DIR = Path(__file__).parent.parent / "references"

def _load_json(filename: str) -> Dict[str, Any]:
    file_path = DATA_DIR / filename
    if file_path.exists():
        with open(file_path, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

class NepaliTextAugmenter:
    """Specialized data augmentation for low-resource Nepali text."""

    # Common orthographic and OCR confusion pairs in Devanagari
    ORTHOGRAPHIC_CONFUSIONS = {
        "श": "स", "ष": "स", "स": "श",
        "ब": "व", "व": "ब",
        "भ": "म", "म": "भ",
        "ण": "न", "न": "ण",
        "ध": "घ", "घ": "ध",
        "इ": "ई", "ई": "इ",
        "उ": "ऊ", "ऊ": "उ",
        "ि": "ी", "ी": "ि",
        "ु": "ू", "ू": "ु",
        "ऋ": "रि", "रि": "ऋ",
        "ज्ञ": "ग्य", "ग्य": "ज्ञ",
        "क्ष": "छ्य", "छ्य": "क्ष"
    }

    @classmethod
    def inject_orthographic_noise(cls, sentence: str, p: float = 0.15) -> str:
        """Injects typical low-resource Devanagari spelling / OCR confusion noise."""
        chars = list(sentence)
        for i, c in enumerate(chars):
            if c in cls.ORTHOGRAPHIC_CONFUSIONS and random.random() < p:
                chars[i] = cls.ORTHOGRAPHIC_CONFUSIONS[c]
        return "".join(chars)

    @classmethod
    def random_swap(cls, sentence: str, n_swaps: int = 1) -> str:
        """Randomly swaps two words in the sentence n times."""
        words = sentence.split()
        if len(words) < 2:
            return sentence
        words = list(words)
        for _ in range(n_swaps):
            idx1, idx2 = random.sample(range(len(words)), 2)
            words[idx1], words[idx2] = words[idx2], words[idx1]
        return " ".join(words)

    @classmethod
    def random_deletion(cls, sentence: str, p: float = 0.1) -> str:
        """Randomly deletes words with probability p."""
        words = sentence.split()
        if len(words) <= 2:
            return sentence
        new_words = [w for w in words if random.random() > p]
        return " ".join(new_words) if len(new_words) >= 2 else words[0]

    @classmethod
    def entity_replacement(cls, sentence: str) -> str:
        """Replaces named entities (places, names) with alternatives from reference database."""
        p_data = _load_json("person.json")
        g_data = _load_json("geographic.json")
        
        first_names = p_data.get("first_names", ["राम", "श्याम", "हरि", "गीता", "सीता"])
        districts = g_data.get("districts", ["काठमाडौँ", "पोखरा", "चितवन", "भोजपुर", "सोलुखुम्बु"])
        
        words = sentence.split()
        for i, w in enumerate(words):
            if w in first_names:
                words[i] = random.choice([n for n in first_names if n != w])
            elif w in districts:
                words[i] = random.choice([d for d in districts if d != w])
        return " ".join(words)

    @classmethod
    def augment(cls, text: str) -> List[str]:
        """Generates multiple augmented variants of input Nepali text."""
        return [
            cls.inject_orthographic_noise(text, p=0.2),
            cls.random_swap(text, n_swaps=1),
            cls.random_deletion(text, p=0.15),
            cls.entity_replacement(text)
        ]
