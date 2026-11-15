# 5x32 q=7 row-deficient maximal nonexistence — class-split sweep

Date: 2026-11-15 (UTC). Fast lane, successor of K0844 (5x31 witness-free).

## Status

IN FLIGHT — this lane claims the 5x32 q=7 witness-free determination
(62 CNFs). Calibration already re-verified: the 5x18 class {0} positive
control solved SAT 343,134 conflicts (bit-exact with the
K0821..K0844 lane controls, eleventh cross-lane reproduction), decoded
29 stones rows (5,6,6,6,6), census-free verifyConfig PASS.

## Claim

Witness frontier of (5,7): widths 19..31 were verified witness-free
(K0738-K0759, K0816, K0821, K0834-K0842, K0844); this lane decides 5x32.
If all instances are UNSAT the witness-free width set of (5,7) becomes
{19,...,32}; set form M_{5,7} in {19,...,32} or >= 33; sharp form
(K0821-audit convention) **M = 19 or >= 34**. Upper 158 (K0332
substitution) unchanged. Frontier would move to 5x33.

## Instances

62 CNFs: 17 direct row-occupancy classes + {0},{1} krow k=0..4 (10) +
{0},{1} k=5 x minpos=0..15 (32 — the m=32 sound bound stays
floor((32-1)/2)=15, 16 points per class, columns 0..31:
min(x_min, 31-x_max) <= 15) + 2 lex=H cross-checks + the 5x18 positive
control. kissat 4.0.4 (official rel-4.0.4 binary, md5 verified).

## Scripts

mkcnf.sh (62 CNFs), qrun.sh (2-worker claim-directory queue runner),
mkrecords5732.js (records/summary builder; log-name templates match the
pushed raw-log names); sat.js/sat2.js/sat3.js byte-identical to the m=31
lane scripts (restored from main, git blob shas verified:
6c3262d67698 / edfae1d2c518 / 6dfa7db3ac6c). mkcnf.sh/qrun.sh ported
m=31 -> m=32 (identifier grep verified, no stale m=31 identifiers).
