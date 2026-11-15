# 5x32 q=7 row-deficient maximal nonexistence — class-split sweep

Date: 2026-11-15 (UTC). Fast lane, successor of K0844 (5x31 witness-free).

## Status

IN FLIGHT — claimed before the run. This lane decides 5x32 q=7
(witness-free or witness). 62 CNFs generated (17 direct classes + {0},{1}
k=0..4 + k=5 x minpos=0..15 — the minpos sound bound stays
floor((32-1)/2)=15, columns 0..31: min(x_min, 31-x_max) <= 15, 16 points
per class, plus 2 lex=H cross-checks and the 5x18 positive control). At
m=32 the minpos bound does NOT grow, so the CNF set stays 62 (same as
m=31).

## Claim (claimed, not yet verified)

Witness frontier of (5,7): widths 19..31 were verified witness-free
(K0738-K0759, K0816, K0821, K0834-K0842, K0844); this lane decides 5x32.
If UNSAT (expected — the deciding difficulty is monotonically decreasing
m=23..31: 20,916,467 -> ... -> 7,275,763, projected ~6.8M conflicts here),
the witness-free width set of (5,7) extends to {19,...,32}; set form
M_{5,7} in {19,...,32} or >= 33; sharp form (K0821-audit convention)
**M = 19 or >= 34**. Upper 158 (K0332 substitution) unchanged. Frontier
moves to 5x33.

## Scripts

mkcnf.sh (62 CNFs), qrun.sh (2-worker claim-directory queue runner),
mkrecords5732.js (records/summary builder; log-name templates match the
actual log names, no c prefix); sat.js/sat2.js/sat3.js byte-identical to
the K0836..K0842/K0844 lane scripts (copied from the local m=31 lane,
restored from main with blob shas 6c3262d6 / edfae1d2 / 6dfa7db3; md5
re-verified against the m=31 lane copies; the control CNF c5x18q7_0.cnf
regenerates md5-identical).

Raw logs will be pushed batch-by-batch as r5x32q7_*.txt.
