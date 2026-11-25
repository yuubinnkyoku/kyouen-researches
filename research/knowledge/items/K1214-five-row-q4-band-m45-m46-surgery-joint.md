# K1214: the (5,4) witness band extends to m=46 — SurgeryJoint (engine 2-addition coverage gap closed by an exact joint pool) finds 17 m=45 witness species and 4 species families at R=46, with the m=47 frontier UNDETERMINED under budget-3 joint surgery; M_{5,4} in [47, 567]

Date: 2026-11-21
Lane: standard-rule fixed-width q=4, five-row band (fast lane). Single-owner
declaration: `research/log/2026-11-21-five-row-q4-m45-surgery-single-owner-note.md`
(commit `59b1251aa7360d48ed0a553212fda9ddd38da9b6`, HEAD-at-declaration `451e0fe8e4`,
2026-11-21). Acceptance conditions: published engine/pin byte-identical re-use,
census calibration against the published K1209 surgery positive control,
3-system verification with tamper negative controls, byte-identical determinism
doubles, lower-bound-only value update, csv untouched. All conditions met.

## Claims (each machine-verified and exactly scoped)

1. **Engine coverage gap closed (method result, first).** The published five-row
   surgery engine (`engine_v2.py`, used byte-identical, unmodified) enumerates
   2-addition blocker candidates only as "addition z on a curve through the target
   cell and a pair of surviving stones". A final-set cell can additionally be
   blocked by the *joint triple* {one surviving stone + both additions} (the same
   shape K1213 called case-c on the six-row control). On the published K1209
   m39→40 positive control this is load-bearing: the engine alone reproduces
   14/16 witness stone sets per D4 base; the new SurgeryJoint
   (`scripts/surgery45.py`, subclass, engine unmodified) reproduces **16/16
   completely** across all 4 D4 images with exact set equality (2 runs
   byte-identical). The exactness argument: for each removal set the mode-(d)
   pool jpool(u, y) = OR over survivors s of the cells of curve(u, s, y) makes the
   pairwise prefilter exact — every surviving z reaches the final verifier.
   Also recorded: two implementation hazards found by cross-checks (disc=0
   duplicate curves; degenerate joint curves at removed-stone coordinates).
2. **m=45 witnessed by surgery (17 species).** Bounded-edit surgery (removal
   budget 2, complete classes 1R1A/2R1A/2R2A with the joint mode) from the 34
   published K1209-derived census placements with R>=41: 10 placements yield 34
   witness records, **17 D4-canonical species** (14 stones each, row type
   [3,2,3,3,3], min_row 2). Verified by 3 independent integer families
   (engine det4; append_criterion.py exact Fractions; verify_node.mjs BigInt
   Bareiss): 17/17 OK, tamper control fails loudly.
3. **m=46 witnessed (band update, the only value change).** A scan-60 D4 x
   translation census over the 17 species (1792 placements, two fail-closed
   calibration gates: w45-05 id0 -> R=46, w45-00 id0 -> R=45) reaches **R=46 in
   16 placements** from 4 species families (w45-05, w45-11 directly; w45-13 and
   w45-16 via mirrored placements), with **no R=47 placement in the scan**
   (bounded-family negative only). Addendum: scan-96 and scan-128 censuses
   (4240 / 6416 placements, byte-identical doubles, gates re-asserted) show
   **translation saturation** — max R stays 46, and both the 16 R=46 and 64
   R=45 key sets are identical to the scan-60 sets; no R>=47 placement exists
   in any D4/translation window up to shift 128
   (`output/census-45w-saturation.json`). All 16 R=46 placements re-verified as
   5x46 witnesses by engine verifymany and node (16/16 each; criterion
   witness_widths agree). Every width m in {45, 46} is therefore witnessed:
   **M_{5,4} in [47, 567]** (lower bound 45 -> 47; upper bound T_5 = 567
   unchanged, K1207). `mwq_stabilization.csv` unchanged (K1201/K1209/K1212
   precedent). The frontier moves to m=47.
4. **Staircase records replaced.** w45-00 / w45-01 (maxx=25) are witnesses at
   **20 consecutive widths 26..45** (previous (5,4) record: 9 widths, K1209,
   then [25,44] by K1212); w45-16 at widths 30..46 (17 consecutive). Re-verified
   per width in a dedicated re-run (staircase-45.txt).
5. **m=47 negative searches (scoped).** Budget-2 and budget-3 joint surgery
   (budget 3 adds classes 3R1A/3R2A complete) over all 16 R=46 placements:
   zero witnesses (~5 s and ~33 s per placement). This is a bounded-neighbourhood
   non-discovery record; **no absence claim** — m=47 remains UNDETERMINED.

## What this is not

- No completeness claim for the m=45/46 witness populations (only bounded-edit
  neighbourhoods of the published seeds and D4 x translation re-placements of the
  17 species were enumerated).
- No existence or absence claim at m=47: UNDETERMINED.
- The joint pool completes the 2-/3-addition prefilter classes only; higher
  budgets are future work. The six-row case-c engine (K1213) is a separate
  implementation and was not touched.
- csv/T_5 unchanged; standard 11x11 questions unrelated and remain UNKNOWN.

## Evidence

- Experiment: `research/experiments/five-row-q4-band-45-46-surgery-20261121/`
  (README with method + claims + honesty record; the new surgery45.py plus the 4
  published scripts byte-identical; configs incl. the census config with calib
  anchors; outputs: control 16/16, m45 hunt jsonl, witness bank, criterion record,
  census extract and translation-saturation record
  (full censuses byte-pinned and regenerable), verification batteries for
  m=45 and all 16 R=46 placements, tamper checks, m=47 budget-2/3
  negatives, staircase re-run; sha256 digests for outputs/scripts/published
  inputs, fetch-back byte-verified).
- Session log: `research/log/2026-11-21-five-row-q4-band-45-46-surgery-session.md`.

## Relations

- Uses K1209: m39→40 surgery as the positive control (the engine gap was found
  reproducing it); the published m40-seeds census that seeds the m=45 hunt; the
  s5x39q4 seed; erratum precedent (K1212) for README/raw consistency norms.
- Uses K1212: the 41plus census/pins (byte-identical inputs) and the band
  accounting ([45,567] before this item).
- Confirms K1213's case-c diagnosis as a general engine-design phenomenon
  (five-row instance here), with an exact-pool construction that other lanes can
  reuse; the six-row counterpart remains theirs to apply.
- Uses K1207 (T_5 = 567).
- Non-goals (other lanes' territory, untouched): six-row m=52+ questions, the
  q6/q5 m21/m25 species lanes, seven-row band, 11x11 root lanes, csv.
