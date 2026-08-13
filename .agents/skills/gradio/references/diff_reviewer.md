# Interactive Canvas & Diff Reviewer Guide

This guide details implementation patterns for rendering structural/textual differences and capturing interactive annotation coordinate bounds in Gradio without Svelte compilation overhead.

---

## 1. HTML5 Canvas Bounding Box Overlay (Pure JS Integration)

Gradio doesn't ship a native drawing box selector. We resolve this by overlaying an HTML5 Canvas on a target image container, passing serialization strings via hidden text inputs.

### Setup Structure

```
+---------------------------------------------------+
| HTML5 Container (#canvas-container)              |
|  +---------------------------------------------+  |
|  | Image Asset (#annotate-target)              |  |
|  +---------------------------------------------+  |
|  | Absolute Overlay Canvas (#overlay-canvas)   |  |
|  +---------------------------------------------+  |
+---------------------------------------------------+
  │ (mouse drag draws boundary)
  ▼
 Serialize coordinate JSON array: "[{"x":5,"y":10,"w":40,"h":40}]"
  │
  ▼
 Write to value attribute of target textarea
  │
  ▼
 Dispatch event: targetTextarea.dispatchEvent(new Event('input'))
  │
  ▼
 triggers Python change(fn) event callback
```

### Python/HTML Markup Code
```python
def make_drawing_canvas(image_url):
    html_markup = f"""
    <div id="canvas-container" style="position: relative; display: inline-block; width: 100%;">
        <img id="annotate-target" src="{image_url}" style="width: 100%; display: block; user-select: none;" />
        <canvas id="overlay-canvas" style="position: absolute; top: 0; left: 0; width: 100%; height: 100%; cursor: crosshair;"></canvas>
    </div>
    
    <script>
        (function() {{
            const canvas = document.getElementById('overlay-canvas');
            const img = document.getElementById('annotate-target');
            const ctx = canvas.getContext('2d');
            let isDrawing = false;
            let startX = 0, startY = 0;
            let boxList = [];

            // Match canvas dimensions to image size
            img.onload = () => {{
                canvas.width = img.clientWidth;
                canvas.height = img.clientHeight;
            }};
            
            canvas.addEventListener('mousedown', (e) => {{
                startX = e.offsetX;
                startY = e.offsetY;
                isDrawing = true;
            }});

            canvas.addEventListener('mousemove', (e) => {{
                if (!isDrawing) return;
                ctx.clearRect(0, 0, canvas.width, canvas.height);
                // Draw all saved boxes
                ctx.strokeStyle = '#ef4444';
                ctx.lineWidth = 2;
                boxList.forEach(box => ctx.strokeRect(box.x, box.y, box.w, box.h));
                // Draw active box
                ctx.strokeStyle = '#3b82f6';
                ctx.strokeRect(startX, startY, e.offsetX - startX, e.offsetY - startY);
            }});

            canvas.addEventListener('mouseup', (e) => {{
                if (!isDrawing) return;
                const w = e.offsetX - startX;
                const h = e.offsetY - startY;
                boxList.push({{ x: startX, y: startY, w: w, h: h }});
                isDrawing = false;

                // Sync data to hidden Gradio input
                const tx = document.querySelector('#coords-input-box textarea');
                if (tx) {{
                    tx.value = JSON.stringify(boxList);
                    tx.dispatchEvent(new Event('input', {{ bubbles: true }}));
                }}
            }});
        }})();
    </script>
    """
    return html_markup
```

---

## 2. Textual & Structural JSON Diff Reviewers

Based on `trail-exp` specifications, comparing spelling-noised (ASR / OCR) source text with target Devanagari text requires custom diff rendering.

### A. Line & Word Textual Diff (Unified & Side-by-Side)
- **Unified Diff**: Display inline deletions and insertions using color highlights:
  - Deletions (`-`): Red highlight (`background-color: #fee2e2; color: #b91c1c; text-decoration: line-through;`).
  - Insertions (`+`): Green highlight (`background-color: #d1fae5; color: #047857;`).
- **Side-by-Side Diff**: Construct a `gr.Row()` containing two `gr.HTML` panels. Re-align lines with matching line index arrays to ensure visual comparisons.

### B. Structural JSON Diff (Field-Level highlighting)
- If comparing metadata sidecars:
  - Do NOT diff raw text strings of the serialized YAML.
  - Diff the dictionary key-value hierarchies.
  - Highlight added fields, changed values, and array index differences (e.g. added/deleted tags) inside a clean HTML tree.
