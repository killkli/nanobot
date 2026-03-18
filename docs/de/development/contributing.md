# Beitragshinweise

## Repository-Struktur

```
nanobot/
├── agent/          # Kern-LLM-Loop
├── bus/            # Message Bus
├── channels/       # Channel-Implementierungen
├── config/          # Pydantic-Schema
├── providers/       # LLM Provider
├── skills/          # Skills im Workspace
├── tools/           # Tool-Implementierungen
└── cli/             # CLI-Kommandos
```

## Coding-Standards

- Verwende Python 3.11+ (Typisierung optional, aber willkommen)
- Halte Funktionen klein und gut testbar
- Nutze `black` und `ruff` für Formatierung/Linting
- Schreib Tests für neue Logik

## Pull Request Workflow

1. Forke das Repository
2. Erstelle ein Feature-Branch
3. Schreibe klar beschriftete Commits
4. Führe Tests lokal aus (`pytest`) und stelle sicher, dass sie bestehen
5. Öffne eine PR mit folgenden Angaben:
   - Ziel & Beschreibung
   - Relevante Tests
   - Falls nötig: Release Notes

## Code Reviews

- Verstehe die Änderungen vollständig
- Achte auf Klarheit und Lesbarkeit
- Stelle sicher, dass Tests vorhanden oder ergänzt wurden

## Dokumentation

- Ergänze docs/ beim Hinzufügen neuer Funktionen
- Halte Übersetzungen konsistent
- Nutze die bestehenden Docs-Stile (Kurze Absätze, Tabellen, Codeblöcke)
