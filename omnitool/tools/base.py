"""Tool Manager - organizes and runs device management tools"""

from typing import Dict, List, Callable


class Tool:
    def __init__(self, name: str, category: str, description: str, callback: Callable = None):
        self.name = name
        self.category = category
        self.description = description
        self.callback = callback
        self.is_premium = False


class ToolManager:
    def __init__(self):
        self.tools: List[Tool] = []
        self._register_tools()

    def _register_tools(self):
        """Register all available tools"""
        tool_defs = [
            # FRP Tools
            ("Samsung TalkBack Method", "FRP", "Bypass FRP using TalkBack accessibility"),
            ("ADB Bypass", "FRP", "Bypass FRP via ADB commands"),
            ("QR Code Method", "FRP", "Bypass FRP using QR code"),
            ("Google Account Bypass", "FRP", "Remove Google account verification"),
            ("MTK FRP Reset", "FRP", "Reset FRP on MTK devices"),
            ("Qualcomm FRP", "FRP", "FRP bypass for Qualcomm devices"),
            ("Samsung ADB Enabler", "FRP", "Enable ADB on locked Samsung"),
            ("FRP Info", "FRP", "Learn about FRP protection"),
            # Android Tools
            ("ADB Shell", "Android", "Interactive ADB shell"),
            ("Fastboot Commands", "Android", "Fastboot mode operations"),
            ("Device Info", "Android", "Get full device information"),
            ("APK Installer", "Android", "Install APK files to device"),
            ("Screen Mirroring", "Android", "Mirror device screen to PC"),
            ("File Manager", "Android", "Browse device filesystem"),
            ("Logcat Viewer", "Android", "View system logs"),
            # IMEI Tools
            ("IMEI Lookup", "IMEI", "Lookup device info by IMEI"),
            ("TAC Database", "IMEI", "Check Type Allocation Code"),
            ("Blacklist Check", "IMEI", "Check if IMEI is blacklisted"),
            ("Warranty Check", "IMEI", "Check device warranty status"),
            ("Model Lookup", "IMEI", "Get model info from IMEI"),
            # Diagnostic Tools
            ("Full Diagnostics", "Diagnostics", "Run complete device diagnostics"),
            ("Battery Health", "Diagnostics", "Check battery status"),
            ("Storage Analysis", "Diagnostics", "Analyze storage usage"),
            ("Network Info", "Diagnostics", "View network status"),
            ("Hardware Test", "Diagnostics", "Test hardware components"),
            # Knox Tools
            ("Knox Status", "Knox", "Check Samsung Knox status"),
            ("Knox Decode", "Knox", "Decode Knox counter"),
            ("Warranty Status", "Knox", "Check Samsung warranty"),
            # Scripts
            ("Batch Unlock", "Scripts", "Run batch unlock script"),
            ("Device Backup", "Scripts", "Backup device data"),
            ("Factory Reset", "Scripts", "Reset device to factory state"),
            ("ROM Flash", "Scripts", "Flash custom/stock ROM"),
            ("Root Check", "Scripts", "Check root status"),
            ("Bootloader Unlock", "Scripts", "Unlock bootloader"),
            ("TWRP Install", "Scripts", "Install TWRP recovery"),
            ("Magisk Patch", "Scripts", "Patch boot image with Magisk"),
        ]

        for name, category, desc in tool_defs:
            self.tools.append(Tool(name, category, desc))

    def get_by_category(self, category: str) -> List[Tool]:
        return [t for t in self.tools if t.category == category]

    def get_all_categories(self) -> List[str]:
        return sorted(set(t.category for t in self.tools))

    def find(self, name: str) -> Tool:
        for t in self.tools:
            if t.name == name:
                return t
        return None

    def count(self) -> int:
        return len(self.tools)
