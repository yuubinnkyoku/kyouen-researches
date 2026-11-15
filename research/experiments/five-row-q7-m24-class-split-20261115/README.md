# 5x24 q=7 row-deficient maximal nonexistence — class-split sweep

**IN FLIGHT claim (fast lane, 2026-11-15).** Status: computing. Do not duplicate.

Successor of K0835 (5x23 witness-free). Extends the (5,7) witness-free sweep one width:
17 direct classes, {0}/{1} complete k x minpos decomposition (k = 0..4; k = 5 x
minpos = 0..11 — at m = 24 the sound bound is still floor((m-1)/2) = 11: x1 >= 12
forces mirror leftmost 23-x5 <= 11), lex=H cross-checks ({0,1}, {2}), positive control
5x18 {0} SAT (343,134 conflicts expected, bit-exact with the K0821/K0834/K0835 controls).

Encoder sat3.js (K0810 census, K0816/K0821/K0834/K0835 protocol), official kissat 4.0.4
linux-amd64, per-instance caps 60-260 s, raw logs pushed batch-by-batch. Outcomes:

- all UNSAT => witness-free width set of (5,7) = {19,20,21,22,23,24}, set form
  M in {19..24} or >= 25, sharp form M = 19 or >= 26; frontier moves to 5x25.
- any SAT => a deficient maximal safe configuration on 5x24 => M_{5,7} >= 25;
  model decoded and census-free verifyConfig-checked.
