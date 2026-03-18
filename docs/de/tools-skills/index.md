# Werkzeuge & Skills-Übersicht

Nanobot erweitert sich über zwei Ebenen: **Tools** sind eingebettete Aktionen (Shell, Datei, Web), während **Skills** wiederverwendbare Markdown-Module mit Wissen und Workflows sind. Gemeinsam bilden sie eine flexible KI-Assistenzplattform.

---

## Tools

Tools sind Python-Funktionen, die konkrete Operationen ausführen: Shell-Befehle, Dateioperationen, Websuchen, Cron-Aufgaben usw. Nanobot liefert die Tools und du passt sie über Konfiguration an.

| Tool | Beschreibung |
|---------|------|
| `exec` | Führt Shell-Kommandos und Skripte aus |
| `read_file` | Liest Dateien (inkl. Paging) |
| `write_file` | Schreibt Dateien (erstellt Verzeichnisse automatisch) |
| `edit_file` | Ersetzt Textabschnitte gezielt |
| `list_dir` | Listet Verzeichnisse auf |
| `web_search` | Websuche über mehrere Provider |
| `web_fetch` | Ruft und analysiert Webseiten ab |
| `cron` | Scheduler für wiederkehrende Aufgaben |
| `spawn` | Startet Hintergrund-Agenten für komplexe Tasks |
| `message` | Sendet Nachrichten an Nutzer (inkl. Anhänge) |

Details siehe [Tools Guide](tools.md).

---

## Skills

Skills sind Markdown-basierte Module, die dem Agenten erklären, wie bestimmte Aufgaben ausgeführt werden sollen. Sie laden bei Bedarf Fachwissen, Beispiele, Skripte und Befehle in den Kontext.

Skills orientieren sich am [OpenClaw-Skill-Format](https://github.com/openclaw/openclaw) und bleiben kompatibel mit dessen Ökosystem.

| Skill | Beschreibung |
|---------|------|
| `github` | Interagiert über `gh` CLI mit GitHub |
| `weather` | Holt Wetterdaten (wttr.in / Open-Meteo) |
| `summarize` | Fasst URLs, YouTube-Videos und lokale Dateien zusammen |
| `tmux` | Steuert tmux-Workspaces fern |
| `memory` | Zwei-Ebenen-Memory (Facts + History) |
| `cron` | Leitfaden für Cron und Erinnerungen |
| `clawhub` | Sucht und installiert Skills aus dem ClawHub-Repository |
| `skill-creator` | Führt durch die Erstellung eigener Skills |

Details siehe [Skills Guide](skills.md).

---

## Unterschied Tools vs. Skills

| Aspekt | Tools | Skills |
|------|--------------|---------------|
| Natur | Python-Code, direkt aufrufbar | Markdown-Dokumente, laden Kontext |
| Erweiterung | Core oder MCP | Jeder kann `.skill` schreiben |
| Trigger | Agent entscheidet | `description` löst Laden aus |
| Fähigkeit | Führt Operationen aus (Shell, Web, Datei) | Bietet Wissen, Prozesse, Beispiele |
| Distribution | Teil der nanobot-Installation | `.skill`-Archive, ClawHub |

---

## MCP-Integration

MCP (Model Context Protocol) verbindet externe Tool-Server mit nanobot. So können neue Tools ohne Core-Änderung eingebunden werden.

Verbindungstypen:

- **Stdio**: Lokaler Prozess über STDIN/STDOUT
- **HTTP/SSE**: Remote per URL

Jedes MCP-Tool erscheint als `mcp_<server>_<toolname>` und wird wie Core-Tools vom Agenten verwendet.

Details siehe [MCP Guide](mcp.md).
