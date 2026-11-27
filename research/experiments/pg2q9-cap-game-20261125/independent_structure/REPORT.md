# Independent verification of K1331: PG(2,9) cap decomposition

**Verdict: PASS on all five requested tasks. No discrepancy with the claim.**

- Date: 2026-11-26 (Asia/Tokyo)
- Working directory: `research/experiments/pg2q9-cap-game-20261125/independent_structure/`
- Environment: Python 3.12.13, standard library only.
- Nothing outside this directory was modified; no commit was made.

## Inputs (read-only)

| file | SHA-256 |
|---|---|
| `../output/board_pg2q9.txt` | `81C82D03B5094C3B3B4C912B8144B4CB119B2DB365B6790E0C844DFBF228486B` |
| `../output/census_pg2q9.txt` | `F65AB9964B8B1F259782AAD915FBF7A45EDBA22FDC0370EEEE6BDD114A5D75FE` |
| `../output/conic_layer.json` | `98FBA46242FBEE9C97063E310FE5F3529F0BFCF1A54657B6FA4F71ED5946D99D` |

## 1. Board verification and coordinate convention (Task 1a)

Command:

```sh
python research/experiments/pg2q9-cap-game-20261125/independent_structure/scripts/verify_board.py
```

Result:

```text
board: 91 points, 91 lines
PLANE_AXIOMS: PASS
candidate encodings tested: 48; exact line-set matches: 2
  MATCH M=(0, 1, 1, 0) diff 0
  MATCH M=(0, 2, 1, 0) diff 0
generated lines: 91; board lines: 91; EQUAL=True
```

Checked on the raw board: every line has 10 distinct points, every point lies on
10 lines, every pair of points lies on exactly one line, and every pair of lines
meets in exactly one point. Thus the incidence structure is a projective plane
of order 9.

The line family was then matched against the explicit model
`GF(9) = GF(3)[i]/(i^2+1)`, canonical vectors (first nonzero coordinate = 1),
sorted lexicographically by coordinate labels. Of the 48 additive bijections
`GF(9) -> {0,...,8}`, exactly two reproduce the board's 91 line sets:

- `label(a+bi) = 3a + b` (chosen convention);
- `label(a+bi) = 3a + 2b`, which is the same plane relabelled by the field
  automorphism `i -> -i`.

With the chosen convention the point index formula is

```text
point  0          = (0,0,1)
point  1+z        = (0,1,z),             z = 0..8
point 10+9y+z     = (1,y,z),             y,z = 0..8
```

where the coordinates are the integer labels above. The generated 91 lines are
exactly the board lines (set equality, zero symmetric difference).
`out/board_coordinates.json` records the full index-to-vector map.

## 2. Conics and the exhaustive 5-cap check (Task 1b)

### 2.1 All conics

Command:

```sh
python research/experiments/pg2q9-cap-game-20261125/independent_structure/scripts/verify_conics.py
```

Result:

```text
normalized projective forms: 66430; nondegenerate: 58968; distinct zero sets: 58968
conics with size != 10: 0
conics with a 3-point line (not caps): 0
conics that are not maximal (addable point exists): 0
conic count == 58968: True
CONICS: PASS
```

The nondegenerate conics were enumerated as zero sets of nondegenerate
symmetric 3x3 quadratic forms, one representative per projective class. All
58,968 zero sets have exactly 10 points, are caps, and are maximal. This matches
`q^5 - q^2 = 9^5 - 9^2 = 58,968`. Incidence checks:

```text
point-conic incidences: each of 91 points lies on 6480 conics
pair-conic incidences: each of 4095 pairs lies on 648 conics
a conic meets lines as: 45 secants, 10 tangents, 36 external lines
```

### 2.2 Every 5-cap lies on a conic

Command:

```sh
python research/experiments/pg2q9-cap-game-20261125/independent_structure/scripts/verify_5caps.py
```

Result:

```text
brute-force 4-arc count: 1769040
4-arc incidence table: 1769040 keys
incidence table equals brute-force 4-arc count: True
total conic/4-arc incidences: 12383280
bad |E|: 0; bad conic-count: 0; bad coverage: 0
sum |E(Q)| = 74299680
#5-caps = sum/5 = 14859936
58968*C(10,5) = 14859936
5-cap count matches conic-subset count: True
EVERY_5CAP_CONIC: PASS
```

The proof is exhaustive, not sampled:

1. There are exactly 1,769,040 four-caps (brute force over all C(91,4)
   four-subsets; also `91*90*81*64/24 = 1,769,040`).
2. Each four-cap lies on exactly 7 conics (`12,383,280 / 1,769,040 = 7`), and
   the union of their remaining `7*6 = 42` points equals the set `E(Q)` of
   points not on any of the six connecting lines.
3. Every four-cap has `|E(Q)| = 42`. Hence every 5-cap `Q + {p}` is contained
   in one of the conics through `Q`.
4. Therefore every 5-cap is a conic 5-subset. The total number is

   ```text
   #5-caps = (#four-caps) * 42 / 5 = 1,769,040 * 42 / 5 = 14,859,936
           = 58,968 * C(10,5).
   ```

In particular there are **0 non-conic 5-caps**. Every 5-cap has 21 addable
points (checked for all 252 five-subsets of one conic; every conic is a
PGL(3,9)-image of that conic, so the same holds for all), hence **0 maximal
5-caps**.

For completeness, the addable-point distribution over all k-subsets of one
conic (PGL(3,9)-transitivity makes this conic-independent) is:

```text
k=5 : {21: 252}
k=6 : {4: 30, 8: 180}
k=7 : {3: 120}
k=8 : {2: 45}
k=9 : {1: 10}
k=10: {0: 1}
```

So every conic k-subset with k<10 has an addable point (non-maximal), and the
conic 10-caps are maximal. Command:
`python .../scripts/verify_conic_extensions.py`.

## 3. Concrete arithmetic (Task 2)

Command:

```sh
python research/experiments/pg2q9-cap-game-20261125/independent_structure/scripts/verify_data_arithmetic.py
```

All requested products and sums check exactly:

| k | 58,968*C(10,k) | claim | check |
|---:|---:|---:|:---:|
| 5 | 14,859,936 | 14,859,936 | PASS |
| 6 | 12,383,280 | 12,383,280 | PASS |
| 7 | 7,076,160 | 7,076,160 | PASS |
| 8 | 2,653,560 | 2,653,560 | PASS |
| 9 | 589,680 | 589,680 | PASS |
| 10 | 58,968 | 58,968 | PASS |

Claimed decompositions:

```text
k=5 : 14,859,936 = 14,859,936 conic + 0 non-conic; maximal 0
k=6 : 52,009,776 = 12,383,280 conic + 39,626,496 non-conic; maximal 707,616
k=7 : 51,554,880 = 7,076,160 conic + 2,021,760 maximal + 42,456,960 non-conic non-maximal
k=8 :  7,960,680 = 2,653,560 conic + 5,307,120 maximal
k=9 :    589,680 = conic
k=10:     58,968 = conic
```

All sums, products, and the non-conic non-maximal 7-cap difference are exact.

Independent cross-check of k=6 total: all 5-caps are conic and every 5-subset
of a conic has exactly 21 addable points (distribution over all 252
five-subsets of a conic: `{21: 252}`), hence

```text
#6-caps = 14,859,936 * 21 / 6 = 52,009,776
       = 12,383,280 conic 6-subsets + 39,626,496 non-conic 6-caps.
```

## 4. Concrete caps (Task 3)

Command:

```sh
python research/experiments/pg2q9-cap-game-20261125/independent_structure/scripts/verify_specific_caps.py
```

### (a) A non-conic 8-cap is maximal

```text
M = {11,22,29,32,41,44,61,89}
cap=True, conic=False (0 containing conics), addable=[] (#0), maximal=True
```

It was obtained by extending the specified 7-cap by its unique addable point
41. Independently, a random-greedy search found other maximal non-conic 8-caps
(e.g. `{11,35,36,58,62,74,75,86}`), all with zero addable points.

### (b) The specified 7-cap is non-conic and non-maximal

```text
S = {11,22,29,32,44,61,89}
cap=True, conic=False (0 containing conics)
addable=[41] (#1), maximal=False
S + 41 = {11,22,29,32,41,44,61,89} is a non-conic maximal 8-cap.
```

All eight 7-subsets of that 8-cap are non-conic and have exactly the removed
point addable.

### (c) A conic 9-cap is non-maximal and inside a conic 10-cap

Using the conic `C = {0,1,10,20,31,45,51,62,75,88}` and deleting 88:

```text
9-cap = {0,1,10,20,31,45,51,62,75}
cap=True, conic=True, addable=[88] (#1), maximal=False
```

It is contained in the conic 10-cap `C`, and the removed point 88 is addable.
For every conic, each 9-subset has exactly 1 addable point (all 10 such
9-subsets of a conic checked; PGL-transitivity carries this to all conics).

### (d) A conic 10-cap is maximal

`C` has no addable point; more strongly, all 58,968 conics are maximal
(`conics that are not maximal: 0` in section 2.1). Each conic 8-subset has
exactly 2 addable points (the other two conic points), so conic 8-caps are
non-maximal; every 9-subset has exactly 1 addable point.

## 5. Repo data files and maximal counts (Task 4)

### 5.1 `output/census_pg2q9.txt`

```text
N 91 B 91 SAFE 128917712
SIZE  0 total        1 maximal       0
SIZE  1 total       91 maximal       0
SIZE  2 total     4095 maximal       0
SIZE  3 total   110565 maximal       0
SIZE  4 total  1769040 maximal       0
SIZE  5 total 14859936 maximal       0
SIZE  6 total 52009776 maximal  707616
SIZE  7 total 51554880 maximal 2021760
SIZE  8 total  7960680 maximal 5307120
SIZE  9 total   589680 maximal       0
SIZE 10 total    58968 maximal   58968
```

Checks:

- The sum of all `SIZE` totals is 128,917,712, equal to the file's `SAFE`
  value.
- Independently reproduced totals for k = 0..5: 1, 91, 4095, 110,565,
  1,769,040, 14,859,936 (matches `SIZE 0`..`SIZE 5`).
- Independently reproduced k=6 total: 52,009,776 (section 3).
- The five requested maximal numbers are present and correct:
  **707,616 / 2,021,760 / 5,307,120 / 0 / 58,968** for k = 6, 7, 8, 9, 10.

### 5.2 `output/conic_layer.json`

- `"conics": 58968` equals the independent conic count.
- `"pgl2_9_order": 720` equals `9*(9^2-1) = |PGL(2,9)|`.
- Its conic representative `[0,1,10,20,31,45,51,62,75,88]` is a conic in the
  independent list and is a 10-cap.
- For k = 3..9 the `k[k].caps` values equal `58,968*C(10,k)` exactly, and each
  row's `orbit_size` sum equals the same value.

Caveat (not a contradiction; the JSON notes it itself): the k=3 and k=4 rows
are **conic-incidence counts**, not numbers of distinct caps. The distinct
counts are 110,565 three-caps and 1,769,040 four-caps; `7,076,160` and
`12,383,280` are the numbers of conic 3-/4-subsets counted over conics. For
k >= 5 conic k-subsets are distinct (two distinct conics share at most 4
points), so those rows are also distinct-cap counts for conic caps.

### 5.3 Maximal counts verified by orbit-stabilizer

Commands:

```sh
python research/experiments/pg2q9-cap-game-20261125/independent_structure/scripts/verify_max_orbits.py
python research/experiments/pg2q9-cap-game-20261125/independent_structure/scripts/verify_7cap_orbits.py
```

PGL(3,9) maps maximal k-caps to maximal k-caps, so the orbit of one explicit
maximal k-cap is contained in the set of all maximal k-caps. Computing the
stabilizer by enumerating all ordered 4-frames inside the cap gives:

| type | representative | stabilizer | orbit size = 42,456,960 / stab | census |
|---|---|---:|---:|---:|
| conic 10-cap | `[0,1,10,20,31,45,51,62,75,88]` | 720 | 58,968 | 58,968 |
| conic 7-cap | `[0,1,10,20,31,45,51]` | 6 | 7,076,160 | 7,076,160 |
| maximal 6-cap | `[4,32,39,55,57,81]` | 60 | 707,616 | 707,616 |
| maximal 7-cap | `[33,39,57,70,74,80,89]` | 21 | 2,021,760 | 2,021,760 |
| maximal 8-cap | `[11,22,29,32,41,44,61,89]` | 8 | 5,307,120 | 5,307,120 |
| non-conic non-max 7-cap, orbit 1 | `[11,22,29,32,44,61,89]` | 2 | 21,228,480 | — |
| non-conic non-max 7-cap, orbit 2 | `[11,22,32,41,44,61,89]` | 2 | 21,228,480 | — |

Since each orbit size equals the census maximal count, the explicit orbit is
the full set of maximal caps of that size. Thus 707,616 / 2,021,760 /
5,307,120 / 58,968 are independently verified, not merely copied from the
data file. The two 7-cap representatives above are in different orbits
(`maps_to(S,T) = False`), and the two orbit sizes sum to 42,456,960.

The census value `maximal 9-caps = 0` is verified as follows: the 58,968
conics give 58,968*10 = 589,680 conic 9-subsets. They are all distinct,
because two distinct conics share at most 4 points (two distinct degree-2
curves meet in at most 4 points over the algebraic closure). Every conic
9-subset is a 9-cap. The census total for size 9 is also 589,680, so every
9-cap is conic. Every conic 9-subset extends by the remaining conic point,
hence no 9-cap is maximal.

Consequently every 8-cap that is not conic must be maximal (otherwise it would
extend to a 9-cap, which would be conic, making the 8-cap conic). Hence the
8-caps split exactly into `2,653,560` conic 8-caps plus `5,307,120` maximal
8-caps, total 7,960,680, matching the claim.

### 5.4 8-cap maximality sample

Command:

```sh
python research/experiments/pg2q9-cap-game-20261125/independent_structure/scripts/verify_max8_sample.py
```

```text
maximal 8-caps sampled=5000
7-subset addable-count distribution: {1: 40000}
bad addable count (!=1): 0
bad addable point (!= removed point): 0
MAX8_STRUCTURE: PASS
```

Each of 40,000 seven-subsets of 5,000 random maximal 8-caps has exactly one
addable point, namely the removed point. Also, the external/internal point
classification of a conic was verified: 45 external points (4 secants,
2 tangents, 4 external lines) and 36 internal points (5 secants, 5 external
lines). This is the geometric input to the proof that no maximal 8-cap
contains a conic 7-subset.

## 6. |PGL(3,9)| and the non-conic non-maximal 7-cap count (Task 5)

```text
|GL(3,9)| = (9^3-1)(9^3-9)(9^3-9^2) = 339,655,680
|PGL(3,9)| = 339,655,680 / 8 = 42,456,960
```

The claim's non-conic non-maximal 7-cap count is

```text
51,554,880 - 7,076,160 - 2,021,760 = 42,456,960.
```

This is **not a numerical coincidence**. PGL(3,9) has two orbits of
non-conic non-maximal 7-caps (representatives and stabilizers above), each of
size `|PGL(3,9)|/2 = 21,228,480`; their union has size 42,456,960 = |PGL(3,9)|.
The two orbit representatives are genuinely different orbits, and the
stabilizer-2 computation is exact (enumerating all 840 ordered 4-frames in the
7-cap).

Why these are all non-conic non-maximal 7-caps:

1. All 9-caps are conic (section 5.3), so every non-conic 8-cap is maximal.
2. Every maximal 8-cap is in the single PGL orbit of the explicit maximal
   8-cap A (section 5.3; orbit size equals the census maximal-8 count).
3. The stabilizer of A on its 8 points has two orbits of size 4,
   `{11,22,32,41}` and `{29,44,61,89}`. Hence the 7-subsets of A fall into
   the two PGL orbits represented by `A\{41}` and `A\{29}`.
4. Every non-conic non-maximal 7-cap extends to a non-conic 8-cap, which is
   maximal, hence is a PGL-image of A; its 7-subset is therefore in one of the
   two orbits.

Thus the class is exactly the union of the two 21,228,480-caps orbits, and its
cardinality is |PGL(3,9)|. Independently, |PGL(3,9)| also equals the number of
ordered 4-arcs/projective frames:

```text
91*90*81*64 = 42,456,960
```

This frame identity is a separate structural fact (PGL(3,9) acts sharply
transitively on ordered 4-point frames; the frame stabilizer is scalar only,
verified in `verify_misc.py`). The 7-cap equality is structural for the
two-orbit reason above, not because the 7-caps are literally frames.

The full 7-cap decomposition is therefore independently reproduced:

```text
7,076,160 (conic 7-caps, one PGL orbit, stab 6)
+ 2,021,760 (maximal 7-caps, one PGL orbit, stab 21)
+ 2 * 21,228,480 (two non-conic non-maximal 7-cap orbits, stab 2)
= 51,554,880.
```

## 7. PASS/FAIL

| Task | Status | Basis |
|---|---|---|
| 1. Board is PG(2,9); every 5-cap conic; conic counts | **PASS** | plane axioms + exact GF(9) line-family match; exhaustive 4-arc/conic coverage; 58,968 conics; 14,859,936 five-caps |
| 2. Concrete arithmetic | **PASS** | all products/sums exact |
| 3. Concrete caps (a)-(d) | **PASS** | explicit caps verified (non-conic maximal 8-cap; specified 7-cap; conic 9-cap; conic 10-cap) |
| 4. Data-file maximal counts | **PASS** | census/conic_layer numbers match; maximal 6/7/8/10 counts independently reproduced by orbit-stabilizer; maximal 9 = 0 via all 9-caps conic |
| 5. |PGL(3,9)| and 7-cap equality | **PASS** | |PGL|=42,456,960; two PGL orbits of size 21,228,480 each give 42,456,960; structural |

## 8. Discrepancies / caveats

- **No discrepancy with K1331.**
- The only data-format caveat is the one already stated in
  `conic_layer.json`: its k=3 and k=4 `caps` fields are conic-incidence counts
  (7,076,160 and 12,383,280), not distinct cap counts (110,565 and
  1,769,040). This is not an error in the claim's k>=5 statements.
- The coordinate labelling is determined only up to the field automorphism
  `i -> -i`; both labellings reproduce the same line family and the same
  conic/cap families, so no conclusion depends on the choice.
- Maximal-9 = 0 uses the census 9-cap total (589,680) together with the
  independent conic 9-subset count; this is a data cross-check, as allowed by
  Task 4. The maximal counts 6, 7, 8, 10 and the non-conic non-maximal 7-cap
  count are verified structurally by orbit-stabilizer, not just from data.
- The uniqueness of the addable point for every non-conic non-maximal 7-cap
  follows from the orbit decomposition together with the incidence count:
  there are `8 * 5,307,120 = 42,456,960` marked maximal 8-caps, and each maps
  to a non-conic non-maximal 7-cap; every such 7-cap has at least one
  preimage; source and target both have size 42,456,960, so the map is a
  bijection. It was also checked directly on 40,000 seven-subsets of 5,000
  maximal 8-caps and on the explicit task cap.

## 9. Reproduce

From the repository root:

```sh
python research/experiments/pg2q9-cap-game-20261125/independent_structure/scripts/verify_board.py
python research/experiments/pg2q9-cap-game-20261125/independent_structure/scripts/verify_conics.py
python research/experiments/pg2q9-cap-game-20261125/independent_structure/scripts/verify_5caps.py
python research/experiments/pg2q9-cap-game-20261125/independent_structure/scripts/verify_specific_caps.py
python research/experiments/pg2q9-cap-game-20261125/independent_structure/scripts/verify_conic_extensions.py
python research/experiments/pg2q9-cap-game-20261125/independent_structure/scripts/verify_data_arithmetic.py
python research/experiments/pg2q9-cap-game-20261125/independent_structure/scripts/verify_misc.py
python research/experiments/pg2q9-cap-game-20261125/independent_structure/scripts/verify_max_small.py
python research/experiments/pg2q9-cap-game-20261125/independent_structure/scripts/verify_max8_sample.py
python research/experiments/pg2q9-cap-game-20261125/independent_structure/scripts/verify_pgl_orbit.py
python research/experiments/pg2q9-cap-game-20261125/independent_structure/scripts/verify_max_orbits.py
python research/experiments/pg2q9-cap-game-20261125/independent_structure/scripts/verify_7cap_orbits.py
```

Outputs:

- `out/board_coordinates.json` — index-to-GF(9)-vector map.
- `out/conics.txt` — the 58,968 conics as 91-bit masks.
- `out/all_results.txt` — consolidated console log of the main scripts.
