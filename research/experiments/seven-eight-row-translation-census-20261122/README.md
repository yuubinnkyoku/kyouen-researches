# Seven-row q=4 width-65 witness (w65-01) — discovery, translation sweep, and width-66 class-(i) surgery

Lane: 高速レーン (single-owner declaration `66e7033b6e`, log
`2026-11-22-seven-eight-row-translation-census-single-owner-note.md`).
Date: 2026-11-22. All claims are existence claims or scoped finite negatives;
no absence claims anywhere. nodes/candidate counts are not read as outcomes.
標準 11×11 空盤・二石 root・class 1/2/4 は本レーン非接触で UNKNOWN のまま。

## Main result

**w65-01**: a 20-stone deficient maximal witness on the 7×65 board, q=4,
rows [3,3,3,3,3,3,2] (def-mode), stones:

    (10,2) (13,4) (14,6) (17,1) (17,3) (20,4) (26,3) (28,2) (29,5)
    (31,3) (32,0) (33,0) (33,1) (38,4) (42,2) (42,6) (43,1) (43,5)
    (57,0) (63,5)

⇒ **M_{7,4} ≥ 66** (previous lower bound 60; frontier moves 7x60 → 7x66).
Upper bound T_7 = 1929 unchanged. 7×66 remains UNDETERMINED (this experiment
does not decide it; below classes scanned are locally exhausted only).

Origin: 2R2A targeted surgery (class (ii), c0=1) on the translated
pair0-family id-image of the width-60 witnesses at shift +10 on the 7×65
board; remove [[21,5],[50,1]], add [[33,1],[63,5]]. Discovered by the lane's
JS surgery engine (session-lost, see session log), kept and fully re-verified
independently here.

## Verification (two independent systems)

1. JS engine (discovery engine, clean-room BigInt, session-lost):
   fullVerify safe+maximal+def, tamper check drop (13,4) → not maximal with
   cell (1,4) unblocked.
2. `scripts/verify_int.py` (this experiment, written fresh, no shared code):
   integer circles via 3×3 determinant, integer lines, lattice point
   enumeration by exact quadratic solution (isqrt discriminant, no floats).
   Result: safe=true (max curve count 3), maximal=true (0 unblocked cells of
   435), def=true. Tamper controls reproduced the JS engine's exact record:
   drop (13,4) → maxCurveCount stays safe but maximal breaks with (1,4) the
   first unblocked (23 unblocked total); relocate (13,4)→(50,6) → unsafe
   (5-point circle). See `output/verify_w65-01.json`,
   `output/tamper-and-controls.json`.

`verify_int.py` v1 had a real defect that this experiment caught and fixed:
`tangent` circles (discriminant zero, circle touching a lattice column line)
produced the same lattice point twice; the duplicate inflated per-curve stone
counts and produced spurious 4- and 5-stone "curves" (10 false unsafe curves)
plus a false unblocked list. The fix (collect roots in a set per column) is in
the published script. Lesson (already established by the 2026-11-21
verify_general.py incident): every verifier must be validated against negative
controls before its green outputs are trusted; here the negative controls are
what exposed the bug.

## Translation sweep (`output/translation_sweep_54_75.json`)

Left-flush-normalized D4 images × every pure-x shift on board widths 54..75,
each placement verified from scratch. The single w65-01 stone family witnesses
**12 consecutive widths 54..65**:

| width | witnesses |
|---|---|
| 54 | 4 (id/H/V/HV @ 0) |
| 55..64 | 8 each (id and H at two consecutive shifts + their V/HV mirrors) |
| 65 | 4 (id@10, H@1, V@10, HV@1) |
| 66..75 | 0 |

All found placements are def-mode (rows ≤ q−1). No width ≥ 66 placement of
the family exists in the scanned range (observation, scoped to this seed
family; NOT an absence claim about other stone sets).

## Width-66 targeted surgery, class (i) (`scripts/surgery66.py`, `output/surgery66_summary.json`)

Base: w65-01 id-image @ shift 11 on 7×66 (bbox cols 11..64). All cells
blocked except T=(0,6) (single-cell deficiency; left-roof cell).

Class (i) c0=2 completeness (blocking curve carries exactly 2 base stones +
one added stone on it): 190 distinct two-stone T-curves, 93 add cells
(empty cells on those curves, plus T itself). Final states verified from
scratch by verify_int.verify (safe+maximal, k preserved or reduced):
- **1R1A**: 1860 candidates complete, **0 hits**.
- **2R1A**: 17670 candidates complete (93 add cells × 190 remove pairs,
  addcells ∩ base = ∅ machine-checked), **0 hits**.

Class (ii) 2R2A was completed in batch 2 (see the next section): complete
over all def-compatible branches, 0 hits. Class (iii) (c0=0, T covered only
by added stones) needs the added stones to reproduce the base's blocking
without the base carrier; in the 2R2A partition it collapses into branch C
(T occupied by an add). This is a scoped local negative, not an absence
claim.

## Batch 2: width-66 class (ii) 2R2A complete + all-cap witness family (`scripts/surgery66_2r2a.py`, `scripts/fastv.py`, `scripts/wcap_1r1a.py`, `witness/w66-cap-witness.json`)

**Class (ii) 2R2A complete** (base = w65-01 id-image @ shift 11 on 7×66,
T=(0,6) the single unblocked base cell). The add-pair space is partitioned
by the carried-base-stone count of the curve that must keep unblocked cells
covered (def-mode enforced by row gates; 0R2A is def-incompatible because
both adds land in row 6):

- Branch A "(1,2)": both adds on one curve with exactly 1 base stone
  (final on-curve count 3 = q−1): 9,657 pairs
- Branch B "(2,1)": one add on a curve with exactly 2 base stones, the
  other add free (same-curve double adds skipped: final count 4 = unsafe):
  125,510 pairs (enumerated per (curve, a1, a2) role; R-avoid set differs
  per curve)
- Branch C: T occupied by an add, the other add anywhere empty: 441 pairs

Total 135,608 (remove-pair × add-pair) candidates; row-sum + hot-cell
gates admit 1,615,395; 102,385 unique final states screened with `fastv.py`
(exact residual-count screen over the same curve universe as verify_int;
dual-checked against `verify_int.verify` on the first 1,500 states and
every 250th thereafter: 1,877 checks, **0 mismatch**; only screen-passing
states would be confirmed authoritatively). **0 hits** → scoped local
negative over this seed's 2R2A neighborhood; 7×66 stays UNDETERMINED (no
absence claim).

**w66-cap-01 (all-cap witness).** Branch C's T-placement: base 20 stones +
cap stone (0,6) = 21 stones, rows [3,3,3,3,3,3,3], safe + maximal on 7×66
(`witness/w66-cap-witness.json`; verify_int 3×3-determinant circles + an
independent bisector/Fraction system, unblocked 0/0 both; tamper: removing
any single stone breaks maximality, 21/21).

**All-width family theorem.** The same 21-stone set is safe+maximal on
7×m for every width m ≥ 65 (any translation/mirror placement with span
65 ≤ m). Proof: safety depends only on the stone set (the curve universe
is generated by base pair-lines and triple circles and closed under board
resizing); maximality holds because each row carries exactly q−1 = 3
stones, so the horizontal line of row y blocks every empty cell of row y
at any width. Machine checks: all placements at widths 65..80 (4(w−64)
per width, all witnesses: 8/8 at w=66 … 64/64 at w=80) plus widths 1500
and 1929 safe+maximal (`output/w66cap_translation_sweep.json`,
`output/w66cap_wide_check.json`). This is the (7,4) counterpart of the
K0069 all-cap stable class. It does NOT move M_{7,4}: all-cap has no
deficient row and is outside the deficient-witness class that defines M
(M_{7,4} ∈ [66,1929] unchanged).

**Row-sum parity lemma.** A def-mode (7,4) config with |S| = 21 stones
must be all-cap (7 rows × 3 = 21); edit classes reaching 21 stones
(0R1A, 1R2A) therefore cannot produce deficient witnesses, and 0R2A (22
stones) is outside def-mode. With batch 1 this closes the complete
deficient-class surgery program around this seed: 1R1A (1,860) + 2R1A
(17,670) from batch 1, 2R2A (135,608) from this batch, 0R1A (64 add cells:
only T yields the all-cap config, the other 63 all-cap placings are not
deficient) — all complete, **0 deficient hits**.

**Cap-side 1R1A relocation sweep** (`scripts/wcap_1r1a.py`). From
w66-cap-01, all single relocations with add-row ≠ removed-row (so the
removed row stays deficient) at widths 66..80: 132,300 screens,
1,027 dual-checked vs verify_int (0 mismatch), **0 hits**. 1R0A single
stones: tamper already shows all 21 drops non-maximal; kR0A (k ≥ 2)
follows because an unblocked cell persists under stone removal
(persistence argument, machine-checked at the 1R0A level).

## Session incident (recorded for reproducibility)

The lane's earlier working tree (JS surgery engine, 26 width-60 witnesses
from pair0/band53 seeds, census chain records, staged negatives across
(7,4)–(8,10)) was destroyed by an infrastructure reset (Koyeb 503) before
publication. Of those, only w65-01 (printed in-conversation at discovery
time with full stones/removals/additions) survived verbatim; its two-system
verification above is the basis of this publication. The 26 width-60
witnesses' stone sets were lost and are NOT claimed here; reconstruction
(re-running the lost stages from published seeds) is queued for a later
batch. The (7,4) width-60 pair1-track published negative was reproduced by
the lost engine pre-reset (PC/NC controls all PASS pre-loss); those numbers
are recorded in the session log as session-only observations.

## Files

Batch 1 (width-65 witness + class (i)):

- `witness/w65-01.json` — witness record + discovery provenance
- `scripts/verify_int.py` — independent integer verifier (fixed variant)
- `scripts/surgery66.py` — class (i) width-66 surgery with resume-by-a1 progress
- `output/verify_w65-01.json`, `output/tamper-and-controls.json`
- `output/translation_sweep_54_75.json` — full sweep machine record
- `output/surgery66_summary.json`, `output/surgery66_results.jsonl` (empty: 0 hits)

Batch 2 (class (ii) complete + cap witness family):

- `witness/w66-cap-witness.json` — all-cap 21-stone witness stones
- `scripts/fastv.py` — exact fast screen (same curve universe as verify_int)
- `scripts/surgery66_2r2a.py` — complete 2R2A surgery, branches A/B/C
- `scripts/wcap_1r1a.py` — cap-side 1R1A relocation sweep, widths 66..80
- `output/surgery66_2r2a_progress.json` (135,608/135,608 complete),
  `output/surgery66_2r2a_log.jsonl`, `output/surgery66_2r2a_hits.jsonl`
  (empty: 0 hits)
- `output/w66cap_translation_sweep.json` (widths 65..80, all placements
  witnesses), `output/w66cap_wide_check.json` (widths 1500, 1929)
- `output/wcap1r1a_progress.json`, `output/wcap1r1a_log.jsonl`,
  `output/wcap1r1a_hits.jsonl` (empty: 0 hits)
- `MANIFEST-sha256.txt`

Reproduce: `python3 scripts/verify_int.py witness/w65-01.json`;
`python3 scripts/surgery66.py` (uses `w65-01.json` in cwd);
batch 2: `python3 scripts/surgery66_2r2a.py 240` and
`python3 scripts/wcap_1r1a.py 240` (resumable; writes `output66b/`
next to the scripts — published copies live in `output/`; run with
`witness/w65-01.json` copied next to `scripts/`).
 