"""Configuration loader for AI Flashcards addon."""

import json
import os
from pathlib import Path
from typing import Any

from .models import ConfigModel
from .logger import logger

RUNTIME_READY_PROVIDERS = {"gemini"}


def load_config_from_dict(config_dict: dict[str, Any]) -> ConfigModel:
    """Load configuration from dictionary and apply environment variable overrides.

    Args:
        config_dict: Configuration dictionary (typically from Anki's addonManager.getConfig)

    Returns:
        ConfigModel instance with environment variable overrides applied
    """
    # Create config model from dict
    config = ConfigModel(
        enabled=config_dict.get("enabled", True),
        provider=config_dict.get("provider", "gemini"),
        model=config_dict.get("model", "gemini-2.0-flash"),
        target_deck=config_dict.get("target_deck", ""),
        note_type=config_dict.get("note_type", ""),
        max_cards_per_run=config_dict.get("max_cards_per_run", 10),
        temperature=float(config_dict.get("temperature", 0.2)),
        add_menu_entry=config_dict.get("add_menu_entry", True),
        gemini_api_key=config_dict.get("gemini_api_key", ""),
    )

    # Apply environment variable overrides
    if api_key := os.environ.get("GEMINI_API_KEY"):
        config.gemini_api_key = api_key

    if enabled := os.environ.get("AI_FLASHCARDS_ENABLED"):
        config.enabled = enabled.lower() in ("true", "1", "yes")

    if provider := os.environ.get("AI_FLASHCARDS_PROVIDER"):
        config.provider = provider

    if model := os.environ.get("AI_FLASHCARDS_MODEL"):
        config.model = model

    if config.provider not in RUNTIME_READY_PROVIDERS:
        logger.warning(
            "Provider '%s' is not implemented yet. Falling back to 'gemini'.",
            config.provider,
        )
        config.provider = "gemini"

    # Validate configuration
    errors = config.validate()
    if errors:
        for error in errors:
            logger.warning(f"Configuration warning: {error}")

    return config


def load_config_from_file(file_path: Path) -> dict[str, Any]:
    """Load configuration from JSON file.

    Args:
        file_path: Path to config.json file

    Returns:
        Configuration dictionary
    """
    if not file_path.exists():
        logger.warning(f"Config file not found: {file_path}")
        return {}

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError) as e:
        logger.error(f"Failed to load config file: {e}")
        return {}

