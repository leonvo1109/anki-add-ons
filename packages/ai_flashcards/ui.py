from dataclasses import dataclass

from aqt import mw
from aqt.qt import QAction, QDialog, QDialogButtonBox, QLabel, QMenu, QVBoxLayout
from aqt.utils import qconnect


@dataclass
class UIState:
    menu: QMenu | None = None
    card_count_action: QAction | None = None


class UI:
    def __init__(self) -> None:
        self.state = UIState()
        self._build_menu()

    # ----- Setup -----

    def _build_menu(self) -> None:
        menu = QMenu("AI Flashcards", mw)
        mw.form.menubar.addMenu(menu)
        self.state.menu = menu

        action = QAction("Show card count", mw)
        qconnect(action.triggered, self.show_card_count_dialog)
        menu.addAction(action)
        self.state.card_count_action = action

    # ----- Event handlers -----

    def show_card_count_dialog(self) -> None:
        card_count = mw.col.card_count()

        dialog = QDialog(mw)
        dialog.setWindowTitle("Card Count")

        layout = QVBoxLayout(dialog)
        layout.addWidget(QLabel(f"Card count: {card_count}"))

        buttons = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok)
        buttons.accepted.connect(dialog.accept)
        layout.addWidget(buttons)

        dialog.exec()
