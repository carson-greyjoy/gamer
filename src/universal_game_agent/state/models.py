from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(slots=True)
class ButtonState:
    name: str
    center: tuple[int, int] | None = None
    enabled: bool = True


@dataclass(slots=True)
class GameState:
    page: str = "unknown"
    buttons: list[ButtonState] = field(default_factory=list)
    resources: dict[str, int | float | str] = field(default_factory=dict)

    def has_button(self, name: str) -> bool:
        return any(button.name == name and button.enabled for button in self.buttons)
