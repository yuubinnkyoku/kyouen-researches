# n11 ultra-cheap u04 adoption flip-census/reaudit completion (2026-11-27)

Completion log of the follow-up Part declared in
`research/experiments/n11-ultra-cheap-u04-adoption-reaudit-20261127/DECLARATION.md`
(publish-then-execute, declaration commit `34b3c559`).  Kit:
`research/experiments/n11-ultra-cheap-u04-adoption-reaudit-20261127/`.

## Outcome

- **Refresh (3 fresh-cold runs, ~58 s each): byte-identical.**
  `refresh_adoption_ultra_cheap_u04.py` (sha256 `db61c850...`), a
  byte-clone of the published u03 refresh `84304650...` differing in
  exactly three regions (docstring, CACHE path, expected cache sha;
  computation region machine-verified byte-identical), reproduced the
  SCEN refresh outputs from sha-pinned ROOT inputs against the new
  head `beecb024...`: refresh-summary `d35900b9...`, closure ladder
  800 rows, per-root 20 rows, probe worklist 64,265 rows
  (`c38831c1...`/3,714,832 bytes, UNPUBLISHED per size policy,
  pinned).  An additional cross-check: a temporary (unpublished)
  BASE-variant refresh regen reproduced the published BASE-side
  pins byte-for-byte (worklist `ece16723...`/3,714,889 bytes, summary
  `7cd44879...`, closure `137cc49b...`, per-root `4e27453a...`).
- **Flip-census measurer GATE-PASS (3 fresh-cold runs,
  byte-identical).**
  `scripts/measurer_adoption_ultra_cheap_u04.py` (sha256
  `8f245190...`), a disclosed structural adaptation of the u03
  measurer `a86cf188...` with all expectations measured before
  publication, ran the full fail-closed assertion chain plus the
  tamper battery 4/4.  Measurement record:
  `output/census-deltas-ultra-cheap-u04-adoption.json` (sha256
  `2092e7a8...`).

## Measured facts (BASE `c5082866...` -> SCEN `beecb024...`)

- The adopted u04 WIN row (`1152921505747697664:1032`, s5 index
  745184, serving class 23101) flips ALL FOUR of its owner classes
  from unknown to excluded_now (the first 4-owner adoption in the
  ultra-cheap family): 23092
  (`1152921505747697664:8`, cost-unknown 112 -> 111), 23101
  (`1152921504892059648:16`, the serving class, 1 -> 0), 23115
  (`1152921505680588800:1032`, 105 -> 104) and 23938
  (`1152921504673955840:1032`, 100 -> 99).
- The serving class 23101 was still UNKNOWN on the BASE head (the
  u03 serving-class pre-exclusion caveat did NOT materialise); the
  adopted row resolves its LAST unknown cost child (1 -> 0), the
  class LEAVES the closure ladder (801 -> 800 rows) and flips to
  excluded_now (its first win-hit).
- Census: unknown 34,380 -> 34,376, excluded_now 140 -> 144,
  free_now 39 -> 39 (Board-verified both sides), excluded 390 -> 390.
- Closure ladder left [23101], entered [], ZERO unknown_now churn
  (the first all-rank churn), 800 rank-churn cells.
- Per-root: root 26 individual greedy 5,227 -> 5,087, root 24
  2,776 -> 2,775 (free_now/uncovered identical on all 20 roots);
  joint greedy UNCHANGED at 43,830; worklist 64,266 -> 64,265 (the
  adopted key's own probe row for serving class 23101 leaves the
  worklist; a sorted BASE-variant diff shows exactly one deleted row
  plus trailing-counter decrements on surviving rows; scheduling
  quantities, NOT coverage claims).
- update8: s5 index 745184 sits OUTSIDE the frozen baseline
  requirement (resolved 284 -> 284, remaining_now 31,332 -> 31,332,
  groups_free_now 131 -> 131); win-hit groups UNCHANGED 35 -> 35.

## Deviation from the pre-registered expectation (disclosed)

The declaration pre-registered the graph-derived FOUR-owner union
flip prediction (23092, 23101, 23115, 23938 all unknown ->
excluded_now; census unknown 34,380 -> 34,376, excluded_now 140 ->
144).  The MEASURED census and flip list match the prediction
EXACTLY - the first ultra-cheap adoption with zero census/flip
deviation.  The only measured deviation is a SCHEDULING quantity:
the worklist drops ONE row (64,266 -> 64,265), not the naive
four-membership-rows prediction (64,266 -> 64,262).  Recorded as an
experimental fact, not silently adjusted.

## Disclosures

- The u04 adoption manifest `3241759f...`, increment `c6344d3a...`
  and BASE-side u03 reaudit outputs were byte-fetched from published
  main and sha-verified before the measurement; local work-tree
  copies are byte-identical.
- The measurer transform from the u03 measurer was machine-verified
  (unique-count assertions on every replacement region); the full
  u03 assertion chain was preserved with the u04 measured values
  substituted, then run three times fresh cold from the
  published-byte-verbatim inputs.
- This lane runs without access to the user's computer (scheduled
  task); publication is via the GitHub API only.

## Status guard

Adoption bookkeeping only: NO root verdict is consumed, NO class
freed, NO root excluded.  Nodes are bookkeeping, never verdicts.
The standard 11x11 empty board, every central-reply root, the
two-stone root {60,27} and its remaining third moves {100,108} stay
UNKNOWN.
