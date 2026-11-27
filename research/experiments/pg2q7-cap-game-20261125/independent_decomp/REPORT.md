# Independent verification of claim K1338 — s=2 cap game on AG(2,7)

- Date: 2026-11-26
- Verifier: independent sub-agent. All computation was written from scratch in
  this directory; the claiming C engine was not used for any number here (its
  source was inspected only to learn the exact meaning of the output lines that
  are compared against).
- Board: `research/experiments/s-parameter-kyouen-20261125/output/board_ag2q7.txt`
- Claimed decomposition: K1338 (6-cap / 5-cap Grundy decomposition, totals)
- Reference output compared against:
  `research/experiments/pg2q7-cap-game-20261125/output/grundy_ag2q7_s2.txt`
  (plus the `GSIZE` lines in
  `research/experiments/s-parameter-kyouen-20261125/output/stats_ag2q7_s2.txt`)
- All work is inside
  `research/experiments/pg2q7-cap-game-20261125/independent_decomp/`.
  No commits, no files outside that directory were modified.
- Python 3.12.13, standard library only.

## Verdict

| Task | Result |
|---|---|
| 1. Board is AG(2,7) | **PASS** |
| 2. Enumerate all 6-caps and classify maximal / only-8 / only-7 / mixed | **PASS** |
| 3. Grundy values (sample upset DP, plus full DP over all positions) | **PASS** |
| 4. Totals and size-by-size arithmetic vs. reference file | **PASS** (75/75 checks) |
| 5. What is proved / discrepancies | **No discrepancy found** |

The claimed decomposition is reproduced **exactly**:

- 6-caps: `maximal 271,656 (G=0)`, `only-8 172,872 (G=0)`,
  `only-7 16,464 (G=1)`, `mixed 0`; total `460,992`.
- 5-caps: `444,528` total; all have a maximal 6-child; `G=2` exactly for the
  `49,392` five-subsets of maximal 7-caps; the other `395,136` have `G=1`.
- Totals: `G=0 581,827`, `G=1 477,505`, `G=2 49,392`, total `1,108,724`.

## Environment / reproducibility

Scripts (run in this order; each can be run from any working directory):

```text
python task1_board.py        # board axioms + explicit AG(2,7) coordinatisation
python selftest_small.py     # machinery checked against brute force on AG(2,2/3/4)
python task2_enum6.py        # DFS enumeration + 6-cap classification -> caps_by_size.bin
python task3_grundy.py       # full bottom-up DP + 60 recursive sample checks
python task4_totals.py       # reference-file and arithmetic checks
```

Observed wall times: task2 ≈ 11.6 s, task3 ≈ 34.4 s (full DP 14.7 s,
5-cap scan 14.3 s), task1/task4/selftest < 5 s. `caps_by_size.bin` is a
simple little-endian file: magic `CAPS1\n`, `u32 N`, then for each size
`u64 count` followed by `count` uint64 point masks.

SHA-256 of inputs actually used:

```text
board_ag2q7.txt      17e2bae586f60dd243aa201b451a5952b02360477e7bf066bbe25f28ad088594
grundy_ag2q7_s2.txt  4dc7cdd0c966e95921987577dee7895dc9c0c794cdc6d88d67d030bb21f194f7
stats_ag2q7_s2.txt   9ca852eb768a8b0d5bcbe29a6872408054f1219bb2cea3c8b300d45332b20b2b
```

Artifacts: `task1_board.json`, `selftest_small.json`, `summary_enum.json`,
`caps_by_size.bin`, `summary_grundy.json`, `summary_totals.json`.

## Task 1 — the board is AG(2,7)

Parsed strictly: first line `49 56`, then 56 lines of the form `7 p1 ... p7`.
All checks in `task1_board.json` pass:

| Check | Result |
|---|---|
| 49 points, 56 lines, every line has 7 distinct points in range | PASS |
| no duplicate lines | PASS |
| every unordered pair lies on exactly one line (1,176 pairs, 0 violations) | PASS |
| every point lies on 8 lines | PASS |
| any two lines meet in 0 or 1 point | PASS |
| each line is disjoint from exactly 6 others | PASS |
| lines split into 8 parallel classes of 7 lines; each class partitions the 49 points | PASS |
| explicit coordinatisation to `F_7^2` found | PASS |

The last check is stronger than the axioms: a bijection
`points -> F_7^2` was searched for, and one was found (x-axis labels
`[0,1,2,3,4,5,6]`, y-axis labels `[1,0,6,5,4,3,2]`, reference-line equation
`y = x`), such that all 56 board lines map to **exactly** the 56 affine lines of
`AG(2,7)` and the map is a bijection. So this board is AG(2,7), not merely an
affine-plane-axiom system.

The s=2 cap condition is the one used throughout:
`S` safe iff `|S ∩ L| <= 2` for every board line. The exhaustive enumeration
below finds maximum cap size **8** and no 9-cap. As an additional primitive
check, for 320 sampled caps (40 per size 1..8) the incremental forbidden-mask
safety test was compared with the literal line definition and with direct
one-point safety tests: 0 mismatches.

## Task 2 — exhaustive 6-cap enumeration and classification

Method: depth-first enumeration of every safe set, adding points in increasing
index order so each cap is visited exactly once. When a point `p` is added, the
forbidden mask is updated with the union of lines through `p` and each old point;
the addable set is `all_points \ (S ∪ forbidden)`. Every addable point of a
6-cap `S` gives a distinct 7-cap `S+p`; that 7-cap is maximal iff it has no
addable point. This yields the classification:

- `maximal`: no addable point;
- `only8`: non-maximal and every 7-extension is non-maximal (hence extends to an 8-cap);
- `only7`: every 7-extension is maximal;
- `mixed`: both kinds occur.

All caps, by size:

| size k | caps | maximal |
|---:|---:|---:|
| 0 | 1 | 0 |
| 1 | 49 | 0 |
| 2 | 1,176 | 0 |
| 3 | 16,464 | 0 |
| 4 | 127,596 | 0 |
| 5 | 444,528 | 0 |
| 6 | **460,992** | **271,656** |
| 7 | 51,744 | 2,352 |
| 8 | 6,174 | 6,174 |
| total | **1,108,724** | 280,182 |

No cap of size 9 exists.

6-cap classification:

| class | count | Grundy |
|---|---:|---:|
| maximal | 271,656 | 0 |
| only8 | 172,872 | 0 |
| only7 | 16,464 | 1 |
| mixed | 0 | — |
| total | 460,992 | |

Independent incidence cross-checks (all pass):

- maximal 7-caps: 2,352; their 6-subsets are 7 × 2,352 = 16,464 incidences and
  16,464 **distinct** masks, every one classified `only7`;
- 8-caps: 6,174, all maximal; their 6-subsets are 28 × 6,174 = 172,872 incidences
  and 172,872 **distinct** masks, every one classified `only8`;
- therefore the only8 and only7 classes are disjoint and exhaust the
  non-maximal 6-caps: 172,872 + 16,464 = 460,992 − 271,656 = 189,336, with
  mixed = 0.

5-cap scan used for Task 3 (independent of the reference output):

| quantity | value |
|---|---:|
| 5-caps total | 444,528 |
| with a maximal 6-child | **444,528** (all) |
| with an only7 6-child | 49,392 |
| without an only7 6-child | **395,136** |
| with an only8 6-child | 345,744 |
| with a mixed 6-child | 0 |
| distinct 5-subsets of maximal 7-caps | 49,392 = 21 × 2,352 |
| distinct 5-subsets of 8-caps | 345,744 |
| distinct 5-subsets of any 7-cap (maximal or not) | 395,136 |

The machinery was also checked against exhaustive subset brute force on the
small boards AG(2,2), AG(2,3), AG(2,4): counts, maximal counts, per-size Grundy
distributions and the root Grundy value matched in all cases
(`selftest_small.json`, `all_pass: true`).

## Task 3 — Grundy values

Two computations were made:

1. **Full bottom-up DP over all 1,108,724 caps** (sizes 8 down to 0), using only
   `G(S) = mex { G(S+p) : p addable to S }`. This is exhaustive, not a sample.
2. **Fresh recursive upset DP for 60 sampled 5-caps** (30 with an extension to a
   maximal 7-cap, 30 without), each with a new memo table; all 60 matched the
   full DP and the expected value.

Full distribution:

| size | G=0 | G=1 | G=2 |
|---:|---:|---:|---:|
| 0 | 1 | 0 | 0 |
| 1 | 0 | 49 | 0 |
| 2 | 1,176 | 0 | 0 |
| 3 | 0 | 16,464 | 0 |
| 4 | 127,596 | 0 | 0 |
| 5 | 0 | 395,136 | **49,392** |
| 6 | 444,528 | 16,464 | 0 |
| 7 | 2,352 | 49,392 | 0 |
| 8 | 6,174 | 0 | 0 |
| **total** | **581,827** | **477,505** | **49,392** |

No Grundy value ≥ 3 occurs. Root `G(∅) = 0`; all 49 size-1 positions have
`G = 1`, consistent with `FIRSTMOVE 1 49`.

5-cap checks (all positions, not just samples):

- every one of the 444,528 5-caps has a maximal 6-child (G=0 option);
- the set of 5-caps with `G = 2` is **exactly** the set of 5-subsets of maximal
  7-caps: 49,392 masks, set equality (not only equal counts);
- the other 395,136 5-caps have `G = 1`.

Sample checks (seed 20261125): all 30 sampled 5-caps with a maximal-7 extension
gave `G_recursive = G_full_DP = 2`; all 30 without gave
`G_recursive = G_full_DP = 1`; all 60 had a maximal 6-child; 0 bad samples.
Examples: points `{12,13,15,17,23}` (with) → 2; points
`{14,17,25,27,47}` (without) → 1. Full lists are in `summary_grundy.json`.

## Task 4 — reference file and arithmetic

Reference values parsed from `grundy_ag2q7_s2.txt`:
`POINTS 49`, `CIRCLES 56`, `SAFE 1108724`, `SIZE 0..8`, `GRUNDY 0/1/2`,
`ROOT 0 ...`, `FIRSTMOVE 1 49`. All 75 checks in `summary_totals.json` pass.

- Every `SIZE k <count> <maximal> <grundy0>` line equals the independent
  values (count, maximal count, and G=0 count) for k = 0..8.
- The `GRUNDY` histogram equals `{0: 581827, 1: 477505, 2: 49392}` and sums to
  `SAFE = 1,108,724`.
- All `GSIZE k g count` lines in the stats file equal the independent per-size
  distribution (e.g. `GSIZE 5 2 49392`, `GSIZE 6 1 16464`,
  `GSIZE 7 1 49392`).
- Arithmetic claimed in K1338:

```text
460,992 = 271,656 + 172,872 + 16,464 + 0
172,872 = 28 * 6,174          (6-subsets of the 8-caps)
 16,464 =  7 * 2,352          (6-subsets of the maximal 7-caps)
444,528 = 49,392 + 395,136
 49,392 = 21 * 2,352          (5-subsets of the maximal 7-caps)
581,827 + 477,505 + 49,392 = 1,108,724
```

The reference file itself has no per-class 6-cap split column; the split is not
hidden in it. The file's SIZE 6 row gives `count 460,992`, `maximal 271,656`,
`G=0 444,528`; together with the independently verified fact that all 6-caps
have G ∈ {0,1}, this forces
`only8 = 444,528 − 271,656 = 172,872` and
`only7 = 460,992 − 444,528 = 16,464`, and mixed = 0. The independent
classification gives those classes directly. The `GSIZE` lines in the stats
file state the same G=1 count (16,464) explicitly.

## Task 5 — what is proved, and discrepancies

**What is proved by this computation.** For the concrete 49-point board in
`board_ag2q7.txt`, which is explicitly isomorphic to AG(2,7) (verified above),
an exhaustive enumeration of all safe sets and an exhaustive bottom-up Grundy
computation over all 1,108,724 positions were performed. Within that finite
game:

- the number of caps of each size and the number of maximal caps of each size
  are exactly as listed;
- the 6-cap classes `maximal / only8 / only7 / mixed` are exactly
  `271,656 / 172,872 / 16,464 / 0`;
- every maximal 6-cap and every only8 6-cap has G=0, every only7 6-cap has G=1;
- all 5-caps have a maximal 6-child; exactly the 49,392 five-subsets of maximal
  7-caps have G=2, and the other 395,136 have G=1;
- the total distribution is exactly `G=0: 581,827`, `G=1: 477,505`,
  `G=2: 49,392`, and the reference file's `SIZE`/`GRUNDY`/`SAFE` lines agree
  exactly.

So the claimed decomposition is **fully reproduced for this board**, not merely
spot-checked. The 60-sample request was also satisfied (30 + 30), but the full
DP is stronger.

**Limits / not proved here.**

- This is a finite verification for this board (and hence for AG(2,7) up to the
  explicit isomorphism found). It is not a general theorem for other orders,
  other boards, or s=3.
- Misère play and the `ROOT` misère bit / `PROBE` lines of the reference
  program were not part of the claimed decomposition and were not verified.
  The normal-play root value `0` and `FIRSTMOVE 1 49` were checked.
- The reference C engine was not audited; only its output numbers were compared,
  and they agree with the independent Python computation.

**Discrepancies.** None. One semantic point: reading "5-caps with a
7-extension" as "contained in *any* 7-cap" gives 395,136 such 5-caps, not
49,392; the claim's parenthetical ("the 49,392 five-subsets of maximal 7-caps")
shows that extension to a **maximal** 7-cap is intended. Under that reading the
claim is exact. Likewise "extend to 8-caps only" is read as "every 7-extension
is non-maximal"; since mixed = 0 this is the same as "has an 8-extension".
