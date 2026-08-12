"""
Noising pipeline: JSONL in -> noised (clean, noised) pairs JSONL out, plus a report.

The pipeline is deliberately small: noising is one thing, pipelines are another.
Data acquisition/ingestion pipelines live elsewhere; this folder is for noising-related
orchestration only.
"""

import json
from pathlib import Path
from typing import Dict, List, Optional, Union

from ..denoise.pairs import make_pairs_from_records, write_jsonl
from ..noise.engine import list_noise_ops


class NoisingPipeline:
    """Applies a noise recipe to every text field in a JSONL dataset."""

    def __init__(
        self,
        ops: Optional[List[str]] = None,
        k: int = 1,
        seed: Optional[int] = None,
        text_field: str = "text",
    ):
        self.ops = ops or list_noise_ops()
        self.k = k
        self.seed = seed
        self.text_field = text_field

    def run(
        self,
        input_path: Union[str, Path],
        output_path: Union[str, Path],
        sample: Optional[int] = None,
    ) -> Dict:
        """Process a JSONL file and return a run report."""
        records = self._load_records(input_path, sample=sample)
        if not records:
            return {"status": "FAILED", "reason": "No records loaded", "pairs": 0}

        pairs = make_pairs_from_records(
            records,
            text_field=self.text_field,
            ops=self.ops,
            k=self.k,
            seed=self.seed,
        )
        write_jsonl(pairs, output_path)

        noised_count = sum(1 for p in pairs if p.noised != p.clean)
        return {
            "status": "SUCCESS",
            "input_records": len(records),
            "output_pairs": len(pairs),
            "changed": noised_count,
            "unchanged": len(pairs) - noised_count,
            "ops": list(dict.fromkeys(p.ops for p in pairs).keys()) if pairs else [],
            "output_path": str(output_path),
        }

    def _load_records(self, path: Union[str, Path], sample: Optional[int] = None) -> List[Dict]:
        records = []
        with open(path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                rec = json.loads(line)
                if isinstance(rec.get(self.text_field), str):
                    records.append(rec)
                if sample is not None and len(records) >= sample:
                    break
        return records
