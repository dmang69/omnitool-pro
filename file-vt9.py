"""Tests for automation module."""
import pytest
import tempfile
from pathlib import Path
from utils.config import ConfigLoader
from utils.security import SecurityManager
from toolkit.automation import AutomationEngine


@pytest.fixture
def engine():
    config = ConfigLoader("config/default.yaml")
    security = SecurityManager(config)
    return AutomationEngine(security, config)


def test_run_safe_command(engine):
    result = engine.run_command("echo hello")
    assert result["success"] is True
    assert "hello" in result["stdout"]


def test_run_restricted_command(engine):
    result = engine.run_command("rm -rf /")
    assert result["success"] is False


def test_run_script(engine):
    with tempfile.NamedTemporaryFile(
        mode="w", suffix=".py", delete=False
    ) as f:
        f.write("print('script output')")
        path = f.name
    
    result = engine.run_script(path)
    assert result["success"] is True
    assert "script output" in result["stdout"]