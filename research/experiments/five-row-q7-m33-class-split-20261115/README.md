# 5x33 q=7 row-deficient maximal nonexistence — class-split sweep

Date: 2026-11-15 (UTC). Fast lane, successor of K0845 (5x32 witness-free).

## Status

COMPLETE — all 64 records decided: 61 deciding instances UNSAT (17 direct
classes + {0},{1} k=0..4 + k=5 x minpos=0..16), 2 lex=H cross-checks UNSAT,
positive control SAT. **5x33 q=7 is witness-free.** Raw logs pushed
batch-by-batch (batch-1 pre-reset on main byte-exact; batches 2-4 after a
full environment reset, recovered by the established protocol: scripts
restored from main with git blob shas verified, kissat re-downloaded from
the official rel-4.0.4 asset (md5 3a5eba83...), CNFs regenerated, control
343,134 and c01 334,184 reproduced bit-exactly). See report.md and
records.jsonl / summary.json. Knowledge item: K0846.

## Claim

Witness frontier of (5,7): widths 19..32 were verified witness-free
(K0738-K0759, K0816, K0821, K0834-K0842, K0844, K0845); this lane decides
5x33 — witness-free. The witness-free width set of (5,7) is now
{19,...,33}; set form M_{5,7} in {19,...,33} or >= 34; sharp form
(K0821-audit convention) **M = 19 or >= 35**. Upper 158 (K0332
substitution) unchanged. Frontier moves to 5x34.

## Results

- 17 direct classes all UNSAT: hardest {0,1} 334,184 conflicts (+16.5% vs
  its m=32 counterpart — the direct-hardest series is no longer
  monotone); direct total 1,804,062 (+3.9% vs m=32 1,735,912 — the first
  direct-total non-decrease in the m=22..33 series: 5,256,816 -> 4,673,619
  -> 4,160,006 -> 3,534,969 -> 3,307,565 -> 2,656,426 -> 2,503,468 ->
  2,261,532 -> 1,960,401 -> 1,916,295 -> 1,735,912 -> 1,804,062) + lex=H
  cross-checks on {0,1},{2} UNSAT (241,070 / 99,898 conflicts).
- {0},{1} krow k=0..4 all UNSAT (10 instances; hardest {1} k=4: 356,896 /
  {0} k=4: 218,095; krow total 760,709).
- {0},{1} k=5 x minpos=0..16 all UNSAT (34 instances — the minpos sound
  bound grows to floor((33-1)/2)=16 at m=33, 17 points per class; hardest
  {1} k=5 mp=0: 651,985 / 25.39 s — down 2.7% from its m=32 counterpart
  670,375; {0} k=5 mp=0: 446,878 — up 0.7% from 443,637, the second
  consecutive k5p0 non-decrease; {0}k5p total 1,480,222; {1}k5p total
  2,095,616).
- Positive control: 5x18 class {0} SAT 343,134 conflicts, bit-exact with
  the K0821..K0845 lane controls (twelfth cross-lane reproduction);
  decoded 29 stones rows (5,6,6,6,6), census-free verifyConfig PASS.
- Deciding 61 instances total 6,140,609 conflicts (17 direct 1,804,062 +
  10 krow 760,709 + 34 k=minpos 3,575,838); deciding+lex=H 6,481,577
  (= total_conflicts_33, same convention as m=27..m=32 summaries);
  records total 6,824,711; INDET 0, SAT 0.

## Scripts

mkcnf.sh (64 CNFs — 17 direct + 44 k/minpos with the minpos sound bound
floor((33-1)/2)=16, i.e. minpos=0..16 = 17 points per class, plus 2 lex=H
and the 5x18 control), qrun.sh (2-worker claim-directory queue runner),
mkrecords5733.js (records/summary builder; log-name templates match the
pushed raw-log names); sat.js/sat2.js/sat3.js are byte-identical to the
K0836..K0845 lane scripts (git blob shas 6c3262d6 / edfae1d2 / 6dfa7db3;
the control CNF c5x18q7_0.cnf regenerates md5-identical).

## Next

5x34: the minpos sound bound stays floor((34-1)/2) = 16 (17 points per
class, columns 0..33: min(x_min, 33-x_max) <= 16 — the CNF set stays 64).
Deciding totals keep decreasing on average (m=23..33: 20,916,467 ->
17,349,736 -> 15,521,919 -> 13,845,697 -> 11,363,141 -> 10,218,568 ->
8,677,594 -> 7,809,347 -> 7,275,763 -> 6,569,505 -> 6,140,609), but the
m=33 direct-total non-decrease means the ~6M projection for m=34 should
be treated as approximate; m=34 projected ~5.7M conflicts.
