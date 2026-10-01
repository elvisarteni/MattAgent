# ADR-003: No --yolo; run the task in an empty sandbox folder
Status: accepted (3.0.0)

Context: `vero task` starts an agent that can read/write files and run shell commands; `--yolo` auto-approves them
(integration guide 3.7). The availability probe only needs `attempt_completion`.
Decision: never pass `--yolo`; pass `-c data/sandbox` (an empty folder) and `-t` (timeout); kill the process tree at
`-t + min(30 s, -t)`. The prompt is fixed and harmless.
Consequences: if a Vero version starts asking for approval even for completion, the task check reports DOWN
("no completion"); the guide explains how to diagnose it.
