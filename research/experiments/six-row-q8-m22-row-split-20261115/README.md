# six-row q=8 m=22 row-split sweep — (6,8) witness frontier

Date: 2026-11-15 (UTC). Fast lane, successor of K0829 (6x21 q=8 row-deficient
maximal nonexistence, witness-free width set {19,20,21}).

## Status

IN FLIGHT — this lane is actively running (single continuous session).
Do not start a parallel 6x22 q=8 lane. Machinery byte-identical to the K0829
lane: sat2.js + sat.js from seven-row-q7-witness-search-20261114/scripts
(blob shas 6c3262d6... / edfae1d2...), kissat 4.0.4 official linux-amd64
(md5 3a5eba830aa6008a604fcc9bbe99a325). Calibrations already bit-exact on
this machine: 6x21 q=8 rowY=1 UNSAT 2,862,649 conflicts (K0829 record
bit-exact), 6x18 q=8 def-OR SAT 492,432 conflicts + decoded 41-stone witness
rows [7,7,7,7,6,7] js verifyConfig PASS + Python Fraction PASS.

## Plan / intended claim

3 row-mirror rowY classes y=0,1,2 (complete coverage by the K0829 mirror
argument y<->5-y), generous per-class budget, plus a lex=H cross-encoding
re-check on the hardest class. If all UNSAT: 6x22 is row-deficient-maximal-free,
the witness-free width set of (6,8) extends to {19,20,21,22} and
M_{6,8} in {19,20,21,22} or >= 24; frontier moves to 6x23. If any class is
SAT: a decoded witness extends the witness band (M_{6,8} >= 23 candidate),
dual-verified (js census verifyConfig + Python Fraction).

Knowledge item: K0843 (provisional number; 5x30 lane plans K0842).

## Not claimed yet

Nothing. INDET at caps would be honest negatives, not absence.
