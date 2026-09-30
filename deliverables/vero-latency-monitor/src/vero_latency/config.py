"""Load and validate config/monitor.json. Non-secret settings only."""
from __future__ import annotations

import copy
import json
import os
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CONFIG_DIR = ROOT / "config"
CONFIG_FILE = CONFIG_DIR / "monitor.json"
EXAMPLE_FILE = CONFIG_DIR / "monitor.example.json"

DEFAULTS = {
    "cli": {
        "command": ["vero", "-p", "{prompt}", "--model", "{model}"],
        "prompt_via": "arg",
        "timeout_s": 60,
        "version_command": ["vero", "--version"],
        "env": {},
    },
    "prompt": "Reply with OK",
    "expect": "OK",
    "models": [{"id": "", "label": "default"}],
    "schedule": {"interval_minutes": 15, "run_in_dashboard": True},
    "thresholds_ms": {"warn": 5000, "crit": 15000},
    "retention_days": 90,
    "server": {"host": "127.0.0.1", "port": 8765},
    "data_dir": "data",
}


class ConfigError(Exception):
    pass


def _merge(base: dict, over: dict) -> dict:
    out = copy.deepcopy(base)
    for k, v in over.items():
        if k.startswith("_"):
            continue
        if isinstance(v, dict) and isinstance(out.get(k), dict):
            out[k] = _merge(out[k], v)
        else:
            out[k] = v
    return out


def read_json(path: Path) -> dict:
    # utf-8-sig: Notepad on Windows may save "UTF-8 with BOM"
    text = Path(path).read_text(encoding="utf-8-sig")
    try:
        return json.loads(text)
    except json.JSONDecodeError as e:
        hint = ""
        if "escape" in str(e).lower():
            hint = " (Windows paths: write C:\\\\Tools\\\\x or C:/Tools/x)"
        raise ConfigError(f"{path}: invalid JSON: {e}{hint}") from e


def write_json(path: Path, data: dict) -> None:
    clean = {k: v for k, v in data.items() if not k.startswith("_")}
    Path(path).write_text(json.dumps(clean, indent=2) + "\n", encoding="utf-8")


def load(path: Path | str | None = None) -> dict:
    path = Path(path or os.environ.get("VLM_CONFIG") or CONFIG_FILE)
    if not path.exists():
        raise ConfigError(f"config not found: {path} (run setup.bat or: python vlm.py configure)")
    raw = read_json(path)
    if not isinstance(raw, dict):
        raise ConfigError(f"{path}: top level must be a JSON object")
    cfg = _merge(DEFAULTS, raw)
    try:
        validate(cfg)
    except (KeyError, TypeError, ValueError) as e:
        raise ConfigError(f"{path}: wrong value or type near {e}") from e
    data_dir = Path(os.path.expandvars(os.path.expanduser(str(cfg["data_dir"]))))
    cfg["data_dir"] = str(data_dir if data_dir.is_absolute() else ROOT / data_dir)
    cfg["_path"] = str(path)
    return cfg


def validate(cfg: dict) -> None:
    cli = cfg["cli"]
    if not isinstance(cli["command"], list) or not cli["command"] or not all(isinstance(a, str) for a in cli["command"]):
        raise ConfigError("cli.command must be a non-empty list of strings")
    if cli["prompt_via"] not in ("arg", "stdin"):
        raise ConfigError("cli.prompt_via must be 'arg' or 'stdin'")
    if cli["prompt_via"] == "arg" and not any("{prompt}" in a for a in cli["command"]):
        raise ConfigError("cli.command needs a {prompt} placeholder when prompt_via is 'arg'")
    cli["timeout_s"] = float(cli["timeout_s"])
    if cli["timeout_s"] <= 0:
        raise ConfigError("cli.timeout_s must be > 0")
    if not isinstance(cli.get("env") or {}, dict):
        raise ConfigError("cli.env must be an object")
    if not isinstance(cfg["models"], list) or not cfg["models"]:
        raise ConfigError("models must list at least one entry")
    labels = set()
    for m in cfg["models"]:
        if not isinstance(m, dict) or "id" not in m:
            raise ConfigError("every model needs an 'id' (use \"\" for the CLI default)")
        m["id"] = str(m["id"])
        m["label"] = str(m.get("label") or m["id"] or "default")
        if m["label"] in labels:
            raise ConfigError(f"duplicate model label {m['label']!r}")
        labels.add(m["label"])
    s = cfg["schedule"]
    s["interval_minutes"] = int(s["interval_minutes"])
    if not 1 <= s["interval_minutes"] <= 1440:
        raise ConfigError("schedule.interval_minutes must be between 1 and 1440")
    t = cfg["thresholds_ms"]
    t["warn"], t["crit"] = float(t["warn"]), float(t["crit"])
    if not 0 < t["warn"] <= t["crit"]:
        raise ConfigError("thresholds_ms: need 0 < warn <= crit")
    cfg["retention_days"] = int(cfg["retention_days"])
    if cfg["retention_days"] < 1:
        raise ConfigError("retention_days must be >= 1")
    cfg["server"]["port"] = int(cfg["server"]["port"])


def public_view(cfg: dict) -> dict:
    """What the dashboard may show. Never includes cli.env values."""
    return {
        "models": [m["label"] for m in cfg["models"]],
        "prompt": cfg["prompt"],
        "interval_minutes": cfg["schedule"]["interval_minutes"],
        "run_in_dashboard": cfg["schedule"]["run_in_dashboard"],
        "thresholds_ms": cfg["thresholds_ms"],
        "timeout_s": cfg["cli"]["timeout_s"],
        "retention_days": cfg["retention_days"],
    }
