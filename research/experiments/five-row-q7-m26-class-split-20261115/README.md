# 5x26 q=7 row-deficient maximal nonexistence — class-split sweep

Date: 2026-11-15 (UTC). Fast lane, successor of K0837 (5x25 witness-free).

## Status

COMPLETE — all 56 instances decided: 53 deciding instances UNSAT (17 direct
classes + {0},{1} k=0..4 + k=5 x minpos=0..12), 2 lex=H cross-checks UNSAT,
positive control SAT. **5x26 q=7 is witness-free.** The sweep ran across a
full execution-environment reset between batch-1 and batch-2 (pre-reset
batch-1 logs byte-exact on main; the resuming session re-downloaded kissat
4.0.4, restored scripts from main, regenerated CNFs and calibrated c2/5x18
bit-exactly — third demonstrated cross-reset bit-exactness). See report.md
and records.jsonl / summary.json. Knowledge item: K0838.

## Claim

Witness frontier of (5,7): widths 19..25 were verified witness-free
(K0738-K0759, K0816, K0821, K0834, K0835, K0836, K0837); this lane decides
5x26 — witness-free. The witness-free width set of (5,7) is now
{19,...,26}; set form M_{5,7} in {19,...,26} or >= 27; sharp form
(K0821-audit convention) **M = 19 or >= 28**. Upper 158 (K0332
substitution) unchanged. Frontier moves to 5x27.

## Results

- 17 direct classes all UNSAT (batch-1, pre-reset session): hardest {0,1}
  654,569 conflicts; direct total 3,307,565 (the m=22..26 direct trend is
  monotonically decreasing: 5,256,816 -> 4,673,619 -> 4,160,006 ->
  3,534,969 -> 3,307,565) + lex=H cross-checks on {0,1},{2} UNSAT
  (446,133 / 236,958 conflicts).
- {0},{1} krow k=0..4 all UNSAT (batch-2; 10 instances; hardest {1} k=4:
  913,377 / {0} k=4: 620,428 conflicts).
- {0},{1} k=5 x minpos=0..12 all UNSAT (batches 3-4; 26 instances — the m=26
  sound bound is floor((m-1)/2)=12, same as m=25: for columns 0..25,
  min(x_min, 25-x_max) <= 12; hardest {1} k=5 mp=0: 1,758,742 / 71.28 s,
  {0} k=5 mp=0: 1,202,057 / 47.17 s — both below their m=25 counterparts).
- Positive control: 5x18 class {0} SAT 343,134 conflicts, bit-exact with the
  K0821/K0834/K0835/K0836/K0837 lane controls (fifth cross-lane
  reproduction); decoded 29 stones rows (5,6,6,6,6), census-free
  verifyConfig PASS.
- Deciding 53 instances total 13,845,697 conflicts (17 direct 3,307,565 +
  36 decomposition 10,538,132); records total 14,871,922; INDET 0.

## Scripts

mkcnf.sh (56 CNFs — 17 direct + 36 k/minpos with the m=26 sound bound
floor((m-1)/2)=12, i.e. minpos=0..12 = 13 points per class), qrun.sh
(2-worker claim-directory queue runner), mkrecords5726.js (records/summary
builder); sat.js/sat2.js/sat3.js are byte-identical to the K0836/K0837 lane
scripts (restored from this directory after the environment reset; blob sha
verified).

## Resume protocol (proven twice now)

1. Regenerate CNFs with the byte-identical encoders (mkcnf.sh, ~26 s).
2. Calibrate: re-run 1-2 already-decided instances and compare conflicts with
   the main logs bit-exactly (c2 / 5x18 control here).
3. Run the remaining instances via qrun.sh; push raw logs batch-by-batch.
4. Build records/summary (mkrecords5726.js), report.md, K item, research
   log, results CSV/README rows.

This outage hit between batches with zero evidence loss (batch-1 logs were
already pushed); the calibration step turned the resume into a cross-run
determinism witness.

## Next

5x27: minpos sound bound grows to floor((27-1)/2)=13 (14 points per class,
28 k=5 sub-instances; 58 CNFs total). Deciding difficulty still decreasing
(20,916,467 -> 17,349,736 -> 15,521,919 -> 13,845,697 for m=23..26).
