# 5x29 q=7 row-deficient maximal nonexistence — class-split sweep

Date: 2026-11-15 (UTC). Fast lane, successor of K0840 (5x28 witness-free).

## Status

IN FLIGHT — claimed by the fast lane at 2026-11-15T03:15Z. Scripts ported
from the 5x28 lane (sat.js/sat2.js/sat3.js byte-identical; mkcnf.sh/qrun.sh
ported m=28 -> m=29, minpos sound bound grows to floor((29-1)/2)=14, 15
points per class, CNF set grows to 60: 17 direct + 10 krow + 30 k=5 x
minpos=0..14 + 2 lex=H cross-checks + 1 positive control). Raw logs are
pushed batch-by-batch; this README is updated to COMPLETE when all 60
instances are decided. Knowledge item (planned): K0841.

## Claim (target)

Witness frontier of (5,7): widths 19..28 are verified witness-free
(K0738-K0759, K0816, K0821, K0834-K0840); this lane decides 5x29. If all
deciding instances are UNSAT, the witness-free width set of (5,7) becomes
{19,...,29}; set form M_{5,7} in {19,...,29} or >= 30; sharp form
(K0821-audit convention) M = 19 or >= 31. Upper 158 (K0332 substitution)
unchanged. Frontier would move to 5x30.
