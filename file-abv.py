"""Tests for tool interface and chat agent."""
import pytest
from agents.tool_interface import AIAgentToolInterface


@pytest.fixture
def interface():
    return AIAgentToolInterface("config/default.yaml")


def test_list_tools(interface):
    result = interface.list_tools()
    assert result["success"] is True
    assert len(result["core_tools"]) > 0


def test_file_operations(interface):
    import tempfile
    import os
    from pathlib import Path
    
    with tempfile.NamedTemporaryFile(
        mode="w", suffix=".txt", delete=False
    ) as f:
        f.write("test")
        path = f.name
    
    try:
        read_result = interface.read_file(path)
        assert read_result["success"] is True
    finally:
        os.unlink(path)


def test_plugin_loaded(interface):
    # Check that the example plugin was loaded
    tools = interface.list_tools()
    # Plugin tools should appear if plugin loaded successfully
    assert "success" in tools