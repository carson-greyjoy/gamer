from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path

from universal_game_agent.state.models import GameState
from universal_game_agent.vision.base import DetectionResult


class GameDetector:
    def build_state(self, result: DetectionResult) -> GameState:
        raise NotImplementedError


@dataclass(slots=True)
class UIPoint:
    x: int
    y: int


@dataclass(slots=True)
class UIPageProfile:
    name: str
    points: dict[str, UIPoint] = field(default_factory=dict)


@dataclass(slots=True)
class GamePlugin:
    name: str
    workflow_root: Path
    detector: GameDetector
    pages: dict[str, UIPageProfile] = field(default_factory=dict)

    def resolve_point(self, page: str | None, target: str | None) -> tuple[int, int] | None:
        if page is None or target is None:
            return None
        profile = self.pages.get(page)
        if profile is None:
            return None
        point = profile.points.get(target)
        if point is None:
            return None
        return (point.x, point.y)
