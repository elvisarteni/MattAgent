"""Vero Chat check: MCP `initialize` handshake over streamable HTTP (integration guide 2.1).

No tool is called, so no model runs and nothing is billed. The reply may be plain JSON or
Server-Sent Events (`data:` lines). The bearer token comes from an environment variable;
it is never stored, logged or shown.
"""

from __future__ import annotations

import json
import os
import ssl
import time
import urllib.error
import urllib.request
from typing import Any, Dict, Optional

from .. import __version__
from ..config import Config
from ..domain import Check, CheckResult, Status
from .vero_cli import clean

INITIALIZE = {
    "jsonrpc": "2.0",
    "id": 1,
    "method": "initialize",
    "params": {
        "protocolVersion": "2024-11-05",
        "capabilities": {},
        "clientInfo": {"name": "vero-availability-monitor", "version": __version__},
    },
}


def parse_reply(body: str) -> Optional[Dict[str, Any]]:
    """Return the JSON-RPC message from a JSON or SSE body, or None."""
    candidates = [body.strip()]
    candidates += [ln[5:].strip() for ln in body.splitlines() if ln.startswith("data:")]
    for c in candidates:
        if not c.startswith("{"):
            continue
        try:
            msg = json.loads(c)
        except json.JSONDecodeError:
            continue
        if isinstance(msg, dict) and ("result" in msg or "error" in msg):
            return msg
    return None


def check_chat(cfg: Config) -> CheckResult:
    token = os.environ.get(cfg.chat.token_env, "").strip()
    if not token:
        return CheckResult(
            Check.CHAT, Status.DOWN, None, f"environment variable {cfg.chat.token_env} is not set (see guide: Vero Chat token)"
        )
    req = urllib.request.Request(
        cfg.chat.url,
        data=json.dumps(INITIALIZE).encode(),
        method="POST",
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
            "Accept": "application/json, text/event-stream",
        },
    )
    ctx = ssl.create_default_context(cafile=cfg.chat.ca_bundle or None)
    t0 = time.perf_counter()
    try:
        with urllib.request.urlopen(req, timeout=cfg.chat.timeout_s, context=ctx) as r:
            body = r.read(256 * 1024).decode("utf-8", "replace")
    except urllib.error.HTTPError as e:
        hint = " (token rejected or expired)" if e.code in (401, 403) else ""
        return CheckResult(Check.CHAT, Status.DOWN, (time.perf_counter() - t0) * 1000, f"HTTP {e.code}{hint}")
    except (urllib.error.URLError, OSError, ValueError) as e:
        reason = getattr(e, "reason", e)
        return CheckResult(Check.CHAT, Status.DOWN, (time.perf_counter() - t0) * 1000, clean(f"unreachable: {reason}"))
    ms = (time.perf_counter() - t0) * 1000
    msg = parse_reply(body)
    if msg is None:
        return CheckResult(Check.CHAT, Status.DOWN, ms, "reply is not an MCP JSON-RPC message")
    if "error" in msg:
        err = msg["error"] if isinstance(msg["error"], dict) else {}
        return CheckResult(Check.CHAT, Status.DOWN, ms, clean(f"MCP error: {err.get('message', msg['error'])}"))
    info = (msg.get("result") or {}).get("serverInfo") or {}
    version = clean(f"{info.get('name', '?')} {info.get('version', '')}".strip())
    slow = ms > cfg.chat_slow_s * 1000
    return CheckResult(
        Check.CHAT, Status.DEGRADED if slow else Status.UP, ms, f"slow: {ms / 1000:.1f} s" if slow else "", version=version
    )
