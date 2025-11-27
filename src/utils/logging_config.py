# src/utils/logging_config.py

import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path

LOG_DIR = Path("logs")
LOG_FILE = LOG_DIR / "app.log"

def setup_logging():
    """
    Configure logging for the application.

    - Logs go to both console and file
    - File logs are rotated (so file doesn't grow forever)
    """

    LOG_DIR.mkdir(parents=True, exist_ok=True)

    logger = logging.getLogger()  # root logger
    logger.setLevel(logging.INFO)  # default level

    # Avoid adding duplicate handlers if setup_logging is called multiple times
    if logger.handlers:
        return

    # Console handler (prints to terminal)
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)

    # File handler (writes to logs/app.log)
    file_handler = RotatingFileHandler(
        LOG_FILE, maxBytes=500_000, backupCount=3, encoding="utf-8"
    )
    file_handler.setLevel(logging.INFO)

    # Log format
    formatter = logging.Formatter(
        fmt="%(asctime)s [%(levelname)s] [%(name)s] %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    console_handler.setFormatter(formatter)
    file_handler.setFormatter(formatter)

    logger.addHandler(console_handler)
    logger.addHandler(file_handler)
