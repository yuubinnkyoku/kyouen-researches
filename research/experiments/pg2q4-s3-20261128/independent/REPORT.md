# Independent verification of K1355: PG(2,4), s = 3 layer spectrum

Date: 2026-11-28 (Asia/Tokyo).
Scope: `research/experiments/pg2q4-s3-20261128/independent/` only (no commits, no edits outside).
Board: `research/experiments/projective-blocking-kyouen-20261125/output/board_pg2q4.txt`.
Python 3.12.13, standard library only.

## Verdict

* The **board geometry**, the **PGL(3,4) transitivity on triangles**, both **cone sizes** (5,038 and
  3,809), the **T_m table**, the **3-cap orbit counts**, the **layer Grundy values**
  `G(k) = (k+1) mod 2`, and the **max safe size 9** are all confirmed.
* The **claimed multiplicities for k = 4,5,6,7,8,9 are wrong**, as are the claimed total
  (157,398) and the claimed G0/G1 totals.  The true multiplicity table is
  `1, 21, 210, 1,330, 5,880, 18,648, 41,328, 58,320, 42,840, 11,480` for k = 0..9,
  total **180,058**, with **G0 = 89,799**, **G1 = 90,259**.
* Root cause: the double-counting formula in the claim omits the **collinear 3-caps**.  The
  correct identity is `1,120·T_m + 210·U_m = C(m,3)·N_m`, where `U_m` comes from the cone of the
  collinear triple `{0,1,2}`.  The claim used only the first term, so it computed
  `N_m − 210·U_m/C(m,3)`.  The claimed numbers are *exactly* this flawed formula (reproduced
  independently), so the claim is internally consistent but does not count the true position set.

## 1. Definitions used

* Points/lines: the 21 given lines of 5 points; `S` is safe iff `|S ∩ L| ≤ 3` for all 21 lines.
* Normal play: `G(S) = mex{ G(S ∪ {p}) : p ∉ S, S ∪ {p} safe }`, `G(S) = 0` if no move
  (terminal).  This is the standard interpretation matching the claim's "mex chain" and its
  `G = 0/1` values.
* Layer spectrum: number of safe sets of each size and each Grundy value.

Three independent computation paths were used:

1. a full DFS enumeration of the safe-set lattice (each safe set exactly once) + bottom-up Grundy DP;
2. a brute-force check of **all 2^20 subsets of size ≤ 10** (no pruning), and the fact that any
   safe 11-set would contain a safe 10-subset;
3. cone DPs started from the two representative 3-caps, cross-checked against the full lattice;
   plus a separate memoised full-upset DP for 91 random samples.

## 2. The board is PG(2,4)

`verify_group.py` checks:

* 21 points, 21 distinct lines, every line has exactly 5 points, every point is on exactly 5 lines,
  every pair of points lies on exactly one line (all pairwise coverages = 1).
* An explicit isomorphism to the standard F4 coordinate model is verified line by line:
  * points 0..4 are the points at infinity (0 = slope 0, 1 = vertical, 2 = slope 1, 3 = slope 3,
    4 = slope 2);
  * points 5..20 are the affine points `(x,y) ∈ F_4^2` with `p = 5 + 4y + x`;
  * all 21 board lines map onto the 21 projective lines of `PG(2,4)` over `F_4 = {0,1,ω,ω²}`.
* The coordinate model itself was independently built from `F_4` arithmetic and passes the same
  projective-plane axioms.

## 3. PGL(3,4) transitivity on triangles

`verify_group.py` builds `PGL(3,4)` from six elementary transvections plus `diag(ω,1,1)`, acting on
the 21 board points through the explicit isomorphism above.

| item | result |
|---|---|
| `|GL(3,4)|` by brute force over all 262,144 matrices | 181,440 |
| `|PGL(3,4)| = |GL|/3` | 60,480 |
| order of the generated permutation group on the board | 60,480 |
| generators preserve the line system | yes (checked for all 6+1 generators) |
| ordered frames (4 points, no 3 collinear) by brute force | 60,480 |
| `21·20·16·9` | 60,480 |
| orbit of one ordered frame | 60,480 (free action) |
| unordered non-collinear triangles | one orbit of size **1,120** = all of them |
| unordered collinear triples | one orbit of size **210** = all of them |
| ordered non-collinear triples | one orbit of size 6,720 |
| ordered collinear triples | one orbit of size 1,260 |

So every non-collinear triangle is equivalent under a collineation, and likewise every collinear
triple.  This justifies using one representative cone per orbit.

## 4. True safe-set counts and Grundy spectrum

Full DFS enumeration and the brute-force check agree exactly.

| k | true N_k | true G | terminal N_k | claimed N_k | claimed G |
|---:|---:|---:|---:|---:|---:|
| 0 | 1 | 1 | 0 | 1 | 1 |
| 1 | 21 | 0 | 0 | 21 | 0 |
| 2 | 210 | 1 | 0 | 210 | 1 |
| 3 | 1,330 | 0 | 0 | 1,330 | 0 |
| 4 | 5,880 | 1 | 0 | 5,040 | 1 |
| 5 | 18,648 | 0 | 0 | 16,128 | 0 |
| 6 | 41,328 | 1 | 0 | 35,952 | 1 |
| 7 | 58,320 | 0 | **360** | 50,976 | 0 |
| 8 | 42,840 | 1 | 0 | 37,620 | 1 |
| 9 | 11,480 | 0 | 11,480 | 10,120 | 0 |
| **all** | **180,058** | | | **157,398** | |

* `G0 = 89,799` (odd sizes), `G1 = 90,259` (even sizes); total 180,058.
* Every safe set of size k has the same Grundy value `(k+1) mod 2`; there are no values ≥ 2.
  This confirms the claim's Grundy assignment for **all positions**, not merely on average.
* Max safe size is 9: no safe set of size 10 exists (verified by the exhaustive subset check);
  since every subset of a safe set is safe, no safe set of size ≥ 10 exists either.
* 360 safe 7-sets are maximal (terminal) already at size 7.  This is worth recording: not every
  position extends to size 9, even though the maximum is 9.  It does not change any layer Grundy
  value (those 7-sets have G = 0, like every other 7-set).

Checks of the claimed Grundy values: `G(0)=1`, `G(1)=0`, `G(2)=1` and the layer values for
k = 3..9 are all confirmed.

## 5. The two cones

`verify_game.py` enumerates all safe supersets of each base 3-cap with a dedicated DFS, computes
their Grundy values by a local DP closed under extension, and cross-checks the size profile against
filtering the full safe-set list.

### 5.1 Triangle cone F = {0,1,5} (non-collinear)

Cone size **5,038**, base Grundy 0.  `T_m` = number of safe m-sets containing F:

| m | 3 | 4 | 5 | 6 | 7 | 8 | 9 | sum |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| T_m | 1 | 18 | 144 | 642 | 1,593 | 1,881 | 759 | 5,038 |
| G | 0 | 1 | 0 | 1 | 0 | 1 | 0 | |

### 5.2 Collinear cone C = {0,1,2} (on line 0)

Cone size **3,809**, base Grundy 0.  `U_m`:

| m | 3 | 4 | 5 | 6 | 7 | 8 | 9 | sum |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| U_m | 1 | 16 | 120 | 512 | 1,224 | 1,392 | 544 | 3,809 |
| G | 0 | 1 | 0 | 1 | 0 | 1 | 0 | |

Both T and U tables are exactly as claimed (the claim's JSON T table matches this one), and the
cone sizes 5,038 / 3,809 are confirmed.

## 6. Double-counting audit: the discrepancy

Count pairs `(S, Δ)` with `S` a safe m-set and `Δ ⊂ S` a 3-subset.  Every safe m-set contains
`C(m,3)` triples.  The triples split into 1,120 non-collinear ones (one PGL orbit) and 210
collinear ones (one PGL orbit).  Hence

```
C(m,3)·N_m = 1,120·T_m + 210·U_m .
```

The claim's formula `N_m = 1,120·T_m / C(m,3)` drops the second term.  Consequently the claim
counts `N_m − 210·U_m/C(m,3)`, i.e. it undercounts by exactly `210·U_m/C(m,3)`:

| m | C(m,3) | T_m | U_m | claimed 1,120·T/C | correct (1,120·T+210·U)/C | true N_m | deficit |
|---:|---:|---:|---:|---:|---:|---:|---:|
| 3 | 1 | 1 | 1 | 1,120 (+210 = 1,330) | 1,330 | 1,330 | 0 |
| 4 | 4 | 18 | 16 | 5,040 | 5,880 | 5,880 | 840 |
| 5 | 10 | 144 | 120 | 16,128 | 18,648 | 18,648 | 2,520 |
| 6 | 20 | 642 | 512 | 35,952 | 41,328 | 41,328 | 5,376 |
| 7 | 35 | 1,593 | 1,224 | 50,976 | 58,320 | 58,320 | 7,344 |
| 8 | 56 | 1,881 | 1,392 | 37,620 | 42,840 | 42,840 | 5,220 |
| 9 | 84 | 759 | 544 | 10,120 | 11,480 | 11,480 | 1,360 |

* Total deficit: `840+2,520+5,376+7,344+5,220+1,360 = 22,660 = 180,058 − 157,398`.
* All divisions in the claimed formula are integers, and all divisions in the corrected formula
  are also integers; the corrected values match the exhaustive enumeration exactly for every m.
* The claim's numbers are **exactly** the values of the flawed formula, so the claimed experiment
  script reproduces its own claim; the formula itself is the error.  The k = 3 correction was
  applied manually (210 collinear triples added), which masks the problem only at k = 3.
* Note that `210·U_m` counts **incidences** `(S, collinear triple)`, not sets `S` containing a
  collinear triple: for m ≥ 5 a safe set can contain two or more collinear triples on different
  lines (e.g. `{a,b,c}` on one line and `{a,d,e}` on another).  So dividing by `C(m,3)` is not a
  count of anything with a direct set interpretation, and cannot be repaired by a per-set
  inclusion–exclusion of "sets with a collinear triple".

The corrected formula was also checked Grundy-resolved: at each m the whole layer has a single
Grundy value, and the same identity holds per value (there is only one nonzero class per m).

## 7. The 3-caps

* All `C(21,3) = 1,330` triples are safe (a line contains at most 3 of them).
* Collinear triples: `21·C(5,3) = 210` (each line contributes 10, and a collinear triple lies on
  exactly one line).
* Non-collinear triples: `1,330 − 210 = 1,120`.
* The PGL orbits are 210 and 1,120 respectively (Section 3).
* **All 1,330 3-caps have Grundy 0**, as claimed.

## 8. Sampling check (full upset DP)

Fixed seed 2026-11-28; 10 random caps of each size class were drawn (size 0 has only one position,
so all positions were used there; sizes 1 and 2 have 21 and 210, and 10 were sampled).  For each
sampled position the Grundy value was recomputed from scratch by a memoised recursion over its full
safe upset, using only safe-set membership (not the layer DP values).  91 samples were computed;
**all matched both the claimed Grundy value and the full-layer DP**.  The smallest/largest upset
sizes explored were 1 (a 9-cap is terminal) and 180,058 (the empty position).  Details, including
the sampled point sets and state counts, are in `game_out.json`.

## 9. The mex chain for k = 0,1,2

* The empty set: all 21 singletons have G = 0, so `G(∅) = mex{0} = 1`.
* Every 2-set has at least one extension, all 3-sets have G = 0, so `G(2-set) = mex{0} = 1`.
* Every 3-set has at least one extension, all 4-sets have G = 1, so `G(3-set) = mex{1} = 0`.

This confirms the claim's `G(0)=1, G(1)=0, G(2)=1` and `G(3)=0` chain, and is also what the full
DP computes.

## 10. What is proved, and what is refuted

Confirmed (exhaustive finite computation):

1. the board is PG(2,4), with an explicit isomorphism to the `F_4` coordinate model;
2. `PGL(3,4)` has order 60,480 = 21·20·16·9 and is transitive on non-collinear triangles
   (orbit 1,120), collinear triples (orbit 210), ordered frames (orbit 60,480, free);
3. cone sizes 5,038 and 3,809 and both T/U tables;
4. all 3-caps are G = 0; 210 collinear / 1,120 non-collinear;
5. every layer k = 0..9 has Grundy `(k+1) mod 2`, and the maximum safe size is 9;
6. the mex chain k = 0,1,2.

Refuted:

1. the size multiplicities for k = 4..9 (see table above); the true total is 180,058;
2. the claimed totals G0 = 78,575 / G1 = 78,823 (true 89,799 / 90,259);
3. the double-counting formula `N_m = 1,120·T_m/C(m,3)` as a count of safe sets — it is missing
   the collinear-triple term.  The correct identity is `1,120·T_m + 210·U_m = C(m,3)·N_m`, and
   the corrected values reproduce the exhaustive enumeration.

The claimed per-layer Grundy *values* are correct, so any downstream statement that uses only
`G(k) = (k+1) mod 2` and the maximum size 9 survives; any statement using the multiplicity table,
the total 157,398, or the G0/G1 totals must be revised.

Corrected spectrum (G is constant on each layer):

| k | N_k | G |
|---:|---:|---:|
| 0 | 1 | 1 |
| 1 | 21 | 0 |
| 2 | 210 | 1 |
| 3 | 1,330 | 0 |
| 4 | 5,880 | 1 |
| 5 | 18,648 | 0 |
| 6 | 41,328 | 1 |
| 7 | 58,320 | 0 |
| 8 | 42,840 | 1 |
| 9 | 11,480 | 0 |
| total | 180,058 | |

## 11. Reproduction

```
python research/experiments/pg2q4-s3-20261128/independent/verify_group.py
python research/experiments/pg2q4-s3-20261128/independent/verify_game.py
```

`verify_group.py` writes `group_out.json`; `verify_game.py` writes `game_out.json`.
`explore.py` / `explore_out.json` are the first quick pass (same enumeration results).
The scripts read the board from the parent experiment but write only inside this directory.

Files:

* `verify_group.py` — board axioms, explicit F_4 isomorphism, |GL|, |PGL|, frame count, orbits.
* `verify_game.py` — exhaustive brute force, full DFS + Grundy DP, cone DPs, double-counting
  audit, 3-caps, 91 full-upset samples, mex chain.
* `explore.py` — quick first-pass enumeration and cone profiles.
* `group_out.json`, `game_out.json`, `explore_out.json` — raw machine-readable results.
