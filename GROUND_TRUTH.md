# Repo-Vibe — verified public-badge privacy repair

2026-11-04. Source base 98c13fb5c2cad2364fec822f5bd7ac7b5a4989bc.

## Implemented and verified

Public badge requests check unauthenticated repository visibility on every request, including cache hits. Private, inaccessible and unknown-visibility repositories never return cached data. Badge statistics never receive an installation token or environment token. The existing tara/public-badge-privacy branch supplied the original privacy repair and three regression tests; it was adapted without rewriting that branch.

Cache entries expire after 300 seconds and at the UTC day boundary, bounded to 256 entries. Invalid owner/repository paths reject before network access. Webhook bodies reject invalid/negative/oversized Content-Length, transfer encoding and invalid envelope shapes.

The old GitHub App manifest callback consumed a one-time conversion but discarded returned credentials. Automatic setup routes now return 410 before any network request. Existing signed push-webhook invalidation still works. No live credentials were exchanged during verification.

Original baseline: 4 pytest tests passed. Final: 13 passed, 0 failed. Raw evidence is under evidence/privacy-20261104/. Regression controls cover visibility changes, private cache exclusion, unauthenticated statistics, expiry, midnight, bounds, path validation, payload admission and one-time setup-code preservation.

## Remaining limits

No hosted deployment, installation, customer or revenue is verified. Public API quota and single-process HTTP serving limit scale. Activity still samples at most 30 daily commits; individual detail-fetch errors may yield partial totals, and CI lookup failure currently can display NO CI RUNS. These core data-quality limits are open. This is a verified privacy/operability repair, not completed commercial productization.
