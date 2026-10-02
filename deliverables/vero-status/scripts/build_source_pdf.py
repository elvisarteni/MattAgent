#!/usr/bin/env python3
"""Build dist/Vero_Status_<version>_Source.pdf: the complete source as a PDF document.

For channels that accept only documents. Developer tool (needs reportlab):
    uv run --no-project --with reportlab python scripts/build_source_pdf.py

Listing format (survives PDF text extraction, which drops blank lines and collapses spaces):
    "  12 | content"   line 12 of the file; every MARK (U+2423, open box) in content is one space
                       (used for leading spaces, runs of 2+ spaces and spaces at a row edge)
    "  12 |"           line 12 is empty
    "     + more"      continuation of the previous line (joined with nothing in between)
The MARK character never appears in the sources (checked at build time).
"""

import hashlib
import re
import sys
from pathlib import Path

from reportlab.lib.pagesizes import A4, landscape
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from vero_status import __version__  # noqa: E402

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
}
SKIP_SUFFIXES = (".pyc", ".log", ".egg-info")
SKIP_FILES = {"docs/Vero_Status_Guide.html"}
CRLF = (".bat", ".cmd")
CRLF_FILES = {"START_HERE.txt"}
FONT_PATHS = ["/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf", "C:/Windows/Fonts/consola.ttf"]
SIZE, LEADING, MARGIN = 6.4, 7.7, 28
PAGE_W, PAGE_H = landscape(A4)
MARK = "\u2423"  # open box, shown for a space that extraction could lose


def files():
    for f in sorted(ROOT.rglob("*")):
        rel = f.relative_to(ROOT)
        if (
            f.is_dir()
            or SKIP_DIRS & set(rel.parts)
            or any(part.endswith(SKIP_SUFFIXES) for part in rel.parts)
            or rel.as_posix() in SKIP_FILES
        ):
            continue
        yield rel.as_posix(), f.read_bytes().decode("utf-8").replace("\r\n", "\n")


def lf_sha(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def protect(chunk: str) -> str:
    """Mark every space an extractor could drop: leading, trailing, and runs of 2+."""
    chunk = re.sub(r" {2,}", lambda m: MARK * len(m.group()), chunk)
    if chunk.startswith(" "):
        chunk = MARK + chunk[1:]
    if chunk.endswith(" "):
        chunk = chunk[:-1] + MARK
    return chunk


def encode(lines, width):
    """Source lines -> listing rows (see module docstring)."""
    rows = []
    for n, line in enumerate(lines, 1):
        head = f"{n:>4} |"
        if not line:
            rows.append(head)
            continue
        chunks = [line[i : i + width] for i in range(0, len(line), width)]
        rows.append(f"{head} {protect(chunks[0])}")
        rows.extend(f"     + {protect(c)}" for c in chunks[1:])
    return rows


VERIFY_TEMPLATE = """import hashlib, pathlib, sys
# usage: py verify_rebuild.py C:\\Tools\\vero-status
root = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else "vero-status")
CRLF = {crlf!r}
FILES = {{
{entries}}}
bad = 0
for path, sha in FILES.items():
    p = root / path
    if not p.exists():
        print("MISSING  ", path); bad += 1; continue
    text = p.read_bytes().decode("utf-8").replace("\\r\\n", "\\n")
    if hashlib.sha256(text.encode("utf-8")).hexdigest() != sha:
        print("DIFFERENT", path); bad += 1; continue
    want = text.replace("\\n", "\\r\\n") if path in CRLF else text
    if p.read_bytes() != want.encode("utf-8"):
        p.write_bytes(want.encode("utf-8")); print("fixed line endings", path)
print("OK: all files match" if not bad else str(bad) + " file(s) wrong: recreate them from the document")
sys.exit(1 if bad else 0)
"""


class Doc:
    def __init__(self, path: Path, font: str):
        self.c = canvas.Canvas(str(path), pagesize=(PAGE_W, PAGE_H))
        self.c.setTitle(f"Vero Status {__version__} - complete source for rebuild")
        self.c.setAuthor("Quality AI Automation (ASPF-1578)")
        self.c.setSubject("Source listing. A document only: nothing in it runs.")
        self.font = font
        self.page = 0
        self.y = 0.0
        self.new_page()

    def new_page(self):
        if self.page:
            self.c.showPage()
        self.page += 1
        self.c.setFont(self.font, 6)
        self.c.setFillGray(0.45)
        self.c.drawString(MARGIN, PAGE_H - 16, f"Vero Status {__version__} · source for rebuild · ASPF-1578")
        self.c.drawRightString(PAGE_W - MARGIN, 12, f"page {self.page}")
        self.c.setFillGray(0)
        self.y = PAGE_H - MARGIN - 8

    def row(self, text: str, size: float = SIZE, gray: float = 0):
        if self.y < MARGIN:
            self.new_page()
        self.c.setFont(self.font, size)
        self.c.setFillGray(gray)
        self.c.drawString(MARGIN, self.y, text)
        self.y -= max(LEADING, size * 1.25)

    def gap(self, n: float = 1):
        self.y -= LEADING * n

    def save(self):
        self.c.save()


def main() -> None:
    font_path = next((p for p in FONT_PATHS if Path(p).exists()), None)
    if not font_path:
        sys.exit("no monospace TTF font found (DejaVu Sans Mono or Consolas)")
    pdfmetrics.registerFont(TTFont("Mono", font_path))
    char_w = pdfmetrics.stringWidth("M", "Mono", SIZE)
    width = int((PAGE_W - 2 * MARGIN) / char_w) - 8  # minus the "NNNN | " gutter
    items = list(files())
    bad = [p for p, t in items if MARK in t]
    if bad:
        sys.exit(f"MARK character found in {bad}: the listing would be ambiguous")
    crlf = sorted(p for p, _ in items if p.endswith(CRLF) or p in CRLF_FILES)
    out = ROOT / "dist" / f"Vero_Status_{__version__}_Source.pdf"
    out.parent.mkdir(exist_ok=True)
    d = Doc(out, "Mono")

    d.row(f"VERO STATUS {__version__} - COMPLETE SOURCE FOR REBUILD", 13)
    d.row("Jira ASPF-1578 · Quality AI Automation · a document only: nothing in it runs", 8, 0.35)
    d.gap()
    intro = f"""\
What this is: the full source ({len(items)} text files) of "Vero Status", a small program that shows in the browser whether
Vero is available and which model it uses. Python 3.8+ standard library only. The guide PDF is sent separately.

INSTRUCTIONS FOR THE AI ASSISTANT (Vero CLI or other) - recreate the project folder EXACTLY:
 1. Create the folder vero-status in the location the user gives (default C:\\Tools\\).
 2. Every file starts with a row  "=== FILE: <path> (<n> lines) ===" and ends with  "=== END FILE: <path> ===".
 3. Rows between them encode the file, one source line per numbered row:
      "  12 | content"  -> line 12. Every {MARK} (open box) in the content is ONE SPACE. It marks leading
                           spaces, runs of 2+ spaces and spaces at a row edge; single spaces between words
                           are printed normally. The {MARK} character never occurs in the real files.
      "  12 |"          -> line 12 is an empty line.
      "     + more"     -> continuation of the previous line: append "more" directly (no space, no newline).
    Ignore page headers/footers ("Vero Status ... source for rebuild", "page N").
    Line numbers must run 1..n without gaps; n is in the FILE row. Every file ends with a newline.
 4. Write files as UTF-8 without BOM, LF line endings. Do not reformat, translate, summarise or "fix" anything.
 5. Create verify_rebuild.py from the section VERIFY SCRIPT at the end (same row rules), OUTSIDE the project
    folder, and run:  py verify_rebuild.py C:\\Tools\\vero-status
    It checks every file's SHA-256 and sets CRLF line endings where Windows needs them (.cmd, START_HERE.txt).
    Recreate any file reported MISSING or DIFFERENT, then run it again until it prints "OK: all files match".
 6. Run the tests inside the folder:  py -m unittest discover -s tests -t .    Expected: OK (43 tests).
 7. Tell the user it is ready: double-click "Vero Status.pyw" to open the dashboard (see START_HERE.txt).
 Do not start the program or call the real Vero CLI unless the user asks.
"""
    for line in intro.splitlines():
        d.row(line, 7.2)
    d.gap()
    d.row("FILE LIST (path · lines · line endings · SHA-256 of the content with LF endings)", 7.2)
    for p, t in items:
        lines = t.split("\n")[:-1] if t.endswith("\n") else t.split("\n")
        d.row(f"  {p:<52} {len(lines):>5}  {'CRLF' if p in crlf else 'LF  '}  {lf_sha(t)}", 6.2)

    for p, t in items:
        lines = t.split("\n")[:-1] if t.endswith("\n") else t.split("\n")
        d.new_page()
        d.row(f"=== FILE: {p} ({len(lines)} lines) ===", 7.5)
        for r in encode(lines, width):
            d.row(r)
        d.row(f"=== END FILE: {p} ===", 7.5)

    entries = "".join(f"    {p!r}: {lf_sha(t)!r},\n" for p, t in items)
    verify = VERIFY_TEMPLATE.format(crlf=crlf, entries=entries)
    d.new_page()
    vlines = verify.split("\n")[:-1]
    d.row(f"=== VERIFY SCRIPT: verify_rebuild.py ({len(vlines)} lines) ===", 7.5)
    for r in encode(vlines, width):
        d.row(r)
    d.row("=== END VERIFY SCRIPT ===", 7.5)
    d.save()
    (ROOT / "dist" / "verify_rebuild.py").write_text(verify, encoding="utf-8")
    print(f"wrote {out} ({len(items)} files, {d.page} pages, {out.stat().st_size // 1024} KB, {width} chars per row)")


if __name__ == "__main__":
    main()
