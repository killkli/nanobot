# Onboarding-Assistent

`nanobot onboard` ist der interaktive Setup-Assistent, der Konfiguration und Workspace-Vorlagen erstellt, damit Sie sofort loslegen können.

---

## Was der Assistent erledigt

Beim Start von `nanobot onboard` erledigt der Wizard Folgendes:

1. **Legt die Konfiguration an** (`~/.nanobot/config.json`, falls noch nicht vorhanden)
2. **Erstellt das Workspace-Verzeichnis** (`~/.nanobot/workspace/`)
3. **Generiert Vorlagendateien** (AGENTS.md, USER.md, SOUL.md, TOOLS.md, HEARTBEAT.md)
4. **Fragt Basiseinstellungen ab** (LLM-Provider, Modell usw.)

!!! note "Sichere Wiederholung"
    `nanobot onboard` überschreibt bestehende Dateien nicht. Fehlende Einträge werden ergänzt.

---

## Assistent starten

```bash
nanobot onboard
```

Der Wizard führt Sie Schritt für Schritt durch die Einstellungen. Am Ende stehen alle benötigten Dateien bereit.

---

## Speicherorte der Dateien

### Standardpfade

| Datei / Verzeichnis | Pfad |
|--------------------|------|
| **Konfiguration** | `~/.nanobot/config.json` |
| **Workspace** | `~/.nanobot/workspace/` |
| **Cron-Jobs** | `~/.nanobot/cron/` |
| **Medien / Status** | `~/.nanobot/media/` |

### Eigene Pfade

Sie können mit den Flags `-c` (`--config`) und `-w` (`--workspace`) eigene Pfade angeben, ideal für Multi-Instance-Setups:

```bash
nanobot onboard --config ~/.nanobot-telegram/config.json \
                --workspace ~/.nanobot-telegram/workspace

nanobot onboard --config ~/.nanobot-discord/config.json \
                --workspace ~/.nanobot-discord/workspace
```

!!! tip "Mehrere Instanzen"
    Mit unterschiedlichen `--config`-Paaren betreiben Sie mehrere Nanobot-Instanzen gleichzeitig, z. B. für verschiedene Channels. Siehe [Multi-Instance Deployment](../configuration/multi-instance.md).

---

## Struktur der `config.json`

Die vom Assistenten erzeugte Konfiguration sieht typischerweise so aus:

```json
{
  "providers": {
    "openrouter": {
      "apiKey": ""
    }
  },
  "agents": {
    "defaults": {
      "model": "anthropic/claude-opus-4-5",
      "provider": "openrouter",
      "workspace": "~/.nanobot/workspace"
    }
  },
  "channels": {},
  "tools": {
    "restrictToWorkspace": false
  },
  "gateway": {
    "port": 18790
  }
}
```

### Wichtige Felder

| Feld | Bedeutung |
|------|-----------|
| `providers.<name>.apiKey` | API-Schlüssel für den jeweiligen LLM-Provider |
| `agents.defaults.model` | Standardmodell |
| `agents.defaults.provider` | Standardprovider (`"auto"` erkennt automatisch) |
| `agents.defaults.workspace` | Workspace-Pfad |
| `channels.<name>.enabled` | Kanal aktivieren |
| `tools.restrictToWorkspace` | Tools auf den Workspace beschränken |
| `gateway.port` | HTTP-Port des Gateways (Standard 18790) |

---

## Workspace-Vorlagen

Der Assistent erzeugt unter `~/.nanobot/workspace/` folgende Dateien, die als Systemprompt für den Agenten dienen:

### AGENTS.md — Agenten-Anweisungen

Definiert Verhalten, Fähigkeiten und Grenzen des Agenten.

```markdown
# Agent Instructions

You are a helpful personal AI assistant powered by nanobot.

## Capabilities
- Answer questions and provide information
- Help with coding, writing, and analysis
- Execute shell commands and manage files
- Search the web for current information

## Guidelines
- Be concise and helpful
- Ask for clarification when needed
- Respect user privacy
```

**Zweck:** Legen Sie den Antwortstil und die Spezialisierung des Agenten fest.

### USER.md — Benutzerprofil

Beschreibt Ihren Hintergrund, Präferenzen und häufige Informationen.

```markdown
# User Profile

## About Me
- Name: [Your Name]
- Location: [Your City/Timezone]
- Occupation: [Your Role]

## Preferences
- Language: Traditional Chinese preferred
- Response style: Concise and practical

## Frequently Used
- Work directory: ~/projects
- Preferred editor: vim
```

**Zweck:** Vermeidung wiederholter Erklärungen und Anpassung an Ihre Favoriten.

### SOUL.md — Persönlichkeit des Agenten

Definiert Tonfall und Charakterzüge.

```markdown
# Soul

You have a friendly, professional personality.
You are curious, helpful, and direct.
You communicate clearly and adapt your tone to the conversation.
```

**Zweck:** Kontrollieren Sie den Stil der Antworten.

### TOOLS.md — Werkzeugrichtlinien

Beschreibt die Verwendung von Werkzeugen durch den Agenten.

```markdown
# Tool Usage Guidelines

## Shell Commands
- Always explain what a command does before running it
- Ask for confirmation before destructive operations

## Web Search
- Search for current information when needed
- Cite sources when providing factual information

## File Operations
- Work within the workspace directory by default
- Create backups before modifying important files
```

**Zweck:** Regeln für Tool- und Datenzugriff.

### HEARTBEAT.md — Periodische Aufgaben

Definiert Aufgaben, die der Gateway alle 30 Minuten automatisch ausführt.

```markdown
## Periodic Tasks

- [ ] Check weather forecast and send a summary
- [ ] Scan inbox for urgent emails
```

!!! info "Heartbeat-Funktion"
    Das Gateway liest alle 30 Minuten `HEARTBEAT.md`, führt die Aufgaben aus und sendet die Ergebnisse an den zuletzt aktiven Kanal.

    **Hinweis:** Gateway (`nanobot gateway`) muss laufen und Sie müssen dem Agenten mindestens eine Nachricht gesendet haben, damit er weiß, wohin er antworten soll.

---

## Workspace anpassen

Workspace-Dateien sind Markdown-to-Text und können direkt bearbeitet werden:

```bash
# Agentenrichtlinien bearbeiten
vim ~/.nanobot/workspace/AGENTS.md

# Benutzerprofil aktualisieren
vim ~/.nanobot/workspace/USER.md

# Periodische Aufgaben definieren
vim ~/.nanobot/workspace/HEARTBEAT.md
```

### Häufige Anpassungen

**Nur chinesisch antworten:**

Fügen Sie in `AGENTS.md` ein:

```markdown
## Language
Always respond in Traditional Chinese (繁體中文) unless the user writes in another language.
```

**Werkzeugnutzung limitieren:**

```markdown
## Security
- Never execute shell commands without explicit user approval
- Do not access files outside the workspace directory
```

**Fachgebiete festlegen:**

```markdown
## Expertise
You specialize in Python development and data analysis.
Prioritize clean, Pythonic code and provide explanations for complex algorithms.
```

**Tägliche Zusammenfassung:**

```markdown
## Periodic Tasks

- [ ] Every morning at 9am: Check today's calendar events and send a summary
- [ ] Every evening at 6pm: Summarize today's news in Traditional Chinese
```

### Vorlagen synchronisieren

!!! tip "Vorlagen-Updates"
    Nach einem nanobot-Update können neue Felder in den Vorlagen hinzugefügt werden. `nanobot onboard` aktualisiert die Vorlagen, ohne bestehende Inhalte zu überschreiben.

---

## Flags `-c` und `-w`

Alle nanobot-Befehle unterstützen `-c` (`--config`) und `-w` (`--workspace`), um flexibel zwischen Instanzen zu wechseln.

### `-c` / `--config`

```bash
# Gateway mit spezifischer Konfiguration starten
nanobot gateway --config ~/.nanobot-telegram/config.json

# CLI-Chat mit anderer Konfiguration
a
anobot agent --config ~/.nanobot-discord/config.json -m "Hello!"
```

### `-w` / `--workspace`

```bash
# Test-Workspace nutzen
nanobot agent --workspace /tmp/nanobot-test

# Kombination mit Custom-Config
nanobot agent --config ~/.nanobot-telegram/config.json \
              --workspace /tmp/nanobot-telegram-test
```

!!! note "Flag-Priorität"
    `--workspace` überschreibt `agents.defaults.workspace` im config nur für den laufenden Befehl.

### Beispiel: Mehrere Instanzen

```bash
# Telegram-Instanz erstellen
nanobot onboard \
  --config ~/.nanobot-telegram/config.json \
  --workspace ~/.nanobot-telegram/workspace

# Discord-Instanz erstellen
nanobot onboard \
  --config ~/.nanobot-discord/config.json \
  --workspace ~/.nanobot-discord/workspace

# Gateways starten (unterschiedliche Ports)
nanobot gateway --config ~/.nanobot-telegram/config.json
nanobot gateway --config ~/.nanobot-discord/config.json --port 18791
```

---

## Ablauf des Onboardings

```
nanobot onboard
    ↓
~/.nanobot/config.json erstellen
    ↓
~/.nanobot/workspace/
    ├── AGENTS.md
    ├── USER.md
    ├── SOUL.md
    ├── TOOLS.md
    └── HEARTBEAT.md
    ↓
Config editieren und API-Schlüssel hinzufügen
    ↓
(Optional) Workspace-Vorlagen anpassen
    ↓
nanobot agent   ← CLI-Chat
nanobot gateway ← Kanal-Server starten
```

---

## Nächste Schritte

- **Schnellstart durchlaufen**: [5-Minuten-Anleitung](quick-start.md)
- **Chatkanäle anbinden**: [Kanalübersicht](../channels/index.md)
- **LLM-Provider einrichten**: [Providers-Dokument](../providers/index.md)
