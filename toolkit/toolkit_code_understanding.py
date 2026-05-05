"""Code analysis and understanding capabilities."""
import ast
import json
from pathlib import Path
from typing import Any, Dict, List, Optional


class CodeUnderstanding:
    """Analyze and understand Python code structure."""
    
    def parse_ast(self, code: str) -> Dict[str, Any]:
        """Parse code into an AST summary."""
        try:
            tree = ast.parse(code)
            return {
                "success": True,
                "ast_dump": ast.dump(tree, annotate_fields=True),
            }
        except SyntaxError as e:
            return {
                "success": False,
                "error": f"Syntax error: line {e.lineno}: {e.msg}",
            }
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def summarize_module(self, filepath: str) -> Dict[str, Any]:
        """Generate a comprehensive module summary."""
        try:
            file_path = Path(filepath)
            if not file_path.exists():
                return {"success": False, "error": "File not found"}
            
            code = file_path.read_text(encoding="utf-8")
            tree = ast.parse(code)
            
            summary = {
                "filename": file_path.name,
                "total_lines": len(code.split("\n")),
                "total_bytes": len(code.encode("utf-8")),
                "functions": [],
                "classes": [],
                "imports": [],
                "global_variables": [],
            }
            
            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef):
                    summary["functions"].append({
                        "name": node.name,
                        "line": node.lineno,
                        "args": [a.arg for a in node.args.args],
                        "docstring": ast.get_docstring(node) or "",
                        "decorators": [
                            ast.dump(d) for d in node.decorator_list
                        ],
                    })
                
                elif isinstance(node, ast.ClassDef):
                    methods = [
                        n.name
                        for n in node.body
                        if isinstance(n, ast.FunctionDef)
                    ]
                    summary["classes"].append({
                        "name": node.name,
                        "line": node.lineno,
                        "docstring": ast.get_docstring(node) or "",
                        "methods": methods,
                        "bases": [ast.dump(b) for b in node.bases],
                    })
                
                elif isinstance(node, ast.Import):
                    for alias in node.names:
                        summary["imports"].append({
                            "module": alias.name,
                            "alias": alias.asname,
                            "type": "import",
                        })
                
                elif isinstance(node, ast.ImportFrom):
                    for alias in node.names:
                        summary["imports"].append({
                            "module": node.module or "",
                            "name": alias.name,
                            "alias": alias.asname,
                            "type": "from_import",
                        })
                
                elif isinstance(node, ast.Assign):
                    for target in node.targets:
                        if isinstance(target, ast.Name):
                            summary["global_variables"].append(
                                target.id
                            )
            
            return {"success": True, "summary": summary}
        
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def extract_functions(self, filepath: str) -> Dict[str, Any]:
        """Extract all function signatures from a file."""
        try:
            code = Path(filepath).read_text(encoding="utf-8")
            tree = ast.parse(code)
            
            functions = []
            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef):
                    functions.append({
                        "name": node.name,
                        "args": [a.arg for a in node.args.args],
                        "defaults": [
                            ast.dump(d) for d in node.args.defaults
                        ],
                        "line": node.lineno,
                        "docstring": ast.get_docstring(node) or "",
                    })
            
            return {"success": True, "functions": functions}
        
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def generate_tests(self, filepath: str) -> Dict[str, Any]:
        """Generate test scaffolding for a module."""
        try:
            summary_result = self.summarize_module(filepath)
            if not summary_result["success"]:
                return summary_result
            
            summary = summary_result["summary"]
            module_name = Path(filepath).stem
            
            test_code = f'"""\nAuto-generated tests for {module_name}\n"""\nimport pytest\nimport sys\nfrom pathlib import Path\n\nsys.path.insert(0, str(Path(__file__).parent.parent))\n\nimport {module_name}\n\n'
            
            for func in summary["functions"]:
                args = func["args"]
                # Skip 'self' argument for methods
                test_args = ", ".join(
                    [f'"{a}_test_value"' for a in args if a != "self"]
                )
                test_code += f"\ndef test_{func['name']}():\n"
                test_code += f'    """Test {func['name']}."""\n'
                if test_args:
                    test_code += f"    result = {module_name}.{func['name']}({test_args})\n"
                else:
                    test_code += f"    result = {module_name}.{func['name']}()\n"
                test_code += "    assert result is not None\n\n"
            
            for cls in summary["classes"]:
                test_code += f"\nclass Test{cls['name']}:\n"
                test_code += f'    """Tests for {cls["name"]}."""\n\n'
                
                if "__init__" in cls["methods"]:
                    test_code += "    def setup_method(self):\n"
                    test_code += f"        self.instance = {module_name}.{cls['name']}()\n\n"
                
                for method in cls["methods"]:
                    if method.startswith("_"):
                        continue
                    test_code += f"    def test_{method}(self):\n"
                    test_code += f'        """Test {cls["name"]}.{method}."""\n'
                    test_code += f"        result = self.instance.{method}()\n"
                    test_code += "        assert result is not None\n\n"
            
            return {"success": True, "tests": test_code}
        
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def calculate_complexity(self, filepath: str) -> Dict[str, Any]:
        """Calculate basic code complexity metrics."""
        try:
            code = Path(filepath).read_text(encoding="utf-8")
            tree = ast.parse(code)
            
            metrics = {
                "total_functions": 0,
                "total_classes": 0,
                "total_imports": 0,
                "max_depth": 0,
                "total_lines": len(code.split("\n")),
            }
            
            def count_depth(node, depth=0):
                max_d = depth
                for child in ast.iter_child_nodes(node):
                    child_d = count_depth(child, depth + 1)
                    max_d = max(max_d, child_d)
                return max_d
            
            metrics["max_depth"] = count_depth(tree)
            
            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef):
                    metrics["total_functions"] += 1
                elif isinstance(node, ast.ClassDef):
                    metrics["total_classes"] += 1
                elif isinstance(node, (ast.Import, ast.ImportFrom)):
                    metrics["total_imports"] += 1
            
            # Simple complexity: functions per 100 lines
            if metrics["total_lines"] > 0:
                metrics["complexity_ratio"] = round(
                    metrics["total_functions"] / metrics["total_lines"] * 100,
                    2,
                )
            else:
                metrics["complexity_ratio"] = 0
            
            return {"success": True, "metrics": metrics}
        
        except Exception as e:
            return {"success": False, "error": str(e)}