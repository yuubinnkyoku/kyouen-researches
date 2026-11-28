# n11 thirteenth k01+k02 adoption flip-census/reaudit completion (2026-11-28)

Completion log of the Part declared in
`research/experiments/n11-thirteenth-k01k02-adoption-reaudit-20261128/DECLARATION.md`
(publish-then-execute, declaration commit `0bb54826`).  Kit:
`research/experiments/n11-thirteenth-k01k02-adoption-reaudit-20261128/`.

## Outcome

- **Refresh (3 fresh-cold runs, ~60 s each): byte-identical.**
  `reaudit/scripts/refresh-adoption-thirteenth-k01k02.py`
  (published to both `reaudit/scripts/` and `scripts/`, sha256
  `c24e9072...`), a byte-clone of the published u04 refresh differing
  in exactly three regions (docstring, CACHE path, expected cache
  sha; computation region machine-verified byte-identical),
  reproduced the SCEN refresh outputs from sha-pinned ROOT inputs
  against the new head `d772f73c...` (three runs, stdout sha
  `38cb8bec...` x3): refresh-summary `0d02503c...` (39,887 B),
  closure ladder 799 rows, per-root 20 rows, probe worklist 64,263
  rows (`da2d22e1...`/3,714,716 bytes, UNPUBLISHED per size
  policy, pinned).
- **Flip-census measurer GATE-PASS (2 fresh-cold runs,
  byte-identical).**
  `scripts/measurer-adoption-thirteenth-k01k02.py` (sha256
  `d5263fc7...`, 37,367 B), a disclosed machine-verified structural
  adaptation of the u04 measurer (unique-count assertions on every
  replacement region; every failure-to-fix loop adjusted the
  expectation to the MEASURED value, never the reverse), ran the full
  fail-closed assertion chain plus the tamper battery 4/4.
  Measurement record:
  `output/census-deltas-thirteenth-k01k02-adoption.json` (sha256
  `7b6027d3...`, 62,008 B).
- All published kit files were fetch-back verified byte-identical
  at their push commits via commit-pinned raw URLs (DECLARATION
  `5b940855`, README `dfac038c`, MANIFEST `d7648691`, per-root
  `96cf51b7`, refresh summary `0d02503c`, closure `be8bcff1`,
  measurer `d5263fc7`, census json `7b6027d3`).  Two placeholder
  push mistakes (`6466f775`, `a393326b`) were immediately fixed
  (`46fdedfe`, `9483b2fe`) and the fixes fetch-back verified; a
  one-digit transcription slip in closure-classes.csv row 756
  (`90147711`) was fixed in `6387843d` and fetch-back verified
  (`be8bcff1...`).  All fixed by fetch-back sha comparison, none
  silently adjusted.

## Measured facts (BASE `beecb024...` -> SCEN `d772f73c...`)

- The thirteenth adoption consumes exactly the two published
  ladder-top rows (k01 `1153204147814662144:65536`, s5 index
  556117; k02 `1152922672837951488:65792`, s5 index 558553; both
  WIN, both serving class 16757; head 6,894/212/6,682 ->
  6,896/214/6,682).
- **The declaration's pre-exclusion caveat MATERIALISED (first
  thirteenth adoption where it does).**  The naive four-owner union
  flip prediction does NOT hold: of the owner union 16612, 16740,
  16757, 30542, the shared classes 16757 and 30542 were ALREADY
  excluded_now on the BASE head via earlier win-hits; only the
  k01-only owner 16612 and the k02-only owner 16740 flip unknown ->
  excluded_now.  Census: unknown 34,376 -> 34,374, excluded_now
  144 -> 146, free_now 39 -> 39 (Board-verified both sides),
  excluded 390 -> 390.
- The serving class 16757 (`1153204079095185408:65536`) stays
  excluded_now on both sides and resolves its LAST TWO unknown cost
  children (the adopted keys themselves, cost-unknown 2 -> 0); the
  class LEAVES the closure ladder (800 -> 799 rows).  Closure churn:
  left [16757], entered [], ZERO unknown_now churn, 799 rank-churn
  cells (an all-rank churn).
- Per-root: root 48 individual greedy 2,980 -> 3,069, root 36
  3,029 -> 3,028 (free_now/uncovered identical on all 20 roots);
  joint greedy 43,830 -> 43,151; worklist 64,265 -> 64,263 (the two
  adopted keys' own membership rows leave the worklist; scheduling
  quantities, NOT coverage claims).
- update8: BOTH adopted s5 indices (556117, 558553) sit INSIDE the
  frozen baseline requirement (resolved 284 -> 286, remaining_now
  31,332 -> 31,332, groups_free_now 131 -> 131); win-hit groups
  UNCHANGED 35 -> 35 (the serving class 16757 is an update8 plan
  group class with 5 groups already win-hit at BASE; 16612, 16740,
  30542 are not plan classes).

## Deviation from the pre-registered expectation (disclosed)

The declaration pre-registered the naive graph-derived four-owner
union flip (census unknown 34,376 -> 34,372, excluded_now 144 ->
148) WITH an explicit u03-style serving-class pre-exclusion caveat.
The caveat MATERIALISED exactly as pre-registered: the measured
census is unknown 34,376 -> 34,374, excluded_now 144 -> 146 and the
flip list is [16612, 16740].  Recorded as an experimental fact, not
silently adjusted; the measurer asserts the materialised form
(flip-subset, pre-exclusion and serving-class assertions).

## Disclosures

- The thirteenth adoption manifest `18433ac0...`, increment
  `cebd8dc9...`, merged head `d772f73c...` and the BASE-side u04
  reaudit outputs (summary `d35900b9`, closure `ef344748`, per-root
  `d3c404e9`) were byte-fetched from published main and
  sha-verified before the measurement; local work-tree copies are
  byte-identical.
- The measurer transform from the u04 measurer was machine-verified
  (unique-count assertions on every replacement region); the full
  u04 assertion chain was preserved with the thirteenth measured
  values substituted, then run twice fresh cold from the
  published-byte-verbatim inputs.
- This lane runs without access to the user's computer (scheduled
  task); publication is via the GitHub API only.

## Status guard

Adoption bookkeeping only: NO root verdict is consumed, NO class
freed, NO root excluded.  Nodes are bookkeeping, never verdicts.
The standard 11x11 empty board, every central-reply root, the
two-stone root {60,27} and its remaining third moves {100,108} stay
UNKNOWN.
