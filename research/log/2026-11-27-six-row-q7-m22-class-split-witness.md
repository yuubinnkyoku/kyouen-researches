# 2026-11-27 Six-row q=7, 6x22: class-split SAT witness — M_{6,7} >= 23

## Status

Complete, published. Declaration `d35234a7`
(`research/log/2026-11-27-six-row-q7-m22-class-split-declaration.md`,
declaration-time HEAD `a4ea02e4`), kit `03487c4b`
(`research/experiments/six-row-q7-m22-class-split-20261127/`,
fetch-back 23/23 byte-identical).

## Result

The krow/minpos decomposition of the (6,7) frontier width 6x22 resolved the
previously INDET class {2}: **sub-instance class {2}, krow=2:5, minpos=7 is
SAT (kissat 4.0.4, 2,050,424 conflicts, cold pair identical)** — a 35-stone
deficient maximal safe witness exists on 6x22, rows [6,6,5,6,6,6], with a
stone at (21,2) (genuine 6x22 board witness, full column span 0..21).

**M_{6,7} >= 23; the range becomes [23, 402]** (upper K0806/K0318 unchanged).
This resolves the 6x22 frontier in the SAT direction: the plain class {2}
280s/5,038,264-conflict INDET collapsed under the krow/minpos split, and the
same-day two-edit-surgery NEGATIVE (kit
`six-row-q7-m22-two-edit-surgery-20261127`) is consistent — the new witness
sits at symmetric difference 12 (>= 6 stone moves) from the m=21 witness
over all 8 dihedral images x translations, outside the <= 2-edit
neighborhood.

New frontier: **6x23**. Extension probes (disclosed as beyond the declared
6x22 target): class {2} k=5 minpos 6/7/8 all INDET at 262s caps
(4,968,075 / 5,055,896 / 4,935,522 conflicts) — honest negatives, not
absence. The free-column right-shift of the m=22 witness to 6x23 fails
(cell (0,2) unblocked).

## Verification

- Dual independent verification: sat.js census-free `verifyConfig` and a
  fresh Python exact-Fraction verifier (`scripts/verify_frac.py`, no repo
  code) both PASS (safe, maximal, max curve occupancy 6 = q-1).
- Negative controls: removing (21,2) -> not maximal (exactly [(21,2)]
  unblocked, rc=1); adding (2,0) -> rejected (rc=1).
- Verifier self-test: published m=21 witness verifies PASS on the same path.
- Positive control: 6x20 class {2} SAT, 641,859 conflicts — bit-exact with
  the published value.
- Determinism: deciding CNF cold pair identical (conflicts and model
  v-lines byte-identical); encoder metadata recorded; CNFs regenerable and
  not published (size policy, same as the m21 kit).

## Honest disclosures

- One execution-environment reset mid-session (a batched command exceeded
  the wall-clock cap). The pre-reset first observation (SAT, 2,050,424
  conflicts, identical decoded witness) and a pre-reset 6x23 minpos=7 run
  (INDET 5,076,037 at a 265s cap, same trajectory) are disclosed; all
  published raw logs were regenerated post-reset from re-fetched
  byte-identical scripts and the pinned kissat binary and reproduce those
  observations exactly.
- The 6x20 calibration ran before the declaration commit (disclosed in the
  declaration).
- Scope: witness existence only; no absence claim at any width (34 other
  canonical classes at 6x22 remain unswept). K0815 updated with a dai-8
  section and artifact; `results/fixed-width/mwq_stabilization.csv` (6,7)
  row updated to [23,402], frontier 6x23.
- Standard 11x11 empty board, two-stone roots, third move, S2, closure
  classes: UNKNOWN at all times; verdicts not consumed.

## Next tasks (fast lane candidates)

1. (6,7) 6x23: continue the class {2} k=5 minpos sweep (P = 0..5, 9..18
   remain), or two-edit surgery of the new m=22 witness on 6x23 targeting
   the uncovered cells of its right-shift (the m=22 witness is
   one-stone-short on 6x23 at (0,2)).
2. (6,6) 6x26 and (7,6) 7x32 frontiers remain untouched; the krow/minpos
   decomposition that collapsed 6x22 is directly transferable.
