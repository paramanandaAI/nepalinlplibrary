# Testing Gradio Applications with Playwright

This guide documents the design of automated end-to-end UI testing rigs for Gradio applications, detailing selectors, synchronization patterns, and verification tests.

---

## 1. Playwright Testing Framework Setup

To run automated browser tests, we use the `pytest` runner paired with the `playwright` synchronous or asynchronous APIs.

### Directory Structure for Tests
```
kiss/
├── app.py
└── tests/
    ├── conftest.py          # Pytest fixtures (starts and stops Gradio)
    └── test_workbench.py    # UI interaction and assertion tests
```

---

## 2. Setting Up the Test Harness (`conftest.py`)

The test suite must spin up the Gradio server as a background subprocess before running browser scripts, and safely terminate it afterward.

```python
import subprocess
import time
import socket
import pytest

def is_port_in_use(port: int) -> bool:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex(('127.0.0.1', port)) == 0

@pytest.fixture(scope="session", autouse=True)
def run_gradio_server():
    # Start Gradio app as a subprocess
    process = subprocess.Popen(
        ["python", "app.py"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    
    # Wait for the server to bind to port 7860
    for _ in range(30):
        if is_port_in_use(7860):
            break
        time.sleep(0.5)
    else:
        process.terminate()
        raise RuntimeError("Gradio server failed to launch on port 7860.")
        
    yield
    
    # Clean up
    process.terminate()
    process.wait()
```

---

## 3. UI Interaction & Locator Rules

Because Gradio dynamically updates the DOM and wraps components in Svelte containers, referencing fragile CSS selectors (like `.css-1n7t8`) is bad practice. Instead, target components using **accessible roles, labels, and placeholders**:

### A. Targeting Forms & Inputs
```python
# Locate input boxes by their visible label
page.get_by_label("Language Code (COMPULSORY)").fill("ne")

# Locate textareas by placeholder text
page.get_by_placeholder("Provide a clear, factual description...").fill("सडकमा हिँडिरहेका मानिसहरू।")
```

### B. Handling Selectors & Dropdowns
Gradio Dropdowns use custom Svelte markup. To interact with them:
```python
# Click the dropdown container to expand options
page.get_by_label("Annotation Status").click()

# Click the specific item in the popover dropdown list
page.get_by_role("listitem").filter(has_text="done").click()
```

### C. Asserting Async Updates & Page State
Playwright automatically waits for elements to appear in the DOM. Use these locators to assert events:
```python
def test_save_workflow(page):
    page.goto("http://127.0.0.1:7860")
    
    # Select an image from the dropdown list
    page.get_by_label("Select Image to Annotate").click()
    page.get_by_role("listitem").filter(has_text="monsoon_field.jpg").click()
    
    # Input metadata
    page.get_by_label("Language Code (COMPULSORY)").fill("ne")
    page.get_by_placeholder("Provide a clear, factual description...").fill("मन्सुनको समयमा धान रोप्दै।")
    
    # Click save button
    page.get_by_role("button", name="Save Annotation").click()
    
    # Assert successful status indicator is rendered
    status_label = page.locator("text=Saved annotation for monsoon_field.jpg successfully!")
    expect(status_label).to_be_visible(timeout=5000)
```
