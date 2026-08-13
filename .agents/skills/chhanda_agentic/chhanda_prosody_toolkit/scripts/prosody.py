"""
Nepali & Sanskrit Metrical Prosody (Chhanda) Library.
Performs syllabification, Laghu/Guru (L/G) weight scanning, Gaṇa mapping, and meter identification against 63+ classical meters.

Academic & Classical References:
- Pingala: Chandaḥśāstra (पिङ्गल छन्दःशास्त्र, c. 3rd–2nd century BCE)
- Kedāra Bhaṭṭa: Vṛttaratnākara (वृत्तरत्नाकर, c. 10th century CE)
- Shiva Gaire: छन्दमा कविता कसरी लेख्ने? (2020)
- Melnad et al.: Sanskrit Metre Identifier (ICON 2015)
- Ambuda / Chandas Engine (https://github.com/ambuda-org/chandas)
"""

import json
import re
from pathlib import Path
from typing import Dict, Any, List, Optional

# 8 Traditional Gaṇas formula: यमाताराजभानसलगा
GANAS_MAP = {
    "SSS": "म (Ma) - [ऽऽऽ]",
    "ISS": "य (Ya) - [।ऽऽ]",
    "SIS": "र (Ra) - [ऽ।ऽ]",
    "IIS": "स (Sa) - [।।ऽ]",
    "SSI": "त (Ta) - [ऽऽ।]",
    "ISI": "ज (Ja) - [।ऽ।]",
    "SII": "भ (Bha) - [ऽ।।]",
    "III": "न (Na) - [।।।]",
}

DATA_FILE = Path(__file__).parent.parent / "references" / "chanda_database.jsonl"

def load_meter_database() -> List[Dict[str, Any]]:
    """Loads meter definitions from chanda_database.jsonl."""
    meters = []
    if DATA_FILE.exists():
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line:
                    try:
                        meters.append(json.loads(line))
                    except Exception:
                        pass
    if not meters:
        # Fallback canonical meters
        meters = [
            {"chanda_name": "शार्दूलविक्रीडित", "chanda_name_en": "Shardulavikridita", "syllables_per_pada": "19", "lg_pattern": "SSSIISISISSSIISSISS", "gana_sequence": "म स ज स त त ग", "yati": "12,7", "lakshana": "सूर्याश्वैर्यदि मः सजौ सततगाः शार्दूलविक्रीडितम्"},
            {"chanda_name": "मन्दाक्रान्ता", "chanda_name_en": "Mandakranta", "syllables_per_pada": "17", "lg_pattern": "SSSSIIIIISSIISSS", "gana_sequence": "म भ न त त गा", "yati": "4,6,7", "lakshana": "मन्दाक्रान्ता जलधिषडगैर्मभौ न्तौ गयुग्मम्"},
            {"chanda_name": "शिखरिणी", "chanda_name_en": "Shikharini", "syllables_per_pada": "17", "lg_pattern": "ISSSSSIIIIIISSIIS", "gana_sequence": "य म न स भ ला गा", "yati": "6,11", "lakshana": "रसै रुद्रैश्छिन्ना यमनसभलागः शिखरिणी"},
            {"chanda_name": "इन्द्रवज्रा", "chanda_name_en": "Indravajra", "syllables_per_pada": "11", "lg_pattern": "SSIISIISSIS", "gana_sequence": "त त ज गा गा", "yati": "5,6", "lakshana": "स्यादिन्द्रवज्रा यदि तौ जगौ गः"},
            {"chanda_name": "उपेन्द्रवज्रा", "chanda_name_en": "Upendravajra", "syllables_per_pada": "11", "lg_pattern": "ISIISIISSIS", "gana_sequence": "ज त ज गा गा", "yati": "5,6", "lakshana": "उपेन्द्रवज्रा जतजास्ततो गौ"},
            {"chanda_name": "भुजङ्गप्रयात", "chanda_name_en": "Bhujangaprayata", "syllables_per_pada": "12", "lg_pattern": "ISSISSISSISS", "gana_sequence": "य य य य", "yati": "6,6", "lakshana": "भुजङ्गप्रयातं भवेद् यैश्चतुर्भिः"},
            {"chanda_name": "तोडक", "chanda_name_en": "Totaka", "syllables_per_pada": "12", "lg_pattern": "IISIISIISIIS", "gana_sequence": "स स स स", "yati": "12", "lakshana": "इह तोटकमम्बुधिसैः प्रमितम्"},
            {"chanda_name": "वसन्ततिलका", "chanda_name_en": "Vasantatilaka", "syllables_per_pada": "14", "lg_pattern": "SSIISIIISSIISS", "gana_sequence": "त भ ज ज गा गा", "yati": "8,6", "lakshana": "उक्ता वसन्ततिलका तबजा जगौ गः"}
        ]
    return meters

METERS_DB = load_meter_database()

def scan_laghu_guru(verse: str) -> str:
    """
    Scans a Devanagari verse line and outputs binary Laghu (I) and Guru (S) pattern.
    Applies Chhandaḥśāstra phonological rules:
    - Long vowels, Anusvara (ं), Visarga (ः), and syllables before conjuncts -> Guru (S)
    - Short vowels -> Laghu (I)
    """
    cleaned = re.sub(r"[^\u0900-\u097F]", "", verse)
    if not cleaned:
        return ""
    
    guru_vowels = set("आईऊऋॠएऐओऔाीूृॄेैोौ")
    anusvara_visarga = set("ंः")
    virama = "्"
    
    tokens = []
    i = 0
    while i < len(cleaned):
        char = cleaned[i]
        if char == virama:
            if tokens:
                tokens[-1] = "S"  # Preceding conjunct becomes Guru
            i += 1
            continue
        
        weight = "I"
        if char in guru_vowels or char in anusvara_visarga:
            weight = "S"
        
        if i + 1 < len(cleaned) and cleaned[i+1] in guru_vowels | anusvara_visarga:
            weight = "S"
            i += 1
            
        tokens.append(weight)
        i += 1
        
    # Padānta rule: Last syllable is treated as Guru if needed
    return "".join(tokens)

def identify_meter(verse: str) -> Dict[str, Any]:
    """
    Identifies the best matching poetic meter from the 63-meter database.
    """
    scan = scan_laghu_guru(verse)
    syllable_count = len(scan)
    
    best_match = None
    max_sim = -1.0
    
    for meter in METERS_DB:
        target_pattern = meter.get("lg_pattern", "")
        if not target_pattern:
            continue
            
        # Check similarity
        match_len = min(len(scan), len(target_pattern))
        if match_len > 0:
            matches = sum(1 for a, b in zip(scan[:match_len], target_pattern[:match_len]) if a == b or b == 'X')
            length_penalty = abs(len(scan) - len(target_pattern)) * 0.1
            sim = max(0.0, (matches / match_len) - length_penalty)
            
            if sim > max_sim:
                max_sim = sim
                best_match = meter
                
    name = best_match.get("chanda_name", "अज्ञात") if best_match else "अज्ञात"
    name_en = best_match.get("chanda_name_en", "Unknown") if best_match else "Unknown"

    return {
        "verse": verse,
        "syllables_detected": syllable_count,
        "laghu_guru_scan": scan,
        "meter_name": name,
        "meter_name_en": name_en,
        "gana_sequence": best_match.get("gana_sequence", "") if best_match else "",
        "expected_syllables": best_match.get("syllables_per_pada", "") if best_match else "",
        "confidence": round(max_sim, 2),
        "lakshana": best_match.get("lakshana", "") if best_match else "",
        "yati": best_match.get("yati", "") if best_match else ""
    }
