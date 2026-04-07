"""Example unit tests for AI Flashcards services."""

from unittest.mock import Mock, patch

from ai_flashcards.models import Card, GenerationResponse, ConfigModel
from ai_flashcards.providers_base import AIProvider
from ai_flashcards.card_generator import CardGeneratorService
from ai_flashcards.container import DIContainer


class MockProvider(AIProvider):
    """Mock AI Provider for testing."""

    def generate(self, prompt: str, temperature: float = 0.2) -> GenerationResponse:
        """Return mock response."""
        return GenerationResponse(
            success=True,
            content="Q: What is Python?\nA: Python is a programming language.",
            metadata={"model": "mock", "provider": "mock"}
        )


def test_card_generator_service():
    """Test CardGeneratorService with mock provider."""
    # Setup
    config = ConfigModel(provider="gemini", model="test-model")
    provider = MockProvider(api_key="test", model="test-model")
    service = CardGeneratorService(provider, config)

    # Test: Generate single card
    card = service.generate_card("Python programming")
    assert card is not None
    assert card.question == "What is Python?"
    assert card.answer == "Python is a programming language."


def test_card_generator_batch():
    """Test batch card generation."""
    config = ConfigModel(provider="gemini", model="test-model", max_cards_per_run=5)
    provider = MockProvider(api_key="test", model="test-model")
    service = CardGeneratorService(provider, config)

    # Test: Batch generation respects max_cards_per_run
    topics = ["Python", "JavaScript", "Go", "Rust", "C++", "Java", "Ruby"]
    cards = service.batch_generate(topics)

    assert len(cards) <= config.max_cards_per_run
    assert all(isinstance(card, Card) for card in cards)


def test_config_validation():
    """Test ConfigModel validation."""
    # Valid config
    config = ConfigModel(temperature=0.5, max_cards_per_run=10)
    errors = config.validate()
    assert len(errors) == 0

    # Invalid temperature
    config_bad_temp = ConfigModel(temperature=1.5)
    errors = config_bad_temp.validate()
    assert len(errors) > 0
    assert "temperature must be between 0 and 1" in errors

    # Invalid max_cards
    config_bad_cards = ConfigModel(max_cards_per_run=-1)
    errors = config_bad_cards.validate()
    assert len(errors) > 0


def test_di_container():
    """Test dependency injection container."""
    container = DIContainer()

    # Register services
    config = ConfigModel(provider="gemini")
    container.register_singleton("config", config)

    provider = MockProvider(api_key="test", model="test")
    container.register_singleton("provider", provider)

    # Retrieve services
    retrieved_config = container.get("config")
    assert retrieved_config is config

    retrieved_provider = container.get("provider")
    assert retrieved_provider is provider

    # Test factory/lazy-loading
    call_count = 0

    def factory():
        nonlocal call_count
        call_count += 1
        return "lazy_service"

    container.register_factory("lazy", factory)
    service1 = container.get("lazy")
    service2 = container.get("lazy")

    assert call_count == 1  # Factory called only once, then cached
    assert service1 is service2


if __name__ == "__main__":
    print("Running tests...")
    test_card_generator_service()
    print("✓ test_card_generator_service passed")

    test_card_generator_batch()
    print("✓ test_card_generator_batch passed")

    test_config_validation()
    print("✓ test_config_validation passed")

    test_di_container()
    print("✓ test_di_container passed")

    print("\nAll tests passed! ✓")

