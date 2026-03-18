# Feishu / 飛書

nanobot verbindet sich per **WebSocket-Long-Connection** mit Feishu und benötigt weder öffentliche IP noch Webhook. Multimodale Eingaben (Bilder, Dateien), Gruppen-@Erwähnungen und zitierte Antworten werden unterstützt.

---

## Voraussetzungen

- Ein Feishu-Account
- Berechtigung innerhalb eines Unternehmens oder Teams, Apps zu erstellen

---

## Schritt 1: Feishu-App erstellen

1. Besuche die [Feishu Open Platform](https://open.feishu.cn/app)
2. Klicke auf **建立企業自建應用**, gib Namen und Beschreibung ein
3. Navigiere in den App-Einstellungen zu **功能** → **機器人** und aktiviere die Bot-Funktion

---

## Schritt 2: Berechtigungen konfigurieren

Wechsle zu **開發設定** → **權限管理** und füge folgende Berechtigungen hinzu:

- `im:message` — Empfang und Versand von Einzel- und Gruppennachrichten
- `im:message.p2p_msg:readonly` — Empfang privater Nachrichten
- (Optional) `im:message.group_at_msg:readonly` — Empfang von @Erwähnungen in Gruppen

---

## Schritt 3: Events abonnieren und Long Connection wählen

1. Gehe zu **開發設定** → **事件訂閱**
2. Füge das Event `im.message.receive_v1` hinzu (Nachrichtenempfang)
3. Wähle **使用長連線接收事件** (Long Connection) als Verbindungsmethode

!!! tip "Keine öffentliche IP erforderlich"
    Die Long Connection wird aktiv von nanobot zur Feishu-Infrastruktur aufgebaut. Es ist keine Webhook-URL oder öffentliche IP notwendig.

---

## Schritt 4: App ID und App Secret besorgen

1. Öffne **憑證與基礎資訊**
2. Kopiere die **App ID** (Format: `cli_xxx`)
3. Kopiere das **App Secret**

---

## Schritt 5: App veröffentlichen

Gehe zu **版本管理與發佈**, erstelle eine Version und beantrage die Veröffentlichung (für Unternehmens-Apps ist eine Administratorfreigabe erforderlich).

!!! note "Testmodus"
    Während der Entwicklung kannst du die App im "線上測試"-Modus belassen und ohne Veröffentlichung testen.

---

## Schritt 6: config.json konfigurieren

```json
{
  "channels": {
    "feishu": {
      "enabled": true,
      "appId": "cli_xxx",
      "appSecret": "YOUR_APP_SECRET",
      "allowFrom": ["ou_YOUR_OPEN_ID"],
      "groupPolicy": "mention"
    }
  }
}
```

### Weitere Optionen

```json
{
  "channels": {
    "feishu": {
      "enabled": true,
      "appId": "cli_xxx",
      "appSecret": "YOUR_APP_SECRET",
      "encryptKey": "",
      "verificationToken": "",
      "allowFrom": ["ou_YOUR_OPEN_ID"],
      "reactEmoji": "THUMBSUP",
      "groupPolicy": "mention",
      "replyToMessage": false
    }
  }
}
```

| Parameter | Standardwert | Beschreibung |
|-----------|--------------|--------------|
| `enabled` | `false` | Kanal aktivieren |
| `appId` | `""` | Feishu App ID |
| `appSecret` | `""` | Feishu App Secret |
| `encryptKey` | `""` | Verschlüsselungsschlüssel (bei Long Connection leer lassen) |
| `verificationToken` | `""` | Event-Verifikationstoken (bei Long Connection leer lassen) |
| `allowFrom` | `[]` | Liste erlaubter Open IDs |
| `reactEmoji` | `"THUMBSUP"` | Emoji-Reaktion bei eingehenden Nachrichten |
| `groupPolicy` | `"mention"` | Verhalten in Gruppenchats (siehe unten) |
| `replyToMessage` | `false` | Antwort als Zitat der Originalnachricht |

### `groupPolicy`

| Wert | Verhalten |
|------|-----------|
| `"mention"` (Standard) | Antwortet nur auf @-Erwähnungen in Gruppen |
| `"open"` | Reagiert auf alle Gruppennachrichten |

Private Chats werden unabhängig von `groupPolicy` immer beantwortet.

---

## Schritt 7: Gateway starten

```bash
nanobot gateway
```

---

## Deine Open ID herausfinden

Trage in `allowFrom` die Open ID des jeweiligen Feishu-Nutzers ein (Format: `ou_xxxxxxxx`).

**So funktioniert es:**

1. Setze `allowFrom` vorübergehend auf `["*"]`, um alle Nutzer zuzulassen
2. Starte nanobot und sende dem Bot eine Nachricht
3. Die Logs zeigen deine Open ID
4. Stelle `allowFrom` auf `[
"ou_xxxxxxxx"]`

---

## Multimodale Unterstützung

Feishu akzeptiert folgende Medien:

- **Bilder** – werden direkt an die KI weitergegeben (auch visuelle Modelle)
- **Sprachnachrichten** – mit konfiguriertem Groq API-Key automatisch transkribiert
- **Dateien** – werden heruntergeladen und an die KI übergeben
- **Sticker** – erscheinen als `[sticker]`

---

## Häufige Fragen

**Bot empfängt keine Nachrichten?**

- Prüfe, ob die App veröffentlicht ist und der Bot aktiviert wurde
- Stelle sicher, dass `im.message.receive_v1` abonniert ist
- Vergewissere dich, dass der Empfangsmodus auf Long Connection eingestellt ist

**Bot reagiert nicht in Gruppen?**

- Bei `groupPolicy: "mention"` muss der Bot erwähnt werden
- Prüfe, ob der Bot Mitglied der Gruppe ist

**Muss `encryptKey` gesetzt werden?**

- Bei Long Connection kannst du `encryptKey` und `verificationToken` leer lassen
- Nur im HTTP-Callback-Modus sind diese Felder erforderlich
