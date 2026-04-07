"""Simple dependency injection container for managing service instances."""

from typing import Any, Callable, Dict, TypeVar

from .models import ConfigModel
from .config_loader import load_config_from_dict
from .providers_base import AIProvider
from .providers_factory import ProviderFactory
from .card_generator import CardGeneratorService
from .logger import logger

T = TypeVar("T")


class DIContainer:
    """Simple dependency injection container."""

    def __init__(self):
        """Initialize DI container."""
        self._services: Dict[str, Any] = {}
        self._factories: Dict[str, Callable[[], Any]] = {}

    def register_singleton(self, key: str, instance: Any) -> None:
        """Register a singleton instance.

        Args:
            key: Service key
            instance: Service instance
        """
        self._services[key] = instance
        logger.debug(f"Registered singleton: {key}")

    def register_factory(self, key: str, factory: Callable[[], Any]) -> None:
        """Register a factory function for lazy instantiation.

        Args:
            key: Service key
            factory: Callable that returns service instance
        """
        self._factories[key] = factory
        logger.debug(f"Registered factory: {key}")

    def get(self, key: str) -> Any:
        """Get service instance.

        Args:
            key: Service key

        Returns:
            Service instance

        Raises:
            KeyError: If service not found
        """
        if key in self._services:
            return self._services[key]

        if key in self._factories:
            instance = self._factories[key]()
            self._services[key] = instance  # Cache after first call
            return instance

        raise KeyError(f"Service not found: {key}")


class ContainerBuilder:
    """Builder for configuring and creating DI container."""

    @staticmethod
    def build(config_dict: dict[str, Any]) -> DIContainer:
        """Build DI container with all services.

        Args:
            config_dict: Configuration dictionary from Anki

        Returns:
            Configured DIContainer instance
        """
        container = DIContainer()

        # Load and register configuration
        config = load_config_from_dict(config_dict)
        container.register_singleton("config", config)

        # Register provider factory
        provider = ProviderFactory.create(config)
        container.register_singleton("provider", provider)

        # Register card generator service
        card_generator = CardGeneratorService(provider, config)
        container.register_singleton("card_generator", card_generator)

        logger.info("DI Container initialized")
        return container

