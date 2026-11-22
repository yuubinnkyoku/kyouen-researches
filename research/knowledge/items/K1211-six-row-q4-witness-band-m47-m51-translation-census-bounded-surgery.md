# K1211: the (6,4) witness band extends to m=51 — four width-47 witnesses by pure translation of the published m=46 witness, an R(S)=51 surgery-and-translation chain to m=48/49/50/51, three-family verification, and M_{6,4} in [52, 1113]

Date: 2026-11-21
Lane: standard-rule fixed-width q=4, six-row band ("(6,4) m=47 witness
constructive surgery" fast lane). Single-owner declaration:
`research/log/2026-11-21-six-row-q4-m47-witness-surgery-single-owner-note.md`
(commit `ad2c411`, 2026-11-21T20:24Z, HEAD-at-declaration `b19d79a6`),
with acceptance conditions: clean-room engine, K1209 positive control,
>= 2 independent integer verification families, byte-identical
determinism runs, negatives as finite bounded-neighborhood records
only, csv unmodified. All conditions were met except the positive
control in full: 56/64 of the published K1209 hits were rediscovered
(gap diagnosed exactly — see claim 6), compensated by a three-family
83/83 re-verification of the complete published control bank.

## Claims (each machine-verified and exactly scoped)

1. **R(S) translation census of the published (6,4) band-top witnesses
   (exact integer arithmetic).** Calibration gate (asserted in-engine,
   fail-closed): the published m=46 witness at its published position
   has R=46, first unblocked cell (46,0) — m=47 was a genuine frontier
   (previously blocked behind the SAT CNF RAM wall of
   `six-row-q4-m47-rowY0-oom-20261115`). Over the published seeds
   m=41/42/43/44/m46 (1708 placements, D4 images x shifts, scan 120):
   the m=41..44 families reach at most R=41/42/43/44; the m=46 family
   reaches **R=47 in exactly 4 placements** (id/V shift 5, H/HV shift 6).
   Consequence: **four width-47 witnesses with the m=46 stone structure
   unchanged — pure translation, no stone edit**; each 17 stones, rows
   rows [2,3,3,3,3,3] up to the vertical mirror
   (single-deficient, row 0 or row 5).
2. **Width-48 by bounded-edit surgery.** From the four width-47
   placements on the 6x48 board: remove<=2/add classes 1R1A/2R1A/2R2A.
   The H/HV shift-6 seeds yield 2 witnesses each (W1, W2 and their
   V-images; all from the 2R2A class — the same fertile class as
   K1209); the id/V shift-5 seeds yield 0 (case-c scope applies).
   **Four width-48 witnesses**, 17 stones, single-deficient (rows
   [2,3,3,3,3,3] or its vertical mirror).
3. **Widths 49/50/51 by translation of W1.** Census over the W1/W2
   families (680 placements): **four W1-family placements reach R=51**
   (id/V shift 6, H/HV shift 9; consecutive placements reach 49, 50,
   51); the W2 family stops at R=48. Consequence: **widths 49, 50, 51
   are witnessed**; the id/V W1 stone set witnesses **ten consecutive
   widths 42..51** — the widest single-set staircase recorded for
   (6,4) (K1209's (5,4) analogue was nine, widths 32..40). An
   intermediate bounded-surgery chain at the R=48..50 seeds found
   nothing (16 negative runs, not part of the published raw set): the
   48->51 advance here is translation, not stone edits.
4. **51->52 bounded escalation: negative, scoped.** On the four R=51
   placements, 6x52 board, classes 1R1A/2R1A/2R2A/3R1A/3R2A
   (pairCandidates up to ~2.27M per seed): **0 witnesses**. Scope: the
   single-add classes are complete; the pair classes cover only
   blocking through >= 2 surviving seed stones; remove-3/add-3 is not
   implemented. **m=52: UNDETERMINED** — a finite negative record, not
   an absence proof.
5. **Band update (the only value change).** With widths 6..46 published
   (K1207 re-verified bank m=6..31; `four-row-q4-q5-frontier-20261115`
   batches to m=46), this lane adds m=47..51:
   **M_{6,4} in [52, 1113]** (lower bound: width 51 witnessed; upper
   bound T_6 = 1113 = B_max(6)+1 from the K1207 demand-supply
   inequality, unchanged). `mwq_stabilization.csv` is unchanged
   (K1201 precedent); the frontier moves to m=52.
6. **Verification and the positive-control outcome.** Witness bank
   (20 stone sets) and control bank (83 items: the complete published
   K1209 m=40 material) verified by **three independent integer
   families** (engine 4x4-determinant + exact curve registry; Fraction
   center-radius; BigInt Bareiss): **20/20 and 83/83 PASS, zero
   disagreement**; add/move-stone tamper fails loudly on every family;
   every main output pair (census x2, surgery rounds x2, control x2)
   is byte-identical (deterministic engine, seedless). The engine
   rediscovers **56 of the 64 published K1209 hits** (14 per image, all
   56 subset of the published set, stone-set level): the 8 missing hits
   each contain exactly one empty cell whose every blocking curve holds
   exactly one surviving seed stone plus both added stones (case c) —
   a coverage class engine v2 does not enumerate (diagnostic machine
   record in the experiment, re-derived independently at publication
   time). The published bank itself passes all three families, so the
   gap is a search-restriction gap in this engine, not a disagreement
   about witnesses.

## What this is not

- No completeness claim for the width-47..51 witness populations: only
  the declared translation families and bounded-edit neighborhoods were
  searched (pair classes within the >= 2-survivor coverage scope).
- No existence or absence claim at m=52 or beyond: UNDETERMINED.
- mwq_stabilization.csv is unchanged (K1201 precedent).
- The positive-control reproduction is 56/64, not 64/64; the
  acceptance condition is recorded as partially met with the exact
  single-cell diagnosis.
- The standard 11x11 empty board, two-stone roots {49,60}/{59,60},
  S2 {59,60}, class 1/2/4 are unrelated to this lane and remain
  UNKNOWN.
- The K1207 inequality and the published band witnesses m<=46 are used
  as verified inputs; not re-derived here. K1209's publication is not
  modified.

## Evidence

- Experiment: `research/experiments/six-row-q4-m47-m51-witness-chain-20261121/`
  (README, 3 scripts, 14 configs, 21 raw outputs incl. banks, three
  verification batteries, case-c diagnostic and sha256 pins;
  fetch-back byte-verified).
- Session log: `research/log/2026-11-21-six-row-q4-m47-m51-witness-chain-session.md`.

## Relations

- Uses K0853/K1209 methodology (append-criterion census lineage and
  bounded-edit surgery with the 2R2A fertile class; the K1209 control
  material is this lane's positive control).
- Uses K1207 (T_6 = 1113 upper bound; re-verified (6,4) bank m=6..31;
  demand-supply inequality source of B_max(6)+1).
- Uses the published (6,4) band witnesses m=41..46
  (`four-row-q4-q5-frontier-20261115` / band-extension batches; the
  m=46 constructive free-column-append record is the census calibrant).
- Bypasses, and does not resolve, the
  `six-row-q4-m47-rowY0-oom-20261115` SAT frontier (constructive
  witnesses move the lower bound past it without touching the SAT
  lane; that lane's INDET record stands as-is).
- Six-row counterpart of K1209 ((5,4) band to m=40): same honesty
  rules; the (5,4) m=41 / (6,5) m=29 / (6,6) m=25 / (6,7) m=22
  frontiers remain the other lanes' territory.
