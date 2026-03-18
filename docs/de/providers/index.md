# LLM-Anbieterübersicht

Dieser Artikel erklärt das Provider-System von nanobot: was ein Anbieter ist, wie die automatische Erkennung funktioniert und wie du den passenden Service auswählst.

---

## Was ist ein Anbieter?

**Anbieter (Provider)** sind die Brücke zwischen nanobot und externen LLM-Diensten. Jeder Provider kapselt folgende Informationen:

- API-Schlüssel und Endpunkt-URL
- LiteLLM-Routing-Präfix (z. B. `deepseek/deepseek-chat`)
- Schlüsselwörter für die automatische Erkennung des Modells
- Ob es sich um ein Gateway oder eine lokale Installation handelt
- Spezielle Parameter-Override (z. B. Kimi verlangt `temperature >= 1.0`)

Alle Provider werden zentral in `nanobot/providers/registry.py` definiert und bilden die Single Source of Truth.

---

## Automatische Erkennung

nanobot greift auf drei Ebenen zurück, um zu bestimmen, welcher Provider benutzt werden soll:

### 1. API-Schlüssel-Präfix

Einige Anbieter liefern Schlüssel mit eindeutigen Präfixen, die automatisch zugeordnet werden:

| Präfix | Provider |
|-------|----------|
| `sk-or-v1-...` | OpenRouter |

### 2. API-Base-URL Schlüsselwörter

Wenn du ein eigenes `api_base` setzt, gleicht nanobot die URL nach Schlüsselwörtern ab:

| Schlüsselwort im URL | Provider |
|---------------------|----------|
| `openrouter` | OpenRouter |
| `aihubmix` | AiHubMix |
| `siliconflow` | SiliconFlow (硅基流動) |
| `volces` | VolcEngine (火山引擎) |
| `bytepluses` | BytePlus |
| `11434` | Ollama (lokal) |

### 3. Schlüsselwörter im Modellnamen

Wenn die ersten beiden Methoden nichts liefern, analysiert nanobot den Modellnamen:

| Modellname enthält | Provider |
|-------------------|----------|
| `anthropic`, `claude` | Anthropic |
| `openai`, `gpt` | OpenAI |
| `deepseek` | DeepSeek |
| `gemini` | Google Gemini |
| `zhipu`, `glm`, `zai` | 智譜 AI |
| `qwen`, `dashscope` | DashScope (阿里雲) |
| `moonshot`, `kimi` | Moonshot |
| `minimax` | MiniMax |
| `mistral` | Mistral |
| `groq` | Groq |
| `ollama`, `nemotron` | Ollama |
| `vllm` | vLLM / lokal |

> **Hinweis:** Gateways und lokale Provider nehmen nicht an der Modellnamen-Erkennung teil. Sie werden ausschließlich über API-Schlüssel-Präfixe oder URL-Schlüsselwörter identifiziert.

---

## Unterstützte Provider

nanobot bietet mehr als 28 Provider und unterteilt sie in die folgenden Kategorien:

### Gateway-Typen — liefern Zugriff auf beliebige Modelle

Gateways bündeln viele Modelle hinter einem Schlüssel und bieten flexible Abrechnung sowie Redundanz.

| Provider | Beschreibung | Empfehlung |
|----------|-------------|------------|
| **OpenRouter** | Größtes Modell-Gateway mit 300+ Modellen | ⭐⭐⭐⭐⭐ Erste Wahl |
| **AiHubMix** | OpenAI-kompatible API mit vielen Modellen | ⭐⭐⭐⭐ |
| **SiliconFlow（硅基流動）** | Kostenloses Kontingent mit open-source Modellen | ⭐⭐⭐⭐ |
| **VolcEngine（火山引擎）** | ByteDance Cloud, Pay-per-use | ⭐⭐⭐ |
| **VolcEngine Coding Plan** | Spezieller Plan für Code-Modelle | ⭐⭐⭐ |
| **BytePlus** | Internationale Variante von VolcEngine | ⭐⭐⭐ |
| **BytePlus Coding Plan** | Code-spezifischer Plan von BytePlus | ⭐⭐⭐ |

### Standard-Cloud-Anbieter

Direkter Zugriff auf die offiziellen APIs der Hersteller:

| Provider | Hauptmodelle | Region |
|----------|--------------|--------|
| **Anthropic** | Claude Opus/Sonnet/Haiku | Weltweit |
| **OpenAI** | GPT-4o, GPT-4 Turbo, o1/o3 | Weltweit |
| **DeepSeek** | DeepSeek-V3, DeepSeek-R1 | Global/China |
| **Google Gemini** | Gemini 2.0 Flash/Pro | Weltweit |
| **智譜 AI（Zhipu）** | GLM-4, GLM-Z1 | China |
| **DashScope（阿里雲）** | Qwen-Serie | China/Global |
| **Moonshot（Kimi）** | Kimi K2.5, moonshot-v1 | China/Global |
| **MiniMax** | MiniMax-M2.1 | China |
| **Mistral** | Mistral Large, Codestral | Weltweit (Europa) |
| **Groq** | Llama, Mixtral + Whisper | Weltweit |

### OAuth-Authentifizierung (ohne API-Schlüssel)

| Provider | Authentifizierung | Voraussetzungen |
|----------|-------------------|-----------------|
| **OpenAI Codex** | OAuth | ChatGPT Plus/Pro Abo |
| **GitHub Copilot** | OAuth | GitHub Copilot Abo |

### Direkte Endpunkte

| Provider | Beschreibung |
|----------|--------------|
| **Azure OpenAI** | Direkter Zugriff auf Azure-Deployments ohne LiteLLM |
| **Custom** | Jeder OpenAI-kompatible Endpunkt |

### Lokale Installationen

| Provider | Beschreibung |
|----------|-------------|
| **Ollama** | Automatische Erkennung auf `localhost:11434` |
| **vLLM** | Beliebiger OpenAI-kompatibler lokaler Server |

---

## Auswahlhilfe

### Schneller Einstieg

Nutze **OpenRouter**. Ein Schlüssel reicht für fast alle Modelle, du musst nicht mehrere Konten verwalten. Siehe die [OpenRouter-Einrichtungsanleitung](./openrouter.md).

### Claude verwenden

Nutze die **Anthropic**-API. Sie unterstützt Prompt Caching und bietet Einstellungen für Thinking. Siehe die [Anthropic-Anleitung](./anthropic.md).

### GPT-Familie

Nutze **OpenAI** direkt oder den OAuth-Fluss von OpenAI Codex (ChatGPT Plus/Pro erforderlich). Siehe die [OpenAI-Anleitung](./openai.md).

### In China ansässig

Empfohlen:
- **SiliconFlow（硅基流動）** — kostenloses Kontingent, unterstützt Qwen & DeepSeek
- **DashScope** — Alibaba-offiziell mit stabiler Qwen-Serie
- **Moonshot** — Kimi K2.5 über `api.moonshot.cn`
- **智譜 AI** — GLM-Serienmodelle

Siehe auch [Weitere Cloud-Provider](./others.md).

### Lokale Modelle

Nutze **Ollama** oder **vLLM**, wenn du Daten lokal behalten möchtest. Siehe [Lokale / Self-Hosted Modelle](./local.md).

### Du hast GitHub Copilot oder ChatGPT Plus?

Verwende OAuth, du brauchst keine zusätzlichen API-Guthaben. Details in der [OpenAI-Anleitung](./openai.md).

---

## Provider-Konfiguration

Alle Provider stehen unter dem `providers`-Knoten und folgen dem gleichen Aufbau:

```json
{
  "providers": {
    "<provider_name>": {
      "api_key": "your-api-key",
      "api_base": "https://custom-endpoint.example.com/v1",
      "extra_headers": {
        "X-Custom-Header": "value"
      }
    }
  }
}
```

| Feld | Pflicht | Beschreibung |
|------|--------|--------------|
| `api_key` | ja (außer bei OAuth) | API-Schlüssel des Dienstes |
| `api_base` | nein | Überschreibt die Standard-URL |
| `extra_headers` | nein | Zusätzliche HTTP-Header |

---

## Provider-Routing und Hochverfügbarkeit

### Mehrere Provider parallel

Trage in `providers` mehrere Services ein. nanobot wählt automatisch den passenden Provider basierend auf dem Modellnamen.

```json
{
  "agents": {
    "defaults": {
      "model": "claude-opus-4-5"
    }
  },
  "providers": {
    "anthropic": {
      "api_key": "sk-ant-..."
    },
    "openai": {
      "api_key": "sk-..."
    },
    "deepseek": {
      "api_key": "sk-..."
    }
  }
}
```

In diesem Beispiel enthält der Modellname `claude`, also wählt nanobot `anthropic`.

### Provider erzwingen

Um einen bestimmten Provider unabhängig vom Modell zu nutzen, setze `agents.defaults.provider`:

```json
{
  "agents": {
    "defaults": {
      "model": "claude-opus-4-5",
      "provider": "openrouter"
    }
  },
  "providers": {
    "openrouter": {
      "api_key": "sk-or-v1-..."
    }
  }
}
```

### Priorität von Gateways

Gateway-Provider (OpenRouter, AiHubMix usw.) stehen in `registry.py` ganz oben. Sind sie konfiguriert und der Schlüssel gültig, nutzt nanobot sie zuerst. Standard-Provider (Anthropic, OpenAI usw.) folgen und werden über Modellnamen-Schlüsselwörter gewählt.

---

## Weiterführende Links

- [OpenRouter (empfohlen)](./openrouter.md)
- [Anthropic / Claude Modelle](./anthropic.md)
- [OpenAI / GPT Modelle](./openai.md)
- [Weitere Cloud-Provider](./others.md)
- [Lokale / Self-Hosted Modelle](./local.md)
