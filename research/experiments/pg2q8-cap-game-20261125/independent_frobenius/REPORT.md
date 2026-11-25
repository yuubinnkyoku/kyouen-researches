# Independent verification of K1329

**Claim under test (K1329).** Let
`A = {10,47,49,55,61,64}`, `B = {17,27,30,44,52,70}`, `C = {8,48,50,51,58,61}`
be representatives of the three PGL(3,8)-orbits of maximal 6-caps in PG(2,8)
(each orbit 686,784, total 2,060,352), and let φ be the Frobenius automorphism
`(x,y,z) -> (x²,y²,z²)`. Then
`φ(A) = {10,28,31,59,65,67}` is in the PGL orbit of `C`, and
`φ²(A) = {10,29,33,37,43,46}` is in the PGL orbit of `B`; since φ³ = id the
three classes are cyclically permuted `A -> C -> B -> A`, so
`PΓL(3,8) = PGL(3,8) ⋊ C₃` is transitive on all maximal 6-caps, with stabiliser
order 24 and `|PΓL| = 3·16,482,816 = 49,448,448`.

**Verdict: all tasks PASS. No discrepancy found.** The claim is confirmed, and
in fact the exhaustive part is confirmed unconditionally: an independent
enumeration of *all* caps of PG(2,8) shows that there are exactly 2,060,352
maximal 6-caps and that every one of them lies in one of the three computed
PGL orbits (so the three orbits are not merely pairwise distinct, they are all
of them).

| Task | Verdict |
|---|---|
| 1. A, B, C, φ(A), φ²(A) are maximal 6-caps; board convention / φ bijection | **PASS** |
| 2. φ(A), φ²(A) equal the claimed sets; φ³ = id | **PASS** |
| 3. PGL(3,8) from own generators: collineation group of order 16,482,816 | **PASS** |
| 4. φ(A) ∈ PGL·C, φ²(A) ∈ PGL·B; A, B, C in pairwise distinct PGL orbits | **PASS** |
| 5. Transitivity conclusion and arithmetic 3·16,482,816 = 49,448,448 = 2,060,352·24 | **PASS** |

Everything below was produced by code in this directory only (no commit, no
files outside `independent_frobenius/` were modified).

---

## 1. Environment, input, conventions

* Python 3.12.13 (standard library only), gcc 15.2.0 (MSYS2) for the census.
* Board: `../output/board_pg2q8.txt`, SHA-256
  `E3FDAD754BDF4D42DE7BBFA076768F18A6FC141D48F42435CCF7EABFC93F6ADB`.
  Header `73 73`, then 73 lines of 9 point indices. The rows are the 73 lines
  of PG(2,8) (the row *order* is "grouped by smallest point on the line", which
  is irrelevant to the claims).
* GF(8) = GF(2)[x]/(x³+x+1); element `a0 + a1·x + a2·x²` is the integer
  `a0 | a1<<1 | a2<<2`; 2 = x is primitive. The squaring (Frobenius) table is
  `0,1,4,5,6,7,2,3` for `0..7`.
* Point = canonical nonzero vector over GF(8) whose **first** nonzero coordinate
  is 1; **rank** = position in lexicographic order of these 73 vectors:
  rank 0 → `(0,0,1)`, ranks 1..8 → `(0,1,c)`, ranks 9..72 → `(1,a,c)`.
  This convention is independently confirmed: the 73 lines generated from it
  (`l(x,y,z) = 0` over all canonical dual vectors) are exactly the 73 board
  rows as point sets (`verify_core.py`, 73/73 match), and it reproduces the
  claimed φ images below.
* Matrix `M` acts on row vectors, `p -> p·M`, followed by canonicalisation.
* φ acts as entrywise squaring; it is well defined on canonical vectors because
  `1² = 1`, and is verified to be a bijection.
* Permutations are tuples `p[0..72]`; composition `a then b` is
  `tuple(b[x] for x in a)`.

## 2. Reproduce

```
cd research/experiments/pg2q8-cap-game-20261125/independent_frobenius

python verify_core.py            # tasks 1,2,3, arithmetic + phi/PGL          (~20 s)
python test_group_order.py       # 116 brute-force checks of the order code  (~10 s)
python orbit_bfs.py              # task 4, exhaustive PGL orbit BFS           (~44 s)
gcc -O2 -o maxcaps.exe maxcaps.c # extra exhaustive cap census
./maxcaps.exe ../output/board_pg2q8.txt .                                   (~2.3 s)
python verify_extra.py           # witness replay + phi on whole orbits      (~10 s)
python verify_summary.py         # consolidated PASS/FAIL + arithmetic
```

Outputs: `core_results.json`, `orbit_results.json`, `extra_results.json`,
`summary_results.json`, `census_output.txt`, `orbit_{A,B,C}.bin`, and the
`*_log.txt` transcripts.

## 3. Task 1 — the five sets, the board, φ

**Board reconstruction.** The 73 generated lines equal the board rows as sets
(73 distinct 9-point blocks); every point is on 9 lines; every pair of points
lies on a unique line; every pair of lines meets in a unique point
(`verify_core.py` all PASS). This fixes the rank convention above.

**Cap / maximality.** A 6-set is a cap iff it has no 3 collinear points; it is
maximal iff no point outside it can be added, i.e. iff the union of the lines
through its pairs together with the cap covers all 73 points. Direct check:

| set | points | cap | addable points |
|---|---|---|---|
| A | (10,47,49,55,61,64) | yes | none |
| B | (17,27,30,44,52,70) | yes | none |
| C | (8,48,50,51,58,61) | yes | none |
| φ(A) | (10,28,31,59,65,67) | yes | none |
| φ²(A) | (10,29,33,37,43,46) | yes | none |

**φ is well defined.** φ is a bijection of the 73 points, φ³ = id on all 73,
φ ≠ id and φ² ≠ id (order exactly 3); φ is a field automorphism
(`φ(x+y)=φ(x)+φ(y)`, `φ(xy)=φ(x)φ(y)`, fixed field GF(2)) and a collineation
(it maps every one of the 73 board lines to a board line and induces an order-3
permutation of the 73 lines).

## 4. Task 2 — the specific Frobenius images

Computed directly from the board rank convention:

* `φ(A)  = (10,28,31,59,65,67)`  — matches the claim exactly.
* `φ²(A) = (10,29,33,37,43,46)` — matches the claim exactly.
* `φ³ = id` on all 73 points (checked point by point).

## 5. Task 3 — PGL(3,8) from own generators

Eight generators of GL(3,8) (their projective images generate PGL(3,8)):

```
E01 = [[1,1,0],[0,1,0],[0,0,1]]     E02 = [[1,0,1],[0,1,0],[0,0,1]]
E10 = [[1,0,0],[1,1,0],[0,0,1]]     E12 = [[1,0,0],[0,1,1],[0,0,1]]
E20 = [[1,0,0],[0,1,0],[1,0,1]]     E21 = [[1,0,0],[0,1,0],[0,1,1]]
D1  = diag(2,1,1)                   D2  = diag(1,2,1)
```

(Conjugating the E_ij(1) by D1, D2 produces E_ij(α^k) for every nonzero field
element, so SL(3,8) is generated; D1 has determinant 2 = α, so GL(3,8) is
generated.)

Verified:

* every generator is invertible (det ≠ 0) and non-scalar;
* every generator permutes the 73 points and maps every board line to a board
  line — hence the generated group is a **collineation group**;
* **group order** computed by an exact orbit-stabiliser recursion with
  Schreier generators (the routine was separately validated on 116 small
  permutation groups against brute-force enumeration, `test_group_order.py`,
  0 failures). Stabiliser chain orbit sizes:

  `73 · 72 · 7 · 64 · 7 = 16,482,816`

  (Schreier-generator counts at the five levels: 234, 3093, 447, 6, 0);
* `|GL(3,8)| = (8³−1)(8³−8)(8³−8²) = 511·504·448 = 115,379,712`, and
  `115,379,712 / 7 = 16,482,816`; since the generated group is a subgroup of
  PGL(3,8) of the same order `|GL|/7`, it **is** PGL(3,8);
* the action is transitive on the 73 points and on the 73 lines; the point
  stabiliser has order `16,482,816/73 = 225,792` (also computed directly);
* the 7 scalar matrices act trivially on points (the GL action factors through
  PGL).

## 6. Task 4 — PGL orbit membership

Exhaustive BFS on 6-caps under the 8 generators above (a group of order
16,482,816 = PGL(3,8), so these are exactly the PGL orbits):

| orbit | size | φ(A) ∈? | φ²(A) ∈? |
|---|---|---|---|
| PGL·A | 686,784 | no | no |
| PGL·B | 686,784 | no | **yes** |
| PGL·C | 686,784 | **yes** | no |

Membership matrix of the probe sets:

|  | A | B | C | φ(A) | φ²(A) |
|---|---|---|---|---|---|
| PGL·A | yes | no | no | no | no |
| PGL·B | no | yes | no | no | yes |
| PGL·C | no | no | yes | yes | no |

Hence **A, B, C are in pairwise distinct PGL orbits**, `φ(A) ∈ PGL·C`, and
`φ²(A) ∈ PGL·B`.

Explicit witnesses were recovered from the BFS tree (generator indices
`0..5 = E01,E02,E10,E12,E20,E21`, `6,7 = D1,D2`):

* `C -> φ(A)`: `[D1,D1,E01,E10,E12,D1,D1,D1]` (8 letters), image
  `(10,28,31,59,65,67)`;
* `B -> φ²(A)`: `[E20,E01,E02,D1,D1,E02,D1,D2,E21,E12]` (10 letters), image
  `(10,29,33,37,43,46)`.

Both composed permutations were replayed independently, verified to be
collineations, and to map the stated cap to the stated cap.

Moreover, applying φ to **every** cap of each saved orbit gives
`φ(PGL·A) = PGL·C`, `φ(PGL·C) = PGL·B`, `φ(PGL·B) = PGL·A`
(0 exceptional images out of 686,784 in each case), which is exactly the
claimed cyclic permutation `A -> C -> B -> A`.

## 7. Task 5 — transitivity and arithmetic

**PΓL.** φ normalises the generated PGL group: for each of the 8 generators g,
`φ⁻¹gφ` lies in PGL (membership proved rigorously by comparing exact group
orders: `|<PGL, φ⁻¹gφ>| = |PGL|`, so the conjugate is in PGL). φ ∉ PGL, φ has
order 3, and

`|<PGL, φ>| = 49,448,448 = 3 · 16,482,816`,

so `PΓL(3,8) = PGL(3,8) ⋊ C₃` (the permutation action on the 73 points is
faithful).

**Transitivity, unconditionally.** Since φ cycles the three PGL orbits and the
extra census (below) shows that the union of the three orbits is *all* maximal
6-caps:

`PΓL·A = PGL·A ∪ PGL·C ∪ PGL·B = all 2,060,352 maximal 6-caps`,

a single PΓL orbit. Stabiliser order `49,448,448 / 2,060,352 = 24` (PGL
stabiliser likewise `16,482,816 / 686,784 = 24`).

**Arithmetic (all exact):**

* `3 · 16,482,816 = 49,448,448` ✔
* `2,060,352 · 24 = 49,448,448` ✔
* `49,448,448 / 24 = 2,060,352` ✔
* `3 · 686,784 = 2,060,352` ✔
* `16,482,816 / 686,784 = 24` ✔
* `49,448,448 / 2,060,352 = 24` ✔

## 8. Extra independent check — exhaustive census of all caps

Written independently in C (`maxcaps.c`): DFS over all increasing sequences of
points that are caps (each cap exactly once); a cap S is maximal iff
`S ∪ F(S)` is all 73 points, where `F(S)` is the union of the lines through
pairs of points of S. This also loads the three saved PGL orbit files into a
hash set and tests every maximal 6-cap for membership.

```
cap census by size:
  size  0 :            1 caps,          0 maximal
  size  1 :           73 caps,          0 maximal
  size  2 :         2628 caps,          0 maximal
  size  3 :        56064 caps,          0 maximal
  size  4 :       686784 caps,          0 maximal
  size  5 :      4120704 caps,          0 maximal
  size  6 :      8928192 caps,    2060352 maximal
  size  7 :      3924480 caps,          0 maximal
  size  8 :      1471680 caps,          0 maximal
  size  9 :       327040 caps,          0 maximal
  size 10 :        32704 caps,        32704 maximal
  total caps: 19550350
maximal 6-caps: 2060352
  in the union of the three PGL orbits: 2060352
  NOT in the union:                     0
CENSUS OK
```

So the total number of maximal 6-caps is exactly 2,060,352 and the three
computed PGL orbits cover all of them — the transitivity claim does not depend
on taking the three representatives as a premise. As a check of the enumerator,
the total cap count 19,550,350 and the maximal 10-cap count 32,704 also match
the figures reported in the experiment's README (from its own, separately
written C census).

## 9. Discrepancies / notes

* **No discrepancies.** Every numeric and set-theoretic assertion of K1329 was
  reproduced exactly.
* Note (not a discrepancy): in `board_pg2q8.txt` the 73 rows are ordered by
  smallest point on the line, not by canonical dual-vector rank. This does not
  affect anything; the row *sets* are exactly the 73 lines generated from the
  stated rank convention.
* The group-order recursion is exact, not randomised; it was validated against
  brute-force group enumeration on 116 small test groups.
* The census and the Python orbit computation share only the board geometry
  (line incidence); the census itself is independent C code and does not use
  the PGL orbit computation except to test membership against the saved orbit
  files.

## 10. Files

| file | role |
|---|---|
| `pg2q8.py` | GF(8), rank convention, lines, caps, matrices, φ, exact permutation-group order |
| `verify_core.py` | tasks 1–3 + arithmetic + φ/PGL normalisation (`core_results.json`) |
| `test_group_order.py` | 116 brute-force validation tests of the order routine |
| `orbit_bfs.py` | task 4: exhaustive PGL orbit BFS + witness recovery (`orbit_results.json`, `orbit_*.bin`) |
| `maxcaps.c` / `maxcaps.exe` | independent exhaustive census of all caps (`census_output.txt`) |
| `verify_extra.py` | witness replay and φ on all 686,784 caps of each orbit (`extra_results.json`) |
| `verify_summary.py` | consolidated task-level verdicts (`summary_results.json`) |
| `*_log.txt` | captured command output |
