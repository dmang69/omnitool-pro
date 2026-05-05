"""Security controls for toolkit operations."""
import re
from pathlib import Path
from typing import List, Optional


class SecurityManager:
    """Enforces security policies for file and command operations."""
    
    def __init__(self, config):
        self.config = config
        self.restricted_commands = config.get(
            "security.restricted_commands", []
        )
        self.allowed_paths = config.get("security.allowed_paths", [])
        self.sandbox_enabled = config.get("toolkit.sandbox_enabled", True)
        self.allowed_extensions = config.get(
            "toolkit.allowed_extensions", []
        )
    
    def is_path_allowed(self, path: str) -> bool:
        """Check if a path is within allowed boundaries."""
        if not self.sandbox_enabled:
            return True
        
        try:
            resolved = Path(path).resolve()
        except (OSError, ValueError):
            return False
        
        if not self.allowed_paths:
            cwd = Path.cwd().resolve()
            return (
                resolved == cwd
                or cwd in resolved.parents
                or str(resolved).startswith(str(cwd))
            )
        
        for allowed in self.allowed_paths:
            allowed_resolved = Path(allowed).resolve()
            if str(resolved).startswith(str(allowed_resolved)):
                return True
        
        return False
    
    def is_command_safe(self, command: str) -> bool:
        """Check if a command contains restricted patterns."""
        command_lower = command.lower()
        for restricted in self.restricted_commands:
            if restricted.lower() in command_lower:
                return False
        return True
    
    def validate_extension(self, filepath: str) -> bool:
        """Validate file extension against allowed list."""
        if not self.allowed_extensions:
            return True
        
        ext = Path(filepath).suffix.lower()
        return ext in self.allowed_extensions
    
    def sanitize_filename(self, filename: str) -> str:
        """Remove potentially dangerous characters from filename."""
        # Remove path traversal attempts
        sanitized = filename.replace("..", "").replace("/", "").replace("\\", "")
        # Remove null bytes and other control characters
        sanitized = re.sub(r'[\x00-\x1f\x7f]', '', sanitized)
        return sanitized.strip()
    
    def is_path_within_directory(self, path: str, directory: str) -> bool:
        """Check if a path is within a specific directory."""
        try:
            resolved_path = Path(path).resolve()
            resolved_dir = Path(directory).resolve()
            return (
                str(resolved_path).startswith(str(resolved_dir))
            )
        except (OSError, ValueError):
            return False