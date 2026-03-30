# Anki Add-ons Monorepo

Ein strukturiertes Repository für die Entwicklung und das Packaging von Anki-Add-ons, mit Build-Automatisierung, Development-Setup und CI/CD.

## Features

- 📦 **Monorepo-Layout**: Mehrere Add-ons im gleichen Repo verwaltbar
- 🔧 **Automated Build**: `scripts/build_all.py` mit Validierung
- 🧪 **Validierung**: Manifest-Prüfung, Paket-Integrität
- 🚀 **CI/CD**: GitHub Actions für automatische Builds
- 📝 **Konfigurierbar**: JSON-Configs + Markdown-Dokumentation pro Add-on
- 🔄 **Dev-Workflow**: Quick-Install direkt ins Anki-Addons-Verzeichnis

## Schnellstart

### Anforderungen

- Python 3.14+
- [uv](https://docs.astral.sh/uv/) (Fast Python package manager)
- Anki 25.9+

### Setup

```zsh
# Repository klonen
git clone <repo-url>
cd anki-add-ons

# Python-Umgebung initialisieren
uv sync

# (Optional) Mit Hatch CLI arbeiten
uv run hatch --version
```

### Add-on Entwickeln

```zsh
# Build + direkt installieren (schnellste Iteration)
uv run hatch run install-dev

# Dann Anki neustarten
```

Mehr Details in [`DEVELOPMENT.md`](DEVELOPMENT.md).

## Verfügbare Add-ons

### AI Flashcards

KI-gestützte Kartengenerierung mit konfigurierbarem LLM-Provider.

**Features:**
- Menüeintrag in Tools
- Sidebar-Tab mit Start-Button
- Konfigurierbare KI-Modelle und Deck-Ziele

**Dateien:**
- `packages/ai_flashcards/__init__.py`: Main-Logic
- `packages/ai_flashcards/config.json`: Standard-Konfiguration
- `packages/ai_flashcards/config.md`: User-Dokumentation
- `packages/ai_flashcards/manifest.json`: Anki-Metadaten

## Projektstruktur

```
anki-add-ons/
├── packages/
│   └── ai_flashcards/
│       ├── __init__.py           # Entry point
│       ├── manifest.json         # Anki-Metadaten
│       ├── config.json           # Standard-Config
│       ├── config.md             # User-Doku
│       └── user_files/           # Benutzerdaten (persistent)
├── scripts/
│   ├── build_all.py             # Build-Pipeline mit Validierung
│   └── install_dev.py           # Dev-Installation
├── build/                        # Generierte .ankiaddon Dateien
├── pyproject.toml               # Projekt-Konfiguration
├── uv.lock                      # Abhängigkeits-Lock
├── DEVELOPMENT.md               # Development-Guide
└── README.md                    # Diese Datei
```

## Build & Release

### Local Build

```zsh
python scripts/build_all.py
# Erzeugt: build/ai_flashcards.ankiaddon
```

### GitHub Actions

Bei Push/PR auf `main` wird automatisch:
1. Build ausgeführt (mit Validierung)
2. `.ankiaddon`-Dateien als Artifacts hochgeladen

Siehe: [`.github/workflows/build-addons.yml`](.github/workflows/build-addons.yml)

## Installation (Endbenutzer)

1. Download der `.ankiaddon`-Datei (von GitHub Releases oder manuell gebaut)
2. In Anki: Tools → Add-ons → Install from File
3. Anki neustarten

## Konfiguration

### AI Flashcards Config

**Datei:** `~/.local/share/Anki2/addons21/ai_flashcards/config.json` (Linux/macOS)

```json
{
  "enabled": true,
  "provider": "openai",
  "model": "gpt-4.1-mini",
  "target_deck": "Default",
  "note_type": "Basic",
  "max_cards_per_run": 10,
  "temperature": 0.2,
  "add_menu_entry": true
}
```

Für Details siehe: [`packages/ai_flashcards/config.md`](packages/ai_flashcards/config.md)

## Development

### Schnell-Commands

```zsh
# Build
hatch run build

# Build + Install
hatch run install-dev

# Format & Lint
hatch run fmt

# Type-Check
hatch run check
```

### Struktur eines neuen Add-ons

1. Ordner unter `packages/<addon-name>/` erstellen
2. Pflichtdateien hinzufügen:
   - `__init__.py`: Python-Entry-Point
   - `manifest.json`: Anki-Metadaten mit eindeutigem `package`-Feld
3. Optional:
   - `config.json`: Standard-Konfiguration
   - `config.md`: User-Dokumentation
   - `user_files/`: Benutzerdaten

### Validierung

Der Build validiert automatisch:
- `manifest.json` existiert und ist valides JSON
- `manifest.package` entspricht Ordnernamen
- `manifest.name` nicht leer, `manifest.mod` ist Integer
- `__init__.py` existiert

## Troubleshooting

### `ModuleNotFoundError: aqt`

```zsh
uv sync
```

### Add-on erscheint nicht in Anki

1. Build erfolgreich? → `python scripts/build_all.py`
2. Installiert? → `hatch run install-dev` + Anki neustarten
3. Enabled in Config? → `config.json` prüfen

### Build schlägt fehl

```zsh
python scripts/build_all.py  # Ausführliche Fehlermeldung
```

## Links

- [Anki Developer Hub](https://github.com/ankitects/anki)
- [AQT (Anki Qt Frontend)](https://github.com/ankitects/anki/tree/main/qt)
- [Anki Add-on Dokumentation](https://addon-docs.ankiweb.net/)

## License

[Bitte einfügen – z.B. MIT, GPL-3.0, etc.]

## Contributing

Siehe [`DEVELOPMENT.md`](DEVELOPMENT.md) für Details zum Setup und Workflow.

