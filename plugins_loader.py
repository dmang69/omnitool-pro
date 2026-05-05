import importlib.util
import json
import os
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional

from utils.logging_config import setup_logging

logger = setup_logging()

class PluginLoader:
    def __init__(self, plugins_dir: Optional[str] = None):
        env_override = os.getenv("AI_TOOLKIT_PLUGINS_DIR")
        if plugins_dir:
            self.plugins_workspace_dir = Path(plugins_dir)
            self.search_dirs = [self.plugins_workspace_dir]
        elif env_override:
            self.plugins_workspace_dir = Path(env_override)
            self.search_dirs = [self.plugins_workspace_dir]
        else:
            self.plugins_workspace_dir = Path.home() / ".ai_toolkit" / "plugins"
            self.search_dirs = [self.plugins_workspace_dir, Path(__file__).resolve().parent]

        self.plugins_workspace_dir.mkdir(parents=True, exist_ok=True)
        self.loaded_plugins: Dict[str, Any] = {}
        self.plugin_metadata: Dict[str, Any] = {}
        self.registry_path = self.plugins_workspace_dir / "registry.json"

    def discover_plugins(self) -> List[str]:
        found = []
        seen = set()

        for base in self.search_dirs:
            if not base.exists():
                continue

            for file in base.rglob("plugin.py"):
                name = file.parent.name
                if name not in seen:
                    seen.add(name)
                    found.append(name)

            for file in base.glob("*.py"):
                if file.stem in {"__init__", "loader"}:
                    continue
                name = file.stem
                if name not in seen:
                    seen.add(name)
                    found.append(name)

        return found

    def _resolve_plugin_file(self, plugin_name: str) -> Optional[Path]:
        candidates = []
        for base in self.search_dirs:
            candidates.append(base / plugin_name / "plugin.py")
            candidates.append(base / f"{plugin_name}.py")
        for candidate in candidates:
            if candidate.exists():
                return candidate
        return None

    def load_plugin(self, plugin_name: str, tool_interface=None) -> bool:
        try:
            plugin_file = self._resolve_plugin_file(plugin_name)
            if not plugin_file:
                return False

            spec = importlib.util.spec_from_file_location(
                f"ai_toolkit_plugin_{plugin_name}",
                plugin_file,
            )
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)

            if hasattr(module, "register") and callable(module.register):
                registered = module.register(tool_interface)
                if not registered:
                    return False

            self.loaded_plugins[plugin_name] = module
            if hasattr(module, "METADATA"):
                self.plugin_metadata[plugin_name] = module.METADATA
                self._save_registry()

            logger.info(f"Plugin loaded: {plugin_name}")
            return True
        except Exception as e:
            logger.error(f"Plugin load error [{plugin_name}]: {e}")
            return False

    def load_all_plugins(self, tool_interface=None) -> Dict[str, bool]:
        results = {}
        for plugin_name in self.discover_plugins():
            results[plugin_name] = self.load_plugin(plugin_name, tool_interface)
        return results

    def list_loaded_plugins(self) -> Dict[str, Any]:
        return {
            "plugins": [
                {
                    "name": name,
                    "metadata": self.plugin_metadata.get(name, {}),
                }
                for name in sorted(self.loaded_plugins.keys())
            ]
        }

    def _save_registry(self) -> None:
        try:
            self.registry_path.parent.mkdir(parents=True, exist_ok=True)
            self.registry_path.write_text(json.dumps(self.plugin_metadata, indent=2), encoding="utf-8")
        except Exception as e:
            logger.warning(f"Could not save plugin registry: {e}")