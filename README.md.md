# AI Developer Toolkit v2.0

Modular Python toolkit for AI developers. Compiles to a single Windows `.exe`.

## Features

- **File System Intelligence** — read, write, search, snapshot
- **Code Understanding** — AST parsing, module summaries, test generation
- **Python Automation** — script runner, package installer
- **Device Repair & Bypass**
  - Android FRP bypass (ADB, fastboot, TalkBack)
  - iCloud / Activation Lock bypass (DNS, checkm8, signal)
  - IMEI read/write/blacklist check (MTK, Qualcomm)
  - Knox & MDM removal
  - Root (Magisk) & Jailbreak (checkra1n) helpers
  - Soft-brick & hard-brick recovery
  - Rubber Ducky / O.MG payload generation
  - Factory reset / restore / user management
- **AI Chat Window** — GUI with natural language tool dispatch
- **Plugin Architecture** — auto-discover, hot-load, registry

## Quick Start

```bash
pip install -r requirements.txt

# GUI mode
python main.py --gui

# CLI mode
python main.py --tool list_tools
python main.py --tool device --category android_frp_bypass --device-tool bypass_via_adb
python main.py --tool read_file --file main.py