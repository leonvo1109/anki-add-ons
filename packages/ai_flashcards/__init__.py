from __future__ import annotations

from typing import Any

from aqt import gui_hooks, mw
from aqt.qt import QAction, QDockWidget, QWidget, QVBoxLayout, QLabel, QPushButton
from aqt.qt import Qt

ADDON_MENU_LABEL = "AI Flashcards"
_action: QAction | None = None
_dock_widget: QDockWidget | None = None


def _config() -> dict[str, Any]:
    return mw.addonManager.getConfig(__name__) or {}


def on_trigger() -> None:
    config = _config()
    print("AI Flashcards triggered")
    print(config)


def _create_dock_widget() -> QDockWidget:
    """Erstellt das Dock-Widget für den AI Flashcards Tab."""
    dock = QDockWidget(ADDON_MENU_LABEL, mw)
    widget = QWidget()
    layout = QVBoxLayout(widget)
    layout.setContentsMargins(10, 10, 10, 10)

    # Titel
    title = QLabel(ADDON_MENU_LABEL)
    title.setStyleSheet("font-weight: bold; font-size: 14px;")
    layout.addWidget(title)

    # Info-Text
    info = QLabel("Klick auf 'Starten' um Karten zu generieren.")
    layout.addWidget(info)

    # Start-Button
    button = QPushButton("Starten")
    button.clicked.connect(on_trigger)
    layout.addWidget(button)

    # Platzhalter für zukünftige Inhalte
    layout.addStretch()

    dock.setWidget(widget)
    return dock


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
        _action.triggered.connect(on_trigger)
        mw.form.menuTools.addAction(_action)


gui_hooks.main_window_did_init.append(_setup_ui)
