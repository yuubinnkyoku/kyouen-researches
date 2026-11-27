# n11 ultra-cheap u03 adoption flip-census/reaudit completion (2026-11-27)

Completion log of the follow-up Part declared in
`research/experiments/n11-ultra-cheap-u03-adoption-reaudit-20261127/DECLARATION.md`
(publish-then-execute, declaration commit `7446f225`).  Kit:
`research/experiments/n11-ultra-cheap-u03-adoption-reaudit-20261127/`
(commit `651db168`, fetch-back 8/8 byte-identical).

## Outcome

- **Refresh (3 fresh-cold runs, ~63-68 s each): byte-identical.**
  `refresh_adoption_ultra_cheap_u03.py` (sha256 `84304650...`), a
  byte-clone of the published u02 refresh `525a130d...` differing in
  exactly three regions (docstring, CACHE path, expected cache sha;
  computation region machine-verified byte-identical), reproduced the
  SCEN refresh outputs from sha-pinned ROOT inputs against the new
  head `c5082866...`: refresh-summary `7cd44879...`, closure ladder
  801 rows, per-root 20 rows, probe worklist 64,266 rows
  (`ece16723...`/3,714,889 bytes, UNPUBLISHED per size policy,
  pinned).  An additional cross-check: a temporary (unpublished)
  BASE-variant refresh regen reproduced the published BASE worklist
  pin `9fec423a...`/3,715,002 bytes and the BASE census 34,382/138.
- **Flip-census measurer GATE-PASS (3 fresh-cold runs,
  byte-identical).**
  `scripts/measurer_adoption_ultra_cheap_u03.py` (sha256
  `a86cf188...`), a disclosed structural adaptation of the u02
  measurer `e3df6a73...` with all expectations measured before
  publication, ran the full fail-closed assertion chain plus the
  tamper battery 4/4.  Measurement record:
  `output/census-deltas-ultra-cheap-u03-adoption.json` (sha256
  `98208ad9...`).

## Measured facts (BASE `82b52577...` -> SCEN `c5082866...`)

- The adopted u03 WIN row (`1153202979851993088:272`, s5 index
  550879, serving class 16371) flips TWO of its THREE owner classes
  from unknown to excluded_now: 16404
  (`1154047404580798464:64`, cost-unknown 98 -> 97) and 16930
  (`1152921504875282432:272`, 52 -> 51).
- The serving class 16371 (`1153202979851993088:16`) was ALREADY
  excluded_now on the BASE head (its win-hit predates the u03
  adoption); the adopted row resolves its LAST unknown cost child
  (1 -> 0) and the class LEAVES the closure ladder (802 -> 801 rows)
  without changing census status.
- Census: unknown 34,382 -> 34,380, excluded_now 138 -> 140,
  free_now 39 -> 39 (Board-verified both sides), excluded 390 -> 390.
- Closure ladder left [16371], entered [], one unknown_now churn
  (16930: 52 -> 51), 797 rank-churn cells.
- Per-root: root 48 individual greedy 2,893 -> 2,980, root 26
  5,228 -> 5,227 (free_now/uncovered identical on all 20 roots);
  joint greedy UNCHANGED at 43,830; worklist 64,268 -> 64,266 (the
  adopted key's TWO membership rows, serving classes 16371 and
  16930, leave the worklist; scheduling quantities, NOT coverage
  claims).
- update8: s5 index 550879 sits OUTSIDE the frozen baseline
  requirement (resolved 284 -> 284, remaining_now 31,332 -> 31,332,
  groups_free_now 131 -> 131); win-hit groups UNCHANGED 35 -> 35.

## Deviation from the pre-registered expectation (disclosed)

The declaration pre-registered the graph-derived THREE-owner union
flip prediction (16371, 16404, 16930 all unknown -> excluded_now;
census unknown 34,382 -> 34,379, excluded_now 138 -> 141).  The
MEASURED flip count is TWO: the serving class 16371 was already
excluded_now on the BASE head (another of its 52 cost children is a
known WIN in the u02 head), so the win-hit pattern differs from the
u01/u02 parts for the first time (serving-class pre-exclusion).  The
measured census unknown 34,380 / excluded_now 140 supersedes the
prediction everywhere; recorded as an experimental fact, not
silently adjusted.

## Disclosures

- The u03 adoption manifest `f09075f0...`, increment `0796a210...`
  and BASE-side u02 reaudit outputs were byte-fetched from published
  main and sha-verified before the measurement; local work-tree
  copies are byte-identical.
- The measurer transform from the u02 measurer was machine-verified
  (unique-count assertions on every replacement); one config slip
  (the BASE worklist pin left at the u01-side value) was fail-closed
  by the pin assertion before any output was written, then corrected
  and re-run three times fresh cold.
- This lane runs without access to the user's computer (scheduled
  task); publication is via the GitHub API only.

## Status guard

Adoption bookkeeping only: NO root verdict is consumed, NO class
freed, NO root excluded.  Nodes are bookkeeping, never verdicts.
The standard 11x11 empty board, every central-reply root, the
two-stone root {60,27} and its remaining third moves {100,108} stay
UNKNOWN.
