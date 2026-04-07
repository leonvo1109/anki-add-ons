"""UI components and widgets for AI Flashcards addon."""

from aqt import mw
from aqt.qt import (
    QAction,
    QDockWidget,
    QLabel,
    QLineEdit,
    QPushButton,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)

from .container import DIContainer
from .controller import PromptController
from .logger import logger

ADDON_MENU_LABEL = "AI Flashcards"


class AIFlashcardsDockWidget:
    """Factory for creating and managing dock widget."""

    @staticmethod
    def create(container: DIContainer) -> tuple[QDockWidget, PromptController]:
        """Create dock widget with all UI components.

        Args:
            container: DI container for service access

        Returns:
            Tuple of (QDockWidget, PromptController)
        """
        dock = QDockWidget(ADDON_MENU_LABEL, mw)
        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(10, 10, 10, 10)

        # Titel
        title = QLabel(ADDON_MENU_LABEL)
        title.setStyleSheet("font-weight: bold; font-size: 14px;")
        layout.addWidget(title)

        # Prompt-Eingabe
        prompt_input = QLineEdit()
        prompt_input.setPlaceholderText("Prompt eingeben...")
        layout.addWidget(prompt_input)

        # Info-Text
        info = QLabel("Klick auf 'Prompt' um KI-Antwort zu generieren.")
        layout.addWidget(info)

        # Start-Button
        button = QPushButton("Prompt")
        layout.addWidget(button)

        # Ausgabe
        response_output = QTextEdit()
        response_output.setReadOnly(True)
        response_output.setPlaceholderText("Die Antwort erscheint hier...")
        layout.addWidget(response_output)

        # Platzhalter für zukünftige Inhalte
        layout.addStretch()

        dock.setWidget(widget)

        # Create controller and connect button
        controller = PromptController(container, prompt_input, response_output)
        button.clicked.connect(controller.on_prompt_click)

        logger.info("Dock widget created")
        return dock, controller


class MenuItemManager:
    """Manager for menu entries."""

    @staticmethod
    def create_menu_action(on_triggered) -> QAction:
        """Create menu action for AI Flashcards.

        Args:
            on_triggered: Callback function for action triggered

        Returns:
            QAction instance
        """
        for existing_action in mw.form.menuTools.actions():
            if existing_action.text() == ADDON_MENU_LABEL:
                logger.info("Menu action already exists, reusing existing action")
                return existing_action

        action = QAction(ADDON_MENU_LABEL, mw)
        action.triggered.connect(on_triggered)
        mw.form.menuTools.addAction(action)
        logger.info("Menu action created")
        return action

