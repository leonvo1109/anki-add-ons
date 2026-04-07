# Implementierungs-Guide für zukünftige Features

## 1. Neuer AI-Provider (z.B. OpenAI API)

### Schritt 1: Provider-Klasse erstellen

```python
# providers_openai.py - bereits vorhanden als Stub
from .providers_base import AIProvider
from .models import GenerationResponse

class OpenAIProvider(AIProvider):
    def generate(self, prompt: str, temperature: float = 0.2) -> GenerationResponse:
        try:
            # import openai  # würde "pip install openai" benötigen
            # response = openai.ChatCompletion.create(...)
            
            logger.info(f"Generating with OpenAI model: {self.model}")
            # ... Implementation
            
            return GenerationResponse(
                success=True,
                content=content,
                metadata={"model": self.model, "provider": "openai"}
            )
        except Exception as exc:
            logger.error(f"OpenAI generation failed: {exc}")
            return GenerationResponse(success=False, error=str(exc))
```

### Schritt 2: Neuen Provider-Type hinzufügen

```python
# types.py - erweitern
class AIProviderType(str, Enum):
    GEMINI = "gemini"
    OPENAI = "openai"           # ← neue Zeile
    ANTHROPIC = "anthropic"
```

### Schritt 3: In Factory registrieren

Das ist bereits vorbereitet in `providers_factory.py`:

```python
_providers = {
    AIProviderType.GEMINI: GeminiProvider,
    AIProviderType.OPENAI: OpenAIProvider,  # ← wird automatisch gefunden
    AIProviderType.ANTHROPIC: AnthropicProvider,
}
```

### Schritt 4: Config erweitern

```python
# config.json - neue API-Key Felder hinzufügen
{
    "provider": "openai",
    "openai_api_key": "",
    "anthropic_api_key": ""
}

# config.md - Dokumentieren
**`openai_api_key`**: API-Schlüssel für OpenAI API...
```

### Schritt 5: ConfigModel anpassen

```python
# models.py
@dataclass
class ConfigModel:
    gemini_api_key: str = ""
    openai_api_key: str = ""      # ← neu
    anthropic_api_key: str = ""   # ← neu
```

### Schritt 6: Env-Var Support

Die `config_loader.py` automatisch erweitern:

```python
def load_config_from_dict(config_dict: dict[str, Any]) -> ConfigModel:
    # ... existing code ...
    
    # Environment variable overrides
    if openai_key := os.environ.get("OPENAI_API_KEY"):
        config.openai_api_key = openai_key
```

## 2. Batch Processing Optimierungen

### Parallele Kartenerstellung

```python
# card_generator.py - erweitern
from concurrent.futures import ThreadPoolExecutor

class CardGeneratorService:
    def batch_generate_parallel(self, topics: list[str], max_workers: int = 3) -> list[Card]:
        """Generate cards in parallel threads."""
        cards = []
        
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            futures = [
                executor.submit(self.generate_card, topic)
                for topic in topics[:self.config.max_cards_per_run]
            ]
            
            for future in futures:
                try:
                    card = future.result(timeout=30)
                    if card:
                        cards.append(card)
                except Exception as exc:
                    logger.error(f"Batch generation failed: {exc}")
        
        return cards
```

### Prompt-Caching

```python
# cache.py - neue Datei
from functools import lru_cache
from hashlib import md5

class PromptCache:
    def __init__(self, max_size: int = 100):
        self.cache = {}
        self.max_size = max_size
    
    def get(self, prompt: str) -> Optional[Card]:
        key = md5(prompt.encode()).hexdigest()
        return self.cache.get(key)
    
    def set(self, prompt: str, card: Card) -> None:
        if len(self.cache) >= self.max_size:
            # Remove oldest entry (simple FIFO)
            self.cache.pop(next(iter(self.cache)))
        
        key = md5(prompt.encode()).hexdigest()
        self.cache[key] = card
```

## 3. Deck Management Service

```python
# deck_manager.py - neue Datei
from typing import Optional
from aqt import mw

class DeckManager:
    """Manage Anki decks and card creation."""
    
    def __init__(self):
        self.col = mw.col
    
    def get_deck(self, deck_name: str) -> Optional[int]:
        """Get deck ID by name."""
        try:
            return self.col.decks.id(deck_name)
        except Exception as exc:
            logger.error(f"Deck not found: {deck_name}")
            return None
    
    def create_card(self, card: Card, deck_name: str, note_type: str) -> bool:
        """Create a card in Anki."""
        try:
            deck_id = self.get_deck(deck_name)
            if not deck_id:
                raise ValueError(f"Deck not found: {deck_name}")
            
            # Create note
            note = self.col.new_note()
            note['Front'] = card.question
            note['Back'] = card.answer
            
            # Add to deck
            self.col.add_note(note, deck_id)
            self.col.save()
            
            logger.info(f"Card created: {card.question[:50]}...")
            return True
            
        except Exception as exc:
            logger.error(f"Failed to create card: {exc}")
            return False
    
    def batch_create_cards(self, cards: list[Card], deck_name: str, note_type: str) -> int:
        """Create multiple cards."""
        created = 0
        for card in cards:
            if self.create_card(card, deck_name, note_type):
                created += 1
        
        logger.info(f"Created {created} cards out of {len(cards)}")
        return created
```

### Integration in ContainerBuilder

```python
# container.py - erweitern
from .deck_manager import DeckManager

class ContainerBuilder:
    @staticmethod
    def build(config_dict: dict[str, Any]) -> DIContainer:
        container = DIContainer()
        
        # ... existing code ...
        
        # Register deck manager
        deck_manager = DeckManager()
        container.register_singleton("deck_manager", deck_manager)
        
        return container
```

## 4. Note-Type Service

```python
# note_type_service.py - neue Datei
from aqt import mw
from typing import Optional, Dict, Any

class NoteTypeService:
    """Manage Anki note types and field mapping."""
    
    def __init__(self):
        self.col = mw.col
    
    def get_note_type(self, name: str) -> Optional[Dict[str, Any]]:
        """Get note type by name."""
        return self.col.models.byName(name)
    
    def get_fields(self, note_type_name: str) -> list[str]:
        """Get field names for note type."""
        note_type = self.get_note_type(note_type_name)
        if not note_type:
            return []
        return [field['name'] for field in note_type['flds']]
    
    def validate_fields(self, note_type_name: str, data: Dict[str, str]) -> bool:
        """Validate that all required fields are provided."""
        required_fields = self.get_fields(note_type_name)
        return all(field in data for field in required_fields)
    
    def map_card_to_fields(self, card: Card, note_type_name: str) -> Dict[str, str]:
        """Map Card object to note type fields."""
        fields = self.get_fields(note_type_name)
        
        # Simple mapping: Question → First field, Answer → Second field
        data = {}
        if len(fields) >= 1:
            data[fields[0]] = card.question
        if len(fields) >= 2:
            data[fields[1]] = card.answer
        
        return data
```

## 5. Erweiterte Logging & Monitoring

```python
# metrics.py - neue Datei
from dataclasses import dataclass, field
from datetime import datetime

@dataclass
class GenerationMetrics:
    """Track metrics for AI generation requests."""
    
    total_requests: int = 0
    successful_requests: int = 0
    failed_requests: int = 0
    total_tokens: int = 0
    average_response_time: float = 0.0
    errors: list[str] = field(default_factory=list)
    
    def record_success(self, response_time: float) -> None:
        self.successful_requests += 1
        self.total_requests += 1
    
    def record_failure(self, error: str) -> None:
        self.failed_requests += 1
        self.total_requests += 1
        self.errors.append(error)
    
    def success_rate(self) -> float:
        if self.total_requests == 0:
            return 0.0
        return self.successful_requests / self.total_requests * 100
```

## 6. UI Erweiterungen

### Batch-Input Dialog

```python
# ui.py - erweitern
class BatchGenerationDialog:
    """Dialog for batch card generation."""
    
    @staticmethod
    def create() -> QDialog:
        dialog = QDialog(mw)
        dialog.setWindowTitle("Batch Card Generation")
        
        layout = QVBoxLayout()
        
        # Topics input (textarea)
        topics_label = QLabel("Topics (eine pro Zeile):")
        topics_input = QTextEdit()
        topics_input.setPlaceholderText("Python\nJavaScript\nGo\n...")
        layout.addWidget(topics_label)
        layout.addWidget(topics_input)
        
        # Generate button
        button = QPushButton("Generate Cards")
        layout.addWidget(button)
        
        dialog.setLayout(layout)
        return dialog
```

## 7. Fehlerbehandlung & Recovery

```python
# resilience.py - neue Datei
from typing import Callable, Optional, TypeVar
import time

T = TypeVar('T')

class RetryPolicy:
    """Retry strategy for API calls."""
    
    def __init__(self, max_retries: int = 3, backoff_factor: float = 2.0):
        self.max_retries = max_retries
        self.backoff_factor = backoff_factor
    
    def execute(self, func: Callable[[], T]) -> Optional[T]:
        """Execute function with retry logic."""
        last_error = None
        
        for attempt in range(self.max_retries):
            try:
                return func()
            except Exception as exc:
                last_error = exc
                if attempt < self.max_retries - 1:
                    wait_time = self.backoff_factor ** attempt
                    logger.warning(f"Attempt {attempt + 1} failed, retrying in {wait_time}s...")
                    time.sleep(wait_time)
        
        logger.error(f"All {self.max_retries} attempts failed: {last_error}")
        return None
```

## Zusammenfassung der Architektur-Erweiterungen

| Feature | Datei | Status |
|---------|-------|--------|
| Multi-Provider Support | `providers_*.py` | ✅ Grundstruktur |
| Batch Processing | `card_generator.py` | ⚠️ Basis vorhanden |
| Prompt Caching | `cache.py` | ❌ Zu implementieren |
| Deck Management | `deck_manager.py` | ❌ Zu implementieren |
| Note-Type Handling | `note_type_service.py` | ❌ Zu implementieren |
| Metrics & Monitoring | `metrics.py` | ❌ Zu implementieren |
| Resilience & Retry | `resilience.py` | ❌ Zu implementieren |
| Batch UI Dialog | `ui.py` | ❌ Zu implementieren |

Alle diese Features können **modular und unabhängig** in die bestehende Architektur integriert werden, dank der sauberen Separation of Concerns! 🎯

