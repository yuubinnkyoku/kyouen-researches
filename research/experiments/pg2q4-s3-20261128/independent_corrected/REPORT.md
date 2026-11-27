# Independent verification report — PG(2,4), s=3 game (corrected K1355 claim)

**Scope.** Board `research/experiments/projective-blocking-kyouen-20261125/output/board_pg2q4.txt`,
game: a position is a set `S` of points that is *safe*, i.e. `|S ∩ L| ≤ 3` for every
line `L`; a move adds one point while preserving safety; Grundy values are for
normal play (terminal position = 0). All work was done in this directory only
(`research/experiments/pg2q4-s3-20261128/independent_corrected/`), Python 3.12.13
standard library only; nothing was committed and nothing outside this directory
was modified.

**Verdict.** Every number in the corrected claim is confirmed exactly. There is
**no numerical discrepancy** in the size-layer spectrum, the totals, the two cone
sizes, the T/U tables, or the double-count identity. Two non-numerical remarks:

1. **Structural caveat:** there are **360 maximal safe 7-sets** (no extension)
   in addition to the 11,480 maximal 9-sets. If any write-up claims "maximal safe
   sets have size 9" or "every safe set of size < 9 is extendable", that statement
   is false. The claimed Grundy spectrum is nevertheless correct, because a
   terminal 7-set also has Grundy 0 (see §4).
2. **Metadata issue (outside my write scope):** the K1355 front-matter title and
   the `scope:` field still say "全 157,398 局面" (the old 22,660-undercounted
   value), while the K1355 body, the experiment README, and the task's corrected
   claim say 180,058. The body is right; the title/scope are stale.

---

## 1. Board verification

The file was parsed and checked directly (script `01_board_dfs.py`):

| Check | Result |
|---|---|
| Header `21 21`; 21 lines, each prefix 5 and 5 distinct points in `0..20` | pass |
| Lines pairwise distinct | pass (21 distinct lines) |
| Every point lies on exactly 5 lines | pass (all degrees 5) |
| Every unordered pair of points lies on exactly one line | pass (210 pairs, each on exactly 1 line) |
| Every two distinct lines meet in exactly one point | pass (all 210 line pairs intersect in 1 point) |
| `(v, k, λ) = (21, 5, 1)`, i.e. a projective plane of order 4 | pass |

A projective plane of order 4 is the Desarguesian `PG(2,4)`, so the board is
verified as a `2-(21,5,1)` design / `PG(2,4)`. The points are labelled 0..20,
the 21 lines are the 21 rows of the file.

---

## 2. Exhaustive enumeration and full Grundy DP

Three independent computations were used, and all agree:

* **Method A (DFS):** depth-first enumeration of safe sets with line counters;
  a point is addable iff none of the 5 lines through it already contains 3
  chosen points. 180,058 leaves, 0.76 s.
* **Method B (full subset lattice):** for all 2^21 = 2,097,152 subsets, safety
  is decided by `safe[mask] = safe[mask \ {p}]` and the 5 lines through `p`
  (`p` = lowest bit of `mask`). The task assumed brute force was impossible, but
  2^21 masks is small: 0.77 s. The resulting safe-set universe is *identical*
  mask-for-mask to Method A.
* **Method C (direct upset recursion):** memoized recursion
  `G(S) = mex{ G(S∪{p}) : S∪{p} safe }`, with safety tested only from the five
  lines through `p`. Starting from the empty position it reaches exactly
  180,058 positions; it reproduces Method B's value on every safe set (0
  mismatches).

### 2.1 Counts and Grundy values by size (exhaustive)

`N_k` = number of safe sets of size k; `G` = Grundy value (all positions on a
layer have the same value).

| k | N_k (computed) | N_k (claim) | G (computed) | G (claim) | status |
|---:|---:|---:|---:|---:|---|
| 0 | 1 | 1 | 1 | 1 | match |
| 1 | 21 | 21 | 0 | 0 | match |
| 2 | 210 | 210 | 1 | 1 | match |
| 3 | 1,330 | 1,330 | 0 | 0 | match |
| 4 | 5,880 | 5,880 | 1 | 1 | match |
| 5 | 18,648 | 18,648 | 0 | 0 | match |
| 6 | 41,328 | 41,328 | 1 | 1 | match |
| 7 | 58,320 | 58,320 | 0 | 0 | match |
| 8 | 42,840 | 42,840 | 1 | 1 | match |
| 9 | 11,480 | 11,480 | 0 | 0 | match |

* Total: **180,058** (claim 180,058).
* Maximum safe size: **9** (no safe 10-set exists; a safe 9-set exists).
* G0 = **89,799**, G1 = **90,259**, no other Grundy values (claim exactly).
* Each layer is Grundy-uniform: `dist(k) = {1: N_k}` for even k and
  `{0: N_k}` for odd k. In particular `G(k) = (k+1) mod 2` for k = 0..9.

The DP itself is the complete verification: every one of the 180,058 positions
had its options enumerated and its mex taken, so the claimed layer values do not
rest on an induction hypothesis.

---

## 3. Extension statistics of safe sets

For every safe set the number of safe one-point extensions was recorded
(exhaustive, script `05_maximal_audit.py`):

| k | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| min extensions | 21 | 20 | 19 | 16 | 15 | 12 | 7 | **0** | 1 | 0 |
| max extensions | 21 | 20 | 19 | 18 | 17 | 16 | 15 | 8 | 4 | 0 |

Thus only size 7 contains non-maximum maximal positions: **360 safe 7-sets have
no extension**. Every safe set of size 0–6 or 8 does extend. One of them, e.g.
`{0,1,2,5,6,9,10}`, is a union of three 3-point "edges" through a common point
(lines `{0,1,2,3,4}`, `{0,5,6,7,8}`, `{0,9,10,11,12}` each contribute 3 points;
every outside point completes a 4-point line).

**Why the spectrum is unaffected.** Let `G_k` be the value on layer k.

* k=9: no safe 10-set exists, so all 9-sets are terminal → `G_9 = 0`.
* k=8: every 8-set has at least one extension (min 1), and all children are
  9-sets with value 0 → `mex{0} = 1` → `G_8 = 1`.
* k=7: a non-terminal 7-set has children that are 8-sets with value 1 →
  `mex{1} = 0`; a terminal 7-set has `mex(∅) = 0`. Both give `G_7 = 0`.
  (This is exactly where the 360 exceptional positions are harmless.)
* k=6: every 6-set has at least one extension (min 7) and all children are
  7-sets with value 0 → `mex{0} = 1`.
* k=5: every 5-set extends (min 12); children are 6-sets with value 1 →
  `mex{1} = 0`.
* k=4, 3, 2, 1, 0: similarly, using the minima 15, 16, 19, 20, 21, the values
  alternate `1, 0, 1, 0, 1`.

So the only possible source of non-uniformity would be a terminal position on
an even layer (which would force value 0 instead of 1), and the exhaustive
extension minima show there is none. This is the correct repair of the tempting
(but false) lemma "max size 9 ⇒ every smaller position extends".

---

## 4. The two 3-cap cones and the corrected double count

Every 3-subset of a safe set is safe (a line can contain all 3). There are
`C(21,3) = 1,330` triples, split into:

* **1,120 triangles** (non-collinear triples),
* **210 collinear triples** (21 lines × `C(5,3) = 10`).

All 1,330 triples are safe 3-sets and all have Grundy 0 (layer k=3).

For a fixed 3-cap `A`, its cone is `{S safe : A ⊆ S}`. The extension table over
all 1,330 triples was computed by scanning every safe set and all its 3-subsets
(6,442,450 incidences). Results:

* All **1,120 triangles have the same extension vector**; all **210 collinear
  triples have the same extension vector**. (So no group-theory input is needed:
  the uniformity was checked directly, not only inferred from PGL(3,4)
  transitivity.)
* Triangle `{0,1,5}` (non-collinear, verified) and collinear triple `{0,1,2}`
  (verified collinear) are representatives; a direct independent rescan of all
  safe sets gives the same vectors (`06_reps.py`).

`T_m = #{S in triangle cone : |S| = m}`, `U_m` analogously:

| m | 3 | 4 | 5 | 6 | 7 | 8 | 9 | total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| T_m | 1 | 18 | 144 | 642 | 1,593 | 1,881 | 759 | **5,038** |
| U_m | 1 | 16 | 120 | 512 | 1,224 | 1,392 | 544 | **3,809** |

The cone totals **5,038** (triangle) and **3,809** (collinear triple) match the
claim. One-point cones are 18 (triangle) and 16 (collinear triple: the two
further points of its line are blocked), as expected.

Since the Grundy value depends only on the size layer, `T_m(g) = T_m` for
`g = G(m)` and 0 otherwise (same for `U`). The identity

```
1,120·T_m(g) + 210·U_m(g) = C(m,3)·N_m(g)
```

was checked for **every m = 0..9 and every g ∈ {0,1}**:

| m | N_m(0) | N_m(1) | T_m | U_m | 1,120·T_m + 210·U_m | C(m,3)·N_m |
|---:|---:|---:|---:|---:|---:|---:|
| 0 | 0 | 1 | 0 | 0 | 0 | 0 |
| 1 | 21 | 0 | 0 | 0 | 0 | 0 |
| 2 | 0 | 210 | 0 | 0 | 0 | 0 |
| 3 | 1,330 | 0 | 1 | 1 | 1,330 | 1,330 |
| 4 | 0 | 5,880 | 18 | 16 | 23,520 | 23,520 |
| 5 | 18,648 | 0 | 144 | 120 | 186,480 | 186,480 |
| 6 | 0 | 41,328 | 642 | 512 | 826,560 | 826,560 |
| 7 | 58,320 | 0 | 1,593 | 1,224 | 2,041,200 | 2,041,200 |
| 8 | 0 | 42,840 | 1,881 | 1,392 | 2,399,040 | 2,399,040 |
| 9 | 11,480 | 0 | 759 | 544 | 964,320 | 964,320 |

Every entry is an exact integer equality; all rows pass. (For m < 3 both sides
vanish because `C(m,3) = 0`.) Total pair count:

```
1,120·5,038 + 210·3,809 = 5,642,560 + 799,890 = 6,442,450
Σ_m C(m,3)·N_m = 6,442,450.
```

This confirms both the cone sizes and the corrected double count, including the
crucial 210 collinear-triple term (the old triangle-only count undercounts by
22,660).

---

## 5. Random caps by direct upset DP

For each size k = 0..9, 20 safe sets were sampled uniformly (seed 20261128;
size 0 has only the empty set, sampled 20 times). Each layer used a **fresh**
memoized direct-upset solver (safety checked from the five lines through the
candidate point, no precomputed safe table). All sampled values match the claim:

| k | pool size | samples | observed G values | claim |
|---:|---:|---:|---|---:|
| 9 | 11,480 | 20 | {0} | 0 |
| 8 | 42,840 | 20 | {1} | 1 |
| 7 | 58,320 | 20 | {0} | 0 |
| 6 | 41,328 | 20 | {1} | 1 |
| 5 | 18,648 | 20 | {0} | 0 |
| 4 | 5,880 | 20 | {1} | 1 |
| 3 | 1,330 | 20 | {0} | 0 |
| 2 | 210 | 20 | {1} | 1 |
| 1 | 21 | 20 | {0} | 0 |
| 0 | 1 | 20 (same position) | {1} | 1 |

All 200 evaluations pass (0 mismatches). Across the ten layer solvers 612,933
nodes were expanded, including a complete 180,058-node recomputation of the
whole space from the empty position in the k=0 layer.

---

## 6. Mex chain and totals

The exhaustive DP gives directly:

* `G_9 = 0`, `G_8 = 1`, `G_7 = 0`, `G_6 = 1`, `G_5 = 0`, `G_4 = 1`,
  `G_3 = 0`, `G_2 = 1`, `G_1 = 0`, `G_0 = 1` — i.e.
  `G(k) = (k+1) mod 2` for k = 0..9.
* `G_0 = 89,799`, `G_1 = 90,259`, sum 180,058, no value > 1.
* The layer-wise mex relations hold (this is how the DP computed them); the
  induction argument in §3 explains why the values are uniform and alternating,
  with the 360 terminal 7-sets causing no exception.

---

## 7. What is established, and discrepancies

**Established by exhaustive computation for this board (all 2^21 subsets and all
180,058 safe positions):**

1. The board is a projective plane of order 4 (`PG(2,4)`), with the given 21
   lines.
2. The safe-set counts by size are exactly
   `1, 21, 210, 1,330, 5,880, 18,648, 41,328, 58,320, 42,840, 11,480`
   (total 180,058; max size 9), confirming the corrected claim.
3. The Grundy spectrum is exactly `1, 0, 1, 0, 1, 0, 1, 0, 1, 0` by size,
   uniformly on each layer; G0 = 89,799 and G1 = 90,259.
4. There are 1,120 triangles and 210 collinear triples among the 3-caps; all are
   safe with G = 0. All triangles share one extension vector; all collinear
   triples share one extension vector.
5. The cone sizes are 5,038 (triangle `{0,1,5}`) and 3,809 (collinear triple
   `{0,1,2}`), and the identity
   `1,120·T_m(g) + 210·U_m(g) = C(m,3)·N_m(g)` holds exactly for every m and g.
6. Random caps of every size 0..9 give the claimed Grundy values under a direct
   upset solver.

**No numerical discrepancy with the corrected claim was found.**

**Caveats / notes:**

* **360 maximal safe 7-sets** exist. Any argument that uses "maximal safe ⇒ size
  9" is invalid; the correct argument uses the extension minima of §3 (and the
  fact that terminal and non-terminal 7-sets both have value 0). The claimed
  spectrum itself is correct.
* The K1355 front-matter **title and `scope:` field** still say "全 157,398 局面"
  (the pre-correction undercount), while its body says 180,058. This is a metadata
  inconsistency in the knowledge item, not in the mathematics; I did not modify
  it (outside this task's write scope).
* The task's premise that subset brute force is impossible is not true here:
  2^21 = 2,097,152 masks is small (0.77 s in Python), so a full subset-lattice
  DP was used as an independent check in addition to DFS. This strengthens the
  enumeration result rather than changing it.
* Finite exhaustive verification establishes the stated finite facts; it does
  not by itself verify the prose claim that PGL(3,4) is transitive on triangles,
  but the needed consequence (identical cone data for all triangles) was checked
  directly for all 1,120 triangles.

---

## 8. Reproducibility

All artifacts are in this directory. Python 3.12.13, standard library only.

| File | Purpose |
|---|---|
| `01_board_dfs.py` | board axiom checks; DFS enumeration; writes `stage1.pkl`/`stage1.json` |
| `02_fullscan_grundy.py` | full 2^21 subset DP; Grundy DP; writes `stage2.json`, `safe_bytearray.bin`, `grundy_bytearray.bin` |
| `03_cones.py` | all-triple extension table; cone vectors; identity for all (m,g); writes `stage3.json` |
| `04_random_caps.py` | direct upset solver; 20 random caps per size; mex chain/totals; writes `stage4.json` |
| `05_maximal_audit.py` | zero-extension audit, example maximal 7-set; writes `stage5.json` |
| `06_reps.py` | direct rescan of the two named cones; writes `stage6.json` |
| `07_final_gate.py` | re-reads all stage JSONs, asserts every PASS, prints headline summary |

Run order and wall times (this machine): `01` 0.9 s, `02` 2.1 s, `03` 3.2 s,
`04` 15 s, `05` ≈2 s, `06` ≈1 s. Random seed: 20261128. No external
dependencies, no network, no commits.
