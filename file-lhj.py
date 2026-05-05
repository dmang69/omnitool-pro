"""Tests for filesystem module."""
import pytest
import tempfile
import os
from pathlib import Path
from utils.config import ConfigLoader
from utils.security import SecurityManager
from toolkit.filesystem import FileSystemIntelligence


@pytest.fixture
def fs():
    config = ConfigLoader("config/default.yaml")
    security = SecurityManager(config)
    return FileSystemIntelligence(security, config)


def test_read_file(fs):
    with tempfile.NamedTemporaryFile(
        mode="w", suffix=".txt", delete=False
    ) as f:
        f.write("Hello, World!")
        path = f.name
    
    try:
        result = fs.read_file(path)
        assert result["success"] is True
        assert result["content"] == "Hello, World!"
    finally:
        os.unlink(path)


def test_write_file(fs):
    with tempfile.TemporaryDirectory() as tmpdir:
        path = str(Path(tmpdir) / "test.txt")
        result = fs.write_file(path, "test content")
        assert result["success"] is True
        assert Path(path).exists()


def test_write_no_overwrite(fs):
    with tempfile.TemporaryDirectory() as tmpdir:
        path = str(Path(tmpdir) / "test.txt")
        fs.write_file(path, "first")
        result = fs.write_file(path, "second", overwrite=False)
        assert result["success"] is False


def test_list_directory(fs):
    with tempfile.TemporaryDirectory() as tmpdir:
        (Path(tmpdir) / "file.txt").touch()
        (Path(tmpdir) / "subdir").mkdir()
        result = fs.list_directory(tmpdir)
        assert result["success"] is True
        assert result["count"] == 2


def test_read_nonexistent(fs):
    result = fs.read_file("/nonexistent/path/file.txt")
    assert result["success"] is False


def test_search_codebase(fs):
    with tempfile.TemporaryDirectory() as tmpdir:
        (Path(tmpdir) / "test.py").write_text("def hello():\n    pass")
        result = fs.search_codebase(tmpdir, "hello", [".py"])
        assert result["success"] is True
        assert result["total_matches"] >= 1