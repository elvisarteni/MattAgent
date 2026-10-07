# Review of v1 and changes in v2

Date: 2026-10-07. Scope: Task 1, Pingtool (Vero Status) on the Linux VM; Task 2, the Confluence page; Task 3, the ASPF-1561 plan.

How v1 was reviewed:
- Ran the VM installer end to end. The systemd path was checked with stub tools, and the generated unit was checked with `systemd-analyze verify`.
- Ran ruff, mypy (Linux and Windows), shellcheck, and the unit tests on Python 3.8 and 3.13.
- Rendered both HTML pages at desktop and phone width.
- Checked every claim in the docs against the code and the Vero integration guide.

## Task 1: Pingtool on the VM

| # | Finding in v1 | Severity | v2 |
|---|---|---|---|
| 1 | In local mode the server accepted only `localhost:8767`. VS Code forwards to another local port when 8767 is busy (for example when Vero Status also runs on the laptop), and `ssh -L 9000:…` does the same. **Every request then got 403.** | High | Fixed. Loopback names are accepted on any port. Origin is still checked, and DNS rebinding is still blocked. Tests added. |
| 2 | On a shared VM, `ps -eo args` lists every user's processes, so another user's Vero showed as *your* open CLI. | Medium | Fixed. Only the current user's processes are listed (`ps -U <uid>`). |
| 3 | Under systemd, the admin link (with the key) was written to stdout and so to the journal, which admins can read. | Medium | Fixed. The console log is used only on a terminal; otherwise the link goes only to the private log. |
| 4 | `install_vm.sh` crashed with `USER: unbound variable` where `$USER` is not set. Found by running it. | Medium | Fixed. Falls back to `id -un`. |
| 5 | Without systemd or crontab, the started process kept the installer's stdout open, so `ssh vm 'bash scripts/install_vm.sh'` or `… \| tee` **hung forever**. Found by re-running the installer through a pipe. | Medium | Fixed. The start is fully detached; re-tested through a pipe. |
| 6 | Extracting with `python3 -m zipfile` drops the executable bit, so `scripts/install_vm.sh` would fail. | Low | Fixed. Docs use `bash scripts/install_vm.sh`, and the zip stores the script as 0755. |
| 7 | Linting the installer found an unused loop variable and a non-constant `source`. | Low | Fixed. Shellcheck is clean. |

Improvements already in v1, kept in v2:
- The Vero CLI is found when it is installed with nvm or npm-global and is not on PATH, and nvm's `node` is found too.
- No browser is started on a headless VM.
- The installer sets up a systemd user service or a crontab line, and needs no sudo.
- `data/` and the admin key are readable by their owner only.
- SIGTERM stops the program cleanly.
- VS Code Remote-SSH session logs are read.
- The page footer shows which machine runs the checks.

## Task 2: Confluence page

| # | Finding in v1 | v2 |
|---|---|---|
| 1 | `scripts/install_vm.sh` fails after `python3 -m zipfile` extraction, and `unzip` may be missing on the VM. | Uses `python3 -m zipfile -e` and `bash scripts/…`. |
| 2 | "Restart: `systemctl --user restart`" is wrong when crontab is used instead. | Restart means running the installer again, which works with both. |
| 3 | The update step ("unzip over the folder") was vague. | Exact commands; notes that `data/` is kept. |
| 4 | It assumed port 8767 on the laptop. | Explains that VS Code may show another port, and gives the `-L 9000:` variant. |
| 5 | It did not say where the zip comes from, and the paste instruction was awkward. | Attach the zip to the page; select from the title down. |
| 6 | Missing: proxy, number of checks per day, and that only your own processes are read. | Added. |
| 7 | At phone width, long commands pushed the page sideways (442 px wide in a 390 px window). | Long lines now wrap. |
| 8 | Broken tag `</i›` (introduced and caught in this review). | Fixed. The HTML nesting is validated. |

## Task 3: ASPF-1561 plan

| # | Finding in v1 | v2 |
|---|---|---|
| 1 | It said Vero "keeps tokens in clear text" without saying which. The guide says MCP bearer tokens and conversations are in clear text, and Bedrock uses AWS credentials. | Made precise. Recommends a short-lived AWS role session. |
| 2 | The manifest example mounted a file over a folder (`…/.vero/data/settings`). | Now an AWS credentials file with a `ttl`, and the path is marked "to confirm". |
| 3 | The bind mount assumes a local Docker daemon. | Notes that the broker must run on the Docker host, and adds the Kubernetes route (External Secrets or CSI). |
| 4 | Masking only the plain value misses base64 and URL-encoded headers. | Encodings added. |
| 5 | No effort estimates, so the "doesn't fit 3 SP" claim had no support. | Each phase has an estimate (about 10–11 days in total). |
| 6 | The Jira text claimed "no approved way" without evidence. | Rewritten on the SCMP fact: the store is still a placeholder. |
| 7 | Open points were missing the runtime choice and the owner of the Vero functional account. | Added (integration guide, open decision 5). |

## Still open (decisions, not defects)
- **VM:** whether the VM admin enables lingering, and whether IT opens the port, which team mode needs.
- **ASPF-1561:** which secret store is approved; Docker or Kubernetes; who owns the functional account.
- **Jira:** ASPF-1561 is marked *Resolved / Fixed* while its status is *In Progress*.
