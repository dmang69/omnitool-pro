"""
Example Plugin for AI Developer Toolkit

This demonstrates how to create a plugin that adds new tools.
"""
from typing import Any, Dict


def analyze_performance(filepath: str) -> Dict[str, Any]:
    """Example: Analyze code performance metrics."""
    from pathlib import Path
    
    try:
        code = Path(filepath).read_text(encoding="utf-8")
        lines = code.split("\n")
        
        return {
            "success": True,
            "metrics": {
                "total_lines": len(lines),
                "blank_lines": sum(1 for l in lines if not l.strip()),
                "comment_lines": sum(
                    1 for l in lines if l.strip().startswith("#")
                ),
                "code_lines": sum(
                    1 for l in lines
                    if l.strip() and not l.strip().startswith("#")
                ),
            },
        }
    except Exception as e:
        return {"success": False, "error": str(e)}


def register(tool_interface):
    """Register plugin tools with the tool interface."""
    tool_interface.analyze_performance = analyze_performance
    print("Example plugin registered successfully")
    return True


METADATA = {
    "name": "example_plugin",
    "version": "1.0.0",
    "description": "Example plugin demonstrating plugin architecture",
    "author": "AI Toolkit",
}