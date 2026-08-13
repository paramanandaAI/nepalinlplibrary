"""
Unit tests for nepalinlplibrary.dataloader package
"""

import pytest
import os
import tempfile
import yaml
try:
    from nepalinlplibrary.dataloader import DatasetSpec, DatasetLoader, CatalogManager
except ModuleNotFoundError:
    from dataloader import DatasetSpec, DatasetLoader, CatalogManager

@pytest.fixture
def sample_yaml_file():
    content = {
        "id": "huggingface_test_dataset",
        "name": "test/dataset",
        "source_url": "https://huggingface.co/datasets/test/dataset",
        "task": "sft/qa",
        "status": "verified",
        "quality_tier": "gold",
        "modality": "text",
        "language": "ne",
        "size_stats": {
            "max_rows": 5000,
            "download_rows_default": 5000,
            "total_size_mb": 12.5
        },
        "languages": {"ne": 5000},
        "column_mapping": {"q": "question", "a": "answers"},
        "export_templates": {
            "t5": {
                "task_prefix": "qa: ",
                "source_text": "Q: {q}",
                "target_text": "{a}"
            },
            "gemma4": {
                "messages": [
                    {"role": "user", "content": "Question: {q}"},
                    {"role": "model", "content": "{a}"}
                ]
            }
        }
    }
    
    with tempfile.NamedTemporaryFile("w", suffix=".yaml", delete=False, encoding="utf-8") as f:
        yaml.dump(content, f)
        filepath = f.name
        
    yield filepath
    if os.path.exists(filepath):
        os.remove(filepath)

def test_dataset_spec_parsing(sample_yaml_file):
    spec = DatasetSpec.from_yaml_file(sample_yaml_file)
    assert spec.id == "huggingface_test_dataset"
    assert spec.status == "verified"
    assert spec.modality == "text"
    assert spec.max_rows == 5000
    assert spec.languages["ne"] == 5000
    assert spec.total_size_mb == 12.5

def test_export_record_t5(sample_yaml_file):
    spec = DatasetSpec.from_yaml_file(sample_yaml_file)
    record = {"q": "नेपाल कस्तो देश हो?", "a": "सुन्दर"}
    exported = spec.export_record(record, "t5")
    assert exported["source"] == "qa: Q: नेपाल कस्तो देश हो?"
    assert exported["target"] == "सुन्दर"

def test_export_record_gemma4(sample_yaml_file):
    spec = DatasetSpec.from_yaml_file(sample_yaml_file)
    record = {"q": "नेपाल कस्तो देश हो?", "a": "सुन्दर"}
    exported = spec.export_record(record, "gemma4")
    assert len(exported["messages"]) == 2
    assert exported["messages"][0]["content"] == "Question: नेपाल कस्तो देश हो?"
    assert exported["messages"][1]["content"] == "सुन्दर"

def test_dataset_loader_discovery(sample_yaml_file):
    parent_dir = os.path.dirname(sample_yaml_file)
    loader = DatasetLoader(root_dir=parent_dir, auto_clone=False)
    assert len(loader.specs) >= 1
    assert "huggingface_test_dataset" in loader.specs

def test_catalog_manager(sample_yaml_file):
    parent_dir = os.path.dirname(sample_yaml_file)
    loader = DatasetLoader(root_dir=parent_dir, auto_clone=False)
    cat_mgr = CatalogManager(loader)
    entries = cat_mgr.generate_catalog_dict()
    assert len(entries) >= 1
    assert entries[0]["id"] == "huggingface_test_dataset"
