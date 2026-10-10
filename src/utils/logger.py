"""
Logging Utility Module.
Provides centralized logging configuration for cloud audit readiness.
"""

import os
import json
import logging
from typing import Dict, Any

def load_config(config_path: str = "config/config.json") -> Dict[str, Any]:
    """Load configuration variables from JSON file."""
    if not os.path.exists(config_path):
        return {
            "data_file": "data/students.json",
            "log_file": "logs/app.log",
            "log_level": "INFO",
            "export_dir": "exports"
        }
    with open(config_path, "r") as f:
        return json.load(f)

def setup_logger(name: str = "StudentSysLogger") -> logging.Logger:
    """Configures and returns a multi-handler logger instance."""
    config = load_config()
    log_file = config.get("log_file", "logs/app.log")
    log_level = getattr(logging, config.get("log_level", "INFO").upper(), logging.INFO)

    log_dir = os.path.dirname(log_file)
    if log_dir and not os.path.exists(log_dir):
        os.makedirs(log_dir, exist_ok=True)

    logger = logging.getLogger(name)
    logger.setLevel(log_level)

    if not logger.handlers:
        # File Handler
        file_handler = logging.FileHandler(log_file)
        file_formatter = logging.Formatter(
            "[%(asctime)s] [%(levelname)s] [%(name)s]: %(message)s"
        )
        file_handler.setFormatter(file_formatter)
        logger.addHandler(file_handler)

        # Stream Handler (Console)
        stream_handler = logging.StreamHandler()
        stream_formatter = logging.Formatter("[%(levelname)s] %(message)s")
        stream_handler.setFormatter(stream_formatter)
        logger.addHandler(stream_handler)

    return logger