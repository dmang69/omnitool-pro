"""Code Understanding — AST parsing, dependency mapping, summaries, docstrings."""

from __future__ import annotations

import ast
import logging
import textwrap
from pathlib import Path
from typing import Any

from utils.json_response import error, success

log = logging.getLogger("ai_toolkit.code_understanding")


class CodeUnderstanding:
    """Parse Python source into structured intelligence."""

    def __init__(self, cfg: dict[str, Any]) -> None:
        cu = cfg.get("code_understanding", {})
        self._supported: set[str] = set(cu.get("supported_extensions", [".py"]))
        self._max_lines: int = cu.get("max_lines_for_summary", 5000)
        self._docstyle: str = cu.get("docstring_style", "google")

    # -- AST parse -------------------------------------------------------------

    def parse_file(self, path: str | Path) -> dict[str, Any]:
        """Parse a Python file and return structured AST data."""
        p = Path(path)
        if not p.exists():
            return error(f"File not found: {p}", "NOT_FOUND")
        if p.suffix not in self._supported:
            return error(f"Unsupported extension: {p.suffix}", "UNSUPPORTED")
        try:
            source = p.read_text(encoding="utf-8")
            tree = ast.parse(source, filename=str(p))
        except SyntaxError as exc:
            return error(f"Syntax error: {exc}", "SYNTAX_ERROR")

        functions: list[dict[str, Any]] = []
        classes: list[dict[str, Any]] = []
        imports: list[str] = []

        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef):
                functions.append(self._extract_func(node, source))
            elif isinstance(node, ast.ClassDef):
                classes.append(self._extract_class(node, source))
            elif isinstance(node, ast.Import):
                for alias in node.names:
                    imports.append(alias.name)
            elif isinstance(node, ast.ImportFrom):
                module = node.module or ""
                for alias in node.names:
                    imports.append(f"{module}.{alias.name}")

        return success({
            "file": str(p),
            "lines": len(source.splitlines()),
            "functions": functions,
            "classes": classes,
            "imports": sorted(set(imports)),
        })

    def _extract_func(self, node: ast.FunctionDef | ast.AsyncFunctionDef, source: str) -> dict[str, Any]:
        args = [a.arg for a in node.args.args]
        return_ann = ast.get_source_segment(source, node.returns) if node.returns else None
        return {
            "name": node.name,
            "line": node.lineno,
            "args": args,
            "returns": return_ann,
            "docstring": ast.get_docstring(node) or "",
            "is_async": isinstance(node, ast.AsyncFunctionDef),
            "decorators": [ast.dump(d) for d in node.decorator_list],
        }

    def _extract_class(self, node: ast.ClassDef, source: str) -> dict[str, Any]:
        methods = []
        for item in node.body:
            if isinstance(item, ast.FunctionDef | ast.AsyncFunctionDef):
                methods.append(self._extract_func(item, source))
        bases = [ast.get_source_segment(source, b) or ast.dump(b) for b in node.bases]
        return {
            "name": node.name,
            "line": node.lineno,
            "bases": bases,
            "docstring": ast.get_docstring(node) or "",
            "methods": methods,
        }

    # -- dependency map --------------------------------------------------------

    def dependency_map(self, root: str | Path) -> dict[str, Any]:
        """Walk a directory and map every Python file to its imports."""
        base = Path(root).resolve()
        mapping: dict[str, list[str]] = {}
        for py in base.rglob("*.py"):
            result = self.parse_file(py)
            if result["status"] == "success":
                mapping[str(py.relative_to(base))] = result["data"]["imports"]
        return success(mapping, f"{len(mapping)} files mapped")

    # -- summarize -------------------------------------------------------------

    def summarize(self, path: str | Path) -> dict[str, Any]:
        """Produce a human-readable summary of a module."""
        result = self.parse_file(path)
        if result["status"] != "success":
            return result
        d = result["data"]
        parts: list[str] = [f"## Module: {d['file']}  ({d['lines']} lines)\n"]

        if d["imports"]:
            parts.append("### Imports")
            for imp in d["imports"]:
                parts.append(f"  - {imp}")

        for cls in d["classes"]:
            parts.append(f"\n### Class `{cls['name']}` (line {cls['line']})")
            if cls["docstring"]:
                parts.append(f"  {cls['docstring'][:200]}")
            for m in cls["methods"]:
                sig = f"({', '.join(m['args'])})"
                parts.append(f"  - `{m['name']}{sig}`")

        for fn in d["functions"]:
            sig = f"({', '.join(fn['args'])})"
            parts.append(f"\n### Function `{fn['name']}{sig}` (line {fn['line']})")
            if fn["docstring"]:
                parts.append(f"  {fn['docstring'][:200]}")

        summary_text = "\n".join(parts)
        return success({"summary": summary_text})

    # -- docstring generation --------------------------------------------------

    def generate_docstrings(self, path: str | Path) -> dict[str, Any]:
        """Generate stub docstrings for undocumented functions/classes."""
        result = self.parse_file(path)
        if result["status"] != "success":
            return result
        d = result["data"]
        stubs: list[dict[str, str]] = []

        for fn in d["functions"]:
            if not fn["docstring"]:
                stubs.append({
                    "name": fn["name"],
                    "line": fn["line"],
                    "stub": self._make_docstring(fn),
                })
        for cls in d["classes"]:
            if not cls["docstring"]:
                stubs.append({
                    "name": cls["name"],
                    "line": cls["line"],
                    "stub": f'"""{cls["name"]} class.\n\nTODO: describe purpose.\n"""',
                })
            for m in cls["methods"]:
                if not m["docstring"]:
                    stubs.append({
                        "name": f"{cls['name']}.{m['name']}",
                        "line": m["line"],