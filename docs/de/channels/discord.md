# Discord

nanobot verbindet sich über das Discord Gateway WebSocket, sodass keine öffentliche IP oder Webhook benötigt wird. Threads, Dateianhänge und @Erwähnungen in Gruppenchats werden unterstützt.

---

## Voraussetzungen

- Ein Discord-Account
- Ein Discord-Server zum Testen

---

## Schritt 1: Discord-App und Bot erstellen

1. Öffne das [Discord Developer Portal](https://discord.com/developers/applications)
2. Klicke oben rechts auf **New Application**, gib einen Namen ein und erstelle die App
3. Wähle im linken Menü **Bot** aus
4. Klicke auf **Add Bot** (oder **Reset Token**) → bestätige
5. Klicke auf **Copy**, um das **Bot Token** zu kopieren

!!! warning "Token-Sicherheit"
    Das Bot-Token ist wie ein Passwort. Bitte nie in der Versionsverwaltung speichern oder teilen. Bei einem Leak sofort auf derselben Seite ein neues Token generieren.

---

## Schritt 2: Message Content Intent aktivieren

Scrolle auf der Bot-Seite zu **Privileged Gateway Intents**:

- Aktiviere **MESSAGE CONTENT INTENT** ← **erforderlich**, sonst kann der Bot Nachrichteninhalte nicht lesen
- (Optional) Aktiviere **SERVER MEMBERS INTENT**, wenn du Filter auf Basis von Servermitgliedern brauchst

Klicke auf **Save Changes**.

---

## Schritt 3: Deine Benutzer-ID erhalten

1. Öffne die Discord-Einstellungen → **Advanced**
2. Aktiviere den **Developer Mode**
3. Rechtsklicke auf dein Avatar → **Benutzer-ID kopieren**

Die ID hat das Format `123456789012345678`.

---

## Schritt 4: Bot auf den Server einladen

1. Gehe im Developer Portal zu **OAuth2** → **URL Generator**
2. Wähle unter **Scopes** `bot` aus
3. Unter **Bot Permissions** wähle:
   - `Send Messages`
   - `Read Message History`
   - (Optional) `Attach Files`, falls der Bot Dateien senden soll
4. Kopiere die generierte URL, öffne sie im Browser und lade den Bot auf deinen Server ein

---

## Schritt 5: config.json konfigurieren

```json
{
  "channels": {
    "discord": {
      "enabled": true,
      "token": "YOUR_BOT_TOKEN",
      "allowFrom": ["YOUR_USER_ID"],
      "groupPolicy": "mention"
    }
  }
}
```

### Vollständige Konfigurationsoptionen

```json
{
  "channels": {
    "discord": {
      "enabled": true,
      "token": "YOUR_BOT_TOKEN",
      "allowFrom": ["YOUR_USER_ID"],
      "gatewayUrl": "wss://gateway.discord.gg/?v=10&encoding=json",
      "intents": 37377,
      "groupPolicy": "mention"
    }
  }
}
```

| Parameter | Standardwert | Beschreibung |
|-----------|--------------|--------------|
| `enabled` | `false` | Kanal aktivieren |
| `token` | `""` | Discord Bot Token |
| `allowFrom` | `[]` | Liste der erlaubten Nutzer-IDs |
| `gatewayUrl` | Discord-Standard | Gateway-WebSocket-URL (normalerweise nicht ändern) |
| `intents` | `37377` | Gateway-Intent-Bitmaske (normalerweise nicht ändern) |
| `groupPolicy` | `"mention"` | Strategie für Gruppennachrichten (siehe unten) |

### Erläuterung zu `groupPolicy`

| Wert | Verhalten |
|------|-----------|
| `"mention"` (Standard) | Antwortet nur bei @Erwähnung im Kanal |
| `"open"` | Reagiert auf alle Nachrichten im Kanal |

Direktnachrichten (DMs) werden immer beantwortet, unabhängig von `groupPolicy`.

---

## Schritt 6: Starten

```bash
nanobot gateway
```

---

## Thread-Unterstützung

Wenn nanobot in einem Discord-Kanal antwortet, bleibt die Unterhaltung im gleichen Thread. Der Kontext jedes Nutzers bleibt dabei separat erhalten.

---

## Dateianhang-Unterstützung

nanobot kann Discord-Anhänge empfangen und senden:

- **Empfangen**: Bilder oder Dateien werden heruntergeladen und an die KI weitergegeben
- **Senden**: Von der KI generierte Dateien (z. B. Code, Bilder) werden als Anhänge hochgeladen
- Einzelanhänge dürfen maximal **20 MB** groß sein (Discord-Free-Account-Beschränkung)

---

## Häufig gestellte Fragen

**Bot sieht Nachrichten im Kanal nicht?**

- Prüfe, ob **MESSAGE CONTENT INTENT** aktiviert ist. Das ist die häufigste Ursache.
- Ohne diesen Intent erhält der Bot Events, kann aber keine Inhalte lesen.

**Bot wurde eingeladen, reagiert aber nicht?**

- Stelle sicher, dass deine ID in `allowFrom` enthalten ist
- Bei `groupPolicy: "mention"` musst du den Bot in der Nachricht erwähnen

**Bot-Token falsch?**

- Überprüfe, dass du das Bot Token kopiert hast und nicht das OAuth Client Secret
- Bot Tokens starten meist mit `MT`, `NT` etc. und sind etwa 70 Zeichen lang

**Rate-Limit-Warnung?**

- Discord hat API-Rate-Limits. nanobot versucht automatisch erneut.
- Wenn Warnungen häufig auftreten, reduziere parallele Anfragen.
