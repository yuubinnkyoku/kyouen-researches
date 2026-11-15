# 5x35 q=7 row-deficient maximal nonexistence — class-split sweep

Date: 2026-11-15 (UTC). Fast lane, successor of K0847 (5x34 witness-free).

## Status

IN FLIGHT — claim staked before the sweep. 66 CNFs generated (17 direct
classes + {0},{1} k=0..4 + k=5 x minpos=0..17 + 2 lex=H cross-checks + the
5x18 positive control). Positive control run before the sweep: 5x18 class
{0} SAT 343,134 conflicts, bit-exact with the K0821..K0847 lane controls
(fourteenth cross-lane reproduction) — encoder + solver path confirmed.

## Claim

Witness frontier of (5,7): widths 19..34 were verified witness-free
(K0738-K0759, K0816, K0821, K0834-K0842, K0844, K0845, K0846, K0847);
this lane decides 5x35. If all deciding instances come back UNSAT, the
witness-free width set of (5,7) becomes {19,...,35}; set form M_{5,7} in
{19,...,35} or >= 36; sharp form (K0821-audit convention) **M = 19 or
>= 37** (M = 36 would require a witness at the verified witness-free
width 35). Upper 158 (K0332 substitution) unchanged. Frontier would move
to 5x36.

## Setup

mkcnf.sh (66 CNFs — the minpos sound bound grows to floor((35-1)/2) = 17,
18 points per class, columns 0..34: min(x_min, 34-x_max) <= 17), qrun.sh
(2-worker claim-directory queue runner), mkrecords5735.js
(records/summary builder; log-name templates match the pushed raw-log
names); sat.js/sat2.js/sat3.js byte-identical to the K0836..K0847 lane
scripts (restored from the m=34 lane on main, git blob shas verified
6c3262d6 / edfae1d2 / 6dfa7db3; the control CNF c5x18q7_0.cnf
regenerates md5-identical 0bb6187d36e537a170e4fb451359bb94). kissat
4.0.4 (official rel-4.0.4 linux-amd64 asset, binary md5
3a5eba830aa6008a604fcc9bbe99a325).
