# src/utils/helpers.py

import os
import yaml
from typing import Any, Dict, Optional

def load_config(path: str) -> Dict[str, Any]:
    """
    Load a YAML configuration file from the given path and return a dict.
    Raises FileNotFoundError if the file does not exist.
    """
    if not os.path.exists(path):
        raise FileNotFoundError(f"Configuration file not found: {path}")

    with open(path, "r", encoding="utf-8") as f:
        config = yaml.safe_load(f)
    return config or {}

def mask_sensitive(data: str, show_last: int = 4, mask_char: str = "*") -> str:
    """
    Mask a string except for the last `show_last` characters.
    Useful for logging or partial display of IDs or account numbers.
    Example: mask_sensitive("123456789", show_last=4) -> "*****6789"
    """
    if data is None:
        return ""
    length = len(data)
    if length <= show_last:
        return data
    return mask_char * (length - show_last) + data[-show_last:]

def ensure_directory(path: str) -> None:
    """
    Ensure that the directory at `path` exists. If not, create it.
    """
    os.makedirs(path, exist_ok=True)
