# repo-vibe — Ground Truth

**Last verified:** 2026-11-01 (live API state; audit evidence 2026-10-29)
**Canonical branch:** main @ 5e9151f824

## What this repo is

Repo-Vibe badge service: a live README badge (SVG) showing lines
changed today, latest build status, a commit-mood read, and a
star-milestone meter, fed by the real GitHub API. Small, stdlib-only
Python; self-hostable.

## Verified current state

- **Head:** `5e9151f824` — unchanged from the audit freeze. Tree = 9 blobs.
- **Open PRs:** none.
- **Tests:** `pytest test_repo_vibe.py` → **4 passed, 0 failed**
  (audit lane run, reproduced): mood classification, milestone ladder,
  SVG validity with real numbers, GitHub App manifest shape.
- Webhook security verified by code read: `X-Hub-Signature-256`
  checked with `hmac.compare_digest`, rejected if the secret is
  unset — fail-closed.

## Known defects / honest gaps

- **No hosted deployment is evidenced anywhere.** The README's
  example badge URL uses a placeholder domain; the GitHub App half
  (manifest + JWT path) is coded and manifest-tested but no created
  App or live installation is evidenced.
- No caching/rate-limit handling for badge traffic at scale
  (single-file stdlib server).

## Merged in the 2026-11-01 train

Nothing.

## Parked PRs

None open. (An unmerged side branch, `tara/public-badge-privacy`,
exists; its contents were not diffed by the audit.)

## Where it is going

No direction ruled. The audit's first-dollars sequence lists a
Repo-Vibe hosted deploy as step 7 (a lane sequence, not a ruling);
it has not been executed.

## Estate rule

Update this file after any significant repo change. No claims without verification.
