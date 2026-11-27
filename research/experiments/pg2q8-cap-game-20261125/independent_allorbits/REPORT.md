# Independent verification of K1327 — PGL(3,8) orbit decomposition of the caps of PG(2,8)

Directory: `research/experiments/pg2q8-cap-game-20261125/independent_allorbits/`
Everything here was written from scratch for this check.  The only input read
from outside this directory is the board file
`../output/board_pg2q8.txt` (read-only).

Environment: Windows, Python 3.12.13 (standard library only), gcc 15.2.0
(MSYS2) for the C engine `pg8.exe`.  No third-party Python packages, no
network, nothing committed.

## Summary

| task | subject | verdict |
|------|---------|---------|
| 1 | board is PG(2,8) in the claimed labelling | **PASS** |
| 2 | PGL(3,8) generators, \|PGL\| = 16,482,816, collineations | **PASS** |
| 3 | orbit sizes of the four K1327 start caps | **PASS** |
| 4 | conic orbit sizes for k = 6,7,8,9 | **PASS** |
| 5 | arithmetic closure / census / maximal-6 distinctness | **PASS**, with one discrepancy in the *stated* census total |

Every orbit size in K1327 was reproduced exactly, by an exhaustive orbit
decomposition of the cap set (not just from the listed representatives).
The only discrepancy found is arithmetic in the claim text:

> **K1327 says** "the sum of all sizes equals the independent census total
> 19,550,350".  The 11 per-k numbers listed in K1327 sum to **19,550,349**,
> and the independent enumeration also gives **19,550,349** non-empty caps.
> The two differ by exactly 1 — the empty cap (size 0) would make the total
> 19,550,350, so the stated total is either a typo or a count that includes
> the empty cap.  No orbit size or per-k census count is affected.

## Conventions

* `GF(8) = GF(2)[x]/(x^3+x+1)`; the element `a0 + a1 x + a2 x^2` is the
  integer `a0 + 2 a1 + 4 a2` (so `x = 2`; `x` is primitive, `x^3 = x+1`).
* Points of PG(2,8) = 1-dimensional subspaces of `GF(8)^3`, each represented
  by the unique vector whose first non-zero coordinate is 1.
* The board index of a point is its rank among the 73 canonical non-zero
  vectors sorted by integer value `a*64 + b*8 + c` (equivalently,
  lexicographic on the coordinate triple).  This is exactly the convention
  stated in the task.
* A cap is a point set with no three collinear.
* All orbit computations use the four generators `D, T, S, U` below.

---

## Task 1 — the board is PG(2,8) — PASS

`task1_board.py` (results in `results_task1.txt`).

* File syntax: header `73 73`; 73 lines, each with 9 distinct indices in 0..72.
* Projective-plane axioms (verified independently of any field model):
  * 73 distinct lines, 657 incidences;
  * every point on exactly 9 lines;
  * the 2628 point pairs are covered by the lines exactly once (no pair twice);
  * every two distinct lines meet in exactly one point.
  → the board is *some* projective plane of order 8.
* Desarguesian check: PG(2,8) was constructed from scratch from the field
  and the canonical-vector labelling.  The **set of 73 board lines equals the
  set of 73 constructed lines** (0 lines on either side differ).  Hence the
  board is exactly PG(2,8), and moreover exactly with the claimed point
  labelling.
* Labelling cross-checks: point 0 = `[0:0:1]`, points 1..8 = `[0:1:c]`,
  point `9+8b+c` = `[1:b:c]`; board line 0 = `{x0 = 0}`; the 8 affine lines
  through point 0 partition points 9..72.

The C engine repeats the line-set comparison (`board_lines_match_constructed=1`,
`results_c.txt`).

## Task 2 — PGL(3,8) — PASS

`task2_group.py` (`results_task2.txt`) and `pg8.exe order` (`results_c.txt`).

Generators (3×3 matrices over GF(8), acting on column vectors):

| name | matrix | det | meaning |
|------|--------|-----|---------|
| D | `diag(x, 1, 1)` | x | multiply x0 by x |
| T | `[[1,1,0],[0,1,0],[0,0,1]]` | 1 | x0 += x1 |
| S | swap x0,x1 | 1 | coordinate swap |
| U | swap x1,x2 | 1 | coordinate swap |

* All four are invertible, induce permutations of the 73 points, and **map
  every one of the 73 lines onto a line** — they are collineations (checked
  both in Python and in C).
* `|GL(3,8)| = (8^3-1)(8^3-8)(8^3-8^2) = 511*504*448 = 115,379,712`; the 7
  scalar matrices act trivially on points (checked), so
  `|PGL(3,8)| = 115,379,712/7 = 16,482,816`.
* **Schreier–Sims** (exact orbit–stabiliser recursion with Schreier
  generators, pure Python): stabiliser chain orbit lengths
  `73 * 72 * 64 * 49 = 16,482,816`, base points `[10, 1, 2, 9]`.
  The product is the order of the generated group, so
  `<D,T,S,U> = PGL(3,8)`.
* Independent second method (C): BFS on **ordered 4-arcs**.  A projective
  transformation fixing 4 points in general position is the identity, so the
  action is free and every orbit has size exactly `|<generators>|`.  The BFS
  (2^28 states) returns exactly **16,482,816**.

Both computations hit 16,482,816 = |PGL(3,8)|.

## Task 3 — orbit sizes of the four start caps — PASS

Each orbit computed twice: C hash-set BFS over 73-bit masks (`pg8.exe`) and an
independent pure-Python BFS (byte-chunk table action, `pgl_act.py`).

| cap | points | cap? | extensions | C orbit | Python orbit | K1327 | 
|-----|--------|------|-----------|---------|--------------|-------|
| cap7 | 12,16,18,22,54,66,69 | yes | 3 | 2,747,136 | 2,747,136 | 2,747,136 |
| cap8 | 12,16,18,22,40,54,66,69 | yes | 2 | 1,177,344 | 1,177,344 | 1,177,344 |
| cap6 non-max non-conic | 1,10,12,59,62,65 | yes | 4 | 4,120,704 | 4,120,704 | 4,120,704 |
| cap6 maximal | 10,47,49,55,61,64 | yes | 0 (maximal) | 686,784 | 686,784 | 686,784 |

None of the four is contained in the standard conic (so they are non-conic,
as K1327 states).  The maximal 6-cap has no extension; the other three are
extendable.  Implied stabiliser orders `|PGL|/|orbit|` are 6, 14, 4, 24.

Exhaustive check: the full orbit decomposition of *all* caps of each size
(`pg8.exe decompose`) gives exactly the same sizes (see Task 5), so these are
the only orbits of these sizes.

## Task 4 — conic layer — PASS

`task4_conics.py` (`results_task4.txt`), `pg8.exe orbits`, `pg8.exe quads`.

* The conic `Q = x0^2 + x1*x2 = 0` has 9 points
  `{0,1,18,30,39,48,51,60,69}` and is a cap (no three collinear).
* Its PGL orbit (9-point sets) is **32,704** = `|PGL|/504`, i.e. the number of
  conics; the setwise stabiliser therefore has order 504 = |PGL(2,8)|.
* Independent confirmation of the conic layer: enumerating **all 37,449
  quadratic forms up to scalar** (all 8^6 forms, one representative per
  scalar class) gives 32,704 forms whose zero set is a 9-point arc, and
  **32,704 distinct conics**.  So the orbit above is the complete conic layer.
* PGL orbit of a k-subset of one conic:

| k | orbit size | 32,704·C(9,k) | K1327 |
|---|-----------|---------------|-------|
| 5 | 4,120,704 | 4,120,704 | (k=5 orbit, bonus check) |
| 6 | 2,747,136 | 2,747,136 | 2,747,136 |
| 7 | 1,177,344 | 1,177,344 | 1,177,344 |
| 8 | 294,336 | 294,336 | 294,336 |
| 9 | 32,704 | 32,704 | 32,704 |

Since the orbit of a conic k-subset has exactly as many elements as there are
conic k-subsets (32,704·C(9,k)), the conic k-subsets form a **single orbit**
for every k, and every conic k-subset is PGL-equivalent to the chosen one.
k = 8 and k = 9 were recomputed in pure Python (294,336 and 32,704) and agree.

Bonus: the hyperoval (conic + nucleus (1,0,0) = point 9) is a 10-cap and its
orbit is 32,704 = the number of 10-caps.

## Task 5 — arithmetic closure — PASS (one stated-total discrepancy)

`task5_arithmetic.py` (`results_task5.txt`), from `results_c.txt`.

### 5.1 Cap census (exhaustive DFS, all sizes)

| k | computed | K1327 |
|---|----------|-------|
| 1 | 73 | 73 |
| 2 | 2,628 | 2,628 |
| 3 | 56,064 | 56,064 |
| 4 | 686,784 | 686,784 |
| 5 | 4,120,704 | 4,120,704 |
| 6 | 8,928,192 | 8,928,192 |
| 7 | 3,924,480 | 3,924,480 |
| 8 | 1,471,680 | 1,471,680 |
| 9 | 327,040 | 327,040 |
| 10 | 32,704 | 32,704 |
| total | **19,550,349** | stated 19,550,350 |

Also: maximal 6-caps = **2,060,352** = 3·686,784 (K1327), and no caps of size
≥ 11 exist.

### 5.2 Orbit decomposition (exhaustive; every cap of every size is covered)

| k | orbits (sizes) | stabiliser orders | K1327 |
|---|----------------|-------------------|-------|
| 1 | 73 | 225,792 | OK |
| 2 | 2,628 | 6,272 | OK |
| 3 | 56,064 | 294 | OK |
| 4 | 686,784 | 24 | OK |
| 5 | 4,120,704 | 4 | OK |
| 6 | 4,120,704 · 2,747,136 · 686,784 · 686,784 · 686,784 | 4, 6, 24, 24, 24 | OK (five orbits) |
| 7 | 2,747,136 · 1,177,344 | 6, 14 | OK (two) |
| 8 | 1,177,344 · 294,336 | 14, 56 | OK (two) |
| 9 | 294,336 · 32,704 | 56, 504 | OK (two) |
| 10 | 32,704 | 504 | OK |

* Every orbit size divides `|PGL| = 16,482,816`; the implied stabiliser
  orders are all integers (right-hand columns).
* Per-k sums of orbit sizes equal the census counts exactly.
* Sum of all orbit sizes = 19,550,349 = census total (all caps are accounted
  for; the decomposition is a partition).
* k = 6 identification: conic 6-subsets 2,747,136 (orbit of any conic
  6-subset), non-maximal non-conic 4,120,704 (orbit of the K1327 start cap;
  also `8,928,192 − 2,747,136 − 2,060,352`), maximal 6-caps 3 · 686,784
  (each orbit of size 686,784 consists of maximal caps; the K1327 maximal
  6-cap `{10,47,49,55,61,64}` lies in the orbit with representative
  `0,1,9,18,28,35`).
* k = 7/8/9 identification: the conic orbit is the one of size
  1,177,344 / 294,336 / 32,704; the non-conic orbit is the one of size
  2,747,136 / 1,177,344 / 294,336 (matches the K1327 start caps and the
  constructed non-conic 9-cap).
* k = 10: single orbit 32,704 (the hyperovals).

### 5.3 The three maximal 6-cap orbits are pairwise distinct

Exhaustive decomposition of the 2,060,352 maximal 6-caps gives exactly three
orbits of 686,784 each, with representatives

```
rep0 = 0,1,9,18,28,35      rep1 = 0,1,9,18,28,53      rep2 = 0,1,9,18,28,71
```

Membership probes (BFS orbit of each representative, then membership test):

```
probe k1327_max6_in_orbit0=1   k1327_max6_in_orbit1=0   k1327_max6_in_orbit2=0
probe rep1_in_orbit0=0  rep2_in_orbit0=0
probe rep0_in_orbit1=0  rep2_in_orbit1=0
probe rep0_in_orbit2=0  rep1_in_orbit2=0
```

So the three orbits are pairwise disjoint, each is a set of maximal 6-caps,
and the K1327 maximal 6-cap belongs to exactly one of them.

### 5.4 Discrepancy

Only one:

* **Stated census total 19,550,350 vs computed 19,550,349 (−1).**
  The 11 per-k values listed in K1327 themselves sum to 19,550,349; the
  exhaustive enumeration also gives 19,550,349.  The difference is exactly the
  empty cap, so the stated total is consistent only if it counts the empty cap
  (size 0).  This does not affect any orbit size, any per-k census count, or
  any stabiliser order.

Nothing else differed: all sizes, all orbit counts, all sums matched.

---

## Methods — why these computations are exact

* **Group order.**  Two independent exact methods: (a) the Schreier–Sims
  recursion, where each level's stabiliser is generated by Schreier
  generators (Schreier's lemma gives an exact generating set, so the product
  of orbit lengths is exactly the group order); (b) BFS on ordered 4-arcs,
  where the action of PGL(3,8) is free (a collineation fixing 4 points in
  general position is the identity), so every orbit has size `|G|`.
* **Orbit sizes.**  BFS with a hash set of visited 73-bit masks.  The
  decomposition additionally asserts that every image of an orbit element is
  again a cap of the same size (so no orbit can leave the enumerated cap
  set).
* **Census.**  Depth-first enumeration of caps with an incremental "forbidden
  set" (points collinear with an already chosen pair), adding points in
  increasing index order, so every cap is generated exactly once.  The
  counts of k-caps are therefore exact, not estimated.
* **Conic layer.**  Conics are counted twice: as the PGL orbit of one conic
  (32,704) and as the number of distinct 9-point arcs arising as zero sets of
  all quadratic forms up to scalar (32,704).  The k-subsets are counted as a
  PGL orbit and compared with 32,704·C(9,k).

## Files

| file | contents |
|------|----------|
| `pg2q8.py` | GF(8), points/lines of PG(2,8), board reader, matrices, permutations |
| `pgl_act.py` | fast pure-Python point-set action + orbit BFS |
| `parse_out.py` | parser for the C engine output |
| `task1_board.py` | Task 1 checks → `results_task1.txt` |
| `task2_group.py` | Task 2 (generators, order, Schreier–Sims) → `results_task2.txt` |
| `task3_orbits.py` | Task 3 (C + Python orbit BFS) → `results_task3.txt`, `task3_out.txt` |
| `task4_conics.py` | Task 4 (conic layer) → `results_task4.txt` |
| `task5_arithmetic.py` | Task 5 (arithmetic) → `results_task5.txt` |
| `pg8.c` | C engine: board check, 4-arc order BFS, cap census, orbit decomposition, conic/quadric enumeration, probes |
| `pg8.exe` | compiled C engine |
| `results_c.txt` | complete C engine output |
| `run_all.ps1` | rebuilds and reruns everything, ~3 minutes |
| `run_all_log.txt` | log of the end-to-end reproduction run |

## Reproduction

From this directory:

```powershell
gcc -O2 -std=c11 -Wall -Wextra -o pg8.exe pg8.c
.\pg8.exe all "..\output\board_pg2q8.txt" > results_c.txt
python task1_board.py
python task2_group.py
python task3_orbits.py
python task4_conics.py
python task5_arithmetic.py
```

or simply `pwsh -File run_all.ps1` (≈3 minutes on 16 cores; the C engine is
about 40 s, the pure-Python orbit BFS about 80 s, everything else a few
seconds).  The end-to-end run was performed after all edits
(`run_all_log.txt`, exit code 0) and printed `TASK 1: PASS` … `TASK 5: PASS`
with the census-total note described above.

## Bottom line

Every numerical claim in K1327 about the PGL(3,8) orbit structure of the caps
of PG(2,8) is reproduced exactly and independently: the per-size orbit
multisets, the conic orbits 32,704·C(9,k), the three maximal 6-cap orbits of
686,784 each, the four start-cap orbits, and the divisibility by
|PGL| = 16,482,816.  The single discrepancy is the stated *total* census
number 19,550,350, which is one larger than both the sum of K1327's own per-k
counts (19,550,349) and the exhaustive enumeration (19,550,349); it is
accounted for by the empty cap.
