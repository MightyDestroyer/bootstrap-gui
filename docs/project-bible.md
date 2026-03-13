# Project Bible — bootstrap-gui

## Uebersicht

- **Projekt:** bootstrap-gui
- **Ziel:** Desktop-App zum Erstellen neuer Governance-konformer Projekte per GUI
- **Stack:** Python, Tkinter, PyInstaller
- **Start:** Maerz 2026
- **Governance:** [MightyDestroyer/governance](https://github.com/MightyDestroyer/governance) v3.5.0

---

## Sprint-Protokoll

### Sprint 1 — 2026-03-12

**Ziel:** Initiale Implementierung der Bootstrap GUI.

**Erreicht:**
- Tkinter GUI mit Formular, Validierung, Live-Log
- Kern-Logik: Ordnerstruktur, Templates, .gitignore, Git init, GitHub-Integration
- Template-Download aus Governance-Repo (GitHub Raw, Cache in %APPDATA%)
- Structured JSON Logging (JSONFormatter)
- PyInstaller Build-Script fuer standalone .exe
- Governance v2.0 konform (CLAUDE.md, README.md, Makefile)

**Entscheidungen:** ADR-001 (Python + Tkinter + PyInstaller)

---

## Architektur-Entscheidungen (ADRs)

| ADR | Titel | Status | Datum |
|-----|-------|--------|-------|
| ADR-001 | Python + Tkinter + PyInstaller | Akzeptiert | 2026-03 |

Vollstaendige ADRs unter `docs/adrs/`.

---

## Zentrale Abhaengigkeiten

| Abhaengigkeit | Version | Zweck |
|--------------|---------|-------|
| Python | 3.12+ | Sprache |
| Tkinter | stdlib | GUI Framework |
| PyInstaller | 6.x | Standalone .exe Build |

---

## Offene Punkte / Backlog

Kein Backlog — alle Findings werden sofort behoben.

---

*bootstrap-gui · Governance v3.5.0*
