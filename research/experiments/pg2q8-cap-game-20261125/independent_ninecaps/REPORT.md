# Independent verification of K1326 — the 9-caps of PG(2,8)

Independent re-computation written from scratch in this directory on 2026-11-26.
Only files under `independent_ninecaps/` were created; **no git commit**, no file
outside this directory was modified. Python 3.12.13, standard library only; the
existing C census of `../independent_orbits/` was **not** used (it was only read
afterwards, as external corroboration — see §7).

Board under test: `../output/board_pg2q8.txt`
sha256 `E3FDAD754BDF4D42DE7BBFA076768F18A6FC141D48F42435CCF7EABFC93F6ADB`.

## 0. Verdict

| Task | Claim under test | Verdict |
|---|---|---|
| 1 | board is PG(2,8); `{2,3,10,12,21,45,47,50,52}` is a 9-cap | **PASS** |
| 2 | the example is not a conic; 32,704 = 8⁵−8² conics, each a 9-cap | **PASS** |
| 3 | \|PGL(3,8)\| = 16,482,816, action by collineations, example orbit 294,336 | **PASS** |
| 4 | exactly 327,040 9-caps; every 9-cap is a conic or in that orbit | **PASS** |
| 5 | three maximal 6-caps have distribution {1:36, 2:24, 3:7}; none in a hyperoval | **PASS** |

No discrepancy was found in claim K1326. All numbers of the claim are
reproduced: 327,040 = 32,704 (conics, one orbit, stabilizer 504) + 294,336
(non-conics, one orbit, stabilizer 56). Section §6 lists observations that are
worth recording but do not contradict the claim.

## 1. Artefacts and commands

```
cd research/experiments/pg2q8-cap-game-20261125/independent_ninecaps

python selftest.py          # validates field, geometry and Schreier machinery
python check_board.py       # task 1
python check_conic.py       # task 2  (writes artifacts/conics.txt)
python check_group.py       # task 3  (writes orbit pickles)
python census.py 10         # task 4  (writes artifacts/caps.pkl)
python check_ninecaps.py    # task 4  (census vs conics vs orbit)
python check_sixcaps.py     # task 5
python check_hyperovals.py  # extra structural check
```

| file | role |
|---|---|
| `pg8.py` | GF(8)=GF(2)[x]/(x³+x+1), canonical points, lines, board loader and intrinsic plane checks, 73-bit incidence structure |
| `group.py` | explicit matrices, induced point permutations, mask-orbit BFS |
| `selftest.py` | field axioms, geometry axioms, Schreier-chain order vs brute force |
| `check_board.py` | task 1 |
| `check_conic.py` | task 2 (all 37,449 projective quadratic forms) |
| `check_group.py` | task 3 (Schreier chain, transvection certificate, cap orbits) |
| `census.py` | task 4 (full cap census by DFS, sizes 1…10) |
| `check_ninecaps.py` | task 4 (census = conics ⊔ non-conic orbit) |
| `check_sixcaps.py` | task 5 (three maximal 6-caps, distributions, orbits, hyperoval test) |
| `check_hyperovals.py` | extra (conic → hyperoval bijection) |
| `artifacts/*.json`, `artifacts/*.log` | machine-readable results and raw logs |

Measured runtimes: census ≈38–40 s, 6-cap orbits ≈36 s, group ≈14 s,
`check_ninecaps` 1.7 s, board 0.3 s, hyperoval check 1.6 s.  A clean sequential
rerun of exactly the commands above from an empty `artifacts/` directory exited
0 for every step; per-step logs are `artifacts/log_*.txt`, the summary is
`artifacts/clean_run_master.log`.

## 2. Board and geometry (task 1, prerequisite)

`check_board.py` output:

```
header [73, 73]; 73 lines; all lines size 9; all lines distinct sets/points
pairs covered 2628 = C(73,2); every pair exactly once; point degrees [9]
matches_coordinate_PG28: True; lines only in board 0; lines only in geo 0
```

* The board was rebuilt from the field alone: points = canonical nonzero
  vectors of GF(8)³ (first nonzero coordinate scaled to 1) **sorted
  lexicographically**, indices 0…72; lines = 2-dimensional subspaces. The
  resulting 73 line sets are **identical** to the board's line sets (not merely
  isomorphic), which confirms the stated index convention (in particular
  `0 = (0,0,1)`, `1…8 = (0,1,c)`, `9+8y+z = (1,y,z)`) instead of assuming it.
* Intrinsically the board is a projective plane of order 8: 73 points, 73
  lines, 9 points per line, 9 lines per point, every pair on exactly one line.
* The example `S = {2,3,10,12,21,45,47,50,52}` has 9 distinct points and is a
  cap: all 36 point pairs were checked and none contains a third point of S.
  Coordinates: `2=(0,1,1) 3=(0,1,2) 10=(1,0,1) 12=(1,0,3) 21=(1,1,4)
  45=(1,4,4) 47=(1,4,6) 50=(1,5,1) 52=(1,5,3)`.
* `S` has exactly one point (23) on no secant; `S ∪ {23}` is therefore a
  10-cap. (This is not in conflict with the claim; see §6.)

## 3. The example is not a conic (task 2)

Homogeneous quadratic forms in characteristic 2, cross terms taken **once**:

```
Q(x,y,z) = a x² + b y² + c z² + d·xy + e·xz + f·yz      (6 coefficients)
```

Evaluation at the 9 points gives a 9×6 matrix over GF(8) whose rows are
`(x², y², z², xy, xz, yz)`. Gaussian elimination over GF(8) gives

```
rank = 6, kernel dimension = 0
```

so the only quadratic form vanishing on all nine points is the zero form: `S`
lies on no conic (degenerate or not). Since a 9-arc spans the plane, this is a
genuine non-conic 9-cap. (`check_conic.py`, printed rank 6 / kernel 0.)

Conics were then counted from scratch by enumerating **all** 37,449 projective
quadratic forms `(8⁶−1)/7`:

| zero-set size | forms | interpretation |
|---:|---:|---|
| 1 | 2,044 | degenerate forms with a single rational point |
| 9 | 32,777 | 32,704 conics + 73 squared lines (`L²`, non-cap) |
| 17 | 2,628 | pairs of distinct lines = C(73,2) |

* forms whose zero set is a 9-**cap**: **32,704 = 8⁵ − 8²** (exact);
* distinct zero sets among them: **32,704**, multiplicity per conic = 1
  (each conic has a unique defining quadratic form);
* every conic is a 9-cap (checked for all 32,704);
* the 73 nine-point non-cap zero sets are exactly the lines.

## 4. PGL(3,8) and the example orbit (task 3)

Own generators (row-vector action `v ↦ vM`, matrices over GF(8)):

| generator | map | order | det |
|---|---|---|---|
| `P` | (a,b,c) → (b,c,a) | 3 | 1 |
| `S12` | (a,b,c) → (a+b,b,c) | 2 | 1 |
| `S23` | (a,b,c) → (a,b+c,c) | 2 | 1 |
| `S13` | (a,b,c) → (a+c,b,c) | 2 | 1 |
| `D` | (a,b,c) → (a,2b,c) | 7 | 2 |

* All five determinants are non-zero and all five induced permutations are
  **collineations**: 5 × 73 = 365 line images, each a member of the board line
  set.
* **Exact group order by a Schreier stabilizer chain** (Schreier's lemma; base
  `9, 1, 17, 0, 10`, i.e. `[1,0,0],[0,1,0],[1,1,0],[0,0,1],[1,0,1]`):

  ```
  orbit sizes:      73, 72, 7, 64, 7
  stabilizer gens:  5, 113, 2696, 447, 6
  final stabilizer generators all identity
  order = 16,482,816
  ```

  The product `73·72·7·64·7 = 16,482,816` equals
  `|PGL(3,8)| = (8³−1)(8³−8)(8³−8²)/7 = 511·504·448/7 = 16,482,816`,
  and a second chain with base `0,9,10,1,17` gives the same order.
* Second, independent certificate: conjugating the transvection `S12` by the
  generators yields **4,599 = 73·9·7** distinct matrices, all of determinant 1,
  all involutory elations with exactly 9 fixed points (i.e. exactly the
  transvections of SL(3,8), whose number is 73·9·7). Hence the generated matrix
  group contains all transvections, so contains SL(3,8). Its projective image
  therefore contains PSL(3,8); scalar matrices in SL(3,8) are trivial because
  λ³ = 1 and gcd(3,7) = 1 force λ = 1, so |PSL(3,8)| = |SL(3,8)| =
  16,482,816 = |PGL(3,8)|, hence PSL(3,8) = PGL(3,8). (The subgroup generated
  by the 5 matrices is a subgroup of GL(3,8); its projective image is exactly
  the permutation group on the 73 points.)
* **Orbit of the example 9-cap: 294,336** (BFS over 73-bit masks, 8.2 s).
  Orbit–stabilizer: `16,482,816 / 294,336 = 56` exactly.
* **Orbit of a conic: 32,704**; stabilizer `16,482,816 / 32,704 = 504`.
* `294,336 = 327,040 − 32,704` exactly.

## 5. Independent census and orbit split (task 4)

Own DFS census (each cap generated once, incidence taken from the board file
only), runtime ≈38–40 s:

| size | caps | decomposition |
|---:|---:|---|
| 1 | 73 | |
| 2 | 2,628 | C(73,2) |
| 3 | 56,064 | |
| 4 | 686,784 | = 32,704 · C(9,4)/6 |
| 5 | 4,120,704 | = 32,704 · C(9,5) |
| 6 | 8,928,192 | 2,747,136 on a conic + 6,181,056 not |
| 7 | 3,924,480 | 1,177,344 on a conic + 2,747,136 not |
| 8 | 1,471,680 | 294,336 on a conic + 1,177,344 not |
| **9** | **327,040** | 32,704 conics + **294,336** non-conics |
| 10 | 32,704 | all hyperovals |
| total | 19,550,349 (+ empty set) | 2,060,352 maximal 6-caps |

The 4/5-cap entries check the conic count independently:
`32,704·C(9,4)/6 = 686,784` (a 4-arc lies on 6 non-singular conics of its
pencil) and `32,704·C(9,5) = 4,120,704`.

Set comparison (`check_ninecaps.py`):

```
census 9-caps            327,040 distinct
conics from forms         32,704  ⊆ census 9-caps
example orbit            294,336  ⊆ census 9-caps
conic set ∩ example orbit      ∅
32,704 + 294,336 = 327,040
(conic set ∪ example orbit) == census 9-caps : True
conics == orbit of one conic (single conic orbit) : True
```

Therefore **every 9-cap of PG(2,8) is either a conic or in the example's
orbit**, and the two PGL(3,8) orbits have sizes 32,704 and 294,336. No 9-cap is
outside the two orbits.

Additional structural fact (extra check, 1.6 s): the 32,704 ten-caps are
exactly `conic ∪ {nucleus}`; each conic has exactly one point on no secant,
giving a bijection conics ↔ 10-caps, and the 10 nine-subsets of the 32,704
ten-caps are 327,040 distinct 9-caps = all 9-caps, each occurring exactly once.
Consequently the 294,336 non-conic 9-caps are exactly “a hyperoval minus one of
its conic points”: `32,704 × 9 = 294,336`.

## 6. The three maximal 6-caps (task 5)

Representatives `R1={10,47,49,55,61,64}`, `R2={17,27,30,44,52,70}`,
`R3={8,48,50,51,58,61}`:

| rep | cap | maximal (blocked∪cap = all 73) | secant lines | outside points on 0 secants | distribution |
|---|---|---|---|---|---|
| R1 | yes | yes | 15 | 0 | {1:36, 2:24, 3:7} |
| R2 | yes | yes | 15 | 0 | {1:36, 2:24, 3:7} |
| R3 | yes | yes | 15 | 0 | {1:36, 2:24, 3:7} |

The distribution is self-consistent: `36+24+7 = 67 = 73−6` outside points and
`36·1+24·2+7·3 = 105 = 15·7` incidences. All three classes therefore have the
same outside-point secant-count distribution — it does not separate them.

`PGL(3,8)`-orbits (BFS, 36 s total):

```
|orbit(R1)| = |orbit(R2)| = |orbit(R3)| = 686,784
pairwise disjoint, union = 2,060,352 = census count of all maximal 6-caps
```

so these are exactly the three maximal 6-cap classes, with stabilizer
`16,482,816 / 686,784 = 24` each. A random sample of 300 members of each orbit
was re-checked to be a cap and maximal (300/300 per orbit).

**Hyperoval containment:** for each representative, the number of 10-caps
containing it is **0**. Since containment in a cap is collineation-invariant
and the three orbits cover *all* maximal 6-caps, no maximal 6-cap is contained
in a hyperoval. (This also follows directly from maximality: a hyperoval is a
cap of size 10, so it would be an extension of the maximal 6-cap.)

## 7. Cross-check with the pre-existing C census (external, read-only)

After completing the Python census above, `../independent_orbits/logs/census_c.log`
was read for comparison. Its counts are identical:

```
size 4: 686784   size 5: 4120704   size 6: 8928192 (maximal 2060352)
size 7: 3924480  size 8: 1471680   size 9: 327040   size 10: 32704
total 19550350 (including empty cap), maximal 2093056
```

This is corroboration only; none of the computations in this report use that
program or its output.

## 8. Self-validation of the verifier

`selftest.py` passes: full field axioms for GF(8) (`x³=x+1`, commutativity,
associativity, distributivity, inverses), the geometry rebuilt from the field
(73 distinct lines of 9 points), the Schreier-chain order against brute-force
closures — S3=6, C7=7, S4=24, D8=8, A5=60 and 5 random subgroups of S7 (brute
force enumeration) — and the permutation compose/inverse helpers. So the
group-order and orbit machinery is validated independently of PG(2,8).

## 9. Discrepancies and observations

1. **No discrepancy** between the computed results and claim K1326: all
   counts, orbit sizes, stabilizer orders and the non-conic example match.
2. Observations (not contradictions):
   * every 9-cap, conic or not, lies in a **unique** 10-cap (the 9-subsets of
     the 32,704 hyperovals are all 327,040 9-caps, each once); in particular
     the example 9-cap extends by point 23;
   * consequently non-conic 9-caps are not maximal, and their count is
     structurally `9 · 32,704 = 294,336`;
   * the statement “no maximal 6-cap is contained in a hyperoval” is automatic
     from maximality (a hyperoval is a larger cap), and was also confirmed
     computationally;
   * the transvection certificate uses the full conjugacy class of elations
     (73·9·7 = 4,599), not the 42 elementary transvections of a fixed basis.
3. No files outside `independent_ninecaps/` were created or modified and no
   commit was made. (`git status` shows unrelated pre-existing worktree
   changes in other directories; they were not touched by this verification.)
