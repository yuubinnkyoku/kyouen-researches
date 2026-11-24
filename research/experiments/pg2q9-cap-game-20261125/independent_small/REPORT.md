# Independent verification — PG(2,9) cap game (small / foundational claims)

Directory: `research/experiments/pg2q9-cap-game-20261125/independent_small/`
Board: `../output/board_pg2q9.txt` (read only; nothing outside this directory was modified)
Python 3.12.13, **standard library only**, no compilation, no network, no third-party packages.
No commit was made.

**Overall: PASS on every one of the five tasks. No discrepancy was found.**

| # | Task | Verdict |
|---|------|---------|
| 1 | board is PG(2,9) (91/91, lines of 10, λ=1, degree 10) | **PASS** |
| 2 | 3-caps = 110,565 and 4-caps = 1,769,040 | **PASS** |
| 3 | single PGL(3,9) orbits, stabilizers 384 / 24, \|PGL\| = 42,456,960 | **PASS** |
| 4 | Grundy({0,1,10}) = 1, Grundy({0,1,10,20}) = 0, upset sizes/totals | **PASS** |
| 5 | 6-cap Grundy 2, maximal 6-cap Grundy 0, five-caps all Grundy 1 | **PASS** |

Everything below was recomputed from field arithmetic (`GF(9) = GF(3)[i]/(i^2+1)`)
and the board file; no code or intermediate result of the original experiment was reused.

---

## 0. Reproduce

```sh
cd research/experiments/pg2q9-cap-game-20261125/independent_small
python run_all.py            # ~100 s, writes run_all.log (everything below)
```

Individual pieces (each prints its own JSON, all deterministic):

```sh
python label_recovery.py     # how the board's point numbering was recovered
python core.py               # task 1 checks + field/group sanity
python task2_counts.py       # 3-cap / 4-cap enumeration
python task3_orbits.py       # generators, |PGL|, orbit BFS, stabilisers (~80 s)
python task4_grundy.py       # upsets + mex DP
python task5_observations.py # the two 6-caps, five-cap sample
python bonus_census.py       # one extra census layer + reference consistency
python genset_check.py       # which generator sets generate PGL(3,9)
```

Machine-readable outputs: `out_task2.json`, `out_task3.json`, `out_task4.json`,
`out_task5.json`, `out_bonus.json`, `out_gensets.json`.

---

## 1. The board is PG(2,9) — PASS

The file gives lines as sets of point indices only, so first the point
numbering was **recovered from the data** (`label_recovery.py`):

* the lines of indices 0–9 all contain point 0 and each is `{0} + a block of 9
  consecutive indices` (1–9, 10–18, …, 82–90): index 0 is the base of a pencil,
  and the other 90 points are grouped block-by-block by pencil line;
* the unique index→vector map consistent with that is

  ```
  index 0             -> (0:0:1)
  index 1+j  (0<=j<9) -> (0:1:E[j])
  index 10+9p+j       -> (1:E[p]:E[j])      E[k] = field element 3*(k//3)+(k%3)
  ```

  (the points with `x=0` first, then the points with `x=1` ordered
  lexicographically by `(y,z)`; this is also the "sorted canonical vectors,
  first non-zero coordinate = 1" order).

Verification (`core.check_board`, `python core.py`):

| check | result |
|-------|--------|
| declared header | `91 91`, no trailing content |
| 91 lines, all of length 10, all distinct | `true` |
| every point on exactly 10 lines | degree set `{10}` |
| every pair of points on exactly one line | 4095/4095 pairs, λ set `{1}` |
| every two distinct lines meet in exactly one point | intersection sizes `{1}` |
| collinear triples | 10,920 = 91·C(10,3) |
| the file reproduces **exactly** the line set computed from my own GF(9) construction | `true`, and even in the file's own line order |

So the board is the projective plane PG(2,9) (91 points, 91 lines of 10,
pair-λ 1, point degree 10), and the intended point indexing is confirmed
line-for-line.

## 2. Counts 3-caps = 110,565, 4-caps = 1,769,040 — PASS

Direct subset enumeration, no census tables used (`task2_counts.py`):

* all `a<b<c` with `c` not on the line `ab` → **110,565**;
  identity check: `C(91,3) − 91·C(10,3) = 121,485 − 10,920 = 110,565` ✓
* all 3-caps extended by `d>c` avoiding the three pair-lines → **1,769,040**;
  every one re-verified as a cap, all distinct;
* layer identity: `Σ_{3-caps} #(4th points) / 4 = 1,769,040` ✓
* bonus layer (`bonus_census.py`): `Σ_{4-caps} #(5th points) / 5 = 14,859,936`,
  which equals the reference census `SIZE 5 14859936` ✓

Reference census (`output/census_pg2q9.txt`) is consistent:
distribution sums to `128,917,712` ✓; `SIZE 9 = 10·SIZE 10` ✓;
`SIZE 10 = 58,968 = q^5 − q^2` (the number of conics in PG(2,q)) ✓.
I did **not** re-enumerate the whole 128,917,712-cap census (see §6).

## 3. Orbit claims — PASS

`|GL(3,9)| = 728·720·648 = 339,655,680`, hence
`|PGL(3,9)| = 339,655,680 / 8 = 42,456,960` ✓.

**Generators** (`core.generators`), 14 explicit invertible matrices over GF(9):
all 12 transvections `I + e_ij` and `I + i·e_ij` (6 positions × 2),
`diag(1+i,1,1)` (1+i is primitive, order 8), and the 3-cycle `e1→e2→e3→e1`.
Every generator was verified to be invertible (explicit inverse computed) and to
induce a permutation of the 91 points that **preserves the whole line set**
(i.e. it is a collineation).

**They generate all of PGL(3,9).** A Schreier stabiliser chain gives base/orbit
lengths `91, 90, 8, 81, 8`, and

```
91 · 90 · 8 · 81 · 8 = 42,456,960 = |PGL(3,9)|
```

Since every generator is in PGL(3,9), the generated group is exactly PGL(3,9)
(product of orbit lengths along the chain = exact group order; the last
stabiliser is trivial). `genset_check.py` shows the same for
(a) the set suggested by the task with `diag(i,1,1)` instead of `diag(1+i,1,1)`
and (b) a 5-element subset — all reach 42,456,960.

**Orbit BFS over 91-bit masks** (`task3_orbits.py`), using all 14 generators:

| cap | orbit size | equals | exact-set comparison with the independent enumeration |
|-----|-----------|--------|------------------------------------------------------|
| {0,1,10} | **110,565** | all 3-caps (110,565) | orbit ≡ enumerated 3-caps, symmetric difference **0** |
| {0,1,10,20} | **1,769,040** | all 4-caps (1,769,040) | orbit ≡ enumerated 4-caps, symmetric difference **0** |

**Stabiliser orders**, by direct enumeration of the projectivities fixing the
cap (matrices whose three basis images are cap points, one representative per
projective class):

| cap | \|Stab\| | orbit × \|Stab\| |
|-----|---------|------------------|
| {0,1,10} | **384** | 110,565 · 384 = 42,456,960 ✓ |
| {0,1,10,20} | **24** | 1,769,040 · 24 = 42,456,960 ✓ |

Hence: all 3-caps are a single PGL(3,9)-orbit with stabiliser order 384, and all
4-caps are a single orbit with stabiliser order 24 — **both claims confirmed**,
with the orbits compared as *sets* against the independent enumeration, not just
by cardinality.

## 4. Grundy values and upsets — PASS

Game model used: position = cap; a move adds a point and keeps it a cap;
terminal = maximal cap; `Grundy(P) = mex{ Grundy(P ∪ {p}) : p admissible }`.
The move graph is acyclic (size strictly increases), so the mex recursion is the
full-game Grundy value. Upsets were enumerated twice by independent methods:
canonical-order DFS with memoisation, and a level-by-level BFS
(`task4_grundy.py`, `upset_levels`), with identical results.

**3-cap {0,1,10}** (verified to be a cap):

| size | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | total |
|------|---|---|---|---|---|---|---|----|-------|
| claim | 1 | 64 | 1344 | 9408 | 16320 | 4032 | 448 | 64 | 31,681 |
| mine | 1 | 64 | 1344 | 9408 | 16320 | 4032 | 448 | 64 | 31,681 |

`Grundy = mex{0} = 1` (all 64 4-cap children have Grundy 0) — **claim 1 confirmed**.

**4-cap {0,1,10,20}** (verified to be a cap):

| size | 4 | 5 | 6 | 7 | 8 | 9 | 10 | total |
|------|---|---|---|---|---|---|----|-------|
| claim | 1 | 42 | 441 | 1020 | 315 | 42 | 7 | 1,868 |
| mine | 1 | 42 | 441 | 1020 | 315 | 42 | 7 | 1,868 |

`Grundy = mex{1} = 0` (all 42 5-cap children have Grundy 1) — **claim 0 confirmed**.

Extra detail (full Grundy distribution over each upset, useful as a consistency
check — e.g. every 8-cap in the 3-cap upset is terminal, every 9-cap has
Grundy 1, every 10-cap Grundy 0):

```
3-cap upset:  3:{1:1}  4:{0:64}  5:{1:1344}  6:{0:6848, 2:2560}
              7:{0:640, 1:15680}  8:{0:4032}  9:{1:448}  10:{0:64}
4-cap upset:  4:{0:1}  5:{1:42}   6:{0:321, 2:120}  7:{0:40, 1:980}
              8:{0:315}  9:{1:42}  10:{0:7}
```

Terminal positions (maximal caps) inside the upsets: 3,520 (3-cap) and 263
(4-cap); all were checked to have no admissible extension.

## 5. Observations — PASS

| observation | check | result |
|---|---|---|
| {0,1,10,20,32,39} is a cap with Grundy 2 | is-cap ✓, mex recursion | **cap: true, Grundy = 2** (7 extensions; upset 6:1, 7:7, 8:3) |
| {4,9,20,32,69,84} is a maximal 6-cap with Grundy 0 | is-cap ✓, 0 admissible points ✓ | **cap: true, maximal: true, Grundy = 0** (a maximal position is terminal, so Grundy 0 by definition) |
| random 5-caps containing {0,1,10,20} have Grundy 1 | all 42 such 5-caps computed (not just 8) | **42/42 have Grundy 1**; distribution `{1: 42}`; a random sample of 5: (0,1,10,20,31), (0,1,10,20,59), (0,1,10,20,71), (0,1,10,20,81), (0,1,10,20,52) → all 1 |

Extra empirical support for the invariance step: 3 random 3-caps
({19,41,50}, {6,9,83}, {12,46,68}) all have Grundy 1, and 3 random 4-caps
({4,11,53,55}, {8,11,30,70}, {7,28,74,80}) all have Grundy 0.

**Logic of the generalisation.** A collineation maps caps to caps and moves to
moves, so it is an isomorphism of the game graph; Grundy values are therefore
constant on PGL(3,9)-orbits. Together with §3 (one orbit of 3-caps, one orbit of
4-caps) and §4 (Grundy 1 and 0 on the representatives), this proves *all* 3-caps
have Grundy 1 and *all* 4-caps have Grundy 0 — the claims' generalisation is
sound.

## 6. Scope / limitations (stated explicitly)

* Not re-enumerated: the full 128,917,712-cap census, and the census/maximal
  counts for sizes 6–10 (`707,616 / 2,021,760 / 5,307,120 / 58,968`). Only
  k = 3, 4 were enumerated exhaustively, k = 5 derived from the 4-cap layer;
  the remaining entries were checked for internal consistency only
  (distribution sum, `q^5−q^2` conics = 58,968, `SIZE 9 = 10·SIZE 10`,
  `orbit·stabiliser = |PGL|` for every row of `output/orbits.txt`).
* Grundy values were computed for the two representatives and for a few random
  caps; the "all 3-caps / all 4-caps" statement is proved via orbit transitivity
  plus invariance, not by 110,565 separate DP runs.
* The `{6,7,8}`-cap orbit claims from `output/orbits.txt` were not recomputed
  (single-element orbits of those sizes were not part of the tasks).
* The board file was treated as read-only input; all point/line arithmetic,
  group elements, cap tests and Grundy values are independent reimplementations.

## 7. Discrepancies

**None.** Every claimed number reproduced exactly:

| quantity | claimed | independent |
|---|---|---|
| board | PG(2,9), 91 points / 91 lines of 10 | identical line set, line for line |
| 3-caps | 110,565 | 110,565 |
| 4-caps | 1,769,040 | 1,769,040 |
| 3-cap orbit / stabiliser | single / 384 | single (set equality) / 384 |
| 4-cap orbit / stabiliser | single / 24 | single (set equality) / 24 |
| \|PGL(3,9)\| | 42,456,960 | 42,456,960 (formula and generated-group order) |
| Grundy{0,1,10} | 1 | 1 |
| Grundy{0,1,10,20} | 0 | 0 |
| upset of 3-cap | {1,64,1344,9408,16320,4032,448,64}, 31,681 | identical |
| upset of 4-cap | {1,42,441,1020,315,42,7}, 1,868 | identical |
| Grundy{0,1,10,20,32,39} | 2 (and it is a cap) | 2, cap ✓ |
| Grundy{4,9,20,32,69,84} | 0 (and it is maximal) | 0, maximal ✓ |
| 5-caps over {0,1,10,20} | sample of 8 all 1 | all 42 are 1 |

Two clarifying notes (not discrepancies):

1. **Point numbering.** The board's indices are not stated in the file; they were
   recovered from the pencil structure and then confirmed by reproducing all 91
   lines in the file's own order. The recovered map is the "sorted canonical
   vectors, first non-zero coordinate = 1" order (index 0 = (0:0:1)), which is
   also what `scripts/build_pg2q9.py` documents.
2. **`E_ij(1), E_ij(i), diag(i,1,1), 3-cycle`** as suggested by the verification
   task does generate all of PGL(3,9) (checked with the Schreier chain), just
   like the `diag(1+i,1,1)` variant used for the main run.

---

### Files

| file | purpose |
|---|---|
| `core.py` | GF(9), plane construction, labelling, caps, PGL matrices, task-1 checks |
| `label_recovery.py` | derives and verifies the index→vector map from the board data |
| `task2_counts.py` | exhaustive 3-cap / 4-cap enumeration |
| `task3_orbits.py` | generators, \|PGL\|, Schreier chain, orbit BFS, stabiliser orders |
| `task4_grundy.py` | upset enumeration (two methods) and mex DP |
| `task5_observations.py` | the two 6-caps, all five-caps over the 4-cap, random samples |
| `bonus_census.py` | 5-cap layer, census/orbit-table consistency |
| `genset_check.py` | alternative generator sets |
| `run_all.py`, `run_all.log` | everything in one reproducible run |
