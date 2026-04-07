"""Custom exceptions for AI Flashcards addon."""


class AIFlashcardsException(Exception):
    """Base exception for AI Flashcards addon."""

    pass


class AIProviderError(AIFlashcardsException):
    """Raised when AI provider fails."""

    pass


class ConfigurationError(AIFlashcardsException):
    """Raised when configuration is invalid."""

    pass


class ValidationError(AIFlashcardsException):
    """Raised when input validation fails."""

    pass


class DeckNotFoundError(AIFlashcardsException):
    """Raised when target deck is not found."""

    pass


class NoteTypeNotFoundError(AIFlashcardsException):
    """Raised when note type is not found."""

    pass

