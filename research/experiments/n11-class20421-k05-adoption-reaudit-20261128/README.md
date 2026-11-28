# n11 class-20421 k05 adoption reaudit (flip-census/refresh)

Execution kit of the Part declared in
`research/log/2026-11-28-n11-class20421-k05-adoption-reaudit-declaration.md`
(commit `2cad2042`, single owner, publish-then-execute): the WIN-side
flip-census review of the class-20421 k05 canonical adoption
(declaration `cf6a21a6`, completion `50037820`; BASE = nineteenth k04
head of record `8cc87263...` 6,904 rows WIN 222 / LOSS 6,682,
SCEN = class-20421 k05 head of record `e1a9cacc...` 6,905 rows
WIN 223 / LOSS 6,682).

## Measured (3 refresh runs + 3 measurer runs byte-identical; prediction holds EXACTLY)

- **Status flips: exactly the 2 non-pre-excluded owner classes
  [18683, 18710] flip unknown -> excluded_now** (the declaration's
  naive TWO-flip prediction holds with zero deviation). Census:
  unknown 34,354 -> 34,352 / excluded_now 166 -> 168 / free_now 39
  (Board-verified both sides) / excluded 390.
- **Serving class 20421 (1155173304420536320:131072) EXITS the
  closure ladder: 798 -> 797 rows, entered [], left [20421]**. It
  is ALREADY excluded_now at BASE (win-hit by previously adopted
  rows of the chain) and does not flip status; the adoption closes
  its LAST cost-unknown child (1 -> 0, exactly k05). Rank churn 769
  cells: 768 ladder cells shift by exactly -1 (the exit pulls the
  remaining rows up) plus one re-order cell - the flipping owner
  class 18683 sits INSIDE the ladder on both sides (unknown_now
  59 -> 58, rank 152 -> 123); the other flipping owner 18710 sits
  OUTSIDE the ladder on both sides. The ladder EXIT is a
  scheduling/census statement, NOT a class closure claim and NOT a
  root verdict.
- Per-root coverage: free_now/uncovered identical on all 20 roots;
  two individual greedy re-routes measured (root 12 drops
  2,932 -> 2,931 and root 37 rises 3,631 -> 3,634, scheduling
  re-route churns of those roots' greedy orderings, NOT coverage
  claims); joint greedy MEASURES 43,184 -> 43,184 (UNCHANGED joint
  size); probing worklist 64,253 -> 64,251 (SCEN regen pin
  `09865553...` / 3,714,021 B, unpublished per size policy; BASE
  pin `7e3c73d4` / 3,714,150 B reproduced).
- update8: the adopted s5 index 625899 sits INSIDE the frozen
  baseline requirement (resolved 290 -> 291, remaining_now 31,332
  unchanged, groups_free_now 131); win-hit group set unchanged
  35 -> 35 with every group entry byte-identical. The two flipping
  owner classes (18683, 18710) are NOT update8 plan group classes;
  the pre-excluded serving class 20421 IS an update8 plan group
  class on BOTH sides (4 of the 35 win-hit groups, already present
  at BASE) and its group entries are untouched by the adoption.

## Gates (fail-closed)

Refresh: 3-region byte-clone of the published nineteenth k04
reaudit refresh (docstring, CACHE path to the class-20421 k05
adoption kit head cache, expected cache sha `e1a9cacc...`);
3 sequential runs byte-identical (~65s/run): summary `dae1f1b3`,
closure `a33f0cb9`, per-root `ecfe4a0c`. BASE-side pin reproduction:
1 run of the published nineteenth k04 refresh (unchanged bytes,
CACHE `8cc87263...`) reproduces the published nineteenth k04 reaudit
outputs (summary `d4b8099b`, closure `877b5f52`, per-root
`0fccacec`) byte-for-byte plus the BASE worklist regen pin
`7e3c73d4` / 3,714,150 B (executed BEFORE the declaration as the
standing disclosed anchor; reads BASE bytes only). Measurer:
structural adaptation of the nineteenth k04 measurer with expected
values pinned from the first measured run; 3 runs byte-identical
(census json `86c2f36b...`); external tamper battery 4/4
fail-closed (MT1 SCEN-cache verdict flip caught by the SCEN cache
sha pin, MT2 BASE closure csv byte-tamper caught by the BASE
closure pin, MT3 adoption-manifest byte-tamper caught by the
manifest pin, MT4 SCEN worklist row deletion caught by the SCEN
worklist pin - each aborted at its own pin BEFORE the census json
was written; census json sha snapshot `86c2f36b...` unchanged
throughout) + clean control re-PASS byte-identical.

## Honest disclosures

- The 19th k04 adoption (prior Part) had raised root 12's greedy
  union to 2,932; this adoption drops it back to 2,931 while root
  37 rises 3,631 -> 3,634; the joint greedy union is UNCHANGED at
  43,184 and the worklist drops by 2 (the adopted key's own
  membership rows leave). These are scheduling re-route churns of
  the greedy orderings, not coverage claims and not deviations
  from the declared prediction (which pre-registered only the flip
  census, the EXIT and the caveat).
- The ladder EXIT of class 20421 is a scheduling statement measured
  here; it is NOT a class closure claim and NOT a root verdict.
- The merger dependency (s5_union_merge.py, pin `90711961...`) is
  fetched read-only from the published sixthlossk38 reaudit kit; its
  sha was re-verified against the pin before the measurer runs.
- This lane runs without access to the user's computer (scheduled
  task); publication is via the GitHub API only.
- The probe-worklist (3.7 MB) stays unpublished per the standing
  size policy; pinned by sha256 only.

## Files

- DECLARATION.md - the Part declaration (copy of the published log).
- output/census-deltas-class20421-k05-adoption.json - measured
  census deltas (schema follows the nineteenth k04 reaudit census
  json).
- output/tamper-battery-stdout.log - the external tamper battery
  stdout (4/4 fail-closed + clean control re-PASS).
- reaudit/output/refresh-summary.json / closure-classes.csv /
  per-root-coverage.csv - the 3-run byte-identical SCEN refresh
  outputs.
- reaudit/scripts/refresh-adoption-class20421-k05.py - the refresh
  (3-region byte-clone of the nineteenth k04 refresh).
- scripts/measurer-adoption-class20421-k05.py - the measurer.
- scripts/refresh-adoption-class20421-k05.py - same refresh bytes at
  the kit-root scripts/ location (prior kit convention).
- MANIFEST.txt - sha256 of every published file.

## Status guard

Measurement bookkeeping only: NO verdict is consumed. Class-status
flips and the closure-ladder EXIT are census bookkeeping, not class
closures and not root verdicts. The standard 11x11 empty board, the
19 central-reply roots, the two-stone root {60,27} and its remaining
third moves 100/108 stay UNKNOWN. Nodes are bookkeeping, never
verdicts.
