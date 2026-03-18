# Docker-Deploy-Guide

Dieser Leitfaden beschreibt die Nutzung von Docker oder Docker Compose für nanobot – ideal für isolierte oder schnelle Server-Deployments.

## Voraussetzungen

- [Docker](https://docs.docker.com/get-docker/) 20.10+
- [Docker Compose](https://docs.docker.com/compose/) v2 (empfohlen)

## Docker Compose Quickstart

Die empfohlene Methode für vollständiges Service-Management.

### Erstmalige Einrichtung

```bash
# 1. Onboarding
docker compose run --rm nanobot-cli onboard

# 2. Konfiguration editieren (API-Keys einfügen)
vim ~/.nanobot/config.json

# 3. Gateway im Hintergrund starten
docker compose up -d nanobot-gateway
```

### Tägliche Commands

```bash
# CLI-Agent (einmalige Unterhaltung)
docker compose run --rm nanobot-cli agent -m "Hallo!"

# Logs einsehen
docker compose logs -f nanobot-gateway

# Alle Services stoppen
docker compose down

# Gateway nach Config-Änderungen neu starten
docker compose restart nanobot-gateway
```

## Docker Compose File

`docker-compose.yml` im Projekt definiert zwei Services:

```yaml
x-common-config: &common-config
  build:
    context: .
    dockerfile: Dockerfile
  volumes:
    - ~/.nanobot:/root/.nanobot

services:
  nanobot-gateway:
    container_name: nanobot-gateway
    <<: *common-config
    command: ["gateway"]
    restart: unless-stopped
    ports:
      - 18790:18790
    deploy:
      resources:
        limits:
          cpus: '1'
          memory: 1G
        reservations:
          cpus: '0.25'
          memory: 256M

  nanobot-cli:
    <<: *common-config
    profiles:
      - cli
    command: ["status"]
    stdin_open: true
    tty: true
```

### Beispiel: Mehrere Gateways

```yaml
x-base: &base
  image: hkuds/nanobot:latest
  restart: unless-stopped

services:
  nanobot-telegram:
    <<: *base
    container_name: nanobot-telegram
    command: ["gateway", "--config", "/root/.nanobot-telegram/config.json"]
    ports:
      - "18790:18790"
    volumes:
      - ~/.nanobot-telegram:/root/.nanobot-telegram

  nanobot-discord:
    <<: *base
    container_name: nanobot-discord
    command: ["gateway", "--config", "/root/.nanobot-discord/config.json"]
    ports:
      - "18791:18790"
    volumes:
      - ~/.nanobot-discord:/root/.nanobot-discord

  nanobot-feishu:
    <<: *base
    container_name: nanobot-feishu
    command: ["gateway", "--config", "/root/.nanobot-feishu/config.json", "--port", "18792"]
    ports:
      - "18792:18792"
    volumes:
      - ~/.nanobot-feishu:/root/.nanobot-feishu
```

## Dockerfile-Aufbau

```dockerfile
FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim

RUN apt-get update && apt-get install -y nodejs ...

WORKDIR /app

COPY pyproject.toml README.md LICENSE ./
RUN uv pip install --system --no-cache .

COPY nanobot/ nanobot/
COPY bridge/ bridge/
RUN uv pip install --system --no-cache .

WORKDIR /app/bridge
RUN npm install && npm run build

WORKDIR /app
RUN mkdir -p /root/.nanobot

EXPOSE 18790
ENTRYPOINT ["nanobot"]
CMD ["status"]
```

**Hinweis:** Die Abhängigkeiten werden vor dem Source-Code kopiert, um Docker-Caches zu nutzen.

## Fertiges Image nutzen

```bash
docker pull hkuds/nanobot:latest

docker run -v ~/.nanobot:/root/.nanobot --rm hkuds/nanobot onboard

docker run -v ~/.nanobot:/root/.nanobot -p 18790:18790 \
  --name nanobot-gateway --restart unless-stopped \
  -d hkuds/nanobot gateway
```

## Eigenes Image bauen

```bash
git clone https://github.com/HKUDS/nanobot.git
cd nanobot
docker build -t nanobot .
docker run -v ~/.nanobot:/root/.nanobot --rm nanobot onboard
vim ~/.nanobot/config.json
docker run -v ~/.nanobot:/root/.nanobot -p 18790:18790 nanobot gateway
```

## Volumes

| Host | Container | Zweck |
|------|-----------|-------|
| `~/.nanobot` | `/root/.nanobot` | Config & Workspace |
| `~/.ssh` | `/root/.ssh` | SSH Keys für Git |
| `/custom/workspace` | `/root/.nanobot/workspace` | Benutzerdefinierter Workspace |

### SSH-Volume Beispiel

```bash
docker run \
  -v ~/.nanobot:/root/.nanobot \
  -v ~/.ssh:/root/.ssh:ro \
  -p 18790:18790 \
  nanobot gateway
```

## Umgebungsvariablen

```bash
docker run \
  -v ~/.nanobot:/root/.nanobot \
  -p 18790:18790 \
  -e ANTHROPIC_API_KEY=sk-ant-xxx \
  -e OPENAI_API_KEY=sk-xxx \
  nanobot gateway
```

In Compose mit `.env`:

```yaml
services:
  nanobot-gateway:
    env_file:
      - .env
```

```bash
# .env
ANTHROPIC_API_KEY=sk-ant-xxx
TELEGRAM_BOT_TOKEN=xxx
```

## Healthchecks

```yaml
services:
  nanobot-gateway:
    image: hkuds/nanobot:latest
    command: ["gateway"]
    healthcheck:
      test: ["CMD", "nanobot", "status"]
      interval: 60s
      timeout: 10s
      retries: 3
      start_period: 30s
    restart: unless-stopped
```

## Logging

### Logs folgen

```bash
docker compose logs -f nanobot-gateway
docker logs -f nanobot-gateway
```

### Logrotation

```yaml
services:
  nanobot-gateway:
    logging:
      driver: "json-file"
      options:
        max-size: "50m"
        max-file: "5"
```

### Syslog-Ausgabe

```yaml
services:
  nanobot-gateway:
    logging:
      driver: syslog
      options:
        syslog-address: "tcp://localhost:514"
        tag: "nanobot"
```

## FAQ

**Container beendet sich sofort**

```bash
docker logs nanobot-gateway
docker run -v ~/.nanobot:/root/.nanobot --rm nanobot status
```

**Gateway-Port nicht erreichbar**

```bash
docker inspect nanobot-gateway | grep -A 10 "Ports"
```

**After config changes**

```bash
docker compose restart nanobot-gateway
```
