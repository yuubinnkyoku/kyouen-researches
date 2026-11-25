# 5x35 q=7 row-deficient maximal nonexistence — class-split sweep

Date: 2026-11-15 (UTC). Fast lane, successor of K0847 (5x34 witness-free).

## Status

COMPLETE — all 66 records decided: 63 deciding instances UNSAT (17 direct
classes + {0},{1} k=0..4 + k=5 x minpos=0..17), 2 lex=H cross-checks UNSAT,
positive control SAT. **5x35 q=7 is witness-free.** Single continuous
session (no reset); raw logs pushed batch-by-batch and all 66 remote blob
shas verified against local sha1s (66/66 OK). See report.md and
records.jsonl / summary.json. Knowledge item: K0849.

## Claim

Witness frontier of (5,7): widths 19..34 were verified witness-free
(K0738-K0759, K0816, K0821, K0834-K0842, K0844, K0845, K0846, K0847);
this lane decides 5x35 — witness-free. The witness-free width set of
(5,7) is now {19,...,35}; set form M_{5,7} in {19,...,35} or >= 36; sharp
form (K0821-audit convention) **M = 19 or >= 37** (M = 36 would require a
witness at the verified witness-free width 35). Upper 158 (K0332
substitution) unchanged. Frontier moves to 5x36.

## Results

- 17 direct classes all UNSAT: hardest {0,1} 252,381 conflicts (−14.8% vs
  its m=34 counterpart); direct total 1,636,361 (−6.1% vs m=34 1,743,108:
  5,256,816 -> 4,673,619 -> 4,160,006 -> 3,534,969 -> 3,307,565 ->
  2,656,426 -> 2,503,468 -> 2,261,532 -> 1,960,401 -> 1,916,295 ->
  1,735,912 -> 1,804,062 -> 1,743,108 -> 1,636,361) + lex=H cross-checks
  on {0,1},{2} UNSAT (175,172 / 102,024 conflicts).
- {0},{1} krow k=0..4 all UNSAT (10 instances; hardest {1} k=4: 352,023 —
  up 0.9% vs m=34 349,040, a local non-decrease; {0} k=4: 207,921 — up
  3.8% vs 200,212; krow total 729,321 — up 0.4% vs 726,502, the first
  krow-total non-decrease in the series, still essentially flat).
- {0},{1} k=5 x minpos=0..17 all UNSAT (36 instances — the minpos sound
  bound grows to floor((35-1)/2)=17 at m=35, 18 points per class, columns
  0..34: min(x_min, 34-x_max) <= 17; hardest {1} k=5 mp=0: 496,388 /
  18.57 s — down 13.6% from its m=34 counterpart 574,663; {0} k=5 mp=0:
  338,617 — down 14.9% from 398,074; {0}k5p total 1,246,094; {1}k5p total
  1,811,248).
- Positive control: 5x18 class {0} SAT 343,134 conflicts, bit-exact with
  the K0821..K0847 lane controls (fourteenth cross-lane reproduction);
  decoded 29 stones rows (5,6,6,6,6), census-free verifyConfig PASS.
- Deciding 63 instances total 5,423,024 conflicts (17 direct 1,636,361 +
  10 krow 729,321 + 36 k=minpos 3,057,342); deciding+lex=H 5,700,220
  (= total_conflicts_35, same convention as m=27..m=34 summaries);
  records total 6,043,354; INDET 0, SAT 0.

## Scripts

mkcnf.sh (66 CNFs — 17 direct + 46 k/minpos with the minpos sound bound
floor((35-1)/2)=17, i.e. minpos=0..17 = 18 points per class, plus 2 lex=H
and the 5x18 control), qrun.sh (2-worker claim-directory queue runner),
mkrecords5735.js (records/summary builder; log-name templates match the
pushed raw-log names); sat.js/sat2.js/sat3.js are byte-identical to the
K0836..K0847 lane scripts (restored from the m=34 lane on main, git blob
shas 6c3262d6 / edfae1d2 / 6dfa7db3; the control CNF c5x18q7_0.cnf
regenerates md5-identical 0bb6187d36e537a170e4fb451359bb94). kissat 4.0.4
official rel-4.0.4 linux-amd64 asset (binary md5
3a5eba830aa6008a604fcc9bbe99a325).

## Next

5x36: the minpos sound bound stays floor((36-1)/2) = 17 (18 points per
class, columns 0..35: min(x_min, 35-x_max) <= 17 — the CNF set stays 66).
Deciding totals keep decreasing on average (m=23..35: 20,916,467 ->
17,349,736 -> 15,521,919 -> 13,845,697 -> 11,363,141 -> 10,218,568 ->
8,677,594 -> 7,809,347 -> 7,275,763 -> 6,569,505 -> 6,140,609 ->
5,928,015 -> 5,423,024); m=36 projected ~5.1M deciding conflicts.
