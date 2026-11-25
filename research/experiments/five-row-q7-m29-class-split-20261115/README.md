# 5x29 q=7 row-deficient maximal nonexistence — class-split sweep

Date: 2026-11-15 (UTC). Fast lane, successor of K0840 (5x28 witness-free).

## Status

COMPLETE — all 60 instances decided: 57 deciding instances UNSAT (17 direct
classes + {0},{1} k=0..4 + k=5 x minpos=0..14), 2 lex=H cross-checks UNSAT,
positive control SAT. **5x29 q=7 is witness-free.** Single continuous session
(no environment reset); scripts restored byte-identically from the m=28 lane
(sat.js/sat2.js/sat3.js; mkcnf.sh/qrun.sh ported m=28 -> m=29), raw logs
pushed batch-by-batch. See report.md and records.jsonl / summary.json.
Knowledge item: K0841.

## Claim

Witness frontier of (5,7): widths 19..28 were verified witness-free
(K0738-K0759, K0816, K0821, K0834, K0835, K0836, K0837, K0838, K0839,
K0840); this lane decides 5x29 — witness-free. The witness-free width set of
(5,7) is now {19,...,29}; set form M_{5,7} in {19,...,29} or >= 30; sharp form
(K0821-audit convention) **M = 19 or >= 31**. Upper 158 (K0332
substitution) unchanged. Frontier moves to 5x30.

## Results

- 17 direct classes all UNSAT: hardest {0,1} 363,639 conflicts; direct total
  2,261,532 (the m=22..29 direct trend is monotonically decreasing:
  5,256,816 -> 4,673,619 -> 4,160,006 -> 3,534,969 -> 3,307,565 -> 2,656,426
  -> 2,503,468 -> 2,261,532) + lex=H cross-checks on {0,1},{2} UNSAT
  (328,996 / 135,892 conflicts).
- {0},{1} krow k=0..4 all UNSAT (10 instances; hardest {1} k=4: 509,585 /
  {0} k=4: 372,205 conflicts; krow total 1,135,398).
- {0},{1} k=5 x minpos=0..14 all UNSAT (30 instances — the m=29 sound bound
  grows to floor((29-1)/2)=14, 15 points per class; hardest {1} k=5 mp=0:
  850,480 / 31.21 s — down 42% from its m=28 counterpart 1,469,014, so the
  m=28 k5p0 non-decrease was transient; {0} k=5 mp=0: 690,557 — below its
  m=28 counterpart 834,706; {0}k5p total 2,239,394; {1}k5p total 3,041,270).
- Positive control: 5x18 class {0} SAT 343,134 conflicts, bit-exact with the
  K0821/K0834/K0835/K0836/K0837/K0838/K0839/K0840 lane controls (eighth
  cross-lane reproduction); decoded 29 stones rows (5,6,6,6,6), census-free
  verifyConfig PASS.
- Deciding 57 instances total 8,677,594 conflicts (17 direct 2,261,532 + 10
  krow 1,135,398 + 30 k=minpos 5,280,664); records total 9,485,616
  (m=29 records incl. lex=H 9,142,482 — same convention as m=27/m=28
  summaries); INDET 0, SAT 0.

## Scripts

mkcnf.sh (60 CNFs — 17 direct + 38 k/minpos with the m=29 sound bound
floor((29-1)/2)=14, i.e. minpos=0..14 = 15 points per class, plus 2 lex=H and
the 5x18 control), qrun.sh (2-worker claim-directory queue runner),
mkrecords5729.js (records/summary builder); sat.js/sat2.js/sat3.js are
byte-identical to the K0836..K0840 lane scripts (restored from the m=28 lane
directory; blob sha verified against main).

## Next

5x30: minpos sound bound stays floor((30-1)/2)=14 (15 points per class, 30
k=5 sub-instances; the CNF set stays at 60). Deciding difficulty still
decreasing (20,916,467 -> 17,349,736 -> 15,521,919 -> 13,845,697 ->
11,363,141 -> 10,218,568 -> 8,677,594 for m=23..29 — the m=28 local exception
{1} k=5 mp=0 resolved by a 42% drop); m=30 projected within this lane's
range.
