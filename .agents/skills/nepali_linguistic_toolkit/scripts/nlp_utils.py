"""
Text Classifier & Autocomplete Modules for Nepali NLP.

Citations:
- Bojanowski et al. (2017): Enriching Word Vectors with Subword Information (fastText).
- Joulin et al. (2016): Bag of Tricks for Efficient Text Classification (EACL).
"""

import heapq
from typing import Dict, Any, List, Optional, Tuple

POSITIVE_WORDS = {"राम्रो", "उत्कृष्ट", "खुसी", "जित", "प्रगति", "सफल", "उत्तम", "शुद्ध", "शान्ति"}
NEGATIVE_WORDS = {"खराब", "दुख", "हार", "समस्या", "नराम्रो", "भ्रष्टाचार", "पीडा", "अवरोध", "हानि"}

class TextClassifier:
    """Text Classification interface for Nepali sentiment and categorical polarity."""
    
    def __init__(self, labels: Optional[List[str]] = None):
        self.labels = labels or ["positive", "neutral", "negative"]

    def predict(self, text: str) -> Dict[str, Any]:
        """Predicts class label and confidence score for input Nepali text."""
        words = set(text.lower().split())
        pos_score = len(words.intersection(POSITIVE_WORDS))
        neg_score = len(words.intersection(NEGATIVE_WORDS))
        
        if pos_score > neg_score:
            label = "positive"
            confidence = min(0.5 + (pos_score * 0.15), 0.95)
        elif neg_score > pos_score:
            label = "negative"
            confidence = min(0.5 + (neg_score * 0.15), 0.95)
        else:
            label = "neutral"
            confidence = 0.60
            
        return {
            "text": text,
            "prediction": label,
            "confidence": round(confidence, 4),
            "scores": {
                "positive": round(pos_score / max(pos_score + neg_score + 1, 1), 2),
                "negative": round(neg_score / max(pos_score + neg_score + 1, 1), 2),
                "neutral": 0.5 if pos_score == neg_score else 0.1
            }
        }


class TrieNode:
    def __init__(self):
        self.children: Dict[str, TrieNode] = {}
        self.is_end_of_word: bool = False
        self.frequency: int = 0

class AutocompleteEngine:
    """Trie-based Autocomplete Engine with Frequency Learning for Devanagari."""
    
    def __init__(self):
        self.root = TrieNode()

    def insert(self, word: str, frequency: int = 1):
        node = self.root
        for char in word:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
        node.is_end_of_word = True
        node.frequency += frequency

    def _dfs_search(self, node: TrieNode, prefix: str, heap: List[Tuple[int, str]], k: int):
        if node.is_end_of_word:
            if len(heap) < k:
                heapq.heappush(heap, (node.frequency, prefix))
            elif node.frequency > heap[0][0]:
                heapq.heappop(heap)
                heapq.heappush(heap, (node.frequency, prefix))

        for char, child_node in node.children.items():
            self._dfs_search(child_node, prefix + char, heap, k)

    def get_top_k(self, prefix: str, k: int = 5) -> List[Tuple[str, int]]:
        node = self.root
        for char in prefix:
            if char not in node.children:
                return []
            node = node.children[char]

        heap: List[Tuple[int, str]] = []
        self._dfs_search(node, prefix, heap, k)
        return [(word, freq) for freq, word in sorted(heap, key=lambda x: (-x[0], x[1]))]
