# Agent Runner Lab

Agent Runner Lab is a small evaluation workbench for RAG and tool-using agents. It stores benchmark datasets, runs deterministic agent simulations, scores traces, and exposes the results through a CLI, API, and lightweight dashboard.

The project is intentionally local-first. It gives teams a way to test agent behavior without sending prompts or traces to a hosted service.

## Why this exists

Agent demos often look good until teams need to answer practical questions:

- Which retrieval sources were used?
- Did the agent cite enough evidence?
- Did latency or token budget drift across runs?
- Which questions repeatedly fail?
- Can a reviewer reproduce an old run?

This repo focuses on those boring but important pieces.

## Planned surface

- SQLite storage for datasets, runs, trace steps, and scores.
- Deterministic baseline agent for repeatable evaluation.
- Scoring utilities for grounding, latency, cost, and answer coverage.
- CLI commands for importing datasets, running evaluations, and exporting reports.
- FastAPI service for local integrations.
- Static dashboard for reviewing recent runs.

