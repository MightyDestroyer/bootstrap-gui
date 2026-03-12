# MightyDestroyer — Governance Bootstrap GUI

> Teil des [MightyDestroyer Governance](https://github.com/MightyDestroyer/Governance) Oekosystems.

Desktop-Anwendung zum Erstellen neuer Governance-konformer Projekte. Standalone `.exe`, die ohne Python auf dem Zielrechner funktioniert.

## v2.0 Changes

- **Structured JSON logging:** Alle Logs werden als strukturiertes JSON ausgegeben (`timestamp`, `level`, `message`, `service`, `...extra`), konform zu `tool-development.md`
- **Governance-konform:** Volle Einhaltung der MightyDestroyer Tool-Entwicklungsstandards
- **Logging von Nutzeraktionen:** Projekt-Erstellung (gestartet, abgeschlossen, fehlgeschlagen), Template-Updates

## Features

- **Projekt-Setup per Knopfdruck:** Name, Stack, Beschreibung eingeben — fertig
- **Governance-konform:** Ordnerstruktur, CLAUDE.md, MEMORY.md, Project Bible, Cursor Rules
- **GitHub-Integration:** Repo erstellen via `gh` CLI (optional)
- **Validierung:** Projektname (kebab-case), Zielordner, Git/gh-Verfuegbarkeit
- **Live-Log:** Echtzeit-Fortschrittsanzeige

## Voraussetzungen

### Fuer Endnutzer (.exe)

| Tool | Status   | Hinweis                              |
| ---- | -------- | ------------------------------------ |
| Git  | Pflicht  | `git --version` muss funktionieren   |
| gh   | Optional | Nur fuer GitHub-Repo-Erstellung      |

Python wird **nicht** benoetigt — ist in der `.exe` gebuendelt.

### Fuer Entwickler / Build

- Python 3.10+
- `pip install -r requirements.txt`

## Nutzung

### Als .exe (Endnutzer)

1. `MightyDestroyer-Bootstrap.exe` starten
2. Projektname eingeben (lowercase, kebab-case)
3. Stack waehlen
4. Optional: GitHub-Checkbox aktivieren
5. "Projekt erstellen" klicken
6. Log verfolgen — bei Erfolg "Ordner oeffnen"

### Als Python-Script (Entwickler)

```bash
cd tools/bootstrap-gui
python bootstrap_gui.py
```

## Build (.exe erzeugen)

```bash
cd tools/bootstrap-gui
pip install -r requirements.txt
python build.py
```

Die `.exe` wird in `tools/bootstrap-gui/dist/MightyDestroyer-Bootstrap.exe` erstellt.

## Architektur

```
tools/bootstrap-gui/
├── bootstrap_gui.py     ← Hauptdatei: Tkinter GUI
├── bootstrap_core.py    ← Kern-Logik (Ordner, Templates, Git)
├── config.py            ← Konfiguration (URLs, Stacks, Pfade)
├── build.py             ← PyInstaller Build-Script
├── requirements.txt     ← Build-Dependencies
├── templates/           ← Eingebettete Templates (in .exe gebuendelt)
│   ├── claude.md
│   ├── project-bible.md
│   ├── governance.mdc
│   └── pull-request-template.md
└── README.md            ← Diese Datei
```

## Verteilung

Die fertige `.exe` kann verteilt werden ueber:

- Interner Fileshare / Teams
- GitHub Release im Governance-Repo
- USB-Stick (im Notfall)

## Version

Aktuelle Version: **2.0.0**

## Prinzipien-Konformitaet

- **Generik**: Governance-URL und Templates als Konfiguration, nicht hardcodiert
- **Contract First**: Templates aus dem Governance-Repo sind der Vertrag
- **Keine Legacy**: Saubere Python-Implementierung, kein Bash-Wrapper
- **Komplexitaets-Budget**: Eine Aufgabe — Projekt bootstrappen
