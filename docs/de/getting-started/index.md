# Einstieg

Willkommen bei **nanobot** — einem ultraleichten Framework für persönliche KI‑Assistenten mit Unterstützung für 16+ Chat‑Plattformen, mehrere LLM‑Provider und MCP‑Integration.

In diesem Abschnitt führen wir Sie in wenigen Minuten von der Installation bis zur ersten Unterhaltung mit Ihrem KI‑Assistenten.

---

## Inhalt dieses Abschnitts

<div class="grid cards" markdown>

-   :material-download-box:{ .lg .middle } **Installation**

    ---

    Systemanforderungen, Installationswege (pip / uv / Quellcode / Docker) sowie häufige Fehlerbehebung.

    [:octicons-arrow-right-24: Installationsanleitung](installation.md)

-   :material-rocket-launch:{ .lg .middle } **Schnellstart**

    ---

    Einrichtung in 5 Minuten und Start von nanobot in Telegram oder der CLI.

    [:octicons-arrow-right-24: Schnellstart](quick-start.md)

-   :material-wizard-hat:{ .lg .middle } **Onboarding‑Assistent**

    ---

    Detaillierte Erklärung aller Schritte von `nanobot onboard` und wie Sie Workspace‑Vorlagen anpassen.

    [:octicons-arrow-right-24: Onboarding‑Assistent](onboarding.md)

</div>

---

## Lernpfad

```
nanobot installieren
    ↓
nanobot onboard ausführen (Konfiguration und Workspace initialisieren)
    ↓
~/.nanobot/config.json bearbeiten (API-Schlüssel und Modell konfigurieren)
    ↓
nanobot agent (Unterhaltung in der CLI)
    ↓
Chat-Kanäle verbinden (Telegram / Discord / Slack usw.)
    ↓
nanobot gateway (Gateway starten und Echtzeitnachrichten empfangen)
```

## Voraussetzungen

Bitte stellen Sie vor dem Start sicher, dass Folgendes bereitsteht:

| Voraussetzung | Beschreibung |
|------|------|
| **Python 3.11+** | nanobot benötigt Python 3.11 oder neuer |
| **uv** (empfohlen) oder **pip** | Python-Paketverwaltung |
| **LLM API-Schlüssel** | z. B. OpenRouter, Anthropic, OpenAI |
| **(Optional) Bot-Token der Chat-Plattform** | z. B. Telegram Bot Token, wenn Sie Chat-Plattformen verbinden möchten |

!!! tip "Empfehlung für Einsteiger"
    Wenn Sie nicht wissen, wo Sie einen API-Schlüssel bekommen, empfehlen wir [OpenRouter](https://openrouter.ai/keys). Dort sind viele wichtige Modelle verfügbar und es gibt ein kostenloses Kontingent.

## Häufigste Fragen

**F: Welche LLMs unterstützt nanobot?**

Es werden 20+ LLM‑Provider unterstützt, darunter OpenAI, Anthropic Claude, Google Gemini, DeepSeek, Qwen und lokales Ollama. Details: [Provider-Dokumentation](../providers/index.md).

**F: Brauche ich eine öffentliche IP?**

Nein. Die meisten Kanäle (Telegram, Discord, Feishu, DingTalk, Slack) verwenden WebSocket‑Langverbindungen oder Socket Mode und benötigen keine öffentliche IP.

**F: Wie viele Ressourcen verbraucht nanobot?**

Sehr wenig. Der Kern umfasst nur etwa 16.000 Zeilen Python‑Code, startet schnell und benötigt wenig Speicher.