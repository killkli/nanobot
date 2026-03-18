# Schnellstart

Richten Sie nanobot in fünf Minuten ein und führen Sie Ihr erstes Gespräch mit dem KI-Assistenten.

---

## Schritt 1: nanobot installieren

=== "uv (empfohlen)"

    ```bash
    uv tool install nanobot-ai
    ```

=== "pip"

    ```bash
    pip install nanobot-ai
    ```

Prüfen Sie anschließend die Installation:

```bash
nanobot --version
```

!!! tip "Noch kein uv installiert?"
    Folgen Sie der [Installationsanleitung](installation.md), um uv und nanobot zu installieren.

---

## Schritt 2: Onboarding-Assistent starten

```bash
nanobot onboard
```

Der Assistent führt Sie durch die Erstkonfiguration und erzeugt folgende Dateien unter `~/.nanobot/`:

```
~/.nanobot/
├── config.json          # Hauptkonfiguration
└── workspace/
    ├── AGENTS.md        # Agenten-Instruction
    ├── USER.md          # Benutzerprofil
    ├── SOUL.md          # Agentenpersönlichkeit
    ├── TOOLS.md         # Werkzeugpräferenzen
    └── HEARTBEAT.md     # Periodische Aufgaben
```

!!! note "Schon eine Konfiguration vorhanden?"
    `nanobot onboard` überschreibt bestehende Einstellungen nicht, sondern ergänzt fehlende Felder.

---

## Schritt 3: API-Schlüssel und Modelle konfigurieren

Öffnen Sie `~/.nanobot/config.json` und tragen Sie Ihre LLM-API-Schlüssel sowie Modellwünsche ein.

```bash
# Mit einem beliebigen Editor öffnen
vim ~/.nanobot/config.json
# oder
nano ~/.nanobot/config.json
# oder
code ~/.nanobot/config.json
```

### API-Schlüssel setzen

Als Beispiel für global empfohlene [OpenRouter](https://openrouter.ai/keys):

```json
{
  "providers": {
    "openrouter": {
      "apiKey": "sk-or-v1-xxxxxxxxxxxx"
    }
  }
}
```

Weitere gängige Provider:

=== "Anthropic (Claude)"

    ```json
    {
      "providers": {
        "anthropic": {
          "apiKey": "sk-ant-xxxxxxxxxxxx"
        }
      }
    }
    ```

=== "OpenAI (GPT)"

    ```json
    {
      "providers": {
        "openai": {
          "apiKey": "sk-xxxxxxxxxxxx"
        }
      }
    }
    ```

=== "DeepSeek"

    ```json
    {
      "providers": {
        "deepseek": {
          "apiKey": "sk-xxxxxxxxxxxx"
        }
      }
    }
    ```

=== "Ollama (lokal)"

    ```json
    {
      "providers": {
        "ollama": {
          "apiBase": "http://localhost:11434"
        }
      },
      "agents": {
        "defaults": {
          "provider": "ollama",
          "model": "llama3.2"
        }
      }
    }
    ```

### Modell festlegen (optional)

Sie können ein Standardmodell vorgeben, andernfalls wählt nanobot automatisch je nach API-Schlüssel:

```json
{
  "agents": {
    "defaults": {
      "model": "anthropic/claude-sonnet-4-5",
      "provider": "openrouter"
    }
  }
}
```

### Minimalbeispiel für eine vollständige Konfiguration

```json
{
  "providers": {
    "openrouter": {
      "apiKey": "sk-or-v1-xxxxxxxxxxxx"
    }
  },
  "agents": {
    "defaults": {
      "model": "anthropic/claude-opus-4-5",
      "provider": "openrouter"
    }
  }
}
```

!!! warning "Schützen Sie Ihre API-Schlüssel"
    `config.json` enthält sensible Schlüssel. Committen Sie diese Datei niemals ins Versionskontrollsystem (z. B. git).

---

## Schritt 4: CLI-Konversation starten

```bash
nanobot agent
```

Sie sehen nun das interaktive Chat-Interface:

```
nanobot> Hallo! Wobei kannst du mir helfen?
```

nanobot bietet verschiedene Modi:

```bash
# Interaktiver Modus (Standard)
nanobot agent

# Einmalige Nachricht (nicht interaktiv)
nanobot agent -m "Wie wird das Wetter heute?"

# Antworten als reinen Text anzeigen
nanobot agent --no-markdown

# Ausführungsprotokolle anzeigen
nanobot agent --logs
```

Verlassen Sie den interaktiven Modus mit `exit`, `quit` oder `Ctrl+D`.

!!! tip "Glückwunsch!"
    Sie haben den Basis-Setup abgeschlossen. Weiter unten zeigen wir, wie Sie Telegram integrieren und per Smartphone mit nanobot chatten.

---

## Schritt 5: Telegram verbinden (optional)

Telegram ist der einfachste Chatkanal für Einsteiger.

### Telegram-Bot erstellen

1. Telegram öffnen und nach **@BotFather** suchen
2. `/newbot` senden
3. Anzeigenamen (z. B. `My Nanobot`) eingeben
4. Benutzernamen festlegen (muss auf `bot` enden, z. B. `my_nanobot_bot`)
5. BotFather liefert ein **Bot Token** im Format `1234567890:ABCdefGHIjklMNOpqrsTUVwxyz`

### Ihre Telegram User ID finden

Die User ID steht in den Telegram-Einstellungen als `@yourUserId`. Kopieren Sie den Wert ohne das `@`.

Alternativ: Senden Sie eine Nachricht an Ihren Bot, schauen Sie in die nanobot-Logs – dort erscheint die ID der sendenden Person.

### Konfiguration aktualisieren

Fügen Sie Folgendes zu `~/.nanobot/config.json` hinzu:

```json
{
  "channels": {
    "telegram": {
      "enabled": true,
      "token": "1234567890:ABCdefGHIjklMNOpqrsTUVwxyz",
      "allowFrom": ["your_telegram_user_id"]
    }
  }
}
```

| Feld | Beschreibung |
|------|--------------|
| `token` | Vom @BotFather erhaltenes Token |
| `allowFrom` | Liste der User IDs, die mit dem Bot kommunizieren dürfen (leer = niemand) |

!!! warning "Sicherheitshinweis"
    `allowFrom` beschränkt den Zugriff auf Ihren Bot. Verwenden Sie `["*"]` nur, wenn Sie den Bot öffentlich anbieten möchten, und achten Sie auf den API-Verbrauch.

---

## Schritt 6: Gateway starten

```bash
nanobot gateway
```

Nach dem Start sehen Sie zum Beispiel:

```
[nanobot] Gateway starting on port 18790
[nanobot] Telegram channel connected
[nanobot] Ready to receive messages
```

Jetzt können Sie Telegram öffnen und eine Nachricht an Ihren Bot schicken!

!!! note "Gateway vs. CLI"
    - `nanobot agent`: Lokaler CLI-Chat direkt im Terminal
    - `nanobot gateway`: Servermodus, nimmt Nachrichten aus Chatkanälen entgegen

---

## Vollständiges Konfigurationsbeispiel

Enthält Telegram als Kanal:

```json
{
  "providers": {
    "openrouter": {
      "apiKey": "sk-or-v1-xxxxxxxxxxxx"
    }
  },
  "agents": {
    "defaults": {
      "model": "anthropic/claude-opus-4-5",
      "provider": "openrouter"
    }
  },
  "channels": {
    "telegram": {
      "enabled": true,
      "token": "YOUR_TELEGRAM_BOT_TOKEN",
      "allowFrom": ["YOUR_TELEGRAM_USER_ID"]
    }
  }
}
```

---

## Nächster Schritt

- **Onboarding-Assistent verstehen**: [Details zum Onboarding](onboarding.md)
- **Weitere Chatkanäle verbinden**: [Kanäle dokumentation](../channels/index.md)
- **Mehr LLM-Provider konfigurieren**: [Providers-Dokument](../providers/index.md)
- **Werkzeuge & Skills erkunden**: [Tools & Skills](../tools-skills/index.md)
