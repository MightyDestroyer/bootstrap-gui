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
APP_VERSION = "2.0.0"

TEMPLATE_FILES = {
    "claude.md": "templates/claude.md",
    "project-bible.md": "templates/project-bible.md",
    "governance.mdc": "templates/cursor-rules/governance.mdc",
    "pull-request-template.md": ".github/pull-request-template.md",
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
