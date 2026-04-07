"""Card generation service."""

from typing import Optional

from .models import ConfigModel, Card, GenerationResponse
from .exceptions import AIProviderError
from .logger import logger
from .providers_base import AIProvider


class CardGeneratorService:
    """Service for generating flashcards using AI provider."""

    def __init__(self, provider: AIProvider, config: ConfigModel):
        """Initialize card generator.

        Args:
            provider: AIProvider instance
            config: Configuration model
        """
        self.provider = provider
        self.config = config

    def generate_card(self, topic: str) -> Optional[Card]:
        """Generate a single flashcard for given topic.

        Args:
            topic: Topic or prompt for card generation

        Returns:
            Card object or None if generation failed
        """
        logger.info(f"Generating card for topic: {topic}")

        # Create prompt for card generation
        prompt = self._create_card_prompt(topic)

        # Call provider
        response = self.provider.generate(
            prompt=prompt,
            temperature=self.config.temperature
        )

        if not response.success:
            logger.error(f"Card generation failed: {response.error}")
            return None

        # Parse response into Card object
        card = self._parse_response_to_card(response.content)
        if card is None:
            logger.error("Failed to parse AI response into card format")
            return None

        logger.info(f"Successfully generated card: Q: {card.question[:50]}...")
        return card

    def _create_card_prompt(self, topic: str) -> str:
        """Create a detailed prompt for card generation.

        Args:
            topic: Topic for the card

        Returns:
            Formatted prompt string
        """
        return (
            f"Create a flashcard question and answer for the following topic:\n\n"
            f"Topic: {topic}\n\n"
            f"Format the response exactly as:\n"
            f"Q: [Question here]\n"
            f"A: [Answer here]\n\n"
            f"Make the question clear and concise, and the answer informative but brief."
        )

    def _parse_response_to_card(self, response: Optional[str]) -> Optional[Card]:
        """Parse AI response into Card object.

        Args:
            response: Raw response from AI provider

        Returns:
            Parsed Card object or None if parsing failed
        """
        if not response:
            return None

        lines = response.strip().split("\n")
        question = None
        answer = None

        for i, line in enumerate(lines):
            if line.startswith("Q:"):
                question = line[2:].strip()
            elif line.startswith("A:"):
                answer = line[2:].strip()

        if not question or not answer:
            logger.warning(f"Could not parse response: {response}")
            return None

        return Card(
            question=question,
            answer=answer,
            tags=self.config.target_deck.split("::") if self.config.target_deck else [],
        )

    def batch_generate(self, topics: list[str]) -> list[Card]:
        """Generate multiple cards (future: with batching optimization).

        Args:
            topics: List of topics to generate cards for

        Returns:
            List of successfully generated Card objects
        """
        cards = []
        for i, topic in enumerate(topics, 1):
            if i > self.config.max_cards_per_run:
                logger.info(f"Reached max cards limit: {self.config.max_cards_per_run}")
                break

            card = self.generate_card(topic)
            if card:
                cards.append(card)

        logger.info(f"Generated {len(cards)} cards out of {len(topics)} topics")
        return cards

