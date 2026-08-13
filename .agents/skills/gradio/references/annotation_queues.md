# Annotation Queue & Pagination Guide

This guide details the pagination and verification pattern for managing large lists of images, transcripts, or data items inside a single Gradio session.

---

## 1. Core Architecture of the Queue

An annotation queue organizes data items into a sequential walkthrough. It avoids loading all items simultaneously to maintain lightweight browser memory footprints.

```
       +---------------------------------------------+
       |   Pagination Header (12/50 Items Complete)   |
       +---------------------------------------------+
       |  [Show All]    [Show Todo]    [Show Done]   | <- Navigation Filter
       +---------------------------------------------+
       |  ◀ Previous                    Next ▶       | <- Navigation Buttons
       +---------------------------------------------+
       |                                             |
       |  [Active Item Viewport: Workbox Form]      |
       |                                             |
       +---------------------------------------------+
```

---

## 2. Inferred Doneness & State Indicators

Rather than requiring manual "Mark Done" clicks:
1. **Doneness Inference**: An item is considered "done" (complete) if it satisfies the compulsory field validation (e.g. `language` is filled AND `caption` is non-empty).
2. **Navigation Indicator**: The item list/selector displays status badges (`[TODO]`, `[DRAFTED]`, `[DONE]`) alongside names.
3. **Completion Gating**: The Export / Share button remains disabled or triggers an error alert until the progress bar reaches 100% completion (or unless the user opts to "Include unannotated records").

---

## 3. Filtering States

Provide filters to constrain pagination:
- **All**: Navigates through the entire index sequentially.
- **Todo (Undone)**: Dynamically filters the list to show only items lacking complete captions or languages. Pressing "Next" automatically jumps to the next incomplete item.
- **Done**: Lists only verified items for quick review.

### Python State Controller Implementation
```python
def get_next_index(items, current_idx, filter_mode="all"):
    """
    Returns the next index in the queue based on filter state.
    """
    n = len(items)
    if n == 0:
        return 0

    idx = (current_idx + 1) % n
    attempts = 0
    
    while attempts < n:
        item = items[idx]
        is_done = bool(item.get("metadata", {}).get("language") and item.get("metadata", {}).get("caption", "").strip())
        
        if filter_mode == "all":
            return idx
        elif filter_mode == "todo" and not is_done:
            return idx
        elif filter_mode == "done" and is_done:
            return idx
            
        idx = (idx + 1) % n
        attempts += 1
        
    return current_idx
```
