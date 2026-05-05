from datetime import datetime, timezone
from typing import Any
from utils.logger import setup_logger

logger = setup_logger()

def success(data: Any = None, message: str = "Operation completed successfully", meta: dict[str, Any] | None = None) -> dict[str, Any]:
    envelope = {
        "status": "success",
        "message": message,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "data": data,
    }
    if meta:
        envelope["meta"] = meta
    logger.debug(f"✅ {message}")
    return envelope

def error(message: str, code: str = "UNKNOWN_ERROR", details: Any = None) -> dict[str, Any]:
    envelope = {
        "status": "error",
        "message": message,
        "error_code": code,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "details": details,
    }
    logger.warning(f"❌ [{code}] {message}")
    return envelope