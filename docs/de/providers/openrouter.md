# OpenRouter (empfohlener Standard-Provider)

OpenRouter ist der Einstiegsempfehlung von nanobot: Ein API-Schlüssel ermöglicht Zugriff auf über 300 Modelle von Anthropic, OpenAI, Google, Meta, Mistral und weiteren Anbietern.

---

## Was ist OpenRouter?

OpenRouter ist ein LLM-Gateway mit OpenAI-kompatibler API, das Anfragen automatisch an verschiedene Anbieter weiterleitet.

**Darum wird es empfohlen:**

- **Ein Schlüssel für alles** – kein separater Account für Anthropic, OpenAI, Google etc. nötig
- **Pay-per-Use** – Modelle werden einzeln nach Nutzung abgerechnet
- **Kostenlose Modelle** – z. B. Llama- oder Qwen-Varianten mit Gratis-Kontingent
- **Provider-Fallback** – mehrere Anbieter für ein Modell als Reserve definierbar
- **Beste Routing-Option** – Auswahl nach Latenz oder Kosten automatisch
- **Prompt Caching** – nanobot nutzt Caching für OpenRouter

---

## API-Key erstellen

1. Besuche [openrouter.ai](https://openrouter.ai)
2. Klicke auf **Sign In** / **Get Started** und melde dich mit Google oder GitHub an
3. Navigiere zu **Settings → Keys**
4. Klicke auf **Create Key**
5. Kopiere den Schlüssel (`sk-or-v1-xxxxxxxx...`)

> Wichtig: nanobot erkennt OpenRouter automatisch anhand des Präfixes `sk-or-`.

---

## Konfiguration

### Minimal

```json
{
  "agents": {
    "defaults": {
      "model": "anthropic/claude-opus-4-5"
    }
  },
  "providers": {
    "openrouter": {
      "api_key": "sk-or-v1-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
    }
  }
}
```

### Vollständig

```json
{
  "agents": {
    "defaults": {
      "model": "anthropic/claude-opus-4-5",
      "provider": "openrouter"
    }
  },
  "providers": {
    "openrouter": {
      "api_key": "sk-or-v1-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
      "api_base": "https://openrouter.ai/api/v1"
    }
  }
}
```

> Das Feld `api_base` ist optional; mit `sk-or-` wird automatisch `https://openrouter.ai/api/v1` verwendet.

---

## Spezifische Modelle wählen

Modelle folgen dem Muster `{provider}/{modell}`. Beispiel:

```json
{
  "agents": {
    "defaults": {
      "model": "anthropic/claude-opus-4-5"
    }
  }
}
```

### Häufig verwendete Modelle

**Anthropic Claude**

| Modell | Beschreibung |
|--------|--------------|
| `anthropic/claude-opus-4-5` | Maximales Reasoning |
| `anthropic/claude-sonnet-4-5` | Gute Balance |
| `anthropic/claude-haiku-3-5` | Schnelle Antworten |

**OpenAI GPT**

| Modell | Beschreibung |
|--------|--------------|
| `openai/gpt-4o` | Multimodales Flaggschiff |
| `openai/gpt-4o-mini` | Kostengünstiger Allrounder |
| `openai/o3` | Reasoning-Flaggschiff |

**Google Gemini**

| Modell | Beschreibung |
|--------|--------------|
| `google/gemini-2.0-flash-001` | Schnelle Alltagsantworten |
| `google/gemini-2.5-pro-preview` | Langer Kontext |

**Open Source (kostenloser Zugriff)**

| Modell | Beschreibung |
|--------|--------------|
| `meta-llama/llama-3.3-70b-instruct` | Llama 3.3 70B |
| `qwen/qwen-2.5-72b-instruct` | Qwen 2.5 72B |
| `deepseek/deepseek-chat` | DeepSeek V3 |
| `deepseek/deepseek-r1` | DeepSeek R1 |
| `mistralai/mistral-large-2411` | Mistral Large |

> Die vollständige Liste findest du auf der OpenRouter-Website.

---

## Kosten optimieren

### 1. Kostenlose Modelle nutzen

Modelle mit `:free`-Suffix (z. B. `meta-llama/llama-3.3-70b-instruct:free`) nutzen das Gratis-Limit.

### 2. Modell passend zum Task wählen

- **Schnelle Antworten:** `claude-haiku`, `gpt-4o-mini`
- **Codegenerierung:** `claude-sonnet`, `deepseek-chat`
- **Komplexe Reasoning:** `claude-opus`, `o3`

### 3. Prompt Caching verwenden

nanobot nutzt Prompt Caching bei OpenRouter – System-Prompts, Tool-Definitionen und Memory-Zusammenfassungen werden gecached.

### 4. Kostenlimit setzen

In den Billing-Einstellungen kannst du tägliche oder monatliche Limits festlegen.

---

## Rate Limits

| Kontostatus | Limit |
|-------------|-------|
| Kein Guthaben | 50 Anfragen/Tag (Free Models) |
| Guthaben | Modell-spezifische Limits |
| Enterprise | Kontakt zum Vertrieb |

Bei `429`:
1. Checke die Limits für das Modell auf der OpenRouter-Seite
2. Aktiviere Provider Fallback
3. Reduziere parallele Anfragen

---

## FAQ

**Unterstützt OpenRouter Streaming?** Ja, nanobot nutzt standardmäßig Streaming.

**Kann ich Modelle mit Sonderzugang nutzen?** Einige Modelle erfordern zusätzliche Vereinbarungen. Prüfe die Modellseite.

**Sind die Preise dieselben wie bei den Herstellern?** Sie können leicht darüber oder darunter liegen, abhängig vom Modell.

---

## Weiterführende Links

- Anbieterübersicht: [providers/index.md](./index.md)
- Anthropic direkt: [providers/anthropic.md](./anthropic.md)
- OpenAI direkt: [providers/openai.md](./openai.md)
