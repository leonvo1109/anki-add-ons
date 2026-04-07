"""Base class for AI providers."""

from abc import ABC, abstractmethod

from .models import GenerationResponse
from .logger import logger


class AIProvider(ABC):
    """Abstract base class for AI providers."""

    def __init__(self, api_key: str, model: str):
        """Initialize provider.

        Args:
            api_key: API key for the provider
            model: Model name to use
        """
        self.api_key = api_key
        self.model = model

    @abstractmethod
    def generate(self, prompt: str, temperature: float = 0.2) -> GenerationResponse:
        """Generate response from prompt.

        Args:
            prompt: Input prompt
            temperature: Temperature/creativity parameter (0-1)

        Returns:
            GenerationResponse with success status and content
        """
        pass

    def validate_api_key(self) -> bool:
        """Validate that API key is set.

        Returns:
            True if API key is configured, False otherwise
        """
        if not self.api_key or self.api_key.strip() == "":
            logger.warning(f"{self.__class__.__name__}: No API key configured")
            return False
        return True

