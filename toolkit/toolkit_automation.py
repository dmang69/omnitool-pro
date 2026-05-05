"""Script execution and automation capabilities."""
import subprocess
import sys
import shlex
import platform
from pathlib import Path
from typing import Any, Dict, List, Optional


class AutomationEngine:
    """Execute scripts and automate tasks safely."""
    
    def __init__(self, security_manager, config):
        self.security = security_manager
        self.config = config
        self.is_windows = platform.system() == "Windows"
    
    def run_command(
        self,
        command: str,
        cwd: Optional[str] = None,
        timeout: int = 300,
        env: Optional[Dict[str, str]] = None,
    ) -> Dict[str, Any]:
        """Run a shell command safely."""
        if not self.security.is_command_safe(command):
            return {
                "success": False,
                "error": "Command contains restricted patterns",
            }
        
        if cwd and not self.security.is_path_allowed(cwd):
            return {"success": False, "error": "Working directory not allowed"}
        
        try:
            # Parse command for safety
            if self.is_windows:
                cmd_list = command
                shell = True
            else:
                cmd_list = shlex.split(command)
                shell = False
            
            result = subprocess.run(
                cmd_list,
                capture_output=True,
                text=True,
                timeout=timeout,
                cwd=cwd,
                shell=shell,
                env=env,
            )
            
            return {
                "success": result.returncode == 0,
                "stdout": result.stdout,
                "stderr": result.stderr,
                "return_code": result.returncode,
            }
        
        except subprocess.TimeoutExpired:
            return {
                "success": False,
                "error": f"Command timed out after {timeout} seconds",
            }
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def run_script(
        self,
        script_path: str,
        args: Optional[List[str]] = None,
        timeout: int = 300,
    ) -> Dict[str, Any]:
        """Run a Python script in a controlled environment."""
        if not self.security.is_path_allowed(script_path):
            return {"success": False, "error": "Script path not allowed"}
        
        file_path = Path(script_path)
        if not file_path.exists():
            return {"success": False, "error": "Script not found"}
        
        cmd = [sys.executable, str(file_path)]
        if args:
            cmd.extend(args)
        
        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=timeout,
                cwd=str(file_path.parent),
            )
            
            return {
                "success": result.returncode == 0,
                "stdout": result.stdout,
                "stderr": result.stderr,
                "return_code": result.returncode,
            }
        
        except subprocess.TimeoutExpired:
            return {
                "success": False,
                "error": f"Script timed out after {timeout} seconds",
            }
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def install_package(
        self, package_name: str, upgrade: bool = False
    ) -> Dict[str, Any]:
        """Install a Python package using pip."""
        if not package_name or not isinstance(package_name, str):
            return {"success": False, "error": "Invalid package name"}
        
        dangerous_chars = set(";&|`$(){}[]")
        if any(c in package_name for c in dangerous_chars):
            return {
                "success": False,
                "error": "Package name contains invalid characters",
            }
        
        cmd = [sys.executable, "-m", "pip", "install"]
        if upgrade:
            cmd.append("--upgrade")
        cmd.append(package_name)
        
        try:
            result = subprocess.run(
                cmd, capture_output=True, text=True, timeout=300
            )
            return {
                "success": result.returncode == 0,
                "stdout": result.stdout,
                "stderr": result.stderr,
            }
        
        except subprocess.TimeoutExpired:
            return {
                "success": False,
                "error": "Installation timed out after 300 seconds",
            }
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def create_virtual_environment(
        self, env_path: str
    ) -> Dict[str, Any]:
        """Create a Python virtual environment."""
        if not self.security.is_path_allowed(env_path):
            return {"success": False, "error": "Path not allowed"}
        
        try:
            cmd = [sys.executable, "-m", "venv", env_path]
            result = subprocess.run(
                cmd, capture_output=True, text=True, timeout=120
            )
            
            return {
                "success": result.returncode == 0,
                "path": env_path,
                "error": result.stderr if result.returncode != 0 else "",
            }
        
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def run_batch_commands(
        self, commands: List[str], stop_on_failure: bool = True
    ) -> Dict[str, Any]:
        """Run a sequence of commands."""
        results = []
        
        for i, cmd in enumerate(commands):
            result = self.run_command(cmd)
            results.append({
                "command": cmd,
                "index": i,
                "success": result["success"],
            })
            
            if not result["success"] and stop_on_failure:
                return {
                    "success": False,
                    "error": f"Command {i} failed: {result.get('error', 'Unknown error')}",
                    "results": results,
                }
        
        return {
            "success": all(r["success"] for r in results),
            "results": results,
        }