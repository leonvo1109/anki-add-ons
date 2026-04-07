"""UI controllers for handling user interactions."""

from aqt.qt import QLineEdit, QTextEdit

from .container import DIContainer
from .card_generator import CardGeneratorService
from .logger import logger


class PromptController:
    """Controller for handling prompt input and response generation."""

    def __init__(
        self,
        container: DIContainer,
        prompt_input: QLineEdit,
        response_output: QTextEdit,
    ):
        """Initialize prompt controller.

        Args:
            container: DI container for accessing services
            prompt_input: QLineEdit widget for user prompt
            response_output: QTextEdit widget for displaying response
        """
        self.container = container
        self.prompt_input = prompt_input
        self.response_output = response_output
        self.card_generator: CardGeneratorService = container.get("card_generator")

    def on_prompt_click(self) -> None:
        """Handle prompt button click event."""
        prompt = self.prompt_input.text().strip()

        if not prompt:
            self.response_output.setPlainText("Bitte gib zuerst einen Prompt ein.")
            return

        logger.info(f"Processing prompt: {prompt[:50]}...")
        self.response_output.setPlainText("Generiere Antwort...")

        try:
            # Generate card with prompt as topic
            card = self.card_generator.generate_card(prompt)

            if card is None:
                self.response_output.setPlainText(
                    "Fehler: Antwort konnte nicht generiert werden."
                )
                return

            # Format response for display
            response_text = f"Frage:\n{card.question}\n\nAntwort:\n{card.answer}"
            self.response_output.setPlainText(response_text)
            logger.info("Successfully displayed generated card")

        except Exception as exc:
            error_msg = f"Fehler beim Generieren: {exc}"
            self.response_output.setPlainText(error_msg)
            logger.error(error_msg)

