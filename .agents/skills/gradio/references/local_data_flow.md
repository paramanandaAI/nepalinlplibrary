# Local Data Flow & Sidecar Syncing Guide

This guide details localized dataset management, state synchronization across Gradio views, and export formatting pipelines for multimodal training.

---

## 1. Localized Sidecar Specifications

To ensure the dataset is fully portable and doesn't rely on database instances:
- Store metadata adjacent to source assets in plain text **YAML sidecar files** (`photo.jpg` $\to$ `photo.jpg.yml` or `photo.yml`).
- Structure Schema:
  ```yaml
  caption: "Detailed description of the visual scene in native script."
  language: "ne"
  status: "todo"
  tags:
    - tag1
    - tag2
  source: "field study"
  notes: "Linguistic observations."
  llm_evaluation:
    score: 8.5
    feedback: "Grammar looks correct."
    qa_history:
      - question: "What is shown in the image?"
        answer: "A traditional ritual."
  ```

---

## 2. Dynamic State Syncing Across Views

Because Gradio operates a single-page application under the hood, navigating between pages requires hiding and showing layout containers. When a user interacts with one page, other pages must be updated in sync:

### A. Jump-From-Gallery Event Handlers
Clicking on an item in the gallery explorer should instantly launch the workspace, select the matching file, and load its metadata:
```python
# Event definition in app.py
gallery.select(
    fn=open_in_workspace,
    inputs=[],
    outputs=[dash_layout, gal_layout, work_layout, ingest_layout, export_layout, workspace_selector]
)

def open_in_workspace(evt: gr.SelectData, items_list):
    selected_idx = evt.index
    selected_item = items_list[selected_idx]
    relative_path = selected_item["relative_path"]
    
    # Return visibility updates (hiding gallery, showing workspace) 
    # and set the workspace image dropdown value to trigger its load handler
    return (
        gr.update(visible=False), # dash
        gr.update(visible=False), # gal
        gr.update(visible=True),  # work
        gr.update(visible=False), # ingest
        gr.update(visible=False), # export
        gr.update(value=relative_path) # selector
    )
```

---

## 3. Dataset Export Formats

1. **JSONL Format**: Convert YAML metadata lists into single-line JSON records containing relative asset references:
   ```json
   {"image_path": "images/monsoon/monsoon.jpg", "language": "ne", "caption": "A rice field during monsoon."}
   ```
2. **ZIP Bundle**: Iterate over the dataset, adding each image and its `.yml` sidecar into a ZIP archive along with the `dataset.jsonl` index.
