"""Data models for AI Flashcards addon."""

from dataclasses import dataclass, field
from typing import Any, Optional


@dataclass
class ConfigModel:
    """Addon configuration model."""

    enabled: bool = True
    provider: str = "gemini"
    model: str = "gemini-2.0-flash"
    target_deck: str = ""
    note_type: str = ""
    max_cards_per_run: int = 10
    temperature: float = 0.2
    add_menu_entry: bool = True
    gemini_api_key: str = ""

    def validate(self) -> list[str]:
        """Validate configuration and return list of errors."""
        errors: list[str] = []

        if self.temperature < 0 or self.temperature > 1:
            errors.append("temperature must be between 0 and 1")

        if self.max_cards_per_run < 1:
            errors.append("max_cards_per_run must be at least 1")

        return errors


@dataclass
class Card:
    """A flashcard to be created."""

    question: str
    answer: str
    tags: list[str] = field(default_factory=list)
    extra: dict[str, Any] = field(default_factory=dict)
    status: str = "draft"


@dataclass
class GenerationResponse:
    """Response from AI provider."""

    success: bool
    content: Optional[str] = None
    error: Optional[str] = None
    usage: dict[str, Any] = field(default_factory=dict)
    metadata: dict[str, Any] = field(default_factory=dict)

