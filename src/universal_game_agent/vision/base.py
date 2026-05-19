from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field

@dataclass(slots=True)
class Detection:
    label: str
    confidence: float
    bbox: tuple[int, int, int, int] | None = None
    text: str | None = None


@dataclass(slots=True)
class DetectionResult:
    page: str | None = None
    detections: list[Detection] = field(default_factory=list)
    metadata: dict[str, str | int | float] = field(default_factory=dict)


class VisionEngine(ABC):
    @abstractmethod
    def detect(self, image_path: str) -> DetectionResult:
        raise NotImplementedError


class NullVisionEngine(VisionEngine):
    """Placeholder engine until OCR and model assets are integrated."""

    def detect(self, image_path: str) -> DetectionResult:
        return DetectionResult(page="unknown", metadata={"image_path": image_path})
