#!/usr/bin/env python3
"""Build dist/vero-latency-monitor-<version>.zip (no data, no local config, no caches)."""
import sys
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from vero_latency import __version__  # noqa: E402

SKIP_DIRS = {"data", "reports", "dist", "__pycache__", ".pytest_cache", ".venv", "venv", ".git"}
SKIP_FILES = {"config/monitor.json"}

name = f"vero-latency-monitor-{__version__}"
out = ROOT / "dist" / f"{name}.zip"
out.parent.mkdir(exist_ok=True)
n = 0
with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as z:
    for f in sorted(ROOT.rglob("*")):
        rel = f.relative_to(ROOT)
        if f.is_dir() or SKIP_DIRS & set(rel.parts) or rel.as_posix() in SKIP_FILES or f.suffix in (".pyc", ".log"):
            continue
        z.write(f, f"{name}/{rel.as_posix()}")
        n += 1
print(f"wrote {out} ({n} files, {out.stat().st_size // 1024} KB)")
