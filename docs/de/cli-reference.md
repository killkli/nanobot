# CLI-Befehlsreferenz

Dieses Dokument beschreibt alle nanobot-Befehle ausführlich.

## Schnellübersicht

| Befehl | Beschreibung |
|--------|--------------|
| `nanobot --version` | Versionsnummer anzeigen |
| `nanobot --help` | Hilfe ausgeben |
| `nanobot onboard` | Interaktives Setup von Konfiguration & Workspace |
| `nanobot onboard -c <pfad> -w <pfad>` | Konfiguration/Workspace eines spezifischen Instances initialisieren oder aktualisieren |
| `nanobot agent` | Interaktiver Chatmodus |
| `nanobot agent -m "..."` | Einmalige Nachricht (non-interactive) |
| `nanobot agent --no-markdown` | Antwort im Nur-Text-Format anzeigen |
| `nanobot agent --logs` | Tools-Logs während des Chats anzeigen |
| `nanobot gateway` | Gateway-Service starten (verbindet Chatkanäle) |
| `nanobot gateway --port <zahl>` | Gateway auf einem spezifischen Port starten |
| `nanobot status` | Konfigurations- und Verbindungsstatus anzeigen |
| `nanobot channels login` | WhatsApp-QR-Code-Login |
| `nanobot channels status` | Status aller Kanäle anzeigen |
| `nanobot plugins list` | Alle installierten Kanal-Plugins auflisten |
| `nanobot provider login <anbieter>` | OAuth-Login (openai-codex, github-copilot) |

---

## `nanobot` — Hauptbefehl

```
nanobot [OPTIONS] COMMAND [ARGS]...
```

Die zentrale Einstiegsschnittstelle von nanobot.

### Globale Optionen

| Option | Beschreibung |
|--------|--------------|
| `--version`, `-v` | Version anzeigen und beenden |
| `--help` | Hilfe anzeigen |

### Beispiele

```bash
# Version anzeigen
nanobot --version

# Alle Befehle auflisten
nanobot --help
```

---

## `nanobot onboard`

```
nanobot onboard [OPTIONS]
```

Interaktives Setup von Konfiguration und Workspace. Der Wizard fragt nach LLM-Anbietern, API-Schlüsseln und Basiseinstellungen.

### Optionen

| Option | Standard | Beschreibung |
|--------|----------|--------------|
| `-c`, `--config PFAD` | `~/.nanobot/config.json` | Pfad zur Konfigurationsdatei |
| `-w`, `--workspace PFAD` | `~/.nanobot/workspace` | Workspace-Verzeichnis |
| `--non-interactive` | `false` | Wizard überspringen und direkt (mit Defaults) erzeugen |

### Verhalten

- **Interaktiv (Standard):** Wizard führt Schritt für Schritt durch API-Schlüssel, Model-Setup und Kanaloptionen.
- **Nicht-interaktiv (`--non-interactive`):** Bestehende Konfiguration wird nur ergänzt, nicht überschrieben; bei fehlender Datei wird sie mit Defaults erzeugt.

### Beispiele

```bash
# Erstes Setup mit Wizard
nanobot onboard

# Spezifische Instanz initialisieren
nanobot onboard --config ~/.nanobot-telegram/config.json --workspace ~/.nanobot-telegram/workspace

# Nicht-interaktives Default-Setup
nanobot onboard --non-interactive

# Nicht-interaktive Initialisierung mit benutzerdefiniertem Pfad
nanobot onboard -c ~/my-nanobot/config.json --non-interactive
```

### Nächste Schritte

```bash
# Setup testen
nanobot agent -m "Hello!"

# Gateway starten
nanobot gateway
```

---

## `nanobot agent`

```
nanobot agent [OPTIONS]
```

Direkter Dialog mit dem AI-Agenten. Unterstützt Einmalnachrichten und interaktive Chats.

### Optionen

| Option | Standard | Beschreibung |
|--------|----------|--------------|
| `-m`, `--message TEXT` | — | Einmalnachricht (non-interactive). Danach beendet sich der Prozess. |
| `-c`, `--config PFAD` | `~/.nanobot/config.json` | Konfigurationsdatei |
| `-w`, `--workspace PFAD` | Wert aus der Konfiguration | Alternative Workspace-Pfad (überschreibt config) |
| `-s`, `--session TEXT` | `cli:direct` | Session-ID |
| `--markdown` / `--no-markdown` | `--markdown` | Antwort als Markdown rendern oder nicht |
| `--logs` / `--no-logs` | `--no-logs` | Tools-Logs während des Chats anzeigen |

### Interaktive Tastenkürzel

| Taste / Befehl | Funktion |
|---------------|----------|
| `exit`, `quit`, `:q` | Dialog verlassen |
| `Ctrl+D` | Dialog verlassen |
| `Ctrl+C` | Dialog verlassen |
| Pfeiltasten ↑/↓ | Verlauf durchsuchen |
| Mehrzeilige Eingabe (bracketed paste) | Wird automatisch unterstützt |

### Beispiele

```bash
# Einmalnachricht
nanobot agent -m "Wie ist das Wetter heute?"

# Interaktiver Chat
nanobot agent

# Mit bestimmter Konfiguration
nanobot agent --config ~/.nanobot-telegram/config.json

# Mit bestimmtem Workspace
nanobot agent --workspace /tmp/nanobot-test

# Config + Workspace kombinieren
nanobot agent -c ~/.nanobot-telegram/config.json -w /tmp/nanobot-telegram-test

# Nur Text (kein Markdown)
nanobot agent --no-markdown

# Tools-Logs anzeigen
nanobot agent --logs

# Einmalnachricht mit Logs
nanobot agent -m "Liste Dateien auf" --logs
```

---

## `nanobot gateway`

```
nanobot gateway [OPTIONS]
```

Startet den Gateway-Service, verbindet alle aktivierten Kanäle (Telegram, Discord, Slack, WhatsApp etc.) und verwaltet Cron/Heartbeat-Aufgaben.

### Optionen

| Option | Standard | Beschreibung |
|--------|----------|--------------|
| `-c`, `--config PFAD` | `~/.nanobot/config.json` | Konfigurationspfad |
| `-w`, `--workspace PFAD` | Wert aus der Konfiguration | Workspace (überschreibt config) |
| `-p`, `--port INT` | Wert aus der Konfiguration | Gateway-HTTP-Port |
| `-v`, `--verbose` | `false` | Detaillierte Debug-Logs aktivieren |

### Beispiele

```bash
# Gateway starten (Standard)
nanobot gateway

# Gateway mit anderem Port
nanobot gateway --port 18792

# Gateway mit spezifischer Config (Multi-Instance)
nanobot gateway --config ~/.nanobot-telegram/config.json

# Mehrere Instanzen gleichzeitig
nanobot gateway --config ~/.nanobot-telegram/config.json &
nanobot gateway --config ~/.nanobot-discord/config.json &
nanobot gateway --config ~/.nanobot-feishu/config.json --port 18792 &

# Debug-Logs aktivieren
nanobot gateway --verbose
```

### Was nach dem Start angezeigt wird

- Liste der aktivierten Kanäle
- Anzahl geplanter Cron-Aufgaben
- Heartbeat-Intervalle

---

## `nanobot status`

```
nanobot status
```

Zeigt Konfigurations-, Workspace- und Modellstatus sowie API-Schlüssel-Informationen der LLM-Provider an.

### Beispiel

```bash
nanobot status
```

### Mögliche Ausgabe

```
🐈 nanobot Status

Config: /Users/yourname/.nanobot/config.json ✓
Workspace: /Users/yourname/.nanobot/workspace ✓
Model: openrouter/anthropic/claude-3.5-sonnet
OpenRouter: ✓
Anthropic: nicht gesetzt
OpenAI: nicht gesetzt
```

---

## `nanobot channels`

```
nanobot channels COMMAND [ARGS]...
```

Verwaltet Chatkanäle über Unterbefehle.

### `nanobot channels login`

```
nanobot channels login
```

Startet WhatsApp-Login via QR-Code. Läuft automatisch bei ersten Login oder Re-Autorisierung.

Wenn der Node.js-Bridge noch nicht installiert ist, lädt der Befehl sie automatisch herunter und baut sie.

**Voraussetzungen:**
- Node.js ≥ 18
- npm

**Beispiele:**

```bash
# Erstes WhatsApp-Login
nanobot channels login

# Bridge neu bauen nach Upgrade
aiming
rm -rf ~/.nanobot/bridge && nanobot channels login
```

---

### `nanobot channels status`

```
nanobot channels status
```

Zeigt alle entdeckten Kanäle (eingebaut + Plugins) in Tabellenform mit Aktivierungsstatus an.

**Beispiel:**

```bash
nanobot channels status
```

**Ausgabe:**

```
        Channel Status
┌──────────────┬─────────┐
│ Channel      │ Enabled │
├──────────────┼─────────┤
│ Telegram     │ ✓       │
│ Discord      │ ✗       │
│ Slack        │ ✗       │
│ WhatsApp     │ ✓       │
└──────────────┴─────────┘
```

---

## `nanobot plugins`

```
nanobot plugins COMMAND [ARGS]...
```

Verwaltet Kanal-Plugins.

### `nanobot plugins list`

```
nanobot plugins list
```

Listet alle erkannten Kanäle (eingebaute + Plugins) inklusive Name, Quelle und Status.

**Beispiel:**

```bash
nanobot plugins list
```

---

## `nanobot provider`

```
nanobot provider COMMAND [ARGS]...
```

Verwaltet LLM-Provider.

### `nanobot provider login`

```
nanobot provider login PROVIDER
```

Startet OAuth-Login für einen Provider.

**Parameter:**

| Parameter | Beschreibung |
|-----------|--------------|
| `PROVIDER` | Name des Providers (siehe Tabelle) |

**Unterstützte OAuth-Provider:**

| Provider | Beschreibung |
|----------|--------------|
| `openai-codex` | OpenAI Codex (OAuth) |
| `github-copilot` | GitHub Copilot (Device Flow) |

**Beispiele:**

```bash
# OpenAI Codex login
nanobot provider login openai-codex

# GitHub Copilot login
nanobot provider login github-copilot
```

---

## Multi-Instance-Betrieb

nanobot unterstützt mehrere gleichzeitig laufende Instanzen mit separaten Konfigurationen/Workspaces. Verwenden Sie `--config` als Trennkriterium.

### Schnellsetup

```bash
# Instanzen initialisieren
nanobot onboard --config ~/.nanobot-telegram/config.json --workspace ~/.nanobot-telegram/workspace
nanobot onboard --config ~/.nanobot-discord/config.json --workspace ~/.nanobot-discord/workspace
nanobot onboard --config ~/..nanobot-feishu/config.json --workspace ~/.nanobot-feishu/workspace

# Gateways für jede Instanz starten
nanobot gateway --config ~/.nanobot-telegram/config.json
nanobot gateway --config ~/.nanobot-discord/config.json
nanobot gateway --config ~/.nanobot-feishu/config.json --port 18792
```

### `nanobot agent` pro Instanz

```bash
# Eine Nachricht an eine bestimmte Instanz senden
nanobot agent -c ~/.nanobot-telegram/config.json -m "Hello from Telegram instance"
nanobot agent -c ~/.nanobot-discord/config.json -m "Hello from Discord instance"

# Workspace überschreiben (Testlauf)
nanobot agent -c ~/.nanobot-telegram/config.json -w /tmp/nanobot-telegram-test
```

### Pfauflösung

| Element | Quelle |
|---------|--------|
| Konfiguration | Pfad von `--config` |
| Workspace | `--workspace` überschreibt `agents.defaults.workspace` |
| Laufzeitdaten (Cron, Media, State) | Abgeleitet vom Konfigurationsverzeichnis |
```}{