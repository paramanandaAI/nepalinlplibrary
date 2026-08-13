"""
Devanagari Autocomplete Engine (`nepalinlplibrary.library.autocomplete.engine`)
Trie-based autocomplete with online frequency learning.
"""

from typing import List, Tuple, Dict, Optional

class TrieNode:
    def __init__(self):
        self.children: Dict[str, "TrieNode"] = {}
        self.frequency: int = 0
        self.is_word: bool = False

class AutocompleteEngine:
    """Trie-backed Devanagari autocompleter supporting frequency learning."""

    def __init__(self):
        self.root = TrieNode()

    def insert(self, word: str, frequency: int = 1):
        """Insert a word with initial frequency."""
        word = word.strip()
        if not word:
            return
        node = self.root
        for ch in word:
            if ch not in node.children:
                node.children[ch] = TrieNode()
            node = node.children[ch]
        node.is_word = True
        node.frequency += frequency

    def learn_frequency(self, word: str, count: int = 1):
        """Increment frequency count for an existing or new word."""
        self.insert(word, frequency=count)

    def get_top_k(self, prefix: str, k: int = 5) -> List[Tuple[str, int]]:
        """Return top-K word autocompletions for a given prefix."""
        prefix = prefix.strip()
        if not prefix:
            return []

        node = self.root
        for ch in prefix:
            if ch not in node.children:
                return []
            node = node.children[ch]

        # DFS to collect all words under prefix
        results: List[Tuple[str, int]] = []
        def dfs(curr_node: TrieNode, curr_str: str):
            if curr_node.is_word:
                results.append((curr_str, curr_node.frequency))
            for ch, child in curr_node.children.items():
                dfs(child, curr_str + ch)

        dfs(node, prefix)
        results.sort(key=lambda x: x[1], reverse=True)
        return results[:k]
