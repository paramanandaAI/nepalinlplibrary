"""
Catalog Management Module (`nepalinlplibrary.dataloader.catalog`)
Generates catalog.jsonl index from dataset specifications.
"""

import json
import os
from typing import Dict, Any, List
from .loader import DatasetLoader
from .spec import DatasetSpec

class CatalogManager:
    def __init__(self, loader: DatasetLoader):
        self.loader = loader

    def generate_catalog_dict(self) -> List[Dict[str, Any]]:
        """Compiles catalog entries from all loaded specs."""
        entries = []
        for spec in self.loader.specs.values():
            entries.append({
                "id": spec.id,
                "name": spec.name,
                "task": spec.task,
                "status": spec.status,
                "quality_tier": spec.quality_tier,
                "modality": spec.modality,
                "max_rows": spec.max_rows,
                "languages": spec.languages,
                "source_url": spec.source_url,
                "filepath": spec.filepath
            })
        return entries

    def export_catalog_jsonl(self, output_path: str):
        """Exports dataset catalog to a JSONL file."""
        entries = self.generate_catalog_dict()
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        with open(output_path, "w", encoding="utf-8") as f:
            for entry in entries:
                f.write(json.dumps(entry, ensure_ascii=False) + "\n")
        return len(entries)
