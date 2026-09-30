# ADR-001: Python standard library only

Status: accepted (ASPF-1578)

## Context
The tool is sent by email as a zip and installed on laptops without admin rights and often without access to PyPI or CDNs.

## Decision
Use only the Python 3.8+ standard library (sqlite3, http.server, subprocess, threading). The dashboard is one HTML file with inline JS and SVG, no external libraries.

## Consequences
Unzip and run; nothing to install or keep patched. Charts are hand-written SVG (simple line chart only). The HTTP server is for local use only (binds to 127.0.0.1).
