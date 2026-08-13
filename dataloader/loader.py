"""
Dataset Loader Module (`nepalinlplibrary.dataloader.loader`)
Discovers, loads, and manages dataset contracts and records across categorized trees.
"""

import os
import subprocess
from typing import List, Dict, Any, Optional
from .spec import DatasetSpec
from nepalinlplibrary.config import _config


CANDIDATE_DATA_ROOTS = [
    _config.data_path,
    os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "data", "datasets")),
    os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "data")),
    os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "data", "awesome_data", "Nepali_data")),
]
CANDIDATE_DATA_ROOTS = [c for c in CANDIDATE_DATA_ROOTS if c is not None]
DEFAULT_DATA_ROOT = CANDIDATE_DATA_ROOTS[0] if CANDIDATE_DATA_ROOTS else os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "data", "datasets"))
REMOTE_REPO_URL = "https://github.com/paramanandanlp/data.git"

class DatasetLoader:
    def __init__(self, root_dir: Optional[str] = None, auto_clone: bool = False):
        if root_dir:
            self.root_dir = root_dir
        else:
            self.root_dir = DEFAULT_DATA_ROOT
            for candidate in CANDIDATE_DATA_ROOTS:
                if os.path.exists(candidate):
                    self.root_dir = candidate
                    break
        if auto_clone and not os.path.exists(self.root_dir):
            self.ensure_data_repository()

            
        self.specs: Dict[str, DatasetSpec] = {}
        self.discover_specs()

    def ensure_data_repository(self):
        """Clones or pulls the data repository if missing locally."""
        parent_dir = os.path.dirname(self.root_dir)
        os.makedirs(parent_dir, exist_ok=True)
        if not os.path.exists(self.root_dir):
            print(f"Data directory missing. Attempting to clone from {REMOTE_REPO_URL}...")
            try:
                subprocess.run(
                    ["git", "clone", REMOTE_REPO_URL, self.root_dir],
                    check=True,
                    capture_output=True
                )
            except (subprocess.SubprocessError, FileNotFoundError) as e:
                print(f"Warning: Could not clone data repository ({e}). Using local spec discovery.")

    def discover_specs(self) -> Dict[str, DatasetSpec]:
        """Scans the root directory recursively for .yaml dataset specifications."""
        self.specs = {}
        if not os.path.exists(self.root_dir):
            return self.specs

        for dirpath, _, filenames in os.walk(self.root_dir):
            for fname in filenames:
                if fname.endswith(".yaml") or fname.endswith(".yml"):
                    full_path = os.path.join(dirpath, fname)
                    try:
                        spec = DatasetSpec.from_yaml_file(full_path)
                        self.specs[spec.id] = spec
                    except Exception as e:
                        print(f"Skipping invalid YAML {full_path}: {e}")
        return self.specs

    def list_datasets(
        self,
        status: Optional[str] = None,
        task: Optional[str] = None,
        modality: Optional[str] = None,
        verified_only: bool = False
    ) -> List[DatasetSpec]:
        """Filters discovered datasets by status, task, modality, or verification level."""
        results = []
        for spec in self.specs.values():
            if verified_only and spec.status != "verified":
                continue
            if status and spec.status != status:
                continue
            if task and task.lower() not in spec.task.lower():
                continue
            if modality and spec.modality != modality:
                continue
            results.append(spec)
        return results

    def get_spec(self, dataset_id: str) -> Optional[DatasetSpec]:
        """Retrieve spec by dataset ID."""
        return self.specs.get(dataset_id)

    def load_dataset_records(
        self,
        dataset_id: str,
        user_requested_rows: Optional[int] = None,
        template_type: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """
        Loads dataset records up to user_requested_rows (defaults to spec's max_rows).
        If raw file does not exist locally, returns dummy structured records for schema testing.
        """
        spec = self.get_spec(dataset_id)
        if not spec:
            raise ValueError(f"Dataset ID '{dataset_id}' not found.")

        rows_to_load = user_requested_rows if user_requested_rows is not None else spec.download_rows_default
        rows_to_load = min(rows_to_load, spec.max_rows)

        # Placeholder loading logic for demonstrated records
        records = []
        for i in range(min(5, rows_to_load)):
            sample = {
                "id": f"{spec.id}_{i+1}",
                "input": f"नमूना वाक्य {i+1}",
                "output": f"सही उत्तर {i+1}",
                "context": f"सन्दर्भ विवरण {i+1}",
                "question": f"प्रश्न {i+1}?",
                "answers": f"उत्तर {i+1}"
            }
            if template_type:
                records.append(spec.export_record(sample, template_type))
            else:
                records.append(sample)
        return records
