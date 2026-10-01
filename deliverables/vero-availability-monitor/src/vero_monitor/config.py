"""Typed configuration loaded from config/monitor.json. Non-secret settings only:
the Vero Chat token is read from an environment variable named in the config, never stored."""

from __future__ import annotations

import copy
import json
import os
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, Tuple

ROOT = Path(__file__).resolve().parents[2]
CONFIG_FILE = ROOT / "config" / "monitor.json"
EXAMPLE_FILE = ROOT / "config" / "monitor.example.json"

DEFAULTS: Dict[str, Any] = {
    "vero": {
        "command": "vero",
        "model": "us.anthropic.claude-haiku-4-5-20251001-v1:0",
        "prompt": "Reply with exactly: OK",
        "expect": "OK",
        "task_timeout_s": 180,
        "task_args": ["task", "--json", "-m", "{model}", "-t", "{timeout}", "-c", "{workdir}", "{prompt}"],
        "version_args": ["version"],
        "env": {},
    },
    "checks": {"cli": True, "task": True, "chat": False},
    "chat": {
        "url": "https://verostudio.sw.nxp.com/mcp",
        "token_env": "VERO_CHAT_TOKEN",
        "timeout_s": 30,
        "ca_bundle": "",
    },
    "thresholds_s": {"task_slow": 90, "chat_slow": 10},
    "schedule": {"interval_minutes": 15, "run_in_dashboard": True},
    "retention_days": 90,
    "server": {"host": "127.0.0.1", "port": 8766},
    "data_dir": "data",
}


class ConfigError(Exception):
    pass


@dataclass(frozen=True)
class VeroSettings:
    command: str
    model: str
    prompt: str
    expect: str
    task_timeout_s: float
    task_args: Tuple[str, ...]
    version_args: Tuple[str, ...]
    env: Tuple[Tuple[str, str], ...]


@dataclass(frozen=True)
class ChatSettings:
    url: str
    token_env: str
    timeout_s: float
    ca_bundle: str


@dataclass(frozen=True)
class Config:
    vero: VeroSettings
    chat: ChatSettings
    check_cli: bool
    check_task: bool
    check_chat: bool
    task_slow_s: float
    chat_slow_s: float
    interval_minutes: int
    run_in_dashboard: bool
    retention_days: int
    host: str
    port: int
    data_dir: Path
    path: Path

    def public(self) -> Dict[str, Any]:
        """What the dashboard may show. No env values, no token, no token variable value."""
        return {
            "model": self.vero.model,
            "prompt": self.vero.prompt,
            "checks": {"cli": self.check_cli, "task": self.check_task, "chat": self.check_chat},
            "chat_url": self.chat.url if self.check_chat else None,
            "interval_minutes": self.interval_minutes,
            "task_timeout_s": self.vero.task_timeout_s,
            "task_slow_s": self.task_slow_s,
            "retention_days": self.retention_days,
        }


def merge(base: Dict[str, Any], over: Dict[str, Any]) -> Dict[str, Any]:
    out = copy.deepcopy(base)
    for k, v in over.items():
        if k.startswith("_"):
            continue
        if isinstance(v, dict) and isinstance(out.get(k), dict):
            out[k] = merge(out[k], v)
        else:
            out[k] = v
    return out


def read_json(path: Path) -> Dict[str, Any]:
    try:
        text = Path(path).read_text(encoding="utf-8-sig")  # Notepad may add a BOM
    except OSError as e:
        raise ConfigError(f"cannot read {path}: {e}") from e
    try:
        data = json.loads(text)
    except json.JSONDecodeError as e:
        hint = " (Windows paths: C:\\\\Tools\\\\x or C:/Tools/x)" if "escape" in str(e).lower() else ""
        raise ConfigError(f"{path}: invalid JSON: {e}{hint}") from e
    if not isinstance(data, dict):
        raise ConfigError(f"{path}: the top level must be a JSON object")
    return data


def write_json(path: Path, data: Dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")


def _str_list(value: Any, name: str) -> Tuple[str, ...]:
    if not isinstance(value, list) or not all(isinstance(a, str) for a in value):
        raise ConfigError(f"{name} must be a list of strings")
    return tuple(value)


def _positive(value: Any, name: str, kind: type = float) -> Any:
    try:
        v = kind(value)
    except (TypeError, ValueError) as e:
        raise ConfigError(f"{name} must be a number, got {value!r}") from e
    if v <= 0:
        raise ConfigError(f"{name} must be > 0")
    return v


def build(raw: Dict[str, Any], path: Path) -> Config:
    d = merge(DEFAULTS, raw)
    v, c, ch = d["vero"], d["checks"], d["chat"]
    task_args = _str_list(v["task_args"], "vero.task_args")
    if not any("{prompt}" in a for a in task_args):
        raise ConfigError("vero.task_args needs a {prompt} placeholder")
    if not isinstance(v["command"], str) or not v["command"].strip():
        raise ConfigError('vero.command must be the program name or full path, e.g. "vero"')
    env = {} if v.get("env") is None else v["env"]
    if not isinstance(env, dict):
        raise ConfigError('vero.env must be an object, e.g. {"HTTPS_PROXY": "..."}')
    flags = {k: c.get(k) for k in ("cli", "task", "chat")}
    if any(not isinstance(x, bool) for x in flags.values()):
        raise ConfigError("checks.cli / checks.task / checks.chat must be true or false")
    if not (flags["cli"] or flags["task"] or flags["chat"]):
        raise ConfigError("enable at least one check")
    interval = _positive(d["schedule"]["interval_minutes"], "schedule.interval_minutes", int)
    if interval > 1440:
        raise ConfigError("schedule.interval_minutes must be between 1 and 1440")
    timeout = _positive(v["task_timeout_s"], "vero.task_timeout_s")
    worst_case = timeout + min(30.0, timeout) + 30  # task hard limit + cli/chat checks
    if flags["task"] and worst_case > interval * 60:
        raise ConfigError(
            f"a run can take up to {worst_case:g} s, longer than the {interval} min interval:"
            " lower vero.task_timeout_s or raise schedule.interval_minutes"
        )
    data_dir = Path(os.path.expandvars(os.path.expanduser(str(d["data_dir"]))))
    return Config(
        vero=VeroSettings(
            command=v["command"].strip(),
            model=str(v["model"]),
            prompt=str(v["prompt"]),
            expect=str(v["expect"]),
            task_timeout_s=timeout,
            task_args=task_args,
            version_args=_str_list(v["version_args"], "vero.version_args"),
            env=tuple((str(k), str(x)) for k, x in env.items()),
        ),
        chat=ChatSettings(
            url=str(ch["url"]),
            token_env=str(ch["token_env"]),
            timeout_s=_positive(ch["timeout_s"], "chat.timeout_s"),
            ca_bundle=str(ch["ca_bundle"]),
        ),
        check_cli=flags["cli"],
        check_task=flags["task"],
        check_chat=flags["chat"],
        task_slow_s=_positive(d["thresholds_s"]["task_slow"], "thresholds_s.task_slow"),
        chat_slow_s=_positive(d["thresholds_s"]["chat_slow"], "thresholds_s.chat_slow"),
        interval_minutes=interval,
        run_in_dashboard=bool(d["schedule"]["run_in_dashboard"]),
        retention_days=_positive(d["retention_days"], "retention_days", int),
        host=str(d["server"]["host"]),
        port=_positive(d["server"]["port"], "server.port", int),
        data_dir=data_dir if data_dir.is_absolute() else ROOT / data_dir,
        path=path,
    )


def load(path: Path | str | None = None) -> Config:
    p = Path(path or os.environ.get("VAM_CONFIG") or CONFIG_FILE)
    if not p.exists():
        raise ConfigError(f"config not found: {p} (run setup.bat, or: python vam.py configure)")
    return build(read_json(p), p)
