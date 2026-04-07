"""Gemini AI provider implementation."""

import asyncio
import inspect

from .models import GenerationResponse
from .exceptions import AIProviderError
from .logger import logger
from .providers_base import AIProvider

# Import Apple FM SDK (bundled in lib/)
try:
    from apple_fm_sdk import LanguageModelSession
except ImportError:
    logger.error("apple_fm_sdk not found. Make sure it's in the lib/ directory.")
    LanguageModelSession = None


class GeminiProvider(AIProvider):
    """Gemini AI provider using Apple On-Device Model."""

    def generate(self, prompt: str, temperature: float = 0.2) -> GenerationResponse:
        """Generate response using Gemini model.

        Args:
            prompt: Input prompt
            temperature: Temperature/creativity parameter (0-1)

        Returns:
            GenerationResponse with generated content or error
        """
        if not self.validate_api_key():
            return GenerationResponse(
                success=False,
                error="Gemini API key not configured"
            )

        if LanguageModelSession is None:
            return GenerationResponse(
                success=False,
                error="apple_fm_sdk not available"
            )

        try:
            logger.info(f"Generating response with Gemini model: {self.model}")

            session = LanguageModelSession()
            response = session.respond(prompt)

            # Handle both sync and async responses
            if inspect.isawaitable(response):
                try:
                    response = asyncio.run(response)
                except RuntimeError:
                    # If event loop already running, create new one
                    loop = asyncio.new_event_loop()
                    try:
                        response = loop.run_until_complete(response)
                    finally:
                        loop.close()

            # Extract text from response
            content = None
            if hasattr(response, "text"):
                content = str(response.text)
            else:
                content = str(response)

            logger.info("Successfully generated response")

            return GenerationResponse(
                success=True,
                content=content,
                metadata={"model": self.model, "provider": "gemini"}
            )

        except Exception as exc:
            error_msg = f"Gemini generation failed: {exc}"
            logger.error(error_msg)
            return GenerationResponse(
                success=False,
                error=error_msg
            )

