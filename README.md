# OmniTool Pro v1.0.0

A professional device management platform for Windows 11.

## Features

- 52+ device management tools
- Built-in AI assistant powered by OpenAI
- Native Windows 11 desktop application
- ADB & Fastboot integration
- Device information & diagnostics
- Modular tool architecture

## Quick Start

### Download & Run (Windows)

1. Download `OmniToolPro.exe` from the [latest release](https://github.com/omnitool-pro/omnitool-pro/releases/latest)
2. Run directly - no installation required

### Build from Source

```bash
# Prerequisites: Python 3.10+ installed

# 1. Clone the repository
git clone https://github.com/omnitool-pro/omnitool-pro.git
cd omnitool-pro

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run directly
python -m omnitool

# 4. (Optional) Build standalone .exe
build.bat
# Output: dist/OmniToolPro.exe
```

## Tool Categories

- **FRP Tools** - Factory Reset Protection utilities
- **Android Tools** - ADB, Fastboot, device management
- **IMEI Tools** - Device identification utilities
- **Diagnostic Tools** - Device info, health checks
- **Script Tools** - Automation and batch operations

## AI Assistant

OmniTool Pro includes a built-in AI assistant that can:
- Recommend the right tool for your task
- Generate ADB/command scripts
- Guide you through procedures step-by-step
- Answer device management questions

Set your OpenAI API key in `config.json` to enable AI features.

## Configuration

Create a `config.json` file:

```json
{
    "openai_api_key": "your-api-key-here",
    "theme": "dark",
    "adb_path": "adb",
    "auto_detect_devices": true
}
```

## Requirements

- Windows 10/11
- Python 3.10+ (for source build)
- ADB (optional, for Android tools)

## License

MIT License - See LICENSE file

## Disclaimer

This tool is for **legitimate device management purposes only**.
Use only on devices you own or are authorized to service.
