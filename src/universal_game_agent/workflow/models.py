from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Literal

ActionType = Literal["click", "swipe", "wait", "input_text", "assert_page"]


@dataclass(slots=True)
class WorkflowAction:
    type: ActionType
    target: str | None = None
    value: str | None = None
    seconds: float | None = None
    start: tuple[int, int] | None = None
    end: tuple[int, int] | None = None
    position: tuple[int, int] | None = None
    duration_ms: int = 300
    params: dict[str, Any] = field(default_factory=dict)


@dataclass(slots=True)
class WorkflowStep:
    name: str
    description: str = ""
    page: str | None = None
    actions: list[WorkflowAction] = field(default_factory=list)


@dataclass(slots=True)
class WorkflowDefinition:
    game: str
    name: str
    steps: list[WorkflowStep] = field(default_factory=list)
