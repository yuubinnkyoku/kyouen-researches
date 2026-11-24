# Independent verification — PGL(3,9) orbit claims for the maximal caps of PG(2,9)

Experiment: `research/experiments/pg2q9-cap-game-20261125/`
Verification directory: `research/experiments/pg2q9-cap-game-20261125/independent_orbits/`
Date: 2026-11-25. Python 3.12.13, **standard library only** (no numpy / third party).
Nothing outside this directory was modified; nothing was committed.

**要点（日本語）**: 主張されている 4 つの極大キャップ（サイズ 6, 7, 8, 10）の個数・軌道・
固定部分群を、GF(9)=GF(3)[x]/(x²+1) からの独自構成とボードとの明示的同型写像、独自生成元
（12 個の基本トランスベクション＋対角＋3-サイクル）による 91 ビットマスク BFS で独立に検証した。
4 つの軌道サイズは 707,616 / 2,021,760 / 5,307,120 / 58,968 で主張と一致し、固定部分群の位数も
60 / 21 / 8 / 720 で一致した。極大キャップの完全な国勢調査もフレーム経由の二重数え上げで独立に
再現し、|PGL(3,9)| = 42,456,960 も 3 通りに確認した。**5 タスクすべて PASS、不一致なし。**

---

## 0. Verdict

| Task | Content | Verdict |
|---|---|---|
| 1 | Four start sets are caps and maximal | **PASS** |
| 2 | Own PG(2,9) model from GF(9), explicit board bijection, own generators, \|PGL(3,9)\| = 42,456,960 | **PASS** |
| 3 | BFS orbit sizes; independent census; single orbit per family; no maximal 9-caps | **PASS** |
| 4 | Second maximal cap of each size + explicit group element start → second | **PASS** |
| 5 | Stabilizer orders and structure (60, 21, 8, 720) | **PASS** |

**Overall: PASS. No discrepancies with the claim.** Every number in the claim was
reproduced: maximal-cap counts `6: 707,616`, `7: 2,021,760`, `8: 5,307,120`,
`10: 58,968`, no maximal 9-caps, one orbit per family under PGL(3,9), stabilizer
orders `60, 21, 8, 720`, `|PGL(3,9)| = 42,456,960`.

---

## 1. What was checked, and how it is independent

The board file is treated as an **unlabelled incidence structure**: it is parsed,
its projective-plane axioms are checked, and an explicit line-preserving bijection
to an independently constructed PG(2,9) is found by constraint propagation +
backtracking (not by reproducing the build script's ordering). The parent's
`output/*.txt` files were read only to compare numbers (`orbits.txt`,
`analysis.json`); no parent code is imported or executed. The four start caps are
taken from the task statement (`common.STARTS`).

| File | Purpose |
|---|---|
| `pgcore.py` | GF(9) arithmetic, PG(2,9) model, board parser, plane-axiom checks, isomorphism search, 3×3 linear algebra over GF(9), permutation generators, 91-bit-mask BFS, frame-census DFS, stabilizer enumeration, permutation-group utilities |
| `common.py` | the four start caps (board labels), claimed numbers, `setup()` = (model, board, φ) |
| `task1_caps.py` | Task 1 — cap + maximality audit of the start sets (pure incidence) |
| `task2_model_iso.py` | Task 2 — field, model, board, bijection, \|PGL\|, generators |
| `task3_orbits.py` | Task 3 — BFS orbits, independent census, conics |
| `task4_second_caps.py` | Task 4 — second caps and explicit projectivities |
| `task5_stabilizers.py` | Task 5 — full stabilizer enumeration and structure |
| `extra_checks.py` | second-frame census, orbit membership of all caps through a frame, identities, group-order arguments, PGL(2,9) order distribution |
| `run_all.py` | runs all of the above in order |
| `results/*.json`, `results/*_run.log` | machine-readable results and captured logs |

Commands (from `independent_orbits/`):

```sh
python task1_caps.py                     #  ~0.1 s
python task2_model_iso.py                #  ~4 s   (brute-force frame count)
python task3_orbits.py 6 7 8 10          #  ~300 s (dominated by the 8-cap BFS)
python task4_second_caps.py              #  ~8 s
python task5_stabilizers.py              #  ~4 s
python extra_checks.py                   #  ~1 s
# or simply:  python run_all.py
```

Exact arithmetic everywhere (GF(9) tables, integer bit masks); no floating point
is used in any decision.

---

## 2. Task 1 — the four start caps are caps and maximal  **PASS**

Pure board incidences (`board_pg2q9.txt`: 91 points, 91 lines, 10 points per line,
each point on 10 lines, every point pair on exactly one line, every two lines meet
once — all verified).

| k | start cap (board labels) | max points on a line | secants (= C(k,2)) | tangents | external | addable points | verdict |
|---|---|---|---|---|---|---|---|
| 6 | `4 9 20 32 69 84` | 2 | 15 | 30 | 46 | none | PASS |
| 7 | `16 47 51 56 60 80 82` | 2 | 21 | 28 | 42 | none | PASS |
| 8 | `32 39 42 47 56 59 84 87` | 2 | 28 | 24 | 39 | none | PASS |
| 10 | `6 9 27 32 34 37 45 75 77 82` | 2 | 45 | 10 | 36 | none | PASS |

Maximality was checked twice: (a) a point outside a cap is addable iff it lies on
no secant line — there are none; (b) brute force add-and-test over all 91 points —
no outside point can be added. Both agree. The secant count equals C(k,2) as it
must for a k-arc.

---

## 3. Task 2 — own model, board match, own generators, \|PGL(3,9)\|  **PASS**

### 3.1 GF(9) = GF(3)[x]/(x²+1)

Elements encoded as `e = a + 3b` for `a + b·i`, `i² = -1`. All field axioms
verified exhaustively: commutativity, associativity, distributivity, 0/1, every
nonzero element invertible, no zero divisors, characteristic 3, `i² = -1`,
`x²+1` has no root in GF(3), additive group ≅ C3×C3, multiplicative group cyclic of
order 8 with order multiplicities `{1:1, 2:1, 4:2, 8:4}`.

### 3.2 Own PG(2,9)

Points = 91 canonical nonzero vectors of GF(9)³ (first nonzero coordinate 1);
lines = kernels of the 91 nonzero covectors up to scalar. Axioms checked:
91 lines of 10 points, every point on 10 lines, 4095 point pairs, pair-λ = 1,
every two lines meet in exactly one point.

### 3.3 The board is PG(2,9): explicit bijection

`find_isomorphism` fixes a projective frame on each side and closes the partial map
under "line through two known points" / "point on two known lines", backtracking on
the few free choices. It terminated after **2 search nodes** and the resulting
bijection φ (board → model) was verified on **all 91 lines** (each board line maps
onto a model line; φ is a bijection). Excerpt:

```
φ(board 0..9) = [0, 1, 4, 7, 2, 5, 8, 3, 6, 9]
board line  0  -> model line [0..9]
board line  1  -> model line [0,10..18]
board line 45  -> [2, 15, 22, 32, 45, 52, 62, 66, 73, 83]
board line 90  -> [9, 15, 20, 34, 37, 54, 59, 71, 76, 84]
```

The full map is in `results/task2_model_iso.json` (`"phi"`). This proves the board
file is a projective plane isomorphic to PG(2,9) (not merely a plane of order 9).

### 3.4 \|PGL(3,9)\| = 42,456,960 — three agreeing counts

| method | value |
|---|---|
| \|GL(3,9)\|/8 = 728·720·648 / 8 = 339,655,680 / 8 | **42,456,960** |
| brute force over all C(91,4) = 2,672,670 four-subsets: 1,769,040 with no collinear triple, × 24 | **42,456,960** |
| 91·90·81·64 (p1 ≠ p0, p2 off a line, p3 off the three sides) | **42,456,960** |

Sharp transitivity was also verified computationally: for 60 random frame pairs the
12×13 linear system for `A f_i = λ_i d_i` has a **unique** solution and it is
invertible (60/60); for 72 random non-frame 4-tuples **no** invertible solution
exists (0/72). (Proof: for frames f, d with `f4 = Σ α_i f_i`, `d4 = Σ β_i d_i` the
map `A f_i = (β_i/α_i) d_i` is invertible and sends f4 ↦ d4; a projectivity fixing
a frame is a scalar matrix.) Hence PGL acts simply transitively on ordered frames
and `|PGL| = #ordered frames`.

### 3.5 Own generating set

14 generators, each given as a 3×3 matrix over GF(9) and converted to a permutation
of the 91 points:

* the 12 elementary transvections `E_ij(1)`, `E_ij(i)` (i ≠ j, 6 ordered pairs × 2),
* `diag(i,1,1)`,
* the 3-cycle `(x,y,z) ↦ (y,z,x)`.

Each is invertible (det 1, except `diag(i,1,1)` with det = i), each induces a
bijection of the 91 points, and a scalar multiple of a generator induces the same
point permutation (checked explicitly) — so the action is a PGL action, not a GL
action.

---

## 4. Task 3 — orbit sizes, single orbits, independent census  **PASS**

### 4.1 BFS orbits under the 14 generators (91-bit masks)

BFS over 91-bit point-set masks; permutations are applied through 8 precomputed
12-bit chunk tables (≈ 2.5 µs per mask per generator, exact).

| k | start cap (board) | orbit size | claim | match | time | 100 sampled members are maximal k-caps |
|---|---|---|---|---|---|---|
| 6 | `4 9 20 32 69 84` | **707,616** | 707,616 | ✔ | 24.7 s | ✔ |
| 7 | `16 47 51 56 60 80 82` | **2,021,760** | 2,021,760 | ✔ | 75.7 s | ✔ |
| 8 | `32 39 42 47 56 59 84 87` | **5,307,120** | 5,307,120 | ✔ | 207.2 s | ✔ |
| 10 | `6 9 27 32 34 37 45 75 77 82` | **58,968** | 58,968 | ✔ | 2.0 s | ✔ |

### 4.2 Independent census of all caps (double counting over one frame)

Method (exact, no group used): take a fixed projective frame F (4 points, no three
collinear) and DFS-enumerate every cap containing F. Since PGL(3,9) is transitive on
frames (§3.4), the number `m_k` of maximal k-caps containing a fixed frame is the
same for every frame, and double counting (maximal k-cap, frame contained in it),
with C(k,4) frames per k-cap and 1,769,040 frames, gives

```
#(maximal k-caps) = 1,769,040 · m_k / C(k,4)        (same for all k-caps with T_k)
```

| k | T_k (all k-caps through F) | all k-caps (derived) | parent `analysis.json` | m_k (maximal through F) | maximal k-caps (derived) | parent |
|---|---|---|---|---|---|---|
| 4 | 1 | 1,769,040 | 1,769,040 | 0 | 0 | 0 |
| 5 | 42 | 14,859,936 | 14,859,936 | 0 | 0 | 0 |
| 6 | 441 | 52,009,776 | 52,009,776 | 6 | **707,616** | 707,616 |
| 7 | 1,020 | 51,554,880 | 51,554,880 | 40 | **2,021,760** | 2,021,760 |
| 8 | 315 | 7,960,680 | 7,960,680 | 210 | **5,307,120** | 5,307,120 |
| 9 | 42 | 589,680 | 589,680 | **0** | **0** | 0 |
| 10 | 7 | 58,968 | 58,968 | 7 | **58,968** | 58,968 |

Sizes 0,1,2,3 are checked by closed forms (1; 91; C(91,2) = 4,095;
C(91,3) − 91·C(10,3) = 110,565). All derived totals match the parent's census
table exactly, including **no maximal 9-caps** (and no maximal 5-caps either) and
the total number of maximal caps 707,616 + 2,021,760 + 5,307,120 + 58,968 =
**8,095,464**, and the total number of caps **128,917,712** = the parent's value.

**Single-orbit conclusion.** The orbit of each start cap under the subgroup H ≤ PGL
generated by our 14 generators is contained in the corresponding family of maximal
k-caps (images of a maximal cap under a collineation are maximal k-caps), and its
size equals the independently counted family size. Hence the orbit **is** the whole
family: each of the four families is a **single orbit**, even under H.

### 4.3 10-caps are conics

Counting nondegenerate ternary quadratic forms over GF(9) modulo scalars:
531,440 nonzero symmetric 3×3 matrices, 471,744 of them with det ≠ 0, /8 =
**58,968 = 9⁵ − 9²** — equal to the number of 10-caps. The start 10-cap is the zero
set of a nonsingular quadratic form (form matrix `[[5,6,5],[6,3,2],[5,2,3]]`, the
1-dimensional space of forms through its 10 points), whose zero set is exactly the
cap. So 10-caps = conics = one orbit of size 58,968.

### 4.4 The 14 generators generate all of PGL(3,9)

Two independent arguments:

* **Computational (given the verified census).** Let H = ⟨generators⟩ ≤ PGL(3,9).
  For each of the four caps, |H·C| equals the full family size = |PGL|/|Stab|, so
  `i := |PGL|/|H|` divides each of 60, 21, 8, 720; `gcd(60,21,8,720) = 1`, hence
  **i = 1 and H = PGL(3,9)**.
* **Structure theory.** Elementary transvections generate SL(3,9); for q = 9 every
  element of GF(9)^* is a cube (`x ↦ x³` is a bijection, verified), so
  GL = SL·Z and PGL = PSL ≅ SL(3,9), of order |GL|/8 = 42,456,960 = |PGL| — hence
  the transvections already generate all of PGL(3,9).

---

## 5. Task 4 — a second maximal cap and an explicit group element  **PASS**

For each size a second maximal cap was constructed **without using the group**:

* (i) incidence DFS: all maximal k-caps through the fixed frame F (pure incidence);
* (ii) random greedy maximal caps grown on the board plane (pure incidence);
* (iii) for k = 10 additionally the conic `x² + y² + z² = 0`.

Then an explicit element of PGL(3,9) mapping the start cap onto the second cap was
found: fix a projective frame f inside the start cap and enumerate ordered frames d
of the second cap; each pair gives a 12×13 homogeneous system
`A f_i = λ_i d_i` whose 1-dimensional solution space is a genuine element
A ∈ GL(3,9) (det ≠ 0), i.e. a point of PGL(3,9). Checks: the matrix maps the start
cap exactly onto the second cap in the **model** labelling *and* after transport to
the **board** labelling by φ, and the induced board permutation preserves all 91
board lines.

| k | second cap (board labels) | built by | explicit elements found | matrix A | det | all checks |
|---|---|---|---|---|---|---|
| 6 | `0 1 10 20 72 89` | incidence DFS | **60** | `[[1,0,0],[1,3,6],[0,6,4]]` | 3 | ✔ |
| 7 | `0 1 10 20 34 49 75` | incidence DFS | **21** | `[[6,7,1],[1,1,3],[2,6,8]]` | 1 | ✔ |
| 8 | `0 1 10 20 34 45 66 78` | incidence DFS | **8** | `[[4,3,4],[4,2,3],[7,0,2]]` | 1 | ✔ |
| 10 | `0 1 10 20 34 48 58 69 81 86` | incidence DFS | **720** | `[[1,0,0],[1,1,4],[6,8,2]]` | 8 | ✔ |

Extra 10-cap: the conic `x²+y²+z² = 0` has board point set
`2 3 13 16 20 21 29 30 37 64`, is a maximal 10-cap, and **720** explicit elements
map the start 10-cap onto it.

The number of elements mapping the start cap onto any other member of its orbit is
exactly |Stab(start cap)|, so these counts independently reproduce the claimed
stabilizer orders 60, 21, 8, 720 (§6). Feasibility: all searches are small
(enumerating ordered frames of a 6/7/8/10-point set and solving linear systems),
and every one found many solutions — transitivity is directly witnessed, not just
inferred from a count.

---

## 6. Task 5 — stabilizer orders and structure  **PASS**

The stabilizer was **fully enumerated** (every g with g(C) = C): fix one ordered
frame f inside C, enumerate all ordered frames d of C, solve `A f_i = λ_i d_i`;
every g ∈ Stab produces exactly one d = g(f), so the number of successes is
exactly |Stab_PGL(C)|.

| k | \|Stab\| (enumerated) | claim | \|PGL\|/orbit | \|Stab\|·\|orbit\| | element orders | structure |
|---|---|---|---|---|---|---|
| 6 | **60** | 60 | 42,456,960/707,616 = 60 | 42,456,960 ✔ | 1:1, 2:15, 3:20, 5:24 | **A5 = PSL(2,5)**, perfect (derived = 60), 2-transitive on the 6 cap points |
| 7 | **21** | 21 | 42,456,960/2,021,760 = 21 | 42,456,960 ✔ | 1:1, 3:14, 7:6 | **C7 : C3** (Frobenius group of order 21): non-abelian, 6 elements of order 7 ⇒ normal Sylow 7, derived subgroup = C7 (order 7) |
| 8 | **8** | 8 | 42,456,960/5,307,120 = 8 | 42,456,960 ✔ | 1:1, 2:5, 4:2 | **D4** (dihedral of order 8): non-abelian, 5 involutions, 2 elements of order 4, derived subgroup = C2 |
| 10 | **720** | 720 | 42,456,960/58,968 = 720 | 42,456,960 ✔ | 1:1, 2:81, 3:80, 4:90, 5:144, 8:180, 10:144 | **PGL(2,9)**, sharply 3-transitive on the 10 points of the conic, derived subgroup of order 360 |

Notes on the identification:

* The 6-cap stabilizer is A5 acting on the 6 cap points as PSL(2,5) on P¹(5)
  (transitive and 2-transitive, 60 = 6·5·2). Orders 1,2,3,5 with multiplicities
  1,15,20,24 and perfectness characterize A5.
* The 7-cap stabilizer has order 21 = 3·7 and is non-abelian with 6 elements of
  order 7, hence C7 ⋊ C3 (the Frobenius group), not C21.
* The 8-cap stabilizer has order 8 with five involutions and two elements of order
  4 and is non-abelian, which identifies D4 among the five groups of order 8
  (C8 has 1 involution, C4×C2 is abelian, C2³ has 7, Q8 has 1).
* The 10-cap stabilizer is the full conic stabilizer PGL(2,9) of order 720, acting
  sharply 3-transitively on the 10 conic points (10·9·8 = 720 distinct images of an
  ordered triple). Its element-order distribution is exactly that of PGL(2,9)
  computed independently from the 5,760 invertible 2×2 matrices over GF(9)
  (§7). It is **not** S6 despite |S6| = 720: S6 has no elements of order 8 or 10,
  whereas this group has 180 of order 8 and 144 of order 10. (Classically this
  sharply 3-transitive group of degree 10 is the Mathieu group M10.)

All four stabilizer orders are therefore consistent with the orbit sizes and with
|PGL(3,9)| = 42,456,960 in the strongest possible way: |Stab|·|orbit| = |PGL| for
each family, with both factors computed independently.

---

## 7. Extra checks  **PASS**

1. **Second frame.** Repeating the census with a different frame `(0,1,10,21)` (and
   with the original `(0,1,10,20)`) gives identical per-frame counts
   `T = [1,42,441,1020,315,42,7]`, `m = [0,0,6,40,210,0,7]`, confirming the
   frame-independence used in §4.2.
2. **Orbit membership of all caps through the frame.** Every maximal k-cap through
   F other than the start cap is projectively equivalent to the start cap
   (an explicit projectivity was found for each): 6/6 (k=6), 40/40 (k=7),
   7/7 (k=10), and 5/5 sampled for k=8 (there are 210 such caps; the sample was
   used because each membership test enumerates up to 1,680 frames × a linear
   solve).
3. **Structural identities.** `#10-caps = #conics = 58,968`;
   `#9-caps = 10·#conics = 589,680`; `#non-maximal 8-caps = C(10,8)·#conics =
   2,653,560`; `#8-caps = 5,307,120 + 2,653,560 = 7,960,680`; total maximal caps
   8,095,464; total caps 128,917,712 — all equal to `output/analysis.json`.
4. **9-caps and non-maximal 8-caps lie in conics.** All 42 nine-caps through F lie
   inside one of the 7 conics through F; all 105 non-maximal 8-caps through F lie
   inside such a conic.
5. **Group-order arguments.** |GL(3,9)| = 339,655,680; |SL(3,9)| = 42,456,960 =
   |PGL(3,9)|; cubing is a bijection of GF(9)^*; gcd(60,21,8,720) = 1.
6. **PGL(2,9) order distribution** from 2×2 matrices agrees exactly with the
   720-element stabilizer, and differs from S6's — settling the identification.

---

## 8. Discrepancies

**None.** Every claimed number was reproduced exactly. Two remarks for the record:

* `output/starts.txt` holds, per size, a triple such as `6 1048608 4296016400`
  (two large integers, apparently Grundy/hash data) — it does **not** contain the
  cap point lists; the start caps used here are the ones given in the task
  statement. Nothing in that file was needed or used.
* While developing the verifier I hit two bugs *in my own check code* (a
  sorted-vs-unsorted list comparison in task 4, and an unbound variable in task 5);
  both were fixed and the runs were repeated. They were never discrepancies in the
  claim.

Caveats / scope:

* The claim is about **PGL(3,9)**; that is exactly what was verified. (PΓL would
  only merge orbits, and since each family is already a single PGL orbit, it is a
  single PΓL orbit as well.)
* The "single orbit" statement is proved as: `orbit ⊆ family` (always) and
  `|orbit| = |family|` with the family size computed by an independent census.
* The census's frame-independence relies on transitivity of PGL on projective
  frames, which is proved in §3.4 (unique invertible projectivity for every frame
  pair, verified on random samples and proved in general).
* All computations are exact finite arithmetic; no probabilistic step influences any
  conclusion (random sampling is used only for spot checks that are additionally
  covered by the exhaustive counts).

---

## 9. Reproduce

```sh
cd research/experiments/pg2q9-cap-game-20261125/independent_orbits
python run_all.py
```

Machine-readable results: `results/task1_caps.json`, `results/task2_model_iso.json`
(includes the full board→model bijection `phi` and all generator permutations),
`results/task3_orbits.json`, `results/task4_second_caps.json` (includes the explicit
matrices and board permutations), `results/task5_stabilizers.json`,
`results/extra_checks.json`. Console logs: `results/task3_run.log`,
`results/task4_run.log`, `results/task5_run.log`, `results/extra_checks_run.log`.
