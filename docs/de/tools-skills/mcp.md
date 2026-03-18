# MCP-Integrationsleitfaden

MCP (Model Context Protocol) ist ein offener Standard von Anthropic, mit dem AI-Agenten externe Tool-Server über eine einheitliche Oberfläche einbinden können. Nanobot unterstützt MCP vollständig und lädt zur Laufzeit beliebige Tools von MCP-Servern, ohne Änderungen am Core-Code.

---

## Wie MCP funktioniert

```
Nanobot-Agent
  → verbindet sich beim Start mit MCP-Servern
  → lädt die Liste verfügbarer Tools
  → kapselt jedes Tool als mcp_<Servername>_<Toolname>
  → nutzt die MCP-Tools wie eingebaute Tools
```

Jedes MCP-Tool erscheint in Nanobot als `mcp_<server>_<tool>`. Verbindet sich Nanobot z. B. mit einem Server namens `filesystem`, wird `read_file` als `mcp_filesystem_read_file` verfügbar.

---

## Konfiguration

Alle MCP-Server werden unter `tools.mcp_servers` in `config.yaml` definiert:

```yaml
tools:
  mcp_servers:
    <server-name>:
      type: stdio        # oder sse oder streamableHttp (optional, Nanobot erkennt automatisch)
      command: "..."     # Nur für stdio: Startbefehl
      args: []           # Nur für stdio: Argumente
      env: {}            # Nur für stdio: Zusätzliche Umgebungsvariablen
      url: "..."         # Für HTTP/SSE: Endpoint
      headers: {}        # Für HTTP/SSE: Custom Header
      tool_timeout: 30   # Timeout pro Toolaufruf
      enabled_tools:     # Welche Tools geladen werden sollen ("[\"*\"]" aktiviert alle)
        - "*"
```

### Automatische Transporterkennung

Lässt du den `type`-Eintrag weg, wählt Nanobot automatisch:

| Bedingung | Ergebnis |
|-----------|----------|
| `command` vorhanden | `stdio` |
| `url` endet auf `/sse` | `sse` |
| Sonst `url` vorhanden | `streamableHttp` |

---

## Stdio-MCP-Server

Stdio-Server laufen lokal als Subprocess und kommunizieren über stdin/stdout. Ideal für lokale Tools und CLI-Wrapping.

### Beispiel: Filesystem-MCP

```yaml
tools:
  mcp_servers:
    filesystem:
      command: "npx"
      args:
        - "-y"
        - "@modelcontextprotocol/server-filesystem"
        - "/Users/john/documents"
      enabled_tools:
        - "read_file"
        - "write_file"
        - "list_directory"
```

Nach dem Start kannst du `mcp_filesystem_read_file`, `mcp_filesystem_write_file` und `mcp_filesystem_list_directory` wie normale Tools verwenden.

### Beispiel: GitHub-MCP

```yaml
tools:
  mcp_servers:
    github:
      command: "npx"
      args:
        - "-y"
        - "@modelcontextprotocol/server-github"
      env:
        GITHUB_PERSONAL_ACCESS_TOKEN: "ghp_xxxxxxxxxxxxx"
      enabled_tools:
        - "create_issue"
        - "get_pull_request"
        - "list_commits"
```

### Beispiel: SQLite-MCP

```yaml
tools:
  mcp_servers:
    sqlite:
      command: "uvx"
      args:
        - "mcp-server-sqlite"
        - "--db-path"
        - "/data/mydb.sqlite"
```

### Beispiel: eigener Python-MCP-Server

```yaml
tools:
  mcp_servers:
    my-tools:
      command: "python3"
      args:
        - "/path/to/my_mcp_server.py"
      env:
        MY_API_KEY: "secret"
      tool_timeout: 60
```

---

## HTTP/SSE-MCP-Server

Remote-Server kommunizieren über HTTP oder Server-Sent Events. Geeignet für Cloud-Dienste oder geteilte Tool-Server.

### SSE-Transport

URLs, die auf `/sse` enden, nutzen automatisch SSE:

```yaml
tools:
  mcp_servers:
    remote-tools:
      url: "https://mcp.example.com/sse"
      headers:
        Authorization: "Bearer your-token-here"
        X-Custom-Header: "value"
      tool_timeout: 45
```

### StreamableHTTP-Transport

Normale HTTP-Endpoints verwenden StreamableHTTP:

```yaml
tools:
  mcp_servers:
    cloud-service:
      url: "https://api.example.com/mcp"
      headers:
        Authorization: "Bearer your-token-here"
      tool_timeout: 60
      enabled_tools:
        - "search"
        - "summarize"
```

### Transport explizit festlegen

Wenn die automatische Erkennung nicht passt, gib den Typ vor:

```yaml
tools:
  mcp_servers:
    my-server:
      type: sse            # Erzwingt SSE
      url: "https://..."
```

---

## Tool-Filter (`enabled_tools`)

Mit `enabled_tools` bestimmst du, welche Tools vom Server geladen werden. Das reduziert die Context-Nutzung.

```yaml
enabled_tools:
  - "*"           # Alle Tools (Standard)
```

```yaml
enabled_tools:
  - "read_file"
  - "write_file"
```

```yaml
enabled_tools:
  - "mcp_filesystem_read_file"
  - "mcp_filesystem_write_file"
```

```yaml
enabled_tools: [] # Keine Tools aktivieren (Server bleibt).```

Wenn ein Eintrag nicht mit den tatsächlich verfügbaren Tools übereinstimmt, protokolliert Nanobot eine Warnung und listet die gültigen Namen auf.

---

## Tool-Timeout (`tool_timeout`)

Jeder MCP-Toolaufruf hat seinen eigenen Timeout (Sekunden). Bei Überschreitung gibt das Tool einen Fehler zurück; der Agent kann erneut versuchen oder ausweichen.

```yaml
tools:
  mcp_servers:
    slow-service:
      url: "https://..."
      tool_timeout: 120    # Erlaubt bis zu 120 Sekunden
```

Passe die Timeout-Werte pro Server individuell an, je nach Ausführungszeit der jeweiligen Tools.

---

## Praktische MCP-Server-Beispiele

### Offizielle Server (`@modelcontextprotocol/*`)

```yaml
tools:
  mcp_servers:
    filesystem:
      command: "npx"
      args: ["-y", "@modelcontextprotocol/server-filesystem", "/home/user"]

    github:
      command: "npx"
      args: ["-y", "@modelcontextprotocol/server-github"]
      env:
        GITHUB_PERSONAL_ACCESS_TOKEN: "ghp_xxx"

    postgres:
      command: "npx"
      args: ["-y", "@modelcontextprotocol/server-postgres",
             "postgresql://user:pass@localhost/mydb"]

    brave-search:
      command: "npx"
      args: ["-y", "@modelcontextprotocol/server-brave-search"]
      env:
        BRAVE_API_KEY: "BSA_xxx"
      enabled_tools:
        - "brave_web_search"
```

### Häufige Drittanbieter-Server

```yaml
tools:
  mcp_servers:
    playwright:
      command: "npx"
      args: ["-y", "@playwright/mcp"]
      tool_timeout: 60

    puppeteer:
      command: "npx"
      args: ["-y", "@modelcontextprotocol/server-puppeteer"]
      tool_timeout: 60

    memory:
      command: "npx"
      args: ["-y", "@modelcontextprotocol/server-memory"]
```

### Gemischte Konfiguration

Local und Remote kombiniert:

```yaml
tools:
  restrict_to_workspace: false
  mcp_servers:
    local-fs:
      command: "npx"
      args: ["-y", "@modelcontextprotocol/server-filesystem", "/workspace"]
      tool_timeout: 15

    ai-search:
      url: "https://search.example.com/mcp"
      headers:
        Authorization: "Bearer sk-xxx"
      tool_timeout: 30
      enabled_tools:
        - "semantic_search"
        - "summarize_results"

    internal-api:
      type: streamableHttp
      url: "http://internal.corp.com:8080/mcp"
      headers:
        X-Internal-Token: "corp-token"
      tool_timeout: 20
```

---

## Fehlersuche

### Serververbindung schlägt fehl

**Symptom**: Log zeigt `MCP server 'xxx': failed to connect`

| Ursache | Lösung |
|--------|--------|
| `npx` oder `uvx` fehlt | Installiere Node.js oder uv |
| MCP-Paketname falsch | Überprüfe den Paketnamen und teste den Befehl manuell |
| API-Key fehlt | Setze den Schlüssel unter `env` |
| URL nicht erreichbar | Stelle sicher, dass der Remote-Server läuft |

Teste stdio-Server manuell:

```bash
npx -y @modelcontextprotocol/server-filesystem /tmp
```

### Werkzeugname nicht gefunden

**Symptom**: Logausgabe `enabledTools entries not found: xxx`

Die Namen in `enabled_tools` stimmen nicht mit den tatsächlich registrierten Tools überein. Nanobot zeigt die verfügbaren Namen an. Du kannst entweder den MCP-Originalnamen (z. B. `read_file`) oder die Nanobot-Variante (z. B. `mcp_filesystem_read_file`) verwenden.

### Toolaufruf überschreitet Timeout

**Symptom**: `MCP tool call timed out after Xs`

Erhöhe `tool_timeout`:

```yaml
tool_timeout: 120
```

### SSE-Verbindung bricht ab

Für lang laufende SSE-Verbindungen prüfe:

- Hat der Remote-Server ein Keep-Alive?
- Blockieren Proxy/Firewall lange Verbindungen?
- Hilft der Wechsel zu `streamableHttp`?

### MCP-Logs einsehen

Beim Start schreibt Nanobot die MCP-Informationen ins Log:

```
INFO  MCP server 'filesystem': connected, 8 tools registered
DEBUG MCP: registered tool 'mcp_filesystem_read_file' from server 'filesystem'
WARN  MCP server 'github': enabledTools entries not found: get_repo. Available: get_repository, ...
```

---

## Sicherheitshinweise

- MCP-Server führen Aktionen im Namen des Agents aus. Nutze nur vertrauenswürdige Quellen.
- Stdio-Server besitzen dieselben Rechte wie Nanobot auf dem Hostsystem.
- HTTP/SSE-Header enthalten möglicherweise API-Schlüssel. Verwende besser Umgebungsvariablen als Klartext in `config.yaml`.
- Nanobots SSRF-Schutz (für `web_fetch`) gilt nicht für MCP-Tools. Stelle sicher, dass deine MCP-Server sichere Netzwerkzugriffe haben.
