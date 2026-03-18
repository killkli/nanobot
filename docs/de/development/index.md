# Entwicklungsdokumentation

Willkommen im nanobot-Entwicklungsbereich. Diese Sektion bietet Einblick in Architektur, Beitrag, und Plugin-Entwicklung.

## Inhaltsverzeichnis

| Dokument | Beschreibung |
|------|------|
| [Architektur](./architecture.md) | Systemdesign, Modulbeziehungen, Datenflüsse |
| [Beitragsleitfaden](./contributing.md) | Branch-Strategie, Code-Stil, Pull-Requests |
| [Kanal-Plugin-Entwicklung](./channel-plugin.md) | So entwickelst du eigene Chat-Plattform-Plugins |

## Schnellstart

### Umgebung einrichten

```bash
# Repository klonen
git clone https://github.com/HKUDS/nanobot.git
cd nanobot

# Abhängigkeiten installieren (inkl. Dev-Dependencies)
uv sync

# Tests ausführen
uv run pytest tests/

# Lokalen Agenten starten
uv run nanobot agent
```

### Kernprinzipien

nanobot verfolgt das Motto: „So wenig Code wie nötig für den Kern.“

- **Leichtgewichtig:** ~16k Python-Zeilen für kompletten Agenten
- **Asynchron:** umfassender Einsatz von `async/await`, keine blockierenden Aufrufe
- **Ereignisgesteuert:** Nachrichten gelangen über den Bus, Komponenten sind lose gekoppelt
- **Erweiterbar:** Plugins erlauben eigene Kanäle und Skills

## Projektstruktur

```
nanobot/
├── agent/          # Agenten-Logik
│   ├── loop.py     # Hauptloop (LLM ↔ Toolausführung)
│   ├── context.py  # Prompt-Erstellung
│   ├── memory.py   # Memory-Subsystem
│   └── tools/      # Tools-Implementierungen
├── bus/            # Nachrichtenbus
├── channels/       # Kanalimplementierungen (Plugin-Architektur)
├── providers/      # LLM-Provider
├── session/        # Gesprächsverwaltung
├── config/         # Pydantic-Schemata
├── skills/         # Eingebaute Skills
├── cron/           # Zeitpläne und Scheduler
└── heartbeat/      # Periodische Aufgaben
```

## Ressourcen

- [GitHub-Repository](https://github.com/HKUDS/nanobot)
- [Issues](https://github.com/HKUDS/nanobot/issues)
- [Discord-Community](https://discord.gg/MnCvHqpUGB)
- [Channel Plugin Guide (Englisch)](../CHANNEL_PLUGIN_GUIDE.md)
