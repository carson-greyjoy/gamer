from __future__ import annotations

import json
from pathlib import Path

from universal_game_agent.workflow.models import WorkflowDefinition
from universal_game_agent.workflow.models import WorkflowAction
from universal_game_agent.workflow.models import WorkflowStep


def load_workflow(path: str | Path) -> WorkflowDefinition:
    workflow_path = Path(path)
    data = json.loads(workflow_path.read_text(encoding="utf-8"))
    steps = []
    for step_data in data.get("steps", []):
        actions = [WorkflowAction(**action_data) for action_data in step_data.get("actions", [])]
        steps.append(
            WorkflowStep(
                name=step_data["name"],
                description=step_data.get("description", ""),
                page=step_data.get("page"),
                actions=actions,
            )
        )
    return WorkflowDefinition(game=data["game"], name=data["name"], steps=steps)
