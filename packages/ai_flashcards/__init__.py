"""AI Flashcards - Anki Add-on for generating flashcards with AI."""

from __future__ import annotations

import os
import sys
from typing import Any

# Setup library path for bundled dependencies
LIB_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "lib")
if LIB_DIR not in sys.path:
    sys.path.insert(0, LIB_DIR)

from aqt import gui_hooks, mw
from aqt.qt import Qt, QDockWidget

# Import modular components
from .container import ContainerBuilder
from .ui import AIFlashcardsDockWidget, MenuItemManager
from .logger import logger

# Global state
_container = None
_dock_widget: QDockWidget | None = None
_menu_action = None
_controller = None
_is_initialized = False


def _get_config() -> dict[str, Any]:
    """Get configuration from Anki's addon manager.

    Returns:
        Configuration dictionary
    """
    return mw.addonManager.getConfig(__name__) or {}


def _on_menu_triggered(_checked: bool = False) -> None:
    """Handle menu action trigger - show/focus dock widget."""
    if _dock_widget is not None:
        _dock_widget.show()
        _dock_widget.raise_()


def _setup_ui() -> None:
    """Setup UI components - called on Anki startup."""
    global _container, _dock_widget, _menu_action, _controller, _is_initialized

    try:
        if _is_initialized:
            logger.info("AI Flashcards already initialized, skipping duplicate setup")
            return

        logger.info("Initializing AI Flashcards Add-on")

        # Load configuration
        config_dict = _get_config()

        # Build dependency injection container with all services
        _container = ContainerBuilder.build(config_dict)
        config = _container.get("config")

        # Check if addon is enabled
        if not config.enabled:
            logger.info("AI Flashcards addon is disabled")
            return

        # Create and register dock widget
        _dock_widget, _controller = AIFlashcardsDockWidget.create(_container)
        mw.addDockWidget(Qt.DockWidgetArea.RightDockWidgetArea, _dock_widget)
        logger.info("Dock widget registered")

        # Optionally add menu entry
        if config.add_menu_entry:
            _menu_action = MenuItemManager.create_menu_action(_on_menu_triggered)

        _is_initialized = True
        logger.info("AI Flashcards Add-on initialized successfully")

    except Exception as exc:
        logger.error(f"Failed to initialize AI Flashcards: {exc}", exc_info=True)


# Register setup function with Anki's startup hook
gui_hooks.main_window_did_init.append(_setup_ui)
