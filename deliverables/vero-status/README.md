# Vero Status

Double-click **Vero Status** and a dashboard opens in your browser showing:

- **Is Vero available?** Big green or red status, since when, and the reason if not.
- **Which model does Vero use?** The model Vero is configured with (`vero config`), and the model that answered the last check.
- The Vero CLI version, how long the last answer took, availability over the last 24 h, and the last checks.

Buttons: **Check now**, **Settings** (how often to check, which model to use for the check, Vero location), **Quit**.

Jira ASPF-1578 · Version 4.0.0 · Python 3.8+ standard library only, no install, no command window.

## Use it

1. Put the folder somewhere fixed, e.g. `C:\Tools\vero-status`.
2. Double-click **`Vero Status.pyw`**. The dashboard opens at http://127.0.0.1:8767.
3. Optional: right-click `Vero Status.pyw` and choose *Send to > Desktop (create shortcut)*.
   To start it with Windows, put that shortcut in the folder that opens with `Win+R` -> `shell:startup`.

Double-clicking again while it runs just opens the dashboard. **Quit** stops it.

## How a check works

1. `vero version`: is Vero installed?
2. `vero config`: which model and provider Vero is set to (free).
3. `vero task --json -t 120 -c <empty folder> -m <check model> "Reply with exactly: OK"`.
   Vero is **available** when the `completion_result` answer arrives. This costs 2 small model calls and takes about 1 minute.
   The check model defaults to the cheap Haiku 4.5; leave it empty in Settings to test Vero's own model.

The checks never use `--yolo`, run in an empty folder, and never store answers or secrets.
The data lives in the program's `data/` folder (`settings.json`, `history.json`, `vero-status.log`).

## Try it without Vero

In Settings, set *Vero CLI location* to `scripts\vero.cmd` (Windows) or `scripts/vero` (Linux/macOS; run `chmod +x scripts/vero` once): a fake Vero that answers like the real one.

## Develop

```
python -m unittest discover -s tests -t .      # 30 tests, fake Vero only
uvx ruff check . && uvx ruff format --check .  # lint + format
uvx mypy && uvx mypy --platform win32          # strict typing
uv run --no-project --with reportlab python scripts/build_source_pdf.py   # source as PDF for rebuild
```
