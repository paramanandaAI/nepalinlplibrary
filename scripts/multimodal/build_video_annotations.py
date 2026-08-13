"""Build annotated_videos_definition.csv from videos_definition.csv + id_mappings.json.

Filters videos_definition.csv down to the 256 annotated clips only, and renames
clip_id per id_mappings.json (clip_1 .. clip_256). Output written to the repo root.
"""
import csv
import json
import os

ROOT = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(ROOT, "annotated_videos_definition.csv")

with open(os.path.join(ROOT, "id_mappings.json"), encoding="utf-8") as f:
    clip_map = json.load(f)["clip_id_mappings"]  # uuid -> clip_N

src_rows = list(csv.DictReader(open(os.path.join(ROOT, "videos_definition.csv"), encoding="utf-8-sig")))
by_id = {r["clip_id"]: r for r in src_rows}

ordered = []
for uuid, label in clip_map.items():          # mapping order == clip_1..clip_256
    r = dict(by_id[uuid])
    r["clip_id"] = label
    ordered.append(r)

with open(OUT, "w", encoding="utf-8-sig", newline="") as f:
    w = csv.DictWriter(f, fieldnames=src_rows[0].keys(), lineterminator="\n")
    w.writeheader()
    w.writerows(ordered)

print(f"wrote {len(ordered)} clips -> {OUT}")
print("distinct source_video_id:", len(set(r['source_video_id'] for r in ordered)))
