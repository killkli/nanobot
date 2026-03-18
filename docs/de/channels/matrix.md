# Matrix / Element

nanobot unterstützt das dezentrale Matrix-Protokoll und kann auf jedem Matrix-Homeserver laufen (z. B. matrix.org oder eigene Instanzen). Ende-zu-Ende-Verschlüsselung (E2EE), Medienanhänge und flexible Gruppenrichtlinien werden unterstützt.

---

## Voraussetzungen

- Ein Matrix-Account (z. B. bei [matrix.org](https://matrix.org) oder einem selbstgehosteten Homeserver)
- Zugriff auf einen Matrix-Client wie Element

---

## Schritt 1: Matrix-Abhängigkeiten installieren

Für den Matrix-Kanal sind zusätzliche Pakete erforderlich:

```bash
pip install nanobot-ai[matrix]
```

Oder mit `uv`:

```bash
uv pip install nanobot-ai[matrix]
```

---

## Schritt 2: Matrix-Account anlegen

Empfohlen wird ein dedizierter Bot-Account:

1. Besuche [app.element.io](https://app.element.io) und erstelle einen Account
2. Wähle den Homeserver (Standard: `matrix.org` oder dein eigener Server)
3. Verifiziere, dass du dich erfolgreich anmelden kannst

---

## Schritt 3: Zugangsdaten sammeln

Benötigt werden:

- **userId** (z. B. `@nanobot:matrix.org`)
- **accessToken** für den Login
- **deviceId** (empfohlen, damit der Schlüsselring nach Neustarts erhalten bleibt)

### Access Token beziehen

**Methode A – Element:**

1. Öffne Element → Profilbild → **Settings**
2. Gehe zum Tab **Help & About**
3. Klicke bei **Access Token** auf **Click to reveal**

**Methode B – API:**

```bash
curl -X POST "https://matrix.org/_matrix/client/v3/login" \
  -H "Content-Type: application/json" \
  -d '{"type":"m.login.password","user":"nanobot","password":"YOUR_PASSWORD"}'
```

Die Antwort enthält `access_token` und `device_id`.

---

## Schritt 4: config.json anpassen

```json
{
  "channels": {
    "matrix": {
      "enabled": true,
      "homeserver": "https://matrix.org",
      "userId": "@nanobot:matrix.org",
      "accessToken": "syt_xxx",
      "deviceId": "NANOBOT01",
      "allowFrom": ["@your_user:matrix.org"]
    }
  }
}
```

### Vollständige Optionen

```json
{
  "channels": {
    "matrix": {
      "enabled": true,
      "homeserver": "https://matrix.org",
      "userId": "@nanobot:matrix.org",
      "accessToken": "syt_xxx",
      "deviceId": "NANOBOT01",
      "e2eeEnabled": true,
      "allowFrom": ["@your_user:matrix.org"],
      "groupPolicy": "open",
      "groupAllowFrom": [],
      "allowRoomMentions": false,
      "maxMediaBytes": 20971520,
      "syncStopGraceSeconds": 2
    }
  }
}
```

| Parameter | Standardwert | Beschreibung |
|-----------|--------------|--------------|
| `enabled` | `false` | Kanal aktivieren |
| `homeserver` | `"https://matrix.org"` | Matrix-Homeserver-URL |
| `userId` | `""` | Matrix-User-ID des Bots (`@name:server`) |
| `accessToken` | `""` | Access Token für den Login |
| `deviceId` | `""` | Geräte-ID (für E2EE-History) |
| `e2eeEnabled` | `true` | Ende-zu-Ende-Verschlüsselung aktivieren |
| `allowFrom` | `[]` | Liste erlaubter Matrix-IDs |
| `groupPolicy` | `"open"` | Verhalten in Gruppen |
| `groupAllowFrom` | `[]` | Raum-Whitelist für `allowlist`-Modus |
| `allowRoomMentions` | `false` | Reaktion auf `@room`-Erwähnungen |
| `maxMediaBytes` | `20971520` | Maximale Mediengröße (Byte) |
| `syncStopGraceSeconds` | `2` | Wartezeit beim Stoppen |

### `groupPolicy`

| Wert | Verhalten |
|------|-----------|
| `"open"` (Standard) | Antwortet auf alle Nachrichten im Raum |
| `"mention"` | Nur bei @-Erwähnung |
| `"allowlist"` | Nur Räume aus `groupAllowFrom` |

---

## Schritt 5: Gateway starten

```bash
nanobot gateway
```

---

## Ende-zu-Ende-Verschlüsselung (E2EE)

Matrix aktiviert standardmäßig E2EE. Das bedeutet:

- Nachrichten sind zwischen Bot und Nutzern verschlüsselt
- Schlüssel werden im lokalen `matrix-store` gehalten

!!! warning "deviceId stabil halten"
    Behalte `deviceId` und das Verzeichnis `matrix-store` bei. Änderungen führen zum Verlust der verschlüsselten Session und verhindern das Entschlüsseln neuer Nachrichten.

Wenn E2EE nicht benötigt wird:

```json
{
  "channels": {
    "matrix": {
      "e2eeEnabled": false
    }
  }
}
```

---

## Medienanhänge

Matrix unterstützt Upload/Download verschlüsselter Medien:

- **Empfangen:** Bilder, Audio, Video, Dateien
- **Senden:** AI-generierte Dateien über Homeserver
- `maxMediaBytes` begrenzt die Dateigröße

---

## FAQ

**Bot sieht verschlüsselte Nachrichten nicht?**

- Stelle sicher, dass `e2eeEnabled` aktiviert ist
- `deviceId` und `matrix-store` müssen unverändert bleiben
- Beim ersten Start ist eine Geräte-Verifizierung nötig

**Access Token abgelaufen?**

- Token bleibt solange gültig, bis man sich ausloggt
- Bei Bedarf neuen Token + Device ID generieren

**Bot reagiert nicht in Gruppen?**

- Der Bot muss in die Gruppe eingeladen sein
- `groupPolicy` steht auf `"open"` oder die Gruppe ist in `groupAllowFrom`
- Logs auf Berechtigungsfehler prüfen

**Eigenen Homeserver verwenden?**

- `homeserver` auf die eigene URL setzen (z. B. `"https://matrix.example.com"`)
- Der Rest der Konfiguration bleibt gleich
