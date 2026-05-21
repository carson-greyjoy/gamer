from __future__ import annotations

import subprocess
from pathlib import Path

from universal_game_agent.core.runtime import RuntimeAdapter
from universal_game_agent.core.runtime import RuntimeContext


class ADBRuntime(RuntimeAdapter):
    """Android runtime backed by the adb command line."""

    def __init__(
        self,
        context: RuntimeContext,
        adb_path: str = "adb",
        adb_host: str | None = None,
        adb_port: int | None = None,
    ) -> None:
        super().__init__(context)
        self.adb_path = adb_path
        self.adb_host = adb_host
        self.adb_port = adb_port

    def screenshot(self) -> Path:
        output = Path("artifacts") / "adb_screenshot.png"
        output.parent.mkdir(parents=True, exist_ok=True)
        raw = self._run_adb("exec-out", "screencap", "-p", capture_output=True)
        output.write_bytes(raw)
        return output

    def tap(self, x: int, y: int) -> None:
        self._run_adb("shell", "input", "tap", str(x), str(y))

    def swipe(self, start: tuple[int, int], end: tuple[int, int], duration_ms: int = 300) -> None:
        self._run_adb(
            "shell",
            "input",
            "swipe",
            str(start[0]),
            str(start[1]),
            str(end[0]),
            str(end[1]),
            str(duration_ms),
        )

    def input_text(self, text: str) -> None:
        safe_text = text.replace(" ", "%s")
        self._run_adb("shell", "input", "text", safe_text)

    def _run_adb(self, *args: str, capture_output: bool = False) -> bytes:
        command = [self.adb_path]
        if self.adb_host:
            command.extend(["-H", self.adb_host])
        if self.adb_port:
            command.extend(["-P", str(self.adb_port)])
        if self.context.device_id:
            command.extend(["-s", self.context.device_id])
        command.extend(args)
        result = subprocess.run(
            command,
            check=True,
            capture_output=capture_output,
        )
        return result.stdout
