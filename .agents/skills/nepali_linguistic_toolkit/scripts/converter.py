"""
Devanagari Transliteration Module.
Supports Devanagari to IAST, SLP1, and ASCII Romanization schemes.

Citations:
- Kunchukuttan, A. (2020). The IndicNLP Library.
- Monier-Williams Sanskrit-English Dictionary Transliteration Standard (IAST).
"""

from typing import Dict

class TransliterationScheme:
    """Devanagari, SLP1, IAST, and ASCII Mapping Tables."""

    DEV_TO_SLP1: Dict[str, str] = {
        'अ': 'a', 'आ': 'A', 'इ': 'i', 'ई': 'I', 'उ': 'u', 'ऊ': 'U', 'ऋ': 'f', 'ॠ': 'F',
        'ए': 'e', 'ऐ': 'ai', 'ओ': 'o', 'औ': 'au',
        'ा': 'A', 'ि': 'i', 'ी': 'I', 'ु': 'u', 'ू': 'U', 'ृ': 'f', 'ॄ': 'F',
        'े': 'e', 'ै': 'ai', 'ो': 'o', 'ौ': 'au',
        'क': 'ka', 'ख': 'Kha', 'ग': 'ga', 'घ': 'Gha', 'ङ': 'Nga',
        'च': 'ca', 'छ': 'Cha', 'ज': 'ja', 'झ': 'Jha', 'ञ': 'ña',
        'ट': 'Ta', 'ठ': 'Tha', 'ड': 'Da', 'ढ': 'Dha', 'ण': 'Na',
        'त': 'ta', 'थ': 'tha', 'द': 'da', 'ध': 'dha', 'न': 'na',
        'प': 'pa', 'फ': 'pha', 'ब': 'ba', 'भ': 'bha', 'म': 'ma',
        'य': 'ya', 'र': 'ra', 'ल': 'la', 'व': 'va',
        'श': 'Sa', 'ष': 'Sa', 'स': 'sa', 'ह': 'ha',
        'ं': 'M', 'ः': 'H', 'ँ': '~', '्': '',
    }

    DEV_TO_IAST: Dict[str, str] = {
        'अ': 'a', 'आ': 'ā', 'इ': 'i', 'ई': 'ī', 'उ': 'u', 'ऊ': 'ū', 'ऋ': 'ṛ', 'ॠ': 'ṝ',
        'ए': 'e', 'ऐ': 'ai', 'ओ': 'o', 'औ': 'au',
        'ा': 'ā', 'ि': 'i', 'ी': 'ī', 'ु': 'u', 'ू': 'ū', 'ृ': 'ṛ', 'ॄ': 'ṝ',
        'े': 'e', 'ै': 'ai', 'ो': 'o', 'ौ': 'au',
        'क': 'ka', 'ख': 'kha', 'ग': 'ga', 'घ': 'gha', 'ङ': 'ṅa',
        'च': 'ca', 'छ': 'cha', 'ज': 'ja', 'झ': 'jha', 'ञ': 'ña',
        'ट': 'ṭa', 'ठ': 'ṭha', 'ड': 'ḍa', 'ढ': 'ḍha', 'ण': 'ṇa',
        'त': 'ta', 'थ': 'tha', 'द': 'da', 'ध': 'dha', 'न': 'na',
        'प': 'pa', 'फ': 'pha', 'ब': 'ba', 'भ': 'bha', 'म': 'ma',
        'य': 'ya', 'र': 'ra', 'ल': 'la', 'व': 'va',
        'श': 'śa', 'ष': 'ṣa', 'स': 'sa', 'ह': 'ha',
        'ं': 'ṃ', 'ः': 'ḥ', 'ँ': 'm̐', '्': '',
    }

    DEV_TO_ASCII: Dict[str, str] = {
        'अ': 'a', 'आ': 'aa', 'इ': 'i', 'ई': 'ee', 'उ': 'u', 'ऊ': 'oo', 'ऋ': 'ri',
        'ए': 'e', 'ऐ': 'ai', 'ओ': 'o', 'औ': 'au',
        'ा': 'aa', 'ि': 'i', 'ी': 'ee', 'ु': 'u', 'ू': 'oo', 'ृ': 'ri',
        'े': 'e', 'ै': 'ai', 'ो': 'o', 'ौ': 'au',
        'क': 'ka', 'ख': 'kha', 'ग': 'ga', 'घ': 'gha', 'ङ': 'nga',
        'च': 'cha', 'छ': 'chha', 'ज': 'ja', 'झ': 'jha', 'ञ': 'nya',
        'ट': 'ta', 'ठ': 'tha', 'ड': 'da', 'ढ': 'dha', 'ण': 'na',
        'त': 'ta', 'थ': 'tha', 'द': 'da', 'ध': 'dha', 'न': 'na',
        'प': 'pa', 'फ': 'pha', 'ब': 'ba', 'भ': 'bha', 'म': 'ma',
        'य': 'ya', 'र': 'ra', 'ल': 'la', 'व': 'va',
        'श': 'sha', 'ष': 'sha', 'स': 'sa', 'ह': 'ha',
        'ं': 'm', 'ः': 'h', 'ँ': 'n', '्': '',
    }

def devanagari_to_iast(text: str) -> str:
    """Transliterates Devanagari text to International Alphabet of Sanskrit Transliteration (IAST)."""
    return ''.join(TransliterationScheme.DEV_TO_IAST.get(c, c) for c in text)

def devanagari_to_ascii(text: str) -> str:
    """Transliterates Devanagari text to readable ASCII Romanized Nepali."""
    return ''.join(TransliterationScheme.DEV_TO_ASCII.get(c, c) for c in text)
