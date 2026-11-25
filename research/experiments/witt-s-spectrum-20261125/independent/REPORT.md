# Independent verification — W_24 Witt design s-parameter game

Scope: independently recompute/verify the claims of
`research/experiments/witt-s-spectrum-20261125/` (raw engine outputs in
`design-kyouen-witt-20261125/output/grundy_w24_s{2..7}.txt`).

All work is inside `research/experiments/witt-s-spectrum-20261125/independent/`.
Nothing outside this directory was modified; nothing was committed.
The board `design-kyouen-witt-20261125/output/board_w24.txt` is only read.

**Overall result: PASS on all five tasks, zero numeric discrepancies.**

Two fully independent implementations were written from scratch (no code from
the original engine was used):

* Python 3.12 (`common.py`, `task1_board.py`, `task2_python.py`,
  `task3_golay.py`, `task5_crosscheck.py`), standard library only;
* C (`witt.c`, gcc 15.2.0, `-O2 -march=native`), two different enumeration
  strategies (incremental DFS, and direct per-size subset scan) plus a mex DP.

Environment: Windows, Python 3.12.13, gcc (MSYS2) 15.2.0.

---

## Task 1 — board is S(5,8,24): PASS

Command: `python task1_board.py` → `out/task1_board.json`

* 759 distinct 8-subsets of {0,…,23}, no repeated point inside a line.
* λ_t (number of octads through a t-subset), t = 0…5:

  | t | distinct t-subsets | λ_t | incidences |
  |---:|---:|---:|---:|
  | 0 | 1 | 759 | 759 |
  | 1 | 24 | 253 | 6,072 |
  | 2 | 276 | 77 | 21,252 |
  | 3 | 2,024 | 21 | 42,504 |
  | 4 | 10,626 | 5 | 53,130 |
  | 5 | 42,504 | 1 | 42,504 |

  All subsets of each size are covered with exactly the S(5,8,24) multiplicity;
  in particular every 5-subset is in exactly one octad.
* Pairwise octad intersections are only 0, 2 or 4, with counts
  11,385 / 170,016 / 106,260 — exactly the values forced by λ2 = 77 and λ4 = 5.
* Derived numbers used below: 21,252 six-subsets and 6,072 seven-subsets lie
  in an octad; a 6- or 7-subset never lies in two octads.

## Task 2 — safe totals and maximal counts, s = 2…6: PASS

Methods: (a) Python increasing-order DFS enumerating every safe set exactly
once, with a full mex DP; (b) C, same task with a separately written engine;
(c) exhaustive per-size subset scans in C (every one of the C(24,k) k-subsets
is inspected for each relevant k — see Task 4/5 for the use of maximal flags).

Claimed vs independently recomputed:

| s | claimed SAFE | ours | claimed maximal | ours | claimed G(∅) | ours | claimed misère | ours |
|---:|---:|---:|---|---:|---:|---:|---:|---:|
| 1 | 25 | 25 | 24 @ size 1 | 24 @ size 1 | 1 | 1 | 0 | 0 |
| 2 | 301 | 301 | 276 @ size 2 | 276 @ size 2 | 0 | 0 | 1 | 1 |
| 3 | 2,325 | 2,325 | 2,024 @ size 3 | 2,024 @ size 3 | 1 | 1 | 0 | 0 |
| 4 | 12,951 | 12,951 | 10,626 @ size 4 | 10,626 @ size 4 | 0 | 0 | 1 | 1 |
| 5 | 168,799 | 168,799 | 113,344 @ size 6 | 113,344 @ size 6 | 0 | 0 | 1 | 1 |
| 6 | 1,937,867 | 1,937,867 | 2,576 @ size 12 | 2,576 @ size 12 | 0 | 0 | 1 | 1 |

Full Grundy distributions also match exactly
(`GRUNDY 0/1` counts: s=2 277/24, s=3 2048/277, s=4 10903/2048,
s=5 124247/44552, s=6 955651/982216; s=1 24/1).
Because for each s every maximal safe set has one fixed size m, the game is
graded and Grundy/parity values are forced by `m mod 2`; this is consistent
with the computed distributions and with G(∅), but the distributions were
computed by a full DP, not assumed.

Per-size safe counts (all match the `SIZE` lines of the reported files):

* s=2: 1, 24, 276; s=3: 1, 24, 276, 2,024; s=4: 1, 24, 276, 2,024, 10,626.
* s=5: … 42,504, 113,344.
* s=6: 1, 24, 276, 2,024, 10,626, 42,504, 134,596, 340,032, 637,560,
  566,720, 170,016, 30,912, 2,576.

Structural checks:

* s = 2,3,4: every (s+1)-set lies in an octad (λ3, λ4, λ5 > 0), so no safe
  (s+1)-set exists (verified exhaustively: 0 safe 3-sets for s=2, 0 safe
  4-sets for s=3, 0 safe 5-sets for s=4) and the maximal safe sets are
  exactly all s-sets (276 / 2,024 / 10,626).
* s = 5: C(24,6) − 759·C(8,6) = 134,596 − 21,252 = 113,344 octad-free 6-sets.
  All 113,344 are safe and every one is maximal: for each such 6-set and each
  of the 18 outside points, some octad through that point meets the 6-set in
  5 points (direct check in Python and in the C brute scanner). No safe
  7-set exists, so there is nothing larger.
* s = 6: safe sizes 7 and 8 agree with the exact formulas
  346,104 − 6,072 = 340,032 and 735,471 − 97,911 = 637,560; sizes 9,10,11
  are 2,576·C(12,3) = 566,720, 2,576·C(12,2) = 170,016, 2,576·12 = 30,912
  and every safe 9/10/11-set is a subset of a dodecad (injectivity follows
  from the code minimum distance 8); size 12 is 2,576 (dodecads). Exhaustive
  scans confirm all of these and that no safe 13-set exists.

## Task 3 — dodecad / Golay identification: PASS

Command: `python task3_golay.py` → `out/task3_golay.json`

* The F2-span of the 759 octads has rank 12. Enumerating all 4,096 codewords
  gives the weight enumerator

  | weight | 0 | 8 | 12 | 16 | 24 |
  |---|---:|---:|---:|---:|---:|
  | count | 1 | 759 | 2,576 | 759 | 1 |

  all weights ≡ 0 mod 4, and the code is self-orthogonal; being [24,12] this
  identifies it as the binary Golay code (doubly even, self-dual).
  The weight-8 words are exactly the 759 octads.
* Weight-12 words (dodecads) = 2,576. Independently, symmetric differences of
  octad pairs with |A∩B| = 2 give the same 2,576 sets (family equality
  checked). Each dodecad arises from exactly 66 such pairs
  (170,016 pairs / 2,576 = 66; every multiplicity is 66). No weight-12 word
  is missing from the pair construction and vice versa.
* For every dodecad D and every octad B, |D∩B| is even and lies in {2,4,6};
  the per-dodecad profile is identical for all 2,576:
  `2:132, 4:495, 6:132` (sum 759). In particular no octad meets a dodecad in
  0 or 8 points, so every dodecad is safe for s=6.
* Every dodecad is maximal for s=6: for each of its 12 outside points there is
  an octad meeting D in 6 points and containing that point (checked for all
  2,576). Complements of dodecads are dodecads.
* Consequently every k-subset of a dodecad (k = 9,10,11,12) is safe; these
  families have 2,576·C(12,k) distinct members each (checked, and injective).

## Task 4 — s=6 maximal sets are exactly the dodecads: PASS (exhaustive)

This was checked **exhaustively, not by sampling**:

* Command: `.\witt.exe brute 6 12` — all 2,704,156 twelve-subsets of
  {0,…,23} were scanned against all 759 octads:
  exactly 2,576 are safe (≤6 points in every octad), all 2,576 are dodecads
  (0 safe 12-sets are non-dodecads), and all 2,576 are maximal
  (`SAFE 2576 MAXIMAL 2576`, `DODECAD_HITS 2576 SAFE_NOT_DODECAD 0`).
* `.\witt.exe brute 6 13` — all 2,496,144 thirteen-subsets: 0 safe, hence no
  safe set of size ≥13 (safe sets are downward closed).
* `.\witt.exe brute 6 k` for every k = 1…11: maximal count is 0 in every
  size, and the safe counts are exactly the totals listed under Task 2.
* The C DFS engine independently reports the only maximal safe sets at
  size 12, count 2,576, and the Python full DP agrees.

Therefore a 12-set is a maximal safe set for s=6 iff it is a dodecad; no
other 12-set is maximal (every non-dodecad 12-set is unsafe, and no safe
12-set can be extended). This is a complete verification, not a sample.

## Task 5 — s=7 totals, maximal counts, Grundy and misère: PASS

Two independent full computations (C DFS+mex DP, and C `fullbrute` which
enumerates every k-subset by direct scan for k = 0…14 and then runs the same
mex recursion) give identical results, as does the exhaustive per-size scan:

* SAFE = **7,932,035** (both engines).
* Maximal counts: size 12 = **1,020,096**, size 13 = **30,912**; maximal
  count is 0 for every other size (checked exhaustively for k = 1…11 and
  k = 12,13; k ≤ 6 cannot be maximal since every safe set of size ≤ 6 has a
  safe extension, and no safe 14-set exists).
* Grundy distribution: **0: 3,662,291; 1: 1,662,832; 2: 2,606,912**
  (sum 7,932,035). No value exceeds 2.
* G(∅) = **0**; misère outcome of ∅ = **0** (first player loses both).
  Misère total distribution: 0: 3,123,907; 1: 4,808,128.
* Per-size Grundy-0 counts match the fourth column of the claimed `SIZE`
  lines: sizes 0…13 = 1, 0, 276, 0, 10,626, 0, 134,596, 0, 734,712, 0,
  1,700,160, 30,912, 1,020,096, 30,912.

Independent checks of the s=7 numbers:

* Exhaustive per-size scans (all C(24,k) subsets): k=7…11 safe counts
  346,104 / 734,712 / 1,295,360 / 1,870,176 / 2,071,104 with maximal 0;
  k=12: safe 1,393,616, maximal 1,020,096; k=13: safe 30,912, maximal
  30,912; k=14: safe 0. These are obtained without the DFS engine.
* Analytic cross-checks: sizes 0…7 are all C(24,k); sizes 8,9,10,11 satisfy
  C(24,k) − 759·C(16,k−8) (no two octads fit in ≤11 points); size 12 is
  C(24,12) − [759·C(16,4) − 106,260 + 35,420] = 2,704,156 − 1,310,540 =
  1,393,616, where 106,260 is the number of octad pairs with |A∩B|=4 and
  35,420 is the number of 12-sets containing exactly three octads
  (each 12-set containing ≥2 octads contains exactly 3; independently
  verified in Task 3). Size 13 is exhaustive. The sum of these exact counts
  is 7,932,035.
* DP value cross-check: 72 safe positions (sizes 9…13) were recomputed from
  scratch in Python (direct octad-intersection safety tests, recursive mex,
  no use of the C table except for comparison) — Grundy and misère all agree.
* Structural DP checks: all 30,912 size-13 positions have Grundy 0
  (terminal); the size-12 Grundy-0 count equals the independently computed
  maximal count 1,020,096 and the remaining 373,520 have Grundy 1.

The fact that maximal sizes have mixed parity (12 and 13) is consistent with
the presence of Grundy values 2; the full DP confirms the exact count.

## Claim comparison

Command: `python compare_claims.py` → `out/compare_claims.json`

For s = 2…7 the claimed raw files were parsed and compared field by field with
the independent C results: `POINTS`, `CIRCLES`, `SAFE`, every `SIZE` line
(size, count, maximal count, Grundy-0 count), the `GRUNDY` totals and
`ROOT` (Grundy, misère). The aggregated values in
`witt-s-spectrum-20261125/output/spectrum.json` (safe, size_total,
maximal_sizes, grundy, root_grundy, root_misere) were compared too.

**`discrepancies: []`, PASS.**

## Discrepancies and notes

* **No numeric discrepancies were found.** All five tasks PASS.
* The claimed raw files exist only for s = 2…7. There is no
  `grundy_w24_s1.txt` (nor s=8) in the claimed output directory; the s=1
  claim comes from the README/report table. s=1 was nevertheless verified
  independently: safe 25, maximal 24 singletons, Grundy {0:24, 1:1},
  G(∅)=1, misère 0. s=8 was outside the requested tasks and not checked
  (its claim is trivial: all sets safe, the full set the only maximal set).
* The raw claimed files have no `MISERE` line; misère values come from the
  README table and `spectrum.json`. They were verified by full DP.
* The fourth `SIZE` column of the claimed files is the number of Grundy-0
  positions of that size; it matched our DP per-size values for every s.

## Artifacts

| file | content |
|---|---|
| `common.py` | board loader + independent DFS enumeration + mex DP helpers |
| `task1_board.py` / `out/task1_board.json` | S(5,8,24) verification |
| `task2_python.py` / `out/task2_python_*.json` | Python full solve (s = 1…6) |
| `task3_golay.py` / `out/task3_golay.json` | Golay code, dodecads, s=7 12-set counting |
| `witt.c` / `witt.exe` | C engine: DFS, fullbrute, brute, dodecads, code |
| `task5_crosscheck.py` / `out/task5_crosscheck.json` | s=7 DP sample cross-check |
| `compare_claims.py` / `out/compare_claims.json` | claim vs recomputation |
| `run_all.ps1` | full reproduction |
| `out/c_full_s{1..7}.txt`, `out/c_fullbrute_s{6,7}.txt` | C engine outputs |
| `out/c_brute_*.txt` | exhaustive subset-scan outputs |
| `out/grundy_s7.bin`, `out/misere_s7.bin` | dumped s=7 DP tables (16 MiB each; deleted after the cross-check, regenerate with `witt.exe full 7 dump`) |

## Commands (observed run times)

```powershell
cd research/experiments/witt-s-spectrum-20261125/independent
gcc -O2 -march=native -o witt.exe witt.c                     # ~1 s
python task1_board.py                                        # ~1 s
python task2_python.py 1 2 3 4                               # ~5 s
python task2_python.py 5                                     # ~2 min
python task2_python.py 6                                     # ~13 min
python task3_golay.py                                        # ~23 s
foreach ($s in 1..7) { .\witt.exe full $s }                  # s=7 ~8 s
.\witt.exe fullbrute 6                                       # ~5 s
.\witt.exe fullbrute 7                                       # ~11 s
foreach ($k in 1..13) { .\witt.exe brute 6 $k }              # ~3 s total
foreach ($k in 1..14) { .\witt.exe brute 7 $k }              # ~6 s total
.\witt.exe full 7 dump                                       # writes out/*_s7.bin
python task5_crosscheck.py                                   # ~8 s
python compare_claims.py                                     # <1 s
```

`run_all.ps1` runs the whole sequence. The two 16 MiB `*_s7.bin` dumps are
binary intermediates and can be deleted; regenerate them with
`.\witt.exe full 7 dump` before `task5_crosscheck.py`.

## Reproduction / independence notes

* The board is only read; no files outside this directory were touched
  (`git status` shows only the untracked `independent/` directory).
* No commits were made.
* The Python and C verifiers share no code. Within C, `full` (incremental
  DFS) and `fullbrute` (direct subset scan) are two different enumerations
  of the safe-set family; they agree on every size, maximal count and DP
  distribution for s=6 and s=7.
* The mex DP logic itself was cross-checked against an independent recursive
  Python implementation on 72 sampled positions and against the structurally
  forced values at sizes 12 and 13.
