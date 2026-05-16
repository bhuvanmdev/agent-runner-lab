from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime
from enum import Enum
from typing import Any


class StepType(str, Enum):
    RETRIEVAL = "retrieval"
    TOOL_CALL = "tool_call"
    MODEL = "model"
    OBSERVATION = "observation"


@dataclass(frozen=True)
class DatasetItem:
    id: str
    question: str
    expected_answer: str
    sources: list[str] = field(default_factory=list)
    tags: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class TraceStep:
    step_type: StepType
    name: str
    input_text: str
    output_text: str
    latency_ms: int
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class AgentRun:
    id: str
    dataset_item_id: str
    answer: str
    steps: list[TraceStep]
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class Score:
    run_id: str
    groundedness: float
    answer_overlap: float
    latency_score: float
    total: float
    notes: list[str] = field(default_factory=list)

