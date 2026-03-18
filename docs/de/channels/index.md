# Kanalübersicht

**Kanäle (Channel)** sind die Brücke zwischen nanobot und den Chat-Plattformen. Jeder Kanal verbindet nanobot mit einem bestimmten Instant-Messaging-Dienst, leitet Nutzeranfragen in den Message-Bus und sendet die KI-Antworten zurück auf die Plattform.

---

## Liste unterstützter Kanäle

nanobot unterstützt derzeit folgende 12 Plattformen:

| Kanal | Beschreibung | Verbindungsmethode |
|------|------|----------|
| [Telegram](telegram.md) | Empfehlenswerter Einstieg: einfache Einrichtung und stabile Verbindung | Long Polling |
| [Discord](discord.md) | Community-Server und Direktnachrichten, unterstützt Dateianhänge | Gateway WebSocket |
| [Slack](slack.md) | Unternehmens-Messaging, Threads für Antworten | Socket Mode |
| [Feishu / 飛書](feishu.md) | Feishu-Unternehmenskommunikation mit Multimodal-Input | WebSocket Langverbindung |
| [DingTalk / 釘釘](dingtalk.md) | Alibaba-Unternehmenskommunikation | Stream Mode |
| [WeCom / 企業微信](wecom.md) | Tencent für Unternehmenskunden | WebSocket Langverbindung |
| [QQ](qq.md) | Offizielle QQ-Bot-Plattform mit Einzel- und Gruppenchats | WebSocket |
| [Email](email.md) | IMAP-Empfang + SMTP-Antwort, ideal für asynchrone Szenarien | IMAP Polling |
| [Matrix](matrix.md) | Dezentrales Protokoll mit Unterstützung für E2EE | Matrix Sync |
| [WhatsApp](whatsapp.md) | Anbindung über Node.js-Bridge | WebSocket Bridge |
| [Mochat / Claw IM](mochat.md) | Offene Claw-IM-Plattform | Socket.IO |

---

## Mehrere Kanäle gleichzeitig aktivieren

Setze in der `channels`-Objektstruktur von `~/.nanobot/config.json` mehrere Kanäle auf `"enabled": true`, dann lauscht nanobot nach dem Start auf alle aktivierten Kanäle gleichzeitig:

```json
{
  "channels": {
    "telegram": {
      "enabled": true,
      "token": "YOUR_TELEGRAM_TOKEN",
      "allowFrom": ["YOUR_TELEGRAM_USER_ID"]
    },
    "discord": {
      "enabled": true,
      "token": "YOUR_DISCORD_BOT_TOKEN",
      "allowFrom": ["YOUR_DISCORD_USER_ID"]
    }
  }
}
```

Starten:

```bash
nanobot gateway
```

Alle aktivierten Kanäle laufen im selben Gateway-Prozess.

---

## Kanal-spezifische Einstellungen vs. globale Optionen

**Globale Einstellungen** stehen auf der obersten Ebene des `channels`-Objekts und gelten für alle Kanäle:

| Parameter | Standardwert | Beschreibung |
|------|--------|------|
| `sendProgress` | `true` | Sendet laufende Antworttexte als Stream in den Kanal |
| `sendToolHints` | `false` | Zeigt Tool-Aufrufe (z. B. `read_file("…")`) dem Nutzer an |

**Kanal-spezifische Einstellungen** liegen in den Unterobjekten. Beispiel: globale Optionen und Kanal in einem Block:

```json
{
  "channels": {
    "sendProgress": true,
    "sendToolHints": false,
    "telegram": {
      "enabled": true,
      "token": "YOUR_BOT_TOKEN",
      "allowFrom": ["YOUR_USER_ID"]
    }
  }
}
```

---

## `sendProgress` und `sendToolHints`

### `sendProgress` (Standard: `true`)

Bei aktiviertem `sendProgress` sendet nanobot während der Antwortgenerierung Zwischenresultate in den Kanal, damit Nutzer sehen, dass die KI noch arbeitet.

```json
{
  "channels": {
    "sendProgress": true
  }
}
```

### `sendToolHints` (Standard: `false`)

Mit aktivem `sendToolHints` erhalten Nutzer eine kurze Nachricht, wenn die KI ein Tool aufruft, z. B.:

```
🔧 web_search("nanobot documentation")
```

Das hilft beim Verständnis, empfiehlt sich aber nicht im ruhigen Modus.

```json
{
  "channels": {
    "sendToolHints": true
  }
}
```

---

## `allowFrom`-Zugriffskontrolle

Jeder Kanal verfügt über das Feld `allowFrom`, um zu steuern, welche Nutzer den Bot verwenden dürfen:

| Einstellung | Wirkung |
|------|------|
| `[]` (leeres Array) | Blockiert alle Nutzer (Standard) |
| `["USER_ID_1", "USER_ID_2"]` | Nur angegebene Nutzer dürfen interagieren |
| `["*"]` | Öffnet den Bot für alle Nutzer (vorsichtig einsetzen) |

!!! warning "Sicherheitshinweis"
    Wenn `allowFrom` leer ist, werden alle Nachrichten abgewiesen. Trage vor dem Start deine Nutzer-ID ein.

---

## Mehrere Instanzen

Du kannst für jeden Kanal eine eigene Instanz mit separater Konfiguration anlegen, damit jeder Bot seinen eigenen Workspace erhält:

```bash
# Für jeden Kanal separat onboarden
nanobot onboard --config ~/.nanobot-telegram/config.json --workspace ~/.nanobot-telegram/workspace
nanobot onboard --config ~/.nanobot-discord/config.json --workspace ~/.nanobot-discord/workspace

# Gateways jeweils starten
nanobot gateway --config ~/.nanobot-telegram/config.json
nanobot gateway --config ~/.nanobot-discord/config.json
```

Details zu den Konfigurationen findest du in den kanalbezogenen Dokumentationen.
