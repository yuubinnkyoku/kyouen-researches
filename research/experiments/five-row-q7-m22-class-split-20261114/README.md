# five-row q=7 m=22 class-split — takeover + completion record

Date: 2026-11-15 (UTC). Fast lane takeover of the stalled batch-1 lane, completed the same day.

## Situation

Batch 1 (2026-11-14T15:25:57Z, commit 1029a0db) pushed 19 raw logs and stopped:

- 17/19 direct classes **UNSAT** (hardest {0,1}: 875,682 conflicts; {0,2,3} log complete:
  199,205 conflicts / 5.9 s);
- {0} and {1} plain instances **INDET** (SIGTERM at ~142 s process time each);
- no report, records, summary, or IN FLIGHT claim followed; the lane had been silent
  for 8+ hours.

The takeover claim was pushed at b637ba8e before any recomputation.

## Result (see report.md, K0834)

**All 19 canonical classes UNSAT — no row-deficient maximal safe configuration exists on
5x22 q=7**; every maximal safe configuration on 5x22 has 30 stones (row occupancy
(6,6,6,6,6)):

- 17 direct classes re-run by this lane reproduce the batch-1 conflict counts
  **bit-exactly (17/17)**.
- {0} and {1} decided by the complete k × minpos decomposition (the K0816/K0821
  protocol): k = 0..4 (krow-only) and k = 5 × minpos = 0..10 — all 32 sub-instances
  UNSAT (hardest {0} k=5 mp=0: 3,380,578 conflicts / 153.8 s; {1} k=5 mp=0:
  3,111,756 / 144.1 s).
- lex=H cross-encoding re-checks on {0,1} and {2}: UNSAT again (627,149 / 310,356).
- Positive control: 5x18 class {0} **SAT** — 343,134 conflicts, bit-exact with the K0821
  lane control; decoded 29 stones rows (5,6,6,6,6), census-free verifyConfig PASS
  (K0332 witness rediscovered end-to-end).
- Deciding-instance conflicts 24,581,763 total (17 direct: 5,256,816; 32 decomposition:
  19,324,947); records total 25,519,268; INDET 0, SAT 0 among deciding instances.

Consequence (with K0738–K0759, K0816, K0821, K0332): the witness-free width set of (5,7)
is **{19, 20, 21, 22}**, so **M_{5,7} ∈ {19, 20, 21, 22} or M_{5,7} ≥ 23**; upper bound 158
(K0332/K0024 substitution) unchanged. The witness-search frontier moves to 5x23.

## Not claimed

- 5x23+, other (w,q), the six-row frontier (see
  ../six-row-q7-m22-class-split-20261115/README.md), 11x11 lanes.

## Status

COMPLETED — raw logs, records, summary, report, scripts and the K0834 item are on main.
