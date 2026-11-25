# 5x31 q=7 row-deficient maximal nonexistence — class-split sweep

Date: 2026-11-15 (UTC). Fast lane, successor of K0842 (5x30 witness-free).

## Status

COMPLETE — all 62 instances decided: 59 deciding instances UNSAT (17 direct
classes + {0},{1} k=0..4 + k=5 x minpos=0..15), 2 lex=H cross-checks UNSAT,
positive control SAT. **5x31 q=7 is witness-free.** Single continuous
session, no environment reset. Raw logs pushed batch-by-batch. See
report.md and records.jsonl / summary.json. Knowledge item: K0844.

## Claim

Witness frontier of (5,7): widths 19..30 were verified witness-free
(K0738-K0759, K0816, K0821, K0834-K0842); this lane decides 5x31 —
witness-free. The witness-free width set of (5,7) is now {19,...,31}; set
form M_{5,7} in {19,...,31} or >= 32; sharp form (K0821-audit convention)
**M = 19 or >= 33**. Upper 158 (K0332 substitution) unchanged. Frontier
moves to 5x32.

## Results

- 17 direct classes all UNSAT: hardest {0,1} 349,508 conflicts (-10.0% vs
  its m=30 counterpart — the m=30 direct-hardest non-decrease was
  transient); direct total 1,916,295 (the m=22..31 direct-total trend
  stays monotonically decreasing: 5,256,816 -> 4,673,619 -> 4,160,006 ->
  3,534,969 -> 3,307,565 -> 2,656,426 -> 2,503,468 -> 2,261,532 ->
  1,960,401 -> 1,916,295) + lex=H cross-checks on {0,1},{2} UNSAT
  (233,024 / 97,713 conflicts).
- {0},{1} krow k=0..4 all UNSAT (10 instances; hardest {1} k=4: 391,719 /
  {0} k=4: 320,407 conflicts; krow total 967,417).
- {0},{1} k=5 x minpos=0..15 all UNSAT (32 instances — the m=31 sound
  bound grows to floor((31-1)/2)=15, 16 points per class; hardest {1} k=5
  mp=0: 654,902 / 24.17 s — down 18.4% from its m=30 counterpart 802,385;
  {0} k=5 mp=0: 485,104 — below its m=30 counterpart 545,523; {0}k5p
  total 1,797,924; {1}k5p total 2,594,127).
- Positive control: 5x18 class {0} SAT 343,134 conflicts, bit-exact with
  the K0821..K0842 lane controls (tenth cross-lane reproduction); decoded
  29 stones rows (5,6,6,6,6), census-free verifyConfig PASS.
- Deciding 59 instances total 7,275,763 conflicts (17 direct 1,916,295 +
  10 krow 967,417 + 32 k=minpos 4,392,051); deciding+lex=H 7,606,500
  (= total_conflicts_31, same convention as m=27..m=30 summaries);
  records total 7,949,634; INDET 0, SAT 0.

## Scripts

mkcnf.sh (62 CNFs — 17 direct + 42 k/minpos with the m=31 sound bound
floor((31-1)/2)=15, i.e. minpos=0..15 = 16 points per class, plus 2 lex=H
and the 5x18 control), qrun.sh (2-worker claim-directory queue runner),
mkrecords5731.js (records/summary builder; log-name templates match the
pushed raw-log names); sat.js/sat2.js/sat3.js are byte-identical to the
K0836..K0842 lane scripts (git blob shas 6c3262d6 / edfae1d2 / 6dfa7db3).

## Next

5x32: the minpos sound bound stays floor((32-1)/2)=15 (16 points per
class, columns 0..31: min(x_min, 31-x_max) <= 15), so the CNF set stays
62. Deciding difficulty still decreasing (m=23..31: 20,916,467 ->
17,349,736 -> 15,521,919 -> 13,845,697 -> 11,363,141 -> 10,218,568 ->
8,677,594 -> 7,809,347 -> 7,275,763); m=32 projected ~6.8M conflicts.
