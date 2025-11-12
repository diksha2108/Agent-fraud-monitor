import os
import tempfile
import yaml
import pytest

from src.utils.helpers import load_config, mask_sensitive, ensure_directory

def test_mask_sensitive_short_string():
    assert mask_sensitive("1234", show_last=4) == "1234"

def test_mask_sensitive_long_string():
    masked = mask_sensitive("1234567890", show_last=4)
    assert masked.endswith("7890")
    assert all(c == "*" for c in masked[:-4])

def test_load_config_file(tmp_path):
    cfg = {"key": "value", "nested": {"a": 1}}
    file_path = tmp_path / "config.yaml"
    with open(file_path, "w", encoding="utf‑8") as f:
        yaml.dump(cfg, f)
    loaded = load_config(str(file_path))
    assert loaded == cfg

def test_load_config_file_not_exist(tmp_path):
    missing = str(tmp_path / "does_not_exist.yaml")
    with pytest.raises(FileNotFoundError):
        load_config(missing)

def test_ensure_directory(tmp_path):
    target = tmp_path / "subdir" / "inner"
    # should not exist yet
    assert not target.exists()
    ensure_directory(str(target))
    assert target.exists() and target.is_dir()
