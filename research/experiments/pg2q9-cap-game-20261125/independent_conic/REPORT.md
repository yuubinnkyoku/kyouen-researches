# Independent verification — PG(2,9) conic layer (K1321)

Directory: `research/experiments/pg2q9-cap-game-20261125/independent_conic/`
Date: 2026-11-25.  Python 3.12, **standard library only** (no numpy, no C,
no network).  Nothing outside this directory was modified; nothing was
committed.

Board: `../output/board_pg2q9.txt` (read only).

## Verdict

| Task | Verdict | Summary |
|:--|:--|:--|
| 1. Board is PG(2,9); coordinate map | **PASS** (with a notation caveat, §1) | 91/91 rows are lines and they are *all* the 91 lines, but only under the digit-pair field convention; the literal reading fails 72/91 rows. |
| 2. `C` is a nondegenerate conic, unique through `{0,1,10,20,31}`; conics = one PGL(3,9) orbit, stabiliser order 720 | **PASS** | `C` = zero set of `xy + 7xz + 7yz` (det 6); 58,968 = 9⁵−9² conics; \|Stab(C)\| = 720; orbit 58,968 = all conics. |
| 3. PGL(2,9) orbits on k-subsets of 10 points, k = 3..9 | **PASS** | orbit-size multisets 120 / {180,30} / {180,72} / {180,30} / 120 / 45 / 10 exactly as claimed. |
| 4. Grundy values of one representative per orbit (full upset DP) | **PASS** | G = 1, 0,0, 1,1, 0,0, 1, 0, 1 for k = 3..9 — every value as claimed; upset sizes 31681 / 1868,1868 / 132,128 / 22,16 / 8 / 4 / 2. |
| 5. Incidence / distinct counts, k = 3..9 | **PASS** | 110,565 3-caps (64 conics each), 1,769,040 4-caps (7 each), 14,859,936 5-caps (1 each), 6/7/8/9-caps 12,383,280 / 7,076,160 / 2,653,560 / 589,680; all 589,680 9-caps are conic. |

One **discrepancy in the parent artifact** (representative labels, not the
claimed numbers) and one **wording caveat** in K1321 are reported in
§6.  The K1321 claims themselves were reproduced without exception.

## Reproduce

```sh
cd research/experiments/pg2q9-cap-game-20261125/independent_conic
python run_all.py            # ~40 s from scratch; writes logs/ and results_*.json
```

Individual steps (each writes its own `results_*.json`):

```sh
python selfcheck_linear.py   # field axioms, det/inverse, projectivity round trip (~2 s)
python task1_board.py        # board axioms + coordinate map                (~1 s)
python task2_conic.py        # conic C, uniqueness, all 58,968 conics       (~12 s)
python task3_orbits.py       # PGL(2,9) orbit structure                    (~12 s)
python task4_grundy.py       # full upset Grundy DP                        (~4 s)
python task5_counts.py       # cap / incidence counts                      (~10 s)
python check_parent_reps.py  # informational: parent artifact labels       (~2 s)
```

Files: `gf9.py` (GF(9) = GF(3)[i]/(i²+1), point/line model, matrices),
`pg9.py` (board labels, caps as 91-bit masks, quadratic forms, projectivity
machinery), `conic.py` (conic enumeration, stabiliser, parameterisation),
`selfcheck_linear.py`, `task1..task5`, `check_parent_reps.py`, `run_all.py`.
Derived caches `cache_conics.txt` / `cache_stab_C.txt` are regenerated
automatically.

---

## 1. Board and coordinate map — PASS (notation caveat)

**Board axioms (pure incidence).** `91 91` header, 91 rows of 10 distinct
points in 0..90; rows pairwise distinct; every point on exactly 10 rows;
the 4095 point pairs lie on a unique row; the 4095 row pairs meet in exactly
one point (`results_task1.json`, `abstract_incidence`).

**Field.** `gf9.py` tables satisfy all field axioms (associativity,
distributivity, identities, inverses, characteristic 3), `i² = −1`, `t²+1`
irreducible over GF(3), nonzero elements cyclic of order 8.

**Coordinate map.** The claim's recipe
`0 → (0:0:1)`, `1+j → (0:1:E[j])`, `10+9p+j → (1:E[p]:E[j])`,
`E[k] = 3(k//3)+(k%3)` was tested with every consistent reading of the
integer labels:

| reading of index k | rows that are lines | distinct lines |
|:--|--:|--:|
| k is the element `(k%3) + (k//3)i` (label `a+3b = k`) | **19/91** | 19 |
| k is the element with digit pair `(a,b) = (k//3, k%3)` | **91/91** | 91 |

Under the second reading the 91 rows are exactly the 91 lines of the
independently constructed PG(2,9), i.e. the map is a collineation and the
board *is* PG(2,9) with these coordinates.  (The Frobenius variants of both
readings behave the same way; Aut GF(9) has order 2.)

**Caveat.** In the working convention the field element `1 = (1,0)` is the
**index/label 3**, and `i = (0,1)` is index 1; `E` is the identity on the
labels, and the content of the convention is that integer `k` denotes the
element with digits `(k//3, k%3)`.  Using index 1 as "1" — the literal
reading — gives a non-collineation (72 of 91 rows are not lines, first
failure row 19, e.g. row `{2,10,25,31,38,53,59,66,81,87}`).  This is exactly
the trap warned about ("the constant 1 must be the field element (1,0)").
Recorded as a **notation clarification, not a mathematical error**.

## 2. `C` is a nondegenerate conic, unique through the 5-cap — PASS

`C = {0,1,10,20,31,45,51,62,75,88}`: 10 distinct points, a cap (45 distinct
secant lines).

* Unique quadratic form through `{0,1,10,20,31}`: the 5×6 system has rank 5,
  so the solution space is 1-dimensional.  Canonical form (basis
  `x²,y²,z²,xy,xz,yz`)
  `Q = xy + 7xz + 7yz`, coefficients `(0,0,0,1,7,7)`, `7 = 1+2i`.
  `det M = 6 ≠ 0` (nondegenerate), and the zero set is **exactly** `C`
  (10 points).  No other conic contains the 5-cap.
* All forms: 66,430 = (9⁶−1)/8 classes; 7,462 degenerate; **58,968 = 9⁵−9²
  nondegenerate conics**; every one has exactly 10 points; the 58,968 point
  sets are distinct; `C` is one of them.
* \|PGL(3,9)\| = (9³−1)(9³−9)(9³−9²)/8 = **42,456,960** = number of ordered
  frames (91·90·81·64), so PGL(3,9) acts regularly on ordered frames.
* Stabiliser of `C`: exhaustive frame enumeration gives **720**
  projectivities, faithful on `C`.  Orbit size 42,456,960/720 = **58,968** =
  number of conics ⇒ the conics are a **single PGL(3,9) orbit**, and the
  stabiliser is the claimed PGL(2,9) (see §3).
* Explicit projectivities `C → C'` were constructed for four further conics.

## 3. PGL(2,9) orbits on k-subsets — PASS

* PGL(2,9) from 2×2 matrices over GF(9) (5760 matrices / 8 scalars = **720**
  projectivities of PG(1,9)); it is **sharply 3-transitive** (720 images of an
  ordered triple = 10·9·8) and coincides with the explicit Möbius 3×3 action
  on the standard conic.
* The stabiliser of `C` (720 projectivities of the plane) induces exactly this
  PGL(2,9) permutation group on the 10 points of `C` under the explicit conic
  parameterisation `T` (the two sets of 720 permutations are equal, not only
  isomorphic), so "PGL(2,9) orbits on k-subsets of C" is unambiguous.
* Orbit sizes per conic (computed twice — from the abstract action on PG(1,9)
  and from the stabiliser on `C`; the two partitions coincide):

| k | orbit sizes | total | claimed |
|--:|:--|--:|:--|
| 3 | 120 | 120 | 120 |
| 4 | 180, 30 | 210 | 30, 180 |
| 5 | 180, 72 | 252 | 180, 72 |
| 6 | 180, 30 | 210 | 180, 30 |
| 7 | 120 | 120 | 120 |
| 8 | 45 | 45 | 45 |
| 9 | 10 | 10 | 10 |

* Extra checks: \|orbit\|·\|stabiliser\| = 720 for every orbit (stabilisers
  6,4,24,4,10,4,24,6,16,72); complement symmetry k ↔ 10−k maps orbits to
  orbits; for k = 4 the 30-orbit is **exactly the harmonic 4-subsets**
  (cross-ratio class −1), computed independently from the cross-ratio
  (30 harmonic vs 180 generic).
* Representatives found (board labels):

| k | orbit | representative |
|--:|--:|:--|
| 3 | 120 | {0,1,10} |
| 4 | 180 / 30 | {0,1,10,20} / {0,1,10,45} |
| 5 | 180 / 72 | {0,1,10,20,31} / {0,1,10,20,51} |
| 6 | 180 / 30 | {0,1,10,20,31,51} / {0,1,10,20,31,45} |
| 7 | 120 | {0,1,10,20,31,45,51} |
| 8 | 45 | {0,1,10,20,31,45,51,62} |
| 9 | 10 | {0,1,10,20,31,45,51,62,75} |

## 4. Grundy values — PASS

Game (as in the parent report): a position is a cap; a move adds one board
point keeping the cap; terminal = maximal cap; `G(S) = mex{G(S+p)}`.
For each representative the **complete upset** (all caps containing it) was
enumerated and the DP run bottom-up by size; a second, recursive
implementation reproduces every value.

| k | representative | orbit | upset positions | upset shape (size:count) | G | claimed |
|--:|:--|--:|--:|:--|--:|--:|
| 3 | {0,1,10} | 120 | 31,681 | 3:1, 4:64, 5:1344, 6:9408, 7:16320, 8:4032, 9:448, 10:64 | **1** | 1 |
| 4 | {0,1,10,20} | 180 | 1,868 | 4:1, 5:42, 6:441, 7:1020, 8:315, 9:42, 10:7 | **0** | 0 |
| 4 | {0,1,10,45} | 30 | 1,868 | same | **0** | 0 |
| 5 | {0,1,10,20,31} | 180 | 132 | 5:1, 6:21, 7:74, 8:30, 9:5, 10:1 | **1** | 1 |
| 5 | {0,1,10,20,51} | 72 | 128 | 5:1, 6:21, 7:70, 8:30, 9:5, 10:1 | **1** | 1 |
| 6 | {0,1,10,20,31,51} | 180 | 22 | 6:1, 7:8, 8:8, 9:4, 10:1 | **0** | 0 |
| 6 | {0,1,10,20,31,45} | 30 | 16 | 6:1, 7:4, 8:6, 9:4, 10:1 | **0** | 0 |
| 7 | {0,1,10,20,31,45,51} | 120 | 8 | 7:1, 8:3, 9:3, 10:1 | **1** | 1 |
| 8 | {0,1,10,20,31,45,51,62} | 45 | 4 | 8:1, 9:2, 10:1 | **0** | 0 |
| 9 | {0,1,10,20,31,45,51,62,75} | 10 | 2 | 9:1, 10:1 | **1** | 1 |

All ten values agree with the claim (and with the parity pattern 1,0,1,0,1,
0,1 in k).  The upset sizes equal those in the parent artifact
(31,681 / 1,868 / 132 / 128 / 22 / 16 / 8 / 4 / 2), which is a further
cross-check of the game definition.  Grundy invariance on each orbit was
tested by pushing 20 representatives through random elements of the conic
stabiliser (all values unchanged).

## 5. Incidence and distinct counts — PASS

Computed without reference to the claimed numbers:

* **3-caps**: 110,565 (direct count of non-collinear triples;
  C(91,3) − 91·C(10,3)).  Every 3-cap has exactly **64** extensions
  (distribution {64: 110,565}), hence #4-caps = 110,565·64/4 = **1,769,040**.
  Nine sampled 3-caps each lie on exactly **64** conics.
* **4-caps**: every 4-cap has exactly **42** extensions (distribution
  {42: 7,076,160}), hence #5-caps = 7,076,160·42/20 = **14,859,936**.
  Ten sampled 4-caps each lie on exactly **7** conics.  For the 4-cap
  {0,1,10,20} the whole pencil was computed: 10 conics, 7 nondegenerate
  (3 degenerate), and the 7 nondegenerate ones cover **exactly the 42**
  allowed extension points — this *proves* that every 5-cap containing a
  4-cap (hence every 5-cap) lies on a conic.
* **5-caps**: 14,859,936 (above).  Each 5-cap lies on **at most one** conic
  (two distinct conics share ≤ 4 points), and conic-5-subset incidence is
  58,968·252 = 14,859,936 = #5-caps, so each 5-cap lies on **exactly one**
  conic.  Both 5-cap orbit representatives have system rank 5, a unique
  nondegenerate conic, zero set `C`, and 21 extensions.
* **k = 5 correspondence**: 58,968·180 = **10,614,240**,
  58,968·72 = **4,245,696**, sum 14,859,936 = #5-caps.  Since PGL(3,9) is
  transitive on conics with stabiliser acting as PGL(2,9) on `C`, the
  PGL(3,9)-orbit of a 5-cap `S ⊂ C` has 58,968·\|Stab(C)·S\| elements, so the
  conic-layer split *is* the PGL(3,9) 5-cap orbit split.  Direct check of the
  K1305 correspondence: {0,1,10,20,42} has a unique conic, which maps onto
  `C`, and its image {0,1,10,62,88} lies in the **72-class** ⇒ that 5-cap
  orbit has 58,968·72 = 4,245,696 elements (stabiliser 10), while
  {0,1,10,20,31} is in the 180-class ⇒ 10,614,240 (stabiliser 4).
* **k = 3, 4 incidences**: 58,968·120 = 7,076,160 = 110,565·64 and
  58,968·210 = 12,383,280 = 1,769,040·7 — the claimed incidence readings are
  correct.  Constancy of the per-cap conic counts follows from PGL(3,9)
  transitivity on non-collinear triples (any two are bases of the vector
  space — explicit projectivities constructed for 8 samples) and on 4-caps
  (frames; regular action, 42,456,960 ordered frames = \|PGL(3,9)\|; 9
  explicit projectivities constructed).
* **k ≥ 6**: 58,968·C(10,k) = **12,383,280 / 7,076,160 / 2,653,560 /
  589,680** for k = 6,7,8,9.  Because a k-cap with k ≥ 5 lies on at most one
  conic, these are exactly the numbers of *distinct k-caps lying on conics*.
* **9-caps**: exhaustive extension from {0,1,10,20} gives 42 9-caps
  containing it (all inside the 7 conics through the 4-cap), hence
  #9-caps = #4-caps·42/C(9,4) = 1,769,040·42/126 = **589,680** = 58,968·10 =
  number of conic 9-subsets; since conic 9-subsets are distinct 9-caps, the
  two sets are equal: **all 589,680 9-caps lie on conics**.
* **Cross-check of the census**: every 5-cap has 21 extensions (both 5-cap
  orbits), so #6-caps = 14,859,936·21/6 = **52,009,776**, exactly the parent
  census value — which confirms that the K1321 k = 6,7,8 numbers count only
  the caps that lie on conics (the total number of 6-caps is 4.2× larger).

## 6. Discrepancies

1. **Coordinate-map notation (Task 1).**  As literally written (`E` applied to
   integer labels, `1` = index 1) the map is not a collineation: 72 of 91
   board rows are not lines.  It *is* a collineation under the digit-pair
   convention `index k ↔ a+bi, (a,b) = (k//3, k%3)`, in which the field
   element `1 = (1,0)` is index/label 3.  K1321 does not state this
   convention.  **No claimed number changes**; recommend adding the explicit
   convention (index 1 = i) to K1321/artifacts.
2. **Parent artifact `output/conic_layer.json` — representative ↔ orbit-size
   labels are wrong** for three rows (the claimed *multisets* of orbit sizes
   and all Grundy values are unaffected):
   * k = 4: the entry labelled "30" uses {0,1,10,20}, which is in the
     **180-class** (generic, non-harmonic 4-set), and the entry labelled
     "180" uses {0,1,10,31}, which is also in the 180-class.  No
     representative of the 30-class is listed.  (Independent proof: the
     30-class is exactly the harmonic 4-subsets, cross-ratio −1; {0,1,10,45}
     is harmonic, {0,1,10,20} is not.)
   * k = 5: the entry labelled "72" uses {0,1,10,31,51}, which is in the
     180-class; the 72-class representative should be e.g. {0,1,10,20,51}.
   * k = 6: the two representatives are swapped — {0,1,10,20,31,45} is the
     **30-class**, {0,1,10,20,31,62} the **180-class**.  The artifact's own
     upset sizes contradict its labels (16 belongs to the 30-class, 22 to the
     180-class; upset size is a PGL-invariant).
   The parent's Grundy values are still correct because both/all classes in
   these rows have the same claimed value.
3. **K1321 wording for k ≥ 6.**  "Each k-cap lies on at most one conic, so
   the numbers above are distinct cap counts" is correct only for *k-caps
   that lie on a conic*.  For k = 6,7,8 not every k-cap is conic (6-caps:
   52,009,776 in total vs 12,383,280 on conics; 8-caps: 7,960,680 total vs
   2,653,560 on conics — parent census, 6-cap total independently
   reconfirmed here).  Only for k = 9 do the two notions coincide, as the
   note says.  Suggest rewording to "number of k-caps contained in a conic".
4. **Minor naming.**  For k = 4 the artifact calls 1,769,040 and 10,614,240
   "orbit_size", but PGL(3,9) is transitive on all 4-caps (all 1,769,040 of
   them); the two numbers are 58,968·30 and 58,968·180, i.e. the sizes of the
   harmonic / generic classes among (conic, 4-subset) incidences.

## 7. Notes and limitations

* The projectivity machinery was itself validated before use: 200/200 random
  determinants against a permutation expansion, 200/200 random inverses, and
  300/300 random projectivity round-trips (`4 points → matrix → same map`).
  An initial version reconstructed a projectivity from only three points
  (leaving a free diagonal); this was caught because the conic stabiliser came
  out as 24 instead of 720, and fixed (a projectivity is determined by four
  points).  All numbers in this report come from the corrected code
  (`selfcheck_linear.py`).
* Grundy values were computed for one representative per orbit (10
  positions); PGL-invariance on each orbit was spot-checked with 20 random
  stabiliser elements.  The claim is per orbit, so this covers it.
* Not independently recomputed: the census totals of 7-caps (51,554,880) and
  8-caps (7,960,680); only the conic-layer parts (7,076,160 and 2,653,560)
  were verified structurally, plus the 9-cap total (589,680) and the 6-cap
  total (52,009,776).
* The `results_summary.json` "all_pass" includes the informational
  `check_parent_reps.py` step, which is expected to report the §6.2
  mismatch; `tasks_all_pass` is `true`.
