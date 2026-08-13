"""
Dataset Specification Module (`nepalinlplibrary.dataloader.spec`)
Parses and validates enhanced dataset YAML contract files.
"""

from dataclasses import dataclass, field
from typing import Dict, Any, Optional, List
import yaml
import os

@dataclass
class DatasetSpec:
    id: str
    name: str
    source_url: str
    task: str
    status: str = "todo"  # 'verified' or 'todo'
    quality_tier: str = "raw"
    modality: str = "text"  # 'text', 'audio', 'image_text', 'sign_language', 'multimodal'
    license: str = "open"
    language: str = "ne"
    script: str = "Devanagari"
    split: str = "train"
    
    # Sizing & row limits
    max_rows: int = 10000
    total_size_mb: Optional[float] = None
    download_rows_default: int = 10000
    
    # Language breakdowns
    languages: Dict[str, int] = field(default_factory=lambda: {"ne": 10000})
    
    # Schema mappings & templates
    column_mapping: Dict[str, str] = field(default_factory=dict)
    output: str = ""
    export_templates: Dict[str, Any] = field(default_factory=dict)
    validation: Dict[str, Any] = field(default_factory=dict)
    filepath: Optional[str] = None

    @classmethod
    def from_yaml_file(cls, filepath: str) -> "DatasetSpec":
        """Load DatasetSpec from a YAML file path."""
        with open(filepath, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f) or {}

        size_stats = data.get("size_stats", {})
        max_rows = size_stats.get("max_rows", data.get("target_rows", 10000))
        download_rows = size_stats.get("download_rows_default", max_rows)
        total_size_mb = size_stats.get("total_size_mb", None)
        
        langs = data.get("languages")
        if not langs:
            langs = {data.get("language", "ne"): max_rows}

        return cls(
            id=data.get("id", os.path.basename(filepath).replace(".yaml", "")),
            name=data.get("name", ""),
            source_url=data.get("source_url", ""),
            task=data.get("task", "general"),
            status=data.get("status", "todo" if "todo_" in os.path.basename(filepath) else "verified"),
            quality_tier=data.get("quality_tier", "raw"),
            modality=data.get("modality", "text"),
            license=data.get("license", "open"),
            language=data.get("language", "ne"),
            script=data.get("script", "Devanagari"),
            split=data.get("split", "train"),
            max_rows=max_rows,
            total_size_mb=total_size_mb,
            download_rows_default=download_rows,
            languages=langs,
            column_mapping=data.get("column_mapping", {}),
            output=data.get("output", ""),
            export_templates=data.get("export_templates", {}),
            validation=data.get("validation", {}),
            filepath=filepath
        )

    def export_record(self, record: Dict[str, Any], template_type: str = "t5") -> Any:
        """
        Transforms raw dataset record into requested template format (t5, gemma4, bert).
        """
        template = self.export_templates.get(template_type)
        if not template:
            return record

        if template_type == "t5":
            prefix = template.get("task_prefix", "")
            source = template.get("source_text", "")
            target = template.get("target_text", "")
            return {
                "source": prefix + source.format(**record),
                "target": target.format(**record)
            }
        elif template_type == "gemma4":
            messages = template.get("messages", [])
            formatted = []
            for msg in messages:
                formatted.append({
                    "role": msg.get("role", "user"),
                    "content": msg.get("content", "").format(**record)
                })
            return {"messages": formatted}
        elif template_type == "bert":
            fmt = template.get("format", "single_sequence")
            result = {"format": fmt}
            for k, v in template.items():
                if k != "format" and isinstance(v, str):
                    result[k] = v.format(**record)
            return result

        return record

    def devanagari_purity_ratio(self, text: str) -> float:
        """Calculates Unicode Devanagari character ratio (U+0900 to U+097F)."""
        if not text:
            return 0.0
        devanagari_count = sum(1 for ch in text if '\u0900' <= ch <= '\u097f')
        return devanagari_count / len(text)

    def validate_record(self, record: Dict[str, Any], min_devanagari_threshold: Optional[float] = None) -> bool:
        """
        Validates record against canonical schema rules:
        - Non-empty output.
        - Devanagari ratio >= threshold (default 80% or spec validation setting).
        """
        threshold = min_devanagari_threshold or self.validation.get("min_devanagari_ratio", 0.80)
        
        # Check non-empty output
        output_val = record.get("output") or record.get("answers") or record.get("target") or ""
        if isinstance(output_val, str) and not output_val.strip():
            return False
            
        # Check Devanagari purity on instruction + output
        combined = f"{record.get('instruction', '')} {output_val}"
        if combined.strip() and self.devanagari_purity_ratio(combined) < threshold:
            return False

        return True

