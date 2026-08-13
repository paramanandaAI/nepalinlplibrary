# Gradio Custom Component Creation Guide

This guide details the interface contract and programming style required to build custom components in Gradio 6.0, dividing implementation between the Python backend and Svelte frontend.

---

## 1. Python Backend Component Structure

Every custom component inherits from `Component` or `FormComponent` (located in `gradio.components.base`).

### Example Python Blueprint
```python
from __future__ import annotations
from typing import Any, Callable, Literal
from gradio.components.base import FormComponent
from gradio.events import Events

class CustomDrawCanvas(FormComponent):
    """
    Custom component for linguists to draw bounding regions on images.
    """
    # Declare the supported Svelte events
    EVENTS = [Events.change, Events.input, Events.select]

    def __init__(
        self,
        value: Any = None,
        *,
        label: str | None = None,
        every: float | None = None,
        show_label: bool | None = None,
        container: bool = True,
        interactive: bool | None = None,
        visible: bool = True,
        scale: int | None = None,
        min_width: int = 160,
        elem_id: str | None = None,
        elem_classes: list[str] | str | None = None,
        **kwargs,
    ):
        super().__init__(
            label=label,
            every=every,
            show_label=show_label,
            container=container,
            interactive=interactive,
            visible=visible,
            elem_id=elem_id,
            elem_classes=elem_classes,
            value=value,
            scale=scale,
            min_width=min_width,
            **kwargs,
        )

    def preprocess(self, x: Any) -> Any:
        """
        Converts the incoming Svelte client value (e.g. JSON string of coordinates)
        before passing it to the Python user callback.
        """
        if x is None:
            return []
        # Return Python dict/list representation
        return x

    def postprocess(self, y: Any) -> Any:
        """
        Serializes the Python function return value into client-friendly format
        before serving it to the Svelte template.
        """
        if y is None:
            return []
        return y
```

---

## 2. Svelte Frontend Component Structure

The frontend lives in a `frontend/` directory with a standard structure:
- `package.json`: Packages dependencies (e.g. `@gradio/atoms`, `@gradio/statustracker`).
- `interactive/InteractiveComponent.svelte`: Handles interactive/input state.
- `static/StaticComponent.svelte`: Handles read-only/output state.
- `shared/`: Holds reusable layout UI blocks.

### Interactive Svelte Blueprint (`InteractiveComponent.svelte`)
```html
<svelte:options accessors={true} />

<script lang="ts">
	import type { Gradio } from "@gradio/utils";
	import { createEventDispatcher } from "svelte";
	import { Block } from "@gradio/atoms";
	import { StatusTracker } from "@gradio/statustracker";
	import type { LoadingStatus } from "@gradio/statustracker";

	const dispatch = createEventDispatcher<{
		change: string;
		input: never;
	}>();

	// Bind Gradio interaction helpers
	export let gradio: Gradio<{
		change: string;
		input: never;
	}> = { dispatch, i18n: (s: string) => s };

	// Bind component parameters
	export let label = "Annotation Canvas";
	export let elem_id = "";
	export let elem_classes: string[] = [];
	export let visible = true;
	export let value = ""; // Binds to the serialized backend value
	export let show_label: boolean;
	export let container = true;
	export let scale: number | null = null;
	export let min_width: number | undefined = undefined;
	export let loading_status: LoadingStatus | undefined = undefined;
	export let value_is_output = false;
</script>

<Block
	{visible}
	{elem_id}
	{elem_classes}
	{scale}
	{min_width}
	allow_overflow={false}
	padding={container}
>
	{#if loading_status}
		<StatusTracker
			autoscroll={gradio.autoscroll}
			i18n={gradio.i18n}
			{...loading_status}
		/>
	{/if}

	<!-- Custom markup panel -->
	<div class="custom-component-panel">
		{#if show_label}
			<span class="component-label">{label}</span>
		{/if}
		
		<!-- Custom Interactive canvas or UI controls -->
		<textarea 
			bind:value 
			on:change={() => gradio.dispatch("change", value)}
			on:input={() => gradio.dispatch("input")}
		></textarea>
	</div>
</Block>
```
