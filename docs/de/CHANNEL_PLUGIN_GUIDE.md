# Kanal-Plugin-Leitfaden

Erstelle ein eigenes nanobot-Kanal-Plugin in drei Schritten: ableiten, paketieren, installieren.

## Funktionsweise

nanobot entdeckt Kanal-Plugins über Python-[Entry Points](https://packaging.python.org/en/latest/specifications/entry-points/). Beim Start von `nanobot gateway` scannt nanobot:

1. Eingebaute Kanäle in `nanobot/channels/`
2. Externe Pakete, die unter der Entry-Point-Gruppe `nanobot.channels` registriert sind

Trifft eine passende Konfiguration mit `"enabled": true` ein, wird der Kanal instanziiert und gestartet.

## Schnellstart

Wir bauen einen minimalen Webhook-Kanal, der Nachrichten per HTTP POST empfängt und Antworten zurücksendet.

### Projektstruktur

```
nanobot-channel-webhook/
├── nanobot_channel_webhook/
│   ├── __init__.py          # WebhookChannel erneut exportieren
│   └── channel.py           # Kanalimplementierung
└── pyproject.toml
```

### 1. Erstelle deinen Kanal

```python
# nanobot_channel_webhook/__init__.py
from nanobot_channel_webhook.channel import WebhookChannel

__all__ = ["WebhookChannel"]
```

```python
# nanobot_channel_webhook/channel.py
import asyncio
from typing import Any

from aiohttp import web
from loguru import logger

from nanobot.channels.base import BaseChannel
from nanobot.bus.events import OutboundMessage


class WebhookChannel(BaseChannel):
    name = "webhook"
    display_name = "Webhook"

    @classmethod
    def default_config(cls) -> dict[str, Any]:
        return {"enabled": False, "port": 9000, "allowFrom": []}

    async def start(self) -> None:
        """Startet einen HTTP-Server und lauscht auf eingehende Nachrichten.

        WICHTIG: start() muss dauerhaft blockieren (oder bis stop() aufgerufen wird).
        Wenn es zurückkehrt, gilt der Kanal als tot.
        """
        self._running = True
        port = self.config.get("port", 9000)

        app = web.Application()
        app.router.add_post("/message", self._on_request)
        runner = web.AppRunner(app)
        await runner.setup()
        site = web.TCPSite(runner, "0.0.0.0", port)
        await site.start()
        logger.info("Webhook hört auf :{}", port)

        # Blockieren bis gestoppt
        while self._running:
            await asyncio.sleep(1)

        await runner.cleanup()

    async def stop(self) -> None:
        self._running = False

    async def send(self, msg: OutboundMessage) -> None:
        """Sende eine ausgehende Nachricht.

        msg.content  — Markdown-Text (ggf. in Plattformformat konvertieren)
        msg.media    — Liste lokaler Dateipfade zum Anhängen
        msg.chat_id  — Empfänger (gleich dem chat_id, den du an _handle_message übergibst)
        msg.metadata — kann `_progress`: True für Streaming-Chunks enthalten
        """
        logger.info("[webhook] -> {}: {}", msg.chat_id, msg.content[:80])
        # In einem echten Plugin: POST an Callback-URL, SDK-Aufruf etc.

    async def _on_request(self, request: web.Request) -> web.Response:
        """Bearbeitet einen eingehenden HTTP POST. """
        body = await request.json()
        sender = body.get("sender", "unknown")
        chat_id = body.get("chat_id", sender)
        text = body.get("text", "")
        media = body.get("media", [])      # Liste von URLs

        # Der entscheidende Aufruf: prüft allowFrom und stellt die Nachricht in den Bus.
        await self._handle_message(
            sender_id=sender,
            chat_id=chat_id,
            content=text,
            media=media,
        )

        return web.json_response({"ok": True})
```

### 2. Entry Point registrieren

```toml
# pyproject.toml
[project]
name = "nanobot-channel-webhook"
version = "0.1.0"
dependencies = ["nanobot", "aiohttp"]

[project.entry-points."nanobot.channels"]
webhook = "nanobot_channel_webhook:WebhookChannel"

[build-system]
requires = ["setuptools"]
build-backend = "setuptools.backends._legacy:_Backend"
```

Der Schlüssel (`webhook`) wird zum Konfigurationsabschnitt. Der Wert verweist auf deine `BaseChannel`-Subklasse.

### 3. Installieren & Konfigurieren

```bash
pip install -e .
nanobot plugins list      # überprüft, ob "Webhook" als "plugin" angezeigt wird
nanobot onboard           # fügt automatisch die Standardkonfiguration hinzu
```

Bearbeite `~/.nanobot/config.json`:

```json
{
  "channels": {
    "webhook": {
      "enabled": true,
      "port": 9000,
      "allowFrom": ["*"]
    }
  }
}
```

### 4. Ausführen & testen

```bash
nanobot gateway
```

In einem zweiten Terminal:

```bash
curl -X POST http://localhost:9000/message \
  -H "Content-Type: application/json" \
  -d '{"sender": "user1", "chat_id": "user1", "text": "Hello!"}'
```

Der Agent erhält die Nachricht und verarbeitet sie. Antworten landen in deiner `send()`-Methode.

## BaseChannel-API

### Erforderlich (abstrakt)

| Methode | Beschreibung |
|--------|-------------|
| `async start()` | **Muss dauerhaft blockieren.** Verbindet zur Plattform, empfängt Nachrichten, ruft `_handle_message()` auf. Gibt die Methode zurück, gilt der Kanal als tot. |
| `async stop()` | Setzt `self._running = False` und räumt auf. Wird beim Herunterfahren aufgerufen. |
| `async send(msg: OutboundMessage)` | Liefert eine ausgehende Nachricht an die Plattform. |

### Vom Base-Klassen bereitgestellt

| Methode / Eigenschaft | Beschreibung |
|-------------------|-------------|
| `_handle_message(sender_id, chat_id, content, media?, metadata?, session_key?)` | **Rufe diese Methode bei eingehenden Nachrichten auf.** `allowFrom` wird geprüft, dann wird die Nachricht in den Bus gelegt. |
| `is_allowed(sender_id)` | Überprüft `config["allowFrom"]`; `"*"` erlaubt alle, `[]` blockiert alle. |
| `default_config()` (Klassenmethode) | Gibt das Standardkonfigurations-Dict für `nanobot onboard` zurück. Überschreiben, um eigene Felder zu deklarieren. |
| `transcribe_audio(file_path)` | Transkribiert Audiodateien über Groq Whisper (falls konfiguriert). |
| `is_running` | Gibt `self._running` zurück. |

### Nachrichtentypen

```python
@dataclass
class OutboundMessage:
    channel: str        # Kanalname
    chat_id: str        # Empfänger (gleich dem chat_id aus _handle_message)
    content: str        # Markdown-Text — ggf. in Plattformformat konvertieren
    media: list[str]    # Lokale Dateipfade zum Anhängen
    metadata: dict      # Kann enthalten: "_progress" (bool) für Streaming, "message_id" für Threading
```

## Config

Dein Kanal erhält die Konfiguration als normales `dict`. Nutze `.get()` für Felder:

```python
async def start(self) -> None:
    port = self.config.get("port", 9000)
    token = self.config.get("token", "")
```

`allowFrom` übernimmt `_handle_message()` automatisch – du musst es nicht selbst prüfen.

Überschreibe `default_config()`, damit `nanobot onboard` die Konfiguration automatisch in `config.json` anlegt:

```python
@classmethod
def default_config(cls) -> dict[str, Any]:
    return {"enabled": False, "port": 9000, "allowFrom": []}
```

Wenn du diese Methode nicht überschreibst, liefert die Basisklasse `{"enabled": false}`.

## Benennungskonventionen

| Was | Format | Beispiel |
|------|--------|---------|
| PyPI-Paket | `nanobot-channel-{name}` | `nanobot-channel-webhook` |
| Entry-Point-Key | `{name}` | `webhook` |
| Konfigurationsabschnitt | `channels.{name}` | `channels.webhook` |
| Python-Paket | `nanobot_channel_{name}` | `nanobot_channel_webhook` |

## Lokale Entwicklung

```bash
git clone https://github.com/you/nanobot-channel-webhook
cd nanobot-channel-webhook
pip install -e .
nanobot plugins list    # sollte "Webhook" als "plugin" anzeigen
nanobot gateway         # End-to-End testen
```

## Verifizieren

```bash
$ nanobot plugins list

  Name       Source    Enabled
  telegram   builtin  yes
  discord    builtin  no
  webhook    plugin   yes
```
