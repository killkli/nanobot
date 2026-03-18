# Skills-System Anleitung

Skills sind nanobot-Wissensmodule in Markdown, die konkrete Workflows, Befehlsbeispiele und wiederverwendbare Ressourcen kapseln. Der Agent lädt sie anhand ihrer Beschreibung automatisch, ohne dass Nutzer:innen sie manuell triggern müssen.

---

## Was ist ein Skill

Ein Skill ist ein Verzeichnis, das mindestens eine `SKILL.md` enthält. `SKILL.md` besteht aus zwei Bereichen:

- **YAML-Frontmatter**: Beschreibt den Namen, Zweck und die Aktivierungsbedingungen des Skills
- **Markdown-Inhalt**: Lädt konkrete Anweisungen in den Kontext, sobald der Skill aktiv ist

Skills folgen der [OpenClaw-Spezifikation](https://github.com/openclaw/openclaw) und bleiben kompatibel zur OpenClaw-Community.

---

## Skill-Format

```
skill-name/
├── SKILL.md              （erforderlich）
└── （optionale Ressourcen）
    ├── scripts/          - Ausführbare Skripte (Python, Bash usw.)
    ├── references/       - Referenzdokumente (nur bei Bedarf laden)
    └── assets/           - Ausgabedateien (Templates, Bilder usw.)
```

### Aufbau von `SKILL.md`

```markdown
---
name: my-skill
description: >
  Beschreibt, was der Skill kann und wann er geladen werden soll.
  Enthält Trigger-Begriffe und Anwendungsszenarien.
always: false    # true lädt den Skill dauerhaft (z. B. memory)
---

# Skill-Titel

Hier stehen die detaillierten Anweisungen.
```

#### Frontmatter-Felder

| Feld | Erforderlich | Bedeutung |
|------|--------------|-----------|
| `name` | Ja | Skill-Name (kleine Buchstaben, Zahlen, Bindestriche) |
| `description` | Ja | Wann soll der Skill ausgelöst werden / was macht er? |
| `always` | Nein | `true` lädt den Skill dauerhaft |
| `homepage` | Nein | Offizielle Webseite oder Referenz |
| `metadata` | Nein | nanobot-spezifische Einstellungen (Emoji, benötigte Tools, Abhängigkeiten) |

> **Wichtig**: `description` entscheidet darüber, ob der Agent den Skill lädt. Sie muss Trigger, Szenarien und den Nutzen präzise beschreiben.

---

## Skill-Installation

### Eingebaute Skills

nanobot lädt beim Start automatisch alle Skills aus `nanobot/skills/`. Keine zusätzliche Installation nötig.

### Eigene Skills

Lege das Skill-Verzeichnis unter `skills/` im Workspace ab:

```
~/.nanobot/workspace/
└── skills/
    └── my-skill/
        └── SKILL.md
```

Nach einem Neustart sind die neuen Skills verfügbar.

### ClawHub installieren

```bash
npx --yes clawhub@latest install <slug> --workdir ~/.nanobot/workspace
```

Starte danach eine neue Session, um den Skill zu laden.

---

## Eingebaute Skills

### GitHub (`github`)

Steuert Issue-, PR- und CI-Workflows mittels `gh` CLI.

**Voraussetzung**: `gh` CLI installiert und `gh auth login` durchgeführt.

```bash
# CI-Status eines PR prüfen
gh pr checks 55 --repo owner/repo

# Letzte Workflows sehen
gh run list --repo owner/repo --limit 10

# Fehlgeschlagene Jobs loggen
 gh run view <run-id> --repo owner/repo --log-failed

# Issues im JSON-Format
gh issue list --repo owner/repo --json number,title \
  --jq '.[] | "\(.number): \(.title)"'
```

**Trigger**: „PR anzeigen“, „CI fehlgeschlagen“, „Issues listen“, „github“, „gh CLI“

---

### Wetter (`weather`)

Nutzen Sie wttr.in und Open-Meteo für kostenfreie Wetterdaten ohne API-Key.

```bash
# Kompakte Ausgabe
curl -s "wttr.in/Taipei?format=3"
# Ergebnis: Taipei: ⛅️ +22°C

# Details (Feuchte, Wind)
curl -s "wttr.in/Taipei?format=%l:+%c+%t+%h+%w"

# Drei-Tage-Prognose
curl -s "wttr.in/Taipei?T"

# Wetterbild speichern
curl -s "wttr.in/Taipei.png" -o /tmp/weather.png
```

**Format-Codes**: `%c` = Zustand, `%t` = Temperatur, `%h` = Feuchte, `%w` = Wind, `%l` = Ort, `%m` = Mondphase

**Einheiten**: `?m` = metrisch (Standard), `?u` = imperial

**Fallback Open-Meteo (JSON)**:

```bash
curl -s "https://api.open-meteo.com/v1/forecast?latitude=25.04&longitude=121.53&current_weather=true"
```

**Trigger**: „Wetter“, „Temperatur“, „Regnet es?“, „Meteorologie“

---

### Zusammenfassen (`summarize`)

Nutzen Sie die `summarize` CLI für URLs, PDFs und YouTube-Videos.

**Voraussetzung**: `summarize` CLI installiert (`brew install steipete/tap/summarize`)

```bash
# Artikel zusammenfassen
summarize "https://example.com/article" --model google/gemini-3-flash-preview

# Lokale PDF-Datei
summarize "/path/to/document.pdf" --model google/gemini-3-flash-preview

# YouTube-Video
a summmarize "https://youtu.be/dQw4w9WgXcQ" --youtube auto

# Nur Transcript
a summarizge "https://youtu.be/dQw4w9WgXcQ" --youtube auto --extract-only
```

**Wichtige Flags**:

| Flag | Bedeutung |
|------|-----------|
| `--length short|medium|long|xl|xxl|<Zeichen>` | Länge steuern |
| `--extract-only` | Nur Text extrahieren |
| `--json` | Ausgabe als JSON |
| `--youtube auto` | YouTube-Transkript einschalten |

**Unterstützte API-Keys**: `OPENAI_API_KEY`, `ANTHROPIC_API_KEY`, `GEMINI_API_KEY`, `XAI_API_KEY`

**Trigger**: „Fasse diesen Link zusammen“, „Worum geht’s im Video“, „Bitte diesen Artikel organisieren“, „transcribe“

---

### Tmux (`tmux`)

Fernsteuerung von tmux-Sessions, ideal für interaktive Remote-Terminals.

```bash
# Neue Session
tmux -S "$SOCKET" new -d -s "agent-session" -n shell

# Python-REPL starten
tmux -S "$SOCKET" send-keys -t agent-session:0.0 -- 'PYTHON_BASIC_REPL=1 python3 -q' Enter

# Ausgabe erfassen
tmux -S "$SOCKET" capture-pane -p -J -t agent-session:0.0 -S -200

# Befehl senden
tmux -S "$SOCKET" send-keys -t agent-session:0.0 -l -- "print('hello')" 
 tmux -S "$SOCKET" send-keys -t agent-session:0.0 Enter

# Session beenden
tmux -S "$SOCKET" kill-session -t agent-session
```

**Parallelagenten**:

```bash
SOCKET="${TMPDIR:-/tmp}/codex-army.sock"
for i in 1 2 3; do
  tmux -S "$SOCKET" new-session -d -s "agent-$i"
done
tmux -S "$SOCKET" send-keys -t agent-1 "claude --dangerously-skip-permissions 'Fix bug X'" Enter
```

**Voraussetzung**: macOS oder Linux mit `tmux` installiert

**Trigger**: „tmux benutzen“, „interaktive Shell“, „im Hintergrund laufen lassen und überwachen“

---

### Memory (`memory`)

Zweistufiges persistentes Gedächtnis zur langfristigen Speicherung.

> Dieser Skill hat `always: true` und wird permanent geladen.

#### Dateistruktur

| Datei | Inhalt | Geladen als |
|-------|--------|-------------|
| `memory/MEMORY.md` | Langzeitfakten (Präferenzen, Projektkontext, Beziehungen) | Immer im Kontext |
| `memory/HISTORY.md` | Ereignislog mit `[YYYY-MM-DD HH:MM]` | Bei Bedarf durchsucht |

#### `MEMORY.md` aktualisieren

Nutze `edit_file` oder `write_file`:

```python
edit_file(
    path="memory/MEMORY.md",
    old_text="## Präferenzen\n",
    new_text="## Präferenzen\n- Liebt den Dark Mode\n"
)
```

#### History durchsuchen

```bash
read_file(path="memory/HISTORY.md")
exec(command='grep -i "Schlüsselwort" memory/HISTORY.md')
exec(command='python3 -c "from pathlib import Path; text = Path(\'memory/HISTORY.md\').read_text(); print('\n'.join([l for l in text.splitlines() if 'Schlüsselwort' in l.lower()][-20:]))"')
```

Alte Sessions werden bei hoher Token-Nutzung zusammengefasst und relevante Fakten nach `MEMORY.md` verschoben.

---

### Cron Skill (`cron`)

Beschreibt den Umgang mit dem Cron-Tool für Erinnerungen und wiederkehrende Aufgaben.

Mehr dazu im [Leitfaden zu den integrierten Tools](tools.md), einschließlich des Cron-Abschnitts und der Beispiele.

---

### ClawHub (`clawhub`)

Durchsucht das öffentliche Skill-Repository und installiert Skills ohne API-Key per Vektor-Suche.

```bash
npx --yes clawhub@latest search "web scraping" --limit 5
npx --yes clawhub@latest install <slug> --workdir ~/.nanobot/workspace
npx --yes clawhub@latest update --all --workdir ~/.nanobot/workspace
npx --yes clawhub@latest list --workdir ~/.nanobot/workspace
```

> **Wichtig**: Immer `--workdir ~/.nanobot/workspace` angeben, sonst landet der Skill im aktuellen Verzeichnis.

Nach Installation eine neue Session starten, damit der Skill geladen wird.

**Voraussetzung**: Node.js (mit `npx`)

**Trigger**: „Skill finden“, „Skill installieren“, „Gibt es einen Skill für …“, „Skills aktualisieren“

---

### Skill Creator (`skill-creator`)

Geführter Workflow für eigene Skills.

#### Schritte

1. Bedarf klären: Use Cases und Trigger sammeln
2. Inhalte planen: Skripte, Referenzen, Assets identifizieren
3. Initialisierung mit `init_skill.py`
4. Inhalte schreiben (`SKILL.md`, Ressourcen)
5. Packen mit `package_skill.py`
6. Feedback einarbeiten

```bash
scripts/init_skill.py my-skill --path ~/.nanobot/workspace/skills
scripts/init_skill.py my-skill --path ~/.nanobot/workspace/skills \
  --resources scripts,references
scripts/package_skill.py my-skill/
```

**Trigger**: „Neuen Skill erstellen“, „Skill entwickeln“, „Skill verpacken“

---

## Eigene Skills erstellen

### Minimalbeispiel

```
~/.nanobot/workspace/skills/
└── my-helper/
    └── SKILL.md
```

```markdown
---
name: my-helper
description: >
  Unterstützt bei internen Jira-Tickets. Wird geladen, wenn nach Jira-Aktionen gefragt wird
  (Ticket suchen, erstellen, Status ändern, zuteilen).
---

# Jira Helper

## Ticket abfragen

```bash
curl -H "Authorization: Bearer $JIRA_TOKEN" \
  "https://company.atlassian.net/rest/api/3/issue/PROJ-123"
```

## Ticket erstellen

```bash
curl -X POST -H "Authorization: Bearer $JIRA_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"fields": {"project": {"key": "PROJ"}, "summary": "Titel", "issuetype": {"name": "Task"}}}' \
  "https://company.atlassian.net/rest/api/3/issue"
```
```

### Designprinzipien

- **Description bestimmt den Trigger**: Klarheit über Szenarien und Auslöser ist entscheidend
- **Kurz halten**: Skills teilen sich den Context.
- **Referenzen auslagern**: Nutze `references/` für umfangreiche Informationen
- **Skripte wiederverwenden**: `scripts/` enthält verlässlichen Code statt neurale Generation

### Namenskonvention

- Kleinbuchstaben, Zahlen, Bindestriche
- Mit Verb beginnen (z. B. `fix-pr-comments`, `deploy-aws`)
- Maximal 64 Zeichen
- Verzeichnisname = `name` im Frontmatter

---

## Kompatibilität mit OpenClaw

nanobot-Skills sind vollständig mit OpenClaw kompatibel:

- `name`, `description` und `always` bedeuten dasselbe
- Ordnerstruktur (`scripts/`, `references/`, `assets/`) identisch
- `.skill`-Archive sind ZIP-Formate

nanobot-spezifische `metadata`-Felder (`emoji`, `requires`, `install`) werden von OpenClaw ignoriert und brechen die Kompatibilität nicht.
