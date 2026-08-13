"""
NLTK Nepali Toolkit Engine:
Pure Python, zero-dependency implementations of canonical NLTK algorithms
adapted specifically for Devanagari, Nepali morphology, and low-resource Indic NLP.
"""

import math
import re
import unicodedata
from collections import Counter, defaultdict
from typing import List, Dict, Tuple, Optional, Any, Set

# ----------------------------------------------------------------------
# 1. Tokenization & Normalization
# ----------------------------------------------------------------------

def normalize_text(text: str) -> str:
    text = unicodedata.normalize("NFC", text)
    text = re.sub(r"[\u200b\u200e\u200f]", "", text)
    return re.sub(r"\s+", " ", text).strip()

def word_tokenize(text: str) -> List[str]:
    text = normalize_text(text)
    # Split while separating punctuation
    tokens = re.findall(r"[\u0900-\u097F]+|[a-zA-Z0-9]+|[।॥\?\!\.,;:\"\'\(\)\-\—]", text)
    return [t for t in tokens if t.strip()]

def sent_tokenize(text: str) -> List[str]:
    text = normalize_text(text)
    raw = re.split(r"([।॥\?\!]+)", text)
    sents = []
    curr = ""
    for piece in raw:
        if not piece:
            continue
        if re.match(r"^[।॥\?\!]+$", piece):
            curr += piece
            sents.append(curr.strip())
            curr = ""
        else:
            curr += piece
    if curr.strip():
        sents.append(curr.strip())
    return [s for s in sents if len(s) > 1]

# ----------------------------------------------------------------------
# 2. N-gram Collocations & Association Measures (PMI)
# ----------------------------------------------------------------------

class CollocationFinder:
    """Finds significant multi-word expressions and collocations using PMI."""
    def __init__(self, words: List[str]):
        self.words = words
        self.unigrams = Counter(words)
        self.bigrams = Counter(zip(words[:-1], words[1:]))
        self.trigrams = Counter(zip(words[:-2], words[1:-1], words[2:]))
        self.total_words = len(words)
        self.total_bigrams = max(1, len(words) - 1)

    def pmi_bigrams(self, min_freq: int = 2, top_k: int = 10) -> List[Tuple[Tuple[str, str], float]]:
        scores = []
        for (w1, w2), count in self.bigrams.items():
            if count < min_freq:
                continue
            p_w1 = self.unigrams[w1] / self.total_words
            p_w2 = self.unigrams[w2] / self.total_words
            p_w1_w2 = count / self.total_bigrams
            pmi = math.log2(p_w1_w2 / (p_w1 * p_w2 + 1e-12))
            scores.append(((w1, w2), round(pmi, 4)))
        scores.sort(key=lambda x: x[1], reverse=True)
        return scores[:top_k]

# ----------------------------------------------------------------------
# 3. N-gram Language Modeling with Laplace / Lidstone Smoothing
# ----------------------------------------------------------------------

class NgramLanguageModel:
    """N-gram language model supporting Unigram, Bigram, and Trigram MLE/Laplace scoring."""
    def __init__(self, n: int = 2, smoothing: float = 1.0):
        self.n = n
        self.smoothing = smoothing
        self.ngram_counts = defaultdict(Counter)
        self.context_counts = Counter()
        self.vocab: Set[str] = set()

    def train(self, corpus: List[List[str]]):
        for sent in corpus:
            padded = ["<s>"] * (self.n - 1) + sent + ["</s>"]
            self.vocab.update(sent)
            for i in range(len(padded) - self.n + 1):
                ctx = tuple(padded[i:i + self.n - 1])
                target = padded[i + self.n - 1]
                self.ngram_counts[ctx][target] += 1
                self.context_counts[ctx] += 1

    def score(self, word: str, context: Tuple[str, ...]) -> float:
        ctx = tuple(context[-(self.n - 1):]) if self.n > 1 else ()
        count = self.ngram_counts[ctx][word]
        total = self.context_counts[ctx]
        vocab_size = max(1, len(self.vocab))
        # Laplace smoothing: (count + alpha) / (total + alpha * V)
        return (count + self.smoothing) / (total + self.smoothing * vocab_size)

    def perplexity(self, sent: List[str]) -> float:
        padded = ["<s>"] * (self.n - 1) + sent + ["</s>"]
        log_prob_sum = 0.0
        n_predictions = len(sent) + 1
        for i in range(len(padded) - self.n + 1):
            ctx = tuple(padded[i:i + self.n - 1])
            target = padded[i + self.n - 1]
            p = self.score(target, ctx)
            log_prob_sum += math.log2(p)
        return round(2 ** (-log_prob_sum / max(1, n_predictions)), 4)

# ----------------------------------------------------------------------
# 4. Sequential POS Tagging (Unigram + Backoff)
# ----------------------------------------------------------------------

class SequentialPOSTagger:
    """Statistical unigram tagger with rule-based morphological backoff."""
    def __init__(self, default_tag: str = "NN"):
        self.default_tag = default_tag
        self.unigram_model: Dict[str, str] = {}

    def train(self, tagged_corpus: List[List[Tuple[str, str]]]):
        word_tag_freq = defaultdict(Counter)
        for sent in tagged_corpus:
            for word, tag in sent:
                word_tag_freq[word][tag] += 1
        for word, freqs in word_tag_freq.items():
            self.unigram_model[word] = freqs.most_common(1)[0][0]

    def tag_word(self, word: str) -> str:
        if word in self.unigram_model:
            return self.unigram_model[word]
        # Morphological heuristics
        if word.endswith(("छ", "थियो", "गर्यो", "भयो", "हुन्", "गर्नु")):
            return "VF"
        if word.endswith(("ले", "लाई", "मा", "को", "बाट", "सँग")):
            return "PPO"
        if word.endswith(("राम्रो", "नयाँ", "ठूलो", "सानो")):
            return "JJ"
        if any(char.isdigit() or '\u0966' <= char <= '\u096f' for char in word):
            return "CD"
        return self.default_tag

    def tag(self, tokens: List[str]) -> List[Tuple[str, str]]:
        return [(t, self.tag_word(t)) for t in tokens]

# ----------------------------------------------------------------------
# 5. Regexp Chunker (Noun & Verb Phrase Chunking)
# ----------------------------------------------------------------------

class RegexpChunker:
    """Chunks tagged tokens into NP (नामपद समूह) and VP (क्रियापद समूह)."""
    @staticmethod
    def chunk(tagged_tokens: List[Tuple[str, str]]) -> List[Dict[str, Any]]:
        chunks = []
        i = 0
        n = len(tagged_tokens)
        while i < n:
            word, tag = tagged_tokens[i]
            # Match Noun Phrase: (JJ)* + (NN|NNP)+ + (PPO)?
            if tag in ("NN", "NNP", "JJ", "PRP"):
                np_words = [word]
                j = i + 1
                while j < n and tagged_tokens[j][1] in ("NN", "NNP", "PPO"):
                    np_words.append(tagged_tokens[j][0])
                    j += 1
                chunks.append({"type": "NP", "words": np_words, "text": " ".join(np_words)})
                i = j
            elif tag in ("VF", "VNF", "VAUX"):
                vp_words = [word]
                j = i + 1
                while j < n and tagged_tokens[j][1] in ("VF", "VNF", "VAUX"):
                    vp_words.append(tagged_tokens[j][0])
                    j += 1
                chunks.append({"type": "VP", "words": vp_words, "text": " ".join(vp_words)})
                i = j
            else:
                chunks.append({"type": "OTHER", "words": [word], "text": word})
                i += 1
        return chunks

# ----------------------------------------------------------------------
# 6. Evaluation Metrics: BLEU, chrF, Levenshtein Distance
# ----------------------------------------------------------------------

def edit_distance(s1: str, s2: str) -> int:
    """Calculates Levenshtein edit distance between two strings."""
    m, n = len(s1), len(s2)
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    for i in range(m + 1):
        dp[i][0] = i
    for j in range(n + 1):
        dp[0][j] = j
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            cost = 0 if s1[i - 1] == s2[j - 1] else 1
            dp[i][j] = min(dp[i - 1][j] + 1, dp[i][j - 1] + 1, dp[i - 1][j - 1] + cost)
    return dp[m][n]

def sentence_bleu(hypothesis: List[str], reference: List[str], max_n: int = 4) -> float:
    """Calculates sentence-level BLEU score with brevity penalty."""
    if not hypothesis or not reference:
        return 0.0
    precisions = []
    for n in range(1, max_n + 1):
        hyp_ngrams = Counter(zip(*[hypothesis[i:] for i in range(n)]))
        ref_ngrams = Counter(zip(*[reference[i:] for i in range(n)]))
        clipped = sum(min(count, ref_ngrams[ng]) for ng, count in hyp_ngrams.items())
        total = max(1, len(hypothesis) - n + 1)
        precisions.append((clipped + 1e-4) / (total + 1e-4))

    geo_mean = math.exp(sum(math.log(p) for p in precisions) / max_n)
    hyp_len = len(hypothesis)
    ref_len = len(reference)
    bp = 1.0 if hyp_len > ref_len else math.exp(1 - ref_len / max(1, hyp_len))
    return round(bp * geo_mean * 100, 2)

def sentence_chrf(hypothesis: str, reference: str, n: int = 6, beta: float = 2.0) -> float:
    """Calculates character n-gram F-score (chrF)."""
    def get_char_ngrams(s: str, n_val: int):
        s_clean = s.replace(" ", "")
        return Counter([s_clean[i:i + n_val] for i in range(len(s_clean) - n_val + 1)])

    total_f = 0.0
    for order in range(1, n + 1):
        hyp_ng = get_char_ngrams(hypothesis, order)
        ref_ng = get_char_ngrams(reference, order)
        overlap = sum(min(count, ref_ng[ng]) for ng, count in hyp_ng.items())
        total_hyp = sum(hyp_ng.values())
        total_ref = sum(ref_ng.values())
        
        prec = (overlap / total_hyp) if total_hyp > 0 else 0.0
        rec = (overlap / total_ref) if total_ref > 0 else 0.0
        if prec + rec > 0:
            f_score = (1 + beta**2) * (prec * rec) / ((beta**2 * prec) + rec)
        else:
            f_score = 0.0
        total_f += f_score
    return round((total_f / n) * 100, 2)

# ----------------------------------------------------------------------
# 7. Word Sense Disambiguation: Simplified Lesk Algorithm
# ----------------------------------------------------------------------

def nepali_lesk(word: str, sentence: str, synset_definitions: Dict[str, Dict[str, Any]]) -> str:
    """Disambiguates word sense by maximizing word overlap with synset gloss/examples."""
    context_words = set(word_tokenize(sentence)) - {word}
    best_sense = ""
    max_overlap = -1

    for sense_id, data in synset_definitions.items():
        definition_text = data.get("gloss", "") + " " + " ".join(data.get("examples", []))
        signature = set(word_tokenize(definition_text))
        overlap = len(context_words.intersection(signature))
        if overlap > max_overlap:
            max_overlap = overlap
            best_sense = sense_id

    return best_sense
