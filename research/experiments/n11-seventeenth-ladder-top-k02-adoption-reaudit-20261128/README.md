# n11 seventeenth ladder-top k02 adoption reaudit (flip-census/refresh)

Execution kit of the Part declared in
`research/log/2026-11-28-n11-seventeenth-ladder-top-k02-adoption-reaudit-declaration.md`
(commit `b59e143a`, single owner, publish-then-execute): the WIN-side
flip-census review of the seventeenth k02 canonical adoption
(declaration `d9f75b8b`, completion `b015cf6c`; BASE = sixteenth k01
head of record `dbc1d950...` 6,901 rows WIN 219 / LOSS 6,682,
SCEN = seventeenth k02 head of record `e56ca5ca...` 6,902 rows
WIN 220 / LOSS 6,682).

## Measured (MAKER 3 runs byte-identical; prediction holds EXACTLY)

- **Status flips: exactly the 3 non-pre-excluded owner classes
  [16104, 16132, 16656] flip unknown -> excluded_now** (the declaration's
  naive THREE-flip prediction holds with zero deviation). Census:
  unknown 34,363 -> 34,360 / excluded_now 157 -> 160 / free_now 39
  (Board-verified both sides) / excluded 390.
- **Serving class 20421 (1155173304420536320:131072) STAYS in the
  closure ladder: 798 -> 798 rows, entered [], left [] (NO exit)**.
  It is ALREADY excluded_now at BASE (win-hit by a previously
  adopted row of the chain) and does not flip status; the adoption
  drops its cost-unknown children 4 -> 3 (k03-k05 remain stage-1
  2M UNKNOWN). Ladder rank churn 0 cells; the serving class keeps
  rank 1 and its unknown_now 4 -> 3. All three flipping owner
  classes (16104, 16132, 16656) sit OUTSIDE the ladder on both
  sides; the ladder's only unknown_now churn is the serving class
  itself.
- Per-root coverage: free_now/uncovered identical on all 20 roots;
  two individual greedy re-routes measured (root 12 drops
  2,842 -> 2,841, root 37 drops 3,638 -> 3,632); joint greedy
  43,146 -> 43,145 (scheduling
  quantities, not coverage claims); probing worklist
  64,256 -> 64,255 (SCEN regen pin `6d3cf3ad...` / 3,714,268 B,
  unpublished per size policy; BASE pin `0aa54ad7` / 3,714,327 B
  reproduced).
- update8: the adopted s5 index 543795 sits INSIDE the frozen
  baseline requirement (resolved 287 -> 288, remaining_now
  31,332 unchanged, groups_free_now 131); win-hit group set
  unchanged 35 -> 35 with every group entry byte-identical. The
  three flipping owner classes (16104, 16132, 16656) are NOT
  update8 plan group classes; the pre-excluded serving class 20421
  IS an update8 plan group class on BOTH sides (4 of the 35
  win-hit groups, already present at BASE) and its group entries
  are untouched by the adoption.

## Gates (fail-closed)

Refresh: 3-region byte-clone of the published sixteenth k01
reaudit refresh (docstring, CACHE path to the seventeenth k02
adoption kit head cache, expected cache sha `e56ca5ca...`);
3 sequential runs byte-identical (~58s/run). BASE-side pin
reproduction: 1 run of the published sixteenth k01 refresh
(unchanged bytes, CACHE `dbc1d950...`) reproduces the published
sixteenth k01 reaudit outputs (summary `071993c8`, closure
`394f27e7`, per-root `d154f890`) byte-for-byte plus the BASE
worklist regen pin `0aa54ad7` (executed BEFORE the declaration as
the standing disclosed anchor; reads BASE bytes only). Measurer:
structural adaptation of the sixteenth k01 measurer
(`0c6f9f0f...`) with expected values pinned from the first measured
run; 3 runs byte-identical (census json `ce6041be...`); external
tamper battery 4/4 fail-closed (MT1 SCEN-cache verdict flip caught
by the sha-pin gate at the SCEN cache pin, MT2 BASE closure csv
byte-tamper caught by the BASE closure pin, MT3 adoption-manifest
byte-tamper caught by the manifest pin, MT4 SCEN worklist row
deletion caught by the SCEN worklist pin - each aborted at its own
pin BEFORE the census json was written) + clean control re-PASS
byte-identical.

## Honest disclosures

- The first tamper-battery attempt in this session failed to
  resolve the measurer script path in one shell invocation (rc=2,
  "can't open file", four cases); NO measurer run happened and NO
  tampered byte was in place during it, so nothing was exercised
  and nothing was corrupted. The battery was redone in full from
  byte-exact backups with per-case abort lines recorded
  (MT1/MT2/MT3/MT4 each aborting at its own pin, census json sha
  snapshot unchanged throughout) and the clean control re-PASSed
  byte-identical.
- The ladder stay of class 20421 is a scheduling statement measured
  here; it is NOT a class closure claim and NOT a root verdict.
- This lane runs without access to the user's computer (scheduled
  task); publication is via the GitHub API only.
- The probe-worklist (3.7 MB) stays unpublished per the standing
  size policy; pinned by sha256 only.

## Files

- DECLARATION.md - the Part declaration (copy of the published log).
- output/census-deltas-seventeenth-k02-adoption.json - measured
  census deltas (schema follows the fifteenth k02 reaudit census
  json).
- output/tamper-battery-stdout.log - the external tamper battery
  stdout (4/4 fail-closed + clean control re-PASS).
- reaudit/output/refresh-summary.json / closure-classes.csv /
  per-root-coverage.csv - the 3-run byte-identical SCEN refresh
  outputs.
- reaudit/scripts/refresh-adoption-seventeenth-k02.py - the refresh
  (3-region byte-clone of the sixteenth k01 refresh).
- scripts/measurer-adoption-seventeenth-k02.py - the measurer.
- scripts/refresh-adoption-seventeenth-k02.py - same refresh bytes at
  the kit-root scripts/ location (sixteenth k01 kit convention).
- MANIFEST.txt - sha256 of every published file.

## Status guard

Measurement bookkeeping only: NO verdict is consumed. Class-status
flips and the closure-ladder stay are census bookkeeping, not class
closures and not root verdicts. Class 20421 is NOT complete
(k03-k05 remain stage-1 2M UNKNOWN). The standard 11x11 empty
board, the 19 central-reply roots, the two-stone root {60,27} and
its remaining third moves 100/108 stay UNKNOWN. Nodes are
bookkeeping, never verdicts.
