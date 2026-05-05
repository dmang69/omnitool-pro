"""Path sandboxing, command restriction, and audit logging."""
import logging
import os
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

log = logging.getLogger("ai_toolkit.security")

class SecurityError(Exception):
    """Raised when a sandboxing or permission check fails."""

class SecurityGate:
    def __init__(self, cfg: dict[str, Any]) -> None:
        sec = cfg.get("security", {})
        self._sandboxing: