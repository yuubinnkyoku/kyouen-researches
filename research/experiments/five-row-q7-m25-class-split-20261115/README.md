# 5x25 q=7 row-deficient maximal nonexistence — class-split sweep

Date: 2026-11-15 (UTC). Fast lane, successor of K0836 (5x24 witness-free).

## Status

COMPLETE — all 56 instances decided: 53 deciding instances UNSAT (17 direct
classes + {0},{1} k=0..4 + k=5 x minpos=0..12), 2 lex=H cross-checks UNSAT,
positive control SAT. **5x25 q=7 is witness-free.** The sweep completed across
an execution-environment outage: the prior session's 29 raw logs (batch-1/2)
are byte-exact on main; the resuming session regenerated all 56 CNFs, verified
cross-run bit-exact calibration (c2 259,243 / 0k4 755,207), and completed the
26 k=5 x minpos instances + control. See report.md and records.jsonl /
summary.json. Knowledge item: K0837.

## Claim

Witness frontier of (5,7): widths 19..24 were verified witness-free
(K0738-K0759, K0816, K0821, K0834, K0835, K0836); this lane decides 5x25 —
witness-free. The witness-free width set of (5,7) is now {19,...,25}; set form
M_{5,7} in {19,...,25} or >= 26; sharp form (K0821-audit convention) **M = 19
or >= 27**. Upper 158 (K0332 substitution) unchanged. Frontier moves to 5x26.

## Results

- 17 direct classes all UNSAT (batch-1, commit 00d5f071): hardest {0,1}
  535,454 conflicts; direct total 3,534,969 (the m=22..25 direct trend is
  monotonically decreasing: 5,256,816 -> 4,673,619 -> 4,160,006 -> 3,534,969)
  + lex=H cross-checks on {0,1},{2} UNSAT (391,407 / 290,573 conflicts).
- {0},{1} krow k=0..4 all UNSAT (batch-2, commit 96f6ee0e; 10 instances;
  hardest {1} k=4: 786,695 / {0} k=4: 755,207 conflicts).
- {0},{1} k=5 x minpos=0..12 all UNSAT (batches 3-4, commits adb13b5c /
  9011948b; 26 instances — the m=25 sound bound is floor((m-1)/2)=12,
  i.e. 13 points per class; hardest {1} k=5 mp=0: 2,021,531 / 83.04 s,
  {0} k=5 mp=0: 1,620,423 / 64.6 s — both below their m=24 counterparts).
- Positive control: 5x18 class {0} SAT 343,134 conflicts, bit-exact with the
  K0821/K0834/K0835/K0836 lane controls (fourth cross-lane reproduction);
  decoded 29 stones rows (5,6,6,6,6), census-free verifyConfig PASS.
- Deciding 53 instances total 15,521,919 conflicts (17 direct 3,534,969 +
  36 decomposition 11,986,950); records total 16,203,899; INDET 0.

## Scripts

mkcnf.sh (56 CNFs — 17 direct + 36 k/minpos with the m=25 sound bound
floor((m-1)/2)=12, i.e. minpos=0..12 = 13 points per class), qrun.sh
(2-worker claim-directory queue runner), mkrecords5725.js (records/summary
builder); sat.js/sat2.js/sat3.js are byte-identical to the K0836 m=24 lane
scripts (copied here for self-containment; blob sha verified against the m=24
lane on main).

## Resume protocol (proven by this run)

1. Regenerate CNFs with the byte-identical encoders (mkcnf.sh, ~26 s).
2. Calibrate: re-run 1-2 already-decided instances and compare conflicts with
   the main logs bit-exactly (c2 / 0k4 here).
3. Run the remaining instances via qrun.sh; push raw logs batch-by-batch.
4. Build records/summary (mkrecords5725.js), report.md, K item, research log,
   results CSV/README rows.

The outage hit exactly like the K0835 mid-sweep reset; the chunk-push
discipline kept all finished instances' evidence on main, and the calibration
step turned the resume into a cross-run determinism witness.
