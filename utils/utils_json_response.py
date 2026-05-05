"""Standardized JSON response handler."""
from typing import Any, Dict, List, Optional


class JsonResponse:
    """Standardized response format for all toolkit operations."""
    
    @staticmethod
    def success(
        data: Any = None,
        message: str = "Operation successful",
        meta: Optional[Dict] = None
    ) -> Dict[str, Any]:
        response = {
            "success": True,
            "message": message,
            "data": data
        }
        if meta:
            response["meta"] = meta
        return response
    
    @staticmethod
    def error(
        error: str,
        data: Any = None,
        code: Optional[str] = None,
        details: Optional[Dict] = None
    ) -> Dict[str, Any]:
        response = {
            "success": False,
            "error": error,
            "data": data
        }
        if code:
            response["code"] = code
        if details:
            response["details"] = details
        return response
    
    @staticmethod
    def paginated(
        items: List,
        total: int,
        page: int = 1,
        per_page: int = 20
    ) -> Dict[str, Any]:
        return {
            "success": True,
            "data": {
                "items": items,
                "pagination": {
                    "total": total,
                    "page": page,
                    "per_page": per_page,
                    "total_pages": (total + per_page - 1) // per_page
                }
            }
        }