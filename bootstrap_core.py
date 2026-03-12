"""MightyDestroyer Governance Bootstrap — Kern-Logik.

Erstellt ein neues Projekt mit Governance-konformer Struktur.
Unabhaengig von der GUI nutzbar.
"""

import json
import logging
import os
import re
import shutil
import subprocess
import sys
from datetime import date
from typing import Callable, Optional

from config import (
    GOVERNANCE_REPO_URL,
    GOVERNANCE_RAW_URL,
    GOVERNANCE_PRINCIPLES_URL,
    TEMPLATE_FILES,
    get_templates_dir,
    get_cache_dir,
)

_SUBPROCESS_FLAGS = 0x08000000 if sys.platform == "win32" else 0

SERVICE_NAME = "bootstrap-gui"
logger = logging.getLogger(SERVICE_NAME)


class JSONFormatter(logging.Formatter):
    """Formats log records as structured JSON."""

    def format(self, record: logging.LogRecord) -> str:
        log_obj = {
            "timestamp": self.formatTime(record, self.datefmt),
            "level": record.levelname,
            "message": record.getMessage(),
            "service": SERVICE_NAME,
        }
        if record.exc_info:
            log_obj["exception"] = self.formatException(record.exc_info)
        for key, value in record.__dict__.items():
            if key not in (
                "name", "msg", "args", "created", "filename", "funcName",
                "levelname", "levelno", "lineno", "module", "msecs",
                "pathname", "process", "processName", "relativeCreated",
                "stack_info", "exc_info", "exc_text", "thread", "threadName",
                "message", "taskName",
            ):
                log_obj[key] = value
        return json.dumps(log_obj, ensure_ascii=False)


def setup_logging(log_level: str = "INFO") -> None:
    """Configure structured JSON logging for bootstrap-gui."""
    log_level_val = getattr(logging, log_level.upper(), logging.INFO)
    logger.setLevel(log_level_val)
    if not logger.handlers:
        handler = logging.StreamHandler(sys.stderr)
        handler.setFormatter(JSONFormatter())
        logger.addHandler(handler)


def _emit_log(msg: str, level: str, log: Optional[Callable[[str], None]]) -> None:
    """Log to structured logger and optionally to GUI callback."""
    getattr(logger, level)(msg)
    if log:
        log(msg)


def update_templates(log: Optional[Callable[[str], None]] = None) -> bool:
    """Laedt Templates aus dem Governance-Repo (GitHub Raw) in den lokalen Cache.
    Gibt True zurueck bei Erfolg, False bei Fehler."""
    import urllib.request
    import urllib.error

    cache = get_cache_dir()
    success = True

    for local_name, remote_path in TEMPLATE_FILES.items():
        url = f"{GOVERNANCE_RAW_URL}/{remote_path}"
        target = os.path.join(cache, local_name)
        try:
            _emit_log(f">> Lade {local_name} ...", "info", log)
            urllib.request.urlretrieve(url, target)
        except (urllib.error.URLError, OSError) as e:
            _emit_log(f">> WARNUNG: {local_name} konnte nicht geladen werden: {e}", "warning", log)
            success = False

    if success:
        _emit_log(">> Templates aktualisiert.", "info", log)
    else:
        _emit_log(
            ">> Einige Templates konnten nicht aktualisiert werden. Fallback: eingebettete Templates.",
            "warning",
            log,
        )

    return success


def validate_project_name(name: str) -> Optional[str]:
    """Validiert den Projektnamen. Gibt Fehlermeldung oder None zurueck."""
    if not name:
        return "Projektname darf nicht leer sein."
    if re.search(r"[A-Z]", name):
        return "Projektname muss lowercase sein."
    if re.search(r"[_ ]", name):
        return "Projektname darf keine Unterstriche oder Leerzeichen enthalten. Nutze kebab-case."
    if not re.match(r"^[a-z][a-z0-9-]*$", name):
        return "Projektname darf nur a-z, 0-9 und Bindestriche enthalten."
    return None


def check_git_available() -> bool:
    try:
        subprocess.run(["git", "--version"], capture_output=True, check=True,
                       creationflags=_SUBPROCESS_FLAGS)
        return True
    except (FileNotFoundError, subprocess.CalledProcessError):
        return False


def check_gh_available() -> bool:
    try:
        result = subprocess.run(["gh", "auth", "status"], capture_output=True,
                                creationflags=_SUBPROCESS_FLAGS)
        return result.returncode == 0
    except FileNotFoundError:
        return False


GITIGNORE_BASE = """\
# OS
.DS_Store
Thumbs.db
desktop.ini

# IDE
.vscode/settings.json
.idea/
*.swp
*.swo

# Environment
.env
.env.*
!.env.example

# Cursor (rules werden getrackt)
.cursor/*
!.cursor/rules/
"""

GITIGNORE_STACK = {
    "node": """
# Node
node_modules/
dist/
build/
.next/
coverage/
*.tsbuildinfo
""",
    "python": """
# Python
__pycache__/
*.py[cod]
*.egg-info/
dist/
build/
.venv/
venv/
.pytest_cache/
.coverage
htmlcov/
""",
    "go": """
# Go
bin/
vendor/
*.exe
*.test
*.out
""",
    "rust": """
# Rust
target/
Cargo.lock
""",
    "generic": "",
}


def _read_template(name: str) -> str:
    path = os.path.join(get_templates_dir(), name)
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def _replace_placeholders(content: str, replacements: dict) -> str:
    for key, value in replacements.items():
        content = content.replace(key, value)
    return content


def _run_cmd(cmd: list[str], cwd: str) -> subprocess.CompletedProcess:
    return subprocess.run(
        cmd, cwd=cwd, capture_output=True, text=True, encoding="utf-8",
        creationflags=_SUBPROCESS_FLAGS,
    )


def bootstrap_project(
    name: str,
    stack: str,
    description: str,
    target_parent: str,
    create_github: bool = False,
    github_org: str = "",
    github_private: bool = True,
    log: Optional[Callable[[str], None]] = None,
) -> str:
    """Erstellt ein neues Projekt. Gibt den Projekt-Pfad zurueck.

    Args:
        name: Projektname (lowercase, kebab-case)
        stack: Tech-Stack (node, python, go, rust, generic)
        description: Kurzbeschreibung
        target_parent: Elternverzeichnis
        create_github: GitHub-Repo erstellen?
        github_org: GitHub-Organisation/User
        github_private: Private Repo?
        log: Callback fuer Log-Ausgabe
    """
    project_dir = os.path.join(target_parent, name)
    today = date.today().isoformat()
    github_url = ""

    if create_github and github_org:
        github_url = f"https://github.com/{github_org}/{name}"

    # --- Validierung ---
    error = validate_project_name(name)
    if error:
        raise ValueError(error)

    if os.path.exists(project_dir):
        raise ValueError(f"Verzeichnis existiert bereits: {project_dir}")

    if not check_git_available():
        raise RuntimeError("Git ist nicht installiert oder nicht im PATH.")

    if create_github and not check_gh_available():
        raise RuntimeError(
            "GitHub CLI (gh) ist nicht installiert oder nicht eingeloggt.\n"
            "Installiere gh: https://cli.github.com\n"
            "Login: gh auth login"
        )

    # --- Ordnerstruktur ---
    _emit_log(">> Ordnerstruktur anlegen...", "info", log)
    dirs = [
        "src/features",
        "src/shared/utils",
        "src/shared/types",
        "src/shared/config",
        "tests/unit",
        "tests/integration",
        "tests/e2e",
        "docs/adrs",
        "scripts",
        ".github/workflows",
        ".cursor/rules",
    ]
    for d in dirs:
        os.makedirs(os.path.join(project_dir, d), exist_ok=True)

    # --- .gitignore ---
    _emit_log(">> .gitignore generieren...", "info", log)
    gitignore = GITIGNORE_BASE + GITIGNORE_STACK.get(stack, "")
    with open(os.path.join(project_dir, ".gitignore"), "w", encoding="utf-8") as f:
        f.write(gitignore)

    # --- .env.example ---
    _emit_log(">> .env.example anlegen...", "info", log)
    env_example = f"""\
# {name} — Environment Variables
# Kopiere diese Datei zu .env und fuelle die Werte aus.
# NIEMALS .env committen!

# App
APP_NAME={name}
APP_ENV=development
APP_PORT=3000

# Database (falls zutreffend)
# DATABASE_URL=

# API Keys (falls zutreffend)
# API_KEY=
"""
    with open(os.path.join(project_dir, ".env.example"), "w", encoding="utf-8") as f:
        f.write(env_example)

    # --- CLAUDE.md ---
    _emit_log(">> CLAUDE.md generieren...", "info", log)
    claude_tpl = _read_template("claude.md")
    lines = [
        l for l in claude_tpl.splitlines()
        if not l.startswith("> Dieses Template")
    ]
    claude_content = "\n".join(lines)
    claude_content = _replace_placeholders(claude_content, {
        "[Projektname]": name,
        "[Kurzbeschreibung — was macht dieses Projekt?]": description,
        "[z. B. TypeScript, Next.js, PostgreSQL]": stack,
        "[GitHub-URL]": github_url or "tbd",
    })
    with open(os.path.join(project_dir, "CLAUDE.md"), "w", encoding="utf-8") as f:
        f.write(claude_content)

    # --- README.md ---
    _emit_log(">> README.md generieren...", "info", log)
    readme = f"""\
# {name}

{description}

## Setup

```bash
git clone {github_url or '<repo-url>'}
cd {name}
cp .env.example .env
```

## Stack

- **Stack:** {stack}

## Governance

Dieses Projekt folgt den MightyDestroyer Governance-Prinzipien.
Siehe: [{GOVERNANCE_REPO_URL}]({GOVERNANCE_REPO_URL})
Kernprinzipien: [standards/principles.md]({GOVERNANCE_PRINCIPLES_URL})

## Dokumentation

- [CLAUDE.md](CLAUDE.md) — Agenten-Anweisungen
- [Project Bible](docs/project-bible.md) — Sprint-Protokoll und Entscheidungen
- [ADRs](docs/adrs/) — Architektur-Entscheidungen

---

*Generiert mit MightyDestroyer Governance Bootstrap*
"""
    with open(os.path.join(project_dir, "README.md"), "w", encoding="utf-8") as f:
        f.write(readme)

    # --- MEMORY.md ---
    _emit_log(">> MEMORY.md anlegen...", "info", log)
    memory = f"""\
# MEMORY.md — {name}

Persistenter Kontext ueber Sessions hinweg. Wird von KI-Agenten bei Session-Start gelesen.

## Projekt-Status

- **Phase:** Initialisierung
- **Erstellt:** {today}
- **Stack:** {stack}

## Zentrale Entscheidungen

_Noch keine Entscheidungen dokumentiert._

## Offene Punkte

_Noch keine offenen Punkte._

---

*Zuletzt aktualisiert: {today}*
"""
    with open(os.path.join(project_dir, "MEMORY.md"), "w", encoding="utf-8") as f:
        f.write(memory)

    # --- Project Bible ---
    _emit_log(">> Project Bible generieren...", "info", log)
    bible_tpl = _read_template("project-bible.md")
    bible_lines = [
        l for l in bible_tpl.splitlines()
        if not l.startswith("> Dieses Template")
    ]
    bible_content = "\n".join(bible_lines)
    bible_content = _replace_placeholders(bible_content, {
        "[Projektname]": name,
        "[Was soll das Projekt erreichen?]": description,
        "[z. B. TypeScript, Next.js, PostgreSQL, Docker]": stack,
        "[Datum]": today,
    })
    with open(os.path.join(project_dir, "docs", "project-bible.md"), "w", encoding="utf-8") as f:
        f.write(bible_content)

    # --- PR Template ---
    _emit_log(">> PR Template kopieren...", "info", log)
    pr_tpl = _read_template("pull-request-template.md")
    with open(os.path.join(project_dir, ".github", "pull-request-template.md"), "w", encoding="utf-8") as f:
        f.write(pr_tpl)

    # --- Cursor Rules ---
    _emit_log(">> Cursor Rules kopieren...", "info", log)
    gov_rule = _read_template("governance.mdc")
    with open(os.path.join(project_dir, ".cursor", "rules", "governance.mdc"), "w", encoding="utf-8") as f:
        f.write(gov_rule)

    # --- Git init ---
    _emit_log(">> Git initialisieren...", "info", log)
    _run_cmd(["git", "init", "-b", "main"], project_dir)
    _run_cmd(["git", "add", "."], project_dir)

    commit_msg = (
        f"Initial setup: {name} (via Governance Bootstrap)\n\n"
        f"- Ordnerstruktur gemaess MightyDestroyer/Governance\n"
        f"- CLAUDE.md, README, MEMORY.md, Project Bible\n"
        f"- .gitignore ({stack}), .env.example\n"
        f"- PR Template, Cursor Rules"
    )
    _run_cmd(["git", "commit", "-m", commit_msg], project_dir)
    _emit_log(">> Git-Repository initialisiert.", "info", log)

    # --- GitHub ---
    if create_github and github_org:
        _emit_log(f">> GitHub-Repo erstellen: {github_org}/{name} ...", "info", log)
        visibility = "--private" if github_private else "--public"
        result = _run_cmd(
            ["gh", "repo", "create", f"{github_org}/{name}", visibility, "--source=.", "--push"],
            project_dir,
        )
        if result.returncode == 0:
            _emit_log(f">> GitHub-Repo erstellt: {github_url}", "info", log)
        else:
            error_msg = result.stderr.strip() or result.stdout.strip()
            _emit_log(f">> WARNUNG: GitHub-Repo konnte nicht erstellt werden: {error_msg}", "warning", log)
            _emit_log(f">> Manuell: gh repo create {github_org}/{name} {visibility} --source=. --push", "info", log)

    _emit_log("", "info", log)
    _emit_log("=== Projekt erfolgreich erstellt! ===", "info", log)
    _emit_log(f"Pfad: {project_dir}", "info", log)

    return project_dir
