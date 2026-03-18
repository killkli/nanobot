# Leitfaden für eingebaute Tools

Nanobot-Agenten bringen eine Reihe eingebauter Tools mit, die Shell-Befehle ausführen, Dateisysteme lesen und schreiben, Webanfragen durchführen, Cron/Planung erledigen und Nachrichten verschicken. Diese Seite erklärt Zweck, Parameter, Sicherheitsaspekte und Beispiele zu jedem Tool.

---

## Shell-Tool (`exec`)

Führt beliebige Shell-Kommandos aus und liefert stdout sowie stderr zurück. Nutze es für Skripte, Paketinstallationen oder Infrastrukturaufgaben.

### Parameter

| Parameter | Typ | Erforderlich | Beschreibung |
|-----------|-----|--------------|--------------|
| `command` | string | Ja | Das auszuführende Shell-Kommando |
| `working_dir` | string | Nein | Arbeitsverzeichnis für den Befehl |
| `timeout` | integer | Nein | Timeout in Sekunden (Standard 60, Max 600) |

### Beispiele

```bash
# Python-Skript ausführen
exec(command="python3 script.py")

# npm-Paket installieren (längerer Timeout)
exec(command="npm install", working_dir="/project", timeout=300)

# Dateien in einem bestimmten Verzeichnis listen
exec(command="ls -la", working_dir="/tmp")
```


### Sicherheitsmechanismen

Das Shell-Tool blockiert gefährliche Muster automatisch:

| Blockiertes Muster | Beschreibung |
|-------------------|--------------|
| `rm -rf` / `rm -r` | Rekursives Löschen |
| `format` / `mkfs` / `diskpart` | Laufwerksformatierung |
| `dd if=` | Direkter Schreibzugriff auf Blockgeräte |
| `shutdown` / `reboot` / `poweroff` | Systemabschaltung |
| Fork-Bombe `:(){ ... }` | Ressourcenerschöpfung |
| URLs mit internen IPs | SSRF-Schutz |

Ist `restrict_to_workspace` aktiviert, werden alle Pfade außerhalb des Workspace (inkl. `../`) verweigert.

### Konfigurationsoptionen

```yaml
tools:
  exec:
    timeout: 120          # Standard-Timeout in Sekunden
    path_append: "/usr/local/bin"  # Zusätzlicher Pfad für PATH
  restrict_to_workspace: false    # Werkzeuge auf den Workspace beschränken
```

Über `deny_patterns` (RegEx-Liste) lässt sich die Blacklist erweitern oder überschreiben. `allow_patterns` definiert stattdessen explizite Ausnahmen (Whitelist-Verhalten).

### Ausgabebegrenzung

Ein Aufruf liefert maximal **10.000 Zeichen**. Bei längeren Ausgaben behält das System Anfang und Ende bei und weist auf die abgeschnittene Länge hin.

---

## Dateisystem-Tools

Diese Gruppe umfasst `read_file`, `write_file`, `edit_file` und `list_dir`. Sie arbeiten mit Pfaden relativ zum Workspace oder mit absoluten Pfaden.

### Pfadauflösung

- **Relative Pfade** beziehen sich auf den Workspace des aktuell laufenden Agents
- **Absolute Pfade** werden direkt verwendet
- `restrict_to_workspace: true` blockiert Zugriffe außerhalb des Workspaces

---

### Datei lesen (`read_file`)

Liest eine Datei und gibt den Inhalt mit Zeilennummern zurück.

#### Parameter

| Parameter | Typ | Erforderlich | Beschreibung |
|-----------|-----|--------------|--------------|
| `path` | string | Ja | Pfad zur Datei |
| `offset` | integer | Nein | Startzeile (1-basiert, Standard 1) |
| `limit` | integer | Nein | Maximal zu lesende Zeilen (Standard 2000) |

#### Beispiele

```python
# Ganze Datei lesen
read_file(path="config.yaml")

# Zeilen 500–700 lesen
read_file(path="large_log.txt", offset=500, limit=200)

# Absoluten Pfad verwenden
read_file(path="/etc/hosts")
```


Die Ausgabe enthält Zeilennummern:
```
1| # Dies ist die erste Zeile
2| Dies ist die zweite Zeile
```

Innerhalb eines Aufrufs gibt `read_file` bis zu **128.000 Zeichen** zurück. Längere Dateien liefern am Ende einen empfohlenen `offset`, um die nächste Seite zu laden.

---

### Datei schreiben (`write_file`)

Schreibt den vollständigen Inhalt in eine Datei und erzeugt fehlende Verzeichnisse automatisch.

#### Parameter

| Parameter | Typ | Erforderlich | Beschreibung |
|-----------|-----|--------------|--------------|
| `path` | string | Ja | Zielpfad |
| `content` | string | Ja | Inhalt, der geschrieben werden soll |

#### Beispiele

```python
# Neue Datei schreiben
write_file(path="output/report.txt", content="Report-Inhalt...")

# Konfigurationsdatei anlegen (Verzeichnisse werden erstellt)
write_file(path="config/settings.json", content='{"debug": true}')
```

> **Hinweis**: `write_file` überschreibt bestehende Dateien vollständig. Für partielle Änderungen nutze `edit_file`.

---

### Datei editieren (`edit_file`)

Ersetzt gezielt Textabschnitte in einer Datei. Unterstützt leichte Whitespaces-Differenzen.

#### Parameter

| Parameter | Typ | Erforderlich | Beschreibung |
|-----------|-----|--------------|--------------|
| `path` | string | Ja | Datei, die angepasst werden soll |
| `old_text` | string | Ja | Zu ersetzender Text |
| `new_text` | string | Ja | Ersatztext |
| `replace_all` | boolean | Nein | Alle Treffer ersetzen (Standard `false`) |

#### Beispiele

```python
# Einzelnes Vorkommen ersetzen
edit_file(
    path="config.yaml",
    old_text="debug: false",
    new_text="debug: true"
)

# Alle Vorkommen ersetzen
edit_file(
    path="app.py",
    old_text="import old_module",
    new_text="import new_module",
    replace_all=True
)
```

Wenn `old_text` mehrfach vorkommt und `replace_all` nicht gesetzt ist, gibt das Tool eine Warnung aus. Wird kein exakter Block gefunden, zeigt es die ähnlichste Stelle an.

---

### Verzeichnis auflisten (`list_dir`)

Listet den Inhalt eines Verzeichnisses auf, optional rekursiv.

#### Parameter

| Parameter | Typ | Erforderlich | Beschreibung |
|-----------|-----|--------------|--------------|
| `path` | string | Ja | Verzeichnis |
| `recursive` | boolean | Nein | Rekursives Listing (Standard `false`) |
| `max_entries` | integer | Nein | Max. zurückzugebende Einträge (Standard 200) |

#### Beispiele

```python
# Aktuelles Verzeichnis auflisten
list_dir(path=".")

# Projektstruktur rekursiv zeigen
list_dir(path="/project", recursive=True, max_entries=500)
```

Die folgenden Ordner werden automatisch ignoriert: `.git`, `node_modules`, `__pycache__`, `.venv`, `venv`, `dist`, `build`, `.tox`, `.mypy_cache`, `.pytest_cache`, `.ruff_cache`.

---

## Netzwerkt-Tools

### Web-Recherche (`web_search`)

Sucht über den konfigurierten Provider und liefert Titel, URLs und Snippets.

#### Parameter

| Parameter | Typ | Erforderlich | Beschreibung |
|-----------|-----|--------------|--------------|
| `query` | string | Ja | Suchanfrage |
| `count` | integer | Nein | Anzahl Ergebnisse (1–10, Standard laut Konfiguration) |

#### Beispiele

```python
# Basis-Suche
web_search(query="Python asyncio Anleitung")

# Ergebnisanzahl fixieren
web_search(query="nanobot AI framework", count=5)
```

#### Anbieter

| Anbieter | Konfigurationswert | API-Key notwendig | Beschreibung |
|----------|--------------------|-------------------|--------------|
| Brave Search | `brave` | Ja (`BRAVE_API_KEY`) | Standardanbieter; ohne Key fällt es auf DuckDuckGo zurück |
| Tavily | `tavily` | Ja (`TAVILY_API_KEY`) | KI-gestützte Recherche für tiefere Analysen |
| DuckDuckGo | `duckduckgo` | Nein | Kostenlos und ohne Key |
| SearXNG | `searxng` | Nein (Self-hosted) | Open-Source-Instanz |
| Jina | `jina` | Ja (`JINA_API_KEY`) | Semantische Suche mit Reader API |

#### Konfiguration

```yaml
tools:
  web:
    search:
      provider: brave          # Suchanbieter
      api_key: "YOUR_KEY"      # API-Key oder Umgebungsvariable
      max_results: 5           # Standard-Trefferanzahl
    proxy: "http://127.0.0.1:7890"  # HTTP/SOCKS5-Proxy (optional)
```

---

### Webseiten erfassen (`web_fetch`)

Lädt eine URL und konvertiert den Inhalt automatisch in Markdown oder reinen Text.

#### Parameter

| Parameter | Typ | Erforderlich | Beschreibung |
|-----------|-----|--------------|--------------|
| `url` | string | Ja | Ziel-URL |
| `extractMode` | string | Nein | Ausgabeformat: `markdown` (Standard) oder `text` |
| `maxChars` | integer | Nein | Max. Zeichen (Standard 50.000) |

#### Beispiele

```python
# Markdown-Ausgabe
web_fetch(url="https://docs.python.org/3/library/asyncio.html")

# Nur Text mit Limit
web_fetch(url="https://example.com/article", extractMode="text", maxChars=10000)
```

#### Ablauf

1. Nutzt bevorzugt die **Jina Reader API** (wenn `JINA_API_KEY` gesetzt ist)
2. Bei Limits (429) oder Fehlern Rückfall auf `readability-lxml`
3. JSON-Antworten werden formatiert zurückgegeben
4. Externe Inhalte erhalten Warnhinweise, damit der Agent sie als Daten erkennt, nicht als Befehle

#### Sicherheit

- Nur `http://` und `https://` sind erlaubt
- Private IPs (RFC 1918), `localhost` und Loopbacks werden blockiert (SSRF-Schutz)
- Redirects werden bei jedem Schritt auf erlaubte IPs geprüft

#### Proxy

```yaml
tools:
  web:
    proxy: "http://127.0.0.1:7890"   # HTTP-Proxy
    # proxy: "socks5://127.0.0.1:1080"  # SOCKS5-Proxy
```

---

## Cron-Tool (`cron`)

Dient Erinnerungen und wiederkehrenden Aufgaben mit festen Intervallen, Cron-Ausdrücken oder Einmalterminen.

### Aktionen

| `action` | Beschreibung |
|----------|--------------|
| `add` | Neuen Cron-Job anlegen |
| `list` | Alle Cron-Jobs auflisten |
| `remove` | Einen Cron-Job entfernen |

### Parameter (für `add`)

| Parameter | Typ | Beschreibung |
|-----------|-----|--------------|
| `message` | string | Erinnerungstext oder Beschreibung |
| `every_seconds` | integer | Fixe Wiederholungsdauer in Sekunden |
| `cron_expr` | string | Cron-Ausdruck (z. B. `"0 9 * * *"`) |
| `tz` | string | IANA-Zeitzone (nur mit `cron_expr`, z. B. `"Asia/Taipei"`) |
| `at` | string | ISO-8601-Zeitpunkt für Einzeltermine (`"2026-03-20T10:00:00"`) |
| `job_id` | string | Job-ID (für `remove`) |

### Beispiele

```python
# Alle 20 Minuten erinnern
cron(action="add", message="Kurze Bewegungspause", every_seconds=1200)

# Täglich um 9 Uhr (Asia/Taipei)
cron(action="add", message="Tagesbericht senden", cron_expr="0 9 * * *", tz="Asia/Taipei")

# Einmalige Erinnerung
cron(action="add", message="Meeting um 15 Uhr", at="2026-03-18T15:00:00")

# Montag bis Freitag um 17 Uhr
cron(action="add", message="Feierabend vorbereiten", cron_expr="0 17 * * 1-5", tz="Asia/Taipei")

# Alle Jobs anzeigen
cron(action="list")

# Job entfernen (ID aus `list`)
cron(action="remove", job_id="abc123")
```

### Zeitvergleich

| Beschreibung | Parameter |
|--------------|-----------|
| Alle 20 Minuten | `every_seconds: 1200` |
| Jede Stunde | `every_seconds: 3600` |
| Täglich um 8 Uhr | `cron_expr: "0 8 * * *"` |
| Wochentags 17 Uhr | `cron_expr: "0 17 * * 1-5"` |
| Monatlich am 1. um Mitternacht | `cron_expr: "0 0 1 * *"` |
| Einzelner Zeitpunkt | `at: "2026-03-20T10:00:00"` |

> **Hinweis**: Cron-Aufgaben dürfen innerhalb ihres eigenen Callbacks **keine neuen Cron-Aufgaben** anlegen.

---

## Spawn-Tool (`spawn`)

Startet Subagenten im Hintergrund, damit komplexe oder lang laufende Aufgaben asynchron ausgeführt werden können. Der Hauptagent behält Kontrolle, während die Ergebnisse später zurückgemeldet werden.

### Parameter

| Parameter | Typ | Erforderlich | Beschreibung |
|-----------|-----|--------------|--------------|
| `task` | string | Ja | Beschreibung der Aufgabe für den Subagenten |
| `label` | string | Nein | Kurzer Name zur Identifikation |

### Beispiele

```python
# Umfangreiche Logdateien analysieren
spawn(
    task="Analysiere /data/logs/ und zähle Fehler pro Stunde, gebe die Ergebnisse tabellarisch zurück",
    label="Log-Analyse"
)

# Mehrere Aufgaben parallel starten
spawn(task="Neueste Nanobot-Releases via GitHub API prüfen", label="Release-Check")
spawn(task="Neue Features in Python 3.13 recherchieren", label="Feature-Research")
```

### Einsatzszenarien

- Workflows mit mehreren Tool-Aufrufen
- Zeitintensive Datenverarbeitung oder Netzwerkanfragen
- Parallele Teilaufgaben, die später zusammengeführt werden

---

## Nachrichten-Tool (`message`)

Sendet proaktiv Nachrichten, inklusive kanalübergreifender Zustellung und Medienanhängen.

### Parameter

| Parameter | Typ | Erforderlich | Beschreibung |
|-----------|-----|--------------|--------------|
| `content` | string | Ja | Nachrichtentext |
| `channel` | string | Nein | Zielkanal (`telegram`, `discord`, …) |
| `chat_id` | string | Nein | Ziel-Chat- oder Nutzer-ID |
| `media` | array | Nein | Liste mit Attachment-Pfaden (Bilder, Audio, Dokumente) |

### Beispiele

```python
# Reiner Text
message(content="Aufgabe abgeschlossen!")

# Mit Anhängen
message(
    content="Hier ist der heutige Report",
    media=["/workspace/report.pdf", "/workspace/chart.png"]
)

# Kanalübergreifend (Slack → Telegram)
message(
    content="Deployment erfolgreich",
    channel="telegram",
    chat_id="123456789"
)
```

### Wann einsetzen?

- Cron-Jobs informieren nach Abschluss automatisch
- Subagenten (`spawn`) liefern Ergebnisse
- Dateien wie Bilder oder PDFs sollen verteilt werden

---

## Globale Tool-Konfiguration

Diese Einstellungen gelten für alle Tools und befinden sich im Abschnitt `tools` der `config.yaml`:

```yaml
tools:
  restrict_to_workspace: false   # Beschränkt Tools auf den Workspace
  exec:
    timeout: 60                  # Default-Timeout für Shell-Aufrufe (Sekunden)
    path_append: ""             # Zusätzliche Pfade für PATH
  web:
    proxy: null                   # Optionaler HTTP/SOCKS5-Proxy
    search:
      provider: brave             # Suchanbieter
      api_key: ""                # API-Key oder Umgebungsvariable
      max_results: 5              # Standardanzahl Treffer
  mcp_servers: {}                # MCP-Serverkonfigurationen (siehe MCP-Guide)
```
