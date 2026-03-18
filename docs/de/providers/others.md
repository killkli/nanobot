# Weitere Cloud-Provider

Dieser Abschnitt beschreibt zusätzliche Cloud-LLM-Anbieter, darunter chinesische Direktzugänge, europäische Modelle und spezialisierte Reasoning-Services.

---

## DeepSeek

DeepSeek liefert hochwertige Open-Source-Modelle (DeepSeek-V3, DeepSeek-R1) mit starkem Fokus auf Code und Reasoning zu deutlich niedrigeren Preisen als GPT-4.

### API-Schlüssel

Fordere einen Schlüssel auf [platform.deepseek.com](https://platform.deepseek.com) unter **API Keys** an.

### Beispielkonfiguration

```json
{
  "agents": {
    "defaults": {
      "model": "deepseek-chat"
    }
  },
  "providers": {
    "deepseek": {
      "api_key": "sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
    }
  }
}
```

### Hauptmodelle

| Modell | Beschreibung |
|--------|--------------|
| `deepseek-chat` | DeepSeek-V3, universelles Flagship |
| `deepseek-reasoner` | DeepSeek-R1, reasoning-fokussiert (ähnlich o1) |

> Modell-Erkennung erfolgt bei Namen mit `deepseek`; LiteLLM-Prefix ist `deepseek/`.

---

## Google Gemini

Gemini überzeugt durch extrem lange Kontexte (100k+ Token) und Multimodalität.

### API-Key

Erstelle einen Schlüssel über [aistudio.google.com](https://aistudio.google.com) → **Get API Key**.

### Beispielkonfiguration

```json
{
  "agents": {
    "defaults": {
      "model": "gemini-2.0-flash"
    }
  },
  "providers": {
    "gemini": {
      "api_key": "AIzaSy-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
    }
  }
}
```

### Hauptmodelle

| Modell | Beschreibung |
|--------|--------------|
| `gemini-2.0-flash` | Schnelle Alltagsantworten |
| `gemini-2.0-flash-thinking-exp` | Experimentelles Reasoning |
| `gemini-2.5-pro-preview` | High-End mit langem Kontext |
| `gemini-1.5-pro` | Stabiler Klassiker mit 1 Mio. Token |

> Erkennung über Modellnamen mit `gemini`; Prefix `gemini/` bei LiteLLM.

---

## Zhipu AI (智谱)

Zhipu AI bietet die GLM-Reihe – beliebt für chinesische Code- und Longform-Tasks.

### API-Key

Beantrage einen Schlüssel auf [open.bigmodel.cn](https://open.bigmodel.cn) unter **API Keys**.

### Konfiguration

```json
{
  "agents": {
    "defaults": {
      "model": "glm-4-plus"
    }
  },
  "providers": {
    "zhipu": {
      "api_key": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx.xxxxxxxxxxxxxxxx"
    }
  }
}
```

### Hauptmodelle

| Modell | Beschreibung |
|--------|--------------|
| `glm-4-plus` | GLM-4 Flagship |
| `glm-4-flash` | Schnelles Modell mit Free-Limit |
| `glm-z1-flash` | Z1 Reasoning v2 |
| `glm-z1-air` | Kompaktes Reasoning-Modell |

> Modellnamen mit `zhipu`, `glm` oder `zai` weisen auf diesen Provider hin; LiteLLM-Prefix `zai/`.

---

## DashScope / Qwen (Alibaba Cloud)

DashScope platziert die Qwen-Serie (通义千问) und ist in China direkt erreichbar.

### API-Key

Hole ihn auf [bailian.aliyun.com](https://bailian.aliyun.com) oder dem DashScope-Portal in der **API-KEY-Verwaltung**.

### Konfiguration

```json
{
  "agents": {
    "defaults": {
      "model": "qwen-max"
    }
  },
  "providers": {
    "dashscope": {
      "api_key": "sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
    }
  }
}
```

### Modelle

| Modell | Beschreibung |
|--------|--------------|
| `qwen-max` | Qwen-Flagship |
| `qwen-plus` | Ausgewogen |
| `qwen-turbo` | Schnelles Modell |
| `qwen3-235b-a22b` | Qwen3 MoE-Flagship |
| `qwen3-30b-a3b` | Leichtere MoE-Variante |
| `qwen-coder-plus` | Code-spezifisch |

> Modelle mit `qwen`/`dashscope` verwenden LiteLLM-Prefix `dashscope/`.

---

## Moonshot / Kimi

Moonshot AI liefert Kimi-Modelle mit 128k+ Kontext und starker chinesischer Sprachverarbeitung.

### API-Key

Beantrage einen Schlüssel auf [platform.moonshot.cn](https://platform.moonshot.cn) unter **API Keys**.

### Beispielkonfiguration

**Internationaler Endpoint:**
```json
{
  "agents": {
    "defaults": {
      "model": "kimi-k2.5"
    }
  },
  "providers": {
    "moonshot": {
      "api_key": "sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
    }
  }
}
```

**China-Endpoint:**
```json
{
  "providers": {
    "moonshot": {
      "api_key": "sk-...",
      "api_base": "https://api.moonshot.cn/v1"
    }
  }
}
```

### Modelle

| Modell | Beschreibung |
|--------|--------------|
| `kimi-k2.5` | Flagship, reasoning-spezifisch (temperature fixiert auf 1.0) |
| `moonshot-v1-8k` | Standard mit 8k Kontext |
| `moonshot-v1-32k` | 32k Kontext |
| `moonshot-v1-128k` | Extrem langer Kontext |

> Hinweis: K2.5 erfordert `temperature >= 1.0`. nanobot setzt dies automatisch per `model_overrides`.

---

## MiniMax

MiniMax bietet das Modell MiniMax-M2.1 über eine OpenAI-kompatible API.

### API-Key

Holen unter [platform.minimaxi.com](https://platform.minimaxi.com) → **API Keys**.

### Konfiguration

```json
{
  "agents": {
    "defaults": {
      "model": "MiniMax-M2.1"
    }
  },
  "providers": {
    "minimax": {
      "api_key": "eyJhbGciOiJSUzI1NiIsInR..."
    }
  }
}
```

### Modelle

| Modell | Beschreibung |
|--------|--------------|
| `MiniMax-M2.1` | Flagship |
| `MiniMax-Text-01` | Allgemeiner Text-Generator |

> Modelle mit `minimax` verwenden LiteLLM-Prefix `minimax/`.

---

## Mistral

Mistral AI bietet europäische Modelle auf EU-Servern – ideal für Datenschutzanforderungen.

### API-Key

Erstelle einen Schlüssel in der [Mistral AI Console](https://console.mistral.ai) unter **API Keys**.

### Beispielkonfiguration

```json
{
  "agents": {
    "defaults": {
      "model": "mistral-large-latest"
    }
  },
  "providers": {
    "mistral": {
      "api_key": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
    }
  }
}
```

### Modelle

| Modell | Beschreibung |
|--------|--------------|
| `mistral-large-latest` | Aktuelles Large-Modell |
| `mistral-small-latest` | Leichtgewicht |
| `codestral-latest` | Code-Modell |
| `pixtral-large-latest` | Multimodal |
| `mistral-nemo` | Open Source (12B) |

> Modelle mit `mistral` nutzen LiteLLM-Prefix `mistral/`.

---

## Groq (+ Whisper)

Groq zeichnet sich durch extrem schnelle Inferenz (LPU) aus und wird auch für Whisper-Transkriptionen verwendet.

### API-Key

Anfordern unter [console.groq.com](https://console.groq.com) (es gibt ein kostenloses Kontingent).

### Konfiguration als LLM

```json
{
  "agents": {
    "defaults": {
      "model": "llama-3.3-70b-versatile"
    }
  },
  "providers": {
    "groq": {
      "api_key": "gsk_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
    }
  }
}
```

### Whisper-Spracherkennung

```json
{
  "providers": {
    "groq": {
      "api_key": "gsk_..."
    }
  },
  "skills": {
    "voice": {
      "stt_provider": "groq",
      "stt_model": "whisper-large-v3-turbo"
    }
  }
}
```

### Modelle

**LLM:**

| Modell | Beschreibung |
|--------|--------------|
| `llama-3.3-70b-versatile` | Meta Llama 3.3 70B |
| `llama-3.1-8b-instant` | 8B, sehr schnell |
| `mixtral-8x7b-32768` | Mixtral MoE |
| `gemma2-9b-it` | Google Gemma 2 9B |

**Whisper:**

| Modell | Beschreibung |
|--------|--------------|
| `whisper-large-v3-turbo` | Schneller, präziser |
| `whisper-large-v3` | Höchste Genauigkeit |

> Groq ist im Registry als optionaler Provider ganz unten platziert. Modelle mit `groq` nutzen LiteLLM-Tag `groq/`.

---

## AiHubMix

AiHubMix ist ein OpenAI-kompatibles Gateway (speziell für China).

### API-Key

Erstelle ihn unter [aihubmix.com](https://aihubmix.com) → **API Keys**.

### Konfiguration

```json
{
  "agents": {
    "defaults": {
      "model": "claude-opus-4-5"
    }
  },
  "providers": {
    "aihubmix": {
      "api_key": "sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
    }
  }
}
```

**Optionaler Header (APP-Code):**

```json
{
  "providers": {
    "aihubmix": {
      "api_key": "sk-...",
      "extra_headers": {
        "APP-Code": "your-app-code"
      }
    }
  }
}
```

> AiHubMix entfernt beim Routing das `anthropic/`-Präfix und ersetzt es durch `openai/`, da es OpenAI-kompatibel ist.

---

## SiliconFlow

SiliconFlow bietet dedizierte Zugangspunkte für Qwen, DeepSeek und Llama mit Gratis-Kontingenten.

### API-Key

Über [siliconflow.cn](https://siliconflow.cn) → **API Keys** erhältlich.

### Konfiguration

```json
{
  "agents": {
    "defaults": {
      "model": "Qwen/Qwen2.5-72B-Instruct"
    }
  },
  "providers": {
    "siliconflow": {
      "api_key": "sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
    }
  }
}
```

### Modelle

| Modell | Beschreibung |
|--------|--------------|
| `Qwen/Qwen2.5-72B-Instruct` | Qwen 2.5 72B |
| `deepseek-ai/DeepSeek-V3` | DeepSeek V3 |
| `deepseek-ai/DeepSeek-R1` | DeepSeek R1 |
| `meta-llama/Meta-Llama-3.1-405B-Instruct` | Meta 3.1 405B |
| `THUDM/glm-4-9b-chat` | Smart GLM |

> Wird automatisch erkannt, wenn `api_base` `siliconflow` enthält. LiteLLM-Prefix `openai/`.

---

## VolcEngine

VolcEngine (ByteDance) bietet die Doubao-Modelle (豆包). Modell `volcengine-plan` eignet sich für Code-Anwendungen.

### API-Key

Unter [console.volcengine.com/ark](https://console.volcengine.com/ark) → **API Key Management** beantragen.

### Beispiel

```json
{
  "agents": {
    "defaults": {
      "model": "doubao-pro-32k"
    }
  },
  "providers": {
    "volcengine": {
      "api_key": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
    }
  }
}
```

**Coding Plan:**

```json
{
  "agents": {
    "defaults": {
      "model": "volcengine-plan/your-endpoint-id",
      "provider": "volcengine_coding_plan"
    }
  },
  "providers": {
    "volcengine_coding_plan": {
      "api_key": "your-volcengine-api-key"
    }
  }
}
```

> Erkennung basiert auf `volcengine`, `volces` oder `ark`. Coding Plan nutzt `https://ark.cn-beijing.volces.com/api/coding/v3`.

---

## BytePlus

BytePlus ist die internationale Version von VolcEngine mit südostasiatischen Endpunkten.

### Beispiel

```json
{
  "agents": {
    "defaults": {
      "model": "byteplus/your-endpoint-id",
      "provider": "byteplus"
    }
  },
  "providers": {
    "byteplus": {
      "api_key": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
    }
  }
}
```

**Coding Plan:**

```json
{
  "providers": {
    "byteplus_coding_plan": {
      "api_key": "your-byteplus-api-key"
    }
  }
}
```

> Modellnamen oder `api_base` mit `bytepluses` leiten automatisch auf diesen Provider um.

---

## Azure OpenAI (direkte API)

nanobot unterstützt Azure OpenAI direkt (API-Version `2024-10-21`, `is_direct=True`).

### Beispiel

```json
{
  "agents": {
    "defaults": {
      "model": "gpt-4o",
      "provider": "azure_openai"
    }
  },
  "providers": {
    "azure_openai": {
      "api_key": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
      "api_base": "https://your-resource.openai.azure.com/openai/deployments/your-deployment"
    }
  }
}
```

> `model` entspricht dem Deployment-Namen, `api_base` der Resource-URL.

---

## Weiterführende Links

- Anbieterübersicht: [providers/index.md](./index.md)
- OpenRouter: [providers/openrouter.md](./openrouter.md)
- Local Provider: [providers/local.md](./local.md)
