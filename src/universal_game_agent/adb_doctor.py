from __future__ import annotations

import argparse
import subprocess
from pathlib import Path


def build_adb_command(args: argparse.Namespace, *adb_args: str) -> list[str]:
    command = [args.adb_path]
    if args.adb_host:
        command.extend(["-H", args.adb_host])
    if args.adb_port:
        command.extend(["-P", str(args.adb_port)])
    if args.device_id:
        command.extend(["-s", args.device_id])
    command.extend(adb_args)
    return command


def run_adb(args: argparse.Namespace, *adb_args: str, binary: bool = False) -> str | bytes:
    command = build_adb_command(args, *adb_args)
    result = subprocess.run(command, check=True, capture_output=True)
    if binary:
        return result.stdout
    return result.stdout.decode("utf-8", errors="replace").strip()


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Check remote ADB connectivity.")
    parser.add_argument("--adb-path", default="adb")
    parser.add_argument("--adb-host", default=None, help="Remote ADB server host, usually the Windows VPN IP.")
    parser.add_argument("--adb-port", type=int, default=5037)
    parser.add_argument("--device-id", default=None)
    parser.add_argument("--screenshot", default="artifacts/adb_doctor.png")
    return parser.parse_args()


def main() -> None:
    args = parse_args()

    print("[adb] devices")
    print(run_adb(args, "devices", "-l") or "(no output)")

    if not args.device_id:
        print("[adb] no --device-id provided; stop after device listing")
        return

    print("[adb] state=", run_adb(args, "get-state"))
    print("[adb] wm size=", run_adb(args, "shell", "wm", "size"))
    print("[adb] density=", run_adb(args, "shell", "wm", "density"))
    print("[adb] android=", run_adb(args, "shell", "getprop", "ro.build.version.release"))
    print("[adb] model=", run_adb(args, "shell", "getprop", "ro.product.model"))

    output = Path(args.screenshot)
    output.parent.mkdir(parents=True, exist_ok=True)
    image = run_adb(args, "exec-out", "screencap", "-p", binary=True)
    if not isinstance(image, bytes):
        raise TypeError("expected binary screenshot output")
    output.write_bytes(image)
    print(f"[adb] screenshot={output}")


if __name__ == "__main__":
    main()
