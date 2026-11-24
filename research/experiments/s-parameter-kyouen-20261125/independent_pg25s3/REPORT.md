# Independent verification — PG(2,5), s = 3 blocking Kyouen game

Date: 2026-11-25
Directory: `research/experiments/s-parameter-kyouen-20261125/independent_pg25s3/`

Everything in this directory was written from scratch (C and Python standard library
only). No file outside this directory was modified, and nothing was committed.
`git status` shows this directory as the only path created by this work; the other
entries in the working tree were pre-existing and untouched.

- Input board: `research/experiments/projective-blocking-kyouen-20261125/output/board_pg2q5.txt`
- Claim file: `research/experiments/s-parameter-kyouen-20261125/output/grundy_pg2q5_s3.txt`
  (This is where the numbers in the task statement live; the `output/` suffix in the
  prompt refers to this experiment's output directory.)
- Environment: Windows, `gcc.exe (Rev8, Built by MSYS2 project) 15.2.0`, Python 3.12.13,
  compiled with `-O2 -Wall -Wextra`. Total wall time of the full pipeline: 45–48 s.

## Verdict

| # | Task | Verdict |
|---|------|---------|
| 1 | Board is PG(2,5) | **PASS** |
| 2 | All safe sets + size distribution (7,906,892) | **PASS** |
| 3 | Maximal safe set sizes/counts (9: 93,000, 10: 248,000, 11: 65,100; none below 9) | **PASS** |
| 4 | Complete Grundy distribution + Grundy(∅) / misère(∅) | **PASS** |
| 5 | Parity characterization (K1298) + caution example | **PASS** for the mathematics; **one discrepancy** in the quoted example value (see §5) |

No discrepancy was found in the claimed game data. The only discrepancy found is a
quoted value inside the K1298 knowledge item (not in the claim file): for its small
counterexample board it states `Grundy(S)=0`, but the correct normal-play value is
`1` (the value `0` is the misère outcome). The qualitative point of the example
still holds.

## 1. Board is PG(2,5) — PASS

`task1_board.py` parses the file independently and checks:

| check | result |
|---|---|
| header `n=31`, `b=31` | PASS |
| every line has exactly 6 distinct in-range points | PASS (histogram `{6: 31}`) |
| all 31 points occur, each on exactly 6 lines | PASS (incidence histogram `{6: 31}`) |
| no duplicate lines | PASS (31/31 distinct) |
| all 465 point pairs covered | PASS (465/465) |
| every pair on **exactly one** line | PASS (multiplicity histogram `{1: 465}`) |
| every pair of lines meets in exactly one point (extra) | PASS (all 465 intersections have size 1) |
| design parameters `2-(31,6,1)` | PASS |

A `2-(31,6,1)` design is a projective plane of order 5; projective planes of prime
order are unique (Desarguesian), so the file is PG(2,5). Output: `out_task1.json`,
`task1_out.txt`.

## 2. All safe sets and size distribution — PASS

Two structurally different exhaustive algorithms, both from scratch:

**(A) DFS enumeration** (`enum_safe.c`, 1.9 s). Enumerates every safe set exactly once
by adding points in increasing order; `cnt[L] = |S∩L|` and `tightpt[p]` = number of
tight (`cnt==3`) lines through `p`; a point is addable iff `tightpt[p]==0`. Stores
each safe mask and its full legal-move mask per size.

**(B) Exhaustive combination enumeration** (`brute_count.c`, 14–18 s). Iterates over
**all** `C(31,k)` subsets for `k = 0..12` via Gosper's hack (301,766,029 subsets) and
tests safety directly by popcounting the subset against all 31 line masks. No DFS,
no pruning, no shared logic with (A).

Both agree exactly with the claim:

| size | claimed | DFS | brute force | maximal (claim) | maximal (DFS) | maximal (brute) |
|---:|---:|---:|---:|---:|---:|---:|
| 0 | 1 | 1 | 1 | 0 | 0 | 0 |
| 1 | 31 | 31 | 31 | 0 | 0 | 0 |
| 2 | 465 | 465 | 465 | 0 | 0 | 0 |
| 3 | 4,495 | 4,495 | 4,495 | 0 | 0 | 0 |
| 4 | 31,000 | 31,000 | 31,000 | 0 | 0 | 0 |
| 5 | 158,100 | 158,100 | 158,100 | 0 | 0 | 0 |
| 6 | 592,100 | 592,100 | 592,100 | 0 | 0 | 0 |
| 7 | 1,550,000 | 1,550,000 | 1,550,000 | 0 | 0 | 0 |
| 8 | 2,557,500 | 2,557,500 | 2,557,500 | 0 | 0 | 0 |
| 9 | 2,216,500 | 2,216,500 | 2,216,500 | 93,000 | 93,000 | 93,000 |
| 10 | 731,600 | 731,600 | 731,600 | 248,000 | 248,000 | 248,000 |
| 11 | 65,100 | 65,100 | 65,100 | 65,100 | 65,100 | 65,100 |
| 12 | — | — | **0** | — | — | 0 |
| **total** | **7,906,892** | **7,906,892** | **7,906,892** | **406,100** | **406,100** | **406,100** |

The brute force additionally proves exhaustively that there is **no safe 12-set**;
because safe sets are downward closed, no safe set of size ≥ 12 exists, so the
maximum size 11 is established independently (the DFS also reaches max size 11).

Independent closed-form sanity checks for the small sizes (no search):
`C(31,0..3) = 1, 31, 465, 4,495`; size 4: `C(31,4) − 31·C(6,4) = 31,465 − 465 = 31,000`;
size 5: `C(31,5) − 31·(C(6,4)·25 + C(6,5)) = 169,911 − 11,811 = 158,100` — all match.

Outputs: `enum_out.txt`, `brute_out.txt`, `safesets.bin` (mask + legal-move dump).

## 3. Maximal safe sets — PASS

A set is maximal iff no outside point is addable, i.e. every point is in `S` or lies
on a tight line (a line with exactly 3 points of `S`). Both algorithms implement this
differently: the DFS records maximality as `addable_mask == 0`, the brute force as
`(S | union_of_tight_lines) == all_points`. They agree:

- no maximal safe sets at sizes 0–8;
- size 9: **93,000** maximal (out of 2,216,500 safe sets);
- size 10: **248,000** maximal (out of 731,600);
- size 11: **65,100** maximal (all safe 11-sets, since no 12-set exists);
- total maximal safe sets: **406,100**.

## 4. Complete Grundy / misère — PASS

Two structurally different full DPs (both compute every one of the 7,906,892 states):

- **Level DP** (`grundy_level.c`, 2.6–3.6 s): processes sizes downwards, each level in
  an open-addressing hash table (`mask → encoded value`); legal children come from the
  stored legal-move masks. Value encoding: 4 bits Grundy, misère bit, 2 bits parity set
  `f(S)`, and a “Grundy ≥ 2 above S” bit.
- **Recursive memo DP** (`grundy_rec.c`, 13–14 s): no dump at all; direct memoized
  recursion from the empty position, maintaining line counts on the stack, its own
  hash table. It independently re-derives all safe/maximal counts as well.

Both give **identical** totals, per-size Grundy distributions, per-size misère
distributions and root value:

| Grundy | claimed | level DP | recursive DP |
|---:|---:|---:|---:|
| 0 | 2,056,726 | 2,056,726 | 2,056,726 |
| 1 | 2,083,666 | 2,083,666 | 2,083,666 |
| 2 | 1,519,000 | 1,519,000 | 1,519,000 |
| 3 | 2,061,500 | 2,061,500 | 2,061,500 |
| 4 | 186,000 | 186,000 | 186,000 |
| **sum** | **7,906,892** | **7,906,892** | **7,906,892** |

`Grundy(∅) = 1`, `misère(∅) = 1` (win for the player to move under “unable to move
wins”), matching `ROOT 1 1`. Misère totals over all positions: lose 2,320,226 /
win 5,586,666.

Per-size Grundy distribution (identical in both DPs; the first column is exactly the
4th field `g0` of the claim file’s `SIZE` lines — see §6):

| size | G=0 | G=1 | G=2 | G=3 | G=4 |
|---:|---:|---:|---:|---:|---:|
| 0 | 0 | 1 | 0 | 0 | 0 |
| 1 | 31 | 0 | 0 | 0 | 0 |
| 2 | 0 | 465 | 0 | 0 | 0 |
| 3 | 4,495 | 0 | 0 | 0 | 0 |
| 4 | 0 | 0 | 31,000 | 0 | 0 |
| 5 | 111,600 | 46,500 | 0 | 0 | 0 |
| 6 | 15,500 | 3,100 | 186,000 | 387,500 | 0 |
| 7 | 480,500 | 697,500 | 186,000 | 0 | 186,000 |
| 8 | 465,000 | 232,500 | 186,000 | 1,674,000 | 0 |
| 9 | 666,500 | 620,000 | 930,000 | 0 | 0 |
| 10 | 248,000 | 483,600 | 0 | 0 | 0 |
| 11 | 65,100 | 0 | 0 | 0 | 0 |

**Third implementation (Python)** — `verify_sample.py`:

- 220 randomly sampled positions of sizes 6–11 (`random.Random(20261125)`), each
  Grundy **and** misère value recomputed from scratch by an independent recursive mex
  (own board parser, no use of the C values except for the final comparison):
  **0 mismatches**.
- The local mex rule was checked exhaustively for **all 194,092** stored states of
  sizes 0–5 against their stored size-≤6 children: **0 violations**.
- 532 randomly sampled stored legal-move masks recomputed from the board: 0 bad;
  no duplicate masks in any level.

## 5. Parity characterization (K1298) — PASS (with one quoted-value discrepancy)

### (a) Big board — exhaustive local verification

The level DP computes, for every position `S`:

- `f(S)` = the set of parities of the maximal safe sets containing `S`
  (bottom-up: terminal `S` has `f = {|S| mod 2}`; otherwise `f(S) = ⋃ f(S∪{p})`),
- `desc2(S)` = whether some `T ⊇ S` has Grundy ≥ 2.

Results over **all 7,906,892** positions:

| K1298 local statement | positions checked | violations |
|---|---:|---:|
| `f(S)` uniform with parity `p` ⇒ `Grundy(S) = (p − |S|) mod 2` | 2,238,200 | **0** |
| `f(S)` mixed ⇔ some `T ⊇ S` has Grundy ≥ 2 | 7,906,892 | **0** |
| `f(S)` uniform ⇒ misère win ⇔ `Grundy(S) = 0` (⇔ `p−|S|` even) | 2,238,200 | **0** |

The maximal safe sets have sizes 9 (odd, 93,000), 10 (even, 248,000), 11 (odd,
65,100): **mixed parity**, so Grundy ≥ 2 must occur — it does, in
`1,519,000 + 2,061,500 + 186,000 = 3,766,500` positions (values 2, 3, 4).
The empty position has Grundy 1 (odd), as a first player win; this is consistent with
the theorem (the theorem constrains only the uniform-parity positions).

### (b) Small counterexample from K1298 — reproduced, with one correction

Board: `n = 5`, `s = 2`, blocks `{(0,2),(0,4),(1,2),(2,4),(1,3,4),(0,2,3,4)}`, `S = {}`
(`task5_parity.py`, brute force over all 32 subsets).

Reproduced exactly as stated:

- 21 safe positions;
- maximal extensions of `S = {}`: exactly **6** —
  `{3,4}` (size 2, even) and `{0,1,2}`, `{0,1,3}`, `{0,1,4}`, `{1,2,3}`, `{1,2,4}`
  (size 3, odd): **mixed parity**;
- Grundy distribution `{0: 9, 1: 10, 2: 2}`; the subgame above `S` does contain
  Grundy ≥ 2 (at `{3}` and `{4}`, both 2), as the theorem requires for mixed parity.

**Discrepancy:** K1298’s note states `Grundy(S) = 0` for this board. Independent
computation (both the bitmask DP and the separate frozenset/`lru_cache`
implementation inside `task5_parity.py`, which agree state-by-state — field
`second_impl` in `out_task5.json`) gives

```
Grundy(∅) = 1,      misère(∅) = 0.
```

The value `0` quoted in K1298 is the **misère outcome**, not the normal-play Grundy
value. The qualitative caution (“a position with mixed maximal-extension parity need
not have Grundy ≥ 2”) is still correct, since `1 < 2`; only the quoted number is
wrong. The local theorem checks on the small board itself pass for all 21 positions
(0 violations for the Grundy formula, the mixed ⇔ Grundy ≥ 2 equivalence, and the
misère formula).

## 6. Claim-file coverage — 81/81 field comparisons PASS

`compare_claims.py` parses the claim file and compares **every field** with the
independent computations (the numerical payload of the claim file is richer than the
task summary). All 81 comparisons pass:

- `POINTS 31`, `CIRCLES 31`, `SAFE 7906892`;
- all 12 `SIZE` lines, each with **four** fields — size, safe count, maximal count,
  and the number of Grundy-0 positions of that size. The 4th field is decoded from the
  engine source (`research/experiments/finite-field-kyouen-20261120/scripts/grundy_full.c`,
  printf `SIZE %d %lld %lld %lld` = `bcount, maximal, g0`) and matches the first column
  of the per-size table in §4 for every size;
- all 5 `GRUNDY` counts;
- `ROOT 1 1`;
- `FIRSTMOVE 0 31` — all 31 first moves lead to Grundy-0 positions (the 31 singletons);
- `PROBE 0 1 0` — `G({0})=0`, `G({0,1})=1`, `G({0,1,2})=0`;
- `PROBE_CHILDREN 2 25` — `{0,1,2}` has exactly 25 legal moves, all to Grundy-2
  positions (the 25 points off the line `{0,1,2,3,4,5}`);
- distribution sums equal `SAFE`; both C DPs agree on every value (the comparison
  includes the recursive DP’s per-size Grundy and misère distributions).

There are **no unknown or unparsed lines** in the claim file, i.e. the whole file was
verified, not just the subset named in the task.

## 7. Discrepancies

1. **K1298 note (knowledge item), small counterexample:** states `Grundy(S) = 0` for
   `S = {}` on `n=5, s=2, blocks {(0,2),(0,4),(1,2),(2,4),(1,3,4),(0,2,3,4)}`;
   the correct normal-play value is **1** (the misère outcome is 0). Everything else
   in that example (6 maximal extensions, mixed parity, Grundy ≥ 2 occurring above
   `S`) is reproduced. Suggested fix: change `Grundy(S)=0` to `Grundy(S)=1`
   (or quote the misère value separately).
2. No discrepancy in any claimed number for PG(2,5), s = 3. The only issues found
   during the work were two bugs in my own first-pass scripts (max-size bookkeeping in
   the DFS dump header, and an ascending instead of descending DP order in the small
   board check), both fixed before the final runs reported here.

## 8. Reproduce

From this directory:

```powershell
pwsh -NoProfile -File .\run_all.ps1
```

or step by step:

```powershell
gcc -O2 -Wall -Wextra -o enum_safe.exe enum_safe.c
gcc -O2 -Wall -Wextra -o brute_count.exe brute_count.c
gcc -O2 -Wall -Wextra -o grundy_level.exe grundy_level.c
gcc -O2 -Wall -Wextra -o grundy_rec.exe grundy_rec.c
$board = "..\..\projective-blocking-kyouen-20261125\output\board_pg2q5.txt"
python task1_board.py
.\enum_safe.exe $board safesets.bin
.\brute_count.exe $board 12
.\grundy_level.exe safesets.bin grundy_values.bin
.\grundy_rec.exe $board 24
python verify_sample.py
python task5_parity.py
python compare_claims.py
```

Timings from the final run (`run_log.txt`; they vary by a few seconds between runs):
task1 0.16 s, DFS 1.90 s, brute force 14.6 s, level DP 2.7 s, recursive DP 13.9 s,
Python sampling 8.8 s, parity 0.17 s, claim comparison 0.27 s; total 45.5 s.

## 9. Artifacts

| file | role |
|---|---|
| `task1_board.py`, `out_task1.json`, `task1_out.txt` | PG(2,5) verification |
| `enum_safe.c`, `enum_out.txt` | DFS enumeration of safe sets + dump |
| `brute_count.c`, `brute_out.txt` | exhaustive all-subsets (k = 0..12) enumeration |
| `safesets.bin` (63,255,348 B) | per-size safe masks + legal-move masks |
| `grundy_level.c`, `grundy_level_out.txt`, `grundy_values.bin` (7,907,008 B) | level DP + per-state values |
| `grundy_rec.c`, `grundy_rec_out.txt` | independent recursive memo DP |
| `verify_sample.py`, `out_task4_sample.json`, `verify_sample_out.txt` | Python third implementation / sampling |
| `task5_parity.py`, `out_task5.json`, `task5_out.txt` | K1298 big-board + small-board checks |
| `compare_claims.py`, `out_claims_comparison.json`, `compare_out.txt` | 81-field comparison against the claim file |
| `run_all.ps1`, `run_log.txt` | end-to-end reproduction |

## 10. Limitations / notes

- The two full Grundy computations are independent in algorithm and data flow (level
  hash DP from a mask dump vs. direct memoized recursion from the board), but both
  were written by this verification run; the claim-file agreement, the Python
  recomputation of 220 sampled positions, and the exhaustive K1298 consistency checks
  are the external anchors.
- The statement “every pair on exactly one line” plus `v = b = 31`, `k = 6` identifies
  a projective plane of order 5; uniqueness of planes of prime order is a standard
  theorem, so no explicit coordinatization was constructed.
- The Python sample cannot recompute the empty position from scratch (its subtree is
  the whole game); `Grundy(∅)` is instead certified by the two full C DPs and by the
  local mex checks (all 31 first moves verified to have Grundy 0, hence mex = 1).
- No commits were made; all generated data stays inside this directory.
