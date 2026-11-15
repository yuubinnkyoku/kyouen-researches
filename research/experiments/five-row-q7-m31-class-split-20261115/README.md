# 5x31 q=7 row-deficient maximal nonexistence — class-split sweep

Date: 2026-11-15 (UTC). Fast lane, successor of K0842 (5x30 witness-free).

## Status

IN FLIGHT — 62 CNFs generated (17 direct classes + {0},{1} k=0..4 + k=5 x
minpos=0..15 — the m=31 sound bound grows to floor((31-1)/2)=15, 16 points
per class — plus 2 lex=H and the 5x18 control). Raw logs pushed
batch-by-batch. Unclaimed status verified against latest main before
starting (no five-row-q7-m31 mentions; the (5,7) frontier sat at 5x31 after
K0842).

## Claim (in flight)

Witness frontier of (5,7): widths 19..30 were verified witness-free
(K0738-K0759, K0816, K0821, K0834-K0842); this lane decides 5x31. If all
59 deciding instances are UNSAT, the witness-free width set of (5,7)
becomes {19,...,31}; set form M_{5,7} in {19,...,31} or >= 32; sharp form
(K0821-audit convention) **M = 19 or >= 33**. Upper 158 (K0332
substitution) unchanged. Frontier would move to 5x32.

## Scripts

mkcnf.sh (62 CNFs), qrun.sh (2-worker claim-directory queue runner, per-
instance timeout caps), mkrecords5731.js (records/summary builder;
log-name templates match the actual log names — no c prefix on
direct/lexH logs, per the m=30 lane lesson); sat.js/sat2.js/sat3.js are
byte-identical to the K0836..K0842 lane scripts (blob shas 6c3262d6 /
edfae1d2 / 6dfa7db3, copied from the local m=30 lane restored from main).

## Verification protocol (same as m=21..30)

Positive control 5x18 class {0} must reproduce SAT 343,134 conflicts
bit-exact with the ten lane controls (K0821..K0842); lex=H cross-encoding
re-checks on {0,1},{2}; decomposition soundness: k=0..5 partitions the
deficient-row stone count, minpos pins the leftmost stone of the first
deficient row at column exactly P, and every configuration or its column
mirror has leftmost stone column <= 15 at m=31 (columns 0..30:
min(x_min, 30-x_max) <= 15).

## Next (if witness-free)

5x32: minpos sound bound grows to floor((32-1)/2)=15 (16 points per
class stays; columns 0..31: min(x_min, 31-x_max) <= 15), CNF set stays
62. Deciding difficulty still decreasing (m=23..30: 20,916,467 ->
17,349,736 -> 15,521,919 -> 13,845,697 -> 11,363,141 -> 10,218,568 ->
8,677,594 -> 7,809,347); m=31 projected ~7M conflicts.
