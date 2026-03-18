# QQ

nanobot verbindet sich über die offizielle QQ **botpy SDK** per WebSocket, sodass keine öffentliche IP erforderlich ist. Private Chats (C2C) und Gruppenerwähnungen (@) sowie Antworten in Klartext oder Markdown werden unterstützt.

---

## Voraussetzungen

- Ein QQ-Account
- Entwicklerzugang auf der QQ Open Platform

---

## Schritt 1: Entwicklerzugang beantragen und Bot erstellen

1. Besuche die [QQ Open Platform](https://q.qq.com)
2. Klicke auf **立即接入** und beantrage als Privat- oder Unternehmenskonto Entwicklerrechte
3. Nach der Genehmigung gehe zu **机器人管理** → **创建机器人**
4. Fülle die Basisinformationen aus und erstelle den Bot

---

## Schritt 2: AppID und AppSecret kopieren

1. Öffne die Bot-Verwaltungsseite
2. Gehe zu **开发设置**
3. Kopiere **AppID** und **AppSecret**

---

## Schritt 3: Sandbox-Test einrichten

Vor dem Live-Gang empfiehlt sich ein Sandbox-Test:

1. Öffne in der Bot-Verwaltung die **沙盒配置**
2. Unter **在消息列表配置** auf **添加成员** klicken und deine QQ-Nummer hinzufügen
3. Nach dem Hinzufügen den QR-Code des Bots mit der mobilen QQ-App scannen
4. Die Bot-Seite öffnen und auf **发消息** tippen, um zu testen

!!! warning "Sandbox vs. Produktionsumgebung"
    Die Sandbox dient ausschließlich Entwicklungszwecken. Für den Einsatz im Produktivbetrieb musst du den Bot über das Verwaltungsportal zur Prüfung einreichen und veröffentlichen. Details: [QQ Bot 文档](https://bot.q.qq.com/wiki/)

---

## Schritt 4: config.json konfigurieren

```json
{
  "channels": {
    "qq": {
      "enabled": true,
      "appId": "YOUR_APP_ID",
      "secret": "YOUR_APP_SECRET",
      "allowFrom": ["YOUR_OPENID"],
      "msgFormat": "plain"
    }
  }
}
```

### Vollständige Optionen

```json
{
  "channels": {
    "qq": {
      "enabled": true,
      "appId": "YOUR_APP_ID",
      "secret": "YOUR_APP_SECRET",
      "allowFrom": ["YOUR_OPENID"],
      "msgFormat": "plain"
    }
  }
}
```

| Parameter | Standardwert | Beschreibung |
|-----------|--------------|--------------|
| `enabled` | `false` | Kanal aktivieren |
| `appId` | `""` | QQ Bot AppID |
| `secret` | `""` | QQ Bot AppSecret |
| `allowFrom` | `[]` | Liste erlaubter OpenIDs |
| `msgFormat` | `"plain"` | Nachrichtenformat (`"plain"` oder `"markdown"`)

### `msgFormat`

| Wert | Einsatzszenario |
|------|-----------------|
| `"plain"` (Standard) | Reiner Text – kompatibel mit allen QQ-Clients |
| `"markdown"` | Markdown-Format – nur von neueren QQ-Clients unterstützt |

---

## Schritt 5: Gateway starten

```bash
nanobot gateway
```

---

## So findest du deine OpenID

`allowFrom` muss die QQ OpenID (nicht die QQ-Nummer) eines Benutzers enthalten.

**Vorgehen:**

1. Setze `allowFrom` testweise auf `[
"*"]`, um alle Nutzer zuzulassen
2. Starte nanobot und sende dem Bot eine Nachricht
3. In den Logs wird deine OpenID angezeigt
4. Trage die OpenID in `allowFrom` ein und entferne `"*"`

---

## Gruppenunterstützung

Der QQ Bot unterstützt derzeit:

- **Private Chats (C2C)** – Eins-zu-eins-Nachrichten
- **Gruppenerwähnungen** – Antworten bei @-Erwähnung
- **Direct Messages über Guild**

---

## Produktionsfreigabe

Nach dem Sandbox-Test:

1. Navigiere zu **版本管理** → Neue Version erstellen
2. Beschreibe Funktionen und Screenshots
3. Reiche die Version zur Prüfung ein
4. Nach Genehmigung veröffentlichen

Siehe auch: [QQ Bot 官方文档](https://bot.q.qq.com/wiki/)

---

## Häufige Fragen

**Bot erhält Nachrichten, antwortet aber nicht?**

- Stelle sicher, dass deine OpenID in `allowFrom` steht (nicht die QQ-Nummer)
- Prüfe die Logs auf „Access denied"

**Bot reagiert in Gruppen nicht?**

- In Gruppenchats muss der Bot @erwähnt werden
- Der Bot muss Mitglied der Gruppe sein

**Sandbox-Umgebung zeigt keinen Bot?**

- Vergewissere dich, dass deine QQ-Nummer in der Sandbox-Config hinzugefügt wurde
- Verwende die mobile QQ-App (nicht die Desktop-Version), um den QR-Code zu scannen
