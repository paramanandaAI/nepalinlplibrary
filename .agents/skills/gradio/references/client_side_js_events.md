# Client-Side Javascript Event Loops in Gradio

This guide details implementation rules for injecting custom client-side Javascript, traversing components, and dispatching state events to trigger Python callbacks.

---

## 1. Bridging Python and Javascript

Gradio doesn't expose a direct hook for registering event listeners on the client side. Instead, we use a **Hidden Textbox Bridge**:

1. **Hidden Input Component**: Instantiate a `gr.Textbox(visible=False, elem_id="js-bridge-input")` in Python.
2. **Javascript Event Emitter**: Bind listener scripts (e.g. keyboard shortcut listeners or canvas drags).
3. **Dispatch State Sync**: Write the value to the textarea DOM element, and dispatch the `'input'` event.
4. **Python Handler**: Catch the update using `js_bridge.change(fn, inputs, outputs)`.

---

## 2. Targeting Gradio Elements (Traversing the DOM)

Gradio wraps components in Svelte Blocks. To reference inputs safely:
- Always set an `elem_id` on the target component (e.g., `elem_id="target-input"`).
- Target the underlying textarea or input field using a descendant query selector:
  ```javascript
  const inputEl = document.querySelector("#target-input textarea, #target-input input");
  ```
- If the Gradio app is rendered inside a hosted environment (like Hugging Face Spaces), it may be wrapped in a **Shadow DOM**. To traverse the shadow root:
  ```javascript
  const gradioApp = document.getElementsByTagName('gradio-app')[0];
  const root = gradioApp.shadowRoot ? gradioApp.shadowRoot : document;
  const inputEl = root.querySelector("#target-input textarea");
  ```

---

## 3. Dispatching Value Changes (Crucial Event Contract)

Simply modifying the `.value` property of a textarea using JS will **not** trigger Gradio's reactive loop, because Svelte binds listeners to DOM input events:
- **Rule**: You MUST call `dispatchEvent(new Event('input', { bubbles: true }))` after updating the value.

```javascript
function sendDataToGradio(elementId, payloadString) {
    const root = document.getElementsByTagName('gradio-app')[0].shadowRoot || document;
    const textarea = root.querySelector(`#${elementId} textarea`);
    if (textarea) {
        textarea.value = payloadString;
        // Trigger Gradio's reactive state update
        textarea.dispatchEvent(new Event('input', { bubbles: true }));
    }
}
```

---

## 4. Real-Time Client-Side Transliteration (Linguist Typing Helper)

Linguists often type Romanized characters (e.g. `nepal`) and expect them to automatically convert to Devanagari script (e.g. `नेपाल`) in the caption field:
- Bind a `keyup` event listener to the caption text area.
- Detect spacebars or punctuation keys.
- Run a dictionary/rules map on the current word buffer, replace the text, and dispatch the change.

```javascript
// Example JS helper injected via gr.Blocks(js=...)
const transliterateMap = {
    "nepal": "नेपाल",
    "paani": "पानी",
    "ghar": "घर"
};

function initTransliterationListener() {
    const root = document.getElementsByTagName('gradio-app')[0].shadowRoot || document;
    const captionBox = root.querySelector("#form-caption-input textarea");
    
    if (!captionBox) return;

    captionBox.addEventListener('keyup', (e) => {
        if (e.key === " " || e.key === "Enter") {
            const words = captionBox.value.split(" ");
            const lastWord = words[words.length - 2]?.toLowerCase();
            
            if (lastWord && transliterateMap[lastWord]) {
                words[words.length - 2] = transliterateMap[lastWord];
                captionBox.value = words.join(" ");
                // Force sync back to Python
                captionBox.dispatchEvent(new Event('input', { bubbles: true }));
            }
        }
    });
}
```
