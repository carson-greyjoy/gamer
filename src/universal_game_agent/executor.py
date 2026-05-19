from __future__ import annotations

from dataclasses import dataclass

from universal_game_agent.core.tools import Toolbelt
from universal_game_agent.games.base import GamePlugin
from universal_game_agent.planner.base import Planner
from universal_game_agent.state.models import GameState
from universal_game_agent.workflow.models import WorkflowAction, WorkflowDefinition, WorkflowStep


@dataclass(slots=True)
class ExecutionResult:
    planned_steps: list[str]
    completed_steps: list[str]


class WorkflowExecutor:
    def __init__(self, toolbelt: Toolbelt, planner: Planner, game: GamePlugin) -> None:
        self.toolbelt = toolbelt
        self.planner = planner
        self.game = game
        self.current_page = "unknown"

    def run(self, workflow: WorkflowDefinition, initial_state: GameState) -> ExecutionResult:
        plan = self.planner.plan(initial_state, workflow)
        completed: list[str] = []
        step_map = {step.name: step for step in workflow.steps}
        self.current_page = initial_state.page

        for step_name in plan:
            step = step_map[step_name]
            self._execute_step(step)
            completed.append(step.name)

        return ExecutionResult(planned_steps=plan, completed_steps=completed)

    def _execute_step(self, step: WorkflowStep) -> None:
        print(f"[workflow] step={step.name} page={step.page}")
        if step.page is not None:
            self.current_page = step.page
        for action in step.actions:
            self._execute_action(action)

    def _execute_action(self, action: WorkflowAction) -> None:
        if action.type == "click":
            position = action.position or self.game.resolve_point(self.current_page, action.target)
            if position is None:
                raise ValueError(f"click action requires a position or resolvable target: {action}")
            self.toolbelt.click(*position)
            self.toolbelt.random_delay()
            return

        if action.type == "swipe":
            if action.start is None or action.end is None:
                raise ValueError(f"swipe action requires start/end: {action}")
            self.toolbelt.swipe(action.start, action.end, action.duration_ms)
            self.toolbelt.random_delay()
            return

        if action.type == "wait":
            if action.seconds is None:
                raise ValueError(f"wait action requires seconds: {action}")
            self.toolbelt.wait(action.seconds)
            return

        if action.type == "input_text":
            self.toolbelt.runtime.input_text(action.value or "")
            self.toolbelt.random_delay()
            return

        if action.type == "assert_page":
            print(f"[workflow] assert_page({action.target})")
            if action.target is not None:
                self.current_page = action.target
            return

        raise ValueError(f"Unsupported action type: {action.type}")
