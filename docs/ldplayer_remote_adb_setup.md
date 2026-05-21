# LDPlayer Remote ADB Setup

This guide connects the cloud Linux agent to LDPlayer running on a Windows PC.

## Current Linux Status

Completed on this Linux host:

- Installed `adb`.
- Installed Tailscale.
- Started and authenticated Tailscale.
- Linux Tailscale IPv4: `100.113.242.69`.
- Project runner supports remote ADB server options:
  - `--adb-host`
  - `--adb-port`
- Added an ADB connectivity checker:
  - `python3 -m universal_game_agent.adb_doctor`

## Target Topology

```text
Cloud Linux agent
  -> Tailscale network
  -> Windows PC
  -> Windows adb server
  -> LDPlayer emulator
```

Use the Windows PC as the ADB gateway. The Linux agent should not connect to the
LDPlayer emulator port directly unless the Windows adb server path fails.

## Windows Preparation

1. Install Tailscale on Windows.
2. Log in with the same Tailscale account used by the Linux host.
3. Find the Windows Tailscale IPv4:

```powershell
tailscale ip -4
```

4. Test Windows can see the Linux node:

```powershell
tailscale ping 100.113.242.69
```

## LDPlayer Preparation

1. Start LDPlayer.
2. Open the game once manually and finish any first-run prompts.
3. Use a fixed emulator resolution. Recommended first pass:
   - landscape
   - `1280x720`
   - DPI around `240`
4. Keep the emulator window open and unlocked.

Common LDPlayer adb locations:

```text
C:\LDPlayer\LDPlayer9\adb.exe
D:\leidian\LDPlayer9\adb.exe
```

If your install path differs, search for `adb.exe` under the LDPlayer install
directory.

## Windows ADB Server

Run these commands in PowerShell from the LDPlayer install directory that
contains `adb.exe`.

Check local emulator visibility:

```powershell
.\adb.exe devices -l
```

If no device appears, try connecting to LDPlayer's local ADB endpoint:

```powershell
.\adb.exe connect 127.0.0.1:5555
.\adb.exe devices -l
```

For multi-instance LDPlayer, the ADB ports are often incremented. Try:

```powershell
.\adb.exe connect 127.0.0.1:5555
.\adb.exe connect 127.0.0.1:5557
.\adb.exe connect 127.0.0.1:5559
.\adb.exe devices -l
```

Start an ADB server that listens on the Windows Tailscale interface:

```powershell
.\adb.exe kill-server
.\adb.exe -a -P 5037 nodaemon server
```

Keep this PowerShell window open while debugging.

Security note: ADB is a control channel. Only expose TCP `5037` on the Tailscale
network, not on the public internet.

## Windows Firewall

If Linux cannot connect to Windows port `5037`, add an inbound firewall rule for
the Tailscale interface or for the Tailscale IP range.

Quick test from Linux:

```bash
nc -vz <WINDOWS_TAILSCALE_IP> 5037
```

If `nc` is not installed, use:

```bash
timeout 3 bash -c '</dev/tcp/<WINDOWS_TAILSCALE_IP>/5037'
```

## Linux Validation

Replace `<WINDOWS_TAILSCALE_IP>` and `<DEVICE_ID>` with values from Windows.

List devices through the Windows ADB server:

```bash
adb -H <WINDOWS_TAILSCALE_IP> -P 5037 devices -l
```

Run the project connectivity checker:

```bash
PYTHONPATH=src python3 -m universal_game_agent.adb_doctor \
  --adb-host <WINDOWS_TAILSCALE_IP> \
  --adb-port 5037 \
  --device-id <DEVICE_ID>
```

Expected output includes:

- `state= device`
- `wm size= Physical size: ...`
- `density= Physical density: ...`
- screenshot saved to `artifacts/adb_doctor.png`

Run the workflow against LDPlayer:

```bash
PYTHONPATH=src python3 -m universal_game_agent.main \
  --game afk_arena \
  --workflow daily \
  --platform adb \
  --adb-host <WINDOWS_TAILSCALE_IP> \
  --adb-port 5037 \
  --device-id <DEVICE_ID>
```

## Fallback: SSH Reverse Tunnel

Use this if Windows firewall or ADB server exposure is troublesome.

On Windows, keep local ADB working first:

```powershell
.\adb.exe devices -l
```

Then open a reverse tunnel from Windows to Linux:

```powershell
ssh -N -R 15037:127.0.0.1:5037 ubuntu@<LINUX_PUBLIC_IP>
```

On Linux, talk to the forwarded ADB server:

```bash
adb -H 127.0.0.1 -P 15037 devices -l
```

Then use:

```bash
PYTHONPATH=src python3 -m universal_game_agent.adb_doctor \
  --adb-host 127.0.0.1 \
  --adb-port 15037 \
  --device-id <DEVICE_ID>
```

## Troubleshooting

If `adb devices` shows `offline`, restart the Windows ADB server and LDPlayer.

If Linux can reach Windows but no emulator appears, the issue is between
Windows ADB and LDPlayer. Re-run `.\adb.exe devices -l` on Windows first.

If screenshots are black or the game window is blank, disable LDPlayer background
frame limiting, keep the emulator in the foreground, and retry
`adb_doctor`.

If click coordinates are wrong, set LDPlayer back to `1280x720` before collecting
screenshots and tuning workflow coordinates.
