# 5x30 q=7 row-deficient maximal nonexistence — class-split sweep

Date: 2026-11-15 (UTC). Fast lane, successor of K0841 (5x29 witness-free).

## Status

COMPLETE — all 60 instances decided: 57 deciding instances UNSAT (17 direct
classes + {0},{1} k=0..4 + k=5 x minpos=0..14), 2 lex=H cross-checks UNSAT,
positive control SAT. **5x30 q=7 is witness-free.** A full
execution-environment reset occurred between batch-1 and batch-2; recovery
followed the established cross-reset protocol (batch-1 logs byte-exact on
main and restored from main; scripts restored byte-identically from the
m=29 lane; kissat 4.0.4 re-downloaded from the official rel-4.0.4 release
asset; CNFs regenerated; calibration c2 103,993 and control 343,134
reproduced bit-exactly). Raw logs pushed batch-by-batch. See report.md and
records.jsonl / summary.json. Knowledge item: K0842.

## Claim

Witness frontier of (5,7): widths 19..29 were verified witness-free
(K0738-K0759, K0816, K0821, K0834-K0841); this lane decides 5x30 —
witness-free. The witness-free width set of (5,7) is now {19,...,30}; set
form M_{5,7} in {19,...,30} or >= 31; sharp form (K0821-audit convention)
**M = 19 or >= 32**. Upper 158 (K0332 substitution) unchanged. Frontier
moves to 5x31.

## Results

- 17 direct classes all UNSAT: hardest {0,1} 388,349 conflicts (+6.8% vs
  its m=29 counterpart — first local non-decrease in the direct-hardest
  series); direct total 1,960,401 (the m=22..30 direct-total trend stays
  monotonically decreasing: 5,256,816 -> 4,673,619 -> 4,160,006 ->
  3,534,969 -> 3,307,565 -> 2,656,426 -> 2,503,468 -> 2,261,532 ->
  1,960,401) + lex=H cross-checks on {0,1},{2} UNSAT (276,589 / 124,495
  conflicts).
- {0},{1} krow k=0..4 all UNSAT (10 instances; hardest {1} k=4: 445,772 /
  {0} k=4: 350,870 conflicts; krow total 1,005,289).
- {0},{1} k=5 x minpos=0..14 all UNSAT (30 instances — the m=30 sound
  bound stays floor((30-1)/2)=14, 15 points per class; hardest {1} k=5
  mp=0: 802,385 / 31 s — down 5.7% from its m=29 counterpart 850,480;
  {0} k=5 mp=0: 545,523 — below its m=29 counterpart 690,557; {0}k5p
  total 2,040,624; {1}k5p total 2,803,033).
- Positive control: 5x18 class {0} SAT 343,134 conflicts, bit-exact with
  the K0821..K0841 lane controls (ninth cross-lane reproduction; run
  twice, pre-reset and as post-reset calibration, both bit-exact);
  decoded 29 stones rows (5,6,6,6,6), census-free verifyConfig PASS.
- Deciding 57 instances total 7,809,347 conflicts (17 direct 1,960,401 +
  10 krow 1,005,289 + 30 k=minpos 4,843,657); deciding+lex=H 8,210,431
  (= total_conflicts_30, same convention as m=27..m=29 summaries);
  records total 8,553,565; INDET 0, SAT 0.

## Scripts

mkcnf.sh (60 CNFs — 17 direct + 40 k/minpos with the m=30 sound bound
floor((30-1)/2)=14, i.e. minpos=0..14 = 15 points per class, plus 2 lex=H
and the 5x18 control), qrun.sh (2-worker claim-directory queue runner),
mkrecords5730.js (records/summary builder; log-name templates match the
pushed raw-log names); sat.js/sat2.js/sat3.js are byte-identical to the
K0836..K0841 lane scripts (restored from the m=29 lane via main; blob sha
verified).

## Next

5x31: minpos sound bound grows to floor((31-1)/2)=15 (16 points per
class, 32 k=5 sub-instances; the CNF set grows to 62). Deciding difficulty
still decreasing (20,916,467 -> 17,349,736 -> 15,521,919 -> 13,845,697 ->
11,363,141 -> 10,218,568 -> 8,677,594 -> 7,809,347 for m=23..30); m=31
projected within this lane's range.
