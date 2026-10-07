#!/usr/bin/env bash
# Vero Status on a Linux VM (no desktop): run it in the background and start it with the machine.
#
#   scripts/install_vm.sh                 personal dashboard (127.0.0.1, with your own Vero sessions)
#   scripts/install_vm.sh team [PORT]     team server for colleagues (all interfaces, no login)
#   scripts/install_vm.sh status          is it running, and where
#   scripts/install_vm.sh uninstall       stop it and remove the autostart
#
# Uses a systemd user service when available, otherwise a crontab @reboot line. Needs no sudo.
# Open the page from your laptop with VS Code port forwarding (PORTS tab) or an SSH tunnel.
set -euo pipefail

DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
UNIT_DIR="${XDG_CONFIG_HOME:-$HOME/.config}/systemd/user"
UNIT="$UNIT_DIR/vero-status.service"
ENV_FILE="$DIR/data/service.env"
TAG="# vero-status autostart"
ACTION="${1:-personal}"
USER="${USER:-$(id -un)}"

say() { printf '%s\n' "$*"; }
die() { printf 'ERROR: %s\n' "$*" >&2; exit 1; }
have_systemd() { command -v systemctl >/dev/null && systemctl --user show-environment >/dev/null 2>&1; }

python_bin() {
  local py
  for py in python3 python; do
    if command -v "$py" >/dev/null && "$py" -c 'import sys; sys.exit(sys.version_info < (3, 8))' 2>/dev/null; then
      command -v "$py"; return 0
    fi
  done
  return 1
}

stop_background() {  # processes started by the crontab fallback
  pkill -f "$DIR/Vero Status.pyw" 2>/dev/null || true
  pkill -f "$DIR/vero_status_server.py" 2>/dev/null || true
}

uninstall() {
  if [ -f "$UNIT" ]; then
    systemctl --user disable --now vero-status.service 2>/dev/null || true
    rm -f "$UNIT"
    systemctl --user daemon-reload 2>/dev/null || true
    say "Removed the systemd user service."
  fi
  if command -v crontab >/dev/null && crontab -l 2>/dev/null | grep -qF "$TAG"; then
    crontab -l 2>/dev/null | grep -vF "$TAG" | crontab -
    say "Removed the crontab line."
  fi
  stop_background
  say "Vero Status is stopped. Your data/ folder (history, settings) is kept; delete the folder to remove everything."
}

write_env() {  # what the service needs from your shell: PATH (nvm, npm) and the proxy. Never AWS keys.
  mkdir -p "$DIR/data"
  chmod 700 "$DIR/data"
  local name value
  : > "$ENV_FILE"
  chmod 600 "$ENV_FILE"  # a proxy URL can contain a password
  for name in PATH HTTPS_PROXY HTTP_PROXY NO_PROXY https_proxy http_proxy no_proxy AWS_PROFILE AWS_REGION; do
    value="${!name:-}"
    [ -n "$value" ] || continue
    value="${value//\\/\\\\}"
    value="${value//\"/\\\"}"
    printf '%s="%s"\n' "$name" "$value" >> "$ENV_FILE"
  done
}

port_of() {  # personal: port from data/settings.json (default 8767)
  (cd "$DIR" && "$PY" -c 'from pathlib import Path; from vero_status.settings import load; print(load(Path("data/settings.json")).port)')
}

wait_healthy() {

  for _ in $(seq 1 20); do
    if "$PY" -c 'import sys, urllib.request; urllib.request.urlopen(f"http://127.0.0.1:{sys.argv[1]}/api/health", timeout=2)' "$1" 2>/dev/null; then
      return 0
    fi
    sleep 1
  done
  return 1
}

status() {
  PY="$(python_bin)" || die "Python 3.8+ not found"
  local port="${1:-$(port_of)}"
  if [ -f "$UNIT" ] && have_systemd; then
    systemctl --user --no-pager status vero-status.service | head -n 5 || true
  fi
  if wait_healthy "$port"; then say "Running on port $port."; else say "Not answering on port $port."; fi
}

case "$ACTION" in
  uninstall) uninstall; exit 0 ;;
  status) status "${2:-}"; exit 0 ;;
  personal | team) ;;
  *) die "unknown action '$ACTION' (use: personal, team [PORT], status, uninstall)" ;;
esac

case "$DIR" in *" "*) die "move the folder to a path without spaces (now: $DIR)" ;; esac
PY="$(python_bin)" || die "Python 3.8 or newer is needed (python3 not found)"
say "Python: $PY ($("$PY" --version 2>&1))"

VERO="$(cd "$DIR" && "$PY" -c 'from vero_status.vero import find_vero; print(find_vero() or "")')"
if [ -n "$VERO" ]; then
  say "Vero CLI: $VERO"
else
  say "WARNING: Vero CLI not found. Install it (npm), run 'vero auth', or set its path later in Settings."
fi

if [ "$ACTION" = team ]; then
  PORT="${2:-8767}"
  case "$PORT" in *[!0-9]*) die "port must be a number" ;; esac
  CMD=("$PY" "$DIR/vero_status_server.py" --port "$PORT")
else
  PORT="$(port_of)"
  CMD=("$PY" "$DIR/Vero Status.pyw")
fi

uninstall >/dev/null  # one autostart at a time
write_env

if have_systemd; then
  mkdir -p "$UNIT_DIR"
  EXEC=""
  for part in "${CMD[@]}"; do EXEC+="\"$part\" "; done
  cat > "$UNIT" <<EOF
[Unit]
Description=Vero Status ($ACTION) - ASPF-1578
After=network-online.target

[Service]
Type=simple
WorkingDirectory=$DIR
EnvironmentFile=$ENV_FILE
ExecStart=$EXEC
Restart=on-failure
RestartSec=30

[Install]
WantedBy=default.target
EOF
  systemctl --user daemon-reload
  systemctl --user enable --now vero-status.service
  say "Installed the systemd user service 'vero-status'."
  if [ "$(loginctl show-user "$USER" -p Linger --value 2>/dev/null || echo no)" != yes ]; then
    if loginctl enable-linger "$USER" 2>/dev/null; then
      say "Enabled lingering: it also runs when you are not logged in."
    else
      say "NOTE: it runs while you are logged in (a VS Code SSH window counts). To keep it running after reboots"
      say "      without a login, ask the VM admin once:  sudo loginctl enable-linger $USER"
    fi
  fi
elif command -v crontab >/dev/null; then
  LINE="@reboot cd \"$DIR\" && set -a && . \"$ENV_FILE\" && set +a && nohup ${CMD[*]@Q} >/dev/null 2>&1 & $TAG"
  { crontab -l 2>/dev/null || true; echo "$LINE"; } | crontab -
  # shellcheck source=/dev/null
  (cd "$DIR" && set -a && . "$ENV_FILE" && set +a && setsid nohup "${CMD[@]}" &) >/dev/null 2>&1 < /dev/null  # detach fully: an ssh or pipe reader must not wait
  say "No systemd user session: added a crontab @reboot line and started it now."
else
  (cd "$DIR" && setsid nohup "${CMD[@]}" &) >/dev/null 2>&1 < /dev/null  # detach fully: an ssh or pipe reader must not wait
  say "WARNING: neither systemd nor crontab is available: started it now, but it will not start after a reboot."
fi

if wait_healthy "$PORT"; then
  say ""
  say "Vero Status is running on this VM, port $PORT. Open it on your laptop:"
  say "  VS Code (Remote-SSH): PORTS tab > Forward a Port > $PORT, then open http://localhost:$PORT"
  say "  or a terminal:        ssh -N -L $PORT:127.0.0.1:$PORT $USER@$(hostname -f 2>/dev/null || hostname)"
  if [ "$ACTION" = team ]; then
    say "  Team link (needs port $PORT open to the VM): http://$(hostname -f 2>/dev/null || hostname):$PORT/"
    say "  Admin key: $DIR/data/admin_key.txt (private)"
  fi
  say "Log: $DIR/data/vero-status.log"
else
  die "it did not start; see $DIR/data/vero-status.log"
fi
