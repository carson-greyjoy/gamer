from __future__ import annotations

from universal_game_agent.core.adb_runtime import ADBRuntime
from universal_game_agent.core.runtime import RuntimeAdapter
from universal_game_agent.core.runtime import RuntimeContext
from universal_game_agent.core.runtime import StubRuntime


def create_runtime(platform: str, device_id: str | None = None) -> RuntimeAdapter:
    context = RuntimeContext(platform=platform, device_id=device_id)
    if platform == "adb":
        return ADBRuntime(context)
    if platform in {"stub", "windows", "emulator"}:
        return StubRuntime(context)
    raise ValueError(f"Unsupported platform: {platform}")
