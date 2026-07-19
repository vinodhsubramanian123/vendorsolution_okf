"""
IKP Structured Logger — Centralized observability for the platform.

Governs: Blueprint 02 §11 (Observability & Telemetry)
"""

import logging
import sys
from pathlib import Path


def setup_logger(
    name: str, log_file: str = "ikp.log", level: int = logging.INFO
) -> logging.Logger:
    """Configure a structured logger with both console and file handlers."""
    logger = logging.getLogger(name)
    logger.setLevel(level)

    # Remove existing handlers if re-initialized
    if logger.hasHandlers():
        logger.handlers.clear()

    # Formatter
    formatter = logging.Formatter(
        fmt="%(asctime)s [%(name)s] %(levelname)s: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    # Console Handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    # File Handler
    try:
        log_path = Path(log_file)
        file_handler = logging.FileHandler(log_path)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
    except OSError:
        # Fallback if cannot write to file
        pass

    return logger


def get_logger(module_name: str) -> logging.Logger:
    """Get a logger for a specific module."""
    return logging.getLogger(f"ikp.{module_name}")
