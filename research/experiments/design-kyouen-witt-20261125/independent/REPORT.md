# Independent verification report — design-kyouen-witt-20261125

Verifier: independent sub-agent (did not write any file outside `independent/`,
did not commit anything, and did not use `grundy_full.exe` or
`scripts/ks_ilp.py`).

Inputs used for computation: only `output/board_<tag>.txt` (parsed by
`independent/common.py`).  `output/summary.json` and `output/ks_ilp.json` were
read **after** recomputing, for comparison only.

Environment: Windows, PowerShell, Python 3.12.13 (`python --version`).

## Commands

```powershell
cd research/experiments/design-kyouen-witt-20261125/independent
python verify_designs.py        # Task 1  -> out/task1_designs.json
python verify_k3_graded.py      # Task 2+3 -> out/task2_3_k3_graded.json
python verify_grundy.py         # Task 4  -> out/task4_grundy.json
python verify_k4.py             # Task 5  -> out/task5_k4.json
# or everything at once:
python run_all.py
```

All scripts are self-contained (only standard library: `itertools`,
`collections`, `fractions`, `json`).

## Overall result

| Task | Result |
|---|---|
| 1. Design parameters from the board files | **PASS** (all 7 boards, all claimed λ2..λ5 exact) |
| 2. K_3 values (with W_22 witness + no-8 proof) | **PASS** (all 7; exhaustive enumeration + independent counting proof) |
| 3. Graded property and layer counts (ag32, w11, w22 + all others) | **PASS** |
| 4. Empty-board normal-play (and misère) outcomes | **PASS** (full Grundy/misère recursion, all 7) |
| 5. K_4 values (ag42, w22, w23, w24 + all others) | **PASS** (exhaustive search + witnesses + counting bound) |

No discrepancy was found in any of the claimed values that were checked.

---

## Task 1 — the boards are the claimed t-designs

Method (`verify_designs.py`): parse each board, check b lines of k distinct
points in `0..v-1`, no duplicate blocks, all points used, then count, for every
t-subset, how many blocks contain it.  A board is accepted as a
t-(v,k,λ_t) design iff every one of the C(v,t) subsets is covered exactly λ_t
times; the double-counting identity `b·C(k,t) = λ_t·C(v,t)` is checked as well.

Exact counts (all uniform over **all** C(v,t) subsets):

| tag | claimed design | v | b | k | 2-subsets: count / λ2 | 3-subsets: count / λ3 | 4-subsets: count / λ4 | 5-subsets: count / λ5 |
|---|---|---:|---:|---:|---|---|---|---|
| ag32 | 3-(8,4,1) | 8 | 14 | 4 | 28 / **3** | 56 / **1** | (not a 4-design) 14 covered of 70, λ∈{0,1} | – |
| ag42 | 3-(16,4,1) | 16 | 140 | 4 | 120 / **7** | 560 / **1** | (not a 4-design) 140 covered of 1820, λ∈{0,1} | – |
| w11 | 4-(11,5,1) | 11 | 66 | 5 | 55 / **12** | 165 / **4** | 330 / **1** | – |
| w12 | 5-(12,6,1) | 12 | 132 | 6 | 66 / **30** | 220 / **12** | 495 / **4** | 792 / **1** |
| w22 | 3-(22,6,1) | 22 | 77 | 6 | 231 / **5** | 1540 / **1** | (not a 4-design) 1155 covered of 7315, λ∈{0,1} | – |
| w23 | 4-(23,7,1) | 23 | 253 | 7 | 253 / **21** | 1771 / **5** | 8855 / **1** | (not a 5-design) 5313 covered of 33649, λ∈{0,1} |
| w24 | 5-(24,8,1) | 24 | 759 | 8 | 276 / **77** | 2024 / **21** | 10626 / **5** | 42504 / **1** |

Every claimed (v,b,k,λ2,λ3,λ4,λ5) matches exactly.  For the 3-designs the
4-subset multiplicity is indeed not uniform and lies in {0,1} (the report's
"0..1"): e.g. AG(3,2) has 14 covered / 70 total 4-subsets, AG(4,2) 140/1820,
W_22 1155/7315; for W_23 the 5-subset multiplicity is 0 or 1 (5313/33649).

Double-counting identities checked: `b·C(k,t) = λ_t·C(v,t)` for every t
(e.g. W_24: 759·56 = 42504 = 1·42504 for t=5; 759·70 = 53130 = 5·10626 for t=4).

**Result: PASS for all 7 boards.**

---

## Task 2 — K_3

Method: exhaustive increasing-point DFS over all sets S with
|S∩B| ≤ 3 for every block.  The search *is* the branch-and-bound: whenever a
block already contains 3 chosen points, every extension is unsafe, so the
subtree is pruned.  This enumerates every safe set exactly once; the maximum
and the per-size counts are therefore exact.

| tag | exhaustive max | claimed K_3 | size counts of safe sets | match |
|---|---:|---:|---|---|
| ag32 | **4** | 4 | 1, 8, 28, 56, 56 | OK |
| ag42 | **6** | 6 | 1, 16, 120, 560, 1680, 2688, 448 | OK |
| w11 | **3** | 3 | 1, 11, 55, 165 | OK |
| w12 | **3** | 3 | 1, 12, 66, 220 | OK |
| w22 | **7** | 7 | 1, 22, 231, 1540, 6160, 7392, 2464, 352 | OK |
| w23 | **3** | 3 | 1, 23, 253, 1771 | OK |
| w24 | **3** | 3 | 1, 24, 276, 2024 | OK |

For the 4-designs (w11, w23) and 5-designs (w12, w24) every 4-subset lies in a
block, so every 4-set is unsafe; every 3-set is safe; hence K_3 = 3.  The
exhaustive search agrees.

### W_22: explicit 7-set and proof that no 8-set exists

Witness: **S = {0, 1, 2, 3, 9, 12, 21}** (0-based).
Over the 77 blocks the intersections |S∩B| are: 42 blocks with 1, 35 blocks
with 3, **maximum 3** — so S is safe.  There are 352 safe 7-sets in total
(matching the report).

No 8-set (independent counting proof, all design parameters re-derived from
`board_w22.txt` in `verify_k3_graded.py`):
assume |S| = 8 and |S∩B| ≤ 3 for all blocks, and let n_j = #{B : |S∩B| = j}.
* Every triple of S lies in exactly λ3 = 1 block, so exactly n_3 = C(8,3) = 56
  blocks meet S in 3 points.
* Those 56 blocks already contribute 3·56 = 168 pair–block incidences
  (each 3-point block contains C(3,2) = 3 pairs of S).
* But the total number of (block, pair-of-S) incidences is
  C(8,2)·λ2 = 28·5 = **140** (each pair of S lies in exactly 5 blocks).
* 168 > 140 → contradiction.  (Equivalently, the moment equation gives
  x_2 = 140 − 3·56 = −28 < 0.)

The same conclusion is obtained by brute force: the exhaustive search above
enumerates all safe sets and the maximum size is 7.

`moment_solutions(...)` status for s = 8: **infeasible**.

**Result: PASS** (all 7 K_3 values; W_22 witness and no-8 proof included).

---

## Task 3 — graded property and layer counts

For each board, all safe sets (≤3 per block) were enumerated.  "Graded" means
every maximal safe set has size exactly K and every safe set can be extended to
one.  Both were checked directly:
* for every safe set of size < K, a safe superset of size K exists (checked
  against the full list of size-K safe sets);
* the maximal sets were computed independently (no safe one-point extension)
  and all of them have size K.

| tag | K | safe sets by size | maximal sets by size | every safe set extends to size K | report counts / total match |
|---|---:|---|---|:---:|---|
| ag32 | 4 | 1, 8, 28, 56, 56 | 4: 56 | yes | OK (149 safe) |
| ag42 | 6 | 1, 16, 120, 560, 1680, 2688, 448 | 6: 448 | yes | OK (5513 safe) |
| w11 | 3 | 1, 11, 55, 165 | 3: 165 | yes | OK (232 safe) |
| w12 | 3 | 1, 12, 66, 220 | 3: 220 | yes | OK (299 safe) |
| w22 | 7 | 1, 22, 231, 1540, 6160, 7392, 2464, 352 | 7: 352 | yes | OK (18162 safe) |
| w23 | 3 | 1, 23, 253, 1771 | 3: 1771 | yes | OK (2048 safe) |
| w24 | 3 | 1, 24, 276, 2024 | 3: 2024 | yes | OK (2325 safe) |

The three requested layer lists match exactly:
* ag32: 1, 8, 28, 56, 56
* w11: 1, 11, 55, 165
* w22: 1, 22, 231, 1540, 6160, 7392, 2464, 352

No maximal safe set of size < K exists on any of the seven boards.
**Result: PASS** (all 7 boards; the three requested ones included).

---

## Task 4 — normal-play and misère outcomes

Method: full independent game search.  The game graph is
`S -> S ∪ {p}` for every p with the new set still safe; a player with no move
loses (normal play).  Grundy values were computed by mex over all safe
positions (descending by size); misère win/loss was computed by the usual
recursion (a terminal position is a win for the player to move under misère).

### Lemma (graded ⇒ parity), used only as a cross-check

If every maximal safe set has size K, then by induction on n = K − |S|:
terminal positions (n = 0) have Grundy 0; for n > 0 every option T has
K − |T| = n − 1, so by induction all options have Grundy (n−1) mod 2; at least
one option exists (S is not maximal); the mex of {0} is 1 and of {1} is 0, so
Grundy(S) = n mod 2.  For misère (terminal = win) the same induction gives
value (n+1) mod 2.

The direct mex computation confirms this formula on **every** safe position of
all seven boards (the script checks the formula position by position).

| tag | K | Grundy distribution (computed) | report | G(∅) | misère(∅) | report misère | empty-board outcome |
|---|---:|---|---|---:|---:|---:|---|
| ag32 | 4 | 0:85, 1:64 | same | **0** | 1 | 1 | **P (second player wins)** |
| ag42 | 6 | 0:2249, 1:3264 | same | **0** | 1 | 1 | **P (second player wins)** |
| w11 | 3 | 0:176, 1:56 | same | **1** | 0 | 0 | **N (first player wins)** |
| w12 | 3 | 0:232, 1:67 | same | **1** | 0 | 0 | **N** |
| w22 | 7 | 0:9306, 1:8856 | same | **1** | 0 | 0 | **N** |
| w23 | 3 | 0:1794, 1:254 | same | **1** | 0 | 0 | **N** |
| w24 | 3 | 0:2048, 1:277 | same | **1** | 0 | 0 | **N** |

The per-size Grundy-0 counts also match `summary.json` exactly
(`size_counts[j].grundy0`), and all Grundy values are in {0,1}.  The claimed
outcomes hold: ag32 and ag42 are P-positions, the other five are N-positions.

**Result: PASS.**

---

## Task 5 — K_4

Method: (a) exhaustive enumeration of all sets with |S∩B| ≤ 4 for every block
(complete DFS); (b) an independent counting upper bound derived from the
design parameters re-derived from the board: if a safe set of size s existed,
the block-intersection profile x_j (j = 0..4) would have to satisfy
Σ_j C(j,r)x_j = λ_r·C(s,r) for r = 0,1,2,3 (and r = 4 for 4-designs); if this
integer system has no nonnegative solution at s = K+1, then |S| ≤ K.  A
witness of size K completes the proof.

| tag | exhaustive max | claimed K_4 | # 4-safe sets | # size-K sets | witness (0-based) | counting bound at K+1 | ILP K4 |
|---|---:|---:|---:|---:|---|---:|---:|
| ag32 | **8** | 8 | 256 | 1 | all 8 points | trivial (k=4) | 8 |
| ag42 | **16** | 16 | 65536 | 1 | all 16 points | trivial (k=4) | 16 |
| w11 | **6** | 6 | 1024 | 66 | {0,1,2,3,4,6} | s=7 infeasible | 6 |
| w12 | **4** | 4 | 794 | 495 | {0,1,2,3} | s=5 infeasible | 4 |
| w22 | **10** | 10 | 311543 | 616 | {0,1,2,3,4,5,6,9,16,20} | s=11 infeasible | 10 |
| w23 | **8** | 8 | 57961 | 506 | {0,1,2,3,4,15,17,20} | s=9 infeasible | 8 |
| w24 | **4** | 4 | 12951 | 10626 | {0,1,2,3} | s=5 infeasible | 4 |

* AG(3,2), AG(4,2): every block has exactly 4 points, so |S∩B| ≤ 4 for the
  whole point set; K_4 = v.
* W_24 and W_12 are 5-designs: every 5-subset lies in a block, so any 5-set is
  unsafe; every 4-set is safe; K_4 = 4.  (W_23 is a 4-design; the exhaustive
  search is what fixes K_4 = 8 there.)
* W_22: K_4 ≤ 10 by the counting system at s = 11 (infeasible); the witness
  above is safe, so K_4 = 10.  The exhaustive enumeration independently gives
  maximum 10 (311543 4-safe sets).  Concretely, with x_4 = t the system forces
  x_3 = 165 − 4t, x_2 = 6t − 220, x_1 = 176 − 4t, x_0 = t − 44; nonnegativity
  gives t = 44 and then x_3 = −11 < 0.
* W_23: counting system at s = 9 is infeasible (its unique solution would have
  x_4 = λ4·C(9,4) = 126 and x_3 = λ3·C(9,3) − 4x_4 = 420 − 504 = −84 < 0);
  the witness gives 8.  Exhaustive enumeration independently gives maximum 8.

**Result: PASS** — all claimed K_4 values `8,16,6,4,10,8,4` verified; no
discrepancy with `ks_ilp.json`.

---

## Discrepancies and limitations

1. **No numerical discrepancy was found.**  Every claimed design parameter,
   K_3, safe-set layer count, maximal count, Grundy distribution, misère root
   and K_4 value that was checked matches the report / `summary.json` /
   `ks_ilp.json`.

2. **Minor metadata inconsistency (not a mathematical error):**
   `output/designs_meta.json` records `W_23` with `"t": 3` and `"lambda_t": [5]`
   (i.e. only λ3), although the board is the claimed 4-(23,7,1) design; the
   board check here confirms λ4 = 1 uniformly.  `W_24` similarly omits λ4 in
   the metadata file.  README/report do state λ4 = 1 for W_23 and λ4 = 5 for
   W_24, and those values are correct.

3. **Not verified (out of scope of the request):**
   * K_5 values (`ks_ilp.json` lists 8,16,11,6,15,11,6) — not checked here.
   * The general upper-bound formula `K_s ≤ (s−2)λ2/λ3 + 2` — not re-proved;
     only concrete values were checked.
   * The claim that the board construction scripts really build these designs
     from codes — only the produced board files were verified.
   * Full misère Grundy distribution beyond the root — misère win/loss was
     computed for all positions (and the parity formula verified), but the
     report contains no per-size misère distribution to compare.

4. **Honest caveat on AG(4,2), K_3:** my own counting/moment upper bound at
   s = 7 is *feasible* (profile x = (7,56,42,35)), so counting alone does not
   prove K_3 ≤ 6 there; the value K_3(AG(4,2)) = 6 is established by the
   exhaustive enumeration (all 5513 safe sets), which is exact.  The report's
   own moment bound was weaker anyway (9).

5. **Graded is verified for these seven boards only**, not as a general
   theorem; the report presents it as an observation, which is consistent.

## Artifacts

* `independent/common.py` — board parser, safe-set enumerator, λ recomputation.
* `independent/moments.py` — exact integer moment-system feasibility
  (Fractions; used for independent counting upper bounds).
* `independent/verify_designs.py` — Task 1.
* `independent/verify_k3_graded.py` — Tasks 2 and 3.
* `independent/verify_grundy.py` — Task 4.
* `independent/verify_k4.py` — Task 5.
* `independent/run_all.py` — runs all of the above.
* `independent/out/*.json` — machine-readable results
  (`task1_designs.json`, `task2_3_k3_graded.json`, `task4_grundy.json`,
  `task5_k4.json`).
