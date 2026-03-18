# Konfigurationsübersicht

Nanobot verwaltet sein Verhalten vollständig über eine einzige JSON-Konfigurationsdatei, die Modelle, Kommunikation, Tools und Gateway-Einstellungen enthält.

---

## Speicherort der Konfiguration

Standardmäßig liegt die Datei unter:

```
~/.nanobot/config.json
```

`nanobot onboard` legt diese Datei automatisch an.

### Benutzerdefinierte Pfade

Mit `-c` bzw. `--config` kannst du einen beliebigen Pfad angeben:

```bash
nanobot gateway --config ~/.nanobot-work/config.json
nanobot agent -c ~/.nanobot-personal/config.json -m "Hallo!"
```

> [!TIP]
> Für Multi-Instance-Deployments hat jede Instanz eine eigene Konfigurationsdatei. Siehe [Multi-Instance Guide](./multi-instance.md).

---

## Dateiformat

Die Datei ist validiertes JSON. Du kannst `camelCase` und `snake_case` mischen:

```json
{
  "agents": {
    "defaults": {
      "model": "anthropic/claude-opus-4-5",
      "maxTokens": 8192,
      "max_tool_iterations": 40
    }
  }
}
```

> [!NOTE]
> Standard-JSON erlaubt keine Kommentare (`//`). Beispiele enthalten gelegentlich Hinweise, aber die tatsächliche Konfiguration darf keine Kommentare enthalten.

---

## Pydantic-Validierung

Nanobot verwendet [Pydantic](https://docs.pydantic.dev/), um das JSON zu parsen und zu validieren. Falsche Werte führen beim Start zu einem sofortigen Fehler mit klarer Fehlermeldung.

---

## Unterstützung für Umgebungsvariablen

Alle Optionen lassen sich per Umgebungsvariable überschreiben. Präfix: `NANOBOT_`; verschachtelte Schlüssel mit doppelten Unterstrichen `__`:

| Variable | Zielpfad |
|----------|----------|
| `NANOBOT_AGENTS__DEFAULTS__MODEL` | `agents.defaults.model` |
| `NANOBOT_PROVIDERS__ANTHROPIC__API_KEY` | `providers.anthropic.api_key` |
| `NANOBOT_GATEWAY__PORT` | `gateway.port` |
| `NANOBOT_TOOLS__EXEC__TIMEOUT` | `tools.exec.timeout` |

Umgebungsvariablen haben Vorrang vor Einträgen in der Datei und eignen sich für Docker/CI/CD.

```bash
export NANOBOT_PROVIDERS__ANTHROPIC__API_KEY="sk-ant-..."
nanobot gateway
```

---

## Überblick über oberste Schlüssel

| Schlüssel | Typ | Beschreibung |
|----------|-----|--------------|
| [`agents`](./reference.md#agents) | Objekt | Vorgaben für Agenten (Modell, Workspace, Token-Limits) |
| [`channels`](./reference.md#channels) | Objekt | Einstellungen für Chat-Kanäle (Slack, Discord, Telegram usw.) |
| [`providers`](./reference.md#providers) | Objekt | LLM-Anbieter mit API-Keys und Endpunkten |
| [`gateway`](./reference.md#gateway) | Objekt | HTTP-Gateway (Host, Port, Heartbeat) |
| [`tools`](./reference.md#tools) | Objekt | Tools (Websuche, Shell, MCP) |

---

## Minimalkonfiguration

Minimaler Telegram- und Anthropic-Aufbau:

```json
{
  "providers": {
    "anthropic": {
      "apiKey": "sk-ant-..."
    }
  },
  "channels": {
    "telegram": {
      "enabled": true,
      "token": "YOUR_BOT_TOKEN",
      "allowFrom": ["YOUR_USER_ID"]
    }
  }
}
```

Nicht erwähnte Optionen nutzen ihre Standardwerte.

---

## Weiterführende Links

- [Vollständige Konfigurationsreferenz](./reference.md)
- [Multi-Instance Guide](./multi-instance.md)
- [CLI-Referenz](../cli-reference.md)
