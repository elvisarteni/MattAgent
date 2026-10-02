"""Vero Status team server: one shared status page for everyone on the network, no login.

    python vero_status_server.py              (port from data/settings.json, default 8767)
    python vero_status_server.py --port 8080

The share link and the private admin link are printed and written to data/vero-status.log.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from vero_status.app import serve_team

sys.exit(serve_team())
