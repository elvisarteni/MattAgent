#!/usr/bin/env python3
"""Build dist/VeroAvailabilityMonitor_<version>_REBUILD.md: the complete source as one Markdown document.

For channels that accept no archives and no scripts. Every file is a readable fenced code block;
an AI assistant (or a person) recreates the folder from it and checks each file with SHA-256.
The HTML guide is left out (it is sent as its own file); everything else is included."""

import hashlib
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from vero_monitor import __version__  # noqa: E402

SKIP_DIRS = {
    "data",
    "data-demo",
    "reports",
    "dist",
    "__pycache__",
    ".pytest_cache",
    ".mypy_cache",
    ".ruff_cache",
    ".venv",
    "venv",
    ".git",
}
SKIP_FILES = {"config/monitor.json", "docs/VeroAvailabilityMonitor_Guide.html"}
CRLF_SUFFIXES = (".bat",)
CRLF_FILES = {"START_HERE.txt"}
LANG = {".py": "python", ".json": "json", ".md": "markdown", ".html": "html", ".bat": "bat", ".toml": "toml", ".txt": "text"}


def lf_sha(text: str) -> str:
    return hashlib.sha256(text.replace("\r\n", "\n").encode("utf-8")).hexdigest()


def fence_for(text: str) -> str:
    longest = max((len(m) for m in re.findall(r"`+", text)), default=0)
    return "`" * max(4, longest + 1)


def files():
    for f in sorted(ROOT.rglob("*")):
        rel = f.relative_to(ROOT)
        if f.is_dir() or SKIP_DIRS & set(rel.parts) or rel.as_posix() in SKIP_FILES or f.suffix in (".pyc", ".log"):
            continue
        yield rel.as_posix(), f.read_bytes().decode("utf-8")


VERIFY = r"""import hashlib, json, pathlib, re, sys
root = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else "vero-availability-monitor")
md = pathlib.Path(sys.argv[2] if len(sys.argv) > 2 else "REBUILD.md").read_text(encoding="utf-8")
manifest = json.loads(re.search(r"<!-- MANIFEST\n(.*?)\n-->", md, re.S).group(1))
bad = 0
for path, info in manifest["files"].items():
    p = root / path
    if not p.exists():
        print("MISSING ", path); bad += 1; continue
    text = p.read_bytes().decode("utf-8").replace("\r\n", "\n")
    if hashlib.sha256(text.encode("utf-8")).hexdigest() != info["sha256_lf"]:
        print("DIFFERENT", path); bad += 1
    elif info["crlf"] and b"\r\n" not in p.read_bytes():
        p.write_bytes(text.replace("\n", "\r\n").encode("utf-8")); print("fixed CRLF", path)
print("OK: all files match" if not bad else f"{bad} file(s) wrong: recreate them from the document")
sys.exit(1 if bad else 0)
"""


def main() -> None:
    items = list(files())
    manifest = {
        "version": __version__,
        "files": {
            p: {"sha256_lf": lf_sha(t), "crlf": p.endswith(CRLF_SUFFIXES) or p in CRLF_FILES, "bytes": len(t.encode("utf-8"))}
            for p, t in items
        },
    }
    out = ROOT / "dist" / f"VeroAvailabilityMonitor_{__version__}_REBUILD.md"
    out.parent.mkdir(exist_ok=True)
    w = []
    w.append(f"""# Vero Availability Monitor {__version__}: complete source for rebuild

**What this is.** The full source of the Vero Availability Monitor (Jira ASPF-1578), a local tool that checks
whether Vero (CLI, optionally Chat) is available and shows it on a status page. It is sent as a readable document because archives
and scripts cannot be attached. Nothing in it runs by itself. Read it before rebuilding.

- {len(items)} files, all plain text, Python 3.8+ standard library only (no downloads, no pip).
- The HTML guide `VeroAvailabilityMonitor_Guide.html` is sent separately; put it in `docs/`.
- `VERO_CONTEXT.md` (included below) explains the architecture, contracts and rules.

---

## Instructions for the AI assistant (Vero CLI or other)

You are asked to recreate a project folder **exactly** from this document.

1. Create the folder `vero-availability-monitor/` in the location the user gives you (default: `C:\\Tools\\`).
2. For **every** section below that starts with `### FILE:`, create that file at that relative path,
   with the content of the code block that follows, **byte for byte**:
   - do not reformat, re-indent, translate, "improve", summarise or skip anything;
   - copy only the lines *between* the opening and closing fence (the fence is 4 or more backticks);
   - keep a trailing newline at the end of each file, exactly as in the block;
   - encoding UTF-8 without BOM.
3. Line endings: LF for every file, **except** those marked `CRLF` in the table (the `.bat` files and
   `START_HERE.txt`), which must use CRLF (Windows).
4. Create empty folders if needed: `data/` is **not** needed (the tool creates it).
5. Verify: save the Python block in the section *Verify the rebuild* as `verify_rebuild.py` next to this
   document (outside the project folder), then run
   `py verify_rebuild.py C:\\Tools\\vero-availability-monitor VeroAvailabilityMonitor_{__version__}_REBUILD.md`.
   It checks every file against its SHA-256 (computed on LF line endings) and fixes CRLF where needed.
   If it reports `DIFFERENT` or `MISSING`, recreate those files again from this document.
6. Then run the tests: `py -m unittest discover -s tests -t .` inside the folder. Expected: `OK` (64 tests, about 10 s).
7. Report the result to the user, then tell them to double-click `setup.bat` (see `START_HERE.txt`).

Do not run `setup.bat`, `install`, `doctor`, `check` or the real Vero CLI yourself unless the user asks.

---

## File list

| # | Path | Bytes | Line endings | SHA-256 (LF) |
|---|------|------:|:---:|---|
""")
    for i, (p, _text) in enumerate(items, 1):
        m = manifest["files"][p]
        w.append(f"| {i} | `{p}` | {m['bytes']} | {'CRLF' if m['crlf'] else 'LF'} | `{m['sha256_lf'][:16]}…` |\n")
    w.append("\n---\n\n## Files\n\n")
    for p, t in items:
        text = t.replace("\r\n", "\n")
        f = fence_for(text)
        lang = LANG.get(Path(p).suffix, "") if not p.endswith(("CODEOWNERS", ".gitignore", ".gitattributes")) else "text"
        body = text if text.endswith("\n") else text + "\n"
        w.append(f"### FILE: `{p}`\n\n{f}{lang}\n{body}{f}\n\n")
    w.append("---\n\n## Verify the rebuild\n\n")
    w.append("Save as `verify_rebuild.py` (outside the project folder) and run it as described in step 5.\n\n")
    w.append(f"````python\n{VERIFY}````\n\n")
    w.append("<!-- MANIFEST\n" + json.dumps(manifest, indent=1) + "\n-->\n")
    out.write_text("".join(w), encoding="utf-8", newline="\n")
    print(f"wrote {out} ({len(items)} files, {out.stat().st_size // 1024} KB)")


if __name__ == "__main__":
    main()
