"""Build-Script fuer MightyDestroyer Governance Bootstrap GUI.

Nutzt PyInstaller um eine standalone .exe zu erstellen.
"""

import os
import sys
import subprocess


def build():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    templates_dir = os.path.join(script_dir, "templates")
    main_script = os.path.join(script_dir, "bootstrap_gui.py")

    separator = ";" if sys.platform == "win32" else ":"

    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--onefile",
        "--windowed",
        "--name", "MightyDestroyer-Bootstrap",
        f"--add-data={templates_dir}{separator}templates",
        "--distpath", os.path.join(script_dir, "dist"),
        "--workpath", os.path.join(script_dir, "build"),
        "--specpath", script_dir,
        "--clean",
        main_script,
    ]

    print("Building MightyDestroyer Bootstrap GUI...")
    print(f"Command: {' '.join(cmd)}")
    print()

    result = subprocess.run(cmd, cwd=script_dir)

    if result.returncode == 0:
        exe_name = "MightyDestroyer-Bootstrap.exe" if sys.platform == "win32" else "MightyDestroyer-Bootstrap"
        exe_path = os.path.join(script_dir, "dist", exe_name)
        print()
        print(f"Build erfolgreich!")
        print(f"Executable: {exe_path}")
        print(f"Groesse: {os.path.getsize(exe_path) / 1024 / 1024:.1f} MB")
    else:
        print()
        print("Build fehlgeschlagen!")
        sys.exit(1)


if __name__ == "__main__":
    build()
