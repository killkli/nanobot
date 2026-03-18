# Email

nanobot kann ein eigenes E-Mail-Konto nutzen. Er pollt neue Nachrichten über **IMAP** und antwortet über **SMTP** automatisch – wie ein persönlicher E-Mail-Assistent.

---

## Voraussetzungen

- Ein dediziertes E-Mail-Konto (am besten eine separate Adresse für den Bot)
- IMAP- und SMTP-Zugangsdaten
- Unterstützung für Gmail, Outlook oder jeden anderen standardkonformen IMAP/SMTP-Server

---

## Sicherheitsgate (Consent Gate)

!!! warning "`consentGranted` setzen"
    `consentGranted` **muss** auf `true` gesetzt werden, damit der Zugriff auf das Postfach aktiviert wird. Das verhindert unbeabsichtigten Zugriff auf echte Konten. Ist der Wert `false` oder fehlt er, bleibt der Kanal trotz `enabled: true` deaktiviert.

---

## Schritt 1: E-Mail-Konto vorbereiten

### Gmail

1. Lege ein eigenes Gmail-Konto an (z. B. `my-nanobot@gmail.com`)
2. Öffne die Google-Kontoeinstellungen → **Sicherheit** → aktiviere die Zwei-Faktor-Authentifizierung
3. Gehe zu [App-Passwörter](https://myaccount.google.com/apppasswords) und erstelle ein neues Passwort
4. Notiere das generierte 16-stellige Passwort; es dient sowohl für IMAP als auch SMTP

!!! tip "App-Passwort verwenden"
    Nutze das App-Passwort statt des Google-Konto-Passworts. Es ist sicherer und funktioniert trotz aktivierter Zwei-Faktor-Authentifizierung.

### Outlook/Hotmail

Verwende `outlook.office365.com` (Port 993) für IMAP und `smtp-mail.outlook.com` (Port 587) für SMTP.

### Eigene SMTP/IMAP-Server

Trage die Serveradresse und Ports ein, die dein E-Mail-Anbieter bereitstellt.

---

## Schritt 2: config.json konfigurieren

### Gmail-Beispiel

```json
{
  "channels": {
    "email": {
      "enabled": true,
      "consentGranted": true,
      "imapHost": "imap.gmail.com",
      "imapPort": 993,
      "imapUsername": "my-nanobot@gmail.com",
      "imapPassword": "your-app-password",
      "smtpHost": "smtp.gmail.com",
      "smtpPort": 587,
      "smtpUsername": "my-nanobot@gmail.com",
      "smtpPassword": "your-app-password",
      "fromAddress": "my-nanobot@gmail.com",
      "allowFrom": ["your-real-email@gmail.com"]
    }
  }
}
```

### Outlook-Beispiel

```json
{
  "channels": {
    "email": {
      "enabled": true,
      "consentGranted": true,
      "imapHost": "outlook.office365.com",
      "imapPort": 993,
      "imapUsername": "my-nanobot@outlook.com",
      "imapPassword": "YOUR_PASSWORD",
      "smtpHost": "smtp-mail.outlook.com",
      "smtpPort": 587,
      "smtpUsername": "my-nanobot@outlook.com",
      "smtpPassword": "YOUR_PASSWORD",
      "fromAddress": "my-nanobot@outlook.com",
      "allowFrom": ["your-real-email@example.com"]
    }
  }
}
```

### Vollständige Optionen

```json
{
  "channels": {
    "email": {
      "enabled": true,
      "consentGranted": true,
      "imapHost": "imap.gmail.com",
      "imapPort": 993,
      "imapUsername": "my-nanobot@gmail.com",
      "imapPassword": "your-app-password",
      "imapMailbox": "INBOX",
      "imapUseSsl": true,
      "smtpHost": "smtp.gmail.com",
      "smtpPort": 587,
      "smtpUsername": "my-nanobot@gmail.com",
      "smtpPassword": "your-app-password",
      "smtpUseTls": true,
      "smtpUseSsl": false,
      "fromAddress": "my-nanobot@gmail.com",
      "autoReplyEnabled": true,
      "pollIntervalSeconds": 30,
      "markSeen": true,
      "maxBodyChars": 12000,
      "subjectPrefix": "Re: ",
      "allowFrom": ["your-real-email@gmail.com"]
    }
  }
}
```

| Parameter | Standardwert | Beschreibung |
|-----------|--------------|--------------|
| `enabled` | `false` | Kanal aktivieren |
| `consentGranted` | `false` | **Muss** auf `true` gesetzt sein, damit der Postfachzugriff funktioniert |
| `imapHost` | `""` | IMAP-Server-Adresse |
| `imapPort` | `993` | IMAP-Port (SSL typischerweise 993) |
| `imapUsername` | `""` | IMAP-Benutzername |
| `imapPassword` | `""` | IMAP-Passwort |
| `imapMailbox` | `"INBOX"` | Überwachter Ordner |
| `imapUseSsl` | `true` | SSL/TLS für IMAP nutzen |
| `smtpHost` | `""` | SMTP-Server-Adresse |
| `smtpPort` | `587` | SMTP-Port (STARTTLS üblich) |
| `smtpUsername` | `""` | SMTP-Benutzername |
| `smtpPassword` | `""` | SMTP-Passwort |
| `smtpUseTls` | `true` | STARTTLS aktivieren (z. B. Gmail-Port 587) |
| `smtpUseSsl` | `false` | SSL für SMTP (Port 465) |
| `fromAddress` | `""` | Absenderadresse für Antworten |
| `autoReplyEnabled` | `true` | Automatische Antworten aktivieren (Auf `false` setzen, um nur zu lesen) |
| `pollIntervalSeconds` | `30` | IMAP-Polling-Intervall in Sekunden |
| `markSeen` | `true` | Nachrichten nach dem Abruf als gelesen markieren |
| `maxBodyChars` | `12000` | Maximale Länge der analysierten Nachricht |
| `subjectPrefix` | `"Re: "` | Präfix für Antworten |
| `allowFrom` | `[]` | Liste erlaubter Absenderadressen |

---

## Schritt 3: Gateway starten

```bash
nanobot gateway
```

nanobot prüft das Postfach alle `pollIntervalSeconds` Sekunden, verarbeitet neue Mails und sendet Antworten.

---

## Nur Lesen (keine Antworten)

```json
{
  "channels": {
    "email": {
      "autoReplyEnabled": false
    }
  }
}
```

---

## Alle Mails erlauben

```json
{
  "channels": {
    "email": {
      "allowFrom": ["*"]
    }
  }
}
```

!!! warning "Spam-Risiko"
    `allowFrom": ["*"]` lässt alle eintrudelnden E-Mails zu – auch Spam. Nutze diese Einstellung nur in kontrollierten Umgebungen.

---

## Häufige Fragen

**Gmail meldet „Anmeldung blockiert“?**

- Stelle sicher, dass du das App-Passwort nutzt und nicht das Google-Konto-Passwort
- Aktiviere die Zwei-Faktor-Authentifizierung

**SMTP-Verbindung schlägt fehl?**

- Gmail (Port 587): `smtpUseTls: true`, `smtpUseSsl: false`
- Gmail (Port 465): `smtpUseTls: false`, `smtpUseSsl: true`
- Stelle sicher, dass `fromAddress` mit `smtpUsername` übereinstimmt

**Bot antwortet nicht?**

- `consentGranted` muss auf `true` stehen
- Der Absender muss in `allowFrom` gelistet sein
- Prüfe die Logs auf Fehler beim IMAP-Polling
