# WhatsApp

nanobot verbindet sich über eine Node.js-Bridge mit dem WhatsApp Web-Protokoll. Die Bridge nutzt das [@whiskeysockets/baileys](https://github.com/WhiskeySockets/Baileys) SDK und kommuniziert über WebSocket mit dem nanobot-Gateway.

---

## Voraussetzungen

- **Node.js ≥ 18**
- Ein WhatsApp-Account mit verbundenem Smartphone

---

## Schritt 1: Node.js-Version prüfen

```bash
node --version
# Sollte v18.0.0 oder neuer anzeigen
```

Bei Bedarf von [nodejs.org](https://nodejs.org) herunterladen.

---

## Schritt 2: Gerät verbinden (QR-Code scannen)

```bash
nanobot channels login
```

Im Anschluss erscheint ein QR-Code. Öffne in WhatsApp auf dem Smartphone:

1. **Einstellungen** → **Verknüpfte Geräte**
2. **Gerät verknüpfen** auswählen
3. QR-Code am Terminal scannen

Nach erfolgreicher Verbindung speichert die Bridge die Session, sodass ein erneutes Scannen meistens nicht nötig ist.

!!! tip "Erstmaliger Login"
    `nanobot channels login` lädt und baut automatisch die Node.js-Bridge unter `~/.nanobot/bridge/` auf. Beim ersten Aufruf dauert dies etwas länger.

---

## Schritt 3: config.json anpassen

```json
{
  "channels": {
    "whatsapp": {
      "enabled": true,
      "allowFrom": ["+886912345678"]
    }
  }
}
```

### Vollständige Optionen

```json
{
  "channels": {
    "whatsapp": {
      "enabled": true,
      "bridgeUrl": "ws://localhost:3001",
      "bridgeToken": "",
      "allowFrom": ["+886912345678"]
    }
  }
}
```

| Parameter | Standardwert | Beschreibung |
|-----------|--------------|--------------|
| `enabled` | `false` | Kanal aktivieren |
| `bridgeUrl` | `"ws://localhost:3001"` | WebSocket-URL der Bridge |
| `bridgeToken` | `""` | Optionales Token für die Bridge |
| `allowFrom` | `[]` | Liste erlaubter WhatsApp-Nummern (inkl. Ländervorwahl, z. B. `+886912345678`)

---

## Schritt 4: Gateway starten

Du benötigst zwei Terminals:

```bash
# Terminal 1: WhatsApp Bridge
nanobot channels login

# Terminal 2: nanobot Gateway
nanobot gateway
```

!!! note "Reihenfolge"
    Starte zuerst die Bridge (`channels login`), dann das Gateway. Die Bridge läuft im Hintergrund weiter und hält die WhatsApp-Verbindung aufrecht.

---

## Bridge-Architektur

```
WhatsApp App (Smartphone)
    ↕ WhatsApp Web-Protokoll
Node.js Bridge (~/.nanobot/bridge/)
    ↕ WebSocket (ws://localhost:3001)
nanobot Gateway (Python)
    ↕ Nachrichtensystem
AI Agent
```

Die Bridge übernimmt das WhatsApp-Protokoll, nanobot spricht nur über einfache WebSocket-Nachrichten mit ihr.

---

## Bridge aktualisieren

Nach einem Upgrade von nanobot muss die Bridge ggf. neu gebaut werden:

```bash
rm -rf ~/.nanobot/bridge && nanobot channels login
```

!!! warning "Bridge manuell rebuilden"
    Die Bridge wird bei Updates nicht automatisch aktualisiert. Führe den obigen Befehl nach jeder nanobot-Aktualisierung aus.

---

## FAQ

**QR-Code läuft sofort ab?**

- WhatsApp-QR-Codes sind zeitlich begrenzt. Scanne ihn schnell oder führe den Login neu aus.

**Muss ich nach Neustart erneut scannen?**

- Normalerweise nicht. Die Session liegt in `~/.nanobot/bridge/`. Zum Zurücksetzen diesen Ordner löschen und den Login erneut starten.

**Verbindung bricht dauerhaft ab?**

- nanobot versucht automatisch neu zu verbinden.
- Falls die Verbindung dauerhaft scheitert, kann WhatsApp die zugehörige Sitzung löschen – dann QR-Code neu scannen.

**`allowFrom`-Format?**

- Nutze internationale Telefonnummern inklusive `+` und Ländervorwahl (z. B. `+886912345678`).
- Alternativ `"*"`, um alle Kontakte zuzulassen.
