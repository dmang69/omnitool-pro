"""Advanced file system operations with safety controls."""
import json
import os
from pathlib import Path
from typing import Any, Dict, List, Optional, Union


class FileSystemIntelligence:
    """Safe, intelligent file system operations."""
    
    def __init__(self, security_manager, config):
        self.security = security_manager
        self.config = config
        self.max_file_size = (
            config.get("toolkit.max_file_size_mb", 50) * 1024 * 1024
        )
    
    def read_file(self, filepath: str) -> Dict[str, Any]:
        """Safely read a file with validation."""
        if not self.security.is_path_allowed(filepath):
            return {"success": False, "error": "Path not allowed"}
        
        if not self.security.validate_extension(filepath):
            return {"success": False, "error": "File extension not allowed"}
        
        file_path = Path(filepath)
        if not file_path.exists():
            return {"success": False, "error": "File not found"}
        
        if file_path.stat().st_size > self.max_file_size:
            return {"success": False, "error": "File too large"}
        
        try:
            content = file_path.read_text(encoding="utf-8")
            return {
                "success": True,
                "content": content,
                "size": file_path.stat().st_size,
                "path": str(file_path.resolve()),
            }
        except UnicodeDecodeError:
            return {"success": False, "error": "File is not valid UTF-8 text"}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def write_file(
        self, filepath: str, content: str, overwrite: bool = False
    ) -> Dict[str, Any]:
        """Safely write to a file."""
        if not self.security.is_path_allowed(filepath):
            return {"success": False, "error": "Path not allowed"}
        
        if not self.security.validate_extension(filepath):
            return {"success": False, "error": "File extension not allowed"}
        
        file_path = Path(filepath)
        
        if file_path.exists() and not overwrite:
            return {"success": False, "error": "File exists. Use overwrite=True"}
        
        try:
            file_path.parent.mkdir(parents=True, exist_ok=True)
            file_path.write_text(content, encoding="utf-8")
            return {
                "success": True,
                "path": str(file_path.resolve()),
                "size": file_path.stat().st_size,
            }
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def list_directory(
        self, dir_path: str = ".", pattern: str = "*"
    ) -> Dict[str, Any]:
        """List directory contents with metadata."""
        if not self.security.is_path_allowed(dir_path):
            return {"success": False, "error": "Path not allowed"}
        
        target = Path(dir_path)
        if not target.exists() or not target.is_dir():
            return {"success": False, "error": "Directory not found"}
        
        try:
            items = []
            for item in target.glob(pattern):
                stat = item.stat()
                items.append({
                    "name": item.name,
                    "path": str(item),
                    "type": "directory" if item.is_dir() else "file",
                    "size": stat.st_size if item.is_file() else 0,
                    "extension": item.suffix if item.is_file() else "",
                })
            
            items.sort(key=lambda x: (x["type"] != "directory", x["name"]))
            
            return {
                "success": True,
                "items": items,
                "count": len(items),
                "path": str(target.resolve()),
            }
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def search_codebase(
        self,
        root_path: str,
        query: str,
        file_extensions: Optional[List[str]] = None,
    ) -> Dict[str, Any]:
        """Search for patterns in codebase."""
        if not self.security.is_path_allowed(root_path):
            return {"success": False, "error": "Root path not allowed"}
        
        if file_extensions is None:
            file_extensions = self.config.get(
                "toolkit.allowed_extensions", [".py"]
            )
        
        results = []
        root = Path(root_path)
        query_lower = query.lower()
        
        try:
            for file_path in root.rglob("*"):
                if not file_path.is_file():
                    continue
                if file_path.suffix.lower() not in file_extensions:
                    continue
                
                try:
                    content = file_path.read_text(encoding="utf-8")
                    if query_lower in content.lower():
                        line_numbers = [
                            i
                            for i, line in enumerate(content.split("\n"), 1)
                            if query_lower in line.lower()
                        ]
                        results.append({
                            "file": str(file_path),
                            "matches": len(line_numbers),
                            "line_numbers": line_numbers,
                        })
                except (UnicodeDecodeError, PermissionError):
                    continue
            
            return {
                "success": True,
                "results": results,
                "total_matches": sum(r["matches"] for r in results),
                "files_searched": len(results),
            }
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def export_project_snapshot(
        self, root_path: str, output_path: str
    ) -> Dict[str, Any]:
        """Export project structure and metadata."""
        if not self.security.is_path_allowed(root_path):
            return {"success": False, "error": "Root path not allowed"}
        
        root = Path(root_path)
        snapshot = {
            "root": str(root),
            "files": [],
            "directories": [],
            "total_files": 0,
            "total_size_bytes": 0,
        }
        
        try:
            for item in root.rglob("*"):
                if item.name.startswith("."):
                    continue
                if item.is_file():
                    size = item.stat().st_size
                    snapshot["files"].append({
                        "path": str(item.relative_to(root)),
                        "size": size,
                        "extension": item.suffix,
                    })
                    snapshot["total_size_bytes"] += size
                elif item.is_dir():
                    snapshot["directories"].append(
                        str(item.relative_to(root))
                    )
            
            snapshot["total_files"] = len(snapshot["files"])
            
            output_file = Path(output_path)
            output_file.parent.mkdir(parents=True, exist_ok=True)
            output_file.write_text(
                json.dumps(snapshot, indent=2), encoding="utf-8"
            )
            
            return {
                "success": True,
                "output_path": str(output_file.resolve()),
                "summary": {
                    "total_files": snapshot["total_files"],
                    "total_directories": len(snapshot["directories"]),
                    "total_size_mb": round(
                        snapshot["total_size_bytes"] / (1024 * 1024), 2
                    ),
                },
            }
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def get_file_info(self, filepath: str) -> Dict[str, Any]:
        """Get detailed file metadata."""
        if not self.security.is_path_allowed(filepath):
            return {"success": False, "error": "Path not allowed"}
        
        file_path = Path(filepath)
        if not file_path.exists():
            return {"success": False, "error": "File not found"}
        
        try:
            stat = file_path.stat()
            return {
                "success": True,
                "info": {
                    "name": file_path.name,
                    "path": str(file_path.resolve()),
                    "size_bytes": stat.st_size,
                    "extension": file_path.suffix,
                    "is_file": file_path.is_file(),
                    "is_dir": file_path.is_dir(),
                    "readable": os.access(file_path, os.R_OK),
                    "writable": os.access(file_path, os.W_OK),
                },
            }
        except Exception as e:
            return {"success": False, "error": str(e)}