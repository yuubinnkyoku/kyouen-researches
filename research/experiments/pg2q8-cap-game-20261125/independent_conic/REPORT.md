# Independent verification — K1323 conic layer, `pg2q8-cap-game-20261125`

**Role.** Independent verifier of the claim K1323. All code in this directory was written
from scratch for this task; nothing from the parent experiment (`scripts/`, `output/`,
`report.md`) was imported or copied. The only external inputs used are the board file
`../output/board_pg2q8.txt` and the parent `README.md` numbers, which are quoted only in
the supplementary census check.

**Environment.** Windows, Python 3.12.13, standard library only. No files outside this
directory were created or modified; nothing was committed.

**Verdict: PASS on all five tasks, no discrepancies with the claim.** Additionally, the
parent's published PG(2,8) cap census is reproduced exactly (supplementary check S1).

| Task | Subject | Verdict |
|---|---|---|
| 1 | board is PG(2,8); point ordering = sorted canonical vectors | **PASS** |
| 2 | `{10,16,29,47,48}` is a 5-cap; unique conic `C` (9 points) | **PASS** |
| 3 | PGL(2,8) order 504; conic parameterisation; k-subset orbits | **PASS** |
| 4 | Grundy values of the conic k-caps, k = 3..8 | **PASS** |
| 5 | parity-theorem consequence `Grundy = k mod 2` | **PASS** |
| S1 | (supplementary) global cap census / hyperoval count | **PASS** |

---

## Reproduction

```sh
cd research/experiments/pg2q8-cap-game-20261125/independent_conic
python run_all.py            # runs everything, writes logs/*.txt, prints PASS/FAIL
# or individually:
python task1_board.py
python task2_conic.py
python task3_pgl.py
python task4_grundy.py
python task5_parity.py
python supplement_census.py
```

Full run: **16.9 s** (task1 0.4 s, task2 3.8 s, task3 4.6 s, task4 0.9 s, task5 0.6 s,
supplement 5.8 s). Logs are in `logs/`.

### Conventions

* **GF(8) = GF(2)[x]/(x³+x+1)**, elements are the integers 0..7 whose binary digits are the
  polynomial coefficients (bit0 = 1, bit1 = x, bit2 = x²); so x = 2, x³ = x+1 = 3.
  All field axioms were brute-force checked, and x was checked to have order 7.
* **Points of PG(2,8)** = canonical non-zero vectors `(a,b,c)` (first non-zero entry = 1),
  ordered lexicographically as integer triples. This is exactly the ordering the board uses.
* **Quadratic forms in characteristic 2** are evaluated with every cross term **once**:
  `q(x,y,z) = q00·x² + q11·y² + q22·z² + q01·xy + q02·xz + q12·yz`. The associated polar
  form is `B(u,v) = q(u+v)+q(u)+q(v)`, an alternating form with matrix having zero diagonal
  and `q_ij` off-diagonal; its radical in dimension 3 is always 1-dimensional (the nucleus),
  which is the correct characteristic-2 replacement for "non-singular polar matrix".
* **s=2 cap game**: position = a cap (a point set meeting every line in ≤ 2 points); a move
  adds one point keeping the set a cap; normal play (no move ⇒ lose);
  `Grundy(S) = mex{ Grundy(S∪{p}) : S∪{p} a cap }`. Terminal positions are maximal caps.
* `C` denotes the 9-point conic through the 5-cap, `n` its nucleus (point 31 = `(1,2,6)`).

---

## Task 1 — the board is PG(2,8), with the sorted-canonical-vector ordering

**PASS**

Modelled PG(2,8) from GF(8) from scratch (73 canonical vectors; lines = 2-dimensional
subspaces) and compared it with the board line by line.

| check | result |
|---|---|
| header | `73 73` |
| lines / line size | 73 lines, every line has 9 distinct points in range |
| lines distinct | yes |
| pairs covered exactly once | 2628 = C(73,2) pairs, each on exactly one line |
| point degrees | all 9 |
| model lines | 73 |
| model line set == board line set | **yes** |
| board line order == model lines sorted by their sorted point tuple | **yes** |
| each board point index == the i-th sorted canonical vector | **yes** |
| model spot check | 0=(0,0,1), 1=(0,1,0), 9=(1,0,0), 10=(1,0,1), 16=(1,0,7), 29=(1,2,4), 47=(1,4,6), 48=(1,4,7), 72=(1,7,7) |

So the board is PG(2,8) and the ordering is exactly the sorted-canonical-vector model
(the board's line order is the lexicographic order of the lines' sorted point tuples).

## Task 2 — the 5-cap and the unique conic through it

**PASS**

`S = {10,16,29,47,48} = {(1,0,1), (1,0,7), (1,2,4), (1,4,6), (1,4,7)}`; no 3 of the 10
triples are collinear, so it is a 5-cap.

Linear system on `(q00,q11,q22,q01,q02,q12)` (one row per point, cross terms once):
**rank 5 of 6, nullity 1** ⇒ the conic through the 5-cap is unique up to scalar.

```
q = x^2 + 3y^2 + 4z^2 + 4xy + 5xz + 7yz        (coefficients (1,3,4,4,5,7))
```

Zero set — the conic `C` (9 points, and a cap, i.e. no 3 collinear):

| board idx | 2 | 3 | 10 | 16 | 18 | 21 | 29 | 47 | 48 |
|---|---|---|---|---|---|---|---|---|---|
| vector | (0,1,1) | (0,1,2) | (1,0,1) | (1,0,7) | (1,1,1) | (1,1,4) | (1,2,4) | (1,4,6) | (1,4,7) |

Uniqueness checks (all agree):

* brute force over **all** 8⁶ = 262144 quadratic forms: exactly **7** (the 8−1 scalar
  multiples) vanish on the 5 points, and they have **one** common zero set = `C`;
* census of all 8⁶−1 forms modulo scalars (37449 canonical forms):
  `|zero set|` distribution `{1: 2044, 9: 32777, 17: 2628}`; of the 9-point zero sets,
  **32704** are caps (conics) and **73** are lines (double lines `l²`);
* **32704 distinct conic point sets**, and each carries a **unique** quadratic form up to
  scalar (no collisions) — matching `q⁵−q² = 8⁵−8² = 32704`;
* exactly **1** conic contains the 5-cap.

Characteristic-2 structure: polar matrix `[[0,4,5],[4,0,7],[5,7,0]]`, radical
dimension 1, nucleus **point 31 = (1,2,6)** (not on `C`); all 9 tangents (lines `P–n`)
meet `C` only in `P`, and `C ∪ {31}` is a 10-cap. (A naive "det of the polar matrix ≠ 0"
test is *not* a valid non-degeneracy test in characteristic 2 — every alternating 3×3
matrix is singular; 9 zeros + cap + 1-dimensional radical is the right criterion.)

## Task 3 — PGL(2,8), conic parameterisation, k-subset orbits

**PASS**

* **PGL(2,8):** all 2×2 matrices over GF(8) with non-zero determinant, modulo scalars
  (canonical form: first non-zero entry = 1) ⇒ **504** matrices; closed under
  multiplication, identity, every element invertible; action on
  `PG(1,8) = {[s:1]} ∪ {[1:0]}` gives 504 distinct permutations and is a homomorphism
  (checked on all 504² pairs). Orbit sizes: |orbit of a point| = 9,
  |orbit of an ordered pair| = 72, |orbit of an ordered triple| = **504 = 9·8·7** ⇒
  sharply 3-transitive.
* **Parameterisation** (as suggested): `P0 = 2 = (0,1,1)`, `L` = line 1 = `{0,9,...,16}`
  (does not contain `P0`). `Q ↦ line(P0,Q)` is a bijection `L →` pencil at `P0`;
  8 of the 9 lines are secants, the 9th is the tangent (at `P0`, through the nucleus).
  Hence `Q ↦` second intersection is a bijection `L → C`. A projective coordinate on `L`
  (from a vector-space basis of `L`) identifies `L` with `PG(1,8)` projectively, so the
  induced action on `C` is the standard PGL(2,8) action. Parameter table
  (`t ∈ PG(1,8) → Q ∈ L → P ∈ C`):

  | t | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 |
  |---|---|---|---|---|---|---|---|---|---|
  | Q | 0 | 9 | 10 | 11 | 12 | 13 | 14 | 15 | 16 |
  | P | 3 | 18 | 10 | 47 | 48 | **2** (=P0, tangent) | 21 | 29 | 16 |

* **Induced permutations of C:** 504 distinct permutations, faithful and transitive; and
  **all 504 are realised by an actual projectivity of PG(2,8) mapping `C` onto `C`**
  (each permutation determines a unique 3×3 projectivity from the images of 4 points of
  `C`, which was checked to preserve `C`).
* **Orbits of k-subsets of C** (k = 3..8): **one orbit each**, of the claimed sizes:

  | k | 3 | 4 | 5 | 6 | 7 | 8 |
  |---|---|---|---|---|---|---|
  | #orbits | 1 | 1 | 1 | 1 | 1 | 1 |
  | orbit size | 84 | 126 | 126 | 84 | 36 | 9 |
  | C(9,k) | 84 | 126 | 126 | 84 | 36 | 9 |

* **Conic orbit (part of K1323):** the orbit of `C` under the subgroup generated by 6
  elementary transvections + 2 diagonal scalings + a coordinate swap (which generates
  `SL(3,8) = PGL(3,8)`, as `GF(8)* = (GF(8)*)³` for q = 8) has **32704** elements, all of
  them 9-point caps; since the total number of conics is 32704 (Task 2), `PGL(3,8)` is
  transitive on conics and `|PGL(3,8)|/32704 = 16 482 816/32704 =` **504** is the
  stabiliser order, matching the 504 projectivities fixing `C` built above.
  (Note: the 6 transvections *alone* generate only a proper subgroup — their orbit of `C`
  has 168 elements — the diagonal generators are needed; this is a property of the
  generating set, not of the claim.)

## Task 4 — independent Grundy values of the conic k-caps

**PASS**

One representative per k (the k smallest points of `C`; by Task 3 all k-subsets are one
orbit). The whole upset `{T : base ⊆ T, T a cap}` was enumerated by memoised DFS with
bitmask move generation; terminal positions were collected as the maximal extensions.

| k | base | Grundy | \|upset\| | upset profile (size:count) | maximal extension sizes | #maximal extensions |
|---|---|---|---|---|---|---|
| 3 | 2,3,10 | **1** | 8450 | 3:1, 4:49, 5:735, 6:3185, 7:2450, 8:1470, 9:490, 10:70 | **{6, 10}** | 6-caps: 735, hyperovals: 70 |
| 4 | +16 | **0** | 646 | 4:1, 5:30, 6:195, 7:200, 8:150, 9:60, 10:10 | **{6, 10}** | 45, 10 |
| 5 | +18 | **1** | 66 | 5:1, 6:13, 7:20, 8:20, 9:10, 10:2 | **{6, 10}** | 3, 2 |
| 6 | +21 | **0** | 16 | 6:1, 7:4, 8:6, 9:4, 10:1 | **{10}** | 1 |
| 7 | +29 | **1** | 8 | 7:1, 8:3, 9:3, 10:1 | **{10}** | 1 |
| 8 | +47 | **0** | 4 | 8:1, 9:2, 10:1 | **{10}** | 1 |

**Grundy = 1, 0, 1, 0, 1, 0 for k = 3,4,5,6,7,8** — exactly as claimed. Every maximal
extension has even size (6-caps and 10-caps only), as claimed.

Cross-checks:

* the bitmask move generator was compared with a naive `is_cap` generator on 300 sampled
  positions — 0 mismatches;
* an independent naive `frozenset` game-tree implementation (using `board.is_cap` for every
  candidate move) reproduces Grundy for k = 7 and k = 8 (the upsets are small there);
* 3 additional random representatives per k all give the same Grundy value, consistent with
  the single-orbit result of Task 3;
* within the whole 8450-position `k=3` upset the Grundy value depends only on the size:
  size 3→1, 4→0, 5→1, 6→0, 7→1, 8→0, 9→1, 10→0.

## Task 5 — parity-theorem consequence

**PASS, no mismatch**

With every maximal extension even (terminal sizes 6 and 10, both ≡ 0 mod 2), the parity
theorem predicts `Grundy = (p − |S|) mod 2 = (10 − k) mod 2 = k mod 2`:

| k | terminal sizes | all even | Grundy | k mod 2 | (10−k) mod 2 | verdict |
|---|---|---|---|---|---|---|
| 3 | {6,10} | yes | 1 | 1 | 1 | OK |
| 4 | {6,10} | yes | 0 | 0 | 0 | OK |
| 5 | {6,10} | yes | 1 | 1 | 1 | OK |
| 6 | {10} | yes | 0 | 0 | 0 | OK |
| 7 | {10} | yes | 1 | 1 | 1 | OK |
| 8 | {10} | yes | 0 | 0 | 0 | OK |

The theorem itself was also verified directly on **all 8450 positions** of the task-4
upset: every position has a single maximal-extension parity `p`, and
`Grundy(S) = (p − |S|) mod 2` holds for **all** of them (0 violations, 0 positions with
mixed parity).

---

## Supplementary check S1 — global PG(2,8) census (beyond the five tasks)

**PASS.** The task-4 upsets are exact counts of caps containing a fixed conic k-cap. For
k = 3,4,5, `PGL(3,8)` is transitive on k-caps, so
`n_j = (#j-caps containing the base)·n_k/C(j,k)` with `n_k` from brute force
(`n_3 = 56 064`, `n_4 = 686 784` by enumerating all C(73,4) = 1 088 430 4-subsets,
`n_5 = n_4·30/5 = 4 120 704`, extension count 30 verified on 300 random 4-caps).
Three independent estimates agree for every j:

| j | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 |
|---|---|---|---|---|---|---|---|---|
| n_j | 56 064 | 686 784 | 4 120 704 | 8 928 192 | 3 924 480 | 1 471 680 | 327 040 | 32 704 |

* maximal 6-caps = **2 060 352** (three estimates agree), hyperovals = **32 704**
  (three estimates agree, and independently: `conic + nucleus` gives exactly 32 704
  distinct 10-caps, nucleus never on its conic, each conic in exactly one hyperoval);
* total number of caps of all sizes
  `1 + 73 + 2 628 + Σ_{j=3..10} n_j = 19 550 350`, which is **exactly the parent README
  census** (19 550 350; maximal 6-caps 2 060 352; hyperovals 32 704).

---

## Discrepancies

**None.** Every quantitative statement in K1323 that was checked matched exactly.

Notes / clarifications (not discrepancies):

1. **The parent census total 19 550 350 includes the empty, 1- and 2-point caps.**
   Its decomposition is `1 + 73 + 2 628 + 19 547 648`; the five-task data cover only sizes
   3..10. This reconciles the README total with the size table above (a useful
   cross-check rather than a conflict).
2. **"Non-degenerate quadratic form" in characteristic 2.** The polar form is alternating,
   so in dimension 3 its matrix is always singular; the radical is 1-dimensional and is
   spanned by the nucleus (point 31 for `C`). Non-degeneracy of the conic was therefore
   verified by "9 zeros and no 3 collinear", plus radical dimension 1 and all 9 tangents
   through the nucleus. A test "det(polar) ≠ 0" would wrongly reject every conic in
   characteristic 2.
3. **Bases k = 6,7,8 cannot be used for the census normalisation**, because `PGL(3,8)` is
   not transitive on 6-caps (e.g. a 6-subset of a conic is not equivalent to "5 conic
   points + nucleus", which lies on no conic). Rescaling the k=6 upset by `n_6/C(j,6)`
   is off by a constant factor 13/10. This only affects the optional census supplement,
   not Tasks 1–5.
4. **Not all 9-caps are conics:** 490 nine-caps contain a fixed conic 3-cap, but only 49
   of them are conics (conics through a fixed triple: `84·32704/56064 = 49`); e.g.
   `{2,3,10,12,21,45,47,50,52}` is a non-conic 9-cap (cap, exactly one extension, a
   hyperoval). Hence `n_9 = 327 040` but only 32 704 nine-caps are conic zero sets — the
   claim's restriction to *conic* k-caps is essential, and nothing in the claim is affected.
5. **Grundy beyond the claim:** within the entire `k=3` upset (8450 positions) the Grundy
   value is exactly `|S| mod 2` for every cap, and every position has a uniform
   maximal-extension parity — the parity theorem applies globally to this part of the
   game, consistent with the parent's global claim.

## Files

| file | purpose |
|---|---|
| `pg8.py` | library: GF(8) arithmetic + axiom checks, canonical points, board parsing and verification, quadratic form / conic solving over GF(8), 3×3 linear algebra and projectivity construction |
| `task1_board.py` | Task 1 |
| `task2_conic.py` | Task 2 |
| `task3_pgl.py` | Task 3 (incl. conic orbit / stabiliser) |
| `task4_grundy.py` | Task 4 (writes `results_grundy.json`) |
| `task5_parity.py` | Task 5 |
| `supplement_census.py` | supplementary census / hyperoval check S1 |
| `run_all.py` | runs all of the above, writes `logs/` |
| `logs/*.txt` | captured output of the final run |
| `results_grundy.json` | machine-readable task-4 results |

No commit was made; nothing outside `independent_conic/` was modified
(`git status --porcelain -- research/experiments/pg2q8-cap-game-20261125` shows only
`?? research/experiments/pg2q8-cap-game-20261125/independent_conic/`).
