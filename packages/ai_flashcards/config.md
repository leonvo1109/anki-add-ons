# AI Flashcards

## Einstellungen

### Aktivierung
**`enabled`** (Boolean, Standard: `true`)
- Aktiviert oder deaktiviert das gesamte Add-on.

### KI-Anbieter & Modell
**`provider`** (String, Standard: `"openai"`)
- Name des KI-Anbieters (z.B. "openai", "gemini", "anthropic").

**`model`** (String, Standard: `"gemini-2.0-flash"`)
- Modellname für die KI-Anfragen (z.B. "gemini-2.0-flash", "gpt-4").

**`gemini_api_key`** (String, Standard: `""`)
- Dein API-Schlüssel für den KI-Anbieter.
- Beispiel: Erhalte deinen Schlüssel unter https://aistudio.google.com

### Karten-Einstellungen
**`target_deck`** (String, Standard: `""`)
- Name des Zieldecks, in dem neue Karten erstellt werden.
- Beispiel: `"Mein Deck"` oder `"Hauptdeck::Unterdeck"`

**`note_type`** (String, Standard: `""`)
- Der Notiztyp für neue Karten.
- Beispiel: `"Basis"`, `"Cloze"`, oder dein eigener Notiztyp.

### Generierung
**`max_cards_per_run`** (Zahl, Standard: `10`)
- Maximale Anzahl Karten, die pro Durchlauf generiert werden.
- Höhere Werte = mehr Karten, aber längere Verarbeitungszeit.

**`temperature`** (Dezimalzahl 0-1, Standard: `0.2`)
- Kreativität/Varianz der Ausgabe.
- `0` = deterministische Antworten (gleiche Prompts → gleiche Ergebnisse)
- `1` = sehr kreativ (variantenreich)

### UI-Einstellungen
**`add_menu_entry`** (Boolean, Standard: `true`)
- Fügt einen Menüeintrag "AI Flashcards" im Anki-Werkzeugmenü hinzu.
