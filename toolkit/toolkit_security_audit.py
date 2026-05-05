"""Security audit tools for devices and systems."""
from typing import Any, Dict, List


class SecurityAudit:
    """Perform security audits on devices and systems."""
    
    def __init__(self, adb_manager, ios_manager, config):
        self.adb = adb_manager
        self.ios = ios_manager
        self.config = config
    
    def audit_android_security(self, device_id: str) -> Dict[str, Any]:
        """Perform a security audit on an Android device."""
        checks = []
        
        # Check if device is encrypted
        encryption = self.adb.get_property(
            device_id, "ro.crypto.state"
        )
        checks.append({
            "check": "encryption",
            "passed": encryption.get("value") == "encrypted",
            "value": encryption.get("value", "unknown"),
            "recommendation": "Enable full disk encryption for data protection",
        })
        
        # Check SELinux status
        selinux = self.adb._run_adb(
            ["shell", "getenforce"], device_id
        )
        selinux_status = selinux.get("stdout", "Unknown")
        checks.append({
            "check": "selinux",
            "passed": selinux_status == "Enforcing",
            "value": selinux_status,
            "recommendation": "SELinux should be in Enforcing mode",
        })
        
        # Check if USB debugging is enabled
        usb_debug = self.adb.get_property(
            device_id, "persist.sys.usb.config"
        )
        checks.append({
            "check": "usb_debugging",
            "passed": "adb" not in usb_debug.get("value", "").lower(),
            "value": usb_debug.get("value", "unknown"),
            "recommendation": "Disable USB debugging when not in use",
        })
        
        # Check unknown sources
        unknown_sources = self.adb._run_adb(
            ["shell", "settings", "get", "secure", "install_non_market_apps"],
            device_id,
        )
        checks.append({
            "check": "unknown_sources",
            "passed": unknown_sources.get("stdout", "1") == "0",
            "value": unknown_sources.get("stdout", "unknown"),
            "recommendation": "Disable installation from unknown sources",
        })
        
        passed = sum(1 for c in checks if c["passed"])
        
        return {
            "success": True,
            "device_id": device_id,
            "checks": checks,
            "summary": {
                "total": len(checks),
                "passed": passed,
                "failed": len(checks) - passed,
                "score": round(passed / len(checks) * 100, 1) if checks else 0,
            },
        }
    
    def audit_ios_security(self, device_id: str) -> Dict[str, Any]:
        """Perform a security audit on an iOS device."""
        checks = []
        
        info = self.ios.get_device_info(device_id)
        device_info = info.get("data", {})
        
        # Check if jailbroken (basic check)
        is_jailbroken = device_info.get("ProductType", "").endswith("jb")
        checks.append({
            "check": "jailbreak_status",
            "passed": not is_jailbroken,
            "value": "jailbroken" if is_jailbroken else "stock",
            "recommendation": "Running stock iOS is recommended for security",
        })
        
        return {
            "success": True,
            "device_id": device_id,
            "checks": checks,
            "summary": {
                "total": len(checks),
                "passed": sum(1 for c in checks if c["passed"]),
            },
        }