# Independent verification — complete size-layer Grundy classification of PG(2,9) caps (K1352)

Verifier: independent sub-agent.
Scope: only `research/experiments/pg2q9-cap-game-20261125/independent_complete/`
was created/written.  Nothing was committed, and nothing outside this
directory was modified.  The board and census were read as input only.

Environment: Windows / PowerShell, Python 3.12.13, **Python standard library
only** (no numpy, no C code, no parent verifier code).  All arithmetic is
exact integer/GF(9) arithmetic.

Board under test:
`research/experiments/pg2q9-cap-game-20261125/output/board_pg2q9.txt`.
Census under test:
`research/experiments/pg2q9-cap-game-20261125/output/census_pg2q9.txt`.

## Verdict

| Task | Verdict | Result |
|---|---|---|
| 1. Board is PG(2,9) | **PASS** | all plane axioms; explicit line-preserving bijection to an independently built GF(9) model of PG(2,9) |
| 1. Per-size census | **PASS** | every size count and every maximal count reproduced exactly: total 128,917,712; maximal total 8,095,464 |
| 2. PGL(3,9) transitivity on 1-, 2-, 3-, 4-caps | **PASS** | own 14 generators; orbit sizes 91 / 4,095 / 110,565 / 1,769,040; \|PGL\| = 91·90·81·64 = 42,456,960; sharp transitivity on ordered frames |
| 3. Full 4-cap / 3-cap upset DPs | **PASS** | 10/10 random 4-caps G=0 (children: 42 five-caps, all G=1); 10/10 random 3-caps G=1 (children: 64 four-caps, all G=0) |
| 4. Full 2-cap DPs; one-caps and empty | **PASS** | 5/5 random 2-caps G=0 (children: 81 three-caps, all G=1); one-caps G=1 and empty G=0 by exact mex from the proven child values |
| 5. Arithmetic / remaining claims | **PASS** | k=6 split, k=7 split, total, parity formula all match |

**Overall: PASS.  No discrepancy with K1352 was found.**

Beyond the requested samples, the full global Grundy table was verified
exactly (not sampled): a full DP on the cone of all caps containing one fixed
4-cap, combined with frame double counting and the proven transitivity,
reproduces the k=4,…,10 distributions of K1352 exactly, including both counts
of the k=6 0/2 split and both counts of the k=7 split.  The k=0,…,4 layers are
then fixed by the mex chain.  The claimed k=5 conic mechanism was also
completed: all 6-subsets of all conics have Grundy 0, and every 5-cap lies on
exactly one conic.

---

## 1. The board is PG(2,9), and the census

### 1.1 Board axioms (`t1_board.py`, `pg.py`)

The board file is parsed as an unlabelled incidence structure.  Exhaustive
checks:

| check | result |
|---|---|
| points / lines | 91 / 91 |
| line sizes | all 10 |
| point degrees | all 10 |
| point pairs covered exactly once | 4,095 = C(91,2), no bad pair |
| pairs of lines meeting exactly once | all 4,095 pairs, 0 bad |
| duplicated lines / repeated point on a line | none |

This is a projective plane of order 9.

### 1.2 Explicit isomorphism to PG(2,9) (`pg.py`, `t1_board.py`)

An independent model is built from GF(9) = GF(3)[x]/(x²+1):

* field axioms checked exhaustively (commutativity, associativity,
  distributivity, inverses, no zero divisors, x²=−1, multiplicative group
  cyclic of order 8 with order profile `{1:1, 2:1, 4:2, 8:4}`);
* points are the 91 canonical nonzero vectors of GF(9)³;
* lines are the kernels of the 91 canonical nonzero covectors;
* the model itself passes all plane axioms (91 lines of 10 points, point
  degree 10, every point pair once, every line pair once).

A bijection φ from board points to model points is found by fixing a
projective frame (board frame `(0,1,10,20)`, model frame `(0,1,10,20)`) and
propagating forced incidences; the search needed **2 nodes**.  The resulting
map sends **all 91 board lines onto model lines**, and its inverse sends all 91
model lines onto board lines.  Hence the board is not merely a projective
plane of order 9: it is isomorphic to PG(2,9).

### 1.3 Census (`t2_frame_census.py`)

Low sizes are fixed by closed forms:

```
N0 = 1
N1 = 91
N2 = C(91,2) = 4,095
N3 = C(91,3) - 91*C(10,3) = 110,565
N4 = 1,769,040        (brute force over all C(91,4)=2,672,670 four-subsets:
                       1,769,040 have no three collinear)
```

For k ≥ 4 the census is obtained from **one fixed 4-cap** F = `(0,1,10,20)`
and exact double counting, avoiding a 128.9M-node walk:

* enumerate every cap containing F (1,868 positions, see §3.1);
* let `T_k` be the number of k-caps containing F and `m_k` the number of
  maximal k-caps containing F;
* every k-cap contains C(k,4) four-caps, and by §2 every 4-cap is a
  PGL(3,9)-image of F, so every 4-cap sees the same `T_k`, `m_k`;
* therefore

```
N_k = T_k * N4 / C(k,4)
#maximal k-caps = m_k * N4 / C(k,4)
```

Observed `T_k` and `m_k`:

| k | T_k (all k-caps through F) | m_k (maximal through F) |
|---:|---:|---:|
| 4 | 1 | 0 |
| 5 | 42 | 0 |
| 6 | 441 | 6 |
| 7 | 1,020 | 40 |
| 8 | 315 | 210 |
| 9 | 42 | 0 |
| 10 | 7 | 7 |

Derived versus published census (every entry equal):

| k | derived N_k | census N_k | derived maximal | census maximal |
|---:|---:|---:|---:|---:|
| 0 | 1 | 1 | 0 | 0 |
| 1 | 91 | 91 | 0 | 0 |
| 2 | 4,095 | 4,095 | 0 | 0 |
| 3 | 110,565 | 110,565 | 0 | 0 |
| 4 | 1,769,040 | 1,769,040 | 0 | 0 |
| 5 | 14,859,936 | 14,859,936 | 0 | 0 |
| 6 | 52,009,776 | 52,009,776 | 707,616 | 707,616 |
| 7 | 51,554,880 | 51,554,880 | 2,021,760 | 2,021,760 |
| 8 | 7,960,680 | 7,960,680 | 5,307,120 | 5,307,120 |
| 9 | 589,680 | 589,680 | 0 | 0 |
| 10 | 58,968 | 58,968 | 58,968 | 58,968 |
| **total** | **128,917,712** | **128,917,712** | **8,095,464** | **8,095,464** |

The structural conic identities also check out:

```
#10-caps = #conics = 58,968
#9-caps = 10 * 58,968 = 589,680
#non-maximal 8-caps = C(10,8) * 58,968 = 2,653,560
#8-caps = 5,307,120 + 2,653,560 = 7,960,680
#5-caps = C(10,5) * 58,968 = 14,859,936
```

(The conic count is `|PGL(3,9)|/|PGL(2,9)| = 42,456,960/720 = 58,968`;
every conic is a 10-cap, and the independently derived N10 is also 58,968,
so the 10-caps are exactly the conics.)

---

## 2. PGL(3,9) and transitivity (`group.py`, `t3_group.py`)

### 2.1 Group order and ordered frames

```
|GL(3,9)| = (9³−1)(9³−9)(9³−9²) = 728*720*648 = 339,655,680
|PGL(3,9)| = |GL(3,9)| / (9−1) = 42,456,960
91 * 90 * 81 * 64 = 42,456,960
```

Every ordered non-collinear triple (there are `91*90*81 = 663,390`) has
exactly 64 valid fourth points; this was checked for **all** 663,390 ordered
triples (extension histogram `{64: 663390}`), giving exactly 42,456,960
ordered frames.  For any two ordered frames the unique projectivity is
constructed by linear algebra: if `f4 = Σ α_i f_i` and `d4 = Σ β_i d_i` in
the bases `(f0,f1,f2)` and `(d0,d1,d2)`, the matrix defined by
`A f_i = (β_i/α_i) d_i` (i=0,1,2) is invertible and sends `f4` to `d4`;
a projectivity fixing a frame is the identity, so it is unique.  30/30 random
frame pairs produced an invertible projectivity mapping one frame onto the
other.  This is the sharp-transitivity/order check requested in the task.

### 2.2 Own generators

14 generators were built as 3×3 matrices over GF(9):

* 12 elementary transvections `E_ij(1)`, `E_ij(x)` for all ordered i ≠ j;
* `diag(x,1,1)`;
* the 3-cycle `(x,y,z) ↦ (y,z,x)`.

All are invertible, each induces a permutation of the 91 points, and each
permutation maps all 91 board lines onto board lines (checked for every
generator).  The transvections generate SL(3,9); for q=9, SL(3,9) = PGL(3,9)
in the action on points, and the extra generators are a safety net.

### 2.3 Orbit BFS

Starting from one cap of each size, BFS under the 14 generators gives:

| k | orbit size | all k-caps (census) | time |
|---:|---:|---:|---:|
| 1 | 91 | 91 | <0.1 s |
| 2 | 4,095 | 4,095 | 0.1 s |
| 3 | 110,565 | 110,565 | 4.0 s |
| 4 | **1,769,040** | **1,769,040** | 77.6 s |

Since the orbit is a subset of the corresponding family of caps and its size
equals the total family size, the generated subgroup — and hence PGL(3,9) —
is transitive on 1-, 2-, 3-, and 4-caps.  Together with the sharp
transitivity on ordered frames, this is exactly the transitivity used by
K1352.

---

## 3. Grundy classification

### 3.1 DP method and its correctness

For a cap S, a point p ∉ S is addable iff p is on no secant line of S.  The
full upset (all caps containing S) is enumerated by adding points in strictly
increasing point order; the secant union is maintained incrementally.  Every
cap containing S is produced exactly once.  Grundy values are then computed
bottom-up by size:

```
G(S) = mex { G(S ∪ {p}) : p addable to S }.
```

The DP on the cone of a fixed 4-cap F is valid for the full game: every
superset of a cap containing F also contains F, so the restricted game and
the full game have the same children and the same Grundy values for all 1,868
positions in the cone.  The canonical enumeration was cross-checked against a
second, level-by-level de-duplicating BFS on the same cone; the two sets of
positions agree exactly at every size (`t7_crosschecks.py`).

### 3.2 Full DP on the cone of F = (0,1,10,20)

The cone has exactly 1,868 caps, matching the independently computed 4-cap
upset size.  Its exact Grundy distribution is:

| k | caps through F | G=0 | G=1 | G=2 | maximal through F |
|---:|---:|---:|---:|---:|---:|
| 4 | 1 | 1 | 0 | 0 | 0 |
| 5 | 42 | 0 | 42 | 0 | 0 |
| 6 | 441 | 321 | 0 | 120 | 6 |
| 7 | 1,020 | 40 | 980 | 0 | 40 |
| 8 | 315 | 315 | 0 | 0 | 210 |
| 9 | 42 | 0 | 42 | 0 | 0 |
| 10 | 7 | 7 | 0 | 0 | 7 |

### 3.3 Exact global distribution by frame double counting

For a fixed Grundy value g let `m_{k,g}` be the number of k-caps containing F
with G=g.  Every k-cap contains C(k,4) four-caps, and every 4-cap is a
PGL-image of F; Grundy values are invariant under collineations (checked
computationally on 24 random cap/generator pairs, in addition to being
immediate from the game-tree isomorphism).  Hence, for every 4-cap F′, the
number of k-caps containing F′ with Grundy g is again `m_{k,g}`: a
collineation carrying F to F′ gives a Grundy-preserving bijection between the
two cones.  Double counting pairs (k-cap, contained 4-cap) therefore gives

```
M_{k,g} = m_{k,g} * N4 / C(k,4),      N4 = 1,769,040.
```

This reproduces the K1352 table **exactly**:

| k | verified global distribution | K1352 claim |
|---:|---|---|
| 0 | G=0: 1 | G=0: 1 |
| 1 | G=1: 91 | G=1: 91 |
| 2 | G=0: 4,095 | G=0: 4,095 |
| 3 | G=1: 110,565 | G=1: 110,565 |
| 4 | G=0: 1,769,040 | G=0: 1,769,040 |
| 5 | G=1: 14,859,936 | G=1: 14,859,936 |
| 6 | G=0: 37,857,456; G=2: 14,152,320 | same |
| 7 | G=0: 2,021,760; G=1: 49,533,120 | same |
| 8 | G=0: 7,960,680 | G=0: 7,960,680 |
| 9 | G=1: 589,680 | G=1: 589,680 |
| 10 | G=0: 58,968 | G=0: 58,968 |

The k=0,…,3 entries are then proved by the mex chain below; the frame double
counting itself covers k=4,…,10.  For the two non-trivial mixed layers this
gives explicitly

```
k=6:  1,769,040 * 321 / 15 = 37,857,456   (G=0)
      1,769,040 * 120 / 15 = 14,152,320   (G=2)
k=7:  1,769,040 *  40 / 35 =  2,021,760   (G=0, maximal)
      1,769,040 * 980 / 35 = 49,533,120   (G=1, non-maximal)
```

### 3.4 The mex chain k=0,…,4

* **k=4:** G(F)=0 by full DP; all 4-caps are PGL-images of F; hence every
  4-cap has G=0.
* **k=3:** every 3-cap has exactly 64 addable points (checked for all 663,390
  ordered triples), so its children are nonempty and all are 4-caps with
  G=0.  Hence every 3-cap has G = mex{0} = 1.
* **k=2:** every 2-cap has 81 children (all 3-caps), all with G=1.  Hence
  G = mex{1} = 0.
* **k=1:** every 1-cap has 90 children (all 2-caps), all with G=0.  Hence
  G = mex{0} = 1.
* **k=0:** the empty position has 91 children (all 1-caps), all with G=1.
  Hence G = mex{1} = 0.

This is a proof for all positions of sizes 0–4, not a sample.

### 3.5 The k=5 conic mechanism

K1352's proof says every 5-cap has a conic 6-child of Grundy 0 and all its
children lie in {0,2}.  This was completed as follows.

* Every 6-cap has G ∈ {0,2}: this is part of the exact global distribution in
  §3.3.
* All 6-subsets of conics have G=0.  Proof by exhaustion plus symmetry:
  - the chosen 10-cap is verified to be a conic by solving for the quadratic
    form vanishing on its ten points (unique nonzero form; zero set exactly
    the 10-cap);
  - the 14 generators act transitively on conics: the orbit of this known
    conic `(6,9,27,32,34,37,45,75,77,82)` has size **58,968 = N10**, and
    every orbit element is a 10-cap, so the orbit is the whole set of
    10-caps (and every 10-cap is a conic);
  - all **210** six-subsets of this one conic were run through the full
    upset DP, and all have G=0;
  - by conic transitivity and Grundy invariance, every 6-subset of every
    conic has G=0 (12,383,280 subsets).
* Every 5-cap lies on exactly one conic: there are
  `N10*C(10,5) = 58,968*252 = 14,859,936` pairs (conic, 5-subset), each such
  5-subset is a 5-cap, two distinct conics share at most 4 points, and
  N5 = 14,859,936; the count is a bijection.
* Therefore every 5-cap has at least one child (indeed five conic 6-children)
  with G=0, and no child with G=1; hence G=1 for every 5-cap.

As an independent sample check, 25 random 5-caps were solved for their conic;
all 5 conic 6-children had G=0 in all 25 cases (125/125), and 25 random
6-subsets of conics all had G=0.

### 3.6 The chain k=6,…,10

* **k=10:** terminal, so G=0.  There are no 11-caps: an 11-cap would
  contain a 4-cap F′, and mapping F′ to F by transitivity would give an
  11-cap through F, but the full enumeration of the cone of F stops at 10.
* **k=9:** no maximal 9-caps (derived maximal count 0), so every 9-cap has
  children; all children are 10-caps with G=0; G=mex{0}=1.
* **k=8:** maximal 8-caps are terminal (G=0); every non-maximal 8-cap has
  9-children, all G=1, so G=mex{1}=0.  Hence every 8-cap has G=0.
* **k=7:** maximal 7-caps are terminal (G=0); every non-maximal 7-cap has
  8-children, all G=0, so G=mex{0}=1.  Hence G=0 exactly for the maximal
  7-caps, G=1 for the other 49,533,120.
* **k=6:** full DP gives only G=0 and G=2.  The frame cone shows the
  structural reason: maximal 6-caps are terminal (G=0); non-maximal 6-caps
  whose 7-children are all non-maximal (G=1) have G=mex{1}=0; those with both
  maximal (G=0) and non-maximal (G=1) 7-children have G=mex{0,1}=2.  No
  G=1 occurs.  The exact counts from §3.3 are 37,857,456 and 14,152,320.

### 3.7 Requested sample DPs

All safe base caps below are random (fixed seed `20261128`); each run is a
full DP over the entire upset.

| base size | samples | upset positions | base G | children | child G distribution |
|---:|---:|---:|---:|---:|---|
| 4 | 10 | 1,868 each | 0 | 42 five-caps each | all G=1 (42/42) |
| 3 | 10 | 31,681 each | 1 | 64 four-caps each | all G=0 (64/64) |
| 2 | 5 | 554,122 each | 0 | 81 three-caps each | all G=1 (81/81) |
| 1 | 5 | 9,057,592 (not enumerated) | 1 | 90 two-caps each | all G=0 (proved) |
| 0 | 1 | 128,917,712 (not enumerated) | 0 | 91 one-caps | all G=1 (proved) |

The 1-cap and empty upsets are too large for a memory-resident Python dict
(9.1M and 128.9M positions), so their values use the exact mex-from-children
argument of §3.4 with the proven child values; this is a proof, not a sample.
The 2-cap upsets *were* fully enumerated (554,122 positions each); five
independent random 2-caps all gave G=0 with child distribution 81×G=1.

Additional layer samples (all cheap because k ≥ 5 upsets are tiny):

| size | samples | observed |
|---:|---:|---|
| 5 | 6 random | all G=1; children in {0,2}, at least one 0 |
| 6 | 16 random | 12 G=0, 4 G=2; no G=1 |
| 7 | 16 random | all non-maximal G=1; explicit maximal 7-cap G=0 |
| 8 | 8 random | all maximal G=0; explicit conic 8-cap G=0 |
| 9 | explicit conic 9-subset | G=1 (children: one 10-cap, G=0) |
| 10 | explicit conic | G=0 (terminal) |

Explicit examples: a G=2 6-cap is `[25,29,40,50,66,86]` (children: one G=0
and six G=1), a G=0 non-maximal 6-cap is `[20,33,47,69,86,88]` (children all
G=1), and maximal 6/7/8/10-caps taken from the task context were re-verified
to be caps, maximal, and G=0.

---

## 4. Arithmetic and remaining claims (`t6_arithmetic.py`)

All checks pass:

* k=6 split: `37,857,456 + 14,152,320 = 52,009,776 = N6`; both counts equal
  the frame-derived values.
* k=7 split: `2,021,760 + 49,533,120 = 51,554,880 = N7`; the G=0 count equals
  the maximal 7-cap count.
* Total: `sum N_k = 128,917,712 = census SAFE`.
* Maximal total: `707,616 + 2,021,760 + 5,307,120 + 58,968 = 8,095,464`.
* Parity rule `G = (10−k) mod 2` holds for k=0,1,2,3,4,5,8,9,10
  (values 0,1,0,1,0,1,0,1,0 respectively).
* Conic identities in §1.3 all hold.
* The double-counting divisibility `N_k * C(k,4) / N4` is integral for every
  k=4,…,10.

---

## 5. Discrepancies, limitations, independence

**Discrepancies: none.**  Every number in K1352 and in the census file was
reproduced exactly.

The proof is self-contained except for two standard structural facts, both
verified computationally in the relevant range:

1. **Grundy invariance under collineations.**  A collineation maps caps to
   caps and preserves inclusion, hence is an automorphism of the game graph.
   Checked on 24 random (cap, generator) pairs.
2. **Two distinct conics share at most 4 points**, used for the uniqueness of
   the conic through a 5-cap.  This is the classical Bézout bound; the
   resulting counting identity is also confirmed by the exhaustive count
   N5 = C(10,5)·N10.

The only computations not run as a single full DP are the 1-cap and empty
upsets (9,057,592 and 128,917,712 positions); their values are proved by the
mex chain from the fully proved 2-cap value, so no claim rests on an
unverified sample.  The 2-cap, 3-cap, and 4-cap layers were additionally
checked by independent full DPs on random caps as requested.

No parent code, C census program, or prior verifier code was imported or
executed.  The board and census files were read-only inputs.

---

## 6. Reproduce

From this directory:

```powershell
python run_all.py
```

Runtime is about 2.5 minutes (dominated by the 77.6 s 4-cap orbit BFS and the
five 554,122-position 2-cap DPs).  Individual steps:

```powershell
python t1_board.py            # board axioms + GF(9) model + explicit isomorphism
python t2_frame_census.py     # N4 brute force, frame census, global G by double counting
python t3_group.py            # 14 generators, |PGL|, ordered frames, orbit BFS
python t4_grundy_samples.py   # 10x 4-cap, 10x 3-cap, 5x 2-cap, 1-cap/empty, extra layers
python t5_extra_layers.py     # explicit maximal caps, conic subsets, G=2 example
python t6_arithmetic.py       # census file, splits, totals, parity, conic identities
python t7_crosschecks.py      # alternative enumeration, child structure, G-invariance
python t8_conic_mechanism.py  # 5-cap conic children on random samples
python t9_conic_orbits.py     # conic transitivity + all 210 6-subsets of one conic
```

Machine-readable results are in `out/`:

```
out/t1_board.json
out/t2_frame_census.json
out/t3_group.json
out/t4_grundy_samples.json
out/t5_extra_layers.json
out/t6_arithmetic.json
out/t7_crosschecks.json
out/t8_conic_mechanism.json
out/t9_conic_orbits.json
```

## 7. File inventory

```
independent_complete/
  pg.py                 GF(9), independent PG(2,9) model, board parsing,
                        plane axioms, isomorphism search/verification
  game.py               caps, secant masks, canonical upset enumeration,
                        full Grundy DP, frame census, double counting
  group.py              3x3 matrices over GF(9), 14 generators, permutations,
                        orbit BFS, ordered-frame counts
  t1_board.py           Task 1a (board is PG(2,9))
  t2_frame_census.py    Task 1b (census, N4, frame double counting)
  t3_group.py           Task 2 (PGL order, generators, transitivity)
  t4_grundy_samples.py  Tasks 3/4 (full DPs, mex chain, extra layer samples)
  t5_extra_layers.py    explicit maximal caps and conic subsets
  t6_arithmetic.py      Task 5 (arithmetic)
  t7_crosschecks.py     enumeration / structure / invariance cross-checks
  t8_conic_mechanism.py 5-cap conic-child checks
  t9_conic_orbits.py    conic transitivity and conic 6-subset exhaustion
  out/*.json            machine-readable results
  REPORT.md             this report
```
