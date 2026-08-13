# Mobile Web Layout — Gradio patterns

Web-first, mobile-responsive layouts in Gradio (no custom frontend needed).
Reference for the **KISS Mobile Template** (`kiss/demos/mobile-template`).

## Bottom navigation (adaptive)

Pattern: a `gr.Column` holding 5 `gr.Button` "nav items" that is a **fixed
bottom bar on phones** and a **left rail on wide screens** via pure CSS:

```python
with gr.Row(elem_classes="k-shell"):
    with gr.Column(elem_classes="k-nav-col", scale=0, min_width=0):
        btn = gr.Button(value='<span class="emoji">🏠</span>Home',
                        elem_classes=["k-nav-item"], scale=1, min_width=0)
    with gr.Column(elem_classes="k-content", scale=1, min_width=0):
        view = gr.Column()  # the toggled screen
```

CSS essentials:

```css
.k-nav-col { display:flex; flex-direction:row; position:fixed; bottom:0; left:0; right:0;
             padding: 6px 8px calc(6px + env(safe-area-inset-bottom,0px)); }
.k-nav-item { min-height: 52px; }            /* >=44px touch target */
@media (min-width: 900px) {
  .k-nav-col { position: sticky; top:0; flex-direction:column; width: 96px;
               height: calc(100vh - 24px); border-right: 1px solid var(--border-color-primary); }
  .k-content { padding-bottom: 24px; }
}
```

- Exactly **5 destinations max** (Material rule). A **center item** can be an
  elevated "primary action" (`border-radius:999px; margin-top:-18px;`).
- **Server-side switching**: each nav button `.click(fn=select_view, ...)`
  toggles `gr.update(visible=...)` on the view columns.
- **Cosmetic only** active-highlight via injected `<script>` in `launch(head=)`:
  a click listener toggles the `.active` class. Logic stays server-side.

## Safe areas & viewport

`env(safe-area-inset-*)` needs `viewport-fit=cover`:

```python
HEAD = '<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">'
demo.launch(head=HEAD, ...)
```

Always provide a fallback: `env(safe-area-inset-bottom, 0px)`.

## Touch targets & spacing

- Buttons/tabs ≥ **44px** (iOS) / **48px** (Android) tall.
- Space nav items with `gap`, not margins, to avoid collapsed taps.
- `min-height: 52px` on nav items; generous `padding` on list rows.

## Theme-awareness

Consume Gradio CSS variables (with light fallbacks) so dark mode is automatic:

```css
.k-card { background: var(--block-background-fill, #fff); }
.k-nav-item.active { color: var(--color-accent, #3b82f6);
                     background: color-mix(in srgb, var(--color-accent) 12%, transparent); }
```

Verified 6.22 variables: `--body-background-fill`, `--body-text-color`,
`--body-text-color-subdued`, `--block-background-fill`, `--border-color-primary`,
`--color-accent`, `--primary-50..950`, `--radius-*`, `--shadow-drop`.

## Multipage caveat

`with demo.route("Site", "/site")` (outside the `with gr.Blocks()` context).
Cross-page component events are NOT supported — routes are for static pages
(e.g. a landing page whose CTA is a plain `<a href="/">`).
