# CLAUDE.md — Template

> Dieses Template wird beim Aufsetzen eines neuen MightyDestroyer-Projekts als `CLAUDE.md` ins Root kopiert und projektspezifisch angepasst.

---

# CLAUDE.md

## Projekt

- **Name:** [Projektname]
- **Beschreibung:** [Kurzbeschreibung — was macht dieses Projekt?]
- **Stack:** [z. B. TypeScript, Next.js, PostgreSQL]
- **Repo:** [GitHub-URL]

## Governance

Dieses Projekt folgt den MightyDestroyer Governance-Prinzipien.  
**Governance-Repo:** [MightyDestroyer/governance](https://github.com/MightyDestroyer/governance)  
**Kernprinzipien:** [standards/principles.md](https://github.com/MightyDestroyer/governance/blob/main/standards/principles.md)

### Verbindliche Standards

- [Kernprinzipien](https://github.com/MightyDestroyer/governance/blob/main/standards/principles.md) — 11 Prinzipien, alle verbindlich.
- [AI Guardrails](https://github.com/MightyDestroyer/governance/blob/main/standards/ai-guardrails.md) — Regeln für KI-Agenten.
- [Security Guidelines](https://github.com/MightyDestroyer/governance/blob/main/standards/security-guidelines.md) — Sicherheitsrichtlinien.
- [Coding Principles](https://github.com/MightyDestroyer/governance/blob/main/standards/coding-principles.md) — Coding-Standards.
- [Compliance by Design](https://github.com/MightyDestroyer/governance/blob/main/standards/compliance-by-design.md) — Compliance-Anforderungen.

## Anweisungen für KI-Agenten

### Allgemein

- Lies diese Datei vollständig, bevor du mit einer Aufgabe beginnst.
- Halte dich an die Governance-Prinzipien — insbesondere: kein Auto-Commit, kein Auto-Deploy, keine Architekturentscheidungen ohne Rücksprache.
- Änderungen nur innerhalb des definierten Scope (siehe Aufgaben-Template).
- Bei Unsicherheit: Stopp und Rückfrage — keine Annahmen.

### Naming Convention

- **Dateien/Ordner:** lowercase, kebab-case.
- **Code:** Siehe Coding Principles (camelCase für JS/TS, snake_case für Python etc.).
- **Branches:** `feature/beschreibung`, `fix/beschreibung`, `docs/beschreibung`.

### Commit-Regeln

- Klare, aussagekräftige Commit-Messages.
- Kein Commit ohne Doku-Update (README, ADRs, MEMORY.md falls betroffen).
- Kein Commit mit Secrets, hardcodierten Werten oder TODO-ohne-Ticket.

### Kontext-Dateien

| Datei | Zweck | Pflicht? |
|-------|-------|----------|
| `CLAUDE.md` | Diese Datei — Agenten-Anweisungen | Ja |
| `README.md` | Projektübersicht, Setup | Ja |
| `MEMORY.md` | Persistenter Kontext über Sessions | Empfohlen |
| `TASKS.md` | Aktuelle Aufgaben, Sprint-Status | Optional |
| `docs/project-bible.md` | Sprint-Protokoll, ADRs, Entscheidungen | Empfohlen |

### Session-Start

1. CLAUDE.md lesen (diese Datei).
2. MEMORY.md lesen (falls vorhanden).
3. Übergabe-Dokument der letzten Session lesen (falls vorhanden).
4. Scope der aktuellen Aufgabe klären.

### Session-Ende

1. Doku aktualisieren (README, MEMORY.md, ADRs).
2. Übergabe-Dokument erstellen (falls relevanter Kontext).
3. TASKS.md aktualisieren (falls vorhanden).

## Projektspezifische Regeln

<!-- Hier projektspezifische Anweisungen einfügen, z. B.: -->
<!-- - Design-System: [Link oder Beschreibung] -->
<!-- - API-Konventionen: [REST, GraphQL, Naming] -->
<!-- - Deployment-Prozess: [Beschreibung] -->
<!-- - Besondere Abhängigkeiten oder Constraints -->

## ADRs

Architektur-Entscheidungen werden unter `docs/adrs/` dokumentiert.  
Template: [ADR-Template](https://github.com/MightyDestroyer/governance/blob/main/standards/architecture-patterns.md#adr-template)

---

*Generiert aus MightyDestroyer/governance — templates/claude.md*
