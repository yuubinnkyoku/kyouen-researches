# 5x34 q=7 row-deficient maximal nonexistence — class-split sweep

Date: 2026-11-15 (UTC). Fast lane, successor of K0846 (5x33 witness-free).

## Status

COMPLETE — all 64 records decided: 61 deciding instances UNSAT (17 direct
classes + {0},{1} k=0..4 + k=5 x minpos=0..16), 2 lex=H cross-checks UNSAT,
positive control SAT. **5x34 q=7 is witness-free.** Single continuous
session (no reset); raw logs pushed batch-by-batch and all 64 remote blob
shas verified against local sha1s (64/64 OK). See report.md and
records.jsonl / summary.json. Knowledge item: K0847.

## Claim

Witness frontier of (5,7): widths 19..33 were verified witness-free
(K0738-K0759, K0816, K0821, K0834-K0842, K0844, K0845, K0846); this lane
decides 5x34 — witness-free. The witness-free width set of (5,7) is now
{19,...,34}; set form M_{5,7} in {19,...,34} or >= 35; sharp form
(K0821-audit convention) **M = 19 or >= 36** (M = 35 would require a
witness at the verified witness-free width 34). Upper 158 (K0332
substitution) unchanged. Frontier moves to 5x35.

## Results

- 17 direct classes all UNSAT: hardest {0,1} 296,276 conflicts (−11.3% vs
  its m=33 counterpart — the m=33 direct-hardest non-decrease was
  transient); direct total 1,743,108 (−3.4% vs m=33 1,804,062 — the
  m=33 direct-total non-decrease did not continue: 5,256,816 ->
  4,673,619 -> 4,160,006 -> 3,534,969 -> 3,307,565 -> 2,656,426 ->
  2,503,468 -> 2,261,532 -> 1,960,401 -> 1,916,295 -> 1,735,912 ->
  1,804,062 -> 1,743,108) + lex=H cross-checks on {0,1},{2} UNSAT
  (249,695 / 86,705 conflicts).
- {0},{1} krow k=0..4 all UNSAT (10 instances; hardest {1} k=4: 349,040 /
  {0} k=4: 200,212; krow total 726,502).
- {0},{1} k=5 x minpos=0..16 all UNSAT (34 instances — the minpos sound
  bound stays floor((34-1)/2)=16 at m=34, 17 points per class, columns
  0..33: min(x_min, 33-x_max) <= 16; hardest {1} k=5 mp=0: 574,663 /
  20.64 s — down 11.9% from its m=33 counterpart 651,985; {0} k=5 mp=0:
  398,074 — down 10.9% from 446,878, ending the two-run k5p0
  non-decrease streak; {0}k5p total 1,464,826; {1}k5p total 1,993,579).
- Positive control: 5x18 class {0} SAT 343,134 conflicts, bit-exact with
  the K0821..K0846 lane controls (thirteenth cross-lane reproduction);
  decoded 29 stones rows (5,6,6,6,6), census-free verifyConfig PASS.
- Deciding 61 instances total 5,928,015 conflicts (17 direct 1,743,108 +
  10 krow 726,502 + 34 k=minpos 3,458,405); deciding+lex=H 6,264,415
  (= total_conflicts_34, same convention as m=27..m=33 summaries);
  records total 6,607,549; INDET 0, SAT 0.

## Scripts

mkcnf.sh (64 CNFs — 17 direct + 44 k/minpos with the minpos sound bound
floor((34-1)/2)=16, i.e. minpos=0..16 = 17 points per class, plus 2 lex=H
and the 5x18 control), qrun.sh (2-worker claim-directory queue runner),
mkrecords5734.js (records/summary builder; log-name templates match the
pushed raw-log names); sat.js/sat2.js/sat3.js are byte-identical to the
K0836..K0846 lane scripts (restored from the m=33 lane on main, git blob
shas 6c3262d6 / edfae1d2 / 6dfa7db3; the control CNF c5x18q7_0.cnf
regenerates md5-identical).

## Next

5x35: the minpos sound bound grows to floor((35-1)/2) = 17 (18 points per
class, columns 0..34: min(x_min, 34-x_max) <= 17 — the CNF set grows to
66). Deciding totals keep decreasing on average (m=23..34: 20,916,467 ->
17,349,736 -> 15,521,919 -> 13,845,697 -> 11,363,141 -> 10,218,568 ->
8,677,594 -> 7,809,347 -> 7,275,763 -> 6,569,505 -> 6,140,609 ->
5,928,015); m=35 projected ~5.6M deciding conflicts.
