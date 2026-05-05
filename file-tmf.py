"""Structured JSON response builder used across every tool call."""
import time
from typing import Any

def success(data: Any = None, message: str = "ok", meta: dict[str, Any] | None = None) -> dict[str, Any]:
    envelope: dict[str, Any] = {
        "status": "success",
        "message": message,
        "timestamp": time.time(),
        "data": data,
    }
    if meta:
        envelope["meta"] = meta
    return envelope

def error(message: str, code: str = "UNKNOWN", details: Any = None) -> dict[str, Any]:
    return {
        "status": "error",
        "message": message,
        "error_code": code,
        "timestamp": time.time(),
        "details": details,
    }