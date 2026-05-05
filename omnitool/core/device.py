"""Device Manager - handles ADB and device detection"""

import subprocess
import platform
from typing import List


class DeviceManager:
    def __init__(self, adb_path: str = "adb"):
        self.adb_path = adb_path
        self.os_type = platform.system()

    def get_devices(self) -> List[str]:
        """Get list of connected Android devices via ADB"""
        try:
            result = subprocess.run(
                [self.adb_path, "devices"],
                capture_output=True, text=True, timeout=5
            )
            lines = result.stdout.strip().split("\n")[1:]
            devices = []
            for line in lines:
                if line.strip() and "device" in line:
                    devices.append(line.split("\t")[0])
            return devices
        except (FileNotFoundError, subprocess.TimeoutExpired):
            return []

    def get_device_info(self, device_id: str) -> dict:
        """Get detailed info for a specific device"""
        try:
            props = subprocess.run(
                [self.adb_path, "-s", device_id, "shell", "getprop"],
                capture_output=True, text=True, timeout=10
            )
            info = {}
            for line in props.stdout.split("\n"):
                if ":" in line:
                    key, _, value = line.partition(":")
                    info[key.strip()] = value.strip()
            return {
                "model": info.get("[ro.product.model]", "Unknown"),
                "android": info.get("[ro.build.version.release]", "Unknown"),
                "sdk": info.get("[ro.build.version.sdk]", "Unknown"),
                "manufacturer": info.get("[ro.product.manufacturer]", "Unknown"),
            }
        except Exception:
            return {}

    def execute_adb(self, device_id: str, command: str) -> str:
        """Execute an ADB shell command on a device"""
        try:
            result = subprocess.run(
                f"{self.adb_path} -s {device_id} shell {command}",
                shell=True, capture_output=True, text=True, timeout=15
            )
            return result.stdout or result.stderr
        except Exception as e:
            return f"Error: {e}"
