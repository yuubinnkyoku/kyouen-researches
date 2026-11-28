# n11 eighteenth ladder-top k03 adoption reaudit (flip-census/refresh)

Execution kit of the Part declared in
`research/log/2026-11-28-n11-eighteenth-ladder-top-k03-adoption-reaudit-declaration.md`
(commit `b841063a`, single owner, publish-then-execute): the WIN-side
flip-census review of the eighteenth k03 canonical adoption
(declaration `7fe49b5e`, completion `86cec4cd`; BASE = seventeenth k02
head of record `e56ca5ca...` 6,902 rows WIN 220 / LOSS 6,682,
SCEN = eighteenth k03 head of record `3abecf8b...` 6,903 rows
WIN 221 / LOSS 6,682).

## Measured (MAKER 3 runs byte-identical; prediction holds EXACTLY)

- **Status flips: exactly the 3 non-pre-excluded owner classes
  [18136, 18143, 20128] flip unknown -> excluded_now** (the
  declaration's naive THREE-flip prediction holds with zero
  deviation). Census: unknown 34,360 -> 34,357 / excluded_now
  160 -> 163 / free_now 39 (Board-verified both sides) /
  excluded 390.
- **Serving class 20421 (1155173304420536320:131072) STAYS in the
  closure ladder: 798 -> 798 rows, entered [], left [] (NO exit)**.
  It is ALREADY excluded_now at BASE (win-hit by previously adopted
  rows of the chain) and does not flip status; the adoption drops its
  cost-unknown children 3 -> 2 (k04 `1153062242096250880:540672`,
  k05 `1152921642046849024:68719477248` remain stage-1 2M UNKNOWN).
  Ladder rank churn 0 cells; the serving class keeps rank 1 and its
  unknown_now 3 -> 2. All three flipping owner classes (18136,
  18143, 20128) sit OUTSIDE the ladder on both sides; the ladder's
  only unknown_now churn is the serving class itself.
- Per-root coverage: free_now/uncovered identical on all 20 roots;
  two individual greedy re-routes measured (root 12 drops
  2,841 -> 2,840, root 37 drops 3,632 -> 3,631); joint greedy
  MEASURES 43,145 -> 43,185 (a +40 scheduling re-route churn of the
  greedy union; scheduling quantity, NOT a coverage claim);
  probing worklist 64,255 -> 64,254 (SCEN regen pin
  `115e3c60...` / 3,714,209 B, unpublished per size policy; BASE
  pin `6d3cf3ad` / 3,714,268 B reproduced).
- update8: the adopted s5 index 605961 sits INSIDE the frozen
  baseline requirement (resolved 288 -> 289, remaining_now 31,332
  unchanged, groups_free_now 131); win-hit group set unchanged
  35 -> 35 with every group entry byte-identical. The three
  flipping owner classes (18136, 18143, 20128) are NOT update8 plan
  group classes; the pre-excluded serving class 20421 IS an update8
  plan group class on BOTH sides (4 of the 35 win-hit groups,
  already present at BASE) and its group entries are untouched by
  the adoption.

## Gates (fail-closed)

Refresh: 3-region byte-clone of the published seventeenth k02
reaudit refresh (docstring, CACHE path to the eighteenth k03
adoption kit head cache, expected cache sha `3abecf8b...`);
3 sequential runs byte-identical (~65s/run). BASE-side pin
reproduction: 1 run of the published seventeenth k02 refresh
(unchanged bytes, CACHE `e56ca5ca...`) reproduces the published
seventeenth k02 reaudit outputs (summary `e22be6db`, closure
`32f0e4f1`, per-root `b1aae491`) byte-for-byte plus the BASE
worklist regen pin `6d3cf3ad` (executed BEFORE the declaration as
the standing disclosed anchor; reads BASE bytes only). Measurer:
structural adaptation of the seventeenth k02 measurer with
expected values pinned from the first measured run; 3 runs
byte-identical (census json `3e0be91a...`); external tamper
battery 4/4 fail-closed (MT1 SCEN-cache verdict flip caught by the
SCEN cache sha pin, MT2 BASE closure csv byte-tamper caught by the
BASE closure pin, MT3 adoption-manifest byte-tamper caught by the
manifest pin, MT4 SCEN worklist row deletion caught by the SCEN
worklist pin - each aborted at its own pin BEFORE the census json
was written; census json sha snapshot `3e0be91a...` unchanged
throughout) + clean control re-PASS byte-identical.

## Honest disclosures

- The first refresh invocation attempt used `/usr/bin/time`, which
  does not exist on this host (rc=127, four cases): NO refresh run
  happened during it and no output was produced; the battery was
  redone with shell timestamps and all 3 runs completed rc=0
  byte-identical.
- The joint greedy union INCREASES by 40 in this adoption
  (43,145 -> 43,185) while the two measured individual greedy
  re-routes both DROP; this is a scheduling re-route churn of the
  greedy ordering, not a coverage claim and not a deviation from
  the declared prediction (which pre-registered only the flip
  census and the caveat).
- The ladder stay of class 20421 is a scheduling statement measured
  here; it is NOT a class closure claim and NOT a root verdict.
- This lane runs without access to the user's computer (scheduled
  task); publication is via the GitHub API only.
- The probe-worklist (3.7 MB) stays unpublished per the standing
  size policy; pinned by sha256 only.

## Files

- DECLARATION.md - the Part declaration (copy of the published log).
- output/census-deltas-eighteenth-k03-adoption.json - measured
  census deltas (schema follows the seventeenth k02 reaudit census
  json).
- output/tamper-battery-stdout.log - the external tamper battery
  stdout (4/4 fail-closed + clean control re-PASS).
- reaudit/output/refresh-summary.json / closure-classes.csv /
  per-root-coverage.csv - the 3-run byte-identical SCEN refresh
  outputs.
- reaudit/scripts/refresh-adoption-eighteenth-k03.py - the refresh
  (3-region byte-clone of the seventeenth k02 refresh).
- scripts/measurer-adoption-eighteenth-k03.py - the measurer.
- scripts/refresh-adoption-eighteenth-k03.py - same refresh bytes at
  the kit-root scripts/ location (prior kit convention).
- MANIFEST.txt - sha256 of every published file.

## Status guard

Measurement bookkeeping only: NO verdict is consumed. Class-status
flips and the closure-ladder stay are census bookkeeping, not class
closures and not root verdicts. Class 20421 is NOT complete
(k04-k05 remain stage-1 2M UNKNOWN). The standard 11x11 empty
board, the 19 central-reply roots, the two-stone root {60,27} and
its remaining third moves 100/108 stay UNKNOWN. Nodes are
bookkeeping, never verdicts.
