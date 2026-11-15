# 5x33 q=7 row-deficient maximal nonexistence — class-split sweep

Date: 2026-11-15 (UTC). Fast lane, successor of K0845 (5x32 witness-free).

## Status

IN FLIGHT — this lane claims the 5x33 q=7 witness-free judgment
(class-split sweep, 64 CNFs). Scripts are final; raw logs will be pushed
batch-by-batch as they are produced; records.jsonl / summary.json /
report.md land at completion. Claimed before execution started.

## Plan

- 17 direct row-mirror-canonical classes + {0},{1} k x minpos complete
  decomposition (k=0..4 and k=5 x minpos=0..16 — the m=33 minpos sound
  bound grows to floor((33-1)/2) = 16: columns 0..32,
  min(x_min, 32-x_max) <= 16, so 17 points per class, CNF set 64) + 2
  lex=H cross-checks + 5x18 positive control. kissat 4.0.4.
- Projected difficulty ~6.1M deciding conflicts (deciding totals are
  decreasing: m=23..32 = 20,916,467 -> 17,349,736 -> 15,521,919 ->
  13,845,697 -> 11,363,141 -> 10,218,568 -> 8,677,594 -> 7,809,347 ->
  7,275,763 -> 6,569,505).

## Scripts

mkcnf.sh (64 CNFs), qrun.sh (2-worker claim-directory queue runner),
mkrecords5733.js (records/summary builder), sat.js/sat2.js/sat3.js
byte-identical to the K0836..K0845 lane scripts (git blob shas
6c3262d6 / edfae1d2 / 6dfa7db3; md5 re-verified against the local m=32
lane; the control CNF c5x18q7_0.cnf regenerates md5-identical and the
control run reproduced 343,134 conflicts bit-exactly before the sweep).

## Next (if witness-free)

5x34: the minpos sound bound stays floor((34-1)/2) = 16 (17 points per
class, CNF set stays 64). Witness-free width set would extend to
{19,...,33}; sharp form M_{5,7} = 19 or >= 35.
