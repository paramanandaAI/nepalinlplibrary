"""
Nepali & Sanskrit Classical Poetic Meter Classifier (`nepalinlplibrary.library.chhanda.meter`)
"""

from typing import Dict, Any, Optional
from .syllable import scan_line

# Classical Meter Definitions (Name, Syllable Count, Target Pattern)
KNOWN_METERS = [
    {"name": "शार्दूलविक्रीडित", "syllables": 19, "pattern": "GGGLLGLGLLLGLLGLGG"},
    {"name": "भुजङ्गप्रयात", "syllables": 12, "pattern": "LGLLGLLGLLGL"},
    {"name": "तोटक", "syllables": 12, "pattern": "LLGLLGLLGLLG"},
    {"name": "इन्द्रवज्रा", "syllables": 11, "pattern": "GGLGGLGLLGG"},
    {"name": "अनुष्टुप्", "syllables": 8, "pattern": "LLLLGLGL"},
]

def analyze_meter(verse_line: str) -> Dict[str, Any]:
    """
    Analyzes a line of Nepali poetry and identifies the best matching meter.
    """
    syllables, scan = scan_line(verse_line)
    count = len(syllables)
    
    best_match: Optional[Dict[str, Any]] = None
    highest_sim = 0.0
    
    for meter in KNOWN_METERS:
        m_name = meter["name"]
        m_syl = meter["syllables"]
        m_pat = meter["pattern"]
        
        # Calculate similarity ratio
        if count == m_syl:
            matches = sum(1 for a, b in zip(scan, m_pat) if a == b)
            sim = matches / len(m_pat)
            if sim > highest_sim:
                highest_sim = sim
                best_match = {"name": m_name, "similarity": round(sim, 2), "expected_syllables": m_syl}
                
    return {
        "syllables": syllables,
        "syllable_count": count,
        "scan_pattern": scan,
        "best_match": best_match
    }
