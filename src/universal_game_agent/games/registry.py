from __future__ import annotations

from universal_game_agent.games.afk_arena.plugin import build_plugin as build_afk_arena_plugin
from universal_game_agent.games.base import GamePlugin


def load_game_plugin(name: str) -> GamePlugin:
    if name == "afk_arena":
        return build_afk_arena_plugin()
    raise ValueError(f"Unsupported game plugin: {name}")
