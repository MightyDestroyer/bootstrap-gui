# ADR-001: Python + Tkinter + PyInstaller

**Status:** Akzeptiert
**Datum:** 2026-03-12
**Kontext:** Architektur-Entscheidung fuer die Bootstrap GUI

---

## Kontext

Es wird eine Desktop-App benoetigt die neue Projekte mit Governance-konformer Struktur erstellen kann.

## Entscheidung

- **Sprache:** Python — breite stdlib, schnelle Prototypen
- **GUI:** Tkinter — keine externe Dependency, Teil der Python stdlib
- **Packaging:** PyInstaller — standalone .exe ohne Python-Installation beim Endnutzer
- **Logging:** JSONFormatter (stdlib logging) — konsistent mit Governance Structured Logging Standard

## Alternativen

| Alternative | Grund fuer Ablehnung |
|------------|---------------------|
| Electron | Zu schwer fuer einfache GUI, Node-Abhaengigkeit |
| Go + Fyne | Zusaetzliche Sprache im Tooling-Mix |
| CLI only | Weniger zugaenglich fuer neue Nutzer |

## Konsequenzen

- Kein externes GUI-Framework noetig (stdlib reicht)
- Single .exe Distribution (kein Python beim Nutzer noetig)
- Template-Download aus Governance-Repo (SSoT)

---

*bootstrap-gui · ADR-001*
