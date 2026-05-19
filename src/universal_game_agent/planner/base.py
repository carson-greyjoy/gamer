from __future__ import annotations

from abc import ABC, abstractmethod

from universal_game_agent.state.models import GameState
from universal_game_agent.workflow.models import WorkflowDefinition


class Planner(ABC):
    @abstractmethod
    def plan(self, state: GameState, workflow: WorkflowDefinition) -> list[str]:
        raise NotImplementedError


class RulePlanner(Planner):
    """Returns steps in workflow order for the current MVP."""

    def plan(self, state: GameState, workflow: WorkflowDefinition) -> list[str]:
        del state
        return [step.name for step in workflow.steps]
