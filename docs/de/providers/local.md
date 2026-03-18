# Lokale / Self-Hosted-Modelle

nanobot unterstützt lokale oder private LLM-Deployments. Diese Seite behandelt Ollama, vLLM und benutzerdefinierte OpenAI-kompatible Endpunkte.

---

## Ollama

Ollama ist die einfachste lokale Lösung mit vielen vorgefertigten Modellen (Llama, Qwen, Mistral, Gemma).

nanobot erkennt Ollama automatisch, wenn ein Dienst auf `localhost:11434` läuft.

### Installation

**macOS / Linux:**

```bash
curl -fsSL https://ollama.com/install.sh | sh
```

**Windows:**

Lade das Installationsprogramm von [ollama.com](https://ollama.com) herunter.

Nach der Installation läuft der Dienst unter `http://localhost:11434`.

### Modelle herunterladen

```bash
ollama pull llama3.2
ollama pull qwen2.5
ollama pull mistral
ollama pull gemma2
ollama list
```

### nanobot-Konfiguration

**Minimal (Auto-Detection):**

```json
{
  "agents": {
    "defaults": {
      "model": "llama3.2"
    }
  },
  "providers": {
    "ollama": {
      "api_base": "http://localhost:11434"
    }
  }
}
```

**Provider explizit festlegen:**

```json
{
  "agents": {
    "defaults": {
      "model": "qwen2.5:7b",
      "provider": "ollama"
    }
  },
  "providers": {
    "ollama": {
      "api_base": "http://localhost:11434"
    }
  }
}
```

**Andere Hosts / Ports:**

```json
{
  "providers": {
    "ollama": {
      "api_base": "http://192.168.1.100:11434"
    }
  }
}
```

> API-Keys sind bei lokalen Ollama-Instanzen optional.

### Beliebte Modelle

| Modell | Parameter | VRAM |
|--------|-----------|------|
| `llama3.2` | 3B | ~2 GB |
| `llama3.2:1b` | 1B | ~1 GB |
| `llama3.1:8b` | 8B | ~5 GB |
| `llama3.1:70b` | 70B | ~40 GB |
| `qwen2.5:7b` | 7B | ~5 GB |
| `qwen2.5:14b` | 14B | ~9 GB |
| `mistral` | 7B | ~5 GB |
| `gemma2:9b` | 9B | ~6 GB |
| `deepseek-r1:8b` | 8B | ~5 GB |
| `phi4` | 14B | ~9 GB |

> Weitere Modelle findest du in der [Ollama Library](https://ollama.com/library).

### Erkennungskriterien

1. `api_base` enthält `11434`
2. Modellname enthält `ollama` oder `nemotron`
3. `provider: "ollama"` explizit gesetzt

LiteLLM-Prefix ist `ollama_chat/`, nanobot regelt das automatisch.

---

## vLLM

vLLM ist ein leistungsfähiger OpenAI-kompatibler Server für GPU-Cluster und große Modelle.

### Einsatzszenarien

- NVIDIA GPU (A100, H100, RTX 4090)
- Hohe Durchsatzanforderungen
- 70B+ Modelle
- Präzise Quantisierung (AWQ, GPTQ)

### Startbefehle

```bash
pip install vllm
python -m vllm.entrypoints.openai.api_server \
  --model meta-llama/Llama-3.1-8B-Instruct \
  --port 8000
```

Für quantisierte Modelle:

```bash
python -m vllm.entrypoints.openai.api_server \
  --model Qwen/Qwen2.5-72B-Instruct-AWQ \
  --quantization awq \
  --port 8000
```

### nanobot-Setup

```json
{
  "agents": {
    "defaults": {
      "model": "meta-llama/Llama-3.1-8B-Instruct",
      "provider": "vllm"
    }
  },
  "providers": {
    "vllm": {
      "api_key": "EMPTY",
      "api_base": "http://localhost:8000/v1"
    }
  }
}
```

**Remote-Server:**

```json
{
  "providers": {
    "vllm": {
      "api_key": "your-vllm-api-key",
      "api_base": "http://gpu-server.internal:8000/v1"
    }
  }
}
```

> API-Keys sind optional. Wenn nicht gesetzt, verwende einen beliebigen String wie `"EMPTY"`.

### Modellnamen

Verwende genau den Namen, den du beim Start übergibst.

> nanobot erkennt vLLM automatisch über den Provider-Namen und verwendet das LiteLLM-Präfix `hosted_vllm/`.

---

## Custom (OpenAI-kompatibel)

Ideal für alle OpenAI-kompatiblen Endpunkte (LM Studio, LocalAI, private Services).

### Wann nutzen?

- Kein passender built-in Provider
- Du möchtest direkte HTTP-Endpunkte spezifizieren
- Individuelle Authentifizierung nötig

> `custom` nutzt `is_direct=True` und ruft die API direkt auf. LiteLLM-Features wie Fallback oder Autoretry entfallen.

### Beispiele

**LM Studio:**

```json
{
  "agents": {
    "defaults": {
      "model": "lmstudio-community/Meta-Llama-3.1-8B-Instruct-GGUF",
      "provider": "custom"
    }
  },
  "providers": {
    "custom": {
      "api_key": "lm-studio",
      "api_base": "http://localhost:1234/v1"
    }
  }
}
```

**LocalAI:**

```json
{
  "providers": {
    "custom": {
      "api_key": "any-key",
      "api_base": "http://localhost:8080/v1"
    }
  }
}
```

**Private Enterprise:**

```json
{
  "providers": {
    "custom": {
      "api_key": "internal-service-key",
      "api_base": "https://llm.internal.company.com/v1",
      "extra_headers": {
        "X-Team-ID": "engineering",
        "X-Service-Version": "v2"
      }
    }
  }
}
```

---

## Empfehlungen

| Hardware | Empfehlung | Modelle |
|---------|------------|---------|
| MacBook Air (8 GB) | Ollama | `llama3.2`, `qwen2.5:3b` |
| MacBook Pro M3 (16 GB) | Ollama | `llama3.1:8b`, `qwen2.5:7b` |
| MacBook Pro M3 Max (32 GB) | Ollama | `llama3.1:70b` (quantisiert), `qwen2.5:14b` |
| RTX 4090 | Ollama/vLLM | `llama3.1:70b` (Q4), `qwen2.5:72b` (AWQ) |
| A100 | vLLM | 70B+ Modelle |
| Multi-GPU | vLLM | 100B+ Modelle |

---

## FAQ

**Kann ich Ollama und vLLM parallel nutzen?**
Ja. Verwende unterschiedliche `api_base`-URLs und setze bei Bedarf `provider`.

**Wie schnell sind lokale Modelle?**
Auf RTX 4090 liefern 7B-Modelle ~40–80 Token/s, 70B-Modelle ~10–20 Token/s.

**Wie verhindere ich das Entladen von Ollama-Modellen?**
Setze `OLLAMA_KEEP_ALIVE=-1`, damit Modelle dauerhaft geladen bleiben.

**Kann vLLM gehypte Modelle (z. B. Llama 3) laden?**
Ja. Nutze `huggingface-cli login` vor dem Start.

---

## Weiterführende Links

- Anbieterübersicht: [providers/index.md](./index.md)
- Weitere Cloud-Provider: [providers/others.md](./others.md)
- Dokumentationen: Ollama (ollama.com), vLLM (docs.vllm.ai), LM Studio (lmstudio.ai)
