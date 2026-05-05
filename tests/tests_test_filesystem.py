from pathlib import Path

from utils.config import Config
from utils.security import SecurityManager
from toolkit.filesystem import FileSystemIntelligence

def make_fs(tmp_path):
    cfg = Config()
    cfg.set("security.allowed_paths", [str(tmp_path)])
    sec = SecurityManager(cfg)
    return FileSystemIntelligence(sec, cfg)

def test_read_write_file(tmp_path):
    fs = make_fs(tmp_path)
    path = tmp_path / "test.txt"

    write_result = fs.write_file(str(path), "hello world", overwrite=False)
    assert write_result["success"] is True

    read_result = fs.read_file(str(path))
    assert read_result["success"] is True
    assert read_result["data"]["content"] == "hello world"

def test_search_files(tmp_path):
    fs = make_fs(tmp_path)
    path = tmp_path / "sample.txt"
    path.write_text("alpha\nbeta\nalpha again", encoding="utf-8")

    result = fs.search_files(str(tmp_path), "alpha", file_extensions=[".txt"])
    assert result["success"] is True
    assert len(result["data"]["matches"]) == 1

def test_export_snapshot(tmp_path):
    fs = make_fs(tmp_path)
    (tmp_path / "a.txt").write_text("x", encoding="utf-8")
    out = tmp_path / "snapshot.json"

    result = fs.export_project_snapshot(str(tmp_path), str(out))
    assert result["success"] is True
    assert out.exists()