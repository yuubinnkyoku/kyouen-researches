# 2026-11-19 two-token y=1 parametric closed-form census (z = 1..60)

## Context

After publishing K1020 (z=15, y=1 slice, universal proof), the y=1 cross-z
family has published universal slices for z = 6..15: K0877 (z=6), K0977 (z=7),
K0983 (z=8), K0985 (z=9), K1003 (z=10), K1012 (z=11), K1016 (z=12),
K1017 (z=13), K1018 (z=14), K1020 (z=15) — with K1016/K1018 (even) and
K1017/K1020 (odd) forming, together with z=8,10 and z=9,11, two four-member
parity series. The natural next question is whether the whole y=1 family is a
single parametric closed form in z.

## What was done

1. Derived, from the published slice tables (both parities), an explicit
   parametric candidate `cand(z, x, R)` for `H(R; (x,1); z)`; the full tables
   are in the experiment report (`report.md`), covering, per parity: the
   ladder rows `x <= z-2`/`x <= z`, the `h = z` row (even z: T-point `z+1`),
   the plain rows `x = z, z+1`, the sweep row `x = z+2` with band
   `O[pin, x+y+z]`, the stable rows `x >= z+3` with pin `z+2y+[z even]`, the
   P-sets with the advanced point `z+1` (P-point for odd z from row x = z and
   for even z from row x = z+1), the E/O mid-bands `[z+4, S-1|S]`, and the tail
   `I[S+1, ∞)` on even-x rows.
2. Exhaustive census against the two raw recursions (order-preserving and
   descending-canonical engines, copied from the published census scripts):
   `z = 1..60`, `x <= max(60, z+8)`, `R <= x+z+6` (past the tail start
   `S+1 = x+z+2` by 4).
3. Third-source agree checks against the published K1018 (z=14) and K1020
   (z=15) formulas, x <= 200.
4. Extension of the height-only collapse observation
   `H(R;(x,1);z) = single_token(x+1,z,R)` from z=4..15 to z=1..60, including
   the first-break level.

## Results

- **z = 1..60: 60/60 CLEAN**, 249,408 points, 0 mismatches, both raw engines
  agree everywhere (0 engine disagreements). Two runs byte-identical
  (`output/census_summary.json`; elapsed time deliberately kept out of the
  JSON).
- Agree vs published K1018: 27,100 points, 0 mismatches. Agree vs published
  K1020: 27,100 points, 0 mismatches.
- Height-only identity on `R <= z+1`: 119,148 points, 0 mismatches over
  z = 1..60; first break at `R = z+2` occurs for **all 60 z values**
  (identity exact on `R <= z+1`).

## Interpretation and proof status

- The candidate is a **theorem** at z = 6..15 (published slices; the census
  agrees with the published machine audits pointwise at z = 14, 15).
- For z = 1..5 and z = 16..60 the grids are **exhaustive finite verification**,
  not proofs. The universal claim (every z >= 1, all x, all R) is recorded as
  **Conjecture P1**; the height-only collapse as **Conjecture P2**
  (exact on `R <= z+1`, first break at `z+2`).
- Identified proof route: parity-alternating induction on z with the uniform
  A/B/C child template of the K1016..K1020 verifiers (B = single_token child
  uniform in z; C = 1^ the previous-z slice; the z=12..15 verifiers are literal
  constant-shifts of each other, i.e. the template is already uniform). A
  symbolic-band verifier (V1..V14 with z symbolic) is the natural next
  artifact; alternatively a one-shot "even z theorem" + "odd z theorem" pair.

## Artifacts

- `research/experiments/vertical-fiber-two-token-y1-parametric-census-20261119/`
  - `census_y1_parametric.py` SHA-256
    `b78f31992181f90279d4b29231ead038aa808d62d22b6897068b1146597b7c26`
  - `output/census_summary.json` SHA-256
    `82a206feafecd2a3cdca8ad0cdd437064417abfa1714258e506fd4cb8bbcb882`
  - `report.md` (full parametric tables, bounds, status labels)

## Relation to the two-series structure

The even-z T-set keeps a 2-gap at the sweep row (`z-1 -> z+3`) while the odd-z
sweep collapses to contiguous `O[1, 2z+3]` because the pin sits directly above
the ladder top (`z -> z+2`). The advanced point `z+1` is a T-point on the h=z
row for even z versus a P-point from row x=z for odd z. These two parity
behaviors were previously established per-slice for z = 8..15; the census shows
they govern the whole range z = 1..60 without exception.

## Non-claims

Finite result: z <= 60, x <= max(60, z+8), R <= x+z+6. No claim about y >= 2.
The 11x11 problems (empty board, two-stone roots, S2, class 1/2/4) remain
UNKNOWN (long lane).
