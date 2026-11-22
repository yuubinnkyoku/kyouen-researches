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

Class (ii) 2R2A (c0=1) and class (iii) (c0=0) were NOT scanned at width 66
in this session: the naive complete Python implementation of 2R2A is
~13.8M final states (≈90 h at current per-candidate cost); class (iii)
needs 3 added stones which necessarily raises some row to q, breaking
def-mode (rows 0..5 already hold q−1 stones). Both remain open; resumed in
a later batch with the incremental-counts engine. This is a scoped local
negative, not an absence claim.

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

- `witness/w65-01.json` — witness record + discovery provenance
- `scripts/verify_int.py` — independent integer verifier (fixed variant)
- `scripts/surgery66.py` — class (i) width-66 surgery with resume-by-a1 progress
- `output/verify_w65-01.json`, `output/tamper-and-controls.json`
- `output/translation_sweep_54_75.json` — full sweep machine record
- `output/surgery66_summary.json`, `output/surgery66_results.jsonl` (empty: 0 hits)
- `MANIFEST-sha256.txt`

Reproduce: `python3 scripts/verify_int.py witness/w65-01.json`;
`python3 scripts/surgery66.py` (uses `w65-01.json` in cwd);
sweep via the code inlined in the session log.
