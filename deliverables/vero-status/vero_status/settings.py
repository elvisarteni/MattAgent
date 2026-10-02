"""User settings, changed from the dashboard and kept in data/settings.json."""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass, replace
from pathlib import Path
from typing import Any, Dict

INTERVALS = (0, 5, 15, 30, 60)  # minutes; 0 = only when "Check now" is clicked
CHEAP_MODEL = "us.anthropic.claude-haiku-4-5-20251001-v1:0"


class SettingsError(ValueError):
    pass


@dataclass(frozen=True)
class Settings:
    vero_path: str = ""  # empty = find it automatically
    check_model: str = CHEAP_MODEL  # empty = Vero's own configured model
    interval_minutes: int = 15
    timeout_seconds: int = 120
    port: int = 8767
    track_sessions: bool = True  # read your own Vero sessions (CLI, VS Code) for latency and the model in use

    def merged(self, changes: Dict[str, Any]) -> Settings:
        """A validated copy with the given changes (unknown keys are rejected)."""
        allowed = set(asdict(self))
        unknown = set(changes) - allowed
        if unknown:
            raise SettingsError(f"unknown setting(s): {', '.join(sorted(unknown))}")
        new = replace(self, **changes)
        new.validate()
        return new

    def validate(self) -> None:
        if not isinstance(self.vero_path, str) or not isinstance(self.check_model, str):
            raise SettingsError("vero_path and check_model must be text")
        if len(self.check_model) > 200 or any(c.isspace() for c in self.check_model):
            raise SettingsError("the model id must be one word without spaces")
        if self.interval_minutes not in INTERVALS:
            raise SettingsError(f"interval must be one of {INTERVALS} minutes")
        if not isinstance(self.timeout_seconds, int) or not 30 <= self.timeout_seconds <= 600:
            raise SettingsError("timeout must be between 30 and 600 seconds")
        if not isinstance(self.track_sessions, bool):
            raise SettingsError("track_sessions must be true or false")
        if not isinstance(self.port, int) or not 1024 <= self.port <= 65535:
            raise SettingsError("port must be between 1024 and 65535")


def load(path: Path) -> Settings:
    """Settings from the file, or defaults. A broken file never stops the program."""
    try:
        raw = json.loads(path.read_text(encoding="utf-8-sig"))
        return Settings().merged({k: v for k, v in raw.items() if k in asdict(Settings())})
    except (OSError, ValueError, TypeError, AttributeError):
        return Settings()


def save(path: Path, settings: Settings) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(".tmp")
    tmp.write_text(json.dumps(asdict(settings), indent=2) + "\n", encoding="utf-8")
    tmp.replace(path)
