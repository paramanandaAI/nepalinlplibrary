# Annotation Canvas — Gradio options

> Stub. See also `vlm_visual_grounding.md` and `annotation_queues.md`.

## Current status

KISS annotation is **form-driven** (caption / language / status / tags), not
canvas-based. Use native Gradio components for image display + metadata:

- `gr.Image(type="filepath", interactive=False)` — read-only viewer.
- `gr.Gallery(..., select=fn)` — thumbnails whose `.select` event carries the
  clicked index (jump to the annotation screen for that item).
- `gr.AnnotatedImage` / `gr.ImageEditor` — built-in annotation display /
  editing components in Gradio 6; prefer these before building a custom canvas.

## If a drawing overlay is ever required

An HTML5 canvas inside `gr.HTML` **cannot fire Gradio server events directly**
and is risky to synchronize. Recommended upgrade path:

1. `gr.ImageEditor(brush=..., layers=...)` for point/box/polygon-ish overlays.
2. `gr.AnnotatedImage` for displaying pre-computed masks/boxes.
3. Only if those are insufficient: a custom `gr.HTML` canvas + the
   `client_side_js_events.md` trigger pattern (`js_on_load` + `trigger`), keeping
   coordinates server-side for persistence.

Coordinate persistence should still go through the same YAML sidecar pipeline
(`utils/yaml_sidecar.py`) as text metadata.
