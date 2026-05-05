"""iOS device management using libimobiledevice."""
import subprocess
from typing import Any, Dict, List, Optional


class IOSManager:
    """Manage iOS devices using libimobiledevice tools."""
    
    def __init__(self, security_manager, config):
        self.security = security_manager
        self.config = config
        self.ideviceinfo = config.get("ios.ideviceinfo_path", "ideviceinfo")
        self.idevice_id = config.get("ios.idevice_id_path", "idevice_id")
        self.idevicebackup = config.get(
            "ios.idevicebackup_path", "idevicebackup2"
        )
        self.timeout = config.get("ios.default_timeout", 30)
    
    def _run_command(
        self, cmd: List[str], timeout: Optional[int] = None
    ) -> Dict[str, Any]:
        """Run a command safely."""
        cmd_str = " ".join(cmd)
        if not self.security.is_command_safe(cmd_str):
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
            return {
                "success": False,
                "error": "libimobiledevice tools not found. Install via: brew install libimobiledevice",
            }
        except subprocess.TimeoutExpired:
            return {"success": False, "error": "Command timed out"}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def list_devices(self) -> Dict[str, Any]:
        """List all connected iOS devices."""
        result = self._run_command([self.idevice_id, "-l"])
        if not result["success"]:
            return {
                "success": False,
                "error": result.get("error", "Failed to list devices"),
            }
        
        devices = []
        for line in result["stdout"].split("\n"):
            device_id = line.strip()
            if device_id:
                info = self.get_device_info(device_id)
                devices.append({
                    "id": device_id,
                    "status": "connected",
                    "info": info.get("data", {}),
                })
        
        return {"success": True, "devices": devices, "count": len(devices)}
    
    def get_device_info(self, device_id: str) -> Dict[str, Any]:
        """Get iOS device information."""
        result = self._run_command(
            [self.ideviceinfo, "-u", device_id]
        )
        if not result["success"]:
            return {"success": False, "error": result.get("error")}
        
        info = {}
        for line in result["stdout"].split("\n"):
            if ":" in line:
                key, value = line.split(":", 1)
                info[key.strip()] = value.strip()
        
        return {"success": True, "data": info}
    
    def check_connectivity(self, device_id: str) -> Dict[str, Any]:
        """Check if iOS device is responsive."""
        result = self._run_command(
            [self.ideviceinfo, "-u", device_id, "-k", "ProductType"],
            timeout=5,
        )
        return {
            "success": result["success"],
            "status": "connected" if result["success"] else "disconnected",
        }
    
    def get_battery_info(self, device_id: str) -> Dict[str, Any]:
        """Get iOS battery information."""
        result = self._run_command(
            [self.ideviceinfo, "-u", device_id, "-q", "com.apple.mobile.battery"]
        )
        if not result["success"]:
            return {"success": False, "error": result.get("error")}
        
        info = {}
        for line in result["stdout"].split("\n"):
            if "=" in line:
                key, value = line.split("=", 1)
                info[key.strip()] = value.strip()
        
        return {"success": True, "data": info}
    
    def get_storage_info(self, device_id: str) -> Dict[str, Any]:
        """Get iOS storage information."""
        result = self._run_command(
            [self.ideviceinfo, "-u", device_id, "-q", "com.apple.disk_usage"]
        )
        if not result["success"]:
            return {"success": False, "error": result.get("error")}
        
        info = {}
        for line in result["stdout"].split("\n"):
            if "=" in line:
                key, value = line.split("=", 1)
                info[key.strip()] = value.strip()
        
        return {"success": True, "data": info}
    
    def create_backup(
        self, device_id: str, backup_path: str
    ) -> Dict[str, Any]:
        """Create a backup of the iOS device."""
        result = self._run_command(
            [self.idevicebackup, "backup", "--full", device_id],
            timeout=3600,
        )
        return {
            "success": result["success"],
            "path": backup_path,
            "error": result.get("error", ""),
        }