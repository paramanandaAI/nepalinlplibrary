"""
CLI script to download HuggingFace Wikipedia dataset (500 rows)
and save to lemmatization/sentence_data/wikipedia/train.jsonl.
"""

import sys
import argparse
from pathlib import Path

# Add project root to path
ROOT_DIR = Path(__file__).resolve().parent.parent.parent.parent
sys.path.insert(0, str(ROOT_DIR))

from lemmatization.src.hf_downloader import WikipediaHFDownloader


def main():
    parser = argparse.ArgumentParser(
        description="Download Hugging Face Wikipedia dataset (500 rows)."
    )
    parser.add_argument(
        "--yaml",
        type=str,
        default=None,
        help="Path to YAML source contract file."
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=500,
        help="Number of articles to download (default: 500)."
    )
    args = parser.parse_args()

    yaml_path = Path(args.yaml) if args.yaml else (Path(__file__).resolve().parent / "wikipedia_ne.yaml")
    downloader = WikipediaHFDownloader(yaml_path=yaml_path)

    print(f"Downloading {args.limit} Wikipedia records based on {downloader.yaml_path}...")
    saved_count = downloader.download_and_save(limit=args.limit)

    print(f"Successfully saved {saved_count} records to {downloader.output_file}")


if __name__ == "__main__":
    main()
