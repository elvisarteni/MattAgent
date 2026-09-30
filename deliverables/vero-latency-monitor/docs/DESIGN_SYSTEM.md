# Design system: vero-latency-monitor

## Colours
Same tokens as the SCMP: pass/ok green `#1f7a45`, warn amber `#a8500b`, fail/crit red `#9b1c2e`, n.a. grey `#8a94a3`, brand `#0a6aa1`. Series colours in fixed order per model. Dark mode redefines every token.

## Typography
IBM Plex Sans / Segoe UI, tabular numbers for figures.

## Components
KPI tile, line chart (p50 solid, p95 dotted, threshold dashed lines, failure ticks), status badge (ok / slow / very slow / error / timeout / unexpected), per-model table, live feed, live pill.

## Rules
Latency colour is set by the thresholds in config (below warn = green, warn to crit = amber, at or above crit = red). Latency figures use successful probes; availability counts every probe.
