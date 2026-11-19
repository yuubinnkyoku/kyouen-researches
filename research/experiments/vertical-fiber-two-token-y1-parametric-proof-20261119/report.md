# Universal proof of the y=1 two-token parametric closed form for all z >= 6

## Status of this document

A **proof + verifier** artifact. It closes Conjecture P1 of the parametric census
(`vertical-fiber-two-token-y1-parametric-census-20261119`) for the universal range
**z >= 6**:

> **Theorem (P1, z >= 6).** For every fiber parameter `z >= 6`, every `x >= 1` and
> every `R >= 0`, the two-token residual-game value `H(R; (x,1); z)` is given by
> the published parametric closed form `cand(z, x, R)` (transcribed verbatim in
> this verifier from census commit `9f7899a8`; tables reproduced in the census
> report).

For `z = 1..5` nothing universal is claimed here: those slices remain
**exhaustive finite verification only** (V1 below extends the raw census to
`z = 1..30` on both engines).

## Proof structure

The proof is a **parity-alternating induction on z** with an inner induction on x,
as identified in the census report, carried out by band algebra that is uniform in
(z, x, R):

1. **Base z = 6** is the published theorem K0877 (z=6, y=1 slice).
2. **Closure identity.** For z >= 7 the option set of H(R; (x,1); z) at any x >= 1
   consists of the A-child `H(R-1; (x-1,1); z)` (x >= 2; the two token-decrement
   moves coincide at x = 1), the B-child `single_token(x, z+1, R-1)`, and the
   C-child `1 ^ H(R-1; (x,1); z-1)`. Hence the universal statement follows by:
   outer induction on z (C-child = the z-1 slice), inner induction on x (A-child
   = the x-1 row of the same slice), K0832 for the B-child, and the *closure
   identity* `cand(z,x,R) = mex{A, B, C}` evaluated through the closed forms.
   If the closure identity holds for all x >= 1, R >= 0 at a fixed z >= 7 and the
   closed form holds for z-1 (and for single tokens), the closed form follows
   for z. This reduces P1 (z >= 6) to the closure identity for all z >= 7.
3. **Symbolic promotion of the closure identity (V5).** The parameter plane
   z >= 7, x >= 1 is partitioned into **21 row classes** (family E: z even >= 8,
   10 classes; family O: z odd >= 7, 11 classes; E1/O1 are the x = 1 rows,
   EL/EO/OL/OO2/OO are ladder-distance classes in m = z - x, EH/OLm1 the x = z-1
   rows, EG0/OG0 the d = z rows, EG1/OG1 the d = z+1 rows, ES/OS the sweep rows
   x = z+2, ESo3/OSe3 the x = z+3 rows, ESoD/OSeD/ESe/OSo the stable x >= z+4
   split by k = x - z parity). The classes partition all x >= 1 at every z of
   their family by construction (interval union over m/k ranges; machine-checked
   pointwise in V5). On each class, all four R-profiles of the closure identity
   `F0/FA/FB/FC` are explicit **symbolic band tables** with affine endpoints in
   (z, m) or (z, k). The audit per class checks:
   - **sym-eval**: band tables == the code formulas (`cand`, `single_token`)
     at every sample point, for all R up to maxflip+8;
   - **slope structure (P2)**: pairwise slope kinds (z/m/k) of all flip forms
     are as asserted, so the *pattern* of the flip arrangement (order of flips
     + adjacency classes {1, >=2}) is constant on the class's stable box;
   - **cross-sample (P5)**: at two pattern-equal box points the per-(segment,
     R-parity) values of all four functions and the closure verdict agree
     directly, i.e. one passing anchor certifies the entire box;
   - **partition**: every sampled (z, x) hits exactly one class; no gaps, no
     overlaps (6,179 points over z = 7..80, x <= 260, 0 failures).
   Every unstable strip (where the pairwise-slope structure has not yet
   settled) is bounded by machine-checked arithmetic: z-kind strips end at
   `z <= zmid <= 6`, m-kind strips at `x <= xmax <= 2` (m-class boxes split
   into the small-x sub-box and a deep box, each carrying its own
   pattern-equal anchors), k-kind strips at `z+k <= skmid <= 11` — all
   inside the concrete V3 box (z <= 120, x <= 4z+240) by a wide margin;
   the verifier re-asserts the containment bounds (zmid <= 118,
   xmax <= 268, skmid <= 125) per class at audit time.
   Beyond the strip the anchor checks pass, so the closure identity holds on
   every class box, hence for **all** z >= 7, x >= 1, R >= 0.
4. Together: base z = 6 (K0877) + closure identity for all z >= 7 (step 3) +
   K0832 (B-child) => **the closed form holds for all z >= 6, x >= 1, R >= 0**.

The z = 16..60 slices of the census report, the z = 16 slice publication of
2026-11-19, and all ten published per-z y=1 theorems (K0877, K0977, K0983,
K0985, K1003, K1012, K1016, K1017, K1018, K1020) are corollaries of this
theorem; the published per-slice proofs remain the independent bases for
z = 6..16 and are used here as B/C-child anchors, not replaced.

## Verifier stages (verify_y1_parametric_proof.py)

Self-contained single file (the published z = 6..15 slice verifiers are
**embedded verbatim**, extracted with the ast module from the published scripts;
no retyping). Exit 0 iff all stages pass; total runtime ~50 s.

| stage | content | points | result |
|---|---|---|---|
| V0 | `single_token` (K0832) vs raw recursion, both engines, x<=24, z<=33, R<=72 | 59,568 | PASS |
| V1 | `cand` vs raw recursion, **both engines**, z = 1..30, x <= max(3z+40,70), R <= x+z+8 (finite census; z = 1..5 live here only) | 203,910 | PASS |
| V2 | `cand` vs the ten published z = 6..15 slice formulas (verbatim ast extraction), x <= 400, R <= x+11 | 850,000 | PASS |
| V3 | closure identity `cand == mex{A,B,C}` concrete sweep, z = 7..120, x <= 4z+240, R <= x+z+10 | 19,615,182 | PASS |
| V4 | joint raw == closure == cand, both engines, z = 7..16, x <= 3z+40, R <= x+z+8 | 44,015 | PASS |
| V5 | symbolic audit: partition (6,179 pts) + full 21-class audit (slope kinds, thresholds, sym-eval 21,394 R-values, anchor closures, cross-sample pattern equality over 1,072 segment-value reps) + unstable-strip containment in the V3 box | 21 classes | PASS |
| V6 | height-only collapse `cand == single_token(x+1, z, R)` for R <= z+1, z = 6..80, x <= 3z+120 (**finite corroboration only**) | 945,825 | PASS |
| V7 | audit.json re-serialization byte-identical (determinism) | - | PASS |

Stage-level details are recorded in `output/audit.json` (deterministic, no
timestamps; byte-identical across runs). All 21 class records carry
`max_unstable_threshold <= 11`.

## Scope boundaries and non-claims

- **z = 1..5**: finite census only (V1); no universal claim. The universal
  quantifier starts at z = 6. Promoting z = 1..5 needs a separate analysis of
  the 0/1-slice residue (the C-child chain bottoms out in z = 0 boundary
  behaviour that the stable bands assume away).
- **y >= 2**: not touched; the y = 2 family has published slices (K1013, K1016,
  K1019, K1021 for z = 11..12 range) but no parametric proof yet.
- **Height-only collapse** (`P2` of the census: identity holds on R <= z+1 and
  first fails at R = z+2) is extended here **finitely** to z = 6..80; the
  universal statement remains a conjecture.
- The 11x11 open problems remain UNKNOWN; this is the fast lane.
- z = 16 and beyond: covered by the theorem (and independently corroborated
  by the z = 16 slice publication and the census z = 17..60 rows).

## Artifacts

- `verify_y1_parametric_proof.py` — SHA-256
  `278f7af2a6d099a987abdf8e0bdb49567675290808e0b4ce72379a6d1ae62fd8`
- `output/audit.json` — SHA-256
  `ab80f73c6e63395d72bba2581393a26c5932cf0b5dbd67932571e4845ded546a`
  (byte-identical across runs and across the two-stage rebuild; no timestamps)
- Runtime: ~50 s per run (single process, pure Python, no deps).

## Provenance

- Parametric candidate `cand()` and `single_token()`: census commit `9f7899a8`
  (`vertical-fiber-two-token-y1-parametric-census-20261119`), transcribed
  verbatim.
- Published slice verifiers embedded verbatim: z = 6 (`...z6-y1-boundary-20261117`),
  z = 7..10 (`...z{z}-y1-boundary-20261119`), z = 11..15
  (`...z{z}-y1-boundary-20261119`).
- This lane (2026-11-19): stage-1 sym-eval and stage-2 pattern audit built and
  run against the code formulas; standalone verifier assembled and re-run
  twice locally (byte-identical audit.json).
