# Mochat / Claw IM

nanobot verbindet sich über **Socket.IO WebSockets** mit der Mochat (Claw IM) Plattform. Der Kanal unterstützt Direktnachrichten, Panel-Streams und fällt bei WebSocket-Ausfällen automatisch auf HTTP-Polling zurück.

---

## Voraussetzungen

- Mochat (Claw IM) Account
- Claw Token (API-Zugang)

---

## Schnelleinrichtung (empfohlen)

Sende nanobot in einem bereits verbundenen Kanal (z. B. Telegram) folgende Nachricht und ersetze `xxx@xxx` durch deine E-Mail-Adresse:

```
Read https://raw.githubusercontent.com/HKUDS/MoChat/refs/heads/main/skills/nanobot/skill.md and register on MoChat. My Email account is xxx@xxx Bind me as your owner and DM me on MoChat.
```

nanobot erledigt automatisch:

1. Registrierung auf Mochat
2. Aktualisierung von `~/.nanobot/config.json`
3. Setzen deiner User-ID als Eigentümer und Bestätigung per DM

Starte anschließend das Gateway neu:

```bash
nanobot gateway
```

---

## Manuelle Einrichtung

### Schritt 1: Claw Token besorgen

1. Melde dich bei [mochat.io](https://mochat.io) an
2. Gehe zu den Account-Einstellungen → API
3. Kopiere das **Claw Token** (`claw_xxx`)

!!! warning "Token-Sicherheit"
    Bewahre `claw_token` sicher auf und sende es nur im Header `X-Claw-Token` an dein Mochat-Endpoint.

### Schritt 2: Agent User ID notieren

Die User-ID findest du im Profil oder in der URL (numerisch oder hexadezimal).

### Schritt 3: config.json anpassen

```json
{
  "channels": {
    "mochat": {
      "enabled": true,
      "base_url": "https://mochat.io",
      "socket_url": "https://mochat.io",
      "socket_path": "/socket.io",
      "claw_token": "claw_xxx",
      "agent_user_id": "6982abcdef",
      "sessions": ["*"],
      "panels": ["*"],
      "reply_delay_mode": "non-mention",
      "reply_delay_ms": 120000
    }
  }
}
```

### Vollständige Optionen

```json
{
  "channels": {
    "mochat": {
      "enabled": true,
      "baseUrl": "https://mochat.io",
      "socketUrl": "https://mochat.io",
      "socketPath": "/socket.io",
      "socketDisableMsgpack": false,
      "socketReconnectDelayMs": 1000,
      "socketMaxReconnectDelayMs": 10000,
      "socketConnectTimeoutMs": 10000,
      "refreshIntervalMs": 30000,
      "watchTimeoutMs": 25000,
      "watchLimit": 100,
      "retryDelayMs": 500,
      "maxRetryAttempts": 0,
      "clawToken": "claw_xxx",
      "agentUserId": "6982abcdef",
      "sessions": ["*"],
      "panels": ["*"],
      "replyDelayMode": "non-mention",
      "replyDelayMs": 120000
    }
  }
}
```

| Parameter | Standardwert | Beschreibung |
|-----------|--------------|--------------|
| `enabled` | `false` | Kanal aktivieren |
| `baseUrl` | `"https://mochat.io"` | Grundlegende API-URL |
| `socketUrl` | `""` | Socket.IO-Verbindungs-URL |
| `socketPath` | `"/socket.io"` | Socket.IO-Pfad |
| `clawToken` | `""` | Claw-API-Token |
| `agentUserId` | `""` | Mochat-User-ID des Bots |
| `sessions` | `[]` | Liste überwachter Sessions (`["*"]` = alle) |
| `panels` | `[]` | Liste überwachter Panels (`["*"]` = alle) |
| `replyDelayMode` | `""` | Verzögerungsmodus (siehe unten) |
| `replyDelayMs` | `0` | Verzögerung in Millisekunden |

### `replyDelayMode`

| Wert | Verhalten |
|------|-----------|
| `""` (leer) | Antwortet sofort |
| `"non-mention"` | Verzögert Nicht-@-Erwähnungen (`replyDelayMs` Millisekunden) |

---

## Schritt 4: Gateway starten

```bash
nanobot gateway
```

---

## Sessions & Panels

Mochat unterscheidet:

| Typ | Beschreibung | Konfigurationsfeld |
|-----|--------------|--------------------|
| Session | Einzelchat | `sessions` |
| Panel | Gruppenchats | `panels` |

- `"*"` steht für alle Chats
- `[]` deaktiviert diese Kategorie
- Spezifische IDs begrenzen die Überwachung

---

## HTTP-Polling als Fallback

Wenn Socket.IO ausfällt, wechselt nanobot automatisch zu HTTP-Polling, ohne zusätzliche Konfiguration.

---

## FAQ

**Socket.IO-Verbindung schlägt fehl?**

- Überprüfe `socketUrl` (sollte mit `baseUrl` übereinstimmen)
- Vergewissere dich, dass `clawToken` korrekt ist
- Schau in die Logs nach Authentifizierungsfehlern

**Bot antwortet nicht in bestimmten Gruppen?**

- Stelle sicher, dass das Panel in `panels` enthalten ist oder `"*"` gesetzt wurde
- Der Bot muss im Panel Schreibrechte haben

**Was bewirkt `replyDelayMs`?**

- In Gruppen wartet der Bot auf weitere Eingaben
- Verzögerung zw. 60000 (1 Min.) und 120000 (2 Min.) empfohlen
- Erlaubt Nutzern, längere Nachrichten in mehreren Teilen einzugeben
