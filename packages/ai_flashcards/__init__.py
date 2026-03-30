from __future__ import annotations

from typing import Any

from aqt import gui_hooks, mw
from aqt.qt import QAction

ADDON_MENU_LABEL = "AI Flashcards"
_action: QAction | None = None


def _config() -> dict[str, Any]:
    return mw.addonManager.getConfig(__name__) or {}

def on_trigger() -> None:
    config = _config()
    print("AI Flashcards gestartet")
    print(config)


def _setup_menu() -> None:
    global _action

    config = _config()
    if not config.get("enabled", True):
        return
    if not config.get("add_menu_entry", True):
        return
    if _action is not None:
        return

    action = QAction(ADDON_MENU_LABEL, mw)
    action.triggered.connect(on_trigger)
    mw.form.menuTools.addAction(action)
    _action = action


gui_hooks.main_window_did_init.append(_setup_menu)
