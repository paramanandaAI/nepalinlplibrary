import random
import re
from typing import List, Dict, Callable
from dataclasses import dataclass


DEVANAGARI_CHARS = [
    'अ', 'आ', 'इ', 'ई', 'उ', 'ऊ', 'ऋ', 'ए', 'ऐ', 'ओ', 'औ',
    'क', 'ख', 'ग', 'घ', 'ङ', 'च', 'छ', 'ज', 'झ', 'ञ',
    'ट', 'ठ', 'ड', 'ढ', 'ण', 'त', 'थ', 'द', 'ध', 'न',
    'प', 'फ', 'ब', 'भ', 'म', 'य', 'र', 'ल', 'व', 'श',
    'ष', 'स', 'ह', 'क्ष', 'त्र', 'ज्ञ', 'श्र'
]

DEVANAGARI_MATRAS = ['ा', 'ि', 'ी', 'ु', 'ू', 'ृ', 'े', 'ै', 'ो', 'ौ', 'ं', 'ः']

DEVANAGARI_AUDIO_SIMILAR: Dict[str, List[str]] = {
    'क': ['ख', 'ग'], 'ख': ['क', 'ग'], 'ग': ['क', 'ख', 'घ'],
    'च': ['छ', 'ज'], 'छ': ['च', 'ज'], 'ज': ['च', 'छ', 'झ'],
    'ट': ['ठ', 'ड'], 'ठ': ['ट', 'ड'], 'ड': ['ट', 'ठ', 'ढ'],
    'त': ['थ', 'द'], 'थ': ['त', 'द'], 'द': ['त', 'थ', 'ध'],
    'प': ['फ', 'ब'], 'फ': ['प', 'ब'], 'ब': ['प', 'फ', 'भ'],
    'श': ['ष', 'स'], 'ष': ['श', 'स'], 'स': ['श', 'ष'],
    'र': ['ड़', 'ढ़'], 'ल': ['ळ'],
    'न': ['ण', 'ञ', 'ङ', 'ं'], 'म': ['ं'],
    'ह': ['ह'], 'य': ['य'], 'व': ['व'],
}


@dataclass
class NoisingConfig:
    char_replace_prob: float = 0.1
    audio_similar_prob: float = 0.05
    word_replace_prob: float = 0.1
    synonym_replace_prob: float = 0.1
    sentence_scramble_prob: float = 0.0


class DevanagariNoiser:
    def __init__(self, config: NoisingConfig = None):
        self.config = config or NoisingConfig()
        self.all_chars = DEVANAGARI_CHARS + DEVANAGARI_MATRAS

    def is_devanagari(self, char: str) -> bool:
        return '\u0900' <= char <= '\u097F'

    def replace_random_char(self, text: str) -> str:
        result = []
        for char in text:
            if self.is_devanagari(char) and random.random() < self.config.char_replace_prob:
                result.append(random.choice(self.all_chars))
            else:
                result.append(char)
        return ''.join(result)

    def replace_audio_similar(self, text: str) -> str:
        result = []
        for char in text:
            if char in DEVANAGARI_AUDIO_SIMILAR and random.random() < self.config.audio_similar_prob:
                result.append(random.choice(DEVANAGARI_AUDIO_SIMILAR[char]))
            else:
                result.append(char)
        return ''.join(result)

    def apply_char_noise(self, text: str) -> str:
        text = self.replace_random_char(text)
        text = self.replace_audio_similar(text)
        return text


class WordNoiser:
    def __init__(self, config: NoisingConfig = None, synonym_dict: Dict[str, List[str]] = None):
        self.config = config or NoisingConfig()
        self.synonym_dict = synonym_dict or {}

    def random_word_replace(self, text: str, vocab: List[str] = None) -> str:
        words = text.split()
        if not words:
            return text
        vocab = vocab or list(set(words))
        result = []
        for word in words:
            if random.random() < self.config.word_replace_prob and vocab:
                result.append(random.choice(vocab))
            else:
                result.append(word)
        return ' '.join(result)

    def synonym_replace(self, text: str) -> str:
        words = text.split()
        result = []
        for word in words:
            clean_word = re.sub(r'[^\w]', '', word)
            if clean_word in self.synonym_dict and random.random() < self.config.synonym_replace_prob:
                synonym = random.choice(self.synonym_dict[clean_word])
                result.append(word.replace(clean_word, synonym))
            else:
                result.append(word)
        return ' '.join(result)


class SentenceNoiser:
    def __init__(self, config: NoisingConfig = None):
        self.config = config or NoisingConfig()

    def scramble_sentences(self, text: str) -> str:
        sentences = re.split(r'(?<=[।.!?])\s+', text.strip())
        if len(sentences) <= 1 or random.random() >= self.config.sentence_scramble_prob:
            return text
        random.shuffle(sentences)
        return ' '.join(sentences)


class CompositeNoiser:
    def __init__(
        self,
        config: NoisingConfig = None,
        synonym_dict: Dict[str, List[str]] = None,
        vocab: List[str] = None
    ):
        self.config = config or NoisingConfig()
        self.devanagari_noiser = DevanagariNoiser(self.config)
        self.word_noiser = WordNoiser(self.config, synonym_dict)
        self.sentence_noiser = SentenceNoiser(self.config)
        self.vocab = vocab or []

    def apply_all(self, text: str) -> str:
        text = self.devanagari_noiser.apply_char_noise(text)
        text = self.word_noiser.random_word_replace(text, self.vocab)
        text = self.word_noiser.synonym_replace(text)
        text = self.sentence_noiser.scramble_sentences(text)
        return text

    def apply_selective(self, text: str, methods: List[str]) -> str:
        method_map = {
            'char_random': self.devanagari_noiser.replace_random_char,
            'char_audio': self.devanagari_noiser.replace_audio_similar,
            'word_random': lambda t: self.word_noiser.random_word_replace(t, self.vocab),
            'word_synonym': self.word_noiser.synonym_replace,
            'sentence_scramble': self.sentence_noiser.scramble_sentences,
        }
        for method in methods:
            if method in method_map:
                text = method_map[method](text)
        return text


def demo():
    config = NoisingConfig(
        char_replace_prob=0.15,
        audio_similar_prob=0.1,
        word_replace_prob=0.1,
        synonym_replace_prob=0.15,
        sentence_scramble_prob=0.3
    )

    synonym_dict = {
        'राम': ['सीता', 'लक्ष्मण', 'भरत'],
        'सीता': ['राम', 'लक्ष्मण'],
        'जाता': ['आता', 'चलता'],
        'घर': ['मकान', 'निवास'],
        'स्कूल': ['विद्यालय', 'पाठशाला'],
        'पढ़ता': ['लिखता', 'सीखता'],
    }

    vocab = ['राम', 'सीता', 'लक्ष्मण', 'घर', 'स्कूल', 'पढ़ता', 'जाता', 'आता', 'मकान', 'विद्यालय']

    noiser = CompositeNoiser(config, synonym_dict, vocab)

    test_text = "राम घर जाता है। सीता स्कूल पढ़ती है। लक्ष्मण भी साथ जाता है।"

    output = []
    output.append(f"Original: {test_text}")
    output.append("\n--- All noise ---")
    output.append(f"Noised:  {noiser.apply_all(test_text)}")
    output.append("\n--- Selective ---")
    output.append(f"Char only: {noiser.apply_selective(test_text, ['char_random', 'char_audio'])}")
    output.append(f"Word only: {noiser.apply_selective(test_text, ['word_random', 'word_synonym'])}")
    output.append(f"Sentence only: {noiser.apply_selective(test_text, ['sentence_scramble'])}")

    output_text = "\n".join(output)
    with open('demo_output.txt', 'w', encoding='utf-8') as f:
        f.write(output_text)
    print("Demo output written to demo_output.txt")


if __name__ == '__main__':
    demo()