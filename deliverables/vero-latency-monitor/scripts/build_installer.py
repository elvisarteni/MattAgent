#!/usr/bin/env python3
"""Build dist/vero_latency_monitor_setup_<version>.py: ONE plain-text Python file that
recreates the whole tool folder. For channels that do not accept .zip attachments.

The output contains every file as a readable string literal plus its SHA-256, so it can be
reviewed before running. Same file selection as build_zip.py (no data, no local config)."""
import hashlib
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from vero_latency import __version__  # noqa: E402

SKIP_DIRS = {"data", "data-demo", "reports", "dist", "__pycache__", ".pytest_cache", ".venv", "venv", ".git"}
SKIP_FILES = {"config/monitor.json"}

HEADER = '''#!/usr/bin/env python3
"""Vero Latency Monitor {version} (ASPF-1578): single-file installer.

Recreates the tool folder from the files embedded below (plain text, readable, SHA-256 checked).
Needs Python 3.8+ only. Nothing is downloaded, nothing is installed system-wide.

    py vero_latency_monitor_setup_{version}.py                 -> .\\vero-latency-monitor
    py vero_latency_monitor_setup_{version}.py C:\\Tools        -> C:\\Tools\\vero-latency-monitor
    py vero_latency_monitor_setup_{version}.py --list          -> show the files, write nothing

Existing config/monitor.json and data/ are never touched (they are not in this file),
so the same command also updates an existing install.
Then open the folder and double-click setup.bat (see START_HERE.txt).
"""
import hashlib
import sys
from pathlib import Path

VERSION = "{version}"
FOLDER = "vero-latency-monitor"

FILES = {{
'''

FOOTER = '''}


def main(argv):
    if "--list" in argv:
        for rel, (sha, text) in FILES.items():
            print(f"{len(text.encode('utf-8')):>9}  {rel}")
        print(f"{len(FILES)} files, version {VERSION}")
        return 0
    args = [a for a in argv if not a.startswith("-")]
    base = Path(args[0]) if args else Path.cwd()
    target = base / FOLDER
    for rel, (sha, text) in FILES.items():
        data = text.encode("utf-8")
        if hashlib.sha256(data).hexdigest() != sha:
            print(f"checksum mismatch for {rel}: this installer file was changed or damaged. Nothing written.")
            return 1
    for rel, (sha, text) in FILES.items():
        p = target / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_bytes(text.encode("utf-8"))
    print(f"Vero Latency Monitor {VERSION}: {len(FILES)} files written to {target}")
    print("Next: open that folder and double-click setup.bat (or setup_demo.bat to see the demo).")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
'''


def main() -> None:
    out = ROOT / "dist" / f"vero_latency_monitor_setup_{__version__}.py"
    out.parent.mkdir(exist_ok=True)
    parts = [HEADER.format(version=__version__)]
    n = 0
    for f in sorted(ROOT.rglob("*")):
        rel = f.relative_to(ROOT)
        if f.is_dir() or SKIP_DIRS & set(rel.parts) or rel.as_posix() in SKIP_FILES or f.suffix in (".pyc", ".log"):
            continue
        data = f.read_bytes()
        text = data.decode("utf-8")  # all project files are text
        parts.append(f"    {rel.as_posix()!r}: ({hashlib.sha256(data).hexdigest()!r},\n        {text!r}),\n")
        n += 1
    parts.append(FOOTER)
    out.write_text("".join(parts), encoding="utf-8", newline="\n")
    print(f"wrote {out} ({n} files, {out.stat().st_size // 1024} KB)")


if __name__ == "__main__":
    main()
