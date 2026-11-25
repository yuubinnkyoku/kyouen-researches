# 5x32 q=7 row-deficient maximal nonexistence — class-split sweep

Date: 2026-11-15 (UTC). Fast lane, successor of K0844 (5x31 witness-free).

## Status

COMPLETE — all 62 instances decided: 59 deciding instances UNSAT (17 direct
classes + {0},{1} k=0..4 + k=5 x minpos=0..15), 2 lex=H cross-checks UNSAT,
positive control SAT. **5x32 q=7 is witness-free.** Single continuous
session, no environment reset. Raw logs pushed batch-by-batch. See
report.md and records.jsonl / summary.json. Knowledge item: K0845.

## Claim

Witness frontier of (5,7): widths 19..31 were verified witness-free
(K0738-K0759, K0816, K0821, K0834-K0842, K0844); this lane decides 5x32 —
witness-free. The witness-free width set of (5,7) is now {19,...,32}; set
form M_{5,7} in {19,...,32} or >= 33; sharp form (K0821-audit convention)
**M = 19 or >= 34**. Upper 158 (K0332 substitution) unchanged. Frontier
moves to 5x33.

## Results

- 17 direct classes all UNSAT: hardest {0,1} 286,945 conflicts (-17.9% vs
  its m=31 counterpart — the direct difficulty keeps decreasing); direct
  total 1,735,912 (the m=22..32 direct-total trend stays monotonically
  decreasing: 5,256,816 -> 4,673,619 -> 4,160,006 -> 3,534,969 ->
  3,307,565 -> 2,656,426 -> 2,503,468 -> 2,261,532 -> 1,960,401 ->
  1,916,295 -> 1,735,912) + lex=H cross-checks on {0,1},{2} UNSAT
  (255,846 / 104,836 conflicts).
- {0},{1} krow k=0..4 all UNSAT (10 instances; hardest {1} k=4: 357,539 /
  {0} k=4: 277,605 conflicts; krow total 857,057).
- {0},{1} k=5 x minpos=0..15 all UNSAT (32 instances — the minpos sound
  bound stays floor((32-1)/2)=15 at m=32, 16 points per class; hardest
  {1} k=5 mp=0: 670,375 / 25.66 s — up 2.4% from its m=31 counterpart
  654,902, the first local non-decrease in the k5p0 sub-series; {0} k=5
  mp=0: 443,637 — down from its m=31 counterpart 485,104; {0}k5p total
  1,624,108; {1}k5p total 2,352,428).
- Positive control: 5x18 class {0} SAT 343,134 conflicts, bit-exact with
  the K0821..K0844 lane controls (eleventh cross-lane reproduction);
  decoded 29 stones rows (5,6,6,6,6), census-free verifyConfig PASS.
- Deciding 59 instances total 6,569,505 conflicts (17 direct 1,735,912 +
  10 krow 857,057 + 32 k=minpos 3,976,536); deciding+lex=H 6,930,187
  (= total_conflicts_32, same convention as m=27..m=31 summaries);
  records total 7,273,321; INDET 0, SAT 0.

## Scripts

mkcnf.sh (62 CNFs — 17 direct + 42 k/minpos with the minpos sound bound
floor((32-1)/2)=15, i.e. minpos=0..15 = 16 points per class, plus 2 lex=H
and the 5x18 control), qrun.sh (2-worker claim-directory queue runner),
mkrecords5732.js (records/summary builder; log-name templates match the
pushed raw-log names); sat.js/sat2.js/sat3.js are byte-identical to the
K0836..K0842/K0844 lane scripts (git blob shas 6c3262d6 / edfae1d2 /
6dfa7db3; md5 re-verified against the m=31 lane copies; the control CNF
c5x18q7_0.cnf regenerates md5-identical).

## Next

5x33: the minpos sound bound grows to floor((33-1)/2)=16 (17 points per
class, columns 0..32: min(x_min, 32-x_max) <= 16), so the CNF set grows
to 64. Deciding difficulty still decreasing (m=23..32: 20,916,467 ->
17,349,736 -> 15,521,919 -> 13,845,697 -> 11,363,141 -> 10,218,568 ->
8,677,594 -> 7,809,347 -> 7,275,763 -> 6,569,505); m=33 projected ~6.1M
conflicts.
