import os
import zipfile
from pathlib import Path

# Define the project structure
PROJECT_STRUCTURE = {
    "ai_toolkit": {
        "config": ["default.yaml"],
        "toolkit": [
            "__init__.py", "filesystem.py", "code_understanding.py", "automation.py",
            "device_diagnostics.py", "adb_manager.py", "ios_manager.py",
            "soft_repair.py", "security_audit.py"
        ],
        "agents": ["__init__.py", "tool_interface.py", "chat_agent.py"],
        "plugins": {
            "__init__.py": None,
            "loader.py": None,
            "example_plugin": ["__init__.py", "plugin.py"]
        },
        "utils": [
            "__init__.py", "logging_config.py", "config.py", "security.py", "json_response.py"
        ],
        "gui": ["__init__.py", "chat_window.py"],
        "tests": [
            "__init__.py", "test_filesystem.py", "test_code_understanding.py",
            "test_automation.py", "test_agents.py"
        ],
        "build": ["build.py"],
        "main.py": None,
        "requirements.txt": None,
        "README.md": None,
    }
}

# Content for each file
FILE_CONTENTS = {
    "main.py": """<Insert main.py content here>""",
    "requirements.txt": """<Insert requirements.txt content here>""",
    "README.md": """<Insert README.md content here>""",
    # Add the rest of the file content here...
}

def create_project_structure(base_dir: Path, structure: dict, contents: dict):
    """Recursively create project structure and populate files."""
    for name, children in structure.items():
        path = base_dir / name
        if isinstance(children, dict):
            # Create subdirectory
            path.mkdir(parents=True, exist_ok=True)
            create_project_structure(path, children, contents)
        elif isinstance(children, list):
            # Create files in this directory
            path.mkdir(parents=True, exist_ok=True)
            for file_name in children:
                file_path = path / file_name
                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(contents.get(file_name, ""))
        else:
            # Create a single file
            with open(path, "w", encoding="utf-8") as f:
                f.write(contents.get(name, ""))

def zip_project(base_dir: Path, output_path: Path):
    """Zip the entire project directory."""
    with zipfile.ZipFile(output_path, "w", zipfile.ZIP_DEFLATED) as zipf:
        for root, _, files in os.walk(base_dir):
            for file in files:
                file_path = Path(root) / file
                arcname = file_path.relative_to(base_dir)
                zipf.write(file_path, arcname)

def main():
    base_dir = Path("ai_toolkit")
    zip_path = Path("ai_toolkit.zip")
    
    # Create the project structure
    create_project_structure(base_dir, PROJECT_STRUCTURE, FILE_CONTENTS)
    print(f"Project structure created at {base_dir}")
    
    # Zip the project
    zip_project(base_dir, zip_path)
    print(f"Project zipped to {zip_path}")

if __name__ == "__main__":
    main()
