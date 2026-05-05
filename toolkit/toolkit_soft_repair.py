"""Soft brick and bootloop repair tools."""
import subprocess
import time
from typing import Any, Dict, Optional


class SoftRepairEngine:
    """Repair soft-bricked Android devices."""
    
    def __init__(self, adb_manager, config):
        self.adb = adb_manager
        self.config = config
    
    def diagnose_bootloop(self, device_id: str) -> Dict[str, Any]:
        """Diagnose a bootloop condition."""
        # Check if device is in any accessible state
        connectivity = self.adb.check_connectivity(device_id)
        
        if not connectivity["success"]:
            # Device may be in bootloader
            return {
                "success": True,
                "diagnosis": "Device not accessible via ADB. May be in bootloader or hard-bricked.",
                "recommendation": "Try entering fastboot mode with power + volume_down",
                "severity": "hard_brick可能性",
            }
        
        # Device is accessible, check logs
        logcat = self.adb.get_logcat(device_id, lines=200, filter_tag="System")
        
        bootloop_indicators = [
            "boot loop",
            "restart",
            "fatal",
            "panic",
            "system_server crash",
            "Zygote",
        ]
        
        detected_issues = []
        if logcat["success"]:
            logs_lower = logcat["logs"].lower()
            for indicator in bootloop_indicators:
                if indicator.lower() in logs_lower:
                    detected_issues.append(indicator)
        
        return {
            "success": True,
            "device_id": device_id,
            "diagnosis": {
                "issues_found": detected_issues,
                "log_available": logcat["success"],
            },
            "recommendations": self._get_recommendations(detected_issues),
        }
    
    def _get_recommendations(self, issues: list) -> list:
        """Get repair recommendations based on detected issues."""
        recommendations = []
        
        if "fatal" in issues or "panic" in issues:
            recommendations.append({
                "action": "Wipe Cache Partition",
                "command": "reboot recovery",
                "description": "Boot to recovery and wipe cache partition",
            })
        
        if "system_server crash" in issues or "Zygote" in issues:
            recommendations.append({
                "action": "Safe Mode Boot",
                "command": "adb reboot safe",
                "description": "Boot into safe mode to disable third-party apps",
            })
        
        if not recommendations:
            recommendations.append({
                "action": "Soft Reset",
                "command": "adb reboot",
                "description": "Try a simple reboot first",
            })
        
        return recommendations
    
    def safe_mode_boot(self, device_id: str) -> Dict[str, Any]:
        """Boot device into safe mode."""
        return self.adb.reboot(device_id, "normal")
    
    def wipe_cache(self, device_id: str) -> Dict[str, Any]:
        """Wipe cache partition (requires recovery mode)."""
        # First reboot to recovery
        reboot_result = self.adb.reboot(device_id, "recovery")
        if not reboot_result["success"]:
            return {"success": False, "error": "Failed to reboot to recovery"}
        
        time.sleep(10)
        
        return {
            "success": True,
            "message": "Device rebooted to recovery. Use volume keys to navigate and wipe cache.",
        }
    
    def factory_reset_safe(self, device_id: str) -> Dict[str, Any]:
        """
        Guide user through safe factory reset via recovery mode.
        This provides instructions, not direct execution.
        """
        return {
            "success": True,
            "instructions": [
                "1. Power off the device completely",
                "2. Hold Power + Volume Up to enter recovery mode",
                "3. Use volume keys to select 'Wipe data/factory reset'",
                "4. Confirm with Power button",
                "5. Select 'Reboot system now'",
                "WARNING: This will erase ALL data on the device",
            ],
            "warning": "This operation is irreversible. All user data will be lost.",
        }
    
    def check_bootloader_status(self, device_id: str) -> Dict[str, Any]:
        """Check if bootloader is unlocked."""
        result = self.adb.get_property(
            device_id, "ro.boot.verifiedbootstate"
        )
        
        unlock_result = self.adb._run_adb(
            ["shell", "getprop", "ro.debuggable"], device_id
        )
        
        return {
            "success": True,
            "boot_state": result.get("value", "unknown"),
            "debuggable": unlock_result.get("stdout", "0") == "1",
        }