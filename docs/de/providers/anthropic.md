# Anthropic (Claude-Modelle)

Anthropic ist der Hersteller der Claude-Modelle und bietet eine direkte API mit niedrigeren Latenzen, stabilerem Prompt Caching und erweiterten Features wie Thinking im Vergleich zu OpenRouter.

---

## API-Schlüssel erhalten

1. Öffne die [Anthropic Console](https://console.anthropic.com)
2. Registriere dich per Google oder E-Mail
3. Gehe zu **API Keys**
4. Klicke auf **Create Key**, gib einen Namen ein und bestätige
5. Kopiere den Schlüssel (`sk-ant-api03-xxxxxxxx...`)

> Anthropic arbeitet mit Guthaben. Neue Accounts erhalten ein kostenloses Kontingent, für weitere Nutzung ist eine Aufladung oder Subscription nötig.

---

## Verfügbare Modelle

### Claude Opus – maximale Reasoning-Performance

| Modell | Merkmal |
|--------|---------|
| `claude-opus-4-5` | Neueste Opus-Version mit Thinking-Unterstützung |

Ideal für komplexe Analysen, Architekturfragen und lange Texte.

### Claude Sonnet – Performance-Kostensbalance

| Modell | Merkmal |
|--------|---------|
| `claude-sonnet-4-5` | Aktuelles Sonnet-Modell mit starkem Preis-Leistungs-Verhältnis |
| `claude-sonnet-3-7` | Unterstützt Extended Thinking |
| `claude-sonnet-3-5` | Bewährt und stabil |

Perfekt für Alltagstasks, Codegenerierung und Q&A.

### Claude Haiku – Geschwindigkeit zuerst

| Modell | Merkmal |
|--------|---------|
| `claude-haiku-3-5` | Schnellstes Modell mit niedrigsten Kosten |

Empfohlen für Echtzeit-Antworten und Batch-Tasks.

---

## Konfigurationsbeispiele

### Basis-Setup

```json
{
  "agents": {
    "defaults": {
      "model": "claude-opus-4-5"
    }
  },
  "providers": {
    "anthropic": {
      "api_key": "sk-ant-api03-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
    }
  }
}
```

### Prompt Caching aktivieren

Anthropic unterstützt `cache_control`. Prompt Caching wirkt automatisch für System-Prompts und Tool-Definitionen. Du kannst es explizit eintragen:

```json
{
  "agents": {
    "defaults": {
      "model": "claude-opus-4-5",
      "prompt_caching": true
    }
  },
  "providers": {
    "anthropic": {
      "api_key": "sk-ant-api03-..."
    }
  }
}
```

Prompt Caching spart bei langen System-Prompts (>1024 Token) Kosten und reduziert den Input um 50–90 % bei Cache Hits.

> Hinweis: Prompt Caching funktioniert nur bei direkter Anthropic-Verbindung oder OpenRouter. Andere Gateways unterstützen `cache_control` möglicherweise nicht.

### Thinking-Modus konfigurieren

Claude Opus und einige Sonnet-Versionen unterstützen Extended Thinking, um anspruchsvolle Reasoning-Aufgaben zu verbessern:

```json
{
  "agents": {
    "defaults": {
      "model": "claude-opus-4-5",
      "thinking": {
        "type": "enabled",
        "budget_tokens": 10000
      }
    }
  },
  "providers": {
    "anthropic": {
      "api_key": "sk-ant-api03-..."
    }
  }
}
```

| Parameter | Bedeutung |
|-----------|-----------|
| `type` | `"enabled"` aktiviert Thinking, `"disabled"` deaktiviert |
| `budget_tokens` | Token-Limit für den Thinking-Prozess (empfohlen: 1000–32000) |

> Hinweis: Bei Thinking muss `temperature` auf 1 gesetzt sein. nanobot übernimmt dies automatisch.

### Beispiel für eine vollständige Konfiguration

```json
{
  "agents": {
    "defaults": {
      "model": "claude-sonnet-4-5",
      "max_tokens": 8192,
      "temperature": 0.7
    }
  },
  "providers": {
    "anthropic": {
      "api_key": "sk-ant-api03-..."
    }
  }
}
```

---

## Modellerkennung

nanobot erkennt Anthropic automatisch, wenn deine Modellbezeichnung `anthropic` oder `claude` enthält.

---

## Prompt Caching erklärt

Anthropic cached wiederkehrende Inhalte (System-Prompts, Tool-Definitionen, lange Memory-Zusammenfassungen) und senkt die Kosten um bis zu 90 %, sofern ein Cache-Hit erfolgt.

nanobot nutzt Prompt Caching für stabile System-Prompts, MCP-Toollisten und Memory-Consolidations.

---

## FAQ

**Kann ich Anthropic und OpenRouter gleichzeitig konfigurieren?**
Ja. nanobot wählt automatisch Anthropic, wenn das Modell `anthropic` bzw. `claude` enthält.

**Ist Anthropic in China verfügbar?**
Die direkte API (`api.anthropic.com`) benötigt in China typischerweise ein VPN. In solchen Fällen empfiehlt sich OpenRouter oder SiliconFlow.

**Wo sehe ich meinen API-Verbrauch?**
In der Anthropic Console unter **Usage**.

---

## Weiterführende Links

- Anbieterübersicht: [providers/index.md](./index.md)
- OpenRouter als Alternative: [providers/openrouter.md](./openrouter.md)
- Anthropic API-Referenz auf der offiziellen Website
