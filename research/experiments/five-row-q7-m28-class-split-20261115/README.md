# 5x28 q=7 row-deficient maximal nonexistence — class-split sweep

Date: 2026-11-15 (UTC). Fast lane, successor of K0839 (5x27 witness-free).

## Status

COMPLETE — all 58 instances decided: 53 deciding instances UNSAT (17 direct
classes + {0},{1} k=0..4 + k=5 x minpos=0..13), 2 lex=H cross-checks UNSAT,
positive control SAT. **5x28 q=7 is witness-free.** Single continuous session
(no environment reset); scripts restored byte-identically from the m=27 lane
(git blob sha verified), raw logs pushed batch-by-batch. See report.md and
records.jsonl / summary.json. Knowledge item: K0840.

## Claim

Witness frontier of (5,7): widths 19..27 were verified witness-free
(K0738-K0759, K0816, K0821, K0834, K0835, K0836, K0837, K0838, K0839); this
lane decides 5x28 — witness-free. The witness-free width set of (5,7) is now
{19,...,28}; set form M_{5,7} in {19,...,28} or >= 29; sharp form
(K0821-audit convention) **M = 19 or >= 30**. Upper 158 (K0332
substitution) unchanged. Frontier moves to 5x29.

## Results

- 17 direct classes all UNSAT: hardest {0,1} 389,650 conflicts; direct total
  2,503,468 (the m=22..28 direct trend is monotonically decreasing:
  5,256,816 -> 4,673,619 -> 4,160,006 -> 3,534,969 -> 3,307,565 -> 2,656,426
  -> 2,503,468) + lex=H cross-checks on {0,1},{2} UNSAT (313,971 / 149,952
  conflicts).
- {0},{1} krow k=0..4 all UNSAT (10 instances; hardest {1} k=4: 515,833 /
  {0} k=4: 483,130 conflicts).
- {0},{1} k=5 x minpos=0..13 all UNSAT (28 instances — the m=28 sound bound
  stays floor((m-1)/2)=13, 14 points per class; hardest {1} k=5 mp=0:
  1,469,014 / 56.59 s — slightly above its m=27 counterpart 1,378,345, the
  first non-decrease in the k5p0 series; {0} k=5 mp=0: 834,706 / 31.48 s —
  below its m=27 counterpart 861,966).
- Positive control: 5x18 class {0} SAT 343,134 conflicts, bit-exact with the
  K0821/K0834/K0835/K0836/K0837/K0838/K0839 lane controls (seventh
  cross-lane reproduction); decoded 29 stones rows (5,6,6,6,6), census-free
  verifyConfig PASS.
- Deciding 53 instances total 10,218,568 conflicts (17 direct 2,503,468 + 38
  decomposition 7,715,100); records total 11,025,625; INDET 0, SAT 0.

## Scripts

mkcnf.sh (58 CNFs — 17 direct + 38 k/minpos with the m=28 sound bound
floor((m-1)/2)=13, i.e. minpos=0..13 = 14 points per class), qrun.sh
(2-worker claim-directory queue runner), mkrecords5728.js (records/summary
builder); sat.js/sat2.js/sat3.js are byte-identical to the K0836..K0839 lane
scripts (restored from the m=27 lane directory; blob sha verified against
main).

## Next

5x29: minpos sound bound grows to floor((29-1)/2)=14 (15 points per class, 30
k=5 sub-instances; the CNF set grows to 60). Deciding difficulty still
decreasing (20,916,467 -> 17,349,736 -> 15,521,919 -> 13,845,697 ->
11,363,141 -> 10,218,568 for m=23..28, with the single local exception
{1} k=5 mp=0 up 6.6% from m=27); m=29 projected within this lane's range.
