# ADR-002: Monitor availability, not latency
Status: accepted (3.0.0)

Context: Vero CLI `task` latency is dominated by start-up and agent orchestration (~52 s for "Reply with OK",
integration guide 3.4). Latency analytics of a cold-start agent say little; what the team needs is "is Vero usable now".
Decision: the tool reports available / degraded / unavailable per run, availability %, timeline and incidents.
Duration is kept only as a check attribute and as the "slow" (degraded) criterion.
Consequences: simpler status page; the 0.x latency monitor is superseded.
