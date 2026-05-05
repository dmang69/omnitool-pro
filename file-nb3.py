"""Build script for packaging AI Developer Toolkit."""
import subprocess
import sys
import shutil
from pathlib import Path


def build_executable():
    """Build Windows executable using PyInstaller."""
    root = Path(__file__).parent.parent
    
    print("Building AI Developer Toolkit...")
    print(f"Project root: {root}")
    
    # Install dependencies first
    print("\nInstalling dependencies...")
    subprocess.run(
        [sys.executable, "-m", "pip", "install", "-r", "requirements.txt"],
        cwd=str(root),
        check=True,
    )
    
    # Build with PyInstaller
    print("\nBuilding executable...")
    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--onefile",
        "--name", "ai_toolkit",
        "--add-data", f"config{Path().sep}config",
        "--add-data", f"plugins{Path().sep}plugins",
        "--distpath", str(root / "dist"),
        "--workpath", str(root / "build" / "temp"),
        "--specpath", str(root / "build"),
        str(root / "main.py"),
    ]
    
    subprocess.run(cmd, cwd=str(root), check=True)
    
    # Create launcher batch file
    launcher = root / "dist" / "start_toolkit.bat"
    launcher.write_text(
        '@echo off\n'
        'echo AI Developer Toolkit\n'
        'echo ====================\n'
        f'start "" "%~dp0ai_toolkit.exe" --chat\n'
        'pause\n',
        encoding="utf-8",
    )
    
    print(f"\nBuild complete!")
    print(f"Executable: {root / 'dist' / 'ai_toolkit.exe'}")
    print(f"Launcher: {launcher}")


if __name__ == "__main__":
    build_executable()