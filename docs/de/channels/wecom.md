# WeCom / 企業微信

nanobot verbindet sich mit dem WeCom AI Bot über eine **WebSocket-Long-Connection**, sodass weder öffentliche IP noch Webhook benötigt werden. Texte, Bilder, Sprachnachrichten und Dateien werden unterstützt.

---

## Voraussetzungen

- Ein WeCom-Admin-Account
- Das Unternehmen muss AI Bot-Funktionalität aktiviert haben

> nanobot nutzt das Community-Python-SDK [wecom-aibot-sdk-python](https://github.com/chengyongru/wecom_aibot_sdk), die Python-Variante des offiziellen [@wecom/aibot-node-sdk](https://www.npmjs.com/package/@wecom/aibot-node-sdk).

---

## Schritt 1: Optionales SDK installieren

WeCom benötigt zusätzliche Abhängigkeiten:

```bash
pip install nanobot-ai[wecom]
```

Oder mit `uv`:

```bash
uv pip install nanobot-ai[wecom]
```

---

## Schritt 2: WeCom AI Bot erstellen

1. Melde dich beim [WeCom-Admin-Portal](https://work.weixin.qq.com/wework_admin/frame) an
2. Gehe zu **应用管理** → **智慧机器人** → **机器人创建**
3. Wähle den **API-Modus** und aktiviere die **Long Connection** (WebSocket)
4. Kopiere nach der Erstellung die **Bot ID** und das **Secret**

!!! tip "Long Connection-Modus"
    Mit dem Long Connection-Modus verbindet sich nanobot aktiv mit WeCom, sodass keine öffentliche IP nötig ist.

---

## Schritt 3: config.json anpassen

```json
{
  "channels": {
    "wecom": {
      "enabled": true,
      "botId": "your_bot_id",
      "secret": "your_bot_secret",
      "allowFrom": ["your_user_id"]
    }
  }
}
```

### Vollständige Optionen

```json
{
  "channels": {
    "wecom": {
      "enabled": true,
      "botId": "your_bot_id",
      "secret": "your_bot_secret",
      "allowFrom": ["your_user_id"],
      "welcomeMessage": ""
    }
  }
}
```

| Parameter | Standardwert | Beschreibung |
|-----------|--------------|--------------|
| `enabled` | `false` | Kanal aktivieren |
| `botId` | `""` | WeCom AI Bot Bot ID |
| `secret` | `""` | WeCom AI Bot Secret |
| `allowFrom` | `[]` | Liste erlaubter User IDs |
| `welcomeMessage` | `""` | Begrüßungsnachricht für neue Nutzer (leer = keine Nachricht)

---

## Schritt 4: Gateway starten

```bash
nanobot gateway
```

---

## Deine User ID herausfinden

Trage in `allowFrom` die WeCom User ID (userid) ein.

**So funktioniert es:**

1. Setze `allowFrom` vorübergehend auf `["*"]`, um alle Nutzer zuzulassen
2. Starte nanobot und sende dem Bot eine Nachricht
3. Die Logs zeigen deine User ID
4. Setze `allowFrom` wieder auf `["your_user_id"]`

---

## Multimediale Unterstützung

WeCom kann folgende Nachrichtenarten verarbeiten:

| Typ | Verhalten |
|-----|-----------|
| Text | Wird direkt an die KI weitergegeben |
| Bilder | Werden heruntergeladen und (bei visuellen Modellen) analysiert |
| Sprache | Mit Groq API-Key automatisch transkribiert |
| Dateien | Werden heruntergeladen und weitergeleitet |
| Gemischte Inhalte | Alle Komponenten separat verarbeitet |

---

## Häufige Fragen

**Erhalte ich trotz Installation eine Fehlermeldung?**

- Stelle sicher, dass du im richtigen Python-Environment installiert hast
- Nutze `uv sync` oder `pip install nanobot-ai[wecom]`, um erneut zu installieren

**Bot verbindet sich nicht?**

- Prüfe, ob Bot ID und Secret korrekt sind
- Stelle sicher, dass es sich um einen Long Connection API-Bot handelt
- Schau in die Logs für weitere Hinweise

**Wie wird die Willkommensnachricht eingestellt?**

- Trage eine Zeichenkette in `welcomeMessage` ein, damit der Bot bei der ersten Interaktion eine Nachricht sendet
- Lass das Feld leer, um keine Begrüßung zu versenden
