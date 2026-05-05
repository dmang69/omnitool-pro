"""Tests for code understanding module."""
import pytest
import tempfile
from pathlib import Path
from toolkit.code_understanding import CodeUnderstanding


@pytest.fixture
def cu():
    return CodeUnderstanding()


def test_parse_valid_code(cu):
    result = cu.parse_ast("def foo(): pass")
    assert result["success"] is True


def test_parse_invalid_code(cu):
    result = cu.parse_ast("def foo(:")
    assert result["success"] is False


def test_summarize_module(cu):
    with tempfile.NamedTemporaryFile(
        mode="w", suffix=".py", delete=False
    ) as f:
        f.write('"""\nTest module\n"""\nimport os\n\ndef hello():\n    """Say hello."""\n    pass\n\nclass MyClass:\n    def method(self):\n        pass\n')
        path = f.name
    
    result = cu.summarize_module(path)
    assert result["success"] is True
    assert len(result["summary"]["functions"]) >= 1
    assert len(result["summary"]["classes"]) >= 1


def test_generate_tests(cu):
    with tempfile.NamedTemporaryFile(
        mode="w", suffix=".py", delete=False
    ) as f:
        f.write("def add(a, b):\n    return a + b\n")
        path = f.name
    
    result = cu.generate_tests(path)
    assert result["success"] is True
    assert "def test_add" in result["tests"]


def test_calculate_complexity(cu):
    with tempfile.NamedTemporaryFile(
        mode="w", suffix=".py", delete=False
    ) as f:
        f.write("def a(): pass\ndef b(): pass\ndef c(): pass\n")
        path = f.name
    
    result = cu.calculate_complexity(path)
    assert result["success"] is True
    assert result["metrics"]["total_functions"] == 3