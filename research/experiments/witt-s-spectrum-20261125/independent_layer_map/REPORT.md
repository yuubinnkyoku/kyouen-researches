# Independent layer map of the W_24 s=7 Grundy spectrum

**Target claim:** K1349 (layer structure of the s=7 Grundy spectrum of the
W_24 board).
**Board (read only):** `research/experiments/design-kyouen-witt-20261125/output/board_w24.txt`
SHA-256 `1DE7BA7BC8875A5F84ACAE6055ED8042EF74B494C4D12FE7D64D90916BAB7892`.
**Work dir:** `research/experiments/witt-s-spectrum-20261125/independent_layer_map/`
(everything here was created by this audit; nothing else was modified; nothing committed).

**Environment:** Windows, gcc 15.2.0 (MSYS2 ucrt64), Python 3.12.13 (stdlib only).
The exhaustive C scan takes ≈ 9 s; the whole reproduction script (`run_all.ps1`)
takes about 20–25 s.

## 0. Verdict

**The K1349 layer description is confirmed in full, exhaustively, with zero numeric
discrepancies.** 84/84 automated claim checks pass (`out/claim_check.txt`).

What was recomputed independently (no code from the original engine or from any
earlier verification was used):

* the board is identified as W_24 = S(5,8,24) and the Golay span is rebuilt from the
  octads, giving exactly 2,576 dodecads and the weight enumerator
  `{0:1, 8:759, 12:2576, 16:759, 24:1}`;
* a complete Grundy DP over **all 7,932,035 safe positions** (all sizes 0…13), so the
  distribution is exhaustive, not sampled;
* the layer *set equalities* are checked on every position of every layer, not on a
  sample: e.g. all 566,720 dodecad 9-subsets have G = 2 and all 728,640 non-dodecad
  9-caps have G = 1;
* the maximal-extension profiles are checked on **all** caps of each type (the claim
  says they were sampled); the 10-random-caps-per-type check requested in the task is
  also done and is reported in the appendix;
* the size-12 / size-13 splits are recomputed and agree.

One wording issue (not a numeric discrepancy) is noted in §8.

## 1. Method — two independent implementations

**C (`layer_map.c`).** Deliberately different from the reference engine:

* safety is decided by an explicit *"mask contains a whole octad"* bitmap built as the
  union of all block supersets (`B ∪ X`, `|X| ≤ 6`), not by the engine's incremental
  blocking counters;
* all `C(24,k)` subsets for `k = 0…14` are scanned against that bitmap to produce the
  exact safe-position lists;
* Grundy values come from a mex DP in decreasing size order using a full 2^24-byte
  value table (no hashing, no compression);
* layer membership (subset of a dodecad) is a second bitmap; all layer cross-tabs,
  maximal counts, maximal 12/13-cap lists and extension profiles are tabulated from it.

**Python (`task1_board.py`, `spotcheck.py`).** A second, structurally different
implementation: it uses the literal rule *"S is safe iff |S ∩ B| ≤ 7 for every block B"*
with no octad-free shortcut, and recomputes both the Grundy value and the full
maximal-extension profile for 65 sampled positions by explicit safe-superset DFS with
its own mex recursion.

Both agree with each other and with the reported s=7 engine files
(`grundy_w24_s7.txt`, `grundy_w24_s7_gsize.txt`) on every quantity.

## 2. Task 1 — the board is W_24, and the dodecads

`python task1_board.py` → `out/task1_board.json`, `out/dodecads.txt`

* 24 points, 759 blocks, every block has 8 distinct points, all blocks distinct, no
  repeated point inside a block.
* Every 5-subset lies in **exactly one** block (42,504 incidences = C(24,5); the C
  program re-checks this by sorting the 42,504 five-subsets). Hence S(5,8,24).

| t | λ_t (blocks through a t-subset) |
|---:|---:|
| 0 | 759 |
| 1 | 253 |
| 2 | 77 |
| 3 | 21 |
| 4 | 5 |
| 5 | 1 |

* Pairwise block intersections are only 0, 2, 4, with counts
  11,385 / 170,016 / 106,260.
* The F_2-span of the 759 octads has rank **12** and 4,096 words; the weight
  enumerator is exactly

  | weight | 0 | 8 | 12 | 16 | 24 |
  |---|---:|---:|---:|---:|---:|
  | count | 1 | 759 | **2,576** | 759 | 1 |

  The span is self-orthogonal and doubly even, the weight-8 words are exactly the 759
  octads, and the code is closed under complement. This is the binary Golay code.
* The **dodecads** (weight-12 words) number **2,576**; each meets each octad in
  {2,4,6} points with the constant profile `2:132, 4:495, 6:132`; complements of
  dodecads are dodecads; no octad is contained in a dodecad, so every dodecad and every
  dodecad subset is safe for s = 7.
* Dodecad subsets are **injective**: exactly 566,720 / 170,016 / 30,912 / 2,576
  distinct 9/10/11/12-subsets (= 2,576·C(12,k)), and none contains a block. The latter
  follows from the constant block/dodecad profile above (a block meets a dodecad in at
  most 6 points, so no 8-point block fits inside any subset); a direct scan of 2,000
  random subsets per size was also negative. These are exactly the layer sizes claimed
  by K1349.

## 3. Task 2 — Grundy distribution per size (exhaustive)

`out/layer_map.txt`. The safe positions number **7,932,035**; a position of size 14 or
more does not exist. Grundy values never exceed 2.

| size | safe positions | maximal | G=0 | G=1 | G=2 |
|---:|---:|---:|---:|---:|---:|
| 0 | 1 | 0 | 1 | 0 | 0 |
| 1 | 24 | 0 | 0 | 24 | 0 |
| 2 | 276 | 0 | 276 | 0 | 0 |
| 3 | 2,024 | 0 | 0 | 2,024 | 0 |
| 4 | 10,626 | 0 | 10,626 | 0 | 0 |
| 5 | 42,504 | 0 | 0 | 42,504 | 0 |
| 6 | 134,596 | 0 | 134,596 | 0 | 0 |
| 7 | 346,104 | 0 | 0 | 346,104 | 0 |
| 8 | 734,712 | 0 | 734,712 | 0 | 0 |
| 9 | 1,295,360 | 0 | 0 | **728,640** | **566,720** |
| 10 | 1,870,176 | 0 | **1,700,160** | **170,016** | 0 |
| 11 | 2,071,104 | 0 | **30,912** | 0 | **2,040,192** |
| 12 | 1,393,616 | **1,020,096** | **1,020,096** | **373,520** | 0 |
| 13 | 30,912 | **30,912** | **30,912** | 0 | 0 |
| 14 | 0 | 0 | 0 | 0 | 0 |
| **Σ** | **7,932,035** | **1,051,008** | **3,662,291** | **1,662,832** | **2,606,912** |

Every maximal position has size 12 or 13. Note `2,606,912 = 566,720 + 2,040,192`,
i.e. the G = 2 positions are exactly the two layers claimed by K1349.

Cross-check against the reported engine files: `SAFE`, every `SIZE` line
(count / maximal / G=0 count), every `GRUNDY` total, `GSIZE` and `ROOT` in
`grundy_w24_s7.txt` and `grundy_w24_s7_gsize.txt` are reproduced **exactly**.

## 4. Task 3 — the layer *set equalities* (full check)

The C program classifies **every** safe 9/10/11-set by "subset of a dodecad / not"
using an exhaustive bitmap of all dodecad subsets (566,720 + 170,016 + 30,912 =
767,648 marked sets), and cross-tabulates that with the DP Grundy value. Result — every
cell is a single (type, G) pair:

| size | dodecad-type caps | their G | non-dodecad caps | their G |
|---:|---:|---:|---:|---:|
| 9 | **566,720** | **2** (all) | **728,640** | **1** (all) |
| 10 | **170,016** | **1** (all) | **1,700,160** | **0** (all) |
| 11 | **30,912** | **0** (all) | **2,040,192** | **2** (all) |
| 12 | 2,576 (the dodecads) | 1 (all; they are non-maximal) | 1,391,040 | 1,020,096 at 0 (maximal) + 370,944 at 1 (non-maximal) |

That is: *membership in a dodecad layer determines the Grundy value on all 9-, 10- and
11-caps*, with no exception anywhere. All 566,720 / 170,016 / 30,912 / 2,576 dodecad
subsets were checked; the sets are pairwise distinct and the DP values are exact.

## 5. Task 4 — maximal-extension profiles

**Definition used (and verified).** For a cap S, the profile is the pair

> `#{maximal 12-caps M : S ⊆ M}` : `#{maximal 13-caps M : S ⊆ M}`,

computed by enumerating all 1,020,096 maximal 12-caps and all 30,912 maximal 13-caps
and summing the incidence over all their 9/10/11/12-subsets (exhaustive, no sampling);
the Python verifier independently enumerates every safe superset of a sampled S and
collects the maximal ones, which reproduces the same pair.

Exhaustive result (every cap of the type, not a sample):

| layer | caps | profile {#max12 : #max13} | constant over the whole layer? |
|---|---:|---|---|
| dodecad 9-subsets | 566,720 | **{12: 180, 13: 21}** | yes (1 distinct profile) |
| non-dodecad 9-caps | 728,640 | **{12: 168, 13: 14}** | yes (1 distinct profile) |
| dodecad 10-subsets | 170,016 | **{12: 36, 13: 12}** | yes (1 distinct profile) |
| non-dodecad 10-caps | 1,700,160 | **{12: 36, 13: 4}** | yes (1 distinct profile) |
| dodecad 11-subsets | 30,912 | **{12: 0, 13: 12}** | yes (1 distinct profile) |
| non-dodecad 11-caps | 2,040,192 | **{12: 6, 13: 1}** | yes (1 distinct profile) |

For completeness the other layers:

| layer | caps | profile |
|---|---:|---|
| maximal 12-caps | 1,020,096 | {12: 1, 13: 0} |
| non-maximal non-dodecad 12-caps | 370,944 | {12: 0, 13: 1} |
| 12-cap dodecads | 2,576 | {12: 0, 13: 12} |
| maximal 13-caps | 30,912 | {12: 0, 13: 1} |

Every one of the claimed profile values is reproduced exactly, and each layer type is
**Grundy-uniform and profile-uniform**. A check of 10 random caps per layer type
(60 caps, appendix) shows the identical histograms; the exhaustive table above is the
stronger statement.

Sanity arithmetic (independent of the program): maximal 12-caps form
1,020,096·C(12,9) = 224,421,120 pairs (M, S) with |S| = 9, and the layer counts give
566,720·180 + 728,640·168 = 224,421,120; maximal 13-caps form
30,912·C(13,9) = 22,102,080 = 566,720·21 + 728,640·14. The same two identities hold for
sizes 10 and 11, so all six layer counts are forced by the maximal-cap counts alone and
are mutually consistent.

## 6. Task 5 — size-12 split and size 13

* **Size 12:** 1,393,616 safe 12-caps. **1,020,096 are maximal** (G = 0) and
  **373,520 are non-maximal** (G = 1). Both counts match the claim.
* The non-maximal 12-caps have an exact structural description, verified on all of
  them: 2,576 are the dodecads, and the remaining **370,944** are exactly the sets
  `S ∪ {p}` with `S` an 11-subset of a dodecad and `p` a point outside that dodecad.
  All 370,944 contain a dodecad 11-subset; no maximal 12-cap contains one; the
  370,944 sets are pairwise distinct (2,576·12·12 = 370,944 = 30,912·12).
  Every dodecad is a non-maximal 12-cap with G = 1 and exactly 12 legal moves.
* **Size 13:** exactly **30,912** safe 13-sets; all are maximal, all have G = 0. No
  safe 14-set exists, so these are the terminal positions.
* Every non-maximal 12-cap has exactly **one** legal extension (to a maximal 13-cap),
  which is why its G is 1 and why the dodecad 11-subsets (whose 12 extensions are all
  non-maximal) get mex = 0.

## 7. Claim-by-claim comparison

| K1349 statement | claimed | independent (exhaustive) | verdict |
|---|---:|---:|---|
| dodecad 9-subsets G=2 | 566,720 | 566,720 (all G=2) | PASS |
| other 9-caps G=1 | 728,640 | 728,640 (all G=1) | PASS |
| dodecad 10-subsets G=1 | 170,016 | 170,016 (all G=1) | PASS |
| other 10-caps G=0 | 1,700,160 | 1,700,160 (all G=0) | PASS |
| dodecad 11-subsets G=0 | 30,912 | 30,912 (all G=0) | PASS |
| other 11-caps G=2 | 2,040,192 | 2,040,192 (all G=2) | PASS |
| maximal 12-caps G=0 | 1,020,096 | 1,020,096 (all maximal, all G=0) | PASS |
| non-maximal 12-caps G=1 | 373,520 | 373,520 (all non-maximal, all G=1) | PASS |
| maximal 13-caps G=0 | 30,912 | 30,912 (all maximal, all G=0) | PASS |
| profile dodecad 9 | {12:180, 13:21} | exact, for every one of the 566,720 | PASS |
| profile non-dodecad 9 | {12:168, 13:14} | exact, for every one of the 728,640 | PASS |
| profile dodecad 10 | {12:36, 13:12} | exact, for every one of the 170,016 | PASS |
| profile non-dodecad 10 | {12:36, 13:4} | exact, for every one of the 1,700,160 | PASS |
| profile dodecad 11 | {13:12} | {12:0, 13:12}, for every one of the 30,912 | PASS |
| profile non-dodecad 11 | {12:6, 13:1} | exact, for every one of the 2,040,192 | PASS |
| dodecads = weight-12 Golay words | 2,576 | 2,576, weight enumerator as claimed | PASS |
| G = 2 total | — | 2,606,912 = 566,720 + 2,040,192 | PASS |

Automated: `python compare_claim.py` → `out/claim_check.txt` / `.json`,
**84/84 checks passed, 0 failed**.

## 8. What is proved, and discrepancies

**Proved (computational, exhaustive).** For the given board file, every safe position
of the s = 7 game (7,932,035 of them, sizes 0…13) has been enumerated and its exact
Grundy value computed by a full mex DP; the layer map and every maximal-extension
profile above are statements about *all* positions, not samples. The board file was
independently verified to be the Witt design S(5,8,24) (the 5-design with
λ₅ = 1, intersections 0/2/4, Golay span of rank 12 and weight enumerator
1 + 759x⁸ + 2576x¹² + 759x¹⁶ + x²⁴), which is W_24 up to isomorphism; hence the
statement is about W_24.

**Independence / confidence.** (i) The C implementation uses different algorithms and
data structures from the reference engine; (ii) the Python implementation recomputes
Grundy values and profiles from the literal `|S ∩ B| ≤ 7` rule for 65 sampled caps and
agrees in all cases (65/65, `out/spotcheck.txt`); (iii) every aggregate and per-size
number agrees exactly with the reported `grundy_w24_s7.txt` and
`grundy_w24_s7_gsize.txt`.

**Discrepancies: none numerically.** Two remarks:

1. K1349 labels the 2,040,192 non-dodecad 11-caps as *"(13-cap non-dodecad
   11-subsets)"*. That label is loose: the class meant is the **non-dodecad 11-caps**
   (each of them happens to lie in exactly one maximal 13-cap, as the profile
   {12: 6, 13: 1} shows). Under that reading the number and the Grundy value are
   exactly right — wording only.
2. K1349 reports the profiles as *sampled*. Here they were verified for **all** caps of
   each type (single profile per type), which is stronger than the claim needs.

**Caveat.** As with any finite computation, the result is conditional on the board file
and on code correctness; the three-way agreement above (C, Python, engine files) plus
the exact incidence identities is the intended mitigation. The profiles' meaning is the
one stated in §5; under any other reading of "maximal-extension profile" the numbers
would have to be re-interpreted, but the stated reading matches all claimed values
exactly and is constant over each layer.

## 9. Files

| file | content |
|---|---|
| `layer_map.c` | exhaustive independent C verifier (safety bitmap, full mex DP, layer cross-tabs, profiles) |
| `layer_map.exe` | compiled binary (gcc 15.2.0, `-O2`) |
| `task1_board.py` | board identification, Golay span, dodecads, dodecad-subset counts |
| `spotcheck.py` | independent Python recomputation of G and profiles for 65 sampled caps |
| `make_tables.py` | builds the appendix table from the C output |
| `compare_claim.py` | 84 claim checks vs the independent outputs and the raw engine files |
| `run_all.ps1` | reproduces everything |
| `out/layer_map.txt` | full C output (board, Golay, safe counts, SIZE/GSIZE, CROSS, PROFILE, SAMPLE, checks) |
| `out/task1_board.json`, `out/dodecads.txt` | task-1 results and the 2,576 dodecads |
| `out/spotcheck.txt` | Python spot-check result |
| `out/claim_check.txt`, `out/claim_check.json` | claim comparison, 84/84 PASS |
| `out/samples_table.md` | the 75 sampled caps with G and profiles |

Reproduce with `./run_all.ps1` (or `gcc -O2 -o layer_map.exe layer_map.c` and then the
four python scripts, in the order used by the script).

## Appendix — 10 random caps per layer type (plus size-12/13 samples)

Drawn with a fixed LCG from the complete list of safe caps of the size, filtered by
type. `G` is the Grundy value, `#max12`/`#max13` are the maximal-extension profile.
Every sample matches the exhaustive profile of its type; the exhaustive statement is in
§5.

| k | layer | mask | G | #max12 | #max13 | point set |
|---:|---|---:|---:|---:|---:|---|
| 9 | dodecad | 1195784 | 2 | 180 | 21 | {3,8,9,10,11,12,13,17,20} |
| 9 | dodecad | 3387524 | 2 | 180 | 21 | {2,7,12,13,15,16,17,20,21} |
| 9 | dodecad | 1968901 | 2 | 180 | 21 | {0,2,8,9,11,17,18,19,20} |
| 9 | dodecad | 1210630 | 2 | 180 | 21 | {1,2,8,11,12,13,14,17,20} |
| 9 | dodecad | 625873 | 2 | 180 | 21 | {0,4,6,7,10,11,15,16,19} |
| 9 | dodecad | 1324720 | 2 | 180 | 21 | {4,5,7,9,10,12,13,18,20} |
| 9 | dodecad | 14722307 | 2 | 180 | 21 | {0,1,8,10,13,15,21,22,23} |
| 9 | dodecad | 12263441 | 2 | 180 | 21 | {0,4,13,16,17,19,20,21,23} |
| 9 | dodecad | 13189360 | 2 | 180 | 21 | {4,5,6,7,14,16,19,22,23} |
| 9 | dodecad | 4484032 | 2 | 180 | 21 | {6,7,8,9,11,13,14,18,22} |
| 9 | non-dodecad | 264079 | 1 | 168 | 14 | {0,1,2,3,7,8,9,10,18} |
| 9 | non-dodecad | 2339204 | 1 | 168 | 14 | {2,7,8,12,13,15,16,17,21} |
| 9 | non-dodecad | 8476826 | 1 | 168 | 14 | {1,3,4,7,11,12,14,16,23} |
| 9 | non-dodecad | 166828 | 1 | 168 | 14 | {2,3,5,7,8,9,11,15,17} |
| 9 | non-dodecad | 7914760 | 1 | 168 | 14 | {3,8,10,14,15,19,20,21,22} |
| 9 | non-dodecad | 4227934 | 1 | 168 | 14 | {1,2,3,4,6,8,9,15,22} |
| 9 | non-dodecad | 4262866 | 1 | 168 | 14 | {1,4,6,7,8,9,11,16,22} |
| 9 | non-dodecad | 6689158 | 1 | 168 | 14 | {1,2,7,8,12,17,18,21,22} |
| 9 | non-dodecad | 13050117 | 1 | 168 | 14 | {0,2,8,13,16,17,18,22,23} |
| 9 | non-dodecad | 5450882 | 1 | 168 | 14 | {1,7,10,11,13,16,17,20,22} |
| 10 | dodecad | 4772391 | 1 | 36 | 12 | {0,1,2,5,9,12,14,15,19,22} |
| 10 | dodecad | 7378252 | 1 | 36 | 12 | {2,3,6,8,10,12,15,20,21,22} |
| 10 | dodecad | 1202602 | 1 | 36 | 12 | {1,3,5,7,8,11,12,14,17,20} |
| 10 | dodecad | 1366200 | 1 | 36 | 12 | {3,4,5,7,11,12,14,15,18,20} |
| 10 | dodecad | 10161190 | 1 | 36 | 12 | {1,2,5,10,11,16,17,19,20,23} |
| 10 | dodecad | 7694856 | 1 | 36 | 12 | {3,9,11,13,14,16,18,20,21,22} |
| 10 | dodecad | 13119052 | 1 | 36 | 12 | {2,3,6,9,10,11,13,19,22,23} |
| 10 | dodecad | 73681 | 1 | 36 | 12 | {0,4,6,7,8,9,10,11,12,16} |
| 10 | dodecad | 1649873 | 1 | 36 | 12 | {0,4,6,7,10,11,13,16,19,20} |
| 10 | dodecad | 3672948 | 1 | 36 | 12 | {2,4,5,6,8,9,11,19,20,21} |
| 10 | non-dodecad | 3870763 | 0 | 36 | 4 | {0,1,3,5,12,16,17,19,20,21} |
| 10 | non-dodecad | 6948209 | 0 | 36 | 4 | {0,4,5,6,8,10,17,19,21,22} |
| 10 | non-dodecad | 1938057 | 0 | 36 | 4 | {0,3,7,9,12,15,16,18,19,20} |
| 10 | non-dodecad | 8817091 | 0 | 36 | 4 | {0,1,6,7,8,11,15,17,18,23} |
| 10 | non-dodecad | 11668523 | 0 | 36 | 4 | {0,1,3,5,10,11,17,20,21,23} |
| 10 | non-dodecad | 7485957 | 0 | 36 | 4 | {0,2,9,11,12,13,17,20,21,22} |
| 10 | non-dodecad | 10754792 | 0 | 36 | 4 | {3,5,6,7,9,11,12,18,21,23} |
| 10 | non-dodecad | 12898056 | 0 | 36 | 4 | {3,8,9,10,11,14,15,18,22,23} |
| 10 | non-dodecad | 10908752 | 0 | 36 | 4 | {4,6,10,12,13,14,17,18,21,23} |
| 10 | non-dodecad | 16124484 | 0 | 36 | 4 | {2,6,9,11,17,18,20,21,22,23} |
| 11 | dodecad | 8770883 | 0 | 0 | 12 | {0,1,6,8,10,12,14,15,16,18,23} |
| 11 | dodecad | 5866558 | 0 | 0 | 12 | {1,2,3,4,5,10,15,16,19,20,22} |
| 11 | dodecad | 3758853 | 0 | 0 | 12 | {0,2,8,9,11,12,14,16,19,20,21} |
| 11 | dodecad | 8477275 | 0 | 0 | 12 | {0,1,3,4,6,9,11,12,14,16,23} |
| 11 | dodecad | 10953315 | 0 | 0 | 12 | {0,1,5,6,9,13,16,17,18,21,23} |
| 11 | dodecad | 14778611 | 0 | 0 | 12 | {0,1,4,5,6,7,15,16,21,22,23} |
| 11 | dodecad | 10438738 | 0 | 0 | 12 | {1,4,6,11,14,16,17,18,19,20,23} |
| 11 | dodecad | 6218376 | 0 | 0 | 12 | {3,7,9,13,14,15,17,18,19,20,22} |
| 11 | dodecad | 3395924 | 0 | 0 | 12 | {2,4,6,8,12,14,15,16,17,20,21} |
| 11 | dodecad | 9259489 | 0 | 0 | 12 | {0,5,6,7,8,11,14,16,18,19,23} |
| 11 | non-dodecad | 8197158 | 2 | 6 | 1 | {1,2,5,10,12,16,18,19,20,21,22} |
| 11 | non-dodecad | 16155809 | 2 | 6 | 1 | {0,5,7,10,15,17,18,20,21,22,23} |
| 11 | non-dodecad | 9672762 | 2 | 6 | 1 | {1,3,4,5,11,12,15,16,17,20,23} |
| 11 | non-dodecad | 3745002 | 2 | 6 | 1 | {1,3,5,6,7,10,13,16,19,20,21} |
| 11 | non-dodecad | 15754524 | 2 | 6 | 1 | {2,3,4,8,10,13,14,20,21,22,23} |
| 11 | non-dodecad | 1265604 | 2 | 6 | 1 | {2,6,7,8,9,10,11,14,16,17,20} |
| 11 | non-dodecad | 9768493 | 2 | 6 | 1 | {0,2,3,5,9,10,11,16,18,20,23} |
| 11 | non-dodecad | 9902634 | 2 | 6 | 1 | {1,3,5,9,11,12,16,17,18,20,23} |
| 11 | non-dodecad | 848665 | 2 | 6 | 1 | {0,3,4,8,9,12,13,14,15,18,19} |
| 11 | non-dodecad | 14853290 | 2 | 6 | 1 | {1,3,5,7,10,13,15,17,21,22,23} |
| 12 | maximal | 3560306 | 0 | 1 | 0 | {1,4,5,6,8,9,12,14,17,18,20,21} |
| 12 | maximal | 5173848 | 0 | 1 | 0 | {3,4,6,9,12,13,14,15,17,18,19,22} |
| 12 | maximal | 9611479 | 0 | 1 | 0 | {0,1,2,4,6,7,11,13,15,17,20,23} |
| 12 | maximal | 1199567 | 0 | 1 | 0 | {0,1,2,3,6,7,8,10,11,14,17,20} |
| 12 | maximal | 6561431 | 0 | 1 | 0 | {0,1,2,4,7,9,10,11,12,18,21,22} |
| 12 | non-maximal | 7548209 | 1 | 0 | 1 | {0,4,5,8,10,11,13,16,17,20,21,22} |
| 12 | non-maximal | 10146187 | 1 | 0 | 1 | {0,1,3,7,8,12,14,15,17,19,20,23} |
| 12 | non-maximal | 4942003 | 1 | 0 | 1 | {0,1,4,5,7,11,13,14,16,17,19,22} |
| 12 | non-maximal | 3681739 | 1 | 0 | 1 | {0,1,3,6,7,8,10,11,13,19,20,21} |
| 12 | non-maximal | 8804045 | 1 | 0 | 1 | {0,2,3,6,7,9,10,12,14,17,18,23} |
| 13 | maximal | 6887999 | 0 | 0 | 1 | {0,1,2,3,4,5,9,11,12,16,19,21,22} |
| 13 | maximal | 15364269 | 0 | 0 | 1 | {0,2,3,5,7,12,13,14,17,19,21,22,23} |
| 13 | maximal | 13978926 | 0 | 0 | 1 | {1,2,3,5,8,10,11,14,16,18,20,22,23} |
| 13 | maximal | 5320179 | 0 | 0 | 1 | {0,1,4,5,6,7,8,10,11,13,16,20,22} |
| 13 | maximal | 6399986 | 0 | 0 | 1 | {1,4,5,6,7,8,9,10,13,15,16,21,22} |

Python re-derivation: of the 75 samples above, 65 were re-analysed by `spotcheck.py`
(5 per size-9 type, 10 per size-10/11 type, 5 per size-12/13 type); every one gave the
identical `(G, #max12, #max13)` triple, and each layer type showed a single distinct
triple. `out/spotcheck.txt` records the run.
