---
name: gradio
description: "Master Gradio skill for building responsive web-first UI applications, annotation canvases, mobile layouts, diff reviewers, client-side event loops, custom components, and automated testing."
---

# Unified Gradio Master Skill

This is the single, comprehensive skill for authoring, refactoring, and maintaining Gradio 6.0 web applications in this workspace.

---

## 1. Quick Reference & Core Conventions

1. **Blocks Launch Constraints (Gradio 6.0)**:
   - Pass `css` and `theme` to `.launch(...)`, NOT to `gr.Blocks(...)`.
     ```python
     with gr.Blocks(title="KISS Workbench") as demo:
         ...
     demo.launch(server_name="0.0.0.0", server_port=7860, css=GRADIO_CSS, theme=gr.themes.Soft())
     ```
2. **Replacing Box Components**:
   - `gr.Box` is removed. Use `gr.Group` (visual grouping) or `gr.Column(variant="panel")`.
3. **Local File Serving**:
   - Use `gr.Image(type="filepath")` or `gr.Gallery` so Gradio serves local disk paths securely.

---

## 2. Modular References Handbook

All detailed sub-guides are available under [`references/`](file:///D:/noising_denoising/kiss/.agents/skills/gradio/references/):

- **[`mobile_web_layout.md`](file:///D:/noising_denoising/kiss/.agents/skills/gradio/references/mobile_web_layout.md)**: Web-first mobile responsive layouts (bottom navigation bar media queries, 44px touch targets, accordion panels).
- **[`annotation_canvas.md`](file:///D:/noising_denoising/kiss/.agents/skills/gradio/references/annotation_canvas.md)**: HTML5 Canvas overlays, click/drag coordinate capturing, and token selection spans.
- **[`annotation_queues.md`](file:///D:/noising_denoising/kiss/.agents/skills/gradio/references/annotation_queues.md)**: Pagination queues, item-by-item prev/next navigation, and `all`/`todo`/`done` state filters.
- **[`client_side_js_events.md`](file:///D:/noising_denoising/kiss/.agents/skills/gradio/references/client_side_js_events.md)**: Shadow DOM traversal, dispatching `'input'` events, and real-time Romanized-to-Devanagari keypress transliterators.
- **[`custom_component_creation.md`](file:///D:/noising_denoising/kiss/.agents/skills/gradio/references/custom_component_creation.md)**: Python `FormComponent` / `Component` backend subclassing and Svelte frontend template structures.
- **[`diff_reviewer.md`](file:///D:/noising_denoising/kiss/.agents/skills/gradio/references/diff_reviewer.md)**: Textual line diffs (unified/side-by-side) and structural field-level JSON diffs.
- **[`local_data_flow.md`](file:///D:/noising_denoising/kiss/.agents/skills/gradio/references/local_data_flow.md)**: Localized YAML sidecars (`metadata.yml`), subview state sync, and JSONL/ZIP export pipelines.
- **[`vlm_visual_grounding.md`](file:///D:/noising_denoising/kiss/.agents/skills/gradio/references/vlm_visual_grounding.md)**: Automated VLM candidate audit loops (Gemini vs DeepSeek) and CLIP/chrF quality metrics.
- **[`automated_testing_playwright.md`](file:///D:/noising_denoising/kiss/.agents/skills/gradio/references/automated_testing_playwright.md)**: Automated end-to-end UI testing using Playwright and pytest fixtures.