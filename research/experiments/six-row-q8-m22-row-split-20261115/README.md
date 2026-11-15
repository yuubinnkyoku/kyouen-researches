# six-row q=8 m=22 (and band continuation) row-split sweep — (6,8) witness frontier

Date: 2026-11-15 (UTC). Fast lane, successor of K0829 (6x21 q=8 row-deficient
maximal nonexistence, witness-free width set {19,20,21}).

## Status

- **Band m=22..59 COMPLETE — every width all 3 row-mirror rowY classes UNSAT
  (plus a lex=H cross-encoding re-check of the hardest class per width).**
  The witness-free width set of (6,8) is now **{19,...,59}**; M_{6,8} in
  {19,...,59} or >= 61 (sharp form per the K0821-audit convention: M = 19 or
  >= 61). Upper 371 (K0318/K0024 substitution) unchanged.
- Frontier width: 6x60 — blocked by the sat2.js generation RAM wall at m=60
  (see the wall section), not by solver difficulty. Long-term: sweeping the band to m=370 witness-free
  would, with U=371, close M_{6,8} = 19 exactly.

## Band results (kissat 4.0.4 official linux-amd64, all exit 20)

conflicts / process-time per instance; "deciding" = sum over the 3 rowY
classes (lex=H cross-check excluded).

| m | rowY=0 | rowY=1 | rowY=2 | lex=H cross | deciding total |
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
| 45 | 79,347 / 6.20s | 54,964 / 4.61s | 46,073 / 3.92s | 61,851 / 5.42s | 180,384 |
| 46 | 71,714 / 5.84s | 53,691 / 4.46s | 35,846 / 3.20s | 58,028 / 5.09s | 161,251 |
| 47 | 70,742 / 5.42s | 68,550 / 5.89s | 39,530 / 3.48s | 48,259 / 4.69s | 178,822 |
| 48 | 66,059 / 5.46s | 47,052 / 4.49s | 36,867 / 3.65s | 50,355 / 4.74s | 149,978 |
| 49 | 66,813 / 5.68s | 48,356 / 4.27s | 36,583 / 3.47s | 48,663 / 4.41s | 151,752 |
| 50 | 65,554 / 5.58s | 59,091 / 4.73s | 32,307 / 3.13s | 48,947 / 4.40s | 156,952 |
| 51 | 78,979 / 6.64s | 66,512 / 6.05s | 36,454 / 4.01s | 57,575 / 5.13s | 181,945 |
| 52 | 95,765 / 7.04s | 66,280 / 5.37s | 33,978 / 3.28s | 73,468 / 6.09s | 196,023 |
| 53 | 98,308 / 7.37s | 99,031 / 6.94s | 33,251 / 3.13s | 73,104 / 6.49s | 230,590 |
| 54 | 109,295 / 8.50s | 89,971 / 7.88s | 32,535 / 3.49s | 73,563 / 7.01s | 231,801 |
| 55 | 130,116 / 9.50s | 76,771 / 6.11s | 28,309 / 3.34s | 82,902 / 6.71s | 235,196 |
| 56 | 96,816 / 7.35s | 69,459 / 6.25s | 31,733 / 3.61s | 81,988 / 7.24s | 198,008 |
| 57 | 102,785 / 8.04s | 71,298 / 6.20s | 32,824 / 3.85s | 62,783 / 6.54s | 206,907 |
| 58 | 96,183 / 8.44s | 105,216 / 9.15s | 30,019 / 4.07s | 76,539 / 7.75s | 231,418 |
| 59 | 95,418 / 8.72s | 71,086 / 7.70s | 29,466 / 4.20s | 76,036 / 7.80s | 195,970 |

Difficulty shape: the deciding totals fell from 4,291,607 (m=22) to a
**local minimum 149,978 at m=48**, then turned and **rose again**
(151,752 / 156,952 / 181,945 / 196,023 / 230,590 / 231,801 / 235,196 for
m=49..55), then levelled off (198,008 / 206,907 / 231,418 / 195,970 for
m=56..59). The hardest class is no longer fixed: from m=44 on it alternates
between y=0 and y=1 (m=53: y=1 at 99,031; m=54/55: y=0 at 109,295 /
130,116; m=58: y=1 at 105,216). The m=56..59 leg is still 18x below the
m=22 start. No SAT witness anywhere in the band.

## Coverage argument (each width)

Identical to K0829: every deficient maximal safe configuration has some row
with <= 6 stones and appears as a solution of the rowfixed(y) instance for
that row; the V mirror y <-> 5-y is a board symmetry, so rowfixed(y) is
equisatisfiable with rowfixed(5-y) and y in {0,1,2} covers all 6 rows. The
lex=H instance re-decides the rowY=1 class under a different encoding
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
- 6x26 CNF regeneration check (m26..31 batch): re-running sat2.js for all
  four m=26 encodings after the sweep reproduced the on-disk CNFs
  byte-identical (cmp PASS on rowY0 and rowY1_lexH; meta re-derived
  verbatim), recovering the meta_26.json that the sweep script had not
  captured.
- **Environment-reset crossing (m45..55 batch)**: a hard environment reset
  wiped the local workdir mid-session (after the m45..47 sweeps, before
  their logs were pushed). All machinery was re-fetched from this repo and
  re-verified by hash (sat.js 6c3262d6..., sat2.js edfae1d2...,
  verify_witness.py ea7203a3..., decode_verify.js ef5390509b..., kissat
  4.0.4 md5 3a5eba830aa6008a604fcc9bbe99a325). m=45, 46, 47 were re-run on
  the rebuilt environment and every conflict count was **bit-exact** with
  the pre-reset runs (79,347 / 46,073 / 54,964 / 61,851; 71,714 / 35,846 /
  53,691 / 58,028; 70,742 / 39,530 / 68,550 / 48,259) — a cross-reset
  determinism calibration of the whole toolchain.

## The m=53 heap wall and the m=60 RAM wall

At m=53 (n=318) the sat2.js CNF generation died with a V8 default-heap OOM
(~512 MB, "Ineffective mark-compacts near heap limit") in all four
encodings — the memory wall predicted from the 7-row lane's n=196 rc137
incident, arriving later than extrapolated (the earlier prediction was
m≈32-33) because it is a V8 heap-limit artifact, not a RAM wall. Re-running
with `node --max-old-space-size=3500` (later 900) generates m=53..59 in
10-20 s per instance; m=53..59 were produced this way (sweep_width.sh now
carries the flag). At **m=60 the wall became real**: the census needs
~750 MB and the environment RAM cap sits just below/around it —
--max-old-space-size=900 generated one m=60 CNF but the next run was
kernel-killed (rc 137); 1400 is killed instantly; 800 dies with a JS heap
OOM at ~585 MB. **sat2.js band frontier: m=59 (free); m=60 blocked by
generation memory, not by the solver.** The designed fallback is the
genfast3.js generator (valid for q >= w+2; (6,8) qualifies with q=8=w+2),
to be calibrated by CNF byte-identity against sat2.js on shared widths
before any genfast3-only width is claimed.

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
verifier - see scripts/. Since m=53 the generator runs with an explicit
`--max-old-space-size` flag (3500 for m=53..59's first runs, 900 from the
m=56 batch on; see the wall section); this changes no output, only the
heap ceiling.

## Incident note

The first push of the two calibration raw logs landed truncated (the
sandbox read_file 64KB page limit; only page 1 was read). Both files were
repushed complete and remote git blob shas now match the local files
(0cdf6de1... / 952629af...). All other raw logs were under 64KB and landed
byte-exact on the first push. (Large batches are now staged through local
JSON to stay under the sandbox 16 MiB op-recording limit.)

## Not claimed

- 6x60 and above until the genfast3.js switch is calibrated (frontier: 6x60,
  blocked by the sat2.js generation RAM wall at m=60, not by difficulty).
- Any band width decided only by genfast3.js before its CNF byte-identity
  calibration against sat2.js passes on shared widths.
- 11x11 empty board, two-stone root {49,60}, S2 {59,60}, class 2, class 4:
  UNKNOWN, unaffected.
- INDET at caps would be honest negatives, not absence.
