"""MightyDestroyer Governance Bootstrap — Desktop GUI.

Standalone-Anwendung zum Erstellen neuer Governance-konformer Projekte.
Tkinter-basiert, kann mit PyInstaller als .exe gebaut werden.
"""

import logging
import os
import sys
import threading
import tkinter as tk
from tkinter import ttk, filedialog, messagebox

from config import APP_NAME, APP_VERSION, STACK_OPTIONS, DEFAULT_ORG, DEFAULT_TARGET_DIR, get_templates_dir, get_cache_dir
from bootstrap_core import (
    validate_project_name,
    check_git_available,
    check_gh_available,
    bootstrap_project,
    update_templates,
    setup_logging,
)

logger = logging.getLogger("bootstrap-gui")


class BootstrapApp:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title(f"Governance Bootstrap v{APP_VERSION}")
        self.root.resizable(False, False)
        self.running = False

        self._center_window(560, 620)
        self._build_ui()
        self._check_prerequisites()

    def _center_window(self, w: int, h: int):
        sw = self.root.winfo_screenwidth()
        sh = self.root.winfo_screenheight()
        x = (sw - w) // 2
        y = (sh - h) // 2
        self.root.geometry(f"{w}x{h}+{x}+{y}")

    def _build_ui(self):
        style = ttk.Style()
        style.configure("Header.TLabel", font=("Segoe UI", 14, "bold"))
        style.configure("TButton", font=("Segoe UI", 10))
        style.configure("TLabel", font=("Segoe UI", 10))

        main = ttk.Frame(self.root, padding=20)
        main.pack(fill="both", expand=True)

        # --- Header ---
        ttk.Label(main, text=APP_NAME, style="Header.TLabel").pack(anchor="w")
        ttk.Separator(main, orient="horizontal").pack(fill="x", pady=(5, 15))

        # --- Form ---
        form = ttk.Frame(main)
        form.pack(fill="x")

        # Projektname
        ttk.Label(form, text="Projektname:").grid(row=0, column=0, sticky="w", pady=4)
        self.name_var = tk.StringVar()
        self.name_entry = ttk.Entry(form, textvariable=self.name_var, width=40)
        self.name_entry.grid(row=0, column=1, columnspan=2, sticky="ew", pady=4, padx=(10, 0))
        self.name_hint = ttk.Label(form, text="lowercase, kebab-case", foreground="gray")
        self.name_hint.grid(row=1, column=1, sticky="w", padx=(10, 0))

        # Stack
        ttk.Label(form, text="Stack:").grid(row=2, column=0, sticky="w", pady=4)
        self.stack_var = tk.StringVar(value="generic")
        stack_combo = ttk.Combobox(
            form, textvariable=self.stack_var, values=STACK_OPTIONS,
            state="readonly", width=37
        )
        stack_combo.grid(row=2, column=1, columnspan=2, sticky="ew", pady=4, padx=(10, 0))

        # Beschreibung
        ttk.Label(form, text="Beschreibung:").grid(row=3, column=0, sticky="w", pady=4)
        self.desc_var = tk.StringVar(value="Ein MightyDestroyer-Projekt")
        ttk.Entry(form, textvariable=self.desc_var, width=40).grid(
            row=3, column=1, columnspan=2, sticky="ew", pady=4, padx=(10, 0)
        )

        # Zielordner
        ttk.Label(form, text="Zielordner:").grid(row=4, column=0, sticky="w", pady=4)
        self.target_var = tk.StringVar(value=DEFAULT_TARGET_DIR)
        ttk.Entry(form, textvariable=self.target_var, width=32).grid(
            row=4, column=1, sticky="ew", pady=4, padx=(10, 0)
        )
        ttk.Button(form, text="...", width=3, command=self._browse_target).grid(
            row=4, column=2, pady=4, padx=(5, 0)
        )

        form.columnconfigure(1, weight=1)

        # --- GitHub ---
        ttk.Separator(main, orient="horizontal").pack(fill="x", pady=(15, 10))

        gh_frame = ttk.Frame(main)
        gh_frame.pack(fill="x")

        self.github_var = tk.BooleanVar(value=False)
        self.gh_check = ttk.Checkbutton(
            gh_frame, text="GitHub-Repo erstellen", variable=self.github_var,
            command=self._toggle_github
        )
        self.gh_check.grid(row=0, column=0, columnspan=3, sticky="w", pady=4)

        ttk.Label(gh_frame, text="Organisation:").grid(row=1, column=0, sticky="w", pady=4)
        self.org_var = tk.StringVar(value=DEFAULT_ORG)
        self.org_entry = ttk.Entry(gh_frame, textvariable=self.org_var, width=30, state="disabled")
        self.org_entry.grid(row=1, column=1, columnspan=2, sticky="ew", pady=4, padx=(10, 0))

        self.visibility_var = tk.StringVar(value="private")
        self.radio_private = ttk.Radiobutton(
            gh_frame, text="Private", variable=self.visibility_var,
            value="private", state="disabled"
        )
        self.radio_private.grid(row=2, column=1, sticky="w", padx=(10, 0))
        self.radio_public = ttk.Radiobutton(
            gh_frame, text="Public", variable=self.visibility_var,
            value="public", state="disabled"
        )
        self.radio_public.grid(row=2, column=2, sticky="w")

        self.gh_status = ttk.Label(gh_frame, text="", foreground="gray")
        self.gh_status.grid(row=3, column=0, columnspan=3, sticky="w", pady=(2, 0))

        gh_frame.columnconfigure(1, weight=1)

        # --- Button ---
        ttk.Separator(main, orient="horizontal").pack(fill="x", pady=(15, 10))

        btn_frame = ttk.Frame(main)
        btn_frame.pack(fill="x")

        self.create_btn = ttk.Button(
            btn_frame, text="Projekt erstellen", command=self._on_create
        )
        self.create_btn.pack(side="left")

        self.open_btn = ttk.Button(
            btn_frame, text="Ordner öffnen", command=self._open_folder, state="disabled"
        )
        self.open_btn.pack(side="left", padx=(10, 0))

        self.update_tpl_btn = ttk.Button(
            btn_frame, text="Templates aktualisieren", command=self._on_update_templates
        )
        self.update_tpl_btn.pack(side="right")

        # --- Log ---
        ttk.Separator(main, orient="horizontal").pack(fill="x", pady=(10, 5))
        ttk.Label(main, text="Log:", font=("Segoe UI", 9, "bold")).pack(anchor="w")

        log_frame = ttk.Frame(main)
        log_frame.pack(fill="both", expand=True, pady=(2, 0))

        self.log_text = tk.Text(
            log_frame, height=10, font=("Consolas", 9),
            state="disabled", wrap="word", bg="#1e1e1e", fg="#d4d4d4",
            insertbackground="#d4d4d4", relief="flat", bd=1
        )
        scrollbar = ttk.Scrollbar(log_frame, orient="vertical", command=self.log_text.yview)
        self.log_text.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")
        self.log_text.pack(fill="both", expand=True)

        self.result_project_dir = None

    def _check_prerequisites(self):
        if not check_git_available():
            self._log("WARNUNG: Git nicht gefunden. Bitte installiere Git.")
        else:
            self._log("Git: OK")

        if check_gh_available():
            self._log("GitHub CLI (gh): OK — eingeloggt")
        else:
            self._log("GitHub CLI (gh): Nicht verfuegbar (optional)")

        tpl_dir = get_templates_dir()
        cache_dir = get_cache_dir()
        if tpl_dir == cache_dir:
            self._log("Templates: Aus Cache (aktualisiert)")
        else:
            self._log("Templates: Eingebettet (Standard)")

        self._log("")

    def _toggle_github(self):
        state = "normal" if self.github_var.get() else "disabled"
        self.org_entry.configure(state=state)
        self.radio_private.configure(state=state)
        self.radio_public.configure(state=state)

        if self.github_var.get() and not check_gh_available():
            self.gh_status.configure(
                text="gh CLI nicht eingeloggt — GitHub-Erstellung wird fehlschlagen.",
                foreground="red",
            )
        else:
            self.gh_status.configure(text="", foreground="gray")

    def _browse_target(self):
        path = filedialog.askdirectory(initialdir=self.target_var.get())
        if path:
            self.target_var.set(path)

    def _log(self, message: str):
        self.log_text.configure(state="normal")
        self.log_text.insert("end", message + "\n")
        self.log_text.see("end")
        self.log_text.configure(state="disabled")
        self.root.update_idletasks()

    def _on_create(self):
        if self.running:
            return

        name = self.name_var.get().strip()
        logger.info(
            "Project creation started",
            extra={"action": "project_creation_started", "project_name": name},
        )
        error = validate_project_name(name)
        if error:
            messagebox.showerror("Ungültiger Projektname", error)
            self.name_entry.focus_set()
            return

        target = self.target_var.get().strip()
        if not target or not os.path.isdir(target):
            messagebox.showerror("Ungültiger Zielordner", f"Verzeichnis existiert nicht: {target}")
            return

        project_path = os.path.join(target, name)
        if os.path.exists(project_path):
            messagebox.showerror("Existiert bereits", f"Verzeichnis existiert bereits:\n{project_path}")
            return

        self.running = True
        self.create_btn.configure(state="disabled")

        thread = threading.Thread(target=self._run_bootstrap, daemon=True)
        thread.start()

    def _run_bootstrap(self):
        try:
            project_dir = bootstrap_project(
                name=self.name_var.get().strip(),
                stack=self.stack_var.get(),
                description=self.desc_var.get().strip(),
                target_parent=self.target_var.get().strip(),
                create_github=self.github_var.get(),
                github_org=self.org_var.get().strip(),
                github_private=(self.visibility_var.get() == "private"),
                log=lambda msg: self.root.after(0, self._log, msg),
            )
            self.result_project_dir = project_dir
            self.root.after(0, self._on_success)
        except Exception as e:
            self.root.after(0, self._log, f"\nFEHLER: {e}")
            self.root.after(0, self._on_error, str(e))

    def _on_success(self):
        self.running = False
        self.create_btn.configure(state="normal")
        self.open_btn.configure(state="normal")
        logger.info(
            "Project creation completed",
            extra={"action": "project_creation_completed", "project_dir": self.result_project_dir},
        )
        messagebox.showinfo("Fertig!", f"Projekt erstellt:\n{self.result_project_dir}")

    def _on_error(self, msg: str):
        self.running = False
        self.create_btn.configure(state="normal")
        logger.error(
            "Project creation failed",
            extra={"action": "project_creation_failed", "error": msg},
        )
        messagebox.showerror("Fehler", msg)

    def _open_folder(self):
        if self.result_project_dir and os.path.isdir(self.result_project_dir):
            if sys.platform == "win32":
                os.startfile(self.result_project_dir)
            elif sys.platform == "darwin":
                os.system(f'open "{self.result_project_dir}"')
            else:
                os.system(f'xdg-open "{self.result_project_dir}"')

    def _on_update_templates(self):
        if self.running:
            return
        self.running = True
        self.update_tpl_btn.configure(state="disabled")
        thread = threading.Thread(target=self._run_update_templates, daemon=True)
        thread.start()

    def _run_update_templates(self):
        try:
            success = update_templates(
                log=lambda msg: self.root.after(0, self._log, msg)
            )
            if success:
                logger.info(
                    "Templates updated",
                    extra={"action": "templates_updated", "success": True},
                )
                self.root.after(0, self._log, "Templates-Quelle: Cache (aktualisiert)\n")
            else:
                logger.warning(
                    "Templates update partial failure",
                    extra={"action": "templates_updated", "success": False},
                )
        except Exception as e:
            logger.error(
                "Templates update failed",
                extra={"action": "templates_update_failed", "error": str(e)},
            )
            self.root.after(0, self._log, f"FEHLER beim Template-Update: {e}\n")
        finally:
            self.running = False
            self.root.after(0, lambda: self.update_tpl_btn.configure(state="normal"))


def main():
    setup_logging()
    root = tk.Tk()
    root.iconname("MightyDestroyer Bootstrap")
    BootstrapApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
