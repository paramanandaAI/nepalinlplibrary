"""
CLI script to download mrlbenchmarks/global-piqa-nonparallel (npi_deva)
and save to lemmatization/sentence_data/global_piqa/test_piqa.jsonl.
"""

import sys
import argparse
from pathlib import Path

# Add project root to path
ROOT_DIR = Path(__file__).resolve().parent.parent.parent.parent
sys.path.insert(0, str(ROOT_DIR))

from lemmatization.src.piqa_processor import GlobalPIQAProcessor


def main():
    parser = argparse.ArgumentParser(
        description="Download Global-PIQA Nepali dataset (mrlbenchmarks/global-piqa-nonparallel)."
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=100,
        help="Number of records to process (default: 100)."
    )
    args = parser.parse_args()

    yaml_path = Path(__file__).resolve().parent / "global_piqa_ne.yaml"
    processor = GlobalPIQAProcessor(yaml_path=yaml_path)
    print(f"Downloading Global-PIQA Nepali (npi_deva) based on {processor.yaml_path}...")
    saved_count = processor.process_and_save(limit=args.limit)

    print(f"Successfully saved {saved_count} records to {processor.output_file}")


if __name__ == "__main__":
    main()
