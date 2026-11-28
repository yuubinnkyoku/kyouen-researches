# n11 sixteenth ladder-top k01 adoption reaudit (flip-census/refresh)

Execution kit of the Part declared in
`research/log/2026-11-28-n11-sixteenth-ladder-top-k01-adoption-reaudit-declaration.md`
(commit `d9d53a8d`, single owner, publish-then-execute): the WIN-side
flip-census review of the sixteenth k01 canonical adoption
(declaration `e1618d8b`, completion `d555c1d6`; BASE = fifteenth k02
head of record `58110025...` 6,900 rows WIN 218 / LOSS 6,682,
SCEN = sixteenth k01 head of record `dbc1d950...` 6,901 rows
WIN 219 / LOSS 6,682).

## Measured (MAKER 3 runs byte-identical; prediction holds EXACTLY)

- **Status flips: exactly the 2 non-pre-excluded owner classes
  [15647, 16901] flip unknown -> excluded_now** (the declaration's
  naive TWO-flip prediction holds with zero deviation). Census:
  unknown 34,365 -> 34,363 / excluded_now 155 -> 157 / free_now 39
  (Board-verified both sides) / excluded 390.
- **Serving class 20421 (1155173304420536320:131072) STAYS in the
  closure ladder: 798 -> 798 rows, entered [], left [] (NO exit)**.
  It is ALREADY excluded_now at BASE (win-hit by a previously
  adopted row of the chain) and does not flip status; the adoption
  drops its cost-unknown children 5 -> 4 (k02-k05 remain stage-1
  2M UNKNOWN). Ladder rank churn 9 cells; the serving class
  re-ranks 31 -> 23 and its unknown_now 54 -> 53. The owner class
  16901 sits IN the ladder on both sides (unknown_now 54 -> 53);
  15647 sits outside the ladder on both sides.
- Per-root coverage: free_now/uncovered identical on all 20 roots;
  three individual greedy re-routes measured (root 12 drops
  2,843 -> 2,842, root 37 drops 3,639 -> 3,638, root 48 drops
  3,069 -> 3,068); joint greedy 43,147 -> 43,146 (scheduling
  quantities, not coverage claims); probing worklist
  64,258 -> 64,256 (SCEN regen pin `0aa54ad7...` / 3,714,327 B,
  unpublished per size policy; BASE pin `a8ebeffc` / 3,714,446 B
  reproduced).
- update8: the adopted s5 index 528689 sits INSIDE the frozen
  baseline requirement (resolved 286 -> 287, remaining_now
  31,332 unchanged, groups_free_now 131); win-hit group set
  unchanged 35 -> 35 with every group entry byte-identical. The
  two flipping owner classes (15647, 16901) are NOT update8 plan
  group classes; the pre-excluded serving class 20421 IS an
  update8 plan group class on BOTH sides (4 of the 35 win-hit
  groups, already present at BASE) and its group entries are
  untouched by the adoption.

## Gates (fail-closed)

Refresh: 3-region byte-clone of the published fifteenth k02
reaudit refresh (docstring, CACHE path to the sixteenth k01
adoption kit head cache, expected cache sha `dbc1d950...`);
3 sequential runs byte-identical (~66s/run). BASE-side pin
reproduction: 1 run of the published fifteenth k02 refresh
(unchanged bytes, CACHE `58110025...`) reproduces the published
fifteenth k02 reaudit outputs (summary `df5e7607`, closure
`e10b5765`, per-root `f2d5d2a7`) byte-for-byte plus the BASE
worklist regen pin `a8ebeffc` (executed BEFORE the declaration as
the standing disclosed anchor; reads BASE bytes only). Measurer:
structural adaptation of the fifteenth k02 measurer
(`8afedb6c...`) with expected values pinned from the first measured
run; 3 runs byte-identical (census json `97aca9cc...`); external
tamper battery 4/4 fail-closed (MT1 SCEN-cache verdict flip caught
by the sha-pin gate at the SCEN cache pin, MT2 BASE closure csv
byte-tamper caught by the BASE closure pin, MT3 adoption-manifest
byte-tamper caught by the manifest pin, MT4 SCEN worklist row
deletion caught by the SCEN worklist pin - each aborted at its own
pin BEFORE the census json was written) + clean control re-PASS
byte-identical.

## Honest disclosures

- The first tamper-battery attempt in this session mis-addressed
  two tamper edits into the adoption kit's published SCEN cache and
  manifest (wrong kit path) before backups were taken; both files
  were reverted byte-exact to their pinned shas (`dbc1d950...`,
  `97604d6c...`), the pins re-verified, and the ENTIRE battery was
  redone from clean backups with per-case abort lines recorded
  (MT1/MT2/MT3/MT4 each aborting at its own pin). No tampered byte
  survived; the clean control re-PASSed byte-identical.
- The MEASURED fact that the serving class 20421 is an update8 plan
  group class (already at BASE) corrects the session-internal
  expectation that none of the owner classes would be a plan group
  class; the fifteenth k02 measurer's disjointness assertion was
  correspondingly narrowed to the two flipping owners, and the
  serving-class plan-group membership is now asserted positively.
- The ladder stay of class 20421 is a scheduling statement measured
  here; it is NOT a class closure claim and NOT a root verdict.
- This lane runs without access to the user's computer (scheduled
  task); publication is via the GitHub API only.
- The probe-worklist (3.7 MB) stays unpublished per the standing
  size policy; pinned by sha256 only.

## Files

- DECLARATION.md - the Part declaration (copy of the published log).
- output/census-deltas-sixteenth-k01-adoption.json - measured
  census deltas (schema follows the fifteenth k02 reaudit census
  json).
- reaudit/output/refresh-summary.json / closure-classes.csv /
  per-root-coverage.csv - the 3-run byte-identical SCEN refresh
  outputs.
- reaudit/scripts/refresh-adoption-sixteenth-k01.py - the refresh
  (3-region byte-clone of the fifteenth k02 refresh).
- scripts/measurer-adoption-sixteenth-k01.py - the measurer.
- scripts/refresh-adoption-sixteenth-k01.py - same refresh bytes at
  the kit-root scripts/ location (fifteenth k02 kit convention).
- MANIFEST.txt - sha256 of every published file.

## Status guard

Measurement bookkeeping only: NO verdict is consumed. Class-status
flips and the closure-ladder stay are census bookkeeping, not class
closures and not root verdicts. Class 20421 is NOT complete
(k02-k05 remain stage-1 2M UNKNOWN). The standard 11x11 empty
board, the 19 central-reply roots, the two-stone root {60,27} and
its remaining third moves 100/108 stay UNKNOWN. Nodes are
bookkeeping, never verdicts.
