# 5x30 q=7 row-deficient maximal nonexistence — class-split sweep

Date: 2026-11-15 (UTC). Fast lane, successor of K0841 (5x29 witness-free).

## Status

IN FLIGHT — this lane is actively running (single continuous session).
Do not start a parallel 5x30 lane. Scripts restored byte-identically from the
m=29 lane (sat.js/sat2.js/sat3.js; mkcnf.sh/qrun.sh ported m=29 -> m=30),
60 CNFs regenerated deterministically (17 direct + {0},{1} k=0..4 + k=5 x
minpos=0..14 — the m=30 sound bound stays floor((30-1)/2)=14, 15 points per
class — plus 2 lex=H and the 5x18 control). Raw logs will be pushed
batch-by-batch; records/summary on completion. Knowledge item: K0842
(planned).

## Claim (intended)

Witness frontier of (5,7): widths 19..29 are verified witness-free
(K0738-K0759, K0816, K0821, K0834-K0841); this lane decides 5x30. If all 19
row-mirror-canonical deficiency classes are UNSAT, the witness-free width set
of (5,7) becomes {19,...,30}; set form M_{5,7} in {19,...,30} or >= 31; sharp
form (K0821-audit convention) M = 19 or >= 32. Upper 158 (K0332 substitution)
unchanged. Frontier would move to 5x31.
