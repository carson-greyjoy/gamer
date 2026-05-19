from __future__ import annotations

import random
from dataclasses import dataclass

from universal_game_agent.core.runtime import RuntimeAdapter


@dataclass(slots=True)
class Toolbelt:
    runtime: RuntimeAdapter

    def click(self, x: int, y: int, jitter: int = 3) -> None:
        self.runtime.tap(
            x + random.randint(-jitter, jitter),
            y + random.randint(-jitter, jitter),
        )

    def swipe(
        self,
        start: tuple[int, int],
        end: tuple[int, int],
        duration_ms: int = 300,
    ) -> None:
        self.runtime.swipe(start, end, duration_ms)

    def wait(self, seconds: float) -> None:
        self.runtime.sleep(seconds)

    def random_delay(self, low: float = 0.4, high: float = 1.2) -> None:
        self.runtime.sleep(random.uniform(low, high))
