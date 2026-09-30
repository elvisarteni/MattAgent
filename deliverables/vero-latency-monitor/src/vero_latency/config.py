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


def load(path: Path | None = None) -> dict:
    path = Path(path or os.environ.get("VLM_CONFIG") or CONFIG_FILE)
    if not path.exists():
        raise ConfigError(f"config not found: {path} (run: vlm init)")
    try:
        raw = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        raise ConfigError(f"{path}: invalid JSON: {e}") from e
    cfg = _merge(DEFAULTS, raw)
    validate(cfg)
    data_dir = Path(cfg["data_dir"])
    cfg["data_dir"] = str(data_dir if data_dir.is_absolute() else ROOT / data_dir)
    cfg["_path"] = str(path)
    return cfg


def validate(cfg: dict) -> None:
    cli = cfg["cli"]
    if not isinstance(cli["command"], list) or not cli["command"]:
        raise ConfigError("cli.command must be a non-empty list of arguments")
    if cli["prompt_via"] not in ("arg", "stdin"):
        raise ConfigError("cli.prompt_via must be 'arg' or 'stdin'")
    if cli["prompt_via"] == "arg" and not any("{prompt}" in a for a in cli["command"]):
        raise ConfigError("cli.command needs a {prompt} placeholder when prompt_via is 'arg'")
    if not cfg["models"]:
        raise ConfigError("models must list at least one entry")
    for m in cfg["models"]:
        if "id" not in m:
            raise ConfigError("every model needs an 'id' (use \"\" for the CLI default)")
        m.setdefault("label", m["id"] or "default")
    if int(cfg["schedule"]["interval_minutes"]) < 1:
        raise ConfigError("schedule.interval_minutes must be >= 1")
    t = cfg["thresholds_ms"]
    if not 0 < t["warn"] <= t["crit"]:
        raise ConfigError("thresholds_ms: need 0 < warn <= crit")


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
