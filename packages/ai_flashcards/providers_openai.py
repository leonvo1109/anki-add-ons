"""OpenAI provider implementation (stub for future implementation)."""

from .models import GenerationResponse
from .logger import logger
from .providers_base import AIProvider


class OpenAIProvider(AIProvider):
    """OpenAI API provider (future implementation)."""

    def generate(self, prompt: str, temperature: float = 0.2) -> GenerationResponse:
        """Generate response using OpenAI API.

        Args:
            prompt: Input prompt
            temperature: Temperature/creativity parameter (0-1)

        Returns:
            GenerationResponse with generated content or error
        """
        logger.warning("OpenAI provider not yet implemented")
        return GenerationResponse(
            success=False,
            error="OpenAI provider not yet implemented"
        )

