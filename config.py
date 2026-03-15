"""MightyDestroyer Governance Bootstrap — Konfiguration."""

import os
import sys

GOVERNANCE_REPO_URL = "https://github.com/MightyDestroyer/governance"
GOVERNANCE_RAW_URL = "https://raw.githubusercontent.com/MightyDestroyer/governance/main"
GOVERNANCE_PRINCIPLES_URL = f"{GOVERNANCE_REPO_URL}/blob/main/standards/principles.md"

STACK_OPTIONS = ["generic", "node", "python", "go", "rust"]

DEFAULT_ORG = "MightyDestroyer"
DEFAULT_TARGET_DIR = os.path.expanduser("~\\dev") if sys.platform == "win32" else os.path.expanduser("~/dev")

APP_NAME = "MightyDestroyer — Project Bootstrap"
APP_VERSION = "3.0.0"

TEMPLATE_FILES = {
    "claude.md": "templates/claude.md",
    "project-bible.md": "templates/project-bible.md",
    "governance.mdc": "templates/cursor-rules/governance.mdc",
    "adr.mdc": "templates/cursor-rules/adr.mdc",
    "makefile.mdc": "templates/cursor-rules/makefile.mdc",
    "yaml-contracts.mdc": "templates/cursor-rules/yaml-contracts.mdc",
    "go.mdc": "templates/cursor-rules/go.mdc",
    "pull-request-template.md": ".github/pull-request-template.md",
    "ci.yml": "templates/workflows/ci.yml",
    "governance-gate.yml": "templates/workflows/governance-gate.yml",
    "hook-pre-commit": "templates/hooks/pre-commit",
    "hook-commit-msg": "templates/hooks/commit-msg",
    "hook-pre-push": "templates/hooks/pre-push",
    "skill-development-workflow": "templates/cursor-skills/development-workflow/SKILL.md",
    "skill-sprint-audit": "templates/cursor-skills/sprint-audit/SKILL.md",
    "skill-audit-loop": "templates/cursor-skills/audit-loop/SKILL.md",
    "skill-onboard-project": "templates/cursor-skills/onboard-project/SKILL.md",
    "skill-create-adr": "templates/cursor-skills/create-adr/SKILL.md",
}

CORE_SKILLS = [
    "development-workflow",
    "sprint-audit",
    "audit-loop",
    "onboard-project",
    "create-adr",
]

UNIVERSAL_RULES = ["governance.mdc", "adr.mdc", "makefile.mdc", "yaml-contracts.mdc"]

STACK_RULES = {
    "go": ["go.mdc"],
    "node": [],
    "python": [],
    "rust": [],
    "generic": [],
}

STACK_CONFIG_FILES = {
    "node": ["Makefile", ".eslintrc.json", ".prettierrc", "tsconfig.json"],
    "python": ["Makefile", "pyproject.toml"],
    "go": ["Makefile", ".golangci.yml"],
    "rust": ["clippy.toml", "rustfmt.toml"],
    "generic": [],
}


def get_cache_dir():
    """Lokaler Cache fuer heruntergeladene Templates."""
    if sys.platform == "win32":
        base = os.environ.get("APPDATA", os.path.expanduser("~"))
    else:
        base = os.path.expanduser("~/.cache")
    cache = os.path.join(base, "MightyDestroyer", "templates")
    os.makedirs(cache, exist_ok=True)
    return cache


def get_bundled_templates_dir():
    """Eingebettete Templates (Fallback)."""
    if getattr(sys, "frozen", False):
        return os.path.join(sys._MEIPASS, "templates")
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), "templates")


def get_templates_dir():
    """Gibt den besten verfuegbaren Templates-Ordner zurueck.
    Prioritaet: Cache (heruntergeladen) > Eingebettet (Fallback)."""
    cache = get_cache_dir()
    if os.path.exists(os.path.join(cache, "claude.md")):
        return cache
    return get_bundled_templates_dir()
