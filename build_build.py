import subprocess
import sys
from pathlib import Path

def main():
    project_root = Path(__file__).resolve().parents[1]
    config_dir = project_root / "config"
    plugins_dir = project_root / "plugins"
    main_py = project_root / "main.py"

    cmd = [
        sys.executable,
        "-m",
        "PyInstaller",
        "--noconfirm",
        "--clean",
        "--onefile",
        "--name",
        "ai_toolkit",
        "--add-data",
        f"{config_dir};config",
        "--add-data",
        f"{plugins_dir};plugins",
        str(main_py),
    ]

    print("Building Windows executable...")
    result = subprocess.run(cmd)
    if result.returncode != 0:
        raise SystemExit(result.returncode)

    print("Build complete. See dist/ai_toolkit.exe")

if __name__ == "__main__":
    main()