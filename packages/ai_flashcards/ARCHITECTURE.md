# AI Flashcards - Architektur-Dokumentation

## Übersicht

Das AI Flashcards Add-on wurde in eine modulare, erweiterbare Architektur mit klarer Separation of Concerns refaktoriert. Die Struktur ermöglicht einfache Addition neuer KI-Provider, bessere Testbarkeit und zukünftige Features.

## Verzeichnisstruktur

```
packages/ai_flashcards/
├── __init__.py                  # Entry Point - minimal, Dependency Injection Setup
├── types.py                     # Enums und Type Definitions
├── models.py                    # Datenmodelle (Config, Card, Response)
├── exceptions.py                # Custom Exception-Hierarchie
├── logger.py                    # Logging Setup
├── config_loader.py             # Config-Laden + Env-Var Override
├── container.py                 # Dependency Injection Container
│
├── providers_base.py            # ABC für AI Provider
├── providers_gemini.py          # Gemini Implementation
├── providers_openai.py          # OpenAI Stub (für Zukunft)
├── providers_factory.py         # Provider Factory (Multi-Provider Support)
│
├── card_generator.py            # Card Generation Service
├── controller.py                # Event Handler + UI Logic
├── ui.py                        # UI Components (Widgets)
│
├── manifest.json                # Anki Addon Manifest
├── config.json                  # Default Config Values
└── config.md                    # Config Documentation
```

## Layer-Architektur

```
┌─────────────────────────────────────────────┐
│         Presentation Layer (UI)             │
│  ┌─────────────────────────────────────┐    │
│  │  UI Components (Qt Widgets)         │    │
│  │  - AIFlashcardsDockWidget           │    │
│  │  - MenuItemManager                  │    │
│  └────────────────┬────────────────────┘    │
│                   │                         │
│  ┌────────────────▼────────────────────┐    │
│  │  Controllers (Event Handlers)       │    │
│  │  - PromptController                 │    │
│  └────────────────┬────────────────────┘    │
└────────────────────┼──────────────────────────┘
                     │
┌────────────────────▼──────────────────────────┐
│     Business Logic Layer (Services)           │
│  ┌─────────────────────────────────────┐     │
│  │  CardGeneratorService               │     │
│  │  - generate_card()                  │     │
│  │  - batch_generate()                 │     │
│  │  - prompt parsing                   │     │
│  └────────────────┬────────────────────┘     │
│                   │                          │
│  ┌────────────────▼────────────────────┐     │
│  │  AI Provider Interface               │     │
│  │  - AIProvider (ABC)                  │     │
│  │  - GeminiProvider                    │     │
│  │  - OpenAIProvider (Stub)             │     │
│  │  - ProviderFactory                   │     │
│  └─────────────────────────────────────┘     │
└────────────────────┬──────────────────────────┘
                     │
┌────────────────────▼──────────────────────────┐
│  Infrastructure / Data Layer                  │
│  ┌─────────────────────────────────────┐     │
│  │  Configuration                       │     │
│  │  - ConfigModel (Dataclass)           │     │
│  │  - ConfigLoader (with Env Override)  │     │
│  └─────────────────────────────────────┘     │
│  ┌─────────────────────────────────────┐     │
│  │  Data Models                         │     │
│  │  - Card, GenerationResponse          │     │
│  └─────────────────────────────────────┘     │
│  ┌─────────────────────────────────────┐     │
│  │  Logging & Exceptions                │     │
│  │  - logger.py, exceptions.py          │     │
│  └─────────────────────────────────────┘     │
│  ┌─────────────────────────────────────┐     │
│  │  Dependency Injection                │     │
│  │  - DIContainer, ContainerBuilder      │     │
│  └─────────────────────────────────────┘     │
└──────────────────────────────────────────────┘
```

## Komponenten-Beschreibung

### 1. **Entry Point** (`__init__.py`)
Minimalistisch gehalten - nur noch Anki-Hook-Registrierung und DI-Setup.

```python
gui_hooks.main_window_did_init.append(_setup_ui)  # Hook nur noch hier
```

### 2. **Dependency Injection** (`container.py`)

Einfacher, selbstgeschriebener DI-Container (kein Framework nötig):

```python
container = ContainerBuilder.build(config_dict)
card_generator = container.get("card_generator")  # Lazy-loaded Service
provider = container.get("provider")               # AI Provider
```

**Vorteile:**
- Keine externe Dependency
- Einfache Testbarkeit (Mock-Services einfach injizierbar)
- Zentrale Service-Verwaltung

### 3. **Provider-System** (`providers_*.py`, `providers_factory.py`)

**ABC (Abstract Base Class):**
```python
class AIProvider(ABC):
    def generate(prompt: str, temperature: float) -> GenerationResponse
```

**Implementierungen:**
- `GeminiProvider` - Wraps Apple On-Device Model (bestehend)
- `OpenAIProvider` - Stub für Zukunft
- `AnthropicProvider` - Stub für Zukunft

**Factory-Pattern für Instantiierung:**
```python
provider = ProviderFactory.create(config)  # Selektiert Provider basierend auf Config
```

### 4. **Card Generation Service** (`card_generator.py`)

Orchestriert:
- AI-Provider Aufrufe
- Prompt Engineering
- Response Parsing
- Batch Processing

```python
service = CardGeneratorService(provider, config)
card = service.generate_card("Machine Learning")
cards = service.batch_generate(["ML", "DL", "NLP"])
```

### 5. **Configuration** (`models.py`, `config_loader.py`)

**Typed Config mit Validierung:**
```python
@dataclass
class ConfigModel:
    enabled: bool
    provider: str
    gemini_api_key: str
    # ... etc
    
    def validate(self) -> list[str]  # Returns validation errors
```

**Env-Var Override (bestehend, jetzt modular):**
```python
config = load_config_from_dict(anki_config)
# GEMINI_API_KEY env-var überschreibt config.json
```

### 6. **Controllers** (`controller.py`)

Event-Handler für UI Interaktionen:
```python
class PromptController:
    def on_prompt_click(self):
        # Holt Service aus Container
        card = self.card_generator.generate_card(prompt)
        # Display Result
```

### 7. **UI Components** (`ui.py`)

Qt-Widget Factories mit Service-Integration:
```python
dock_widget, controller = AIFlashcardsDockWidget.create(container)
```

## Design Patterns

### 1. **Dependency Injection**
- Alle Services über Container verfügbar
- Einfach zu mocken für Tests
- Zentrale Verwaltung

### 2. **Factory Pattern**
- `ProviderFactory` für Multi-Provider Support
- `AIFlashcardsDockWidget.create()` für Widget-Erstellung

### 3. **Strategy Pattern**
- AIProvider-Interface für pluggable Strategien
- Einfach neue Provider hinzufügen

### 4. **Dataclass/Typed Models**
- `ConfigModel`, `Card`, `GenerationResponse`
- Type-safe, validierbar

## Erweiterungspunkte für zukünftige Features

### 1. **Neue AI-Provider hinzufügen**

```python
# 1. Neue Provider-Klasse erstellen
class NewProvider(AIProvider):
    def generate(self, prompt: str, temperature: float) -> GenerationResponse:
        # Implementation

# 2. In Factory registrieren
ProviderFactory.register_provider(AIProviderType.NEW, NewProvider)
```

### 2. **Batch Processing** (Grundstruktur existiert)

```python
# In card_generator.py
def batch_generate(self, topics: list[str]) -> list[Card]:
    # Implementierung mit Optimierungen
    pass
```

### 3. **Deck Management** (vorbereitet)

```python
# Neuer Service: deck_manager.py
class DeckManager:
    def get_deck(self, name: str) -> Deck
    def create_cards_in_deck(self, cards: list[Card], deck: Deck)
```

### 4. **Note-Type Handling** (vorbereitet)

```python
# Neuer Service: note_type_service.py
class NoteTypeService:
    def validate_fields(self, note_type: str, fields: dict) -> bool
    def map_card_to_note(self, card: Card, note_type: str) -> Note
```

### 5. **Logging & Debugging**

Logger ist bereits integriert:
```python
from .logger import logger
logger.info("Message")
logger.error("Error", exc_info=True)
```

### 6. **Fehlerbehandlung**

Custom Exception-Hierarchie vorbereitet:
```python
try:
    provider.generate(...)
except AIProviderError as e:
    # Handle provider-spezifische Fehler
except ConfigurationError as e:
    # Handle config-Fehler
```

## Testing

Architektur unterstützt Unit-Testing:

```python
# Mock Provider für Tests
class MockProvider(AIProvider):
    def generate(self, prompt: str, temperature: float) -> GenerationResponse:
        return GenerationResponse(success=True, content="Q: Test\nA: Answer")

# Test Service mit Mock
provider = MockProvider(api_key="test", model="test")
service = CardGeneratorService(provider, config)
card = service.generate_card("Test Topic")
assert card.question == "Test"
```

## Migration vom alten Code

Die Refaktorierung ist **vollständig rückwärtskompatibel**:
- `__init__.py` registriert denselben Anki-Hook
- Konfiguration funktioniert wie vorher (mit Env-Var Overrides)
- Benutzer sehen keine Unterschiede in der UI

## Performance-Implikationen

- **Lazy Loading:** Services werden nur bei Bedarf instantiiert
- **No Overhead:** DI-Container ist minimal (~50 Zeilen)
- **Caching:** Singletons werden nach erstem Aufruf cached

## Zukünftige Optimierungen

1. **Async/Await Standardisierung**
   - Controllers könnten Qt-Events in async/await wrappen
   - Nicht-blocking UI während Generation

2. **Caching Layer**
   - Cache für häufige Prompts
   - Redis/SQLite für persistentes Caching

3. **Rate Limiting**
   - Integrierung in Provider-Interface
   - Pro API-Provider konfigurierbar

4. **Analytics & Monitoring**
   - Logged alle Generation requests
   - Metriken für Provider-Performance

---

**Zusammenfassung:** Saubere, modulare Architektur mit klarer Separation of Concerns, vorbereitet für zukünftige Features und einfach zu testen.

