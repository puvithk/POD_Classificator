"""Logger configuration."""

import logging
import sys


def setup_logger(name: str = "pod_classifier", level: int = logging.INFO) -> logging.Logger:
    """Set up and return a standardized logger."""
    logger = logging.getLogger(name)
    if not logger.handlers:
        logger.setLevel(level)
        handler = logging.StreamHandler(sys.stdout)
        formatter = logging.Formatter("[%(asctime)s] [%(levelname)s] [%(name)s]: %(message)s")
        handler.setFormatter(formatter)
        logger.addHandler(handler)
    return logger
