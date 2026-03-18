# Vollständige Konfigurationsreferenz

Diese Seite dokumentiert jede Option in `~/.nanobot/config.json`, inklusive Typ, Default und Bedeutung.

> [!NOTE]
> Schlüssel unterstützen sowohl camelCase (`maxTokens`) als auch snake_case (`max_tokens`). Beide Schreibweisen dürfen gemischt werden.

---

## agents

Root für das Agentenverhalten. Aktuell existiert nur `defaults`.

### agents.defaults

| Option | Typ | Default | Bedeutung |
|--------|-----|---------|------------|
| `workspace` | string | `~/.nanobot/workspace` | Arbeitsverzeichnis für Konfiguration, Logs, Memory |
| `model` | string | `anthropic/claude-opus-4-5` | Modell im Format `provider/model-name` |
| `provider` | string | `"auto"` | Erzwingt einen Provider; `"auto"` nutzt Modellname zur Erkennung |
| `max_tokens` | integer | `8192` | Maximale Token-Ausgabe je Anfrage |
| `context_window_tokens` | integer | `65536` | Kontextfenstergröße; überschreitet ein Dialog diese Größe, wird Memory konsolidiert |
| `temperature` | float | `0.1` | Sampling-Temperatur (0 = deterministisch, 1 = zufälliger) |
| `max_tool_iterations` | integer | `40` | Maximale Anzahl Tool-Aufrufe pro Request (schützt vor Schleifen) |
| `reasoning_effort` | string 
| null | `null` | Denkmodus (`"low"`, `"medium"`, `"high"`), `null` deaktiviert |

#### workspace

```json
{
  "agents": {
    "defaults": {
      "workspace": "~/.nanobot/workspace"
    }
  }
}
```

Nanobot nutzt diesen Ordner für Agent-Logs, Shell-Commands, Memory und Sessions. Mit `tools.restrict_to_workspace` werden alle Tools auf diesen Pfad beschränkt.

#### model

```json
{
  "agents": {
    "defaults": {
      "model": "openrouter/anthropic/claude-opus-4-5"
    }
  }
}
```

| Format | Beispiel | Anwendung |
|--------|----------|-----------|
| `provider/model` | `anthropic/claude-opus-4-5` | Standard über LiteLLM |
| `model-only` | `llama3.2` | Lokale Modelle (Ollama) |
| Deployment-Name | `my-gpt4-deployment` | Azure OpenAI |

#### provider

```json
{
  "agents": {
    "defaults": {
      "provider": "ollama"
    }
  }
}
```

`"auto"` (Standard) verwendet Schlüsselwörter im Modellnamen, um den passenden Provider zu wählen. Mit einer festen Provider-ID (z. B. `"anthropic"`, `"openrouter"`) wird das Routing erzwungen.

#### reasoning_effort

```json
{
  "agents": {
    "defaults": {
      "reasoning_effort": "high"
    }
  }
}
```

Aktiviert Extended Thinking bei unterstützten Modellen (z. B. Claude Sonnet 3.7). `null` oder Weglassen deaktiviert den Modus.

---

## channels

Root für Channel-Einstellungen. Pro Plattform existiert ein Unterknoten (z. B. `"telegram"`, `"slack"`).

### Globale Channel-Optionen

| Option | Typ | Default | Bedeutung |
|--------|-----|---------|-----------|
| `send_progress` | bool | `true` | Sende Fortschritts-Streaming an den Channel |
| `send_tool_hints` | bool | `false` | Zeige Tool-Aufruf-Hinweise (z. B. `read_file("…")`) |

```json
{
  "channels": {
    "send_progress": true,
    "send_tool_hints": false,
    "telegram": {
      "enabled": true,
      "token": "YOUR_BOT_TOKEN",
      "allowFrom": ["123456789"]
    }
  }
}
```

### Gemeinsame Felder aller Channels

| Feld | Typ | Default | Bedeutung |
|------|-----|---------|-----------|
| `enabled` | bool | `false` | Kanal aktivieren |
| `allowFrom` | list[string] | `[]` | Whitelist erlaubter IDs (`["*"]` = alle) |

> [!WARNING]
> `allowFrom` ist standardmäßig leer und blockiert alle Nutzer. Trage mindestens einen Eintrag ein.

---

## providers

Root für Provider-Konfigurationen. Jeder Provider ist ein Objekt mit `api_key`, `api_base`, `extra_headers`.

### ProviderConfig-Felder

| Feld | Typ | Default | Bedeutung |
|------|-----|---------|-----------|
| `api_key` | string | `""` | API-Schlüssel |
| `api_base` | string 
| null | `null` | Optionaler API-Endpunkt |
| `extra_headers` | dict 
| null | `null` | Zusätzliche HTTP-Header |

### Unterstützte Provider

| Provider | Beschreibung | Key-Quelle |
|----------|--------------|------------|
| `custom` | Beliebiger OpenAI-kompatibler Endpoint | — |
| `anthropic` | Claude direkt | [console.anthropic.com](https://console.anthropic.com) |
| `openai` | GPT-Modelle direkt | [platform.openai.com](https://platform.openai.com) |
| `openrouter` | Gateway für viele Modelle | [openrouter.ai](https://openrouter.ai) |
| `azure_openai` | Azure OpenAI | [portal.azure.com](https://portal.azure.com) |
| `deepseek` | DeepSeek | [platform.deepseek.com](https://platform.deepseek.com) |
| `gemini` | Google Gemini | [aistudio.google.com](https://aistudio.google.com) |
| `groq` | Groq + Whisper | [console.groq.com](https://console.groq.com) |
| `moonshot` | Moonshot / Kimi | [platform.moonshot.cn](https://platform.moonshot.cn) |
| `minimax` | MiniMax | [platform.minimaxi.com](https://platform.minimaxi.com) |
| `zhipu` | Zhipu GLM | [open.bigmodel.cn](https://open.bigmodel.cn) |
| `dashscope` | Alibaba Qwen | [dashscope.console.aliyun.com](https://dashscope.console.aliyun.com) |
| `siliconflow` | SiliconFlow | [siliconflow.cn](https://siliconflow.cn) |
| `aihubmix` | AiHubMix-Switch | [aihubmix.com](https://aihubmix.com) |
| `volcengine` | VolcEngine (pay-per-use) | [volcengine.com](https://www.volcengine.com) |
| `volcengine_coding_plan` | VolcEngine Coding Plan | — |
| `byteplus` | BytePlus (international) | [byteplus.com](https://www.byteplus.com) |
| `byteplus_coding_plan` | BytePlus Coding Plan | — |
| `mistral` | Mistral AI | [console.mistral.ai](https://console.mistral.ai) |
| `ollama` | Lokale Ollama-Instanz | — |
| `vllm` | Lokaler vLLM / beliebiger OpenAI-kompatibler Server | — |
| `openai_codex` | OAuth (ChatGPT Plus/Pro) | `nanobot provider login openai-codex` |
| `github_copilot` | OAuth (Copilot) | `nanobot provider login github-copilot` |

### Beispiele

**Anthropic direkt:**

```json
{
  "providers": {
    "anthropic": {
      "apiKey": "sk-ant-..."
    }
  }
}
```

**OpenRouter:**

```json
{
  "providers": {
    "openrouter": {
      "apiKey": "sk-or-v1-..."
    }
  },
  "agents": {
    "defaults": {
      "model": "openrouter/anthropic/claude-opus-4-5"
    }
  }
}
```

**Custom:**

```json
{
  "providers": {
    "custom": {
      "apiKey": "your-api-key",
      "apiBase": "https://api.your-provider.com/v1"
    }
  },
  "agents": {
    "defaults": {
      "model": "your-model-name"
    }
  }
}
```

> [!TIP]
> Lokale Dienste ohne Schlüssel können einen beliebigen String wie `"no-key"` verwenden.

**AiHubMix mit Header:**

```json
{
  "providers": {
    "aihubmix": {
      "apiKey": "your-key",
      "extraHeaders": {
        "APP-Code": "your-app-code"
      }
    }
  }
}
```

**Ollama lokal:**

```json
{
  "providers": {
    "ollama": {
      "apiBase": "http://localhost:11434"
    }
  },
  "agents": {
    "defaults": {
      "provider": "ollama",
      "model": "llama3.2"
    }
  }
}
```

**Spezielle `apiBase`-Werte:**

| Provider | Use Case | `apiBase` |
|----------|----------|-----------|
| `zhipu` | Coding Plan | `https://open.bigmodel.cn/api/coding/paas/v4` |
| `minimax` | China | `https://api.minimaxi.com/v1` |
| `dashscope` | Aliyun BaiLian | `https://dashscope.aliyuncs.com/compatible-mode/v1` |

---

## gateway

Konfiguration des HTTP-Gateways.

| Option | Typ | Default | Bedeutung |
|--------|-----|---------|-----------|
| `host` | string | `"0.0.0.0"` | Netzwerkinterface für den Listener |
| `port` | integer | `18790` | TCP-Port |
| `heartbeat.enabled` | bool | `true` | Heartbeat aktivieren |
| `heartbeat.interval_s` | integer | `1800` | Heartbeat-Intervall in Sekunden |

```json
{
  "gateway": {
    "host": "0.0.0.0",
    "port": 18790,
    "heartbeat": {
      "enabled": true,
      "intervalS": 1800
    }
  }
}
```

> [!TIP]
> Starte mehrere Instances mit unterschiedlichen Ports (z. B. `18790`, `18791`, `18792`). Oder überschreibe mit `nanobot gateway --port 18791`.

---

## tools

Root für Tool-Konfigurationen: Web, Shell, Limits und MCP.

### tools.web

Netzwerkeinstellungen.

| Option | Typ | Default | Bedeutung |
|--------|-----|---------|-----------|
| `proxy` | string 
| null | `null` | Optionaler HTTP/SOCKS5-Proxy für alle Web-Anfragen |

```json
{
  "tools": {
    "web": {
      "proxy": "http://127.0.0.1:7890"
    }
  }
}
```

Unterstützte Formate:
- `http://127.0.0.1:7890`
- `socks5://127.0.0.1:1080`

### tools.web.search

Einstellungen für Websuche.

| Option | Typ | Default | Bedeutung |
|--------|-----|---------|-----------|
| `provider` | string | `"brave"` | `"brave"`, `"tavily"`, `"duckduckgo"`, `"searxng"`, `"jina"` |
| `api_key` | string | `""` | API-Key für Brave/Tavily |
| `base_url` | string | `""` | URL für SearXNG |
| `max_results` | integer | `5` | Ergebnisse pro Suche (1–10) |

#### Anbieterübersicht

| Provider | Key nötig | Kostenlos | Env-Variable |
|----------|-----------|----------|--------------|
| `brave` | Ja | Nein | `BRAVE_API_KEY` |
| `tavily` | Ja | Nein | `TAVILY_API_KEY` |
| `jina` | Ja | Kostenlos (10 Mio. Token) | `JINA_API_KEY` |
| `searxng` | Nein (Self-Host) | Ja | `SEARXNG_BASE_URL` |
| `duckduckgo` | Nein | Ja | — |

> Fehlen Keys, fällt nanobot automatisch auf DuckDuckGo zurück.

(Weitere Abschnitte folgen...)