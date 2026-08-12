"""
End-to-end demo for ne_noise.

The in-folder data path for testing hypotheses. Runs and writes (to demo/output/):
  1. text normalization
  2. transliteration tiers (word -> character -> model) on the same words
  3. every noising operator on the demo sentences
  4. denoising pairs + a corruption report

Usage:
    python -m ne_noise.demo
    python -m ne_noise demo          # via the package CLI
"""

import json
from pathlib import Path

try:
    from ..denoise.pairs import make_pairs, write_jsonl
    from ..noise.engine import apply_noising, list_noise_ops
    from ..text.normalize import normalize_nepali_text
    from ..text.scripts import devanagari_ratio
    from ..translit.engine import TransliterationEngine
except ImportError:
    from ne_noise.denoise.pairs import make_pairs, write_jsonl
    from ne_noise.noise.engine import apply_noising, list_noise_ops
    from ne_noise.text.normalize import normalize_nepali_text
    from ne_noise.text.scripts import devanagari_ratio
    from ne_noise.translit.engine import TransliterationEngine

HERE = Path(__file__).resolve().parent
DATA_PATH = HERE / "data" / "sample_nepali.jsonl"
OUTPUT_DIR = HERE / "output"

_DEMO_WORDS = ["काठमाडौँ", "नेपाल", "नमस्ते", "धन्यवाद", "जीवन", "विद्यार्थी"]
_DEMO_SENTENCE = "नेपालको राजधानी काठमाडौँ हो।"


def load_demo_sentences(path: Path = DATA_PATH):
    sentences = []
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                sentences.append(json.loads(line))
    return sentences


def section(title: str) -> None:
    print("\n" + "=" * 68)
    print(title)
    print("=" * 68)


def run_demo(engine: TransliterationEngine = None, out_dir: Path = OUTPUT_DIR) -> None:
    engine = engine or TransliterationEngine()
    out_dir.mkdir(parents=True, exist_ok=True)

    section("1. Nepali Text Normalization")
    raw = "नेपालको   राजधानी\tकाठमाडौँ।\u200b"
    print(f"  raw     : {raw!r}")
    print(f"  clean   : {normalize_nepali_text(raw)!r}")

    section("2. Transliteration Tiers (word -> character -> model)")
    print("  lexicon tier: O(1) dictionary lookup; falls back to character rules.")
    print("  character   : rule-based (matra/conjunct/halant aware).")
    print("  model       : optional HF wrapper, lazy-loaded, not used here.\n")
    for w in _DEMO_WORDS:
        lex = engine.lexicon.deva_to_roman(w) if engine.lexicon and engine.lexicon.has_deva(w) else "-"
        chars = engine.deva_to_roman(w)
        print(f"  {w:<12} lexicon={lex:<14} rules={chars}")

    section("3. Noising Operators (seeded)")
    ops = list_noise_ops()
    for op in ops:
        noised = apply_noising(_DEMO_SENTENCE, op, seed=7)
        deva_ratio = devanagari_ratio(noised)
        print(f"  {op:<28} ratio={deva_ratio:.2f}  {noised}")

    section("4. Denoising Pairs")
    sentences = load_demo_sentences()
    texts = [s["text"] for s in sentences]
    pairs = make_pairs(texts, k=2, seed=11)
    pairs_path = out_dir / "denoise_pairs.jsonl"
    write_jsonl(pairs, pairs_path)
    changed = sum(1 for p in pairs if p.noised != p.clean)
    print(f"  built {len(pairs)} pairs from {len(texts)} sentences; {changed} noised.")
    for p in pairs[:3]:
        print(f"    clean : {p.clean}")
        print(f"    noised: {p.noised}  ops={p.ops}")
    print(f"  wrote -> {pairs_path}")

    section("Hypothesis-Style Check")
    a = devanagari_ratio(apply_noising(_DEMO_SENTENCE, "keyboard_typo", seed=1))
    b = devanagari_ratio(apply_noising(_DEMO_SENTENCE, "char_substitution", seed=1))
    print(f"  devanagari_ratio(keyboard_typo)        = {a:.2f}")
    print(f"  devanagari_ratio(char_substitution)    = {b:.2f}")
    print(f"  -> keyboard noise preserves the script better by {a - b:+.2f} on this sample.")


def main() -> None:
    run_demo()
    print("\nDemo complete. See ne_noise/demo/output/ for artifacts.")


if __name__ == "__main__":
    main()
