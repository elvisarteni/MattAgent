# PRD: vero-latency-monitor

## Problem
The Vero CLI (the client's AI CLI, several models behind pre-defined guardrails) is used in the quality-check workflows. Nobody measures how fast it answers, so slow or failing periods go unnoticed and cannot be proven.

## Goal
Measure Vero CLI latency continuously, at the lowest possible cost, and show it to the Quality Lead on a dashboard.

## Users
Quality Lead (owner of the figures), Quality AI Automation team (operates it), SW QA Engineer (reads reports).

## Requirements
| ID | Requirement | Jira |
|----|-------------|------|
| VLM-001 | Execute the cheapest prompt (fixed, minimal prompt; cheapest model configurable) | ASPF-1578 AC1 |
| VLM-002 | Support time-trigger setup (Windows Task Scheduler / cron, built-in scheduler) | ASPF-1578 AC2 |
| VLM-003 | Record every probe (SQLite, run manifest) and show it on a dashboard | ASPF-1578 AC3 |
| VLM-004 | Run without manual steps once set up (scheduled, retention pruning, logs) | ASPF-1578 AC4 |
| VLM-005 | Install on another laptop from a zip, no internet, no admin rights | ASPF-1578 |
| VLM-006 | Live view of new probes without page reload | ASPF-1578 |
| VLM-007 | Export (CSV) and a self-contained HTML report for email | ASPF-1578 |

## Out of scope
Measuring answer quality; load or stress testing; alerting by email or Teams (possible later); central server deployment.
