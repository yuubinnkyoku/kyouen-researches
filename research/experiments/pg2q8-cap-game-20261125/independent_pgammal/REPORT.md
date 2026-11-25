# Independent verification of K1330 — PΓL(3,8) cap orbits of PG(2,8)

Directory: `research/experiments/pg2q8-cap-game-20261125/independent_pgammal/`  
Date: 2026-11-26  
Board: `../output/board_pg2q8.txt` (read-only; not modified)  
Implementation: Python 3.12 standard library only, plus a C cap census
compiled locally (`cap_census.c`).

**Overall verdict: PASS on all five requested tasks.** Two non-numerical
notes/discrepancies are recorded in §7 (a one-off in the task statement's
"15 orbits including the empty cap", and an incomplete *justification*
sentence in K1330 that does not affect the conclusion).

No file outside this directory was created or modified. Nothing was committed.

---

## 1. Summary

| Task | Subject | Verdict |
|---|---|---|
| 1 | Board, GF(8), the two 6-cap representatives, their φ images, φ bijection/order | **PASS** |
| 2 | PGL(3,8) from own generators, \|PGL\|=16,482,816, φ normalises PGL, φ∉PGL, \|<PGL,φ>\|=49,448,448 | **PASS** |
| 3 | Orbit BFS: φ(C6) in the 2,747,136 conic orbit, φ(D6) in the 4,120,704 non-max orbit | **PASS** |
| 4 | Divisibility of every proposed PΓL orbit size; the four quoted pairwise sums do not divide \|PΓL\| | **PASS** |
| 5 | Total count: 15 non-empty PΓL orbits sum to 19,550,349; with the empty cap, 19,550,350 | **PASS** (wording note in §7) |

Key numbers reproduced independently:

* `|PGL(3,8)| = 16,482,816`, `|PΓL(3,8)| = 49,448,448`.
* PGL has **17** non-empty cap orbits (18 including the empty cap).
* PΓL has **15** non-empty cap orbits (16 including the empty cap).
* Total caps in PG(2,8): **19,550,350** including the empty cap
  (**19,550,349** non-empty).
* All 17 PGL orbit sizes match K1327 exactly, and their per-size sums equal an
  independent C census of all caps (K1300's table).

---

## 2. Files and how to reproduce

| File | Role |
|---|---|
| `common.py` | GF(8)=GF(2)[x]/(x³+x+1), canonical points/indices, all 73 lines, board loader, Frobenius φ |
| `group.py` | permutations, orbit/transversal, deterministic Schreier–Sims (order + membership), self-tests |
| `task1_board.py` | Task 1 checks |
| `task2_group.py` | Task 2 checks (8 elementary generators, orders, φ normalisation, φ∉PGL) |
| `conic.py` | GF(8) linear algebra, quadratic forms, conic through 5 points |
| `reps.py` | representatives of all 17 PGL orbits, conic/non-conic and maximality validation |
| `bfs.py` | 2-generator set of PGL verified by Schreier–Sims; fast 73-bit cap-image kernel; orbit BFS |
| `prep_bfs.py` | scratch search (fixed seed) that found the 2-generator word, plus transform benchmark |
| `task3_orbits.py` | BFS all 17 PGL orbits; records sizes, disjointness, φ-images → `orbits_output.json` |
| `task3b_pgammal_bfs.py` | direct PΓL BFS on the maximal 6-cap triple (2,060,352) |
| `cap_census.c`, `cap_census.exe` | independent DFS census of all caps and maximal caps |
| `census_output.txt` | saved census output |
| `orbits_output.json` | saved orbit sizes/memberships |
| `task45_analysis.py` | Tasks 4–5 arithmetic, divisibility, totals |
| `run_all.py` | runs everything end-to-end (compiles the C census) |

Run all checks from this directory:

```text
python run_all.py
```

Individual commands (in the order used):

```text
python common.py
python group.py
python task1_board.py
python reps.py
python task2_group.py
python bfs.py
python task3_orbits.py          # ~2-3 min; writes orbits_output.json
python task3b_pgammal_bfs.py    # ~20-25 s
gcc -O2 -o cap_census.exe cap_census.c
./cap_census.exe ../output/board_pg2q8.txt | tee census_output.txt   # ~0.75 s
python task45_analysis.py
```

---

## 3. Task 1 — board, GF(8), the explicit sets, Frobenius

Board interpretation re-derived from the definition, not from any other
artefact: elements `0..7` of GF(8) are bit vectors with `x³+x+1=0`; points are
canonical nonzero vectors (first nonzero coordinate 1), sorted lexicographically.

```text
$ python task1_board.py
lines read: 73  each of size [9]
lines generated from GF(8) 2-D subspaces: 73
board == generated line set: True
point pairs: 2628 each on exactly one line
any two distinct lines meet in exactly one point: True
GF(8) elements 0..7, x^3+x+1=0; x*x = 4  x^3 = 3
first 11 canonical points (abridged): [(0,(0,0,1)), (1,(0,1,0)), ..., (8,(0,1,7)), (9,(1,0,0)), (10,(1,0,1))]
phi is a permutation: True
phi^3 == id: True
phi != id: True
phi maps every line to a line (collineation): True
C6        = [2, 3, 10, 16, 18, 21]  cap=True
phi(C6)   = [2, 5, 10, 12, 18, 23]  cap=True
D6        = [1, 10, 12, 59, 62, 65]  cap=True
phi(D6)   = [1, 10, 14, 29, 32, 33]  cap=True
unique conic through C6 has points: [2, 3, 10, 16, 18, 21, 29, 47, 48]
C6 subset of that conic: True
D6 lies on a conic: False
C6 addable points: 4
D6 addable points: 4
TASK 1 CHECKS PASSED
```

Findings:

* The 74-line board file is exactly the projective plane built from
  GF(2)[x]/(x³+x+1): 73 points, 73 lines, 9 points per line, every point pair
  on exactly one line, every two lines meeting in one point.
* `{2,3,10,16,18,21}` and `{1,10,12,59,62,65}`, and both φ-images, are caps.
* φ is a permutation of the 73 points with φ³ = id (φ² = φ⁻¹), φ ≠ id, and φ is
  a collineation (it maps every board line to a board line).
* C6 is a 6-subset of the unique conic
  `{2,3,10,16,18,21,29,47,48}`; D6 is not contained in any conic. Both are
  non-maximal (each has 4 addable points). These facts identify the two orbit
  labels used in Task 3.

---

## 4. Task 2 — PGL(3,8) and PΓL(3,8)

Generators (elementary transvections, all determinant 1):

```text
E12(1), E23(1), E13(1), E21(1), E31(1), E32(1), E12(x), E12(x^2)
```

with indices 0-based and `x=2`, `x²=4` in GF(8). Each is converted to its
permutation of the 73 points.

```text
$ python task2_group.py
det=1 and nontrivial for all 8 generators
Schreier-Sims passes: 9
base: [1, 0, 9, 2, 10]
level sizes: [8, 3, 3, 1, 1]
orbit sizes: [73, 72, 64, 7, 7]
order: 16482816
computed |<gens>| = 16482816
|GL(3,8)| = (8^3-1)(8^3-8)(8^3-8^2) = 115379712
scalars in GL: 7; |GL|/7 = 16482816
ordered projective frames: 16482816
phi E_ij phi^-1 == matrix^2 action: True for all 8 generators
phi member of <gens>: False
diagonal matrix inducing phi: None
computed |<PGL,phi>| = 49448448
ALL TASK-2 CHECKS PASSED
```

Method and cross-checks:

* The group order is computed by a from-scratch deterministic Schreier–Sims
  implementation (`group.py`, self-tested on C5, S3, D8, A4, S4, S5, AGL(1,7)
  against brute force).  The chain gives
  `73·72·64·7·7 = 16,482,816`.
* Independent order derivations agree: `|GL(3,8)|/7 = 115,379,712/7`, and the
  number of ordered projective frames is `73·72·64·49 = 16,482,816` (a
  non-collinear triple leaves 24 points on its three lines, hence 49 choices
  for the fourth frame point).
* φ normalises PGL: for every generator `g` with matrix `M`, the permutation
  `φ g φ⁻¹` equals the action of the entrywise-squared matrix `M^(2)`; this is
  a linear map, hence in PGL.  (Since the generators generate PGL, this
  normalises all of PGL.)
* φ ∉ PGL, two ways: (i) BSGS membership test returns False; (ii) φ fixes the
  three basis points projectively, so any inducing matrix would be diagonal —
  all 343 diagonal matrices were tested and none induces φ.  φ moves point 25
  `(1,x,0)` to point 41 `(1,x²,0)`.
* φ³ = id and φ ∉ PGL give three distinct cosets, hence
  `|<PGL,φ>| = 3·16,482,816 = 49,448,448`; the Schreier–Sims computation
  gives exactly this order.  Thus `PΓL(3,8) = PGL(3,8) ⋊ C3`.

---

## 5. Task 3 — orbit BFS for the two 6-caps (and all PGL orbits)

### 5.1 Two-generator set used for the BFS

To keep the BFS cheap, a 2-generator subset of the 8 generators was found and
verified (not assumed):

* `g1 = E12(1)` (index 0);
* `g2` = product of the 8 generators with index word `[0,5,7,3,0,6,2,7]`,
  composed as `p ← gens[i]·p`.

Schreier–Sims gives `|<g1,g2>| = 16,482,816 = |PGL(3,8)|`, and both generators
are products of determinant-1 elementary matrices, hence in PGL; therefore
`<g1,g2> = PGL(3,8)`.  Both generators were checked to be collineations
(every board line maps to a board line).  The cap-image kernel (10 byte
lookup tables OR-ed together) was checked against direct permutation action
on random caps.

### 5.2 The two required orbits

```text
$ python task3_orbits.py    (excerpt)
=== k6-conic (k=6) expected 2747136 ===
  orbit size 2747136 (expected 2747136)
  phi(rep) in orbit: True; phi^2(rep) in orbit: True
=== k6-nonmax-nonconic (k=6) expected 4120704 ===
  orbit size 4120704 (expected 4120704)
  phi(rep) in orbit: True; phi^2(rep) in orbit: True
```

Specifically:

* `orbit_PGL({2,3,10,16,18,21})` has size **2,747,136**, and
  `φ({2,3,10,16,18,21}) = {2,5,10,12,18,23}` is a member of it.  (The orbit
  contains the 6-subset of the conic `{2,3,10,16,18,21,29,47,48}`.)
* `orbit_PGL({1,10,12,59,62,65})` has size **4,120,704**, and
  `φ({1,10,12,59,62,65}) = {1,10,14,29,32,33}` is a member of it.  D6 is
  non-conic and non-maximal.

### 5.3 Full PGL orbit table (independent re-enumeration)

Every representative was BFS-enumerated; all 17 orbits are pairwise disjoint
(`memberships` in `orbits_output.json` are true exactly for the orbit itself)
and reproduce K1327 exactly:

| k | representative | PGL orbit size | φ-stable? |
|---:|---|---:|---|
| 1 | `{2}` | 73 | yes |
| 2 | `{2,3}` | 2,628 | yes |
| 3 | `{2,3,10}` | 56,064 | yes |
| 4 | `{2,3,10,16}` | 686,784 | yes |
| 5 | `{2,3,10,16,18}` | 4,120,704 | yes |
| 6 | C6 = `{2,3,10,16,18,21}` (conic) | 2,747,136 | yes |
| 6 | D6 = `{1,10,12,59,62,65}` (non-max non-conic) | 4,120,704 | yes |
| 6 | A = `{10,47,49,55,61,64}` (maximal) | 686,784 | no: A→C |
| 6 | B = `{17,27,30,44,52,70}` (maximal) | 686,784 | no: B→A |
| 6 | C = `{8,48,50,51,58,61}` (maximal) | 686,784 | no: C→B |
| 7 | first 7 conic points (conic) | 1,177,344 | yes |
| 7 | `{12,16,18,22,54,66,69}` (non-conic) | 2,747,136 | yes |
| 8 | first 8 conic points (conic) | 294,336 | yes |
| 8 | `{12,16,18,22,40,54,66,69}` (non-conic) | 1,177,344 | yes |
| 9 | the 9 conic points (conic) | 32,704 | yes |
| 9 | `{2,3,10,12,21,45,47,50,52}` (non-conic) | 294,336 | yes |
| 10 | `{2,3,10,16,18,21,29,31,47,48}` (hyperoval = conic + nucleus 31) | 32,704 | yes |

For the maximal triple the BFS membership probes show exactly the K1329 cycle

```text
phi(A) in orbit(C): True    phi(C) in orbit(B): True    phi(B) in orbit(A): True
phi(A) not in orbit(A),     phi(B) not in orbit(B),     phi(C) not in orbit(C)
```

A direct PΓL BFS (`task3b_pgammal_bfs.py`, generators g1,g2,φ) from A gives
size **2,060,352 = 3·686,784** and contains A, B, C, φ(A), φ²(A), confirming
that the maximal triple is one PΓL orbit.

Coverage/completeness:

* Per-k sums of the 17 enumerated orbits equal the independent C census for
  every k = 1..10 (`task45_analysis.py`), e.g. k=6 sum 8,928,192, k=7 sum
  3,924,480, k=8 sum 1,471,680, k=9 sum 327,040.
* Total of the 17 non-empty PGL orbits = 19,550,349 = census non-empty count.
  Hence the 17 orbits cover all caps: there is no additional PGL orbit.

---

## 6. Task 4 — divisibility

`|PΓL(3,8)| = 49,448,448 = 3·16,482,816`.

### 6.1 Proposed PΓL orbit sizes

| k | PΓL orbit | size | \|PΓL\|/size |
|---:|---|---:|---:|
| 1 | single | 73 | 677,376 |
| 2 | single | 2,628 | 18,816 |
| 3 | single | 56,064 | 882 |
| 4 | single | 686,784 | 72 |
| 5 | single | 4,120,704 | 12 |
| 6 | conic | 2,747,136 | 18 |
| 6 | non-max non-conic | 4,120,704 | 12 |
| 6 | maximal (3 PGL orbits fused) | 2,060,352 | 24 |
| 7 | conic | 1,177,344 | 42 |
| 7 | non-conic | 2,747,136 | 18 |
| 8 | conic | 294,336 | 168 |
| 8 | non-conic | 1,177,344 | 42 |
| 9 | conic | 32,704 | 1,512 |
| 9 | non-conic | 294,336 | 168 |
| 10 | single | 32,704 | 1,512 |
| — | empty cap | 1 | 49,448,448 |

Every quotient is an integer (remainders 0).  Sum of the 15 non-empty sizes:
19,550,349.

### 6.2 The four quoted pairwise sums

| pair | sum | \|PΓL\| division |
|---|---:|---|
| k=6 conic + non-max non-conic | 6,867,840 | 7·6,867,840 + 1,373,568 → not divisible |
| k=7 conic + non-conic | 3,924,480 | 12·3,924,480 + 2,354,688 → not divisible |
| k=8 conic + non-conic | 1,471,680 | 33·1,471,680 + 883,008 → not divisible |
| k=9 conic + non-conic | 327,040 | 151·327,040 + 65,408 → not divisible |

All four are multiples of 5 while `|PΓL| = 2⁹·3³·7²·73` has no factor 5, so the
non-divisibility is immediate.

---

## 7. Task 5 — total count, and notes/discrepancies

### 7.1 Independent cap census

`cap_census.c` enumerates every cap exactly once by increasing point order,
maintains the forbidden-point mask, and counts maximal caps.  It reads only the
board file.  Output (`census_output.txt`):

```text
caps k= 0 : 1   maximal: 0
caps k= 1 : 73   maximal: 0
caps k= 2 : 2628   maximal: 0
caps k= 3 : 56064   maximal: 0
caps k= 4 : 686784   maximal: 0
caps k= 5 : 4120704   maximal: 0
caps k= 6 : 8928192   maximal: 2060352
caps k= 7 : 3924480   maximal: 0
caps k= 8 : 1471680   maximal: 0
caps k= 9 : 327040   maximal: 0
caps k=10 : 32704   maximal: 32704
TOTAL (including empty) = 19550350
TOTAL non-empty = 19550349
```

This matches K1300's census exactly and is independent of the orbit BFS.

### 7.2 Counts

* PGL: 17 non-empty orbits, sizes summing to 19,550,349; plus the empty cap
  (an orbit of size 1) gives **18 orbits** and 19,550,350 caps.
* PΓL: 15 non-empty orbits, sizes summing to 19,550,349; plus the empty cap
  gives **16 orbits** and 19,550,350 caps.

The arithmetic of Task 5 is therefore verified: non-empty total 19,550,349;
including the empty cap 19,550,350.  The 15 vs 16 count is the only wording
issue (see below).

### 7.3 Discrepancies / notes

1. **"15 orbits including the empty cap" is off by one in the task statement.**
   K1330's 15 PΓL cap orbits are the non-empty ones (k=1..10); the empty cap
   is an additional fixed orbit.  Thus there are 15 non-empty PΓL orbits
   (sum 19,550,349) and **16 including the empty cap** (sum 19,550,350).
   The same convention is used for PGL in K1327 (17 non-empty, 18 including
   empty).  The mathematical content of K1330 is unaffected.
2. **The divisibility sentence in K1330 is not a complete exclusion argument
   for k=6.**  The listed four pairwise sums indeed do not divide
   `|PΓL|`, but not every "remaining union" is a pairwise sum.  In particular
   `non-max non-conic + maximal triple = 6,181,056 = |PΓL|/8` *does* divide
   `|PΓL|`, and the union of two maximal PGL orbits
   `2·686,784 = 1,373,568 = |PΓL|/36` also divides.  The actual exclusion of
   these unions is the verified φ-stability: the conic and non-max 6-orbits
   are individually φ-stable (BFS membership of their φ-images), and the three
   maximal orbits are a single φ-3-cycle.  Hence the conclusion "only the
   three maximal 6-cap orbits fuse" is correct, but the stated reason
   ("pairwise sums do not divide") is incomplete as a standalone proof.
   This is a justification gap, not a numerical error.
3. No numerical discrepancy with K1327/K1329/K1330 was found: all 17 PGL orbit
   sizes, the three maximal-orbit sizes (686,784 each), the PΓL fusion size
   2,060,352, the two required φ-image memberships, and the four listed
   pairwise non-divisibilities all reproduce exactly.

---

## 8. Independence notes

* The board was re-derived from the GF(8) definition and compared as a set of
  lines; no other construction data was used.
* The group order comes from an independent Schreier–Sims implementation
  (self-tested against brute force on seven small groups), with two further
  order derivations (|GL| formula and ordered-frame count).
* The cap census is an independent C DFS over the pointed hypergraph.
* The orbit enumeration uses a verified 2-generator set and a 73-bit-mask BFS;
  orbit sizes are checked against K1327 and against the independent census.
* The claim text (K1330 and the supplied statement) was used only as the list
  of statements to verify; no existing `independent_*` implementation or
  output was read or reused.
