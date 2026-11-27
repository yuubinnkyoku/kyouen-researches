# Independent verification of K1364 — AG(2,5), s=4 Grundy decomposition

**Verdict: PASS. Every number in the claim checks out; no discrepancy was found.**
The published engine reproduced the claimed output byte for byte, a separately
written solver reproduced the complete size/Grundy table, and the size counts
(hence the 16,249,926 total) were re-derived by two routes that do not use
either Grundy solver.

- Date: 2026-11-28
- Claim: `research/knowledge/items/K1364-ag2q5-s4-grundy-decomposition.md`
- Board: `research/experiments/s-parameter-kyouen-20261125/output/board_ag2q5.txt`
  (SHA-256 `b6fe706177f8d9d19753d770772fb3e7c40f9161bc941aec4bca8f4cd1039b1c`, 25 points)
- Claimed artifact: `research/experiments/ag2q5-s4-20261128/output/gsize_ag2q5_s4.txt`
  (SHA-256 `fb500c8d6f6b92b95849aee53b0f14766e94aa9e7612c697bc3c5d829cbd60bf`, 1002 bytes)
- Everything below lives in `research/experiments/ag2q5-s4-20261128/independent/`.
  Nothing outside that directory was modified and nothing was committed.

---

## 1. The board is AG(2,5)

`verify_board.py` parses the board from first principles and checks:

| check | result |
|---|---|
| header `25 30`; 30 lines, exactly 5 distinct points each, ids in 0..24 | pass |
| no duplicate lines; every point on exactly 6 lines | pass |
| every one of the C(25,2) = 300 point pairs lies on exactly one line | pass |
| parallelism (“disjoint or equal”) has 6 classes of 5 lines | pass |
| each parallel class is a partition of the 25 points; lines from different classes meet in exactly one point | pass |

The six parallel classes (line indices) are
`[0,26,27,28,29]`, `[1,7,13,19,25]`, `[2,8,14,20,21]`, `[3,9,15,16,22]`,
`[4,10,11,17,23]`, `[5,6,12,18,24]`.

The script then constructs an explicit affine coordinate certificate: with
`O = 0`, the two independent lines through `O` with indices 0 and 1 as axes,
`e1 = 1`, `e2 = 5`, it searches the 24×24 affine labellings of the two axes.
The labelling `axis1 = (0,1,2,3,4)`, `axis2 = (0,5,10,15,20)` realises every
one of the 30 board lines as exactly one of the AG(2,5) lines
`{x = c}`, `{y = c}`, `{y = m x + c}` over F_5, with all 30 types distinct and
complete. In these coordinates the board is the standard plane with point id
`p = 5*y + x` (rows `y = c`, columns `x = c`, and the 20 lines of slopes
1,2,3,4). Hence the board is AG(2,5), not merely a 2-(25,5,1) design.

Certificate output: `board_affine_map.json` (point coordinates and the line
equation attached to every board line).

---

## 2. Byte identity of the published engine output

`grundy_s_stats_published.exe` was compiled here from the published source
`research/experiments/pg2q7-cap-game-20261125/scripts/grundy_s_stats.c`
(SHA-256 `fe44d80c3249c8d52e5542766021314c926b0608a32323ffd95fd9893d57b85c`)
with `gcc 15.2.0 -O2`, and run as

```
grundy_s_stats_published.exe <board_ag2q5.txt> 4
```

Its output, `published_run.txt`, is **byte-identical** to the claimed file:

```
claim      sha256 = fb500c8d6f6b92b95849aee53b0f14766e94aa9e7612c697bc3c5d829cbd60bf
published  sha256 = fb500c8d6f6b92b95849aee53b0f14766e94aa9e7612c697bc3c5d829cbd60bf
size       = 1002 bytes both
```

This covers every `SIZE`, `GRUNDY`, `GSIZE`, `ROOT`, `FIRSTMOVE`, `PROBE` and
`PROBE_CHILDREN` line, i.e. the claim was produced by exactly this engine on
exactly this board.

*Line-ending note.* The on-disk claim artifact uses CRLF; the git blob at
`HEAD` is the same 54 lines with LF (948 bytes, SHA-256
`a170ed40de7d480c88f215cf621754a59fcdcaeb1ab63d7fd16731c0bb38162d`).
Text is identical (`disk.replace(b"\r\n", b"\n") == HEAD_blob`).
The byte-identity above is against the on-disk artifact, which is what the
task names as the claimed file.

---

## 3. Independent reproduction of the full table

A second solver, `ag2q5_s4_independent.c`, was written from scratch with a
different algorithm and data structures:

| | published engine | independent engine |
|---|---|---|
| enumeration | DFS with incremental line counters, size buckets | top-down recursion with memoisation |
| memoisation | open-addressing hash maps, two buckets alive | direct `2^25`-byte Grundy table indexed by point mask |
| legality test | counts per line / popcount of circle masks | compare point-removed 4-point line masks |
| evaluation order | bottom-up from the maximum size | memoised depth-first from the empty set |
| maximum size | discovered by enumeration | discovered by the same run |

It was validated against a trivially correct brute-force Python solver on
AG(2,2) s=1 and AG(2,3) s=2 (section 8), and it reproduces the claimed table
exactly. Runtime on this host: ≈8.9 s (published engine ≈0.33 s).

The complete claimed distribution, reproduced value for value:

| k | positions | maximal | G0 | G1 | G2 | G3 |
|---:|---:|---:|---:|---:|---:|---:|
| 0 | 1 | 0 | 1 | 0 | 0 | 0 |
| 1 | 25 | 0 | 0 | 25 | 0 | 0 |
| 2 | 300 | 0 | 300 | 0 | 0 | 0 |
| 3 | 2,300 | 0 | 0 | 2,300 | 0 | 0 |
| 4 | 12,650 | 0 | 12,650 | 0 | 0 | 0 |
| 5 | 53,100 | 0 | 0 | 53,100 | 0 | 0 |
| 6 | 176,500 | 0 | 176,500 | 0 | 0 | 0 |
| 7 | 475,000 | 0 | 0 | 475,000 | 0 | 0 |
| 8 | 1,047,375 | 0 | 1,047,375 | 0 | 0 | 0 |
| 9 | 1,898,000 | 0 | 0 | 1,898,000 | 0 | 0 |
| 10 | 2,809,700 | 0 | 2,809,700 | 0 | 0 | 0 |
| 11 | 3,340,500 | 0 | 0 | 3,268,500 | 0 | 72,000 |
| 12 | 3,089,000 | 0 | 3,010,000 | 7,000 | 72,000 | 0 |
| 13 | 2,103,000 | 0 | 7,000 | 1,958,000 | 6,000 | 132,000 |
| 14 | 961,500 | 1,500 | 868,500 | 12,000 | 81,000 | 0 |
| 15 | 252,600 | 6,600 | 6,600 | 246,000 | 0 | 0 |
| 16 | 28,375 | 28,375 | 28,375 | 0 | 0 | 0 |

Grand totals: **G0 = 7,967,001**, **G1 = 7,919,925**, **G2 = 159,000**,
**G3 = 204,000**; sum **16,249,926** = `SAFE`. Maximum Grundy value **3**,
maximum safe size **16**.

`my_run.txt` is the independent solver's output; `compare.py` asserts equality
of every `SIZE` tuple (count, maximal, g0), every `GRUNDY` total and every
`GSIZE` cell against the claim. It also checks the companion JSON
`../output/ag2q5_s4_gsize.json` (SHA-256
`5c37647bbf3da264b8b3b1cd829f2d5cece9b08cae807b155205009802d61b1f`) and finds
it consistent with the text table.

---

## 4. Arithmetic self-consistency

For the claimed table (`compare.py`, all 54 checks pass):

- for every k, the G counts at that size sum to the `SIZE` count;
- for every k, the `g0` column equals the number of G0 positions;
- for every Grundy value, the counts over all sizes equal the `GRUNDY` total;
- Σ_k count = 16,249,926 = `SAFE` = Σ_g `GRUNDY`;
- the per-size counts are exactly the 17 stated values, in particular
  3,340,500 (k=11), 3,089,000 (k=12), 2,103,000 (k=13), 961,500 (k=14),
  252,600 (k=15), 28,375 (k=16);
- every stated G row sums correctly, e.g. k=13: 7,000+1,958,000+6,000+132,000
  = 2,103,000;
- maximal counts are 14:1,500, 15:6,600, 16:28,375 and zero elsewhere;
- k is present for exactly 0..16; the maximum Grundy is 3.

---

## 5. Maximum safe size and maximal counts (independent proof)

`count_complements.c` enumerates *complements*, a completely different search
space from the Grundy solvers. Since a safe set S is exactly a set whose
complement B meets every line (if a line missed B it would be a full line in S),
the following are equivalent:

- S safe of size k ⟺ B = P∖S is a blocking set of size 25−k;
- S maximal (no legal move) ⟺ B is a **minimal** blocking set.

The second equivalence: adding `p ∉ S` is illegal iff some line through p
already carries 4 points of S, i.e. that line meets B only in p; S is maximal
iff every `p ∈ B` has such a witness line, which is exactly minimality of B.

Result of exhaustive enumeration of all subsets of size m = 0..14
(blocking = meets all 30 lines, minimal = no proper subset is blocking):

| m = 25−k | blocking sets | minimal blocking sets | claimed safe k | claimed maximal k |
|---:|---:|---:|---:|---:|
| 0..8 | **0** | 0 | (k ≥ 17 impossible) | — |
| 9 | 28,375 | 28,375 | 16 | 28,375 |
| 10 | 252,600 | 6,600 | 15 | 6,600 |
| 11 | 961,500 | 1,500 | 14 | 1,500 |
| 12 | 2,103,000 | 0 | 13 | 0 |
| 13 | 3,089,000 | 0 | 12 | 0 |
| 14 | 3,340,500 | 0 | 11 | 0 |

Therefore:

1. **No blocking set has size ≤ 8**, and blocking sets of size 9 exist
   (28,375). Hence the minimum blocking set has size 9 and the **maximum safe
   size is exactly 16 = 25 − 9**. This is an exhaustive proof for this board,
   not a statistical statement.
2. The blocking counts m = 9..14 are exactly the claimed safe counts
   k = 16..11, independently confirming the upper end of the size distribution
   (and, with the closed forms below, all sizes).
3. The minimal blocking counts 28,375 / 6,600 / 1,500 at m = 9,10,11 match the
   claimed maximal counts at k = 16,15,14, and minimality is absent at
   m = 12,13,14 (i.e. no maximal positions of size 13,12,11 measured this way).
4. In particular **all 28,375 size-16 positions are maximal**, and since a
   maximal position has no moves, `mex ∅ = 0`: all are G0. The claimed
   `N = maximal = G0 = 28,375` is consistent.

The DFS solvers independently report the same maximal column for every size
(1,500 / 6,600 / 28,375 and 0 for k ≤ 13), so the two methods agree.

The complement counter was itself validated on AG(2,3) s=2: it reproduces the
brute-force safe counts (54, 72, 36, 9 for k = 4,3,2,1) as blocking counts of
complements of size 5,6,7,8, and minimal blocking sets of size 5 = 54 = maximal
4-sets.

---

## 6. Independent recount of the size distribution

The two routes below do not use either Grundy solver.

### 6a. Closed form for k = 0..10

A k-set is unsafe iff it contains a full line. For k ≤ 10 at most two lines fit
in one k-set (the union of any three lines has at least 12 points), so
inclusion–exclusion stops at pairs. Of the C(30,2) = 435 line pairs, 375 meet
in one point (union size 9) and 60 are parallel (union size 10). Hence

```
safe(k) = C(25,k) − 30·C(20,k−5) + 375·C(16,k−9) + 60·C(15,k−10)
```

(with C(a,b) = 0 for b < 0). This gives exactly

| k | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| formula | 1 | 25 | 300 | 2,300 | 12,650 | 53,100 | 176,500 | 475,000 | 1,047,375 | 1,898,000 | 2,809,700 |

all equal to the claim.

### 6b. Complement counts for k = 11..16

From section 5, the blocking counts at m = 14,13,12,11,10,9 are
3,340,500 / 3,089,000 / 2,103,000 / 961,500 / 252,600 / 28,375, exactly the
claimed counts for k = 11,12,13,14,15,16.

Together, 6a and 6b independently reproduce **all 17 size counts**, hence
`1 + 25 + ... + 28,375 = 16,249,926`. No discrepancy.

---

## 7. Structural claims

| claim | result |
|---|---|
| k = 0..10 parity: even k → all G0, odd k → all G1 | confirmed for every k (single-value distribution) |
| G3 occurs only at sizes 11 and 13 | confirmed: G3 sizes = {11, 13}; 72,000 at k=11, 132,000 at k=13 |
| all 28,375 size-16 positions are maximal G0 | confirmed: N = maximal = G0 = 28,375, no other Grundy value at k=16 |
| maximum safe size 16 | confirmed by the blocking-set proof (section 5) |
| maximum Grundy value 3 | confirmed: GRUNDY lines only for 0,1,2,3 |
| maximal sizes 14, 15, 16 | confirmed: maximal counts 1,500 / 6,600 / 28,375; zero for k ≤ 13 |

The parity law is consistent with the computed table (for k ≤ 10 every child
has the opposite parity value, and every position has a move because the
maximum size is 16); the table itself is the primary evidence.

---

## 8. Validation of the two solvers

**Small-board brute force.** `validate_small.py` enumerates *all* 2^n subsets
for AG(2,2) s=1 (n=4) and AG(2,3) s=2 (n=9), computes Grundy values with a
short independent Python recursion, and compares the complete output of both
C engines:

| board | safe | max size | root G | G counts | both engines |
|---|---:|---:|---:|---|---|
| AG(2,2), s=1 | 5 | 1 | 1 | G0=4, G1=1 | match brute force |
| AG(2,3), s=2 | 172 | 4 | 0 | G0=91, G1=81 | match brute force |

**Permutation invariance.** `permute_test.py` relabels the 25 points with a
fixed pseudo-random permutation (seed 20261128) and reruns both engines. The
game is isomorphic, so the full `SIZE`/`GRUNDY`/`GSIZE` distribution must be
unchanged; both engines reproduce the claimed distribution on the relabelled
board.

---

## 9. What is proved, and what is “computed”

- **Board = AG(2,5):** proved by exhaustive structural checks plus an explicit
  affine coordinate certificate (all 30 lines become the 30 lines of F_5²).
- **Maximum safe size is 16:** proved by exhaustive enumeration of complements:
  no blocking set of size ≤ 8, and blocking sets of size 9 exist. This is a
  finite proof for this board.
- **Size distribution and total 16,249,926:** proved by two independent
  exhaustive/closed-form counts (section 6), both agreeing with the claim and
  with the solvers.
- **Maximal counts:** proved by exhaustive minimal-blocking-set enumeration,
  agreeing with the solvers.
- **Grundy distribution (the assignment of values 0..3 to all 16,249,926
  positions):** established by exhaustive computation with two independently
  written programs. The published program's output is byte-identical to the
  claim; the independent program agrees on every cell; both were validated
  against brute force on small affine planes and under point relabelling.
  This is a complete finite verification, but — as with any large computed
  table — it is a computational proof whose validity rests on the programs
  being correct. No counterexample or inconsistency was found.
- **Structural corollaries** (parity k ≤ 10, G3 only at 11/13, all size-16
  maximal G0, max G = 3) follow from the verified table.

---

## 10. Discrepancies

**None.** All 54 checks in `compare.py` pass, the published engine output is
byte-identical to the claim, the independent solver agrees on every
`SIZE`/`GRUNDY`/`GSIZE` cell, and the size counts and maximal counts were
re-derived independently. The K1364 numbers are confirmed as stated.

Minor presentation note (not a mathematical discrepancy): the claim artifact
is stored with CRLF in the working tree and LF in git; the 1002-byte byte
identity is with the working-tree artifact. The companion JSON is consistent
with the text table.

---

## 11. Reproduce

From the repository root (Windows, `gcc` and `python` on `PATH`):

```powershell
pwsh -File research/experiments/ag2q5-s4-20261128/independent/run_all.ps1
```

This runs, in order: `verify_board.py`; builds the three C programs; runs the
independent solver, the published solver and the complement counter; then
`compare.py` (54 checks), `validate_small.py` and `permute_test.py`.
Alternatively, from inside this directory:

```powershell
python verify_board.py
gcc -O2 -o ag2q5_s4_independent.exe ag2q5_s4_independent.c
gcc -O2 -o count_complements.exe count_complements.c
.\ag2q5_s4_independent.exe <board> 4 > my_run.txt
.\count_complements.exe <board> 4 > complements_run.txt
gcc -O2 -o grundy_s_stats_published.exe ..\..\pg2q7-cap-game-20261125\scripts\grundy_s_stats.c
grundy_s_stats_published.exe <board> 4 > published_run.txt
python compare.py
python validate_small.py
python permute_test.py
```

The claim itself is never written to; `compare.py` only reads it.

---

## Appendix — files and hashes

| file | role | SHA-256 |
|---|---|---|
| `../output/gsize_ag2q5_s4.txt` | claim (read-only) | `fb500c8d…cbd60bf` |
| `published_run.txt` | published engine rerun (byte-identical) | `fb500c8d…cbd60bf` |
| `my_run.txt` | independent solver output | `4082220f…61fc413c` |
| `complements_run.txt` | blocking/minimal-blocking census | `e8c2c87e…ef7181113` |
| `ag2q5_s4_independent.c` | independent Grundy solver | `6895f25a…9d200cb` |
| `count_complements.c` | complement / minimal blocking sets | `404dce67…f61bd6ad2f` |
| `verify_board.py` | AG(2,5) certificate | — |
| `compare.py` | claim/arithmetic/structure checks (54) | — |
| `validate_small.py` | brute-force engine validation | — |
| `permute_test.py` | point-relabelling invariance | — |
| `board_affine_map.json` | explicit affine coordinates | — |
| `verification_summary.json` | machine-readable list of all checks | — |
