# Bereitstellungsübersicht

Dieser Abschnitt erklärt, wie du nanobot in unterschiedlichen Umgebungen betreibst und welcher Deploy-Modus sich wann eignet.

## Vergleich der Deploy-Optionen

| Modus | Kommando | Wann einsetzen | Persistenz |
|------|----------|----------------|------------|
| **CLI-Agent** | `nanobot agent` | Einzelne Chats, Tests, Skripts | Keine, endet nach Ausführung |
| **Gateway-Service** | `nanobot gateway` | Dauerbetrieb mit Chatplattformen | Muss manuell oder über Systemdienste am Laufen gehalten werden |
| **Docker** | `docker compose up -d` | Containerisierte Umgebung, CI/CD | `restart: unless-stopped` sorgt für Persistenz |
| **systemd-Service** | `systemctl --user start nanobot-gateway` | Linux-Server, Autostart | Systemdienst mit automatischer Wiederaufnahme |

## Details zu den Modi

### CLI-Agent (`nanobot agent`)

Ideal für schnelle Tests oder einmalige Gespräche. Der Prozess endet nach Beendigung der Konversation.

```bash
nanobot agent -m "Wie wird das Wetter heute?"
```

> **Hinweis:** `nanobot agent` startet eine lokale CLI-Sitzung und verbindet sich nicht mit einem laufenden `nanobot gateway`.

### Gateway-Service (`nanobot gateway`)

Das Gateway ist der zentrale Service, der alle aktivierten Kanäle (Telegram, Discord, Slack usw.) verbindet, Nachrichten entgegennimmt und durch den Agenten verarbeiten lässt.

Siehe auch: [Gateway-Service Anleitung](./gateway.md)

### Docker

Perfekt für isolierte Deployments oder Hosts ohne native Python-Umgebung.

Siehe auch: [Docker-Deploy-Anleitung](./docker.md)

### Linux systemd-Service

Für langfristigen Betrieb auf Linux-Servern: Autostart, Crash-Neustart und Integration mit dem Systemjournal.

Siehe auch: [Linux-Service Anleitung](./linux-service.md)

## Entwicklungs- vs. Produktionsumgebung

### Empfehlungen für die Entwicklung

- Nutze `nanobot agent` für schnelle Tests
- Starte `nanobot gateway` im Vordergrund, um Logs direkt zu sehen
- Setze `"restrictToWorkspace": false`, um Debugging zu erleichtern

```bash
nanobot gateway
```

### Empfehlungen für die Produktion

- Docker Compose oder systemd, um Gateway dauerhaft laufen zu lassen
- Aktiviere `"restrictToWorkspace": true`, um den Workspace einzuschränken
- Nutze `journalctl` oder `docker compose logs` für zentrales Logging
- Konfiguriere automatische Neustarts (`Restart=always` oder `restart: unless-stopped`)

```bash
docker compose up -d nanobot-gateway
systemctl --user enable --now nanobot-gateway
```

## Konfigurationsdateien

Alle Deploy-Optionen verwenden dieselbe Konfiguration:

```
~/.nanobot/config.json          # Hauptkonfiguration
~/.nanobot/workspace/           # Workspace-Verzeichnis
~/.nanobot/workspace/HEARTBEAT.md  # Periodische Aufgaben
```

Starte das Onboarding:

```bash
nanobot onboard
```

## Weiterführende Links

- [Gateway-Service Anleitung](./gateway.md)
- [Docker-Deploy-Anleitung](./docker.md)
- [Linux-Service Anleitung](./linux-service.md)
- [Architektur](../development/architecture.md)
