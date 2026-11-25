# Universal proof of the parametric closed form for the two-token y=1 family (all z >= 1)

## Status of this document

A **proof artifact** for Conjecture P1 of the parametric census
(2026-11-19, `vertical-fiber-two-token-y1-parametric-census-20261119`),
closing the census's own "identified proof route" at full generality in the
fiber parameter z. It upgrades the census's finite z = 1..60 verification to
a universal statement over **every** z >= 1, x >= 1, R >= 0, by replacing the
per-slice signature-band tables of K1016..K1020 with a **finite type
machinery** that covers the entire (z, x, R) space.

What is proved here:

1. **Theorem P1** (`status: proved`). For every integer z >= 1, x >= 1,
   R >= 0: `H(R; (x,1); z) = cand(z, x, R)`, where `cand` is the parametric
   closed form published in the census (z-parity tables, reproduced
   verbatim in `verify_p1_universal.py` and identical, on every audited
   point, to the published slices K0877, K0977, K0983, K0985, K1003, K1012,
   K1016, K1017, K1018, K1020).
2. **Lemma Z** (base). For every x >= 1, R >= 0: `H(R; (x,1); 0) =
   cand0(x, R)` with the z=0 slice closed form derived here for the first
   time (table below).

What is NOT claimed: y >= 2 slices, the standard two-dimensional board,
fixed-width / q-point stabilization lengths, and 11x11 remain untouched
(fast lane only; see Non-claims).

## Relation to the sibling K1022 artifact

A parallel lane published, as K1022, a proof of the same candidate formula
restricted to **z >= 6** (experiment
`vertical-fiber-two-token-y1-parametric-proof-20261119`), derived from a
verbatim census of the published z-slice verifiers plus a signature-band
construction. Theorem P1 here is a strict extension obtained from an
independently constructed type machine: it covers **every z >= 1** and adds
the z = 0 base slice cand0 (outside K1022's statement), with no use of the
census tables as ground truth beyond formula reuse. The two derivations and
code bases are disjoint; agreement between them is a genuinely independent
double anchor and is audited by `cross_check_k1022.py` (next section).

## The z=0 slice (Lemma Z)

Notation as in the census: `O[a,b]` odd integers in `[a,b]`, `E[a,b]` even,
`I[a,inf)` integers >= a. Value 2 on the T-set, 1 on the P-set, else 0.

| row | T0-set | P0-set |
|---|---|---|
| x = 1 | ∅ | {1} |
| x odd >= 3 | {3} | {1} ∪ E[4, x+1] |
| x even >= 2 | {3} | {1} ∪ E[4, x] ∪ I[x+2, ∞) |

Derivation outline (machine-checked in development by independent census, in
the verifier by C1/C1b engine anchors and the C6 type machine): at z = 0 the
pass move does not exist, so the options of `(x,1)` at height R >= 1 are the
token decrement `A = H(R-1; (x-1,1); 0)` (only for x >= 2) and the y-token
removal `B = single_token(x, 1, R-1)` (K0832 at z'=1). Reading off
`single_token` gives the mex directly: x=1 has the single option
`single_token(1,1,R-1)` (value 1 exactly at R=1, else 0), and x >= 2 rows
combine B's ladder with A from the x-1 row, producing the T0 pin at R=3 and
the parity-homogeneous P0 sets above (odd x stop at x+1; even x continue to
infinity, mirroring the tail law `H = (x+1) mod 2` for R >= x+2).

## Proof architecture

Three ingredients, mirroring and generalizing the slice-lane template:

**(1) Option decomposition (z >= 1).** At any point `(z, x, R >= 1)` the raw
game has exactly the moves: decrement of the x-token (x >= 2), giving
`A = H(R-1; (x-1,1); z)`; removal of the y=1 token, giving
`B = single_token(x, z+1, R-1)` (K0832); and the pass z -> z-1, giving
`C = 1 ^ H(R-1; (x,1); z-1)`. At x = 1 the two token moves coincide into the
single token-child `single_token(1, z+1, R-1)`; the option-existence bit
"x = 1" is the **only** absolute read in the entire z >= 2 machinery
(Lemma S below). Machine anchor: C3 re-derives the option set from the raw
engines (1,350 points, 0 mismatches).

**(2) Induction on z.** Lemma Z is the base. For z = 1 the C-child is
`1 ^ cand0(x, R-1)`, so the identity of the closed form `mex(A,B,C) = cand`
reduces to Lemma Z plus the z=1 type machine (C5/C5b). For z >= 2, granted
the closed form at z-1 (strong induction), C = `1 ^ cand(z-1, x, R-1)`, and
the identity reduces to the z >= 2 type machine (C4/C4b): one identity
per realized type, uniformly in z. There is no per-z work left: the whole
family is a single finite case analysis.

**(3) The type machinery (universal -> finite).** Every closed form and
every child evaluation in the identity reads only a fixed finite family of
linear forms:

- z >= 2: the three parities `(z mod 2, x mod 2, R mod 2)`, the six
  difference forms `w0 = x-z, w1 = R-x, w2 = R-z, w3 = R-x-z, w4 = R-2x,
  w5 = R-2z` clipped to the exact window [-8, 8] with rays ±9, and the
  option-existence bit x = 1.
- z = 1: `(x mod 2, R mod 2)` plus absolute clips `x` in [1,24] (sentinel
  above), `R` in [0,80] (sentinel above), and relative clips `R-x` in
  [-24,24], `R-2x` in [-16,16] (rays beyond).
- z = 0: `(x mod 2, R mod 2)` plus the same absolute clips `x`, `R` and the
  relative clip `R-x` in [-24,24].

A **type** is a value of that finite signature. Two lemmas turn the
machinery into a proof:

**Lemma S (shift closure / type-determinedness).** Every predicate read by
`cand`, `cand0`, `single_token` or their children is a threshold comparison
on one of the family forms, with threshold |t| <= 6; child evaluations shift
each form by δ in {-2,-1,0,1} (z >= 2) or move within the absolute windows
(z = 1, 0). Consequently the full value vector (parent value + option
values, with A dropped when x = 1) is a function of the parent **type**
alone. The threshold table (all reads of all three forms) is in Appendix B;
the clip windows [−8,8]/rays 9 vs thresholds ≤ 6 leave a margin of 1 on the
tightest shifted ray comparison (child of a +ray sits at >= 7 > 6). The
verifier does not trust this lemma: it checks confluence on witness **pairs**
(5,486 z>=2 pairs, 420 z=1, 369 z=0: 0 mismatches) and on every probe point
(see the certificates below).

**Lemma W (witness bound).** Every **realizable** type has a witness inside
the enumeration box: |v0|, |v1|, |v3| <= 60 for z >= 2 (free coordinates
v0 = x-z, v1 = R-x, v3 = R-x-z; z = v1 - v3, x = v0 + v1 - v3,
R = 2v1 + v0 - v3), and x <= 140, R <= 320 / 300 for z = 1 / z = 0.
Proof sketch (Appendix A): pins have constants <= 8, rays sit at ±9,
domains (z >= 2, parities, x = 1 bit) shift coordinates by <= 9; every
coordinate of a minimal witness is fixed by a chain of at most three
family constraints plus one domain adjustment, giving |v| <= 45 < 60
(2-variable machines: pins <= 80 absolute, relative pins <= 24 give
witnesses <= 130 < 140/320).

The verifier then enumerates the box exhaustively (653,310 z>=2 domain
points; 45,080 + 42,000 for z = 1 / z = 0), collects all realized types
with a minimal witness each (**10,750** z >= 2, **5,458** z = 1, **4,994**
z = 0), and checks the identity once **per type**. Since every point of
the space has a type, and every realizable type's identity is checked,
the induction closes over all z, x, R simultaneously.

## Lever and certificates (machine audit)

`verify_p1_universal.py` (808 lines, pure Python, deterministic,
seeded RNG `20261119`), 23 checks, **all ok, 0 mismatches** on
1,875,269 audit points:

- **C1/C1b/C1c/C1d engine anchors.** Both raw recursions
  (order-preserving and canonical) vs `cand`/`cand0`/`single_token`:
  z = 0..6 x <= 16, R <= x+30 (8,848 points); single-token engine anchor
  (3,720); published K1018/K1020 formulas vs `cand` (11,460).
- **C2 formula identity grids**: z = 1..40, x <= 40, R <= x+z+40
  (129,600 points) — the slice identity holds with no engine, on
  formulas alone; z = 0 (12,000); R = 0 trivial rows.
- **C3 option decomposition anchor** vs raw engines (1,350).
- **C4/C5/C6 type identity**: one identity per realized type (21,202
  types in total), each with a minimal witness; C4b/C5b/C6b witness-pair
  confluence (6,275 pairs, 0 mismatches). Single-witness types are
  structurally all-pin types whose feasible set is a singleton lattice
  class (confluence vacuous); types with infinite feasible sets are
  additionally confluence-tested by the probes below.
- **C7 seeded far probes**: 200,000 points, z, x <= 3000, R <= 9000:
  identity + type membership + confluence vs box witnesses, 0 failures.
- **C8 boundary manifold probes**: z in {2,3,97,98,997,998,2999,3000}
  with x, R swept across all six family manifolds (± windows):
  11,686 points, 0 failures.
- **C9 z=0/z=1 far probes**: 60,000 points, x <= 5000, R <= 15000,
  both machines: 0 failures.
- **C10 engine deep anchor**: raw engines vs `cand` at z = 7..12
  (1,944 points) — every z-family the engine can reach quickly agrees.
- **C11 v-space shell sweep (box-boundary stress)**: 33,710 seed-sampled
  points on shells max|v| in [61, 120], i.e. beyond the box up to 2x:
  **zero new types**, confluence clean — the enumeration box is
  demonstrably type-complete at twice its size.
- **C12 ring sweep**: x in [1,300], R in [1,1000] exhaustively for BOTH
  2-variable machines (600,000 point-checks: membership + confluence):
  **zero new types** beyond the boxes.

Additional development certificates: the box was grown from |v| <= 45 to
|v| <= 60 with the realized z>=2 type set **identical** (10,750 in both) —
the witness-bound lemma's conclusion is stable under a 33% box enlargement.

Two consecutive runs produce a **byte-identical** `output/audit.json`
(no timestamps, sorted keys, fixed seed). Runtime ~5 s single process.

## Cross-check against the independently derived K1022 verifier

`cross_check_k1022.py` (pure Python, deterministic, no RNG) compares this
artifact against the sibling K1022 verifier fetched from
`../vertical-fiber-two-token-y1-parametric-proof-20261119/verify_y1_parametric_proof.py`.
It writes `output/cross_check_k1022.json` and exits non-zero on any
mismatch or on a missing sibling file. Results (all **0 mismatches**):

| check | grid | points |
|---|---|---|
| (a) closed forms agree | z = 6..80, x <= 60, R <= x+z+99 (K1022 cand == K1023 cand) | 780,750 |
| (b) closed forms agree, far z | z in {97,98,997,998,2999,3000}, x <= 30, R < x+z+30 | 253,860 |
| (c1) extension domain vs raw engines | z = 1..5, x <= 25, R <= x+z+30 (K1023 cand == K1022 H_canonical == K1022 H_ordered) | 5,875 |
| (c2) z = 0 base vs raw engines | x <= 25, R <= 2x+30 (K1023 cand0 == both raw engines) | 1,425 |
| (c3) z = 0 wide grid | x = 26..40, R <= 2x+10 (K1023 cand0 == K1022 H_canonical) | 1,155 |

Check (c1)/(c2)/(c3) are the load-bearing ones: K1022's published theorem
excludes z <= 5 and z = 0, but its **raw game engines** (two independent
lru-cache recursions over the option decomposition) still define ground
truth there, so they double-anchor the extension domain that only K1023
claims. Additionally, in development the sibling's own verifier was run in
full in this environment: V0..V7 all PASS (~50 s) and its audit.json was
regenerated byte-identically.

## Confluence notes (honest scope of the machine certificates)

- Type-determinedness (Lemma S) is verified by confluence pairs for every
  multi-point type inside the box, and by 900,000+ probe/ring/shell
  confluence checks outside it; Appendix B's threshold table is the
  hand-checkable core making it an equality proof rather than a sample.
- The witness-bound lemma (Lemma W) is proved by the Appendix A chain
  bound (|v| <= 45) with box margin 60; C11/C12/C7/C8/C9 are its machine
  certificates (no new types or confluence breaks at magnitudes up to
  2x-box / 9000 / 15000).
- The induction itself (Lemma Z -> z = 1 -> z >= 2) is ordinary strong
  induction; each induction step's content is exactly the per-type
  identity check that the verifier runs for every realized type.

## Corollary

The published census statement "z = 1..60 finite verification" and the
ten published slice theorems K0877, K0977, K0983, K0985, K1003, K1012,
K1016, K1017, K1018, K1020 (z = 6..15 at y = 1) are all instances of
Theorem P1; the census's z <= 60 bound is removed entirely. K1022 (z >= 6,
independent lane) is likewise an instance on its stated domain, and the
z = 1..5 slices plus the z = 0 base are covered by Theorem P1 + Lemma Z
only. The
height-only collapse identity `H(R; (x,1); z) = single_token(x+1, z, R)`
for `R <= z+1` (census P2, previously verified for z = 1..60) now reduces
to a comparison of two closed forms on a finite band per (z, x) — a
natural next target for the same machinery; it is NOT proved here.

## Artifacts

- `verify_p1_universal.py` — SHA-256
  `ca89da25b31dedf339d4277a1a8a3437b52c9a43befcc527241b18fc7f623370`
- `output/audit.json` — SHA-256
  `b244e9126e587f0d528b5221a6a04e68b6250f32bc06ab8bd1baac46efc87fa4`
  (byte-identical across runs)
- `cross_check_k1022.py` + `output/cross_check_k1022.json` — SHA-256 of the
  JSON: `d6e1ae9e1f9114669b0c7709f12a1a3570c8a9ba8c278434662d80743f479c1a`
  (byte-identical across runs; 5 checks, 1,043,065 points, 0 mismatches)
- Runtime: ~5 s per run (single process, pure Python); cross-check < 1 s.

## Non-claims

- No claim about y >= 2 (the census and slice lanes' y >= 2 items are
  untouched; the machinery generalizes naturally but is not run here).
- No claim about the standard two-dimensional board, fixed-width / q-point
  stabilization lengths, Grundy maximality or 11x11 (fast lane only).
- The height-only collapse P2 (exact band R <= z+1) is not proved here.
- `single_token` (K0832) is used as a black box; its own proof status is
  unchanged.

## Appendix A: witness-bound lemma (sketch)

Work in free coordinates (v0, v1, v3) = (x-z, R-x, R-x-z). The type
constraints read: v0, v1, v3 pinned in [-8,8] or rayed (<= -9 / >= 9)
via w0, w1, w3; the pair sums w2 = v0+v1, w4 = v3-v0, w5 = v0+v3 pinned
in [-8,8] or rayed; plus the three parities, the x = 1 bit, and the domain
z = v1-v3 >= 2, x = v0+v1-v3 >= 1, R = 2v1+v0-v3 >= 1.

Given a feasible type pattern, build a minimal witness as follows: start
every pinned form at its pin; every rayed form at its ray boundary ±9
(direction fixed by the pattern); this determines candidate coordinates.
If a coordinate is not determined by a direct pin (w0/w1/w3), it is
determined by at most one chain: direct ray boundary -> pair-sum pin (adds
<= 16) -> pair-difference pin (adds <= 8), i.e. |coordinate| <= 9 + 16 +
8 = 33; the domain constraints (z >= 2 and parities) move coordinates by
at most one more ray adjustment (<= 9): |coordinate| <= 42 in the worst
chain, with all intermediate constants integral, so a witness satisfying
the parities exists at |v| <= 45 (parity classes within an integer coset
differ by lattice vectors of norm <= 2 in v-space). Infeasible patterns
(chain contradictions, e.g. all-up rays with down pair-sums) have no
witness at any size and never occur as types. The 2-variable machines:
absolute pins <= 80 and relative pins <= 24 chain to coordinates
<= 80 + 24 + 24 + parity = 130 <= 140 <= 320 in the boxes.

The verifier's box (|v| <= 60, x <= 140, R <= 320) therefore contains a
witness of every realizable type; C11 (shells to 2x box), C12 (full ring
x <= 300, R <= 1000), and C7/C9 (magnitudes to 9000/15000) all confirm
zero types beyond the box.

## Appendix B: threshold table (Lemma S core)

All reads of `cand` (both parity blocks; k = w-family value, thresholds
after child shifts δ ∈ {−2,−1,0,+1}):

| form | reads (thresholds) | max |t+δ| |
|---|---|---|
| w0 = x−z | rows x = z−1, z, z+1, z+2, >= z+3, <= z−2, <= z−3: k ∈ {−3,−2,−1,0,1,2,3}, <= −3, >= 3 | 4 |
| w1 = R−x | R <= x, x+1, x+2: k ∈ {0,1,2} | 4 |
| w2 = R−z | R <= z−1, z+1, z+2; R = z+2, z+3; R >= z+3, z+4: k ∈ {−1,1,2,3}, >= 4 | 5 |
| w3 = R−x−z | R <= S−1, S, S+1 ⟺ k <= 0, 1, k >= 2 (S = x+z+1) | 4 |
| w5 = R−2z | R <= 2z+3 ⟺ k <= 3 | 5 |

`single_token` (as B-child, z' = z+1): w0 ∈ {1, >= 2, <= 0} (z' = x / z'
interior / z' above); w2 = R−z: R' <= q_odd(z') ⟺ k ∈ {1,2}; w1 = R−x:
R' <= q_odd(x) ⟺ k ∈ {0,1}, R' <= x−1 ⟺ k <= −2; w3: R' < x+z+1 ⟺ k
< 2; w4 = R−2x: R' <= 2x−1 ⟺ k <= 0. Max threshold 3 (before shift).

`cand0` (z=1 C-child and z=0 A/B-children): x ∈ {1,2, >= 3} exact;
R ∈ {1,2,3,4, >= 5} exact (absolute windows cover to 80); R−x ∈ [−1,2]
thresholds; R−1 ∈ {1,3} via absolute R ∈ {2,4}.

Child shifts: A-child (z, x−1, R−1): w0−1, w1, w2−1, w3−2, w4+1, w5−1;
B-child: forms of single_token at (x, z+1, R−1): w0−1, w1 at R−1
(= w1−1 on rows reading R vs x), w2 at R−1 (= w2−1), w3 (=w3−1),
w4 (=w4−1); C-child (z−1, x, R−1): w0+1, w1−1, w2, w3, w4, w5+2 on the
z-even/odd rows of cand(z−1, ·) — the +2 shift applies to w5 only,
whose threshold 3+2 = 5 <= 6 stays inside the exact-shift margin. The
clip windows [−8,8] (exact) with rays ±9: a child of a +ray sits at
value >= 7, a child of a −ray at <= −7; every comparison threshold
|t| <= 6 is therefore decided on both sides, and exact-window children
have known exact values. This is the complete content of Lemma S.
