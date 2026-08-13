"""
Command-Line Interface (`nepalinlplibrary.dataloader.cli`)
Provides CLI commands to inspect, filter, validate, and export dataset specs.
"""

import argparse
import sys
from .loader import DatasetLoader
from .catalog import CatalogManager

def main():
    parser = argparse.ArgumentParser(description="Nepali NLP Library Dataset Loader CLI")
    subparsers = parser.add_subparsers(dest="command", help="Sub-commands")

    # List command
    list_parser = subparsers.add_parser("list", help="List datasets")
    list_parser.add_argument("--root", type=str, default=None, help="Root dataset directory")
    list_parser.add_argument("--status", type=str, default=None, help="Filter by status ('verified' or 'todo')")
    list_parser.add_argument("--task", type=str, default=None, help="Filter by task string")
    list_parser.add_argument("--modality", type=str, default=None, help="Filter by modality")
    list_parser.add_argument("--verified-only", action="store_true", help="Only show verified datasets")

    # Info command
    info_parser = subparsers.add_parser("info", help="Show dataset details")
    info_parser.add_argument("dataset_id", type=str, help="Dataset ID")
    info_parser.add_argument("--root", type=str, default=None, help="Root dataset directory")

    # Catalog command
    cat_parser = subparsers.add_parser("catalog", help="Export catalog.jsonl")
    cat_parser.add_argument("output_path", type=str, help="Output file path for catalog.jsonl")
    cat_parser.add_argument("--root", type=str, default=None, help="Root dataset directory")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return

    loader = DatasetLoader(root_dir=args.root, auto_clone=False)

    if args.command == "list":
        results = loader.list_datasets(
            status=args.status,
            task=args.task,
            modality=args.modality,
            verified_only=args.verified_only
        )
        print(f"\n--- Discovered Datasets ({len(results)} matches) ---")
        print(f"{'ID':<60} | {'STATUS':<10} | {'MODALITY':<12} | {'MAX ROWS':<10}")
        print("-" * 100)
        for spec in results:
            print(f"{spec.id:<60} | {spec.status:<10} | {spec.modality:<12} | {spec.max_rows:<10}")

    elif args.command == "info":
        spec = loader.get_spec(args.dataset_id)
        if not spec:
            print(f"Error: Dataset '{args.dataset_id}' not found.")
            sys.exit(1)
        print(f"\nDataset ID: {spec.id}")
        print(f"Name: {spec.name}")
        print(f"Status: {spec.status}")
        print(f"Task: {spec.task}")
        print(f"Modality: {spec.modality}")
        print(f"Max Rows: {spec.max_rows}")
        print(f"Download Default Rows: {spec.download_rows_default}")
        print(f"Languages: {spec.languages}")
        print(f"Source URL: {spec.source_url}")
        print(f"Export Templates: {list(spec.export_templates.keys())}")

    elif args.command == "catalog":
        cat_mgr = CatalogManager(loader)
        count = cat_mgr.export_catalog_jsonl(args.output_path)
        print(f"Exported catalog for {count} datasets to {args.output_path}")

if __name__ == "__main__":
    main()
