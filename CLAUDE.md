# Bootstrap GUI — Agenten-Anweisungen

## Purpose

Project bootstrapping GUI: Desktop-Anwendung zum Erstellen neuer Governance-konformer Projekte per Klick. Erstellt Ordnerstruktur, CLAUDE.md, MEMORY.md, Project Bible, Cursor Rules, Git-Init und optional GitHub-Repos.

## Architecture

| File | Role |
|------|------|
| `config.py` | Settings (URLs, Stacks, Pfade, Version) |
| `bootstrap_core.py` | Kern-Logik (Ordner, Templates, Git, GitHub) |
| `bootstrap_gui.py` | Tkinter UI, Einstiegspunkt |
| `build.py` | PyInstaller-Packaging für .exe |

## Standards

- **tool-development.md:** Folgt MightyDestroyer Tool-Entwicklungsstandards
- **Structured JSON logging:** Alle Logs als JSON mit `timestamp`, `level`, `message`, `service`, `...extra`
- **Error handling:** Saubere Exception-Behandlung, keine stummen Fehler

## Build

```bash
python build.py
```

## Test

```bash
python -m pytest tests/
```

*(Tests pending)*
