# ADR-001: Python standard library only
Status: accepted (kept from 0.x)

Context: distributed to laptops without admin rights or PyPI access; archives and scripts are often blocked.
Decision: Python 3.8+ standard library only; dashboard is one HTML file with inline JS/CSS, no CDN.
Consequences: nothing to install or patch; dev tools (ruff, mypy) are used only by developers via `uvx`.
