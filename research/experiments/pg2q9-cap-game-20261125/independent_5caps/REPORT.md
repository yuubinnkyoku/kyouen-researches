# Independent verification — 5-caps of PG(2,9): orbits and Grundy values

Directory: `research/experiments/pg2q9-cap-game-20261125/independent_5caps/`
Board: `research/experiments/pg2q9-cap-game-20261125/output/board_pg2q9.txt`
Standard library only; nothing outside this directory was modified; nothing committed.

## Claim under test

> The 5-caps of PG(2,9) (14,859,936 of them) split into exactly **3** PGL(3,9) orbits of
> sizes **8,491,392 / 4,245,696 / 2,122,848** (stabilizers **5 / 10 / 20**), and all 5-caps
> have Grundy value 1. Representatives `{0,1,10,20,31}`, `{0,1,10,20,42}`, `{0,1,10,20,41}`
> (one per orbit). Method: every 5-cap contains a 4-cap; all 4-caps form a single orbit
> (1,769,040); Stab{0,1,10,20} ≅ S4 (24 projectivities); S4-orbits on the 42 five-caps
> through the frame have sizes 24, 12, 6; by orbit–stabilizer a PGL orbit has size
> 1,769,040·s/5.

## Verdict

| Task | Verdict | Short reason |
|---|---|---|
| 1. board = PG(2,9), coordinate map consistent | **PASS** | 91 points / 91 lines rebuilt from the map equal the board's line set exactly |
| 2. frame 4-cap, 42 extensions, 3 reps are 5-caps, counts | **PASS** | 42 extensions; 1,769,040 4-caps (exhaustive); 14,859,936 5-caps |
| 3. 24 frame-fixing projectivities, S4, orbits on 42, PGL orbit sizes | **FAIL** | S4 part all pass, but the resulting orbit sizes / stabilizers are **wrong** (see D1–D3) |
| 4. Grundy value 1 for the three representatives | **PASS** | g = 1 for all three; upper sets 132 / 128 / 132 |
| 5. pairwise inequivalence + consistency of "all 5-caps have g = 1" | **FAIL** (claim) | `{0,1,10,20,31}` and `{0,1,10,20,41}` are **equivalent**; there are only **2** orbits. The Grundy statement itself is nevertheless true. |

**Main discrepancy: the 5-caps form 2 PGL orbits, not 3 — of sizes 10,614,240 (stabilizer 4) and 4,245,696 (stabilizer 10).**

## Commands

```
cd research/experiments/pg2q9-cap-game-20261125/independent_5caps
python run_all.py            # runs t1..t7, writes logs/ and prints the summary
python t1_board.py           # Task 1
python t2_caps.py            # Task 2   (~14 s: exhaustive 4-cap enumeration)
python t3_frame_s4.py        # Task 3
python t4_grundy.py          # Task 4
python t5_equiv.py           # Task 5   (decisive)
python t6_conic.py           # Task 5, independent conic cross-check
python t7_indep_field.py     # full re-implementation of GF(9) as pairs (a,b)
```

Files: `pg.py` (GF(9) tables, PG(2,9) rebuild, 3x3 matrices, projectivities),
`game.py` (upper sets, Grundy DP + certificate), `t1..t7` (task scripts), `run_all.py`,
`logs/*.log` (full output of every script). Whole suite runs in ≈ 21 s and is deterministic.

---

## Task 1 — the board is PG(2,9); the coordinate map is consistent — PASS

Combinatorics read directly off the board file (no coordinates used):

| property | value |
|---|---|
| lines / points per line | 91 / 10 (91 distinct lines) |
| pairs of points | 4095, each on exactly **one** line |
| pairs of lines | each meets in exactly **one** point |
| lines per point | 10 |

So the board is a projective plane of order 9. Rebuilding from the claimed map

```
index 0 -> (0:0:1);  1+j -> (0:1:E[j]);  10+9p+j -> (1:E[p]:E[j]),  E[k] = 3(k//3)+(k%3) = k
```

in GF(9) = GF(3)[i]/(i²+1), element `a+bi` encoded as `3a+b`, gives 91 distinct points and
91 distinct lines, and the computed line set is **equal to the board's line set**
(`t1_board.py`, `t7_indep_field.py`). Both an all-`(x,y,z)` brute force (91 = all nonzero
vectors up to scalar) and the explicit index formula agree.

**Notational discrepancy (minor, D6).** `E` is the identity map, and the literal `1` in
`(1:E[p]:E[j])` must be read as the *field* element 1, i.e. the encoded integer **3**, not
the encoded integer 1 (= the field element i). The two readings give different point
indexings: the "field 1" reading reproduces all 91 board lines, the "encoded 1" reading
does **not** (checked in `t1_board.py`). With the correct reading the frame is

```
0 -> (0:0:1)   1 -> (0:1:0)   10 -> (1:0:0)   20 -> (1:i:i)   31 -> (1:2i:1)   41 -> (1:1:1+i)   42 -> (1:1:1+2i)
```

## Task 2 — frame, 42 extensions, representatives, global counts — PASS

* `{0,1,10,20}` = `{(0:0:1),(0:1:0),(1:0:0),(1:1:1)}` is a 4-cap: all four triples are
  non-collinear, and every 3 of the four points span a basis (a proper frame).
* Its 6 secant lines are distinct and cover 49 points, so exactly **42** points `p` make
  `{0,1,10,20,p}` a 5-cap:
  `31 32 33 34 35 36 39 41 42 43 44 45 48 49 51 52 53 54 57 58 59 61 62 63 66 67 68 69 71 72 75 76 77 78 79 81 84 85 86 87 88 89`.
  All 42 verified with an independent `is_cap` check.
* The three representatives `{0,1,10,20,31}`, `{0,1,10,20,42}`, `{0,1,10,20,41}` are
  5-caps (each has 21 extension points, i.e. 21 six-caps through it).
* Counts, obtained **without** group theory:
  * collinear triples = 91·C(10,3) = 10,920, so 3-caps = C(91,3) − 10,920 = 110,565;
  * every 3-cap covers exactly 27 points and has exactly 64 extensions (exhaustive over all
    110,565), hence #4-caps = 110,565·64/4 = **1,769,040**;
  * exhaustive enumeration of all 4-subsets: exactly 1,769,040 4-caps, and the distribution
    of extension counts is `{42: 1769040}` — **every** 4-cap has exactly 42 extensions;
  * #5-caps = 1,769,040·42/5 = **14,859,936** ✔ (claim's total is correct).
* "All 4-caps form a single orbit": the pointwise stabilizer of an ordered frame is trivial
  (a projectivity fixing 3 non-collinear points is the identity), so every PGL orbit on
  ordered frames has size |PGL| = 42,456,960; and 24·#4-caps = 24·1,769,040 = 42,456,960.
  Hence the action is transitive (indeed free) on ordered frames.

## Task 3 — 24 frame-fixing projectivities, S4, orbits on the 42 — computations PASS, inference FAIL

**Construction (from scratch).** A projectivity with `M(F) = F` sends `F[i] ↦ c_i·F[σ(i)]`.
`F[0],F[1],F[2]` are a basis, so `M` is determined by the first three images; brute force
over all 24·8³ = 12,288 `(σ, c0,c1,c2)` and keep those for which the image of the fourth
frame point is again a frame point.

Verified:

* exactly **24** distinct projectivities, all invertible; the same set as the independent
  frame formula `λ_i = d_i/c_i` (`M = B·diag(λ)·A⁻¹`);
* closed under multiplication (24×24 products), contains the identity, closed under
  inverses → a **group of order 24**;
* the action on the 4 frame points is faithful and hits all 24 permutations → the group is
  **S4**;
* each of the 24 permutes the 42 extension points;
* **S4 orbits on the 42 five-caps: sizes 24, 12, 6** (24+12+6 = 42) ✔
  * size 24: `31 32 33 34 35 36 39 43 45 48 53 54 57 61 62 66 67 69 75 77 78 84 85 86`
  * size 12: `42 44 51 52 58 59 68 72 76 81 88 89`
  * size 6: `41 49 63 71 79 87`
  * the three claim representatives fall in orbits 24, 12, 6 respectively ✔ (so the claim's
    reading of the S4 orbit sizes is right).

**But the step "S4-orbit of size s ⇒ PGL orbit of size 1,769,040·s/5" is invalid: the
S4-orbits are *fused* by projectivities that do not preserve the frame.** Direct complete
test (all 120 images of the ordered frame, hence every projectivity out of the frame):

```
F+{31} -> F+{42}: inequivalent
F+{31} -> F+{41}: EQUIVALENT, witness M = (8,0,4,5,0,4,5,5,2), M(F) = {0,10,20,41} ≠ F
F+{42} -> F+{41}: inequivalent
```

So the 24-orbit and the 6-orbit lie in one PGL orbit (c = 24+6 = 30 of the 42 caps), and
the 12-orbit is alone (c = 12). The claim's arithmetic table

```
s=24 -> 1,769,040*24/5 = 8,491,392   "stabilizer 5"
s=12 -> 1,769,040*12/5 = 4,245,696   "stabilizer 10"
s= 6 -> 1,769,040* 6/5 = 2,122,848   "stabilizer 20"    sum = 14,859,936
```

is internally consistent and its sum coincides with the total number of 5-caps — but that is
a numerical coincidence, not a verification (see Task 5).

## Task 4 — Grundy value 1 for the three representatives — PASS

Rules used (the standard cap game, stated explicitly): a position is a cap `S`, a move adds
a point `p` with `S+p` a cap, normal play, `g(S) = mex{g(S+p) : p legal}`, `g = 0` for a
maximal position. `10 = q+1` is the largest cap size, so the recursion from a 5-cap has
depth ≤ 5 and the whole upper set is enumerated exactly. Three implementations/certificates:
memoised top-down recursion, BFS upper-set enumeration + bottom-up DP, and a **local mex
certificate** on every state of the upper set (which, on a finite child-closed acyclic set,
proves the labelling is the Grundy function by induction on size).

| representative | upper set (by cap size) | strict upset | terminal positions | children values | **g** |
|---|---|---|---|---|---|
| `{0,1,10,20,31}` | 132 = 1+21+74+30+5+1 | 131 | {7:4, 8:20, 10:1} = 25 | {0:13, 2:8} | **1** |
| `{0,1,10,20,42}` | 128 = 1+21+70+30+5+1 | 127 | {6:1, 8:20, 10:1} = 22 | {0:21} | **1** |
| `{0,1,10,20,41}` | 132 = 1+21+74+30+5+1 | 131 | {7:4, 8:20, 10:1} = 25 | {0:13, 2:8} | **1** |

(So moves are *not* always losing for the mover: some 6-cap children already have value 2;
`mex{0,2} = 1`.)

Further checks: all **42** five-caps through the frame have g = 1; the frame itself (4-cap)
has g = mex{1} = 0 with upper set 1,868 caps; g is invariant under all 24 frame-fixing
projectivities applied to all three representatives (72 images) and under 15 random
projectivities; **400 random 5-caps all have g = 1**.

## Task 5 — stabilizers, equivalence, and the true orbit structure — claim FAIL (conclusion still true)

All searches are **complete**: a projectivity is determined by the images of 4 points in
general position, every 4-subset of a 5-cap is a frame, so fixing the ordered frame of `S`
and enumerating the 120 ordered 4-tuples of `T` decides `S ~ T` exactly (negative = proof).
Positive controls (images under random projectivities, identity) are included.

**Complete stabilizers** (each independently confirmed):

| S | \|Stab_PGL(S)\| | \|PGL\|/\|Stab\| | claim |
|---|---|---|---|
| `{0,1,10,20,31}` | **4** (C4: cycle types 1⁵, 2²1, 4·1, 4·1) | **10,614,240** | 5 / 8,491,392 ✗ |
| `{0,1,10,20,42}` | **10** (D10: 1⁵, 2²1 ×5, 5-cycles ×4) | **4,245,696** | 10 / 4,245,696 ✓ |
| `{0,1,10,20,41}` | **4** | **10,614,240** | 20 / 2,122,848 ✗ |

**Pairwise equivalence:** `{…,31} ~ {…,41}` (explicit witness
`M = (8,0,4,5,0,4,5,5,2)`, det = 1, `M` maps the frame to `{0,10,20,41}`);
`{…,42}` is inequivalent to both. Testing all 42 caps against the two classes gives a
partition **30 + 12** (not 24/12/6), consistent with the S4 fusion above.

**True orbit sizes** (formula `|O| = #4-caps·c/5` with `c` = number of the 42 caps through
the frame that lie in `O`; `c = 30, 12`):

| orbit | c | size | stabilizer |
|---|---|---|---|
| containing `{0,1,10,20,31}` (and `{…,41}`) | 30 | 1,769,040·30/5 = **10,614,240** | 42,456,960/10,614,240 = **4** |
| containing `{0,1,10,20,42}` | 12 | 1,769,040·12/5 = **4,245,696** | **10** |
| sum | 42 | **14,859,936** = total #5-caps | — |

Since the two orbits are disjoint and their sizes sum to the total number of 5-caps, they
are **exactly the two orbits** and every 5-cap lies in one of them.

**Independent conic cross-check (`t6_conic.py`).** The unique conic (10-cap) through
`{0,1,10,20,31}` is `C = {0,1,10,20,31,45,51,62,75,88}`; `|Stab_PGL(C)| = 720 = q(q²−1)`
(complete search); `#conics = |PGL|/720 = 58,968 = q⁵−q²`. The stabilizer `G` acts on the
252 five-subsets of `C` with exactly **two orbits, of sizes 180 and 72**; since
`|PGL orbit| = 58,968 × (G-orbit size)`, the PGL orbits are `58,968·180 = 10,614,240` and
`58,968·72 = 4,245,696`, and `58,968·252 = 14,859,936`. This uses none of the frame/S4
machinery and reproduces the same answer, with stabilizers 720/180 = 4 and 720/72 = 10.

**Fourth, purely combinatorial check (`t6_conic.py`, last section).** The conic stabilizer is
`PGL(2,q)` of order `q(q²−1) = 720`, acting sharply 3-transitively on the `q+1 = 10` points.
Building `PGL(2,9)` directly as fractional-linear maps on `PG(1,9)` (10 points, explicit
`(a,b)` field arithmetic, **no PG(2,9) matrices at all**) gives 720 elements and exactly
**two orbits of sizes 180 and 72** on the 252 five-subsets. Same answer again.

**Second, independent implementation of the field (`t7_indep_field.py`).** GF(9) elements as
explicit pairs `(a,b)`, all operations hand-written, no tables: it re-derives the board
lines, the 42 extensions, `|Stab{0,1,10,20,31}| = 4`, the witness map, and the
inequivalence `{…,31} ≁ {…,42}`. So the refutation does not depend on the lookup tables.

**Consistency of "all 5-caps have Grundy value 1":** true, but for a corrected reason. The
claim's three-orbit premise is false; nevertheless there are exactly two orbits, their
representatives both have g = 1, and the Grundy value is PGL-invariant (the game tree is
transported by a projectivity), so all 14,859,936 5-caps have g = 1. Confirmed also on all
42 caps through the frame and on 400 random 5-caps.

---

## Discrepancies (numbered)

**D1 (main). Number of orbits and sizes.** There are **2** PGL(3,9) orbits of 5-caps, not 3:
`10,614,240` and `4,245,696` (sum 14,859,936). The claim's `8,491,392 / 4,245,696 /
2,122,848` is wrong; only the middle value is correct.

**D2. Stabilizers.** `|Stab|` = **4** and **10**, not 5 / 10 / 20.

**D3. Representatives are not one per orbit.** `{0,1,10,20,31}` and `{0,1,10,20,41}` are
PGL-equivalent (witness `M = (8,0,4,5,0,4,5,5,2)`, `M(F) = {0,10,20,41}`). Only
`{0,1,10,20,31}` and `{0,1,10,20,42}` are needed.

**D4. The orbit-size formula is wrong as used.** `|O| = 1,769,040·s/5` assumes distinct
S4-orbits on the 42 caps lie in distinct PGL orbits. They need not: a projectivity taking
`F+{p}` to `F+{q}` may map the frame `F` to another 4-subset of `F+{q}`. The map
(from S4-orbits to PGL orbits) is surjective but not injective; here the 24- and 6-orbits
fuse. The correct formula uses `c` = number of the 42 caps through the frame in the orbit:
`|O| = 1,769,040·c/5`, with `c = 30, 12` (`30 = 24+6`).

**D5. A misleading coincidence.** Both partitions sum to 14,859,936 (`8,491,392 + 4,245,696
+ 2,122,848` and `10,614,240 + 4,245,696`), because `c` and `s` both sum to 42 over
comparable orbit decompositions. Summing to the total is necessary but not sufficient; only
the direct stabilizer/equivalence computation (or the conic count) distinguishes them.

**D6 (notational).** `E[k] = 3(k//3)+(k%3)` is the identity; and the `1` in `(1:…)` is the
field element 1 (encoded 3). Reading it as the encoded integer 1 (= i) does not reproduce
the board.

## What the claim gets right

* board and coordinate map (with D6's reading);
* 14,859,936 5-caps; 1,769,040 4-caps, all in one orbit; exactly 42 five-caps through
  `{0,1,10,20}`;
* Stab{0,1,10,20} ≅ S4 of order 24 with S4-orbits 24 / 12 / 6 on the 42 caps;
* the three given sets are 5-caps and have Grundy value 1;
* **"all 5-caps have Grundy value 1"** (this conclusion survives, on the corrected 2-orbit
  structure).
