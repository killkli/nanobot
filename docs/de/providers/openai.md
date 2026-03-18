# OpenAI (GPT-Modelle)

nanobot unterstützt drei Wege, um OpenAI-Modelle zu nutzen: direkte API-Schlüssel, OpenAI Codex OAuth (ChatGPT Plus/Pro) und GitHub Copilot OAuth.

---

## Methode 1: Direkte OpenAI-API

### API-Schlüssel erhalten

1. Besuche die [OpenAI Platform](https://platform.openai.com)
2. Melde dich an und gehe zu **API Keys**
3. Klicke auf **Create new secret key**
4. Kopiere den Schlüssel (`sk-proj-xxxxxxxx...` oder ältere `sk-xxxxxxxx...`)

> OpenAI arbeitet mit Prepaid-Guthaben. Lade dein Konto über die Billing-Seite auf.

### Verfügbare Modelle

**GPT-4o-Serie**

| Modell | Merkmale |
|--------|----------|
| `gpt-4o` | Multimodales Flaggschiff mit Bilderkennung |
| `gpt-4o-mini` | Kostengünstig und schnell |
| `gpt-4o-audio-preview` | Unterstützt Spracheingabe/-ausgabe |

**o-Serie**

| Modell | Merkmale |
|--------|----------|
| `o3` | Aktuelles Reasoning-Flaggschiff |
| `o3-mini` | Leichtes Reasoning-Modell |
| `o4-mini` | Schnelles Reasoning mit guter Balance |
| `o1` | Erste Generation der o-Modelle |

**GPT-4 Turbo**

| Modell | Merkmale |
|--------|----------|
| `gpt-4-turbo` | Bis zu 128k Kontext, Bildunterstützung |
| `gpt-4` | Klassischer GPT-4 |

> Die vollständige Liste findest du auf der OpenAI-Plattform.

### Konfigurationsbeispiel

```json
{
  "agents": {
    "defaults": {
      "model": "gpt-4o"
    }
  },
  "providers": {
    "openai": {
      "api_key": "sk-proj-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
    }
  }
}
```

### Eigenes `api_base`

```json
{
  "providers": {
    "openai": {
      "api_key": "sk-proj-...",
      "api_base": "https://your-proxy.example.com/v1"
    }
  }
}
```

---

## Methode 2: OpenAI Codex OAuth (ChatGPT Plus/Pro)

Diese Option erlaubt ChatGPT Plus/Pro-Abonnenten, die Modelle per OAuth zu nutzen, ohne neue Credits zu kaufen.

> Wichtiger Hinweis: Behavior und Nutzungsbedingungen folgen dem ChatGPT-Webclient und können von der offiziellen API abweichen.

### Voraussetzungen

- Aktives ChatGPT Plus oder Pro
- Im Browser bei chatgpt.com eingeloggt

### Einrichtung

1. Aktiviere `openai_codex` als Provider (kein `api_key` benötigt):

```json
{
  "agents": {
    "defaults": {
      "model": "openai-codex/auto",
      "provider": "openai_codex"
    }
  },
  "providers": {
    "openai_codex": {}
  }
}
```

2. Starte nanobot, der OAuth wird im Browser ausgeführt.
3. Token werden lokal gespeichert und müssen danach nicht erneut angefragt werden.

### Modellerkennung

nanobot erkennt Codex, wenn `api_base` `codex` enthält oder das Modell `openai-codex` genannt wird.

```json
{
  "providers": {
    "openai_codex": {
      "api_base": "https://chatgpt.com/backend-api"
    }
  }
}
```

> Einschränkung: OAuth-Provider sind keine Fallback-Kandidaten. Du musst `provider: "openai_codex"` definieren oder das Modell mit `openai-codex/` prefixen.

---

## Methode 3: GitHub Copilot OAuth

Erlaubt Copilot-Abonnenten, per OAuth auf Modelle zuzugreifen.

### Voraussetzungen

- GitHub Copilot Individual/Business/Enterprise
- GitHub CLI (`gh`) oder Desktop installiert und eingeloggt

### Beispielkonfiguration

```json
{
  "agents": {
    "defaults": {
      "model": "github_copilot/claude-sonnet-4-5",
      "provider": "github_copilot"
    }
  },
  "providers": {
    "github_copilot": {}
  }
}
```

Modelle laufen unter `github_copilot/{modell}` wie `github_copilot/gpt-4o`.

### OAuth-Ablauf

nanobot öffnet automatisch den Browser für die OAuth-Autorisierung. Das Token wird lokal gecached.

### Modellerkennung

- Modellname enthält `github_copilot` oder `copilot`
- Alternativ `provider: "github_copilot"` angeben

Dank `skip_prefixes` wird `github_copilot/claude-sonnet-4-5` nicht fälschlich als OpenAI Codex behandelt.

---

## Vergleich der drei Wege

| | Direkte API | Codex OAuth | Copilot OAuth |
|--|-------------|-------------|---------------|
| API-Key nötig | Ja | Nein | Nein |
| Subscription | Nein | ChatGPT Plus/Pro | GitHub Copilot |
| Modellvielfalt | Alle OpenAI-Modelle | ChatGPT-Modelle | Copilot-Modelle |
| Kosten | Token-basiert | Im Abo enthalten | Im Abo enthalten |
| Stabilität | Sehr hoch | Abhängig von ChatGPT | Abhängig von GitHub |
| Empfohlen für | Entwickler | ChatGPT-User | Copilot-User |

---

## FAQ

**Was ist der Unterschied zwischen `gpt-4o` und `gpt-4o-mini`?**
`gpt-4o` ist leistungsfähiger, `gpt-4o-mini` deutlich günstiger bei vergleichbarer Alltagstauglichkeit.

**Unterstützen o-Modelle Streaming?**
Ja, nanobot streamt. o-Modelle ignorieren einige Parameter (z. B. `temperature`), nanobot passt sie automatisch an.

**Wie wechsle ich von ChatGPT Plus zur API?**
Die Accounts sind getrennt. Zur API musst du ein Konto auf platform.openai.com registrieren und aufladen. Mit Codex OAuth kannst du aktuelle ChatGPT Plus-Funktionen ohne zusätzliche Kosten nutzen.

---

## Weiterführende Links

- Anbieterübersicht: [providers/index.md](./index.md)
- OpenRouter als Gateway: [providers/openrouter.md](./openrouter.md)
- OpenAI API-Referenz auf der offiziellen Plattform
