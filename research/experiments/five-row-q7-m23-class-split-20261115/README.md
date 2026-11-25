# 5x23 q=7 row-deficient maximal nonexistence — class-split sweep

Date: 2026-11-15 (UTC). Fast lane, successor of K0834 (5x22 witness-free).

## Result (see report.md, K0835)

**All 19 canonical classes UNSAT — no row-deficient maximal safe configuration exists on
5x23 q=7**; every maximal safe configuration on 5x23 has 30 stones (row occupancy
(6,6,6,6,6)):

- 17 direct classes UNSAT (hardest {0,1}: 708,108 conflicts / 22.3 s; direct total
  4,673,619 — slightly easier than m=22's 5,256,816, continuing the flat-to-decreasing
  difficulty trend).
- {0} and {1} decided by the complete k × minpos decomposition (the K0816/K0821/K0834
  protocol): k = 0..4 (krow-only, 10 UNSAT) and k = 5 × minpos = 0..11 (24 UNSAT; the
  sound bound grows to floor((m−1)/2) = 11 at m = 23). Hardest:
  {1} k=5 mp=0: 2,555,137 conflicts / 107.96 s; {0} k=5 mp=0: 2,135,466 / 89.5 s.
- lex=H cross-encoding re-checks on {0,1} and {2}: UNSAT again (504,359 / 321,039).
- Positive control: 5x18 class {0} **SAT** — 343,134 conflicts, bit-exact with the
  K0821/K0834 lane controls; decoded 29 stones rows (5,6,6,6,6), census-free verifyConfig
  PASS (K0332 witness rediscovered end-to-end).
- Deciding-instance conflicts 20,916,467 total (17 direct: 4,673,619; 34 decomposition:
  16,242,848); records total 22,084,999; INDET 0, SAT 0 among the deciding instances
  (51 deciding instances: 17 direct + 34 decomposition).

Consequence (with K0738–K0759, K0816, K0821, K0834, K0332): the witness-free width set of
(5,7) is **{19, 20, 21, 22, 23}**; set form **M_{5,7} ∈ {19,20,21,22,23} or ≥ 24**,
sharp form (K0821-audit convention) **M_{5,7} = 19 or M_{5,7} ≥ 25** (M = 24 would need
a witness at the verified witness-free width 23); upper bound 158 (K0332/K0024
substitution) unchanged. The witness-search frontier moves to 5x24.

## Operational note

The local scratch was lost to an execution-environment reset mid-sweep (27/51 deciding
instances finished locally pre-reset). The sweep was fully re-run from freshly generated
CNFs and the official kissat 4.0.4 linux-amd64 release binary; all pre-reset instances
reproduce their conflict counts bit-exactly in the re-run, and the raw logs were pushed
batch-by-batch (batches 1–4) so no evidence could be lost again.

## Not claimed

- 5x24+, other (w,q), the six-row frontier, 11x11 lanes.

## Status

COMPLETED — raw logs (54), records.jsonl, summary.json, scripts (sat.js/sat2.js/sat3.js,
mkcnf.sh, qrun.sh, mkrecords5723.js), report.md and the K0835 item are on main.
