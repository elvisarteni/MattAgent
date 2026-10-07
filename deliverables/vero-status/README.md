# Vero Status

Double-click **Vero Status** and a dashboard opens in your browser showing:

- **Is Vero available?** Big green or red status, since when, and the reason if not.
- **Which model does Vero use?** The model Vero is configured with (`vero config`), and the model that answered the last check.
- The Vero CLI version, how long the last answer took, availability over the last 24 h, and the last checks.
- **Vero open now:** when you have a Vero CLI open, or are using Vero in VS Code, the model in use right now.
- **Your Vero sessions: response time:** how long the model takes to start answering in *your* CLI and VS Code
  sessions (median and p95 for the last hour, 24 h median, last 40 requests as bars).

Buttons: **Check now**, **Settings** (how often to check, which model to use for the check, Vero location), **Quit**.

Jira ASPF-1578 · Version 4.3.0 · Python 3.8+ standard library only, no install, no command window.

## Use it

1. Put the folder somewhere fixed, e.g. `C:\Tools\vero-status`.
2. Double-click **`Vero Status.pyw`**. The dashboard opens at http://127.0.0.1:8767.
3. Optional: right-click `Vero Status.pyw` and choose *Send to > Desktop (create shortcut)*.
   To start it with Windows, put that shortcut in the folder that opens with `Win+R` -> `shell:startup`.

Double-clicking again while it runs just opens the dashboard. **Quit** stops it.

## Team server (one page for everyone, no login)

Run it once on a server (or any always-on PC) and share one link. Everyone opens it in the browser, no login,
no registration, nothing to install on their laptops. One check serves the whole team.

```
python vero_status_server.py                 # port 8767, all network interfaces
python vero_status_server.py --port 8080     # another port
```

It prints (and writes to `data/vero-status.log`):

- **Share link** `http://<server>:8767/`: anyone can see whether Vero is available, its model, 24 h availability,
  and **Recent activity** (the last 10 checks: time, result, model, answer time, who started it).
  Viewers can press **Check now** at most once every 5 minutes (shared for everyone).
- **Admin link** `http://<server>:8767/?admin=<key>`: also shows **Settings**. Keep it private. The key is in
  `data/admin_key.txt`; delete that file and restart to get a new one. The key is removed from the address bar after opening.

There is no Quit button and the personal panels (*Vero open now*, *your sessions*) are off: they only make sense on
your own laptop, so keep using `Vero Status.pyw` locally for those.

**Windows server, start with the machine:** Task Scheduler > Create Task > *Run whether user is logged on or not*,
trigger *At startup*, action `pythonw.exe` with arguments `vero_status_server.py` and *Start in* the folder.
Run it as the functional account that is signed in to Vero (`vero auth`). Open the port once (admin PowerShell):

```
New-NetFirewallRule -DisplayName "Vero Status" -Direction Inbound -LocalPort 8767 -Protocol TCP -Action Allow
```

**Linux:** a systemd service with `ExecStart=/usr/bin/python3 /opt/vero-status/vero_status_server.py` and `Restart=always`.

Plain HTTP is fine on the intranet (the page holds no secrets); put IIS or nginx in front for HTTPS.
Record the host, the functional account and the link in the SCMP (`servers.md`, `functional-accounts.md`, `publishing.md`).

## On a Linux VM (no desktop)

```
bash scripts/install_vm.sh            # personal: 127.0.0.1, your own sessions; starts with the VM
bash scripts/install_vm.sh team       # team server on all interfaces (port must be open to the VM)
bash scripts/install_vm.sh status     # or: uninstall
```

Open it from your laptop through VS Code port forwarding (PORTS tab, port 8767) or
`ssh -N -L 8767:127.0.0.1:8767 <user>@<vm-host>`. It uses a systemd user service (or crontab @reboot), needs no sudo,
and copies your PATH and proxy settings for the service. To keep it running after a reboot without a login, the VM admin
runs `sudo loginctl enable-linger <user>` once. Unzip with `python3 -m zipfile -e <zip> .` if `unzip` is missing.

## How a check works

1. `vero version`: is Vero installed?
2. `vero config`: which model and provider Vero is set to (free).
3. `vero task --json -t 120 -c <empty folder> -m <check model> "Reply with exactly: OK"`.
   Vero is **available** when the `completion_result` answer arrives. This costs 2 small model calls and takes about 1 minute.
   The check model defaults to the cheap Haiku 4.5; leave it empty in Settings to test Vero's own model.

The checks never use `--yolo`, run in an empty folder, and never store answers or secrets.
The data lives in the program's `data/` folder (`settings.json`, `history.json`, `vero-status.log`).

## How your own sessions are measured

Vero writes every task's events to `ui_messages.json`: for the CLI in `%USERPROFILE%\.vero\data\tasks\<id>\`,
for VS Code in the extension's storage (`%APPDATA%\Code\User\globalStorage\<vero extension>\tasks\<id>\`).
Each model request starts with an `api_req_started` event; the next event is the model's first response.
The difference is the response time, using Vero's own timestamps. A running `vero` / `node …vero…` process
means the CLI is open. Only timestamps, event kinds, model names and token counts are read, never your prompts
or answers, and nothing is changed. The dashboard's own test questions are left out. Switch it off in Settings.

## Try it without Vero

In Settings, set *Vero CLI location* to `scripts\vero.cmd` (Windows) or `scripts/vero` (Linux/macOS; run `chmod +x scripts/vero` once): a fake Vero that answers like the real one.

## Develop

```
python -m unittest discover -s tests -t .      # 54 tests, fake Vero only
uvx ruff check . && uvx ruff format --check .  # lint + format
uvx mypy && uvx mypy --platform win32          # strict typing
uv run --no-project --with reportlab python scripts/build_source_pdf.py   # source as PDF for rebuild
```
