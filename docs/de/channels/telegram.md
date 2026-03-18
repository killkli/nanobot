# Telegram

Telegram ist der empfohlene nanobot-Einstiegskanal: einfache Einrichtung, stabile Verbindung und keine öffentliche IP bzw. Webhook nötig.

---

## Voraussetzungen

- Ein Telegram-Account
- Zugriff auf `@BotFather`, um einen Bot zu erstellen

---

## Schritt 1: Bot erstellen

1. Öffne Telegram und suche nach **`@BotFather`**
2. Sende den Befehl `/newbot`
3. Gib einen Anzeigenamen für den Bot ein (z. B. `My Nanobot`)
4. Gib einen Benutzernamen ein, der auf `bot` endet (z. B. `my_nanobot_bot`)
5. BotFather liefert daraufhin ein **Bot Token** in folgendem Format:

```
123456789:ABCdefGhIJKlmNoPQRstuVWXyz
```

Bewahre das Token sicher auf.

---

## Schritt 2: Deine Benutzer-ID besorgen

Füge deine Telegram-Benutzer-ID in die `allowFrom`-Whitelist ein, damit du mit dem Bot interagieren darfst.

**So geht’s:**

1. Sieh dir in den Telegram-Einstellungen deinen Benutzername an (`@yourUsername`)
2. Alternativ schreib dem Bot eine Nachricht – die nanobot-Logs zeigen dann deine numerische ID

!!! tip "Benutzername vs. numerische ID"
    Du kannst `allowFrom` sowohl mit deiner numerischen ID (z. B. `"123456789"`) als auch mit dem Benutzernamen (ohne `@`, z. B. `"yourUsername"`) befüllen.

---

## Schritt 3: `config.json` konfigurieren

Füge in `~/.nanobot/config.json` folgende Einstellungen hinzu:

```json
{
  "channels": {
    "telegram": {
      "enabled": true,
      "token": "123456789:ABCdefGhIJKlmNoPQRstuVWXyz",
      "allowFrom": ["YOUR_USER_ID"]
    }
  }
}
```

### Vollständige Optionen

```json
{
  "channels": {
    "telegram": {
      "enabled": true,
      "token": "YOUR_BOT_TOKEN",
      "allowFrom": ["YOUR_USER_ID"],
      "proxy": null,
      "replyToMessage": false,
      "groupPolicy": "mention"
    }
  }
}
```

| Parameter | Standardwert | Beschreibung |
|------|--------|------|
| `enabled` | `false` | Kanal aktivieren |
| `token` | `""` | Bot Token von BotFather |
| `allowFrom` | `[]` | Liste erlaubter IDs oder Benutzernamen |
| `proxy` | `null` | HTTP/SOCKS-Proxy (z. B. `"http://127.0.0.1:1080"`) |
| `replyToMessage` | `false` | Antworten zitieren die Originalnachricht |
| `groupPolicy` | `"mention"` | Gruppennachrichtenverhalten (siehe unten) |

### `groupPolicy`

| Wert | Verhalten |
|----|------|
| `"mention"` (Standard) | Antwortet nur bei @-Erwähnung in Gruppen |
| `"open"` | Reagiert auf alle Gruppennachrichten |

Private Nachrichten (DM) werden unabhängig von der `groupPolicy` beantwortet.

---

## Schritt 4: Starten

```bash
nanobot gateway
```

Sende danach `/start` oder eine beliebige Nachricht an deinen Bot in Telegram.

---

## Verfügbare Befehle

Der Bot registriert standardmäßig folgende Telegram-Kommandos:

| Befehl | Beschreibung |
|------|------|
| `/start` | Bot aktivieren |
| `/new` | Neue Unterhaltung beginnen (Kontext löschen) |
| `/stop` | Aktuelle Aufgabe stoppen |
| `/help` | Zeigt verfügbare Kommandos |
| `/restart` | Bot neu starten |

---

## Sprach-zu-Text (Transkription)

Wenn du einen Groq API-Schlüssel konfigurierst, transkribiert nanobot eingehende Sprachnachrichten automatisch via Whisper:

```json
{
  "providers": {
    "groq": {
      "apiKey": "YOUR_GROQ_API_KEY"
    }
  }
}
```

!!! tip "Kostenlose Transkription"
    Groq bietet eine kostenlose Whisper-Quote – ideal für persönliche Nutzung.

---

## Proxy verwenden

In Regionen mit Telegram-Beschränkungen kannst du einen Proxy angeben:

```json
{
  "channels": {
    "telegram": {
      "enabled": true,
      "token": "YOUR_BOT_TOKEN",
      "allowFrom": ["YOUR_USER_ID"],
      "proxy": "http://127.0.0.1:7890"
    }
  }
}
```

Unterstützte Formate: `http://`, `https://`, `socks5://`.

---

## FAQ

**Bot antwortet nicht?**

- Stelle sicher, dass deine ID in `allowFrom` steht
- Leeres `allowFrom` blockiert alle Nutzer
- Schau in den nanobot-Logs nach „Access denied“

**Ungültiges Token?**

- Kopiere das Token direkt aus BotFather, ohne Leerzeichen
- Bei Kompromittierung `/revoke` bei BotFather verwenden

**Bot reagiert in Gruppen nicht?**

- Bei `groupPolicy: "mention"` muss der Bot erwähnt werden
- Der Bot muss im Kanal sein und Schreibrechte besitzen

**Keine Reaktion auf unbekannte Nutzer?**

- Füge auch deren ID zur `allowFrom`-Liste hinzu oder setze `allowFrom` auf `["*"]`
