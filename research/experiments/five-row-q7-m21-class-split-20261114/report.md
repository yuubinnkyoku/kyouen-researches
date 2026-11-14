# 5x21 q=7 row-deficient maximal nonexistence — all 19 canonical classes UNSAT

Date: 2026-11-14. The (5,7) witness frontier opened by K0816 (5x20 witness-free) is settled by
the same class-split SAT machinery as K0818/K0816's cross-check lane, now in the primary role.

## Claim

1. On the 5x21 integer grid (q=7), for every one of the 19 row-mirror-canonical deficiency
   classes D ⊆ {0..4} (canonical representatives of the 31 non-empty subsets under
   y -> 4-y), the class-split SAT instance — rows in D hold at most 5 stones (unit ¬rowGe[y]),
   rows outside D hold exactly 6 (unit rowGe[y]; safety caps every row at 6 since a row is a
   line of length 21 ≥ q), safety ≤ 6 stones per census curve, maximality (every empty cell
   covered by a ≥6-stone curve) — has **no solution**:
   - 17/19 classes directly **UNSAT** (kissat 4.0.4, exit 20; e.g. {2}: 708,186 conflicts;
     {0,1}: 1,050,634; {0,2}: 704,734; hardest direct: {2}).
   - {0} and {1}: the plain instances resisted single 280 s runs (≈6.0M / 5.7M conflicts,
     INDET) and are decided by the **complete k × minpos decomposition**
     (the K0816 protocol): k = 0..4 (exact deficient-row stone count, 5 instances each) and
     k = 5 × minpos = 0..10 (11 instances each). All 32 sub-instances **UNSAT**
     (hardest: {0} k=5 mp=0: 3,295,997 conflicts / 162.8 s; {1} k=5 mp=0: 2,851,122 / 118.2 s).
     Total conflicts across all 19 classes: 28,617,104.
2. Coverage: the exact deficiency set D = {rows with ≤ q-2 stones} is non-empty for every
   deficient maximal safe configuration and the exact-D instances partition them
   (K0818/K0816 class logic, brute-force-validated on small boards in K0818); the k×minpos
   decomposition is exhaustive: k = 0..5 partitions the deficient row's stone count, and
   for k = 5 every configuration or its column mirror has minpos ≤ 10 at m = 21
   (min(x1, 20−x5) ≤ 10 — otherwise x1 ≥ 11 and x5 ≤ 9, contradicting x1 ≤ x5); the column
   mirror preserves row occupancy, hence the class. Therefore **no row-deficient maximal safe
   configuration exists on 5x21**; every maximal safe configuration on 5x21 has 30 stones
   (row occupancy (6,6,6,6,6)).
3. Combined with K0738–K0759 (5x19 witness-free), K0816 (5x20 witness-free) and K0332
   (29-stone witness at 5x18, least witness width 18): the witness-free width set of (5,7)
   is **{19, 20, 21}**, so **M_{5,7} ∈ {19, 20, 21} or M_{5,7} ≥ 23**; the upper bound 158
   (K0332/K0024 substitution) is unchanged. The witness-search frontier moves to 5x22.

## Method

`sat3.js` class-split encoder on the K0810 census (circleABC integer triples — independent
of the K0738–K0759 runner's circumcenter form) and sequential-counter core, decided by the
official kissat 4.0.4 linux-amd64 binary. 2-worker parallel batches with per-instance
`timeout` 135–285 s; per-class conflicts and process-time taken from each kissat log.

## Verification

- **Positive control**: 5x18 q=7 class {0} **SAT** — 343,134 conflicts / 11.5 s; decoded
  model 29 stones rows (5,6,6,6,6), census-free `verifyConfig` PASS. This is the K0332
  witness board rediscovered end-to-end through the identical encode→solve→decode→verify
  path used for the 19 classes (same control as K0816).
- **Cross-encoding**: {0,1} and {2} re-encoded with --lex=H (lex-leader over column
  reflection — class-preserving, hence sound) are UNSAT again
  (639,843 / 488,589 conflicts).
- **Determinism**: the plain {2} instance reproduces 708,186 conflicts bit-exactly across
  the execution-environment reset that occurred mid-session (pre-reset first run and
  post-reset re-run identical).
- **Encoding-path sanity**: a multi-element-class encoding bug (`--class=01` parsed as
  Number("01") = 1) was detected during the sweep by an exact conflict-count collision with
  the singleton {1} instance and fixed before any use; all recorded multi-element classes
  were encoded with explicit comma form (verified via the per-instance `meta.json`).

## Scope and limits

Finite machine verification up to the correctness of the K0810 census, the class-split
encoding and k×minpos decomposition (protocol brute-force-validated in K0816/K0818), and
kissat 4.0.4; not a number-theoretic proof. Persistence at m ≥ 22 remains open: exact
M_{5,7} needs witness-free verification for all widths up to the K0332/K0024 bound U=158
or a universal tail argument. The witness frontier moves to 5x22: a witness there gives
M ≥ 23, witness-free there extends the free set to {19,20,21,22}. The 11x11 empty board,
two-stone root {49,60}, S2 {59,60}, class 2 and class 4 are unaffected and remain UNKNOWN.

## Files

- `scripts/sat3.js` (+ `sat2.js`, `sat.js` core, verbatim from the K0818/K0810 lanes)
- `scripts/runall57.sh` — deterministic sweep driver (19 classes + k×minpos decomposition + lex cross-checks + control)
- `scripts/mkrecords57.js` — records.jsonl/summary.json builder
- `output/records.jsonl` — 52 records (17 direct UNSAT + 32 decomposition UNSAT + 2 lex cross-checks + 1 positive control)
- `output/summary.json` — aggregate
- `output/r5x21q7_*.txt` — 51 raw kissat logs (UNSAT classes, splits, cross-checks) + `r_ctrl_5x18_c0.txt` (SAT control with model)
