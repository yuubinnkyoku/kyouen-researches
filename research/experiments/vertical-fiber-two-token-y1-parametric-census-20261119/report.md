# Parametric closed form for the two-token residual-game y=1 family: census over z = 1..60

## Status of this document

A **census + conjecture** artifact. It contains:

1. an explicit parametric closed form `cand(z, x, R)` for `H(R; (x,1); z)` (the two-token
   residual game with fiber parameter `z`, tokens `(x, 1)`) as a function of `z` and
   the parity of `z`;
2. an exhaustive finite census of this candidate against two independent raw
   recursions over `z = 1..60`, `x <= max(60, z+8)`, `R <= x + z + 6`;
3. third-source agree checks against the published slices K1018 (z=14) and K1020 (z=15);
4. an extension of the height-only collapse observation to `z <= 60`.

**Proof status.** The candidate is a **published theorem** for z = 6..15 (slices
K0877, K0977, K0983, K0985, K1003, K1012, K1016, K1017, K1018, K1020 cover
z = 6,7,8,9,10,11,12,13,14,15 at y = 1 respectively). For z in {1,2,3,4,5} and
z = 16..60 the results here are **exhaustive finite verification** on the stated
grid, NOT a universal proof. The claim "for every z >= 1" (all x, all R) is a
**conjecture** (Conjecture P1 below). No overclaim is made.

## The parametric closed form

Notation: `O[a,b]` = odd integers in `[a,b]`; `E[a,b]` = even integers in `[a,b]`;
`I[a,inf)` = integers `>= a`; `S = x + y + z` with `y = 1`, i.e. `S = x + z + 1`.
`H = 2` on the T-set, `H = 1` on the P-set, `H = 0` otherwise; `H(0) = 0`.

### Even z (z = 2, 4, 6, ...)

T-set (value 2), by row x:

| rows | T-set |
|---|---|
| x even, 2 <= x <= z-2 | O[1, x+1] |
| x odd, 1 <= x <= z-3 | O[1, x] |
| x = z-1 (the h = z row) | O[1, z+1] |
| x = z, x = z+1 | O[1, z-1] |
| x = z+2 (sweep row) | O[1, z-1] ∪ O[z+3, 2z+3] |
| x >= z+3 | O[1, z-1] ∪ {z+3} |

P-set (value 1), by row x:

| rows | P-set |
|---|---|
| x odd, x <= z-1 | ∅ |
| x even, x <= z-2 | I[x+2, ∞) |
| x = z | I[z+1, ∞) |
| x = z+1 | {z+1} |
| x even, x >= z+2 | {z+1} ∪ E[z+4, S-1] ∪ I[S+1, ∞) |
| x odd, x >= z+3 | {z+1} ∪ E[z+4, S] |

### Odd z (z = 1, 3, 5, ...)

T-set (value 2):

| rows | T-set |
|---|---|
| x even, 2 <= x <= z-1 | O[1, x+1] |
| x odd, 1 <= x <= z | O[1, x] |
| x = z+1 | O[1, z+2] |
| x = z+2 (sweep row) | O[1, 2z+3] |
| x >= z+3 | O[1, z] ∪ {z+2} |

P-set (value 1):

| rows | P-set |
|---|---|
| x odd, x <= z-2 | ∅ |
| x even, x <= z-1 | I[x+2, ∞) |
| x = z | {z+1} |
| x = z+1 | {z+1} ∪ I[z+3, ∞) |
| x = z+2 | {z+1} |
| x odd, x >= z+3 | {z+1} ∪ O[z+4, S] |
| x even, x >= z+4 | {z+1} ∪ O[z+4, S] ∪ I[S+1, ∞) |

### Structural reading (uniform-in-z features confirmed by the census)

- Value-2 ladder: even z tops at `z-1` (plus pin `z+3` in stable rows), odd z tops
  at `z` (plus pin `z+2`). The pin is `pin = z + 2y + [z even]` with y = 1.
- The advanced point `z+1`: for even z it is a **T-point** on the `h = z` row
  (x = z-1, extending the ladder top from z-1 to z+1); for odd z it is a
  **P-point** appearing first on row x = z and then on every higher row.
- The sweep row is x = z + y + 1 = z+2 for both parities. Its band is
  `O[pin, x+y+z]`: for odd z the pin `z+2` sits exactly 2 above the ladder top
  `z`, so the union with `O[1,z]` collapses to the contiguous `O[1, 2z+3]`;
  for even z the pin `z+3` leaves a 2-gap after `z-1`, and the sweep T-set
  keeps the gap `z+1` (the point `z+1` belongs to the sweep P-set instead).
- Mid-band P runs: even z uses E-bands `[z+4, S-1]` (even x) / `[z+4, S]`
  (odd x >= z+3); odd z uses O-bands `[z+4, S]`. Tail: `I[S+1, ∞)` on even-x
  rows (>= z+2 for even z, >= z+1 for odd z), i.e. `H = (x+1) mod 2` for
  `R >= S+1`; odd-x stable rows are value-0 beyond S.

## Census

Engine: the two raw recursions `H_ordered` / `H_canonical` (copied verbatim from
the published census scripts of the slice lane; order-preserving vs sorted-token
formulations). Grid per z: `x in [1, max(60, z+8)]`, `R in [0, x+z+6]` — the
R-range covers the mid-band and reaches 4 levels past the tail start
`S+1 = x+z+2`, so the I-band onset and the first tail values are inside the
grid for every family.

Result (`census_y1_parametric.py`):

- z = 1..60: **60/60 CLEAN**. No mismatch anywhere.
- Total 249,408 points checked; both engines agree on all of them
  (0 engine disagreements).
- `x <= 60` for z <= 52 (>= 8 stable rows beyond the sweep row for every z);
  for z = 53..60, `x <= z+8`.
- Two consecutive runs produce a byte-identical `output/census_summary.json`.
- The R-grid extends to `x+z+6 >= S+4`, covering the band edge at `S-1`, `S`,
  the I-band start `S+1`, and `S+2..S+4` inside the tail.

## Agree checks against published slices

- vs published K1018 formulas (z=14, y=1; transcribed verbatim from the
  published `census_z15_y1.py` child functions): x <= 200, R <= x+34:
  27,100 points, **0 mismatches**.
- vs published K1020 formulas (z=15, y=1; transcribed verbatim from the
  published `verify_z15_y1.py`): 27,100 points, **0 mismatches**.

Together with the published machine audits (27.6M-point verifiers), the
candidate coincides with the published theorems on every audited point at
z = 14, 15.

## Height-only collapse extended to z <= 60

Identity: `H(R; (x,1); z) = single_token(x+1, z, R)` for `R <= z+1`
(`single_token` = the published K0832 closed form; prior finite observation
covered z = 4..15).

- Over z = 1..60, x <= max(60, z+8), R <= z+1: **119,148 points, 0 mismatches**.
- The identity breaks at `R = z+2` for **all 60 z values** (first break exactly
  at z+2, consistently with the prior per-slice observations), supporting the
  refined conjecture that the identity holds **exactly** on `R <= z+1` for all z.

## Conjecture

**P1.** For every integer `z >= 1` and `y = 1`, `H(R; (x,1); z)` is given by the
tables above (all `x >= 1`, all `R >= 0`).

Known theorem instances: z = 6..15 (published slices; see status section).
Census support: complete exhaustion of the structural rows and the full R range
up to `S+4` for z = 1..60 on both raw engines.

**P2** (height-only, sharpened). For every `z >= 1`: `H(R; (x,1); z) =
single_token(x+1, z, R)` holds for `R <= z+1` and first fails at `R = z+2`
(at some x).

## Identified proof route (for the next lane)

The published slice proofs (K1016..K1020 template) decompose each child option
as A (x-outer induction within the slice), B (`single_token(x, z+1, R-1)`), and
C (`1 ^` the published `z-1, y=1` slice). Since (i) B is uniform in z, and
(ii) C is the previous-z slice, a proof of P1 is a **parity-alternating
induction on z**: assuming the closed form for z-1, the same three-child
signature-band analysis closes the closed form for z, with the four case
splits (h=z row, grid row x=z+1, sweep row x=z+2, stable rows x>=z+3) proved
uniformly in z. The z=12..15 verifiers are literally constant-shifts of each
other in exactly the sense this uniform template predicts; a symbolic-band
verifier (V1..V14 with z kept symbolic) is the natural next artifact.

## Artifacts

- `census_y1_parametric.py` — SHA-256
  `b78f31992181f90279d4b29231ead038aa808d62d22b6897068b1146597b7c26`
- `output/census_summary.json` — SHA-256
  `82a206feafecd2a3cdca8ad0cdd437064417abfa1714258e506fd4cb8bbcb882`
  (byte-identical across runs; elapsed time is kept out of the JSON on purpose)
- Runtime: ~32 s per run (single process, pure Python).

## Non-claims

- No claim about z > 60 or x > max(60, z+8).
- No claim about y >= 2 slices.
- The 11x11 open problems (empty board, two-stone roots, S2, class 1/2/4)
  remain UNKNOWN; this line of work is the fast lane only.
