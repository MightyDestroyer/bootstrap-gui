# Project Bible — Template

> Dieses Template wird beim Aufsetzen eines neuen MightyDestroyer-Projekts als `docs/project-bible.md` ins Repo kopiert und projektspezifisch gepflegt.

---

# Project Bible — [Projektname]

## Übersicht

- **Projekt:** [Projektname]
- **Ziel:** [Was soll das Projekt erreichen?]
- **Stack:** [z. B. TypeScript, Next.js, PostgreSQL, Docker]
- **Start:** [Datum]
- **Governance:** [MightyDestroyer/Governance](https://github.com/MightyDestroyer/Governance)

---

## Sprint-Protokoll

### Sprint [N] — [Datum]

**Ziel:** [Was war das Sprint-Ziel?]

**Erreicht:**
- [Was wurde umgesetzt?]

**Offen:**
- [Was ist noch offen?]

**Entscheidungen:**
- [Welche Entscheidungen wurden getroffen? Verweis auf ADR falls vorhanden.]

**Nächste Schritte:**
- [Was kommt als nächstes?]

---

<!-- Weitere Sprints nach demselben Schema ergänzen -->

## Architektur-Entscheidungen (ADRs)

| ADR | Titel | Status | Datum |
|-----|-------|--------|-------|
| ADR-001 | [Titel] | Akzeptiert | [Datum] |

Vollständige ADRs unter `docs/adrs/`.

---

## Zentrale Abhängigkeiten

| Abhängigkeit | Version | Zweck | Bemerkung |
|-------------|---------|-------|-----------|
| [z. B. Next.js] | [z. B. 14.x] | [Framework] | |
| [z. B. PostgreSQL] | [z. B. 16] | [Datenbank] | |

---

## Datenflüsse

<!-- Relevante Datenflüsse beschreiben — für Compliance und Security wichtig -->

| Datenfluss | Quelle | Ziel | Personenbezogen? | Rechtsgrundlage |
|-----------|--------|------|-------------------|-----------------|
| [z. B. User-Registrierung] | [Frontend-Form] | [PostgreSQL] | Ja | Consent |

---

## Offene Punkte / Backlog

- [ ] [Offener Punkt mit Beschreibung]
- [ ] [Compliance-Lücke, die noch adressiert werden muss]
- [ ] [Technische Schulden, die bewusst aufgenommen wurden (mit Begründung)]

---

## Session-Trigger

Hinweise für den Beginn einer neuen Session:

- [ ] CLAUDE.md und diese Project Bible gelesen?
- [ ] MEMORY.md gelesen (falls vorhanden)?
- [ ] Übergabe-Dokument der letzten Session gelesen?
- [ ] Scope der nächsten Aufgabe klar?
- [ ] Relevante ADRs geprüft?

---

*Generiert aus MightyDestroyer/Governance — templates/project-bible.md*
