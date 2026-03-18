# DingTalk / 釘釘

nanobot verbindet sich über den DingTalk **Stream Mode** und empfängt Nachrichten ohne öffentliche IP oder Webhook. Sowohl Einzel- als auch Gruppenchats sowie multimediale Inhalte (Bilder, Dateien) werden unterstützt.

---

## Voraussetzungen

- Ein DingTalk-Account
- Ein Unternehmenskonto mit Berechtigung zur Erstellung von Apps

---

## Schritt 1: DingTalk-App erstellen

1. Öffne die [DingTalk Open Platform](https://open-dev.dingtalk.com/)
2. Nach dem Login unter **应用开发** → **企业内部应用** gehen
3. Klicke auf **创建应用** und wähle **钉钉应用**
4. Gib Name und Beschreibung ein und erstelle die App

---

## Schritt 2: Bot-Funktion aktivieren

1. Öffne die App-Konfiguration und gehe zu **添加应用能力** → **机器人**
2. Bestätige mit **确认添加**
3. Stelle im Bot-Setup sicher, dass:
   - **Stream Mode** aktiv ist (WebSocket, kein Webhook erforderlich)
   - Name und Beschreibung hinterlegt sind

---

## Schritt 3: Berechtigungen einrichten

Unter **权限管理** ggf. folgende Berechtigungen beantragen:

- `qyapi_chat_group` — für Gruppennachrichten
- Berechtigungen zum Senden von interaktiven Karten, falls erforderlich

---

## Schritt 4: Client ID und Client Secret kopieren

1. Öffne die **应用凭证**-Seite
2. Kopiere **AppKey** (Client ID)
3. Kopiere **AppSecret**

---

## Schritt 5: App veröffentlichen

Gehe zu **版本管理** → Erstelle eine Version → Reiche die App zur Prüfung ein oder veröffentliche sie direkt (bei internen Apps ist oft keine Prüfung nötig).

---

## Schritt 6: config.json konfigurieren

```json
{
  "channels": {
    "dingtalk": {
      "enabled": true,
      "clientId": "YOUR_APP_KEY",
      "clientSecret": "YOUR_APP_SECRET",
      "allowFrom": ["YOUR_STAFF_ID"]
    }
  }
}
```

### Volle Konfigurationsoptionen

```json
{
  "channels": {
    "dingtalk": {
      "enabled": true,
      "clientId": "YOUR_APP_KEY",
      "clientSecret": "YOUR_APP_SECRET",
      "allowFrom": ["YOUR_STAFF_ID"]
    }
  }
}
```

| Parameter | Standardwert | Beschreibung |
|-----------|--------------|--------------|
| `enabled` | `false` | Kanal aktivieren |
| `clientId` | `""` | DingTalk AppKey (Client ID) |
| `clientSecret` | `""` | DingTalk AppSecret (Client Secret) |
| `allowFrom` | `[]` | Liste erlaubter Staff-IDs |

---

## Schritt 7: Gateway starten

```bash
nanobot gateway
```

---

## Deine Staff ID herausfinden

Trage in `allowFrom` die Staff ID (Format `user_abc123`) ein.

**So geht es:**

1. Setze `allowFrom` vorübergehend auf `[
"*"]`, um alle Nutzer zuzulassen
2. Starte nanobot und sende dem Bot eine Nachricht
3. Die Logs zeigen deine Staff ID
4. Setze `allowFrom` auf `[
"user_abc123"]`

---

## Multimediale Unterstützung

DingTalk unterstützt folgende Medien:

- **Bilder** – werden automatisch heruntergeladen und an die KI übergeben
- **Dateien** – werden nach dem Download weiterverarbeitet
- **RichText** – Text- und Bildkomponenten werden korrekt analysiert

---

## Häufige Fragen

**Was ist Stream Mode?**

- Stream Mode nutzt eine WebSocket-Verbindung, die nanobot aktiv aufbaut
- Anders als bei HTTP-Callbacks braucht es weder öffentliche IP noch Reverse Proxy

**Bot empfängt keine Nachrichten?**

- Stelle sicher, dass du **Stream Mode** ausgewählt hast
- Prüfe, ob die App veröffentlicht wurde

**Der Bot reagiert nicht in Gruppen?**

- In Gruppenchats muss der Bot erwähnt werden
- Stelle sicher, dass der Bot als Mitglied hinzugefügt wurde
