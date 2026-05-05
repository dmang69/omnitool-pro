"""Android Debug Bridge (ADB) command manager."""
import subprocess
from pathlib import Path
from typing import Any, Dict, List, Optional


class ADBManager:
    """Manage ADB operations for Android devices."""
    
    def __init__(self, security_manager, config):
        self.security = security_manager
        self.config = config
        self.adb_path = config.get("android.adb_path", "adb")
        self.fastboot_path = config.get("android.fastboot_path", "fastboot")
        self.timeout = config.get("android.default_timeout", 30)
    
    def _run_adb(
        self, args: List[str], device_id: Optional[str] = None, timeout: int = None
    ) -> Dict[str, Any]:
        """Run an ADB command."""
        cmd = [self.adb_path]
        if device_id:
            cmd.extend(["-s", device_id])
        cmd.extend(args)
        
        if not self.security.is_command_safe(" ".join(cmd)):
            return {"success": False, "error": "Command not allowed"}
        
        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=timeout or self.timeout,
            )
            return {
                "success": result.returncode == 0,
                "stdout": result.stdout.strip(),
                "stderr": result.stderr.strip(),
            }
        except FileNotFoundError:
            return {"success": False, "error": "ADB not found. Install Android platform-tools."}
        except subprocess.TimeoutExpired:
            return {"success": False, "error": "ADB command timed out"}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def list_devices(self) -> Dict[str, Any]:
        """List all connected Android devices."""
        result = self._run_adb(["devices", "-l"])
        if not result["success"]:
            return {"success": False, "error": result.get("error", "Failed to list devices")}
        
        devices = []
        lines = result["stdout"].split("\n")[1:]
        
        for line in lines:
            line = line.strip()
            if not line or "List of devices" in line:
                continue
            
            parts = line.split()
            if len(parts) >= 2:
                devices.append({
                    "id": parts[0],
                    "status": parts[1],
                    "info": " ".join(parts[2:]) if len(parts) > 2 else "",
                })
        
        return {
            "success": True,
            "devices": devices,
            "count": len(devices),
        }
    
    def get_property(self, device_id: str, prop: str) -> Dict[str, Any]:
        """Get a system property from device."""
        result = self._run_adb(
            ["shell", "getprop", prop], device_id
        )
        if result["success"]:
            return {"success": True, "value": result["stdout"]}
        return {"success": False, "error": result.get("error", "Failed to get property")}
    
    def get_battery_info(self, device_id: str) -> Dict[str, Any]:
        """Get battery information."""
        result = self._run_adb(
            ["shell", "dumpsys", "battery"], device_id
        )
        if not result["success"]:
            return {"success": False, "error": result.get("error")}
        
        battery_info = {}
        for line in result["stdout"].split("\n"):
            if ":" in line:
                key, value = line.split(":", 1)
                battery_info[key.strip()] = value.strip()
        
        return {"success": True, "data": battery_info}
    
    def get_storage_info(self, device_id: str) -> Dict[str, Any]:
        """Get storage information."""
        result = self._run_adb(["shell", "df", "-h"], device_id)
        if not result["success"]:
            return {"success": False, "error": result.get("error")}
        
        partitions = []
        lines = result["stdout"].split("\n")[1:]
        for line in lines:
            parts = line.split()
            if len(parts) >= 6:
                partitions.append({
                    "filesystem": parts[0],
                    "size": parts[1],
                    "used": parts[2],
                    "available": parts[3],
                    "use_percent": parts[4],
                    "mount_point": parts[5],
                })
        
        return {"success": True, "data": partitions}
    
    def check_connectivity(self, device_id: str) -> Dict[str, Any]:
        """Check if device is responsive."""
        result = self._run_adb(
            ["shell", "echo", "connected"], device_id, timeout=5
        )
        return {
            "success": result["success"] and "connected" in result.get("stdout", ""),
            "status": "connected" if result["success"] else "disconnected",
        }
    
    def get_logcat(
        self,
        device_id: str,
        lines: int = 100,
        filter_tag: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Get device logcat output."""
        args = ["logcat", "-d", "-t", str(lines)]
        if filter_tag:
            args.extend(["-s", filter_tag])
        
        result = self._run_adb(args, device_id)
        return {
            "success": result["success"],
            "logs": result.get("stdout", ""),
            "error": result.get("error", ""),
        }
    
    def reboot(self, device_id: str, mode: str = "normal") -> Dict[str, Any]:
        """Reboot device to specified mode."""
        valid_modes = {
            "normal": ["reboot"],
            "recovery": ["reboot", "recovery"],
            "bootloader": ["reboot", "bootloader"],
        }
        
        args = valid_modes.get(mode)
        if not args:
            return {"success": False, "error": f"Invalid reboot mode: {mode}"}
        
        return self._run_adb(args, device_id)
    
    def take_screenshot(
        self, device_id: str, output_path: str
    ) -> Dict[str, Any]:
        """Take a screenshot from the device."""
        remote_path = "/sdcard/screenshot_temp.png"
        
        # Take screenshot on device
        result = self._run_adb(
            ["shell", "screencap", "-p", remote_path], device_id
        )
        if not result["success"]:
            return {"success": False, "error": "Failed to take screenshot"}
        
        # Pull to local
        pull_result = self._run_adb(
            ["pull", remote_path, output_path], device_id
        )
        
        # Clean up remote file
        self._run_adb(["shell", "rm", remote_path], device_id)
        
        return {
            "success": pull_result["success"],
            "path": output_path if pull_result["success"] else None,
        }
    
    def install_apk(
        self, device_id: str, apk_path: str, replace: bool = True
    ) -> Dict[str, Any]:
        """Install an APK on the device."""
        if not self.security.is_path_allowed(apk_path):
            return {"success": False, "error": "APK path not allowed"}
        
        args = ["install"]
        if replace:
            args.append("-r")
        args.append(apk_path)
        
        return self._run_adb(args, device_id, timeout=120)
    
    def push_file(
        self, device_id: str, local_path: str, remote_path: str
    ) -> Dict[str, Any]:
        """Push a file to the device."""
        if not self.security.is_path_allowed(local_path):
            return {"success": False, "error": "Local path not allowed"}
        
        return self._run_adb(
            ["push", local_path, remote_path], device_id
        )
    
    def pull_file(
        self, device_id: str, remote_path: str, local_path: str
    ) -> Dict[str, Any]:
        """Pull a file from the device."""
        if not self.security.is_path_allowed(local_path):
            return {"success": False, "error": "Local path not allowed"}
        
        return self._run_adb(
            ["pull", remote_path, local_path], device_id
        )