# Installationsanleitung

Diese Seite beschreibt, wie Sie nanobot auf Ihrem System installieren, mit mehreren Installationswegen und gängigen Troubleshooting-Hinweisen.

---

## Systemanforderungen

| Anforderung | Version |
|------|------|
| **Python** | 3.11 oder neuer |
| **Betriebssystem** | macOS, Linux, Windows (WSL empfohlen) |
| **uv** (empfohlen) | Neueste Version |
| **Node.js** (optional) | ≥18, nur für WhatsApp erforderlich |

!!! tip "Python-Version prüfen"
    ```bash
    python3 --version
    # Ausgabe sollte Python 3.11.x oder neuer sein
    ```

---

## uv installieren (empfohlen)

[uv](https://github.com/astral-sh/uv) ist das bevorzugte Paketverwaltungs-Tool für nanobot und startet extrem schnell.

=== "macOS / Linux"

    ```bash
    curl -LsSf https://astral.sh/uv/install.sh | sh
    ```

=== "Windows"

    ```powershell
    powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
    ```

=== "pip"

    ```bash
    pip install uv
    ```

Nach der Installation starten Sie Ihr Terminal neu oder führen aus:

```bash
uv --version
```

---

## nanobot installieren

### Methode 1: uv (empfohlen)

```bash
uv tool install nanobot-ai
```

Das ist der schnellste Weg: nanobot wird als eigenständiges CLI-Tool installiert.

**Auf die neueste Version aktualisieren:**

```bash
uv tool upgrade nanobot-ai
nanobot --version
```

### Methode 2: pip

```bash
pip install nanobot-ai
```

**Aktualisierung:**

```bash
pip install -U nanobot-ai
nanobot --version
```

### Methode 3: Installation aus dem Quellcode (empfohlen für Entwickler)

Ideal, wenn Sie Zugriff auf die neuesten Features oder Mitwirkung wollen.

```bash
git clone https://github.com/HKUDS/nanobot.git
cd nanobot
uv sync
```

!!! note "Aus dem Quellcode ausführen"
    Verwenden Sie nach dieser Installation `uv run nanobot` anstelle des direkten `nanobot`-Befehls:
    ```bash
    uv run nanobot --version
    uv run nanobot onboard
    uv run nanobot agent
    ```

---

## Docker-Installation

Keine Lust, eine Python-Umgebung lokal einzurichten? Nutzen Sie Docker.

### Voraussetzungen

- [Docker](https://docs.docker.com/get-docker/) installiert und laufend

### Methode 1: Docker Compose (empfohlen)

```bash
# Repository klonen
git clone https://github.com/HKUDS/nanobot.git
cd nanobot

# Konfiguration initialisieren (nur beim ersten Mal)
docker compose run --rm nanobot-cli onboard

# config bearbeiten und API-Schlüssel ergänzen
vim ~/.nanobot/config.json

# Gateway starten
docker compose up -d nanobot-gateway
```

Häufig genutzte Docker-Compose-Befehle:

```bash
# CLI-Dialog ausführen
docker compose run --rm nanobot-cli agent -m "Hello!"

# Gateway-Logs ansehen
docker compose logs -f nanobot-gateway

# Gateway stoppen
docker compose down
```

### Methode 2: Direkter Docker-Einsatz

```bash
# Image bauen
docker build -t nanobot .

# Konfiguration initialisieren (erstmalig)
docker run -v ~/.nanobot:/root/.nanobot --rm nanobot onboard

# Konfig bearbeiten
vim ~/.nanobot/config.json

# Gateway starten
docker run -v ~/.nanobot:/root/.nanobot -p 18790:18790 nanobot gateway

# Alternativ einmalige CLI-Commands
docker run -v ~/.nanobot:/root/.nanobot --rm nanobot agent -m "Hello!"
docker run -v ~/.nanobot:/root/.nanobot --rm nanobot status
```

!!! tip "Daten persistent halten"
    Der Flag `-v ~/.nanobot:/root/.nanobot` mountet Ihr lokales Config-Verzeichnis in den Container, damit Konfiguration und Workspace nach einem Neustart erhalten bleiben.

!!! note "OAuth-Login im Docker"
    Für interaktive OAuth-Logins (z. B. OpenAI Codex) fügen Sie `-it` hinzu:
    ```bash
docker run -it -v ~/.nanobot:/root/.nanobot --rm nanobot provider login openai-codex
```

---

## Optional dependencies installieren

Einige Kanäle benötigen zusätzliche Pakete:

| Kanal | Installationsbefehl |
|------|--------------------|
| **Matrix** | `pip install nanobot-ai[matrix]` |
| **WeCom (企業微信)** | `pip install nanobot-ai[wecom]` |
| **WhatsApp** | Benötigt Node.js ≥18; beim Ausführen von `nanobot channels login` wird die Bridge automatisch installiert |

---

## Installation validieren

Führen Sie nach der Installation folgenden Befehl aus:

```bash
nanobot --version
```

Erwartete Ausgabe:

```
nanobot 0.1.4.post5
```

Anschließend testen Sie den Status:

```bash
nanobot status
```

Wenn alles korrekt eingerichtet ist, erhalten Sie eine Übersicht über aktuelle Konfiguration und Verbindungen.

---

## Häufige Installationsprobleme

### `nanobot: command not found`

**Grund:** uv hat nanobot installiert, aber `~/.local/bin` ist nicht im `PATH`.

**Lösung:**

```bash
# Folgendes zu ~/.bashrc oder ~/.zshrc hinzufügen
export PATH="$HOME/.local/bin:$PATH"

# Konfiguration neu laden
source ~/.bashrc   # oder source ~/.zshrc
```

### Python-Version nicht kompatibel

**Fehlermeldung:** `requires Python >=3.11`

**Lösung:** Installieren Sie Python 3.11+. Wir empfehlen [pyenv](https://github.com/pyenv/pyenv):

```bash
pyenv install 3.11
pyenv global 3.11
```

### pip-Installationsberechtigung fehlt (Linux / macOS)

**Lösung:** Fügen Sie `--user` hinzu oder nutzen Sie ein virtuelles Environment:

```bash
pip install --user nanobot-ai
```

Oder erstellen Sie ein venv:

```bash
python3 -m venv venv
source venv/bin/activate
pip install nanobot-ai
```

### WhatsApp-Bridge-Build schlägt fehl

**Grund:** Node.js-Version zu alt oder nicht installiert.

**Lösung:**

```bash
# Node.js-Version prüfen (≥18 erforderlich)
node --version

# Bridge neu erstellen
rm -rf ~/.nanobot/bridge
nanobot channels login
```

### SSL-Zertifikatsfehler (Unternehmensnetzwerk / Proxy)

**Lösung:** Konfigurieren Sie einen Proxy in `~/.nanobot/config.json`:

```json
{
  "tools": {
    "web": {
      "proxy": "http://your-proxy:7890"
    }
  }
}
```

---

## Nächster Schritt

Nach der Installation wechseln Sie zu [Schnellstart](quick-start.md) und schließen Ihre erste nanobot-Konfiguration in fünf Minuten ab.
