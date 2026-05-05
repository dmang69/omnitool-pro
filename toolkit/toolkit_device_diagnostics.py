"""Device diagnostic operations for Android and iOS."""
import json
from typing import Any, Dict, List, Optional


class DeviceDiagnostics:
    """Cross-platform device diagnostic tools."""
    
    def __init__(self, adb_manager, ios_manager, config):
        self.adb = adb_manager
        self.ios = ios_manager
        self.config = config
    
    def get_device_summary(self, device_id: str, platform: str) -> Dict[str, Any]:
        """Get comprehensive device summary."""
        if platform == "android":
            return self._android_summary(device_id)
        elif platform == "ios":
            return self._ios_summary(device_id)
        return {"success": False, "error": f"Unsupported platform: {platform}"}
    
    def _android_summary(self, device_id: str) -> Dict[str, Any]:
        """Gather Android device summary."""
        info_fields = self.config.get("android.device_info_fields", [])
        device_info = {}
        
        for field in info_fields:
            result = self.adb.get_property(device_id, field)
            if result["success"]:
                device_info[field] = result["value"]
        
        # Get battery info
        battery = self.adb.get_battery_info(device_id)
        
        # Get storage info
        storage = self.adb.get_storage_info(device_id)
        
        return {
            "success": True,
            "platform": "android",
            "device_info": device_info,
            "battery": battery.get("data", {}),
            "storage": storage.get("data", {}),
        }
    
    def _ios_summary(self, device_id: str) -> Dict[str, Any]:
        """Gather iOS device summary."""
        info = self.ios.get_device_info(device_id)
        
        return {
            "success": True,
            "platform": "ios",
            "device_info": info.get("data", {}),
        }
    
    def run_full_diagnostics(
        self, device_id: str, platform: str
    ) -> Dict[str, Any]:
        """Run comprehensive diagnostics."""
        checks = []
        
        # Basic connectivity
        if platform == "android":
            connectivity = self.adb.check_connectivity(device_id)
        else:
            connectivity = self.ios.check_connectivity(device_id)
        
        checks.append({
            "check": "connectivity",
            "passed": connectivity["success"],
            "details": connectivity,
        })
        
        if connectivity["success"]:
            # Battery
            if platform == "android":
                battery = self.adb.get_battery_info(device_id)
            else:
                battery = self.ios.get_battery_info(device_id)
            
            checks.append({
                "check": "battery",
                "passed": battery["success"],
                "details": battery,
            })
            
            # Storage
            if platform == "android":
                storage = self.adb.get_storage_info(device_id)
            else:
                storage = self.ios.get_storage_info(device_id)
            
            checks.append({
                "check": "storage",
                "passed": storage["success"],
                "details": storage,
            })
        
        passed_count = sum(1 for c in checks if c["passed"])
        
        return {
            "success": True,
            "device_id": device_id,
            "platform": platform,
            "checks": checks,
            "summary": {
                "total": len(checks),
                "passed": passed_count,
                "failed": len(checks) - passed_count,
            },
        }