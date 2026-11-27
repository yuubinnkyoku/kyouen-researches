# Independent verification — K1359: PG(2,5), s=3 Grundy decomposition

**Verdict: PASS — no discrepancy found.**

Every numerical claim in K1359 was reproduced exactly by three computations, one of
which is a complete pure-Python dynamic program over all 7,906,892 safe positions.
All 42 `SIZE`/`GRUNDY`/`GSIZE` lines (plus the four header/root lines) agree across
the claimed file, the recompiled published engine, the independent C implementation
and the complete Python implementation.

- Verification was performed only inside
  `research/experiments/pg2q5-s3-20261128/independent/` (created for this task).
- No commits were made; no files outside that directory were written.
- All programs and outputs below live in `independent/` (or `independent/out/`).

## Inputs

| File | SHA-256 |
|---|---|
| `projective-blocking-kyouen-20261125/output/board_pg2q5.txt` | `6154A5A92E421EDF6265DA439D2DA086CC636C1A36233B2B70839718BD27A5B0` |
| `pg2q5-s3-20261128/output/gsize_pg2q5_s3.txt` (claim) | `49EDB24315E4DCA35086C8E7EE62CDA6F28B16A266D5CA993E1DE9CC16D57715` |

The claimed table has 49 lines: 4 header/root lines, 12 `SIZE`, 5 `GRUNDY`,
25 `GSIZE`, and 3 extra diagnostics (`FIRSTMOVE`, `PROBE`, `PROBE_CHILDREN`)
that are not part of the K1359 decomposition. 46 "core" lines are compared below.

## 1. The board is PG(2,5)

`verify_board.py` parses the board independently of every C program and checks:

- header `31 31`; exactly 31 lines; no trailing tokens;
- every line has 6 distinct points in `0..30`; all 31 lines are distinct;
- every point lies on exactly 6 lines (186 incidences);
- all 465 unordered point pairs are covered **exactly once**
  (31·C(6,2) = 465 = C(31,2));
- every pair of distinct lines meets in **exactly one** point (465/465 pairs).

This is a 2-(31,6,1) design, i.e. a projective plane of order 5. Since 5 is prime,
the projective plane of order 5 is unique up to isomorphism (classical theorem),
so the board is PG(2,5). (The incidence axioms themselves were checked exhaustively;
only the final "= PG(2,5)" identification uses the uniqueness theorem.)

## 2. Independent reproduction of the size-by-size distribution

Three implementations were run on the same board with `s = 3`:

**A. Published engine.** `grundy_s_stats.c` from the pg2q7 experiment was recompiled
here (`gcc 15.2.0 -O2`) and run with `board_pg2q5.txt 3`.
Runtime 9.16 s. Its output file is **byte-for-byte identical** to the claimed file:
both have SHA-256 `49EDB243…D57715` (all 49 lines, including the three diagnostics).
A second run was identical.

**B. Independent C implementation** (`indep_verify.c`). No code shared with A:
separate `fgets`/`strtol` parser; depth-first enumeration in increasing point order;
legality tested point-by-point (a point `p` may be added iff every line through `p`
already holds at most 2 points of the position); per-size arrays of 64-bit masks kept
sorted, child values looked up by binary search; mex and misère computed bottom-up.
Runtime ≈ 18 s. The program aborts on a duplicate position, a missing child or a
parse inconsistency; it did not abort. Output = 46 core lines.

**C. Complete pure-Python dynamic program** (`full_python_dp.py`). Top-down from the
empty position with memoisation; Python integers and recursive mex; computes Grundy
value and misère outcome for every reachable position. Since every subset of a safe
position is safe, the traversal reaches **all** safe positions: 7,906,892 memo
entries in 237.1 s. Output = 46 core lines. This is a different traversal direction
and a different implementation from B.

Raw comparison of the 46 core lines (`POINTS`, `CIRCLES`, `SAFE`, `ROOT`,
12 `SIZE`, 5 `GRUNDY`, 25 `GSIZE`):

| Source | core lines | vs claimed |
|---|---|---|
| published engine rerun | 46 | identical (whole 49-line file byte-identical) |
| independent C | 46 | identical |
| complete Python DP | 46 | identical |

The independent C and Python outputs are themselves byte-identical
(SHA-256 `12582CD0…B93C6`).

### Reproduced distribution

| k | G0 | G1 | G2 | G3 | G4 | total = SIZE count | maximal |
|---:|---:|---:|---:|---:|---:|---:|---:|
| 0 | 0 | 1 | 0 | 0 | 0 | 1 | 0 |
| 1 | 31 | 0 | 0 | 0 | 0 | 31 | 0 |
| 2 | 0 | 465 | 0 | 0 | 0 | 465 | 0 |
| 3 | 4,495 | 0 | 0 | 0 | 0 | 4,495 | 0 |
| 4 | 0 | 0 | 31,000 | 0 | 0 | 31,000 | 0 |
| 5 | 111,600 | 46,500 | 0 | 0 | 0 | 158,100 | 0 |
| 6 | 15,500 | 3,100 | 186,000 | 387,500 | 0 | 592,100 | 0 |
| 7 | 480,500 | 697,500 | 186,000 | 0 | 186,000 | 1,550,000 | 0 |
| 8 | 465,000 | 232,500 | 186,000 | 1,674,000 | 0 | 2,557,500 | 0 |
| 9 | 666,500 | 620,000 | 930,000 | 0 | 0 | 2,216,500 | 93,000 |
| 10 | 248,000 | 483,600 | 0 | 0 | 0 | 731,600 | 248,000 |
| 11 | 65,100 | 0 | 0 | 0 | 0 | 65,100 | 65,100 |
| **total** | **2,056,726** | **2,083,666** | **1,519,000** | **2,061,500** | **186,000** | **7,906,892** | **406,100** |

This is exactly the K1359 table, cell by cell.

## 3. Maximal positions and maximum safe size

- Sizes present: 0 through 11; the enumeration finds **no safe position of size 12**,
  so the maximum safe size is 11.
- Positions with no legal extension ("maximal"): size 9: **93,000**,
  size 10: **248,000**, size 11: **65,100**; zero at every other size.
  Reproduced by both independent C and Python (the C engine counts maximality
  directly from the absence of legal moves, independently of the Grundy value).
- Consistency: every maximal position has Grundy 0. At sizes 10 and 11 the maximal
  count equals the entire G0 count (248,000 and 65,100); this is forced, because
  every move from a size-10 position leads to size 11, where every child has G0.
  At size 9 only 93,000 of the 666,500 G0 positions are maximal.
- Terminology: "maximal" here means *no legal extension*, not maximum cardinality.

## 4. Structural claims

**All 4-caps have G = 2.** Interpreting "4-cap" as a safe position of size 4, there
are exactly 31,000 of them, and the complete enumeration gives
`GSIZE 4 2 31000`: **every one** has Grundy 2 (not a sample; the total 31,000 is
also confirmed by direct enumeration of all 4-subsets and by
C(31,4) − 31·C(6,4) = 31,465 − 465 = 31,000). As an additional independent check,
25 random size-4 positions were evaluated by full-upset DP in Python (each upset
18,493 or 26,499 nodes); all 25 returned 2, and the independent C probe agreed.

**G = 4 only at size 7.** The GSIZE table has exactly one G4 cell:
`(k,g) = (7,4)` with count 186,000. No other size has any G4, and no position has
Grundy > 4; the maximum Grundy value is 4.

**Sample cross-check of the whole table.** 63 random safe positions at sizes
3–11 (25 at size 4, five at each of sizes 5–11, three at size 3) were evaluated
by the Python full-upset DP and compared with the independent C values:
**63/63 agree, 0 mismatches** (`out/sample_check.json`).

## 5. Arithmetic consistency

All of the following were checked mechanically (`check_claims.py`; 24/24 checks pass):

- For every size `k`, the sum of its `GSIZE k g` counts equals its `SIZE k` count
  (12/12 sizes), and `SIZE k`'s fourth field (G0 count) equals `GSIZE k 0`.
- For every Grundy value `g`, the sum of the `GSIZE` cells with that `g` equals the
  `GRUNDY g` total (5/5 values).
- `Σ SIZE counts = Σ GRUNDY totals = SAFE = 7,906,892`.
- Grand totals: G0 2,056,726 / G1 2,083,666 / G2 1,519,000 / G3 2,061,500 /
  G4 186,000, summing to 7,906,892.
- Root (empty position): Grundy 1, misère win 1 — reproduced by all three
  implementations (Python now computes the misère bit too).
- The claimed JSON companion `pg2q5_s3_gsize.json` matches the text table
  (all `N`, `maximal`, `N_g` entries).
- Independent count cross-checks: direct `itertools.combinations` enumeration
  reproduces the size counts for k = 4,5,6,7 (31,000 / 158,100 / 592,100 /
  1,550,000); the closed forms for k = 4 and k = 5 match as shown above.
- The claimed file's extra diagnostics (`FIRSTMOVE 0 31`, `PROBE 0 1 0`,
  `PROBE_CHILDREN 2 25`) are also reproduced exactly by the published engine;
  they are outside K1359 and are not used in the verdict.

## What is proved, and what is not

**Proved computationally (exhaustive finite verification):**

1. The board is a projective plane of order 5 (hence PG(2,5) by uniqueness).
2. The complete size-by-size Grundy decomposition of the s=3 game on this board is
   exactly the K1359 table; the total is 7,906,892.
3. The maximal-position counts are 93,000 / 248,000 / 65,100 at sizes 9 / 10 / 11,
   there are no other maximal positions, and the maximum safe size is 11.
4. All 31,000 safe 4-sets have Grundy 2; Grundy 4 occurs only at size 7, on 186,000
   positions; the maximum Grundy value is 4.
5. All per-size and grand-total arithmetic is internally consistent.

**Caveats (none of which changes the verdict):**

- This is a computational verification, not a formal proof of the programs'
  correctness. Confidence rests on three independently written implementations
  (two C, one Python, with different parsers, legality checks, data structures and
  traversal directions), on internal assertions (no duplicate positions, every
  child found), and on the arithmetic cross-checks above.
- The identification "= PG(2,5)" uses the classical uniqueness of projective planes
  of prime order; the design axioms themselves were verified exhaustively.
- "4-cap" is read as a safe position of size 4. This includes 4-sets with three
  collinear points (allowed by s=3); the conclusion "G = 2" holds for all of them,
  hence a fortiori for classical 4-caps (no three collinear).
- Misère outcomes are not part of K1359; they were reproduced only as a side check.

## Discrepancies

**None.** No numerical or structural discrepancy was found between K1359 and the
independent computations.

## Reproduction

From `independent/` (Windows/PowerShell; Linux equivalents are the same commands):

```sh
python verify_board.py

gcc -O2 -o grundy_s_stats_published.exe \
    ../../pg2q7-cap-game-20261125/scripts/grundy_s_stats.c
./grundy_s_stats_published.exe \
    ../../projective-blocking-kyouen-20261125/output/board_pg2q5.txt 3 \
    | Out-File -Encoding ascii published_run.txt

gcc -O2 -o indep_verify.exe indep_verify.c
./indep_verify.exe \
    ../../projective-blocking-kyouen-20261125/output/board_pg2q5.txt \
    | Out-File -Encoding ascii indep_run.txt

python sizes_bruteforce.py
python sample_dp.py --sizes 3,4,5,6,7,8,9,10,11 \
    --counts 3,25,5,5,5,5,5,5,5 --out out/samples.json
./indep_verify.exe \
    ../../projective-blocking-kyouen-20261125/output/board_pg2q5.txt \
    out/probe.txt | Out-File -Encoding ascii out/indep_probe_run.txt
python compare_samples.py

python full_python_dp.py 2> out/python_full_dp.err \
    | Out-File -Encoding ascii out/python_full_dp.txt
python check_claims.py
```

## Artifacts

| File | Content |
|---|---|
| `verify_board.py`, `out/board_check.json` | board / PG(2,5) structural check |
| `indep_verify.c`, `indep_verify.exe`, `indep_run.txt` | independent C enumeration + Grundy DP |
| `grundy_s_stats_published.exe`, `published_run.txt`, `out/published_run2.txt` | recompiled published engine and its output |
| `full_python_dp.py`, `out/python_full_dp.txt`, `out/python_full_dp.err` | complete Python DP |
| `sizes_bruteforce.py`, `out/sizes_bruteforce.txt` | direct k-subset counts for k = 4..7 |
| `sample_dp.py`, `out/samples.json`, `out/sample_dp_log.txt`, `out/probe.txt` | full-upset DP samples |
| `compare_samples.py`, `out/sample_check.json`, `out/indep_probe_run.txt` | sample vs C comparison |
| `check_claims.py`, `out/checks.json` | consolidated claim/arithmetic checks (24/24 pass) |
| `out/bench.json` | preliminary root traversal (7,906,892 nodes, root G = 1) |
