# PRD: vero-availability-monitor

## Problem
The Quality AI Automation team depends on Vero (Vero CLI, Vero Chat). When Vero is unavailable nobody knows until a workflow fails, and there is no record of how often it happens.

## Goal
Know at a glance whether Vero is available now, since when, and how available it has been over 24 h, 7 d and 30 d, at the lowest possible cost.

## Users
Quality Lead (owner of the figures), Quality AI Automation team, SW QA Engineers.

## Requirements
| ID | Requirement | Jira |
|----|-------------|------|
| VAM-001 | Use the cheapest possible end-to-end call (fixed minimal prompt, pinned cheap model) plus free checks | ASPF-1578 AC1 |
| VAM-002 | Time trigger: Task Scheduler (laptop-safe) / cron, or the status page's own timer | ASPF-1578 AC2 |
| VAM-003 | Record every run (SQLite + run manifest) and show it on a status page | ASPF-1578 AC3 |
| VAM-004 | Fully automated after setup (scheduled checks, status page at logon, pruning, log rotation) | ASPF-1578 AC4 |
| VAM-005 | Status per run: available / degraded / unavailable, with the reason | ASPF-1578 |
| VAM-006 | Availability 24 h / 7 d / 30 d, status timeline, incidents | ASPF-1578 |
| VAM-007 | Optional Vero Chat check without any model call | ASPF-1578 |
| VAM-008 | Install from a guided script; distributable as a readable document | ASPF-1578 |

## Out of scope
Latency analytics (0.x tool), alerting by e-mail/Teams, measuring interactive sessions, Vero use in pipeline stage 4.
