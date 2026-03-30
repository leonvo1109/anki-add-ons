from __future__ import annotations

import asyncio
import inspect
import os
import sys
from typing import Any

LIB_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "lib")
if LIB_DIR not in sys.path:
    sys.path.insert(0, LIB_DIR)

from aqt import gui_hooks, mw
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
from aqt.qt import Qt
from apple_fm_sdk import LanguageModelSession

ADDON_MENU_LABEL = "AI Flashcards"
_action: QAction | None = None
_dock_widget: QDockWidget | None = None
_prompt_input: QLineEdit | None = None
_response_output: QTextEdit | None = None


def _config() -> dict[str, Any]:
    return mw.addonManager.getConfig(__name__) or {}


def _generate_response(prompt: str) -> str:
    """Generiert eine Antwort via Apple On-Device Model."""
    try:
        session = LanguageModelSession()
        response = session.respond(prompt)

        # Einige SDK-Versionen liefern ein Coroutine-Objekt zurück.
        if inspect.isawaitable(response):
            try:
                response = asyncio.run(response)
            except RuntimeError:
                loop = asyncio.new_event_loop()
                try:
                    response = loop.run_until_complete(response)
                finally:
                    loop.close()

        if hasattr(response, "text"):
            return str(response.text)

        return str(response)
    except Exception as exc:
        return f"Fehler beim Generieren der Antwort: {exc}"


def _on_prompt_click() -> None:
    if _prompt_input is None or _response_output is None:
        return

    prompt = _prompt_input.text().strip()
    if not prompt:
        _response_output.setPlainText("Bitte gib zuerst einen Prompt ein.")
        return

    _response_output.setPlainText("Generiere Antwort...")
    answer = _generate_response(prompt)
    _response_output.setPlainText(answer)


def _create_dock_widget() -> QDockWidget:
    """Erstellt das Dock-Widget für den AI Flashcards Tab."""
    global _prompt_input, _response_output

    dock = QDockWidget(ADDON_MENU_LABEL, mw)
    widget = QWidget()
    layout = QVBoxLayout(widget)
    layout.setContentsMargins(10, 10, 10, 10)

    # Titel
    title = QLabel(ADDON_MENU_LABEL)
    title.setStyleSheet("font-weight: bold; font-size: 14px;")
    layout.addWidget(title)

    # Prompt-Eingabe
    _prompt_input = QLineEdit()
    _prompt_input.setPlaceholderText("Prompt eingeben...")
    layout.addWidget(_prompt_input)

    # Info-Text
    info = QLabel("Klick auf 'Prompt' um KI-Antwort zu generieren.")
    layout.addWidget(info)

    # Start-Button
    button = QPushButton("Prompt")
    button.clicked.connect(_on_prompt_click)
    layout.addWidget(button)

    # Ausgabe
    _response_output = QTextEdit()
    _response_output.setReadOnly(True)
    _response_output.setPlaceholderText("Die Antwort erscheint hier...")
    layout.addWidget(_response_output)

    # Platzhalter für zukünftige Inhalte
    layout.addStretch()

    dock.setWidget(widget)
    return dock


def _on_menu_triggered(_checked: bool = False) -> None:
    if _dock_widget is not None:
        _dock_widget.show()
        _dock_widget.raise_()
    if _prompt_input is not None:
        _prompt_input.setFocus()


def _setup_ui() -> None:
    global _action, _dock_widget

    config = _config()
    if not config.get("enabled", True):
        return

    # Dock-Widget hinzufügen
    _dock_widget = _create_dock_widget()
    mw.addDockWidget(Qt.DockWidgetArea.RightDockWidgetArea, _dock_widget)

    # Optional: Menüeintrag hinzufügen
    if config.get("add_menu_entry", True):
        _action = QAction(ADDON_MENU_LABEL, mw)
        _action.triggered.connect(_on_menu_triggered)
        mw.form.menuTools.addAction(_action)


gui_hooks.main_window_did_init.append(_setup_ui)
