# Independent verification — PG(2,8) / AG(2,8) s=2 cap game

**Directory:** `research/experiments/pg2q8-cap-game-20261125/independent/`
**Date:** 2026-11-25
**Role:** independent verifier. Nothing outside `independent/` was modified and
nothing was committed. Python standard library only + locally compiled C.

**Environment:** Windows, AMD Ryzen 7 5800HS; `gcc.exe (Rev8, MSYS2) 15.2.0`
(`-O2 -std=c99`); Python 3.12.13.

## Verdict

| Task | Subject | Verdict |
|---|---|---|
| 1 | Board axioms (PG/AG) + PG board vs own GF(8) construction up to relabelling | **PASS** |
| 2 | Enumeration of all caps, size distributions, totals | **PASS** |
| 3 | Maximal-cap counts, two independent maximality tests | **PASS** |
| 4 | Parity theorem application, p = 0, Grundy distribution, misère | **PASS** |
| 5 | Spot checks (50 random caps per requested class) | **PASS** |

**Discrepancies: none.** Every claimed number was reproduced exactly by three
independent implementations, and all internal consistency identities hold.

## Files

| File | Meaning |
|---|---|
| `verify_boards.py`, `board_verification.log` | board parsing, axioms, GF(8) construction, explicit relabellings |
| `cap_census.c`, `cap_census.exe` | main census: incremental blocked array (test 1) + recomputed secant union (test 2) + reservoir sampling |
| `census_pg_main.log`, `census_ag_main.log` | its output (size table, maximal counts, maximality-test disagreement counter, ADDHIST, samples) |
| `cap_census_alt.c`, `cap_census_alt.exe` | second census: candidate-bitmask recursion, no blocked array |
| `census_pg_alt.log`, `census_ag_alt.log` | its output |
| `python_census.py`, `python_census_pg.log`, `python_census_ag.log` | third, pure-Python census |
| `test_small.py`, `test_small.log` | validation of both C programs against exhaustive brute force on PG(2,3)/AG(2,3) |
| `verify_samples.py`, `verify_samples.log` | independent re-check of every sampled cap |
| `verify_grundy.py`, `verify_grundy.log` | parity/Grundy/misère checks and direct game recursion |
| `verify_identities.py`, `verify_identities.log` | cross-census comparison + extension/containment identities |

## Commands

```sh
gcc -O2 -std=c99 -o cap_census.exe cap_census.c
gcc -O2 -std=c99 -o cap_census_alt.exe cap_census_alt.c
./cap_census.exe     ../output/board_pg2q8.txt 12345 > census_pg_main.log
./cap_census.exe     ../output/board_ag2q8.txt 12345 > census_ag_main.log
./cap_census_alt.exe ../output/board_pg2q8.txt       > census_pg_alt.log
./cap_census_alt.exe ../output/board_ag2q8.txt       > census_ag_alt.log
python python_census.py ../output/board_pg2q8.txt 12 > python_census_pg.log
python python_census.py ../output/board_ag2q8.txt 12 > python_census_ag.log
python verify_boards.py     > board_verification.log
python test_small.py        > test_small.log
python verify_samples.py    > verify_samples.log
python verify_grundy.py     > verify_grundy.log
python verify_identities.py > verify_identities.log
```

(The C programs take the board path and an optional RNG seed; the RNG seed
actually used is printed as `RNGSEED` in the logs.)

---

## Task 1 — boards (PASS)

`board_pg2q8.txt`: 73 points, 73 lines of 9. `board_ag2q8.txt`: 64 points,
72 lines of 8. Both parse exactly as declared.

### PG(2,8) axioms (all PASS)

* 73 lines, all of size 9, all distinct, all 73 points used.
* every point lies on exactly 9 lines;
* every point pair lies on exactly **one** line (all C(73,2)=2628 pairs checked);
* every line pair meets in exactly **one** point (all C(73,2)=2628 pairs checked).

### AG(2,8) axioms (all PASS)

* 72 lines, all of size 8, all distinct, all 64 points used;
* every point on exactly 9 lines; every point pair on exactly one line (2016 pairs);
* disjointness classes of lines: exactly **9** classes, each of **8** pairwise
  disjoint lines, each class partitions the point set into 8 blocks of 8.
  (Since two lines are parallel iff disjoint in an affine plane, these are the
  9 parallel classes.)

### PG(2,8) board vs my own GF(8) construction (PASS)

Rebuilt from scratch with `GF(8) = GF(2)[α]/(α³+α+1)` (α = x, elements as 3-bit
vectors; `α³ = α+1`; field axioms, distributivity, α of order 7 and existence of
inverses all self-tested):

* points = 73 one-dimensional subspaces of GF(8)³,
* lines = 73 two-dimensional subspaces (= kernels of non-zero linear functionals),
  each with 9 points.

The constructed plane was itself re-checked against the projective-plane axioms.
Then an explicit point bijection `phi` was searched with constraint propagation
(lines with two mapped points force the image line; MRV branching) starting from
a board quadrangle `(0, 1, 9, 18)` mapped to the standard frame
`[1:0:0], [0:1:0], [0:0:1], [1:1:1]`. 3 search nodes; the resulting `phi` maps
**all 73 board lines onto the 73 constructed lines** (checked exhaustively both
directions; `phi` is a bijection). So the board's line set agrees with the
GF(8)-built line set **up to relabelling**. `phi` is recorded in
`board_verification.log` and in the appendix.

### AG(2,8) board vs GF(8)² (extra, PASS)

Same technique with the affine frame `(O, X, Y, X+Y)` mapped to
`(0,0), (1,0), (0,1), (1,1)` of GF(8)²; 2 search nodes; all 72 board lines map
onto the 72 constructed lines. The witness is the clean transpose
`board point 8x+y  ↦  (y, x)`, i.e. id `8x+y ↦ 8y+x` (see appendix).

---

## Task 2 — full cap census (PASS)

Three independent enumerations of **all** caps (positions with ≤ 2 points on
every line), each cap visited exactly once by increasing-point DFS:

1. `cap_census.c` — incremental *blocked-pair counter*: `pc[q]` = number of
   secant pairs of the current cap whose line contains `q`; `q` is addable iff
   `pc[q] == 0`. Backtracking restores `pc` exactly.
2. `cap_census_alt.c` — the addable set is carried down the recursion as a
   73-bit candidate mask; appending `p` removes `p` and all points on
   `line(a,p)` for `a` in the cap. No counter array at all.
3. `python_census.py` — same idea as (2) rewritten from scratch in Python with
   arbitrary-precision integer masks, sharing no code or data structure with (1).

The C core was validated on small planes against **exhaustive brute force over
all 2^n subsets** (`test_small.py`):

| plane | brute-force sizes | brute-force maximal |
|---|---|---|
| PG(2,3), 13 pts | 1, 13, 78, 234, 234 (total 560) | size 4: 234 |
| AG(2,3), 9 pts | 1, 9, 36, 72, 54 (total 172) | size 4: 54 |

Both C programs match those numbers for every size and every maximal count.

### Results

PG(2,8) — all three programs identical, **total 19,550,350**:

| size | caps | maximal (test 1) | maximal (test 2) |
|---:|---:|---:|---:|
| 0 | 1 | 0 | 0 |
| 1 | 73 | 0 | 0 |
| 2 | 2,628 | 0 | 0 |
| 3 | 56,064 | 0 | 0 |
| 4 | 686,784 | 0 | 0 |
| 5 | 4,120,704 | 0 | 0 |
| 6 | 8,928,192 | **2,060,352** | **2,060,352** |
| 7 | 3,924,480 | 0 | 0 |
| 8 | 1,471,680 | 0 | 0 |
| 9 | 327,040 | 0 | 0 |
| 10 | 32,704 | **32,704** | **32,704** |

AG(2,8) — all three programs identical, **total 9,136,801**:

| size | caps | maximal (test 1) | maximal (test 2) |
|---:|---:|---:|---:|
| 0 | 1 | 0 | 0 |
| 1 | 64 | 0 | 0 |
| 2 | 2,016 | 0 | 0 |
| 3 | 37,632 | 0 | 0 |
| 4 | 404,544 | 0 | 0 |
| 5 | 2,145,024 | 0 | 0 |
| 6 | 4,158,336 | **959,616** | **959,616** |
| 7 | 1,666,560 | 0 | 0 |
| 8 | 584,640 | **20,160** | **20,160** |
| 9 | 125,440 | 0 | 0 |
| 10 | 12,544 | **12,544** | **12,544** |

These are exactly the claimed distributions and totals. Largest cap found: 10 in
both planes. Runtime: PG 7.5 s (main), 1.1 s (alt); AG 2.9 s (main), 0.5 s (alt).

---

## Task 3 — maximal-cap counts, two maximality tests (PASS)

For **every** cap node (all 28,687,151 caps over both boards) two structurally
different tests were evaluated:

* **Test 1 ("no addable point", blocked array).** `S` is maximal iff
  `zero_count == |S|`, where `zero_count` counts points `q` with `pc[q] == 0`;
  because `pc[a] == 0` for every `a` in a cap (a cap has no point on a secant),
  this is exactly "no addable point".
* **Test 2 (recomputed union of secants).** Recompute
  `U = ∪_{a<b∈S} line(a,b)` from scratch and test `(U ∪ S) == all points`.

The two tests disagreed on **0** of the 28,687,151 caps (`DISAGREE 0` in both
logs). The independent program `cap_census_alt.exe` (candidate-mask recursion,
maximal iff candidate mask is empty) reproduced the same maximal counts, and
so did the Python census.

Maximal counts reproduced exactly:
PG: 6 → 2,060,352; 10 → 32,704 (no maximal caps at any other size).
AG: 6 → 959,616; 8 → 20,160; 10 → 12,544 (no maximal caps at any other size).

### Additional consistency identities (all PASS)

`verify_identities.py` checks, for every size k:

* `Σ_a ADDHIST[k][a] = #caps(k)`;
* **extension-graph identity** `Σ_a a·ADDHIST[k][a] = (k+1)·#caps(k+1)`
  (edges of the one-point-extension graph counted from both ends);
* **containment identities**: every k-subset of a maximal m-cap is a k-cap, and
  the counts
  PG: `#caps(6) = max6 + max10·C(10,6)`, `#caps(7..9) = max10·C(10,k)`,
  AG: `#caps(6) = max6 + max8·C(8,6) + max10·C(10,6)`,
  `#caps(7) = max8·C(8,7) + max10·C(10,7)`, `#caps(8) = max8 + max10·C(10,8)`,
  `#caps(9) = max10·C(10,9)`, `#caps(10) = max10`
  hold **exactly** (to the unit).

The addable-count histograms are also informative:

* PG: every 7-cap has 3 addable points, every 8-cap has 2, every 9-cap has 1;
  every 6-cap has 0 (maximal) or 4 addable points.
* AG: 7-caps have 1 or 3, 8-caps have 0 or 2, 9-caps have 1; 6-caps have 0, 2 or 4.

---

## Task 4 — parity theorem, Grundy, misère (PASS)

1. **All maximal sizes are even in both boards** (6, 10; and 6, 8, 10). Hence
   `p = 0`.
2. With `p = 0` the parity theorem (K1298) gives
   `Grundy(S) = (p − |S|) mod 2 = (0 − |S|) mod 2 = |S| mod 2`.
   Self-contained induction: by (1) every maximal cap has even size, so every
   play starting from `S` has length ≡ `|S| (mod 2)`; hence every child `S'` of
   `S` has `Grundy(S') = (|S|+1) mod 2 = 1 − (|S| mod 2)` by induction, so
   `Grundy(S) = mex{1 − p} = p`; for a maximal `S` (even, no children) this is
   `Grundy = 0 = |S| mod 2`. In particular `Grundy(∅) = 0`.
3. **Grundy distribution = even/odd size totals** of my independent census:

| board | Grundy 0 (even) | Grundy 1 (odd) | claim |
|---|---:|---:|---|
| PG(2,8) | 11,121,989 | 8,428,361 | `{0: 11,121,989, 1: 8,428,361}` — MATCH |
| AG(2,8) | 5,162,081 | 3,974,720 | `{0: 5,162,081, 1: 3,974,720}` — MATCH |

   (PG even = 1+2,628+686,784+8,928,192+1,471,680+32,704; odd = 73+56,064+
   4,120,704+3,924,480+327,040; AG analogous. Even+odd equals the total.)
4. **Misère:** every maximal size is even, so every complete play from the empty
   position has even length; the second player makes the last move and, under
   last-move-loses, loses. Hence the first player wins, i.e. misère value 1 for
   the player to move.
5. **Direct verification of the conclusion (not just the hypothesis):** for all
   600 reservoir-sampled caps (PG 300, AG 300, sizes 6–10), the normal-play
   Grundy number was computed by full memoised game recursion and equals
   `|S| mod 2` in every case; the misère outcome equals "win iff `|S|` even" in
   every case.

---

## Task 5 — spot checks (PASS)

Reservoir sampling (Algorithm R, uniform over each class) inside the census DFS,
50 samples per class; every sample re-verified in pure Python with two
independent addability computations (direct per-point line scan vs. secant-union
mask). All 50/50 per class:

| board | class | samples | addable points per sample | result |
|---|---|---|---:|---|
| PG | 6-caps maximal (`PG6max`) | 50 | 0 every time | all maximal ✔ |
| PG | 6-caps non-maximal (`PG6non`) | 50 | 4 every time | all non-maximal ✔ |
| PG | 7-caps | 50 | 3 every time | all have addable point ✔ |
| PG | 8-caps | 50 | 2 every time | all have addable point ✔ |
| PG | 9-caps | 50 | 1 every time | all have addable point ✔ |
| PG | 10-caps maximal (`PG10max`, extra) | 50 | 0 | all maximal ✔ |
| AG | 6-caps maximal (`AG6max`) | 50 | 0 every time | all maximal ✔ |
| AG | 6-caps non-maximal (`AG6non`) | 50 | 4 (40 samples), 2 (10) | all non-maximal ✔ |
| AG | 7-caps | 50 | 1 (3), 3 (47) | all have addable point ✔ |
| AG | 8-caps maximal (`AG8max`, extra) | 50 | 0 | all maximal ✔ |
| AG | 8-caps non-maximal (`AG8non`, extra) | 50 | 2 | all non-maximal ✔ |
| AG | 9-caps | 50 | 1 every time | all have addable point ✔ |

Consequently there are **no complete arcs of sizes 7, 8, 9** in PG(2,8) and no
complete arcs of sizes 7, 9 (nor non-maximal 8-caps hidden as maximal) in
AG(2,8) — in line with the census giving maximal counts 0 at those sizes.
Every sample also satisfies the structural property `S ∪ {all addable points}`
is again a cap: for PG it is always a 10-cap; for AG it is an 8-cap or a 10-cap
(AG 6-/7-caps with 2 addable points complete to 8-caps, those with 4 to 10-caps).
This matches the containment identities of Task 3 exactly.

Example witnesses (from `verify_samples.log`): PG 9-cap `(17,20,35,41,42,51,56,58,60)`
has addable point 40; PG 8-cap `(1,6,14,33,35,53,55,58)` has addable point 16;
PG 7-cap `(2,7,37,52,53,67,70)` has addable point 19; AG 9-cap
`(2,3,37,39,42,43,55,57,61)` has addable point 49.

---

## Discrepancies / caveats

* **No discrepancies** were found: all claimed totals, size distributions,
  maximal counts and Grundy counts were reproduced exactly, and all three
  independent enumerations agree to the unit.
* External cross-check against the published arc tables of PG(2,8) could not be
  made: the web search tool returned HTTP 502 ("temporarily unavailable") on all
  attempts. The verification therefore rests on (i) the three independent
  enumerations, (ii) exhaustive brute-force validation of both C programs on
  PG(2,3)/AG(2,3), (iii) the exact extension/containment identities, and (iv)
  the board files being independently confirmed isomorphic to the GF(8)
  constructions. (For context only, the census implies the classical values:
  32,704 hyperovals = 10-arcs and 2,060,352 complete 6-arcs in PG(2,8),
  and 12,544 hyperovals / 20,160 maximal 8-arcs / 959,616 complete 6-arcs in
  AG(2,8).)
* The census takes the board files' line lists as its input; those line lists
  were verified independently in Task 1 (axioms + explicit isomorphism to the
  GF(8) model), so this is not a circular dependency.
* Nothing was committed; `git status` shows only new untracked files inside
  `independent/`.

---

## Appendix A — witnesses of the relabellings

PG(2,8), board point → constructed-model point id (`phi`):

```
[9, 1, 17, 33, 41, 49, 57, 65, 25, 0, 10, 12, 13, 14, 15, 16, 11, 2, 18, 36,
 45, 54, 63, 72, 27, 4, 58, 20, 53, 38, 31, 48, 67, 5, 66, 28, 21, 62, 47, 40,
 51, 6, 26, 60, 37, 22, 71, 56, 43, 7, 34, 52, 69, 46, 23, 32, 59, 8, 42, 68,
 61, 30, 55, 24, 35, 3, 50, 44, 29, 70, 39, 64, 19]
```

with model point ids from the lexicographically sorted normalised triples
(`(1,0,0)`↦9, `(0,1,0)`↦1, `(0,0,1)`↦0, `(1,1,1)`↦18, …). Example line images:

```
board line 0: 0..8           -> [1,9,17,25,33,41,49,57,65] = model line 0
board line 1: 0,9..16        -> [0,9,10,11,12,13,14,15,16] = model line 1
board line 2: 0,17..24       -> [2,9,18,27,36,45,54,63,72] = model line 2
```

AG(2,8), board point → constructed GF(8)² point id (`psi`), a pure transpose:

```
[0, 8, 16, 24, 32, 40, 48, 56, 1, 9, 17, 25, 33, 41, 49, 57, 2, 10, 18, 26,
 34, 42, 50, 58, 3, 11, 19, 27, 35, 43, 51, 59, 4, 12, 20, 28, 36, 44, 52, 60,
 5, 13, 21, 29, 37, 45, 53, 61, 6, 14, 22, 30, 38, 46, 54, 62, 7, 15, 23, 31,
 39, 47, 55, 63]
```

i.e. board id `8x+y` ↦ model id `8y+x`.

## Appendix B — reproduction notes

* Both C programs validate their input board before enumerating (line sizes,
  no pair on two lines, every pair on a line); they refuse malformed boards.
* The sample classes and both maximality tests are in `cap_census.c`; the
  histogram `ADDHIST k a count` gives the number of k-caps with exactly `a`
  addable points. For sizes 0–4 in PG the value is the full 73/72/64/49/30
  (not clamped), so the extension identity is exact for every size.
* All logs quoted above are in this directory; the numbers in this report are
  copied from them verbatim.
