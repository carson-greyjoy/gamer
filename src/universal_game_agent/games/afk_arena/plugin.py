from __future__ import annotations

from pathlib import Path

from universal_game_agent.games.afk_arena.detector import AFKArenaDetector
from universal_game_agent.games.base import GamePlugin
from universal_game_agent.games.base import UIPageProfile
from universal_game_agent.games.base import UIPoint


def build_plugin() -> GamePlugin:
    root = Path(__file__).resolve().parent
    return GamePlugin(
        name="afk_arena",
        workflow_root=root / "workflows",
        detector=AFKArenaDetector(),
        pages={
            "launch": UIPageProfile(
                name="launch",
                points={
                    "start_game": UIPoint(640, 610),
                },
            ),
            "home": UIPageProfile(
                name="home",
                points={
                    "mail": UIPoint(1180, 120),
                    "quests": UIPoint(1110, 480),
                    "idle_chest": UIPoint(640, 560),
                },
            ),
            "mailbox": UIPageProfile(
                name="mailbox",
                points={
                    "collect_all": UIPoint(1040, 650),
                },
            ),
            "quests": UIPageProfile(
                name="quests",
                points={
                    "daily_tab": UIPoint(220, 150),
                    "claim_all": UIPoint(1030, 660),
                },
            ),
            "idle_reward": UIPageProfile(
                name="idle_reward",
                points={
                    "claim": UIPoint(840, 615),
                },
            ),
        },
    )
