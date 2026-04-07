# Umgebungsvariablen Setup

## Für lokale Entwicklung / Tests

### 1. `.env` Datei erstellen

Kopiere `.env.example` zu `.env`:

```bash
cp .env.example .env
```

### 2. Deine Werte eintragen

Öffne `.env` und fülle deine Zugangsdaten ein:

```env
GEMINI_API_KEY=dein-api-schluessel-hier
```

### 3. Umgebungsvariablen beim Start laden

**Für `runanki.py`:**

```bash
# Laden und starten
export $(cat .env | xargs) && python runanki.py
```

Oder auf einer Zeile:

```bash
env $(cat .env | xargs) python runanki.py
```

**Alternative mit Python-Loader (empfohlen):**

Falls du `python-dotenv` installierst:

```bash
pip install python-dotenv
```

Dann kannst du in `runanki.py` am Anfang hinzufügen:

```python
from dotenv import load_dotenv
import os

load_dotenv()
```

## Verfügbare Umgebungsvariablen

Das Add-on unterstützt folgende Variablen (mit Priorität vor `config.json`):

| Variable | Beschreibung | Beispiel |
|----------|-------------|---------|
| `GEMINI_API_KEY` | API-Schlüssel für Gemini/Google AI | `AIzaSyD...` |
| `AI_FLASHCARDS_ENABLED` | Aktiviert/deaktiviert das Add-on | `true`, `false` |
| `AI_FLASHCARDS_PROVIDER` | KI-Anbieter | `gemini`, `openai` |
| `AI_FLASHCARDS_MODEL` | Modellname | `gemini-2.0-flash` |

## Workflow zum Testen

1. **Einmalig Setup:**
   ```bash
   cp .env.example .env
   # Bearbeite .env mit deinem API-Key
   ```

2. **Jedes Mal zum Starten:**
   ```bash
   env $(cat .env | xargs) python runanki.py
   ```

3. **Rebuild ist sicher:**
   ```bash
   python scripts/build_all.py  # dein API-Key bleibt lokal
   ```

Die Umgebungsvariablen sind **lokal** und **bleiben nicht in der Config gespeichert**. Sie werden beim Start geladen.

## Sicherheit

- `.env` ist in `.gitignore` und wird **nicht** committet ✅
- Umgebungsvariablen haben **Priorität** vor der config.json ✅
- API-Keys sind **niemals** im Repository ✅
- Beim Rebuild gehen deine lokalen Secrets **nicht verloren** ✅

