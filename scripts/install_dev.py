#!/usr/bin/env python3
"""
Installiert das gebaute Add-on ins lokale Anki-Addons-Verzeichnis.
Nützlich für schnelle Development-Zyklen.
"""

import shutil
import sys
from pathlib import Path

ANKI_ADDONS_DIRS = {
    "darwin": Path.home() / "Library" / "Application Support" / "Anki2" / "addons21",
    "linux": Path.home() / ".local" / "share" / "Anki2" / "addons21",
    "win32": Path.home() / "AppData" / "Roaming" / "Anki2" / "addons21",
}

ROOT = Path(__file__).resolve().parent.parent
BUILD_DIR = ROOT / "build"


def install_addon() -> None:
    import platform

    system = sys.platform
    addons_dir = ANKI_ADDONS_DIRS.get(system)

    if not addons_dir:
        print(f"Unsupported platform: {system}")
        sys.exit(1)

    if not addons_dir.exists():
        print(f"Anki addons directory not found: {addons_dir}")
        print("Bitte starte zuerst Anki, damit das Verzeichnis erstellt wird.")
        sys.exit(1)

    for addon_file in sorted(BUILD_DIR.glob("*.ankiaddon")):
        addon_name = addon_file.stem  # z.B. "ai_flashcards"
        addon_dir = addons_dir / addon_name

        print(f"Installing {addon_name}...")

        # Altes Add-on löschen
        if addon_dir.exists():
            print(f"  Removing old: {addon_dir}")
            shutil.rmtree(addon_dir)

        # Neues Add-on entpacken
        addon_dir.mkdir(parents=True, exist_ok=True)
        shutil.unpack_archive(addon_file, addon_dir)

        print(f"  Installed to: {addon_dir}")

    print("\nDone! Restart Anki to reload addons.")


if __name__ == "__main__":
    install_addon()

