@echo off
setlocal enabledelayedexpansion

echo ================================================
echo  OmniTool Pro v1.0.0 - Build Script
echo ================================================
echo.

REM Check Python
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python not found. Please install Python 3.10+ from python.org
    pause
    exit /b 1
)

REM Check pip
pip --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] pip not found.
    pause
    exit /b 1
)

echo [1/4] Installing dependencies...
pip install -r requirements.txt >nul 2>&1
if errorlevel 1 (
    echo [WARN] Some dependencies may have failed. Continuing...
) else (
    echo       Done.
)

echo [2/4] Installing PyInstaller...
pip install pyinstaller >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Failed to install PyInstaller.
    pause
    exit /b 1
)
echo       Done.

echo [3/4] Building executable...
if not exist dist mkdir dist

pyinstaller --onefile --name OmniToolPro --windowed --icon=icon.ico --add-data "omnitool;omnitool" --hidden-import=customtkinter --hidden-import=openai --hidden-import=adb_shell --hidden-import=pyserial --hidden-import=pillow --hidden-import=pyperclip --hidden-import=colorama --hidden-import=psutil --hidden-import=platformdirs omnitool/__init__.py

if errorlevel 1 (
    echo [ERROR] Build failed.
    pause
    exit /b 1
)

echo       Done.

echo [4/4] Cleaning up...
if exist build rmdir /s /q build
if exist OmniToolPro.spec del OmniToolPro.spec
echo       Done.

echo.
echo ================================================
echo  Build complete! Output: dist\OmniToolPro.exe
echo ================================================
echo.
pause
