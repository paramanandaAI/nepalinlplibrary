---
name: huggingface-trackio
description: Track and visualize ML training experiments with Trackio. Use when logging metrics during training (Python API), firing alerts for training diagnostics, or retrieving/analyzing logged metrics (CLI). Supports real-time dashboard visualization, alerts with webhooks, HF Space syncing, and JSON output for automation.
---

# Trackio - Experiment Tracking for ML Training (Official Skill)

Trackio is an experiment tracking library for logging and visualizing ML training metrics. It syncs to Hugging Face Spaces for real-time monitoring dashboards.

## Three Interfaces

| Task | Interface |
|------|-----------|
| **Logging metrics** during training | Python API |
| **Firing alerts** for training diagnostics | Python API |
| **Retrieving metrics & alerts** after/during training | CLI |

## Python API → Logging

Use `import trackio` in your training scripts to log metrics:
- Initialize tracking with `trackio.init()`
- Log metrics with `trackio.log()` or use TRL's `report_to="trackio"`
- Finalize with `trackio.finish()`

**Key concept**: For remote/cloud training, pass `space_id` — metrics sync to a Space dashboard so they persist after the instance terminates. Auto-created Spaces are public by default — pass `private=True` if the metrics should not be public.
