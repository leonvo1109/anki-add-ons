"""Provider factory for creating AI provider instances."""

from .types import AIProviderType
from .models import ConfigModel
from .exceptions import ConfigurationError
from .logger import logger
from .providers_base import AIProvider
from .providers_gemini import GeminiProvider
from .providers_openai import OpenAIProvider


class ProviderFactory:
    """Factory for creating AI provider instances."""

    _providers = {
        AIProviderType.GEMINI: GeminiProvider,
        AIProviderType.OPENAI: OpenAIProvider,
    }

    @classmethod
    def create(cls, config: ConfigModel) -> AIProvider:
        """Create provider instance based on configuration.

        Args:
            config: ConfigModel with provider settings

        Returns:
            AIProvider instance

        Raises:
            ConfigurationError: If provider type is not supported
        """
        try:
            provider_type = AIProviderType(config.provider)
        except ValueError:
            raise ConfigurationError(
                f"Unknown provider: {config.provider}. "
                f"Supported: {', '.join([p.value for p in AIProviderType])}"
            )

        provider_class = cls._providers.get(provider_type)
        if not provider_class:
            raise ConfigurationError(
                f"Provider {config.provider} not implemented yet"
            )

        logger.info(f"Creating {config.provider} provider with model: {config.model}")
        return provider_class(api_key=config.gemini_api_key, model=config.model)

    @classmethod
    def register_provider(
        cls, provider_type: AIProviderType, provider_class: type[AIProvider]
    ) -> None:
        """Register a new provider implementation.

        Args:
            provider_type: Type of provider
            provider_class: Provider class to register
        """
        cls._providers[provider_type] = provider_class
        logger.info(f"Registered provider: {provider_type.value}")

