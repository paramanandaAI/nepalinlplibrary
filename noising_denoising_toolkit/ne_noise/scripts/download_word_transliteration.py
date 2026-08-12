"""Download the full ~2.4M pair Nepali-Roman transliteration dataset.

Source: Saugatkafley/Nepali-Roman-Transliteration (HuggingFace).
Big data is not vendored into the library; this script fetches it on demand and
writes it where ``ne_noise.translit.lexicon.Lexicon`` expects it.
"""

import argparse
from pathlib import Path

DEFAULT_OUTPUT = Path(__file__).resolve().parent.parent / "translit" / "data" / "nepali_roman_word.csv"
DATASET_NAME = "Saugatkafley/Nepali-Roman-Transliteration"


def download_and_save(output_path: Path = DEFAULT_OUTPUT) -> None:
    try:
        import pandas as pd
        from datasets import load_dataset
    except ImportError as exc:
        raise ImportError(
            "Download requires 'datasets' and 'pandas'. "
            "Install with: pip install \"ne-noise[lexicon]\""
        ) from exc

    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    print(f"Loading HuggingFace dataset: '{DATASET_NAME}'...")
    dataset = load_dataset(DATASET_NAME, split="train")

    print(f"Converting {len(dataset)} rows to DataFrame...")
    df = pd.DataFrame(dataset)

    print(f"Saving CSV: {output_path}")
    df.to_csv(output_path, index=False, encoding="utf-8")
    print(f"Saved {len(df)} rows to {output_path}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Download the Nepali-Roman transliteration dataset.")
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT, help="CSV output path")
    args = parser.parse_args()
    download_and_save(args.output)


if __name__ == "__main__":
    main()
