# n11 ultra-cheap u02 adoption flip-census/reaudit completion (2026-11-27)

Completion log of the follow-up Part declared in
`research/experiments/n11-ultra-cheap-u02-adoption-reaudit-20261127/DECLARATION.md`
(publish-then-execute, declaration commit `a95f1fd4`).  Kit:
`research/experiments/n11-ultra-cheap-u02-adoption-reaudit-20261127/`
(commit `e1465a00`, fetch-back 9/9 git-blob-sha identical).

## Outcome

- **Refresh (3 fresh-cold runs, ~59 s each): byte-identical.**
  `refresh_adoption_ultra_cheap_u02.py` (sha256 `525a130d...`), a
  byte-clone of the published u01 refresh `d0fa1762...` differing in
  exactly three regions (docstring, CACHE path, expected cache sha;
  computation region machine-verified byte-identical), reproduced the
  SCEN refresh outputs from sha-pinned ROOT inputs against the new
  head `82b52577...`: refresh-summary `722c70d8...`, closure ladder
  802 rows, per-root 20 rows, probe worklist 64,268 rows
  (`9fec423a...`/3,715,002 bytes, UNPUBLISHED per size policy,
  pinned).
- **Flip-census measurer GATE-PASS (3 fresh-cold runs,
  byte-identical).**  `scripts/measurer_adoption_ultra_cheap_u02.py`
  (sha256 `e3df6a73...`), a disclosed structural adaptation of the
  u01 measurer `c5ff4883...` with all expectations measured before
  publication, ran the full fail-closed assertion chain plus the
  tamper battery 4/4.  Measurement record:
  `output/census-deltas-ultra-cheap-u02-adoption.json` (sha256
  `fe4e0ad1...`).

## Measured facts (BASE `0ec4080d...` -> SCEN `82b52577...`)

- The adopted u02 WIN row (`1297036830121656320:131074`, s5 index
  93815, serving class 2251) flips exactly its THREE owner classes
  from unknown to excluded_now: 2251 (`1155314042043105280:0`,
  cost-unknown 1 -> 0, owned here), 2287
  (`10412322888236400640:0`, 92 -> 91) and 14338
  (`1152921504606847008:544`, 56 -> 55).
- Census: unknown 34,385 -> 34,382, excluded_now 135 -> 138,
  free_now 39 -> 39 (Board-verified both sides), excluded 390 -> 390.
- Closure ladder 803 -> 802 rows (left [2251], entered []),
  one unknown_now churn (14338: 56 -> 55), 779 rank-churn cells.
- Per-root: root 5 individual greedy 2,866 -> 2,865, root 37
  3,619 -> 3,639 (free_now/uncovered identical on all 20 roots);
  joint greedy 43,776 -> 43,830; worklist 64,270 -> 64,268
  (scheduling quantities, NOT coverage claims).
- update8: s5 index 93815 sits INSIDE the frozen baseline requirement
  (resolved 283 -> 284, remaining_now 31,388 -> 31,332,
  groups_free_now 131 -> 131); win-hit groups 31 -> 35 (four added,
  all owned by class 14338).

## Deviation from the pre-registered expectation (disclosed)

The declaration pre-registered ONE class flip (unknown 34,385 ->
34,384, excluded_now 135 -> 136) with the u01 three-owner caveat
pre-disclosed.  The MEASURED flip count is THREE (the u02 WIN key
has owner classes [2251, 2287, 14338], the same pattern as u01).
The measured values supersede the prediction everywhere; recorded
as an experimental fact, not silently adjusted.

## Disclosures

- The u02 adoption manifest `d8321e8a...`, increment `ef727442...`
  and BASE-side u01 reaudit outputs were byte-fetched from published
  main and sha-verified before the measurement; local work-tree
  copies are byte-identical.
- The measurer transform from the u01 measurer was machine-verified
  (unique-count assertions on every replacement); three consecutive
  fix iterations (INCREMENT path, SCEN_CACHE path, BASE_CENSUS_JSON
  path, merger file fetch) were fail-closed on missing/mistargeted
  pinned inputs before the passing runs; no output was written by
  failed runs.
- This lane runs without access to the user's computer (scheduled
  task); publication is via the GitHub API only.

## Status guard

Adoption bookkeeping only: NO root verdict is consumed, NO class
freed, NO root excluded.  Nodes are bookkeeping, never verdicts.
The standard 11x11 empty board, every central-reply root, the
two-stone root {60,27} and its remaining third moves {100,108} stay
UNKNOWN.
