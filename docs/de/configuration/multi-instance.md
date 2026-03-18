# Multi-Instance Leitfaden

nanobot unterstützt mehrere gleichzeitig laufende Instanzen. Jede Instanz verwendet eigene Configs, Workspaces, Cron-Jobs und Laufzeitdaten – vollkommen isoliert.

---

## Wann braucht man mehrere Instanzen?

| Anwendungsfall | Beschreibung |
|----------------|--------------|
| **Unterschiedliche Plattformen** | Arbeit über Slack + WeCom, privat über Telegram + Discord |
| **Unterschiedliche Modelle** | Eine Instanz verwendet Claude für komplexe Tasks, eine andere ein lokales Ollama-Modell |
| **Getrennte Workspaces** | Teams oder Projekte erhalten eigene Workspaces und Memories |
| **Unterschiedliche Sicherheitsgrenzen** | Produktionsinstanz aktiviert `restrictToWorkspace`, Testinstanz bleibt offen |
| **Getrennte Cron-Jobs** | Jede Instanz pflegt ihre eigene Cron-Liste |

---

## Pfadregeln

Alle Laufzeitdaten leiten sich vom Config-Pfad ab:

| Element | Quelle | Beispiel |
|---------|--------|----------|
| Config | `--config` Flag | `~/.nanobot-work/config.json` |
| Workspace | `--workspace` oder `agents.defaults.workspace` | `~/.nanobot-work/workspace/` |
| Cron-Jobs | Config-Verzeichnis | `~/.nanobot-work/cron/` |
| Media & Runtime | Config-Verzeichnis | `~/.nanobot-work/media/` |

> [!NOTE]
> `--config` bestimmt die geladene Config. Der Workspace stammt standardmäßig aus `agents.defaults.workspace`. Mit `--workspace` kannst du temporär überschreiben, ohne die Datei zu ändern.

---

## Quickstart

### Schritt 1: Configs und Workspaces anlegen

```bash
nanobot onboard --config ~/.nanobot-work/config.json \
                --workspace ~/.nanobot-work/workspace

nanobot onboard --config ~/.nanobot-personal/config.json \
                --workspace ~/.nanobot-personal/workspace
```

Der Assistent schreibt den Workspace-Pfad dauerhaft in die jeweilige Config.

### Schritt 2: Configs editieren

Passe `~/.nanobot-work/config.json` und `~/.nanobot-personal/config.json` individuell an (Channels, Modelle, API-Keys).

### Schritt 3: Beide Instanzen starten

```bash
nanobot gateway --config ~/.nanobot-work/config.json
nanobot gateway --config ~/.nanobot-personal/config.json --port 18791
```

---

## Beispiel: Work vs. Personal

### Work-Instanz (`~/.nanobot-work/config.json`)

```json
{
  "agents": {
    "defaults": {
      "workspace": "~/.nanobot-work/workspace",
      "model": "anthropic/claude-opus-4-5",
      "maxTokens": 8192,
      "maxToolIterations": 40
    }
  },
  "channels": {
    "sendProgress": true,
    "sendToolHints": true,
    "slack": {
      "enabled": true,
      "botToken": "xoxb-WORK-BOT-TOKEN",
      "appToken": "xapp-WORK-APP-TOKEN",
      "allowFrom": ["U01234567", "U07654321"]
    },
    "wecom": {
      "enabled": true,
      "corpId": "YOUR_CORP_ID",
      "corpSecret": "YOUR_CORP_SECRET",
      "agentId": 1000001,
      "allowFrom": ["zhangsan", "lisi"]
    }
  },
  "providers": {
    "anthropic": {
      "apiKey": "sk-ant-work-key"
    }
  },
  "gateway": {
    "host": "0.0.0.0",
    "port": 18790
  },
  "tools": {
    "restrictToWorkspace": true,
    "exec": {
      "timeout": 60
    },
    "web": {
      "search": {
        "provider": "brave",
        "apiKey": "BSA-BRAVE-KEY"
      }
    }
  }
}
```

### Personal-Instanz (`~/.nanobot-personal/config.json`)

```json
{
  "agents": {
    "defaults": {
      "workspace": "~/.nanobot-personal/workspace",
      "model": "anthropic/claude-opus-4-5",
      "maxTokens": 8192
    }
  },
  "channels": {
    "sendProgress": true,
    "sendToolHints": false,
    "telegram": {
      "enabled": true,
      "token": "TELEGRAM-BOT-TOKEN",
      "allowFrom": ["MY_TELEGRAM_USER_ID"]
    },
    "discord": {
      "enabled": true,
      "token": "DISCORD-BOT-TOKEN",
      "allowFrom": ["MY_DISCORD_USER_ID"]
    }
  },
  "providers": {
    "anthropic": {
      "apiKey": "sk-ant-personal-key"
    }
  },
  "gateway": {
    "host": "0.0.0.0",
    "port": 18791
  },
  "tools": {
    "restrictToWorkspace": false,
    "web": {
      "search": {
        "provider": "duckduckgo"
      }
    }
  }
}
```

---

## CLI-Tests pro Instanz

```bash
nanobot agent -c ~/.nanobot-work/config.json -m "Hallo, Work-Instanz"
nanobot agent -c ~/.nanobot-personal/config.json -m "Hallo, Personal-Instanz"
nanobot agent -c ~/.nanobot-work/config.json -w /tmp/work-test -m "Test"
```

> [!NOTE]
> `nanobot agent` startet eine lokale CLI-Sitzung mit dem gewählten Config/Workspace und kommuniziert nicht mit laufenden Gateways.

---

## systemd für mehrere Instanzen

### Template-Service

```ini
[Unit]
Description=Nanobot AI Assistant - %i Instance
After=network.target
Wants=network-online.target

[Service]
Type=simple
User=YOUR_USER
Group=YOUR_GROUP
WorkingDirectory=/home/YOUR_USER
ExecStart=/home/YOUR_USER/.local/bin/nanobot gateway \
    --config /home/YOUR_USER/.nanobot-%i/config.json
Restart=on-failure
RestartSec=10
StandardOutput=journal
StandardError=journal
SyslogIdentifier=nanobot-%i
NoNewPrivileges=yes
ProtectSystem=strict
ReadWritePaths=/home/YOUR_USER/.nanobot-%i

[Install]
WantedBy=multi-user.target
```

### Instanzen starten

```bash
sudo systemctl daemon-reload
sudo systemctl enable --now nanobot@work
sudo systemctl enable --now nanobot@personal
sudo systemctl status nanobot@work
sudo systemctl status nanobot@personal
sudo journalctl -u nanobot@work -f
sudo journalctl -u nanobot@personal -f
```

### Separate Unit-Dateien

Erstelle `/etc/systemd/system/nanobot-work.service` mit angepasster Config.

---

## Minimal ohne Onboard

```bash
mkdir -p ~/.nanobot-work/workspace
mkdir -p ~/.nanobot-personal/workspace
cp ~/.nanobot/config.json ~/.nanobot-work/config.json
cp ~/.nanobot/config.json ~/.nanobot-personal/config.json
```

Passe dann:
1. `agents.defaults.workspace`
2. Channels mit eigenen Credentials
3. `gateway.port` (einzigartig pro Instanz)

---

## Isolation

| Daten | Isolation | Beschreibung |
|-------|-----------|--------------|
| Workspace | Eigene `workspace`-Ordner | Dateien bleiben getrennt |
| Memory | `memory/` im Workspace | Unterschiedliche Memory-Zusammenfassungen |
| Cron | `cron/` im Config-Ordner | Eigene Cron-Listen |
| Media | `media/` im Config-Ordner | Keine gemeinsamen Anhänge |
| API-Keys | Eigene Configs | Unterschiedliche Accounts möglich |

---

## FAQ

**Port-Konflikte?**\
Stelle sicher, dass `gateway.port` pro Config unterschiedlich ist oder verwende `--port` beim Start.

**Kann ich einen Workspace teilen?**\
Technisch möglich, aber riskant. Shared Workspaces vermischen Memories, Cron-Jobs und Dateien.

**Wie sehe ich laufende Instanzen?**\
```bash
lsof -i :18790
lsof -i :18791
nanobot status --config ~/.nanobot-work/config.json
nanobot status --config ~/.nanobot-personal/config.json
```

**Modelle dynamisch wechseln?**\
Fordere es direkt im Kanal an oder setze `--model` bei `nanobot agent` (nicht für laufende Gateways).