from __future__ import annotations

import argparse
from pathlib import Path

from universal_game_agent.bootstrap import create_runtime
from universal_game_agent.core.tools import Toolbelt
from universal_game_agent.executor import WorkflowExecutor
from universal_game_agent.games.registry import load_game_plugin
from universal_game_agent.planner.base import RulePlanner
from universal_game_agent.state.models import GameState
from universal_game_agent.vision.base import NullVisionEngine
from universal_game_agent.workflow.loader import load_workflow


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="UniversalGameAgent runner")
    parser.add_argument("--game", default="afk_arena")
    parser.add_argument("--workflow", default="daily")
    parser.add_argument("--platform", default="stub")
    parser.add_argument("--device-id", default=None)
    parser.add_argument("--adb-host", default=None)
    parser.add_argument("--adb-port", type=int, default=None)
    return parser.parse_args()


def resolve_workflow_path(game: str, workflow_name: str) -> Path:
    plugin = load_game_plugin(game)
    return plugin.workflow_root / f"{workflow_name}.yaml"


def main() -> None:
    args = parse_args()
    plugin = load_game_plugin(args.game)
    workflow_path = resolve_workflow_path(args.game, args.workflow)
    workflow = load_workflow(workflow_path)

    runtime = create_runtime(
        platform=args.platform,
        device_id=args.device_id,
        adb_host=args.adb_host,
        adb_port=args.adb_port,
    )
    toolbelt = Toolbelt(runtime=runtime)
    planner = RulePlanner()
    executor = WorkflowExecutor(toolbelt=toolbelt, planner=planner, game=plugin)

    screenshot_path = runtime.screenshot()
    vision = NullVisionEngine()
    detection_result = vision.detect(str(screenshot_path))
    initial_state: GameState = plugin.detector.build_state(detection_result)

    result = executor.run(workflow, initial_state)
    print("[result] planned_steps=", result.planned_steps)
    print("[result] completed_steps=", result.completed_steps)


if __name__ == "__main__":
    main()
