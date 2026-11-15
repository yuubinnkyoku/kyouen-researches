# six-row q=8 m=22 (and band continuation) row-split sweep — (6,8) witness frontier

Date: 2026-11-15 (UTC). Fast lane, successor of K0829 (6x21 q=8 row-deficient
maximal nonexistence, witness-free width set {19,20,21}).

## Status

- **6x22 COMPLETE — all 3 row-mirror rowY classes UNSAT**: 6x22 q=8 is
  row-deficient-maximal-free. The witness-free width set of (6,8) is now
  {19,20,21,22}; M_{6,8} in {19,20,21,22} or >= 24 (sharp form per the
  K0821-audit convention: M = 19 or >= 24). Upper 371 (K0318/K0024
  substitution) unchanged.
- Band continuation IN FLIGHT: 6x23 sweep running in the same session
  (machinery identical). Each further width extends the free set by one.

## 6x22 results (kissat 4.0.4 official linux-amd64, exit 20)

| instance | conflicts | process-time | verdict |
|---|---|---|---|
| rowY=0 | 337,741 | 15.20s | UNSAT |
| rowY=1 (hardest) | 2,162,296 | 127.19s | UNSAT |
| rowY=2 | 1,791,570 | 95.14s | UNSAT |
| rowY=1 --lex=H cross-encoding | 1,862,336 | 114.92s | UNSAT |

Coverage argument identical to K0829: every deficient maximal safe
configuration has some row with <= 6 stones and appears as a solution of the
rowfixed(y) instance for that row; the V mirror y <-> 5-y is a board symmetry,
so rowfixed(y) is equisatisfiable with rowfixed(5-y) and y in {0,1,2} covers
all 6 rows. Deciding total: 4,291,607 conflicts across 3 instances
(lex=H cross-check excluded). Difficulty did not grow from m=21 to m=22
(rowY=1: 2,862,649 -> 2,162,296, easier; rowY=0: 327,636 -> 337,741;
rowY=2: 1,767,690 -> 1,791,570) - no wall at the K0829 frontier width.

## Calibrations (all bit-exact)

- 6x21 q=8 rowY=1: UNSAT **2,862,649 conflicts** - bit-exact with the
  published K0829 record on the same CNF (md5 472a52be...). Reproduced twice
  in this session (182.35s and 173.80s runs, both 2,862,649).
- 6x18 q=8 def-OR positive control: SAT **492,432 conflicts** - bit-exact
  with the K0829 control; decoded 41-stone witness rows [7,7,7,7,6,7] is
  element-identical to the K0829 control board; js census-free verifyConfig
  PASS + Python Fraction verify_witness.py PASS. Reproduced twice
  (15.82s / 15.67s, both 492,432).

## Machinery

sat2.js + sat.js (K0810 census + sequential counter + maximality) verbatim
from seven-row-q7-witness-search-20261114/scripts (blob shas 6c3262d6... /
edfae1d2...); verify_witness.py (ea7203a3...); kissat 4.0.4 official
linux-amd64 (md5 3a5eba830aa6008a604fcc9bbe99a325). decode_verify.js
(NEW, this lane): decodes the kissat model into stones and runs the js
verifier - see scripts/.

## Incident note

The first push of the two calibration raw logs landed truncated (the
sandbox read_file 64KB page limit; only page 1 was read). Both files were
repushed complete and remote git blob shas now match the local files
(0cdf6de1... / 952629af...). All other raw logs were under 64KB and landed
byte-exact on the first push.

## Not claimed

- 6x23+ until the corresponding sweeps finish (band continuation in flight).
- 11x11 empty board, two-stone root {49,60}, S2 {59,60}, class 2, class 4:
  UNKNOWN, unaffected.
- INDET at caps would be honest negatives, not absence.
