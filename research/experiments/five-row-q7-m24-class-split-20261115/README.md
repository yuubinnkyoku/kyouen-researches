# 5x24 q=7 row-deficient maximal nonexistence — class-split sweep

Date: 2026-11-15 (UTC). Fast lane, successor of K0835 (5x23 witness-free).

## Result (see report.md, K0836)

**All 19 canonical classes UNSAT — no row-deficient maximal safe configuration exists on
5x24 q=7**; every maximal safe configuration on 5x24 has 30 stones (row occupancy
(6,6,6,6,6)):

- 17 direct classes UNSAT (hardest {0,1}: 707,981 conflicts / 23.7 s; direct total
  4,160,006 — the difficulty trend across m=21..24 is clearly decreasing:
  5,256,816 → 4,673,619 → 4,160,006).
- {0} and {1} decided by the complete k × minpos decomposition (the
  K0816/K0821/K0834/K0835 protocol): k = 0..4 (krow-only, 10 UNSAT) and k = 5 ×
  minpos = 0..11 (24 UNSAT; sound bound floor((m−1)/2) = 11 at m = 24). Hardest:
  {1} k=5 mp=0: 2,282,668 conflicts / 92.83 s; {0} k=5 mp=0: 1,745,942 / 74.97 s.
- lex=H cross-encoding re-checks on {0,1} and {2}: UNSAT again (555,120 / 296,008).
- Positive control: 5x18 class {0} **SAT** — 343,134 conflicts, bit-exact with the
  K0821/K0834/K0835 lane controls (third cross-lane reproduction); decoded 29 stones
  rows (5,6,6,6,6), census-free verifyConfig PASS.
- Deciding-instance conflicts 17,349,736 total (17 direct: 4,160,006; 34 decomposition:
  13,189,730); records total 18,543,998; INDET 0, SAT 0 among the 51 deciding instances.

Consequence (with K0738–K0759, K0816, K0821, K0834, K0835, K0332): the witness-free
width set of (5,7) is **{19, 20, 21, 22, 23, 24}**; set form **M_{5,7} ∈ {19,...,24} or
≥ 25**, sharp form (K0821-audit convention) **M_{5,7} = 19 or M_{5,7} ≥ 26** (M = 25
would need a witness at the verified witness-free width 24); upper bound 158
(K0332/K0024 substitution) unchanged. The witness-search frontier moves to 5x25.

## Status

COMPLETED — raw logs (54), records.jsonl, summary.json, scripts (sat.js/sat2.js/sat3.js,
mkcnf.sh, qrun.sh, mkrecords5724.js), report.md and the K0836 item are on main.
