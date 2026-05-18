from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from agent_runner_lab.models import DatasetItem


class DatasetError(ValueError):
    """Raised when a dataset file cannot be loaded."""


def _expect_str(record: dict[str, Any], key: str) -> str:
    value = record.get(key)
    if not isinstance(value, str) or not value.strip():
        raise DatasetError(f"dataset item is missing a non-empty {key!r}")
    return value.strip()


def _expect_str_list(record: dict[str, Any], key: str) -> list[str]:
    value = record.get(key, [])
    if value is None:
        return []
    if not isinstance(value, list) or not all(isinstance(item, str) for item in value):
        raise DatasetError(f"dataset item {key!r} must be a list of strings")
    return [item.strip() for item in value if item.strip()]


def load_dataset(path: str | Path) -> list[DatasetItem]:
    dataset_path = Path(path)
    try:
        payload = json.loads(dataset_path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise DatasetError(f"dataset file not found: {dataset_path}") from exc
    except json.JSONDecodeError as exc:
        raise DatasetError(f"dataset file is not valid JSON: {dataset_path}") from exc

    if not isinstance(payload, list):
        raise DatasetError("dataset root must be a list")

    items: list[DatasetItem] = []
    seen_ids: set[str] = set()
    for record in payload:
        if not isinstance(record, dict):
            raise DatasetError("each dataset item must be an object")
        item = DatasetItem(
            id=_expect_str(record, "id"),
            question=_expect_str(record, "question"),
            expected_answer=_expect_str(record, "expected_answer"),
            sources=_expect_str_list(record, "sources"),
            tags=_expect_str_list(record, "tags"),
            metadata=record.get("metadata", {}) if isinstance(record.get("metadata", {}), dict) else {},
        )
        if item.id in seen_ids:
            raise DatasetError(f"duplicate dataset id: {item.id}")
        seen_ids.add(item.id)
        items.append(item)
    return items


def dump_dataset(items: list[DatasetItem], path: str | Path) -> None:
    payload = [
        {
            "id": item.id,
            "question": item.question,
            "expected_answer": item.expected_answer,
            "sources": item.sources,
            "tags": item.tags,
            "metadata": item.metadata,
        }
        for item in items
    ]
    Path(path).write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")

