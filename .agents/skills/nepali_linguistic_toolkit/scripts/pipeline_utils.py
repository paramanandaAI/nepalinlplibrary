"""
Pipeline Utilities & Linguistic Processors for Nepali NLP.
Provides sentence segmentation, clitic tokenization, rule-based matching,
PII anonymization, negation detection, quote extraction, and visualizers.
"""

import re
import unicodedata
from typing import List, Dict, Any, Tuple

SENTENCE_DELIMITERS = re.compile(r"([।॥\?\!]+|\n+)")
ABBREVIATIONS = {"डा.", "प्रा.", "नं.", "ई.", "वि.सं.", "श्री", "कि.मी."}
CLITIC_SUFFIXES = ["मा", "ले", "लाई", "को", "का", "की", "बाट", "देखि", "सँग", "हरू", "हरु"]

DEVANAGARI_DIGITS = {
    '०': 0, '१': 1, '२': 2, '३': 3, '४': 4,
    '५': 5, '६': 6, '७': 7, '८': 8, '९': 9
}

NEGATIVE_VERB_SUFFIXES = ["दैन", "दिन", "दैनन्", "दिएन", "भएन", "छैन", "छैनन्", "हुन्न", "हुँदैन", "गर्दैन"]

def normalize_text(text: str) -> str:
    """Canonical NFC Unicode normalization and whitespace cleanup."""
    text = unicodedata.normalize("NFC", text)
    text = re.sub(r"[\u200b\u200e\u200f]", "", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text

def segment_sentences(text: str) -> List[str]:
    """Splits Nepali text into sentences while respecting abbreviations."""
    text = normalize_text(text)
    raw_splits = SENTENCE_DELIMITERS.split(text)
    sentences = []
    
    current = ""
    for piece in raw_splits:
        if not piece:
            continue
        if SENTENCE_DELIMITERS.match(piece):
            current += piece
            sentences.append(current.strip())
            current = ""
        else:
            current += piece
            
    if current.strip():
        sentences.append(current.strip())
        
    return [s for s in sentences if len(s) > 1]

def tokenize_words(sentence: str, split_clitics: bool = False) -> List[str]:
    """Tokenizes words, optionally decomposing case-marker clitics."""
    sentence = normalize_text(sentence)
    tokens = sentence.split()
    if not split_clitics:
        return tokens
        
    result = []
    for t in tokens:
        matched = False
        for clitic in sorted(CLITIC_SUFFIXES, key=len, reverse=True):
            if t.endswith(clitic) and len(t) > len(clitic) + 1:
                result.append(t[:-len(clitic)])
                result.append("-" + clitic)
                matched = True
                break
        if not matched:
            result.append(t)
    return result

def lemmatize_word(word: str) -> str:
    """Rule-based stemmer removing common inflectional clitics and suffixes."""
    word = normalize_text(word)
    for clitic in sorted(CLITIC_SUFFIXES, key=len, reverse=True):
        if word.endswith(clitic) and len(word) > len(clitic) + 1:
            return word[:-len(clitic)]
    return word

def extract_named_patterns(text: str) -> Dict[str, List[str]]:
    """Extracts dates, currency amounts, and phone/ID entities via regex matching."""
    text = normalize_text(text)
    dates = re.findall(r"(?:[०-९\d]{4})\s*(?:बैशाख|जेठ|असार|साउन|भदौ|असोज|कार्तिक|मंसिर|पुष|माघ|फागुन|चैत)\s*(?:[०-९\d]{1,2})?", text)
    currency = re.findall(r"(?:रु\.|नेरू\s*)?[०-९\d,]+(?:\.[०-९\d]+)?\s*(?:हजार|लाख|करोड|अरब)?", text)
    
    return {
        "dates": [d.strip() for d in dates if d.strip()],
        "currency": [c.strip() for c in currency if len(c.strip()) > 1 and any(char.isdigit() or '\u0966' <= char <= '\u096f' for char in c)]
    }

def anonymize_pii(text: str) -> str:
    """Redacts Nepali mobile numbers, citizenship IDs, and email addresses."""
    # Redact Nepal phone (+977-98xxxxxxxx, 98xxxxxxxx, 97xxxxxxxx)
    text = re.sub(r"(?:\+977[-\s]?)?(?:98|97)[0-9०-९]{8}", "[PHONE_REDACTED]", text)
    # Redact email
    text = re.sub(r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+", "[EMAIL_REDACTED]", text)
    # Redact Citizenship format: xx-xx-xx-xxxxx or xx/xxxxx
    text = re.sub(r"\b[0-9०-९]{2}-[0-9०-९]{2}-[0-9०-९]{2}-[0-9०-९]{5}\b", "[CITIZENSHIP_REDACTED]", text)
    return text

def detect_negation(sentence: str) -> bool:
    """Detects whether a Nepali clause or sentence carries a negative polarity."""
    sentence = normalize_text(sentence)
    # Strip punctuation
    clean_text = re.sub(r"[।॥\?\!\.,\-\"\'“”]", "", sentence)
    tokens = clean_text.split()
    for t in tokens:
        for neg in ["एनन्", "एन", "दैन", "दिन", "दैनन्", "दिएन", "भएन", "छैन", "छैनन्", "हुन्न", "हुँदैन", "गर्दैन", "नगर्नु"]:
            if t.endswith(neg) or t == neg:
                return True
    return False

def extract_quotes(text: str) -> List[Dict[str, str]]:
    """Extracts direct quotes in inverted commas and attributions."""
    text = normalize_text(text)
    matches = re.finditer(r'["“]([^"”]+)["”]\s*(?:भन्दै|भनेर|भनी)?\s*([^\s।]+(?:\s+[^\s।]+)?\s*(?:बताए|भने|उल्लेख गरे))?', text)
    quotes = []
    for m in matches:
        quote_text = m.group(1).strip()
        speaker = m.group(2).strip() if m.group(2) else "अज्ञात"
        quotes.append({"quote": quote_text, "speaker": speaker})
    return quotes

def parse_devanagari_number(num_str: str) -> int:
    """Parses a Devanagari digit string into an integer."""
    res = ""
    for ch in num_str:
        if ch in DEVANAGARI_DIGITS:
            res += str(DEVANAGARI_DIGITS[ch])
        elif ch.isdigit():
            res += ch
    return int(res) if res else 0

def render_token_visualizer(tokens: List[str], labels: List[str]) -> str:
    """Renders text-based visualizer for token labels (e.g. POS or NER)."""
    header = " | ".join([f"{t:^12}" for t in tokens])
    divider = "-+-".join(["-" * 12 for _ in tokens])
    tags = " | ".join([f"{l:^12}" for l in labels])
    return f"{header}\n{divider}\n{tags}"
