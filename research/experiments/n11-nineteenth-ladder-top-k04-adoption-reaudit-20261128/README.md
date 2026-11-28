# n11 nineteenth ladder-top k04 adoption reaudit (flip-census/refresh)

Execution kit of the Part declared in
`research/log/2026-11-28-n11-nineteenth-ladder-top-k04-adoption-reaudit-declaration.md`
(commit `0c912e89`, single owner, publish-then-execute): the WIN-side
flip-census review of the nineteenth k04 canonical adoption
(declaration `1043d552`, completion `dacc6445`; BASE = eighteenth k03
head of record `3abecf8b...` 6,903 rows WIN 221 / LOSS 6,682,
SCEN = nineteenth k04 head of record `8cc87263...` 6,904 rows
WIN 222 / LOSS 6,682).

## Measured (3 refresh runs + 3 measurer runs byte-identical; prediction holds EXACTLY)

- **Status flips: exactly the 3 non-pre-excluded owner classes
  [18534, 18554, 19885] flip unknown -> excluded_now** (the
  declaration's naive THREE-flip prediction holds with zero
  deviation). Census: unknown 34,357 -> 34,354 / excluded_now
  163 -> 166 / free_now 39 (Board-verified both sides) /
  excluded 390.
- **Serving class 20421 (1155173304420536320:131072) STAYS in the
  closure ladder: 798 -> 798 rows, entered [], left [] (NO exit)**.
  It is ALREADY excluded_now at BASE (win-hit by previously adopted
  rows of the chain) and does not flip status; the adoption drops its
  cost-unknown children 2 -> 1 (k05 `1152921642046849024:68719477248`
  remains stage-1 2M UNKNOWN). Ladder rank churn 0 cells; the serving
  class keeps rank 1 and its unknown_now 2 -> 1. All three flipping
  owner classes (18534, 18554, 19885) sit OUTSIDE the ladder on both
  sides; the ladder's only unknown_now churn is the serving class
  itself.
- Per-root coverage: free_now/uncovered identical on all 20 roots;
  one individual greedy re-route measured (root 12 RISES
  2,840 -> 2,932, a +92 scheduling re-route churn of that root's
  greedy ordering, scheduling quantity, NOT a coverage claim); joint
  greedy MEASURES 43,185 -> 43,184; probing worklist 64,254 ->
  64,253 (SCEN regen pin `7e3c73d4...` / 3,714,150 B, unpublished per
  size policy; BASE pin `115e3c60` / 3,714,209 B reproduced).
- update8: the adopted s5 index 620742 sits INSIDE the frozen
  baseline requirement (resolved 289 -> 290, remaining_now 31,332
  unchanged, groups_free_now 131); win-hit group set unchanged
  35 -> 35 with every group entry byte-identical. The three flipping
  owner classes (18534, 18554, 19885) are NOT update8 plan group
  classes; the pre-excluded serving class 20421 IS an update8 plan
  group class on BOTH sides (4 of the 35 win-hit groups, already
  present at BASE) and its group entries are untouched by the
  adoption.

## Gates (fail-closed)

Refresh: 3-region byte-clone of the published eighteenth k03
reaudit refresh (docstring, CACHE path to the nineteenth k04
adoption kit head cache, expected cache sha `8cc87263...`);
3 sequential runs byte-identical (~65s/run): summary `d4b8099b`,
closure `877b5f52`, per-root `0fccacec`. BASE-side pin reproduction:
1 run of the published eighteenth k03 refresh (unchanged bytes,
CACHE `3abecf8b...`) reproduces the published eighteenth k03 reaudit
outputs (summary `23561801`, closure `77521463`, per-root
`340e5a9c`) byte-for-byte plus the BASE worklist regen pin
`115e3c60` / 3,714,209 B (executed BEFORE the declaration as the
standing disclosed anchor; reads BASE bytes only). Measurer:
structural adaptation of the eighteenth k03 measurer with expected
values pinned from the first measured run; 3 runs byte-identical
(census json `7c0d1649...`); external tamper battery 4/4
fail-closed (MT1 SCEN-cache verdict flip caught by the SCEN cache
sha pin, MT2 BASE closure csv byte-tamper caught by the BASE
closure pin, MT3 adoption-manifest byte-tamper caught by the
manifest pin, MT4 SCEN worklist row deletion caught by the SCEN
worklist pin - each aborted at its own pin BEFORE the census json
was written; census json sha snapshot `7c0d1649...` unchanged
throughout) + clean control re-PASS byte-identical.

## Honest disclosures

- The root-12 individual greedy union INCREASES by 92 in this
  adoption (2,840 -> 2,932) while the joint greedy union DECREASES
  by 1 (43,185 -> 43,184) and the worklist drops by 1; these are
  scheduling re-route churns of the greedy orderings, not coverage
  claims and not deviations from the declared prediction (which
  pre-registered only the flip census and the caveat).
- The first SCEN refresh invocation attempt wrote to a not-yet-
  created reaudit/output directory and failed closed (rc=1,
  FileNotFoundError at the summary write, no partial output); the
  directory was created and all 3 runs completed rc=0
  byte-identical.
- The ladder stay of class 20421 is a scheduling statement measured
  here; it is NOT a class closure claim and NOT a root verdict.
- This lane runs without access to the user's computer (scheduled
  task); publication is via the GitHub API only.
- The probe-worklist (3.7 MB) stays unpublished per the standing
  size policy; pinned by sha256 only.

## Files

- DECLARATION.md - the Part declaration (copy of the published log).
- output/census-deltas-nineteenth-k04-adoption.json - measured
  census deltas (schema follows the eighteenth k03 reaudit census
  json).
- output/tamper-battery-stdout.log - the external tamper battery
  stdout (4/4 fail-closed + clean control re-PASS).
- reaudit/output/refresh-summary.json / closure-classes.csv /
  per-root-coverage.csv - the 3-run byte-identical SCEN refresh
  outputs.
- reaudit/scripts/refresh-adoption-nineteenth-k04.py - the refresh
  (3-region byte-clone of the eighteenth k03 refresh).
- scripts/measurer-adoption-nineteenth-k04.py - the measurer.
- scripts/refresh-adoption-nineteenth-k04.py - same refresh bytes at
  the kit-root scripts/ location (prior kit convention).
- MANIFEST.txt - sha256 of every published file.

## Status guard

Measurement bookkeeping only: NO verdict is consumed. Class-status
flips and the closure-ladder stay are census bookkeeping, not class
closures and not root verdicts. Class 20421 is NOT complete (k05
remains stage-1 2M UNKNOWN). The standard 11x11 empty board, the 19
central-reply roots, the two-stone root {60,27} and its remaining
third moves 100/108 stay UNKNOWN. Nodes are bookkeeping, never
verdicts.
