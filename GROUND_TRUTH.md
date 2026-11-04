# Repo-Vibe — verified public-badge privacy repair

2026-11-04. Source base 98c13fb5c2cad2364fec822f5bd7ac7b5a4989bc.

## Implemented and verified

Public badge requests check unauthenticated repository visibility on every request, including cache hits. Private, inaccessible and unknown-visibility repositories never return cached data. Badge statistics never receive an installation token or environment token. The existing tara/public-badge-privacy branch supplied the original privacy repair and three regression tests; it was adapted without rewriting that branch.

Cache entries expire after 300 seconds and at the UTC day boundary, bounded to 256 entries. Invalid owner/repository paths reject before network access. Webhook bodies reject invalid/negative/oversized Content-Length, transfer encoding and invalid envelope shapes.

The old GitHub App manifest callback consumed a one-time conversion but discarded returned credentials. Automatic setup routes now return 410 before any network request. Existing signed push-webhook invalidation still works. No live credentials were exchanged during verification.

Original baseline: 4 pytest tests passed. The privacy repair finished with 13 passed, 0 failed. A follow-up data-quality repair adds 4 focused regressions: failed or malformed commit details never produce a partial line total, CI lookup failure stays distinct from a successful empty workflow list, and the 30-commit ceiling is labeled as a sample. Current local result: 17 passed, 0 failed. Raw privacy evidence is under evidence/privacy-20261104/ and evidence/data-quality-20261104-local.txt.

## Remaining limits

No hosted deployment, installation, customer or revenue is verified. Public API quota and single-process HTTP serving limit scale. Activity is still capped at 30 daily commits and explicitly labeled as a sample at the cap. Detail-fetch failures now suppress the line total; CI lookup failures now display UNKNOWN. This is a verified privacy and data-quality repair, not completed commercial productization.
