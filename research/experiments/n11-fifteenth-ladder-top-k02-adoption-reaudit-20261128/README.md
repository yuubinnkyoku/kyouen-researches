# n11 fifteenth ladder-top k02 adoption reaudit (flip-census/refresh)

Execution kit of the Part declared in
`research/log/2026-11-28-n11-fifteenth-ladder-top-k02-adoption-reaudit-declaration.md`
(commit `68b18052`, single owner, publish-then-execute): the WIN-side
flip-census review of the fifteenth k02 canonical adoption
(declaration `12d43eb9`, completion `3e316cb9`; BASE = fifteenth k03
head of record `3a527d39...` 6,899 rows WIN 217 / LOSS 6,682,
SCEN = fifteenth k02 head of record `58110025...` 6,900 rows
WIN 218 / LOSS 6,682).

## Measured (MAKER 3 runs byte-identical; prediction holds EXACTLY)

- **Status flips: exactly the 3 non-pre-excluded owner classes
  [5788, 5815, 7678] flip unknown -> excluded_now** (the declaration's
  naive THREE-flip prediction holds with zero deviation). Census:
  unknown 34,368 -> 34,365 / excluded_now 152 -> 155 / free_now 39
  (Board-verified both sides) / excluded 390.
- **Serving class 5804 (6053400849139367936:0) EXITS the closure
  ladder: 799 -> 798 rows, left [5804], entered []**. It was the
  rank-1 ladder row holding its LAST cost-unknown child (k02,
  unknown_now 1 at BASE); the adoption drops its cost-unknown
  1 -> 0. It is ALREADY excluded_now at BASE (fourteenth Part) and
  does not flip status. Ladder rank churn 798 cells (one row leaves
  at rank 1; the ladder re-ranks). The three owner classes sit
  outside the ladder on both sides.
- Per-root coverage: free_now/uncovered identical on all 20 roots;
  two individual greedy re-routes measured (root 38 drops
  2,876 -> 2,875, root 49 drops 2,690 -> 2,689); joint greedy
  43,148 -> 43,147 (scheduling quantities, not coverage claims);
  probing worklist 64,259 -> 64,258 (SCEN regen pin
  `a8ebeffc...` / 3,714,446 B, unpublished per size policy; BASE pin
  `e165cf36` / 3,714,501 B reproduced).
- update8: adopted s5 index 212115 sits OUTSIDE the frozen baseline
  requirement (resolved 286 -> 286, remaining_now 31,332,
  groups_free_now 131); win-hit group set unchanged 35 -> 35
  (no added or removed groups; none of the owner classes is a plan
  group class).

## Gates (fail-closed)

Refresh: byte-clone of the published k03 reaudit refresh
(`b02869ef...`) differing in exactly 3 regions (docstring, CACHE
path, expected cache sha `58110025...`); 3 sequential runs
byte-identical (~66s/run). BASE-side pin reproduction: 1 run of the
published k03 reaudit refresh (unchanged bytes, CACHE `3a527d39...`)
reproduces the published k03 reaudit outputs (summary `8e37ad17`,
closure `01dd4d85`, per-root `fc771d82`) byte-for-byte plus the BASE
worklist regen pin `e165cf36` (executed BEFORE the declaration as
the standing disclosed anchor; reads BASE bytes only). Measurer:
structural adaptation of the k03 measurer (`4a2680aa...`) with
expected values pinned from the first measured run; 3 runs
byte-identical (census json `b089b269...`); external tamper battery
4/4 fail-closed (MT1 SCEN-cache verdict flip caught by the sha-pin
gate, MT2 BASE closure csv byte-tamper caught by the BASE closure
pin, MT3 adoption-manifest byte-tamper caught by the manifest pin,
MT4 SCEN worklist row deletion caught by the SCEN worklist pin - all
aborted before the census json was written) + clean control re-PASS
byte-identical.

## Honest disclosures

- One transient raw-CDN failure during the MT2 restore (the first
  clean control correctly failed closed on the stale BASE closure
  pin `9eb5924a...` and wrote no output); the pin was re-fetched
  from the commit-pinned raw CDN, sha-verified (`01dd4d85...`), and
  the clean control re-run PASSed byte-identical. The fail-closed
  behaviour on the stale pin is itself evidence the gate works.
- The ladder exit of class 5804 is a scheduling statement measured
  here; it is NOT a class closure claim and NOT a root verdict.
- This lane runs without access to the user's computer (scheduled
  task); publication is via the GitHub API only.
- The probe-worklist (3.7 MB) stays unpublished per the standing
  size policy; pinned by sha256 only.

## Files

- DECLARATION.md - the Part declaration (copy of the published log).
- output/census-deltas-fifteenth-k02-adoption.json - measured
  census deltas (schema follows the k03 reaudit census json).
- reaudit/output/refresh-summary.json / closure-classes.csv /
  per-root-coverage.csv - the 3-run byte-identical SCEN refresh
  outputs.
- reaudit/scripts/refresh-adoption-fifteenth-k02.py - the refresh
  (3-region byte-clone of `b02869ef...`).
- scripts/measurer-adoption-fifteenth-k02.py - the measurer.
- scripts/refresh-adoption-fifteenth-k02.py - same refresh bytes at
  the kit-root scripts/ location (k03 kit convention).
- MANIFEST.txt - sha256 of every published file.

## Status guard

Measurement bookkeeping only: NO verdict is consumed. Class-status
flips and the closure-ladder exit are census bookkeeping, not class
closures and not root verdicts. The standard 11x11 empty board, the
19 central-reply roots, the two-stone root {60,27} and its remaining
third moves 100/108 stay UNKNOWN. Nodes are bookkeeping, never
verdicts.
