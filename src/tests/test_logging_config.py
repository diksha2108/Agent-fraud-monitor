import logging
import os
import tempfile
from src.utils.logging_config import configure_logging

def test_configure_logging_console_capture(caplog):
    caplog.set_level(logging.INFO)
    configure_logging(log_level="INFO")
    logger = logging.getLogger("some_module")
    logger.info("hello")
    assert "hello" in caplog.text

def test_configure_logging_file(tmp_path, caplog):
    log_file = tmp_path / "app.log"
    configure_logging(log_level="DEBUG", log_file=str(log_file))
    logger = logging.getLogger("moduleX")
    logger.debug("debug message")
    # Ensure that file exists and contains our message
    logger.handlers[0].flush()
    with open(log_file, "r", encoding="utf‑8") as f:
        content = f.read()
    assert "debug message" in content
