# Independent verification — PG(2,7) / AG(2,7) cap game, s = 2

Date: 2026-11-25 (Asia/Tokyo).  Verifier directory:
`research/experiments/pg2q7-cap-game-20261125/independent/`.
Nothing outside this directory was modified; nothing was committed.

Environment: Python 3.12.13; gcc 15.2.0 (MSYS2 UCRT64); Windows x86-64;
about 21 GB free of 39 GB total RAM.

Inputs (read only):

- `research/experiments/projective-blocking-kyouen-20261125/output/board_pg2q7.txt`
  (PG(2,7), 57 points / 57 lines of size 8)
- `research/experiments/s-parameter-kyouen-20261125/output/board_ag2q7.txt`
  (AG(2,7), 49 points / 56 lines of size 7)

Game checked: a position is a point set meeting every line in at most 2
points (an s = 2 cap); a move adds one point; a player with no move loses
(normal play), or wins (misère).  `G(empty) = 0` and `misere = 1` below mean
normal-play Grundy value 0 at the empty position and that the player to move
from the empty position wins under misère (no move wins).

## Verdict

| Task | Verdict |
|---|---|
| 1. Board axioms | **PASS** |
| 2. All safe sets, totals, size distributions | **PASS** |
| 3. Maximal safe sets (two independent tests) | **PASS** |
| 4. Complete Grundy + misère | **PASS** |
| 5. Parity-theorem consistency | **PASS** |

All 76 machine checks in `comparison.json` pass.  No numerical discrepancy
with the claimed values was found.  Wording/interpretation notes are at the
end.

## 1. Board verification (`verify_boards.py` → `board_checks.json`)

PG(2,7):

- 57 points, 57 lines, every line has 8 distinct points, no duplicate line,
  every point occurs on exactly 8 lines.
- All C(57,2) = 1596 point pairs lie on exactly one line.
- All C(57,2) = 1596 line pairs meet in exactly one point.
- A quadrangle exists (4 points, no 3 collinear), so the incidence structure
  is a non-degenerate projective plane of order 7 (unique up to isomorphism
  for prime order 7).

AG(2,7):

- 49 points, 56 lines, every line has 7 distinct points, no duplicate line,
  every point occurs on exactly 8 lines.
- All C(49,2) = 1176 point pairs lie on exactly one line.
- The disjointness graph of the lines has exactly 8 components (“parallel
  classes”), each of size 7; in each class the 7 lines are pairwise disjoint
  and partition all 49 points; each line has exactly 6 disjoint partners.
- All 28 * 7 * 7 = 1372 cross-class line pairs meet in exactly one point.
- Three non-collinear points exist.

Both boards are therefore the claimed planes (as incidence structures).

## 2. Safe-set enumeration (`cap_engine.c` and `count_caps_py.py`)

Two independent implementations were used; both enumerate **every** safe set
exactly once in increasing-point order, with no sampling:

- `cap_engine.c`: canonical DFS with incremental line counts and a
  blocked-point mask.  Masks are `unsigned __int128` (PG needs 57 bits).
- `count_caps_py.py`: canonical DFS that keeps the explicit list of bisecant
  lines of the current cap and recomputes the forbidden-point union from
  scratch at every node (different data structure and different maximality
  mechanism).

Cross-check of the actual enumerated sets: for each size the 64-bit checksum
`sum splitmix64(mask) mod 2^64` was computed independently by both programs.
All nine per-size checksums agree exactly for both boards (see
`comparison.json`), i.e. the two implementations produced the same sets, not
merely the same counts.

### PG(2,7), s = 2

| k | safe sets | maximal | Grundy 0 | Grundy 1 | misère win | misère loss |
|---:|---:|---:|---:|---:|---:|---:|
| 0 | 1 | 0 | 1 | 0 | 1 | 0 |
| 1 | 57 | 0 | 0 | 57 | 0 | 57 |
| 2 | 1,596 | 0 | 1,596 | 0 | 1,596 | 0 |
| 3 | 26,068 | 0 | 0 | 26,068 | 0 | 26,068 |
| 4 | 234,612 | 0 | 234,612 | 0 | 234,612 | 0 |
| 5 | 938,448 | 0 | 0 | 938,448 | 0 | 938,448 |
| 6 | 1,094,856 | 625,632 | 1,094,856 | 0 | 1,094,856 | 0 |
| 7 | 134,064 | 0 | 0 | 134,064 | 0 | 134,064 |
| 8 | 16,758 | 16,758 | 16,758 | 0 | 16,758 | 0 |
| **total** | **2,446,460** | **642,390** | **1,347,823** | **1,098,637** | **1,347,823** | **1,098,637** |

### AG(2,7), s = 2

| k | safe sets | maximal | Grundy 0 | Grundy 1 | Grundy 2 | misère win | misère loss |
|---:|---:|---:|---:|---:|---:|---:|---:|
| 0 | 1 | 0 | 1 | 0 | 0 | 1 | 0 |
| 1 | 49 | 0 | 0 | 49 | 0 | 0 | 49 |
| 2 | 1,176 | 0 | 1,176 | 0 | 0 | 1,176 | 0 |
| 3 | 16,464 | 0 | 0 | 16,464 | 0 | 0 | 16,464 |
| 4 | 127,596 | 0 | 127,596 | 0 | 0 | 127,596 | 0 |
| 5 | 444,528 | 0 | 0 | 395,136 | 49,392 | 49,392 | 395,136 |
| 6 | 460,992 | 271,656 | 444,528 | 16,464 | 0 | 444,528 | 16,464 |
| 7 | 51,744 | 2,352 | 2,352 | 49,392 | 0 | 2,352 | 49,392 |
| 8 | 6,174 | 6,174 | 6,174 | 0 | 0 | 6,174 | 0 |
| **total** | **1,108,724** | **280,182** | **581,827** | **477,505** | **49,392** | **631,219** | **477,505** |

Closed-form corroboration (no enumeration used):

- PG: size 2 = C(57,2) = 1,596; size 3 = 57·56·49/6 = 26,068; size 4 =
  57·56·49·36/24 = 234,612; size 5 = 57·56·49·36·20/120 = 938,448.  (A
  4-arc has 21 points on its three secants, so 36 fourth points; a 5-arc has
  37 points on its six secants, so 20 fifth points.)  Size 8 = 7^5 − 7^2 =
  16,758 = number of conics in PG(2,7) (and every 8-arc is a conic, Segre).
- AG: size 2 = C(49,2) = 1,176; size 3 = 49·48·42/6 = 16,464; size 4 =
  49·48·42·31/24 = 127,596 (18 points on the three secants, so 31 fourth
  points).
All match the enumerated counts.

## 3. Maximal safe sets (`cap_engine.c`)

Every safe set was tested by **two independent criteria**:

- Test A (incremental): maintain the set of points blocked by a line already
  carrying 2 chosen points; S is maximal iff every point outside S is blocked.
- Test B (from scratch): U = union of all lines carrying exactly 2 points of
  S; S is maximal iff S ∪ U is the whole point set.

Results: Test A and Test B give identical counts **and identical per-size
checksums of the maximal masks**; the Python enumerator (which recomputes the
bisecant union from an explicit line list) gives the same maximal counts and
the same maximal-mask checksums.  Hence the following are verified sets, not
just counts:

- PG(2,7): size 6: **625,632**, size 8: **16,758**; no maximal sets of any
  other size (total 642,390).  All maximal sizes are even.
- AG(2,7): size 6: **271,656**, size 7: **2,352**, size 8: **6,174**; no
  others (total 280,182).  Maximal parity is mixed (7 is odd).

## 4. Complete Grundy and misère values

Two full bottom-up DPs were run over all safe sets:

- `cap_engine.c`: buckets by size, open-addressing hash on 128-bit masks.
- `grundy_py.py`: reads the Python-enumerated masks and repeats the DP with
  Python dicts.

Both agree on every per-size Grundy distribution, every per-size misère
win/loss count, the total distributions, and the root.  In addition,
`sample_check.py` re-solved 30 deterministic sampled positions per board
(sizes 4–8) by direct recursion from the game definition (no bisecant-mask
shortcut); all values and misère flags matched.

- **PG(2,7)**: Grundy **{0: 1,347,823; 1: 1,098,637}** (no value ≥ 2),
  `G(empty) = 0`, root misère = **win** (1).  Moreover
  `G(S) = |S| mod 2 = (8 − |S|) mod 2` holds for **all 2,446,460** safe sets
  (0 mismatch), which is exactly the even/odd size counts.
- **AG(2,7)**: Grundy **{0: 581,827; 1: 477,505; 2: 49,392}**,
  `G(empty) = 0`, root misère = **win** (1).  The 49,392 Grundy-2 positions
  are exactly the size-5 positions with both a Grundy-0 and a Grundy-1
  child; they do not occur at size 6, 7 or 8.  68,208 positions violate
  `G(S) = |S| mod 2`, as expected for mixed maximal parity.

So `G(empty) = 0` and `misere = 1` are confirmed for both boards.

## 5. Parity-theorem consistency

Theorem used only as a consistency check (it is also verified directly by the
DP): if every inclusion-maximal safe set has even size, then induction from
the top gives `G(S) = |S| mod 2` for every safe set, because a non-maximal S
has all children of size |S|+1 and therefore all children carry the single
value (|S|+1) mod 2, whose mex is |S| mod 2.

- PG(2,7): maximal sizes are 6 and 8, both even ⇒ Grundy ⊆ {0,1}.  Confirmed:
  the complete DP has only 0 and 1, and the formula matches all 2,446,460
  positions.
- AG(2,7): maximal sizes 6, 7, 8 are mixed ⇒ the graded formula cannot hold
  and values ≥ 2 must occur.  Confirmed: 49,392 positions have Grundy 2, and
  68,208 positions violate the parity formula.

## Reproduction

From the repository root (PowerShell; `$d` is the independent directory):

```powershell
$d = "research/experiments/pg2q7-cap-game-20261125/independent"
python "$d/verify_boards.py"

gcc -O2 -std=gnu11 -o "$d/cap_engine.exe" "$d/cap_engine.c"
& "$d/cap_engine.exe" "research/experiments/projective-blocking-kyouen-20261125/output/board_pg2q7.txt" pg2q7 > "$d/pg2q7_result.txt"
& "$d/cap_engine.exe" "research/experiments/s-parameter-kyouen-20261125/output/board_ag2q7.txt" ag2q7 > "$d/ag2q7_result.txt"

python "$d/count_caps_py.py" "research/experiments/projective-blocking-kyouen-20261125/output/board_pg2q7.txt" pg2q7 --dump "$d/pg2q7_masks.bin"
python "$d/count_caps_py.py" "research/experiments/s-parameter-kyouen-20261125/output/board_ag2q7.txt" ag2q7 --dump "$d/ag2q7_masks.bin"

python "$d/grundy_py.py" "research/experiments/projective-blocking-kyouen-20261125/output/board_pg2q7.txt" "$d/pg2q7_masks.bin" pg2q7
python "$d/grundy_py.py" "research/experiments/s-parameter-kyouen-20261125/output/board_ag2q7.txt" "$d/ag2q7_masks.bin" ag2q7

python "$d/sample_check.py" "research/experiments/projective-blocking-kyouen-20261125/output/board_pg2q7.txt" "$d/pg2q7_result.txt" pg2q7
python "$d/sample_check.py" "research/experiments/s-parameter-kyouen-20261125/output/board_ag2q7.txt" "$d/ag2q7_result.txt" ag2q7

python "$d/compare_claims.py"
```

Observed runtimes on this machine: C enumeration 3.34 s (PG) / 1.45 s (AG),
C DP 2.85 s / 1.17 s; Python enumeration 13.1 s / 5.9 s, Python DP 36.3 s /
14.9 s.  The `*_masks.bin` files are only intermediates for the Python DP and
can be regenerated with the commands above.

## Files

- `verify_boards.py`, `board_checks.json` — plane axioms.
- `cap_engine.c` — C enumerator, two maximality tests, full DP.
- `pg2q7_result.txt`, `ag2q7_result.txt` — C outputs (counts, maximal counts,
  checksums, per-size Grundy/misère, samples).
- `count_caps_py.py`, `*_py_enum.json` — independent Python enumeration.
- `grundy_py.py`, `*_py_grundy.json` — independent Python full DP.
- `sample_check.py`, `*_sample_check.json` — direct recursive sample checks.
- `compare_claims.py`, `comparison.json` — all 76 claim/consistency checks.

Build products (`cap_engine.exe`) and mask dumps (`*_masks.bin`) were used as
intermediates and removed afterwards to keep the directory text-only; the
commands above regenerate them.

## Discrepancies and notes

1. **No numerical discrepancy** with any claimed value was found: totals,
   per-size distributions, maximal sizes/counts, Grundy distributions,
   `G(empty)` and misère root value all match.  The original experiment
   outputs `output/grundy_pg2q7_s2.txt` and `output/grundy_ag2q7_s2.txt`
   also agree, line by line, with the computed totals, per-size safe counts,
   maximal counts, Grundy-0 counts and total Grundy distributions.
2. The task text for item 4 says “every maximal set has size 8” in PG(2,7).
   That is not literally true: 625,632 maximal sets have size 6 and 16,758
   have size 8.  The parity theorem only needs all maximal sizes to be even,
   which holds; the direct DP independently confirms `G(S) = |S| mod 2` on
   all positions, so the claimed conclusion is unaffected.
3. `misere = 1` was interpreted as “the player to move from the empty position
   wins under misère play (no move wins)”, matching the game definition given
   in the task.  The normal-play Grundy value at the root is 0.
4. The original engine’s `FIRSTMOVE` / `PROBE` output lines are not part of
   the claims and were not checked.
