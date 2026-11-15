# 5x25 q=7 row-deficient maximal nonexistence — class-split sweep

Date: 2026-11-15 (UTC). Fast lane, successor of K0836 (5x24 witness-free).

## Status

IN FLIGHT — interrupted by an execution-environment outage mid-sweep
(2026-11-15); 29/56 raw logs are on main. Resume from the k=5 x minpos batch.

## Claim

Witness frontier of (5,7): widths 19..24 are verified witness-free
(K0738-K0759, K0816, K0821, K0834, K0835, K0836); this lane decides 5x25.
A witness here gives M_{5,7} >= 26; witness-free here extends the free set to
{19,...,25} (sharp form M = 19 or >= 27). Upper 158 (K0332 substitution)
unchanged.

## Progress (raw logs on main)

- batch-1 (commit 00d5f071): 17 direct classes all UNSAT — hardest {0,1}
  535,454 conflicts; direct total 3,534,969 (the m=21..25 direct trend is
  monotonically decreasing: 5,256,816 -> 4,673,619 -> 4,160,006 -> 3,534,969)
  + lex=H cross-checks on {0,1},{2} UNSAT again (391,407 / 290,573 conflicts).
- batch-2 (commit 96f6ee0e): {0},{1} krow k=0..4 all UNSAT (10 instances;
  hardest {1} k=4: 786,695 / {0} k=4: 755,207 conflicts).
- scripts preserved (commit a7eb70e4): mkcnf.sh (56 CNFs — 17 direct +
  36 k/minpos with the m=25 sound bound floor((m-1)/2)=12, i.e. minpos=0..12
  = 13 points per class) and qrun.sh (2-worker claim-directory queue runner);
  sat.js/sat2.js/sat3.js are byte-identical to the K0836 m=24 lane scripts.

## Resume (next run)

1. Regenerate CNFs: copy sat.js/sat2.js/sat3.js from the m=24 lane scripts,
   run mkcnf.sh (56 CNFs, ~26 s).
2. Run the remaining 26 k=5 x minpos instances:
   qrun.sh 260 250 0k5p0..0k5p12 1k5p0..1k5p12 (hardest expected {1} k=5 mp=0,
   m=24 counterpart 2,282,668 conflicts / 92.8 s).
3. Positive control: kissat on c5x18q7_0.cnf -> r_ctrl_5x18_c0.txt (expect SAT
   343,134 conflicts, bit-exact with the K0821/K0834/K0835/K0836 lane controls).
4. Push raw logs batch-by-batch (do not hold local-only evidence).
5. Build records.jsonl/summary.json (port mkrecords5724.js -> mkrecords5725.js:
   m=25, r5x25q7 prefixes, minpos p list 0..12, decomposition split count 36,
   claim string "{19,20,21,22,23,24,25}; M = 19 or >= 27"), report.md, then the
   K0837 item (re-check the max K number on latest main first), research log,
   and the results CSV/README (5,7) row.

Note: the environment outage hit exactly like the K0835 mid-sweep reset; the
chunk-push discipline kept all 29 finished instances' evidence on main.
