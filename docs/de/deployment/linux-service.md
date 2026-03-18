# Linux-Systemd-Service

Dieser Guide zeigt, wie du nanobot gateway als systemd User Service betreibst – mit Auto-Start, automatischer Restart-Strategie und Journald-Integration.

## Warum systemd nutzen?

- **Autostart:** Gateway startet nach dem Login automatisch
- **Automatischer Neustart:** Bei Absturz startet systemd den Service neu
- **Zentraler Logzugriff:** Über `journalctl`
- **Standardbefehle:** `systemctl` steuert den Dienst

## Vorbereitung

### nanobot installieren

```bash
which nanobot
# Beispiel: /home/user/.local/bin/nanobot
```

Wenn nicht vorhanden:

```bash
pip install nanobot-ai
# oder mit uv
uv pip install nanobot-ai
```

### Onboarding ausführen

```bash
nanobot onboard
```

Folge dem Assistenten für API-Keys und Kanäle.

## systemd-Service anlegen

### Schritt 1: Pfad prüfen

```bash
which nanobot
# z. B. /home/user/.local/bin/nanobot
```

### Schritt 2: Service-Ordner anlegen

```bash
mkdir -p ~/.config/systemd/user
```

### Schritt 3: Service-Datei erstellen

Editiere `~/.config/systemd/user/nanobot-gateway.service`:

```ini
[Unit]
Description=Nanobot Gateway
After=network.target

[Service]
Type=simple
ExecStart=%h/.local/bin/nanobot gateway
Restart=always
RestartSec=10
NoNewPrivileges=yes
ProtectSystem=strict
ReadWritePaths=%h

[Install]
WantedBy=default.target
```

> `%h` expandiert zu deinem Home-Verzeichnis.

### Schritt 4: Service aktivieren

```bash
systemctl --user daemon-reload
systemctl --user enable --now nanobot-gateway
```

## Alltägliche Befehle

```bash
systemctl --user status nanobot-gateway
systemctl --user start nanobot-gateway
systemctl --user stop nanobot-gateway
systemctl --user restart nanobot-gateway
systemctl --user disable nanobot-gateway
```

## Logs beobachten

```bash
journalctl --user -u nanobot-gateway -f
journalctl --user -u nanobot-gateway -n 100
journalctl --user -u nanobot-gateway --since today
journalctl --user -u nanobot-gateway --since "2026-01-01 09:00" --until "2026-01-01 18:00"
journalctl --user -u nanobot-gateway -o json
```

## Service neu laden

Wenn du die Unit-Datei änderst:

```bash
vim ~/.config/systemd/user/nanobot-gateway.service
systemctl --user daemon-reload
systemctl --user restart nanobot-gateway
```

## Gateway nach Logout weiterlaufen lassen

Aktiviere lingering:

```bash
loginctl enable-linger $USER
loginctl show-user $USER | grep Linger
# Ausgabe: Linger=yes
```

## Mehrere Instanzen

Erstelle für jeden Channel eine Unit:

**Telegram:**

```ini
[Unit]
Description=Nanobot Gateway (Telegram)
After=network.target

[Service]
Type=simple
ExecStart=%h/.local/bin/nanobot gateway --config %h/.nanobot-telegram/config.json
Restart=always
RestartSec=10
NoNewPrivileges=yes
ProtectSystem=strict
ReadWritePaths=%h

[Install]
WantedBy=default.target
```

**Discord:**

```ini
[Unit]
Description=Nanobot Gateway (Discord)
After=network.target

[Service]
Type=simple
ExecStart=%h/.local/bin/nanobot gateway --config %h/.nanobot-discord/config.json --port 18791
Restart=always
RestartSec=10
NoNewPrivileges=yes
ProtectSystem=strict
ReadWritePaths=%h

[Install]
WantedBy=default.target
```

Aktivieren:

```bash
systemctl --user daemon-reload
systemctl --user enable --now nanobot-telegram
systemctl --user enable --now nanobot-discord
```

## Beispiel mit Environment-Variablen

```ini
[Unit]
Description=Nanobot Gateway
Documentation=https://github.com/HKUDS/nanobot
After=network-online.target
Wants=network-online.target

[Service]
Type=simple
ExecStart=%h/.local/bin/nanobot gateway
# Optional kannst du hier API-Keys setzen
# Environment=ANTHROPIC_API_KEY=sk-ant-xxx
# Environment=TELEGRAM_BOT_TOKEN=xxx
Restart=always
RestartSec=10
NoNewPrivileges=yes
ProtectSystem=strict
ReadWritePaths=%h
StandardOutput=journal
StandardError=journal

[Install]
WantedBy=default.target
```

## Environment-Varianten

**Empfohlen:** Konfiguration ergänzt um API-Keys.

```bash
vim ~/.nanobot/config.json
```

**Alternative mit EnvironmentFile:**

```ini
[Service]
EnvironmentFile=%h/.nanobot/nanobot.env
ExecStart=%h/.local/bin/nanobot gateway
```

```bash
# ~/.nanobot/nanobot.env
ANTHROPIC_API_KEY=sk-ant-xxx
TELEGRAM_BOT_TOKEN=xxx
```

## Troubleshooting

**Service startet nicht**

```bash
journalctl --user -u nanobot-gateway -n 50
/home/user/.local/bin/nanobot gateway
```

**Service rebootet ständig**

```bash
systemctl --user status nanobot-gateway
journalctl --user -u nanobot-gateway --since "5 minutes ago"
```

**Binary nicht gefunden**

```bash
which nanobot
pip show nanobot-ai | grep Location
# In Unit: ExecStart=/voller/pfad/nanobot gateway
```
