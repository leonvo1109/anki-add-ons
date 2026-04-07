"""Type definitions and enums for AI Flashcards addon."""

from enum import Enum


class AIProviderType(str, Enum):
    """Supported AI provider types."""

    GEMINI = "gemini"
    OPENAI = "openai"
    ANTHROPIC = "anthropic"


class GenerationStatus(str, Enum):
    """Status of a generation request."""

    PENDING = "pending"
    PROCESSING = "processing"
    SUCCESS = "success"
    FAILED = "failed"
    CANCELLED = "cancelled"


class CardStatus(str, Enum):
    """Status of a flashcard."""

    DRAFT = "draft"
    REVIEW = "review"
    READY = "ready"
    ARCHIVED = "archived"

