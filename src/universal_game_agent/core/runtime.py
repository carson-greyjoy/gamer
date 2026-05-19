from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any


@dataclass(slots=True)
class RuntimeContext:
    platform: str
    device_id: str | None = None
    resolution: tuple[int, int] | None = None
    metadata: dict[str, Any] = field(default_factory=dict)


class RuntimeAdapter(ABC):
    """Abstract interface for device interaction backends."""

    def __init__(self, context: RuntimeContext) -> None:
        self.context = context

    @abstractmethod
    def screenshot(self) -> Path:
        raise NotImplementedError

    @abstractmethod
    def tap(self, x: int, y: int) -> None:
        raise NotImplementedError

    @abstractmethod
    def swipe(self, start: tuple[int, int], end: tuple[int, int], duration_ms: int = 300) -> None:
        raise NotImplementedError

    @abstractmethod
    def input_text(self, text: str) -> None:
        raise NotImplementedError

    def sleep(self, seconds: float) -> None:
        import time

        time.sleep(seconds)


class StubRuntime(RuntimeAdapter):
    """Dry-run runtime for workflow bring-up and local testing."""

    def screenshot(self) -> Path:
        output = Path("artifacts") / "last_screenshot.png"
        output.parent.mkdir(parents=True, exist_ok=True)
        output.touch()
        return output

    def tap(self, x: int, y: int) -> None:
        print(f"[runtime] tap({x}, {y})")

    def swipe(self, start: tuple[int, int], end: tuple[int, int], duration_ms: int = 300) -> None:
        print(f"[runtime] swipe(start={start}, end={end}, duration_ms={duration_ms})")

    def input_text(self, text: str) -> None:
        print(f"[runtime] input_text({text!r})")
