"""Logger setup for AI Flashcards addon."""

import logging
import os
import sys
from pathlib import Path


def _anki_addons_dir() -> Path | None:
    """Return the platform-specific Anki addons directory, if known."""
    if sys.platform == "darwin":
        return Path.home() / "Library" / "Application Support" / "Anki2" / "addons21"
    if sys.platform.startswith("linux"):
        return Path.home() / ".local" / "share" / "Anki2" / "addons21"
    if sys.platform == "win32":
        return Path.home() / "AppData" / "Roaming" / "Anki2" / "addons21"
    return None


def setup_logger(name: str = "ai_flashcards", level: int = logging.INFO) -> logging.Logger:
    """Setup logger for AI Flashcards addon.

    Args:
        name: Logger name
        level: Logging level (default: INFO)

    Returns:
        Configured logger instance
    """
    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.propagate = False

    # Avoid adding handlers if logger already configured
    if logger.handlers:
        return logger

    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(level)

    # Formatter
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    console_handler.setFormatter(formatter)

    logger.addHandler(console_handler)

    # File handler (optional, if log directory exists)
    addons_dir = _anki_addons_dir()
    log_dir = addons_dir / "ai_flashcards" if addons_dir else None
    if log_dir and (log_dir.exists() or os.environ.get("AI_FLASHCARDS_LOG_FILE")):
        log_dir.mkdir(parents=True, exist_ok=True)
        log_file = log_dir / "ai_flashcards.log"
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(level)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    return logger


# Global logger instance
logger = setup_logger()

