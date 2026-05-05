from pathlib import Path

from utils.config import Config
from utils.security import SecurityManager
from toolkit.automation import PythonAutomationEngine

def make_engine(tmp_path):
    cfg = Config()
    cfg.set("security.allowed_paths", [str(tmp_path)])
    sec = SecurityManager(cfg)
    return PythonAutomationEngine(sec)

def test_run_script(tmp_path):
    engine = make_engine(tmp_path)
    script = tmp_path / "hello.py"
    script.write_text('print("hello")\n', encoding="utf-8")

    result = engine.run_script(str(script))
    assert result["success"] is True
    assert "hello" in result["data"]["stdout"]