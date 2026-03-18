# Slack

nanobot verbindet sich über Slack **Socket Mode**, sodass keine öffentliche URL oder Webhook erforderlich ist. Threads, Datei-Uploads und Reaktionen (emoji reactions) werden unterstützt.

---

## Voraussetzungen

- Ein Slack-Account
- Workspace-Berechtigung zum Installieren von Apps

---

## Schritt 1: Slack-App erstellen

1. Öffne https://api.slack.com/apps
2. Klicke auf **Create New App** → wähle **From scratch**
3. Gib einen App-Namen ein und wähle deinen Workspace aus
4. Klicke auf **Create App**

---

## Schritt 2: Socket Mode aktivieren und App Token erstellen

1. Gehe im Menü zu **Socket Mode**
2. Schalte **Socket Mode** auf **ON**
3. Klicke auf **Generate an app-level token**
4. Vergib einen Namen (z. B. `nanobot-socket`)
5. Klicke auf **Add Scope** → wähle `connections:write`
6. Klicke auf **Generate** und kopiere das **App-Level Token** (`xapp-1-...`)

---

## Schritt 3: OAuth-Permissions und Bot Token konfigurieren

1. Öffne **OAuth & Permissions**
2. Füge unter **Bot Token Scopes** diese Bereiche hinzu:
   - `chat:write` — Nachrichten senden
   - `reactions:write` — Reaktionen hinzufügen
   - `app_mentions:read` — @-Erwähnungen lesen
   - `files:write` — (optional) Dateien hochladen
3. Klicke oben auf **Install to Workspace** und autorisiere die App
4. Kopiere das **Bot User OAuth Token** (`xoxb-...`)

---

## Schritt 4: Events abonnieren

1. Gehe zu **Event Subscriptions**
2. Aktiviere **Enable Events**
3. Trage unter **Subscribe to bot events** die folgenden Events ein:
   - `message.im` — private Nachrichten empfangen
   - `message.channels` — Channel-Nachrichten empfangen
   - `app_mention` — @-Erwähnungen empfangen
4. Klicke auf **Save Changes**

---

## Schritt 5: Messages Tab aktivieren

1. Öffne **App Home**
2. Aktiviere im Bereich **Show Tabs** den **Messages Tab**
3. Aktiviere **Allow users to send Slash commands and messages from the messages tab**

---

## Schritt 6: Deine Slack User ID ermitteln

1. Öffne dein Profil in Slack
2. Klicke auf **...** → **Copy member ID**

Die ID sieht ähnlich aus wie `U0123456789`.

---

## Schritt 7: config.json anpassen

```json
{
  "channels": {
    "slack": {
      "enabled": true,
      "botToken": "xoxb-...",
      "appToken": "xapp-1-...",
      "allowFrom": ["YOUR_SLACK_USER_ID"],
      "groupPolicy": "mention"
    }
  }
}
```

### Vollständige Optionen

```json
{
  "channels": {
    "slack": {
      "enabled": true,
      "mode": "socket",
      "botToken": "xoxb-...",
      "appToken": "xapp-1-...",
      "allowFrom": ["YOUR_SLACK_USER_ID"],
      "groupPolicy": "mention",
      "groupAllowFrom": [],
      "replyInThread": true,
      "reactEmoji": "eyes",
      "doneEmoji": "white_check_mark",
      "dm": {
        "enabled": true,
        "policy": "open",
        "allowFrom": []
      }
    }
  }
}
```

| Parameter | Standardwert | Beschreibung |
|-----------|--------------|--------------|
| `enabled` | `false` | Kanal aktivieren |
| `mode` | `"socket"` | Verbindungsmodus (aktuell nur `"socket"`) |
| `botToken` | `""` | Bot User OAuth Token (`xoxb-...`) |
| `appToken` | `""` | App-Level Token (`xapp-...`) |
| `allowFrom` | `[]` | Liste erlaubter User IDs |
| `groupPolicy` | `"mention"` | Verhalten in Channels |
| `groupAllowFrom` | `[]` | Channel-IDs bei `"allowlist"` |
| `replyInThread` | `true` | Antwortet in Threads |
| `reactEmoji` | `"eyes"` | Reaction bei Eingangsnachrichten |
| `doneEmoji` | `"white_check_mark"` | Reaction bei Abschluss |
| `dm.enabled` | `true` | Direct Messages aktivieren |
| `dm.policy` | `"open"` | DM-Strategie |

### `groupPolicy`

| Wert | Verhalten |
|------|-----------|
| `"mention"` (Standard) | Antwortet nur bei @-Erwähnung im Channel |
| `"open"` | Reagiert auf alle Channel-Nachrichten |
| `"allowlist"` | Reagiert nur in Channels aus `groupAllowFrom` |

---

## Schritt 8: Starten

```bash
nanobot gateway
```

Sende dem Bot danach eine DM oder erwähne ihn in einem Channel, um zu interagieren.

---

## Thread-Unterstützung

`replyInThread` ist standardmäßig `true`, sodass Antworten im ursprünglichen Thread erscheinen und der Channel aufgeräumt bleibt.

```json
{
  "channels": {
    "slack": {
      "replyInThread": false
    }
  }
}
```

!!! note "DMs nutzen keine Threads"
    Direct Messages (DMs) verwenden keine Threads, selbst wenn `replyInThread` aktiv ist.

---

## DMs deaktivieren

Wenn der Bot nur in Channels antworten soll, kannst du DMs deaktivieren:

```json
{
  "channels": {
    "slack": {
      "dm": {
        "enabled": false
      }
    }
  }
}
```

---

## Häufige Fragen

**Keine DM-Antwort?**

- Stelle sicher, dass der Messages Tab aktiviert ist
- Stelle sicher, dass das Event `message.im` abonniert ist

**Bot reagiert nicht im Channel?**

- Prüfe, ob `message.channels` und `app_mention` abonniert sind
- Bei `groupPolicy: "mention"` muss der Bot erwähnt werden

**Was ist das `xapp`-Token?**

- Das ist ein App-Level Token, anders als das Bot Token (`xoxb`)
- Es wird unter **Socket Mode** erstellt und dient der WebSocket-Verbindung

**Muss nach Scope-Änderungen neu autorisiert werden?**

- Ja, nach jeder Änderung der Bot Scopes muss erneut auf **Install to Workspace** geklickt werden
