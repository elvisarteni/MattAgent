# Design system: vero-availability-monitor

## Colours
SCMP tokens: available `#1f7a45`, degraded `#a8500b`, unavailable `#9b1c2e`, no data `#b7bfcb`, brand `#0a6aa1`; tinted
backgrounds for the status banner; full dark-mode token set.

## Typography
IBM Plex Sans / Segoe UI; tabular numbers for figures.

## Components
Status banner (icon, title, since, reason), component card (dot, name, status, facts), availability tile, status
timeline (bars = worst status per slot), incident table, recent-checks table with per-check dots, live pill.

## Rules
Words, not only colour: every status has a label (available / degraded / unavailable / no data). The banner says
what users need first: is Vero available, since when, and why not.
