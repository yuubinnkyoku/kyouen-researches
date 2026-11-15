# 5x27 q=7 row-deficient maximal nonexistence — class-split sweep

Date: 2026-11-15 (UTC). Fast lane, successor of K0838 (5x26 witness-free).

## Status

COMPLETE — all 58 instances decided: 53 deciding instances UNSAT (17 direct
classes + {0},{1} k=0..4 + k=5 x minpos=0..13), 2 lex=H cross-checks UNSAT,
positive control SAT. **5x27 q=7 is witness-free.** Single continuous session
(no environment reset); scripts restored byte-identically from the m=26 lane
(git blob sha verified), raw logs pushed batch-by-batch. See report.md and
records.jsonl / summary.json. Knowledge item: K0839.

## Claim

Witness frontier of (5,7): widths 19..26 were verified witness-free
(K0738-K0759, K0816, K0821, K0834, K0835, K0836, K0837, K0838); this lane
decides 5x27 — witness-free. The witness-free width set of (5,7) is now
{19,...,27}; set form M_{5,7} in {19,...,27} or >= 28; sharp form
(K0821-audit convention) **M = 19 or >= 29**. Upper 158 (K0332
substitution) unchanged. Frontier moves to 5x28.

## Results

- 17 direct classes all UNSAT: hardest {0,1} 467,631 conflicts; direct total
  2,656,426 (the m=22..27 direct trend is monotonically decreasing:
  5,256,816 -> 4,673,619 -> 4,160,006 -> 3,534,969 -> 3,307,565 -> 2,656,426)
  + lex=H cross-checks on {0,1},{2} UNSAT (414,387 / 172,771 conflicts).
- {0},{1} krow k=0..4 all UNSAT (10 instances; hardest {1} k=4: 689,671 /
  {0} k=4: 514,683 conflicts).
- {0},{1} k=5 x minpos=0..13 all UNSAT (28 instances — the m=27 sound bound
  grows to floor((m-1)/2)=13, 14 points per class; hardest {1} k=5 mp=0:
  1,378,345 / 55.94 s, {0} k=5 mp=0: 861,966 — both below their m=26
  counterparts).
- Positive control: 5x18 class {0} SAT 343,134 conflicts, bit-exact with the
  K0821/K0834/K0835/K0836/K0837/K0838 lane controls (sixth cross-lane
  reproduction); decoded 29 stones rows (5,6,6,6,6), census-free
  verifyConfig PASS.
- Deciding 53 instances total 11,363,141 conflicts (17 direct 2,656,426 + 38
  decomposition 8,706,715); records total 12,293,433; INDET 0, SAT 0.

## Scripts

mkcnf.sh (58 CNFs — 17 direct + 38 k/minpos with the m=27 sound bound
floor((m-1)/2)=13, i.e. minpos=0..13 = 14 points per class), qrun.sh
(2-worker claim-directory queue runner), mkrecords5727.js (records/summary
builder); sat.js/sat2.js/sat3.js are byte-identical to the K0836/K0837/K0838
lane scripts (restored from the m=26 lane directory; blob sha verified
against main).

## Next

5x28: minpos sound bound stays floor((28-1)/2)=13 (14 points per class, 28
k=5 sub-instances; the CNF set stays 58). Deciding difficulty still
decreasing (20,916,467 -> 17,349,736 -> 15,521,919 -> 13,845,697 ->
11,363,141 for m=23..27); m=28 projected well within this lane's range.
