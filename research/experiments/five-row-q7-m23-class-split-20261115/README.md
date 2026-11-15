# 5x23 q=7 row-deficient maximal nonexistence — class-split sweep

**IN FLIGHT claim (fast lane, 2026-11-15).** Status: computing. Do not duplicate.

Successor of K0834 (5x22 witness-free, all 19 canonical classes UNSAT). Extends the
(5,7) witness-free sweep one width: 17 direct classes, {0}/{1} complete k x minpos
decomposition (k = 0..4; k = 5 x minpos = 0..11 — at m = 23 every configuration or its
column mirror has leftmost stone column <= floor((m-1)/2) = 11), lex=H cross-checks
({0,1}, {2}), positive control 5x18 {0} SAT (343,134 conflicts expected, K0332 witness).

Encoder sat3.js (K0810 census, K0816/K0821/K0834 protocol), official kissat 4.0.4
linux-amd64, per-instance cap 260 s. Outcomes:

- all UNSAT => witness-free width set of (5,7) = {19,20,21,22,23}, M_{5,7} = 19 or >= 25
  (K0821-audit sharpening convention); frontier moves to 5x24.
- any SAT => a deficient maximal safe configuration on 5x23 (29 stones) =>
  M_{5,7} >= 24; model decoded and census-free verifyConfig-checked.
