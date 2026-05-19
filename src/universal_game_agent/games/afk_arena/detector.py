from __future__ import annotations

from dataclasses import dataclass

from universal_game_agent.state.models import ButtonState, GameState
from universal_game_agent.vision.base import DetectionResult


@dataclass(slots=True)
class AFKArenaDetector:
    """Maps generic vision outputs into AFK Arena page state."""

    def build_state(self, result: DetectionResult) -> GameState:
        buttons = []
        for detection in result.detections:
            center = None
            if detection.bbox is not None:
                x1, y1, x2, y2 = detection.bbox
                center = ((x1 + x2) // 2, (y1 + y2) // 2)
            buttons.append(ButtonState(name=detection.label, center=center))

        return GameState(
            page=result.page or "unknown",
            buttons=buttons,
            resources={"detected_count": len(result.detections)},
        )
