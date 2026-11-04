# Repo-Vibe

### The vibe for your repo.

Your README is a billboard that never changes. **Repo-Vibe turns it into a live terminal.**

One line of markdown, and your profile shows a retro CRT status terminal fed by
*real* data from the GitHub REST API — not a static image, not a fake counter:

![Repo-Vibe Dashboard](https://repo-vibe.example.com/badge/YOUR-OWNER/YOUR-REPO)

- **Lines of Code Changed Today** — summed from today's actual commits
- **Current Build Status** — your latest GitHub Actions run, success or fail
- **Last Contributor Mood** — a transparent lexicon read of your last 3 commit
  messages (`LOCKED IN`, `GRINDING`, `DEBUGGING`…). No black box; the word
  lists are in the code, read them yourself
- **The Star Meter** — a bar that fills toward your next star milestone.
  Watching it grow is the whole point. Vanity, as a service.

Every number is fetched live or it doesn't ship. That's the house rule.

## Use it

Add this to any `README.md`:

```markdown
![Repo-Vibe Dashboard](https://YOUR-DEPLOYMENT/badge/OWNER/REPO)
```

Public badges use only the unauthenticated public API. Private repositories return 404 even if installation credentials are configured. A visibility check runs before every cached response; upstream errors do not serve old cached data.

## Run your own

```bash
python3 app.py
# GET /badge/<owner>/<repo> — public repository SVG
# POST /webhook — optional HMAC-verified push invalidation
python3 -m pytest -q
```

Cache entries expire after five minutes or at the UTC day boundary, with at most 256 entries. Public GitHub API quotas limit this to a small self-hosted service. A deployment and actual usage are not yet verified.

Automatic App setup is disabled: the old callback exchanged a one-time manifest code but discarded its returned credentials. `/setup`, `/manifest` and `/setup/callback` now return 410 without contacting GitHub. Existing manually configured signed push webhooks remain supported. Configure `WEBHOOK_SECRET` for those; no secret belongs in source control.

Activity is bounded to the latest 30 commits from today (UTC), and the badge labels that result as a sample at the cap. If any commit detail cannot be fetched, the line-change total is shown as unavailable rather than as a partial sum. A failed CI lookup displays UNKNOWN; NO CI RUNS is reserved for a successful lookup with an empty workflow list. Counts below the cap cover all commits returned for the current UTC day. This remains a bounded public-repository badge, not an authoritative audit or complete activity report.

Offline / receipt mode (render from a captured API response):

```bash
python3 repo_vibe.py --data-file demo-stats.json --out demo-badge.svg
python3 test_repo_vibe.py   # all tests
```

## Verified demo in this repo

`demo-badge.svg` was rendered from **live** Savage Forge data on 2026-10-14:
build `SUCCESS`, last-3-commit mood `LOCKED IN`, and 347,278 lines changed
across the first 30 commits of the day (v1 fetches up to 30 commits/day —
that cap is stated here, not hidden).

## Roadmap (same family, later)

- **Ghost-Writer AI** — a GitHub App bot that drafts doc updates on PRs that
  change a function signature without touching the docs.
- **Chrono-Repo** — `/chronos <date>` on an issue/PR opens an ephemeral,
  read-only snapshot of the repo as it existed that day.

## License

MIT. If Repo-Vibe makes your repo look alive, the footer links back here —
star it and the meter moves for both of us.
