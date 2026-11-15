# six-row q=8 m=22 (and band continuation) row-split sweep — (6,8) witness frontier

Date: 2026-11-15 (UTC). Fast lane, successor of K0829 (6x21 q=8 row-deficient
maximal nonexistence, witness-free width set {19,20,21}).

## Status

- **Band m=22..44 COMPLETE — every width all 3 row-mirror rowY classes UNSAT
  (plus a lex=H cross-encoding re-check of the hardest class per width).**
  The witness-free width set of (6,8) is now **{19,...,44}**; M_{6,8} in
  {19,...,44} or >= 46 (sharp form per the K0821-audit convention: M = 19 or
  >= 46). Upper 371 (K0318/K0024 substitution) unchanged.
- Frontier width: 6x45. The predicted sat2.js all-triples census memory wall
  (extrapolated from the 7x28 n=196 rc137 incident) did NOT materialize:
  generation and solving stayed cheap through m=44 (n=264). Next steps in
  this lane: continue the same sat2.js rowY sweep (m=45, 46, ...) while it
  stays cheap; the genfast3.js switch (valid for q >= w+2; (6,8) qualifies
  with q=8=w+2) remains the fallback if generation cost or memory eventually
  walls, with a CNF byte-identity calibration against sat2.js before any
  genfast3-only width is claimed. Long-term: sweeping the band to m=370
  witness-free would, with U=371, close M_{6,8} = 19 exactly.

## Band results (kissat 4.0.4 official linux-amd64, all exit 20)

conflicts / process-time per instance; "deciding" = sum over the 3 rowY
classes (lex=H cross-check excluded).

| m | rowY=0 | rowY=1 (hardest) | rowY=2 | lex=H cross | deciding total |
|---|---|---|---|---|---|
| 22 | 337,741 / 15.20s | 2,162,296 / 127.19s | 1,791,570 / 95.14s | 1,862,336 / 114.92s | 4,291,607 |
| 23 | 335,230 / 14.11s | 1,810,456 / 107.92s | 776,370 / 36.62s | 1,659,164 / 104.66s | 2,922,056 |
| 24 | 251,593 / 10.41s | 1,630,859 / 101.26s | 599,993 / 28.11s | 1,537,786 / 97.16s | 2,482,445 |
| 25 | 236,900 / 9.86s | 1,404,703 / 78.46s | 438,783 / 20.85s | 1,190,336 / 65.70s | 2,080,386 |
| 26 | 156,508 / 7.22s | 990,038 / 49.75s | 412,481 / 18.03s | 918,270 / 47.60s | 1,559,027 |
| 27 | 157,697 / 7.61s | 786,169 / 38.20s | 295,947 / 13.36s | 771,797 / 39.67s | 1,239,813 |
| 28 | 108,238 / 4.85s | 583,705 / 27.43s | 217,461 / 9.26s | 605,585 / 28.77s | 909,404 |
| 29 | 82,831 / 4.25s | 482,137 / 22.89s | 211,837 / 9.68s | 474,291 / 22.23s | 776,805 |
| 30 | 204,178 / 9.15s | 385,419 / 17.53s | 160,357 / 7.61s | 329,657 / 17.21s | 749,954 |
| 31 | 214,319 / 10.15s | 400,693 / 19.39s | 130,995 / 6.97s | 351,655 / 17.41s | 746,007 |
| 32 | 249,964 / 12.03s | 299,427 / 14.94s | 113,507 / 5.95s | 256,550 / 13.54s | 662,898 |
| 33 | 273,720 / 13.65s | 210,820 / 10.55s | 85,752 / 4.44s | 198,993 / 10.31s | 570,292 |
| 34 | 236,543 / 11.20s | 175,116 / 9.64s | 91,526 / 5.05s | 161,884 / 9.17s | 503,185 |
| 35 | 167,284 / 9.07s | 124,021 / 7.19s | 76,265 / 4.22s | 149,515 / 8.62s | 367,570 |
| 36 | 214,784 / 10.63s | 134,327 / 7.65s | 82,548 / 4.50s | 97,529 / 6.62s | 431,659 |
| 37 | 160,244 / 8.91s | 115,414 / 7.36s | 67,031 / 4.13s | 100,168 / 6.67s | 342,689 |
| 38 | 144,271 / 8.41s | 115,643 / 7.13s | 68,262 / 4.28s | 96,678 / 6.32s | 328,176 |
| 39 | 134,185 / 8.13s | 99,560 / 6.34s | 52,317 / 3.37s | 90,299 / 6.24s | 286,062 |
| 40 | 95,625 / 6.07s | 82,449 / 5.76s | 47,194 / 3.22s | 80,272 / 5.67s | 225,268 |
| 41 | 91,670 / 6.26s | 69,692 / 5.13s | 42,010 / 3.18s | 79,155 / 5.54s | 203,372 |
| 42 | 94,471 / 6.17s | 56,759 / 4.64s | 46,264 / 3.57s | 63,345 / 5.00s | 197,494 |
| 43 | 83,296 / 6.12s | 54,643 / 4.77s | 37,520 / 2.96s | 72,852 / 5.81s | 175,459 |
| 44 | 107,765 / 7.52s | 73,372 / 5.54s | 41,643 / 3.42s | 63,396 / 5.41s | 222,780 |

The hardest-class conflict series (rowY=1) fell from 2,862,649 at m=21
(K0829) to 54,643 at m=43 (local minima 54,643 / 56,759 at m=43/42), i.e. by
a factor of ~52 across the band; deciding totals fell from 4,291,607 (m=22)
to ~200k (m=40..44 range 175,459..222,780 with local non-monotonicities —
e.g. m=44 at 222,780 is above m=43). No SAT witness and no generation or
memory wall so far; difficulty is collapsing as the width grows.

## Coverage argument (each width)

Identical to K0829: every deficient maximal safe configuration has some row
with <= 6 stones and appears as a solution of the rowfixed(y) instance for
that row; the V mirror y <-> 5-y is a board symmetry, so rowfixed(y) is
equisatisfiable with rowfixed(5-y) and y in {0,1,2} covers all 6 rows. The
lex=H instance re-decides the hardest class under a different encoding
(sequential-counter lex H constraints) as a cross-encoding check.

## Calibrations (all bit-exact)

- 6x21 q=8 rowY=1: UNSAT **2,862,649 conflicts** - bit-exact with the
  published K0829 record on the same CNF (md5 472a52be...). Reproduced twice
  in this session (182.35s and 173.80s runs, both 2,862,649).
- 6x18 q=8 def-OR positive control: SAT **492,432 conflicts** - bit-exact
  with the K0829 control; decoded 41-stone witness rows [7,7,7,7,6,7] is
  element-identical to the K0829 control board; js census-free verifyConfig
  PASS + Python Fraction verify_witness.py PASS. Reproduced twice
  (15.82s / 15.67s, both 492,432).
- 6x26 CNF regeneration check (this batch): re-running sat2.js for all four
  m=26 encodings after the sweep reproduced the on-disk CNFs byte-identical
  (cmp PASS on rowY0 and rowY1_lexH; meta re-derived verbatim), recovering
  the meta_26.json that the sweep script had not captured.

## Honest negative

- 6x24 q=8 def-OR (deficient-mode single-instance OR encoding): INDET at
  the 140s cap, 3,248,777 conflicts - honest negative, not absence;
  nonexistence for m=24 rests on the 3-class rowY split. Def-mode difficulty
  is decreasing too (m=21: 5,011,833 at 240s, K0829 -> m=24: 3,248,777 at
  140s).

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

- 6x45 and above until the corresponding sweeps finish (frontier: 6x45).
- Any band width decided only by genfast3.js before its CNF byte-identity
  calibration against sat2.js passes on shared widths.
- 11x11 empty board, two-stone root {49,60}, S2 {59,60}, class 2, class 4:
  UNKNOWN, unaffected.
- INDET at caps would be honest negatives, not absence.
