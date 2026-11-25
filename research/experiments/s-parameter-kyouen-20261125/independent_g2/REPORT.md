# Independent verification of K1336 — Grundy-2 positions in three s=2 cap games

**Verifier:** independent sub-agent (separate implementation, Python 3.12.13, standard library only)
**Date:** 2026-11-26
**Scope:** only `research/experiments/s-parameter-kyouen-20261125/independent_g2/`.
No commit was made and no file outside this directory was modified.

**Overall verdict: PASS on all five requested tasks.** Every number in the K1336
table is confirmed by independent computation (the PG(2,9) total G=2 value uses
K1333 as the task permits, with the entire 14,152,320-subset side independently
recomputed). One wording defect in K1336 is documented below: the
sentence "the Grundy-2 positions are exactly the caps contained in an odd-size
maximal cap" is false as literally written. The verified statement is the
sharper one actually tabulated by K1336: **the G=2 positions are exactly the
`m-1`-subsets of the odd maximal `m`-caps** (`m=7` for PG(2,9) and AG(2,7),
`m=5` for AG(2,5)).

| Task | Verdict |
|---|---|
| 1. Board validity / s=2 incidence | **PASS** |
| 2. Maximal-cap enumeration, subset counts, distinctness | **PASS** |
| 3. Representative full Grundy by upset DP, mixed extensions | **PASS** |
| 4. Published G=2 totals | **PASS** |
| 5. Proved vs. conjectural statement | **PASS** (with the K1336 wording correction in §5.2) |

---

## 0. Inputs and integrity

| Board | File | SHA-256 |
|---|---|---|
| PG(2,9) | [`board_pg2q9.txt`](../../pg2q9-cap-game-20261125/output/board_pg2q9.txt) | `81c82d03b5094c3b3b4c912b8144b4cb119b2db365b6790e0c844dfbf228486b` |
| AG(2,7) | [`board_ag2q7.txt`](../output/board_ag2q7.txt) | `17e2bae586f60dd243aa201b451a5952b02360477e7bf066bbe25f28ad088594` |
| AG(2,5) | [`board_ag2q5.txt`](../output/board_ag2q5.txt) | `b6fe706177f8d9d19753d770772fb3e7c40f9161bc941aec4bca8f4cd1039b1c` |

Other inputs: [`census_pg2q9.txt`](../../pg2q9-cap-game-20261125/output/census_pg2q9.txt),
[`gens.txt`](../../pg2q9-cap-game-20261125/output/gens.txt),
[`grundy_ag2q7_s2.txt`](../../pg2q7-cap-game-20261125/output/grundy_ag2q7_s2.txt),
[`grundy_general.json`](../output/grundy_general.json),
[`results.txt`](../../pg2q9-sixcap-20261126/results.txt) (six-cap distinctness).

Game: a position is a **cap** `S` (no line contains 3 points of `S`); a move
adds one point while remaining a cap; normal play. `G(S) = mex{G(S+p) : p
addable}`, so maximal caps are exactly the terminal positions (`G=0`).

---

## 1. Task 1 — boards are valid s=2 incidence structures

**PASS.** Independent parsing and full incidence checks:

| Check | PG(2,9) | AG(2,7) | AG(2,5) |
|---|---:|---:|---:|
| points `n` / lines `b` | 91 / 91 | 49 / 56 | 25 / 30 |
| line size `k` | 10 | 7 | 5 |
| point degree | 10 | 8 | 6 |
| pairs of points | 4,095 | 1,176 | 300 |
| pairs on exactly one line | 4,095 | 1,176 | 300 |
| pairs on more than one line | 0 | 0 | 0 |
| line intersections | all 1 (projective) | 0 or 1 | 0 or 1 |
| parallel classes | — | 8 classes × 7 lines | 6 classes × 5 lines |
| structure | projective plane order 9 | affine plane order 7 | affine plane order 5 |

All pairs lie on **exactly** one line (stronger than the required "at most
one"), so no three points are collinear on more than one line and the s=2 cap
condition is well-defined. Each board is a `2-(v,k,1)` design with the expected
parameters. Raw output: [`results/task1_boards.json`](results/task1_boards.json).

---

## 2. Task 2 — maximal caps, subsets, distinctness

**PASS.**

Method:
- **AG(2,5), AG(2,7):** exhaustive DFS over all caps (incremental line counts),
  followed by a full descending-size Grundy DP. This reproduces the complete
  cap census, not just the maximal layer.
- **PG(2,9):** the published census is checked for internal consistency and its
  rows `k<=4` are re-enumerated independently. Independently, a complete
  7-arc is generated: the seed `{33,39,57,70,74,80,89}` is checked to be a
  maximal 7-cap, the eight published point permutations are checked to be
  incidence automorphisms, and the orbit under them is enumerated by BFS.
  Every orbit element is a maximal 7-cap (automorphism invariance plus seed
  check). All `C(7,6)=7` six-subsets are inserted into a Python hash set.

| Board | total caps | maximal caps by size | odd `m` | `m`-caps | `(m-1)`-subsets generated | distinct | duplicates | claimed | G=2 total |
|---|---:|---|---:|---:|---:|---:|---:|---:|---:|
| PG(2,9) | 128,917,712 (census) | 6: 707,616; 7: **2,021,760**; 8: 5,307,120; 10: 58,968 | 7 | 2,021,760 | 14,152,320 | **14,152,320** | **0** | 14,152,320 | 14,152,320 |
| AG(2,7) | 1,108,724 | 6: 271,656; 7: **2,352**; 8: 6,174 | 7 | 2,352 | 49,392 | **49,392** | **0** | 49,392 | 49,392 |
| AG(2,5) | 16,426 | 5: **600**; 6: 1,000 | 5 | 600 | 3,000 | **3,000** | **0** | 3,000 | 3,000 |

Additional PG(2,9) details:

- Census: `N 91 B 91 SAFE 128917712`; the 11 size rows sum to `128,917,712`;
  maximal counts sum to `8,095,464`; `9`-caps `= 10 × 10`-caps; non-maximal
  `8`-caps `= C(10,8) ×` ovals. All checks pass.
- Independent low-size census (`k=0..4`): `1, 91, 4,095, 110,565, 1,769,040`
  and **0 maximal caps** at each size — exactly the census rows.
- The 8 generators are permutations of the 91 points and map every one of the
  91 lines to a line (0 bad lines each).
- The BFS orbit has **2,021,760** elements, matching the census maximal-7
  count. BFS levels: `9, 61, 371, 2125, 11630, 60216, 283716, 1042529,
  1948515, 2021759, 2021760`. A random sample of 1,000 orbit elements was
  re-checked to be maximal 7-caps.
- `C(7,6)-subset` count `14,152,320 = 7 × 2,021,760`, all distinct; this is
  27.21% of the 52,009,776 six-caps.

Caveat: completeness of the PG maximal-7 list uses the census total
`2,021,760` as the matching upper bound (the task explicitly allows verifying
the count from the census instead of re-enumerating all 128.9M caps). The
orbit itself is an independent construction of 2,021,760 distinct maximal
7-caps, so the lower bound is unconditional.

Raw output: [`results/task2_AG2q5.json`](results/task2_AG2q5.json),
[`results/task2_AG2q7.json`](results/task2_AG2q7.json),
[`results/task2_pg.json`](results/task2_pg.json). The 2,021,760 seven-arcs are
saved compactly in [`results/pg_max7_arcs.bin`](results/pg_max7_arcs.bin)
(7 bytes per arc, 14,152,320 bytes).

---

## 3. Task 3 — full Grundy values of representatives by upset DP

**PASS.** For each board, 8 random representatives were drawn as random
subsets of random maximal odd caps (one point short for PG(2,9) and AG(2,5),
two points short for AG(2,7)). For each representative `X`, the entire upset
`{caps T : X ⊆ T}` was enumerated and the exact Grundy value computed by a
descending-size DP over that upset. The maximal caps in the upset are exactly
the maximal extensions of `X`.

| Board | reps | `|X|` | upset positions | G(X) | maximal-extension size histogram | mixed? | verdict |
|---|---:|---:|---:|---:|---|---|---|
| PG(2,9) | 8 | 6 | 11 | **2** | `{7: 1, 8: 3}` | yes `{7,8}` | PASS (8/8) |
| AG(2,7) | 8 | 5 | 8 | **2** | `{6: 4, 7: 1}` | yes `{6,7}` | PASS (8/8) |
| AG(2,5) | 8 | 4 | 8 | **2** | `{5: 1, 6: 2}` | yes `{5,6}` | PASS (8/8) |

All representatives also have exactly **one** odd maximal extension (the
parent maximal cap), matching the distinctness result. The complete list of
representatives is in [`results/task3_reps.json`](results/task3_reps.json);
examples:

- PG(2,9): `[9,13,17,36,64,68]` → G=2, extensions `{7:1, 8:3}`.
- AG(2,7): `[0,9,14,33,40]` → G=2, extensions `{6:4, 7:1}`.
- AG(2,5): `[5,15,16,23]` → G=2, extensions `{5:1, 6:2}`.

---

## 4. Task 4 — published G=2 totals

**PASS.**

| Board | Published source | Published value | Independent result | Match |
|---|---|---|---:|---|
| AG(2,7) | `grundy_ag2q7_s2.txt`: `GRUNDY 2 49392` | 49,392 | full re-computation: `{0: 581,827, 1: 477,505, 2: 49,392}` | **PASS** |
| AG(2,5) | `grundy_general.json`, `AG2(5)_s2.grundy_dist["2"]` | 3,000 | full re-computation: `{0: 5,401, 1: 8,025, 2: 3,000}` | **PASS** |
| PG(2,9) | K1333 (and `pg2q9-sixcap-20261126/results.txt`) | 14,152,320 | 14,152,320 distinct six-subsets; 20-sample DP (below) | **PASS** |

The AG(2,7) full re-computation also reproduces every size total, the
maximal-count column and the G=0 column of the `SIZE` lines in
`grundy_ag2q7_s2.txt`; the AG(2,5) full re-computation reproduces every
`size_counts`, `maximal_by_size`, `grundy_dist`, and `root_grundy` field of
the published JSON.

PG(2,9) cross-checks:

- `results.txt`: `n = 14152320 = 7 * 2021760`, `distinct = 14152320`,
  `duplicates = 0` — matches our independent orbit/hash-set computation.
- Arithmetic: `52,009,776 − 14,152,320 = 37,857,456`, matching K1333's G=0
  count for six-caps.
- Sample of 20 random six-caps (10 with a maximal-7 child, 10 without):
  - with maximal-7 child: **all G=2**, all with maximal extensions `{7,8}`;
  - without maximal-7 child: **all G=0**, maximal extensions even-only
    (`{8}`, `{8,10}`, or `{6}` for a maximal six-cap);
  - this independently illustrates the K1333 six-cap classification. Raw data:
    [`results/task4_pg.json`](results/task4_pg.json).

Note: the *exhaustive* PG(2,9) G=2 total is K1333's value (as the task
permits). We independently verified the exhaustive 14,152,320 distinct
six-subset side, all representative/sample G values, and the arithmetic; we
did not run a full DP over all 128,917,712 caps.

---

## 5. Task 5 — what is proved, what is not

### 5.1 Proved/verified by this audit

1. All three boards are valid s=2 incidence structures (indeed `2-(v,k,1)`
   designs with the expected parameters).
2. **AG(2,5):** exact exhaustive proof that `{X : G(X)=2}` equals the set of
   4-subsets of maximal 5-caps; 600 maximal 5-caps, 3,000 subsets, all
   distinct; total G=2 = 3,000.
3. **AG(2,7):** exact exhaustive proof that `{X : G(X)=2}` equals the set of
   5-subsets of maximal 7-caps; 2,352 maximal 7-caps, 49,392 subsets, all
   distinct; total G=2 = 49,392.
4. **PG(2,9):** 2,021,760 maximal 7-caps (orbit matching the census upper
   bound) and 14,152,320 six-subsets, all distinct; these six-subsets are
   G=2 (representatives and 20 samples), and the total 14,152,320 matches
   K1333's exhaustive classification.
5. For 8 random representatives on each board: exact upset-DP Grundy value is
   2, and the maximal extensions have mixed size `{7,8}` / `{6,7}` / `{5,6}`
   respectively.

### 5.2 The literal K1336 wording is false

K1336 says "the G=2 positions are exactly the caps contained in an odd-size
maximal cap". Read literally (all subsets), this is false even on these three
boards. An odd maximal cap `M` is contained in an odd maximal cap (itself) but
is terminal, hence `G(M)=0`. Lower subsets are also not generally G=2. Exact
upset-DP values for one maximal cap per board:

| Board | odd maximal cap `M` | subset `X` | `|X|` | G(X) | maximal extensions of X |
|---|---|---:|---:|---|
| PG(2,9) | `[33,39,57,70,74,80,89]` | `[33,39,57,70,74]` | 5 | **1** | `{7,8,10}` |
| PG(2,9) | same | `[33,39,57,70]` | 4 | **0** | `{6,7,8,10}` |
| PG(2,9) | same | `[33,39,57]` | 3 | **1** | `{6,7,8,10}` |
| AG(2,7) | `[0,1,7,9,19,36,40]` | `[0,1,7,9,19,36]` | 6 | **1** | `{7}` |
| AG(2,7) | same | `[0,1,7,9]` | 4 | **0** | `{6,7,8}` |
| AG(2,5) | `[0,1,5,7,17]` | `[0,1,5]` | 3 | **1** | `{5,6}` |
| AG(2,5) | same | `[0,1]` | 2 | **0** | `{5,6}` |

Thus "contained in an odd maximal cap" is not sufficient for G=2. The correct
exact statement, verified here, is:

> **G=2 positions = the `(m-1)`-subsets of the odd maximal `m`-caps.**

Quantitatively, the literal reading also fails by counting: PG(2,9)'s maximal
7-caps have `2,021,760 × C(7,5) = 42,456,960` five-subsets with multiplicity,
while the whole board has only `14,859,936` five-caps and K1333 gives G=1 for
every one of them.

The K1336 table itself lists only this `m-1` layer, so its *numbers* are
correct; only its prose sentence is too broad. A second imprecise sentence in
K1336 ("positions with only even maximal extensions are G=0, the others are
G=1") should also be read with care: mixed-parity maximal extensions can
belong to G=0 or G=1 positions (e.g. PG(2,9) 5-subset above has mixed
`{7,8,10}` and G=1; the 4-subset has mixed `{6,7,8,10}` and G=0). The local
K1298 corollary concerns the subgame above `S`, not `G(S)` itself.

### 5.3 What remains conjectural

- The **general implication** "contained in an odd-size maximal cap ⇒ G=2"
  (or its correct one-below version) is not proved for arbitrary s=2 boards.
  It is an observation on these three boards, supported by exhaustive
  computation for the two AG boards and by K1333 plus extensive independent
  checks for PG(2,9).
- The **exact structural reason** for the mixed-child Grundy values
  (a maximal odd extension gives a G=0 child, and the other children have
  even maximal extensions hence G=1) is understood case-by-case via K1298,
  but no general theorem is established here.
- Completeness of the PG maximal-7 enumeration is tied to the census count
  2,021,760 (and the independent C census in `pg2q9-sixcap-20261126`); the
  orbit construction gives the matching lower bound but does not by itself
  prove the upper bound.

---

## 6. Discrepancies and notes

1. **Wording (main discrepancy):** K1336's prose "all caps contained in an
   odd-size maximal cap" is false literally; the table's `m-1`-subset
   statement is correct. This is a documentation defect, not a numerical one.
2. **Task wording:** the task text says "5-/6-/5-subsets"; the actual layers
   per K1336 are 4-subsets (AG(2,5)), 5-subsets (AG(2,7)), 6-subsets
   (PG(2,9)). This audit used the sizes in the K1336 table.
3. **PG(2,9) exhaustive G=2 total:** relies on K1333, as allowed by the task.
   Everything else about PG(2,9) (maximal 7 count, six-subsets, distinctness,
   representative G=2, arithmetic) is independently recomputed.
4. **Pre-existing worktree state:** the repository already had unrelated
   modified/deleted files before this audit. No file outside
   `independent_g2/` was touched by this audit; nothing was committed.

---

## 7. Reproduction

Run from this directory (`research/experiments/s-parameter-kyouen-20261125/independent_g2`):

```sh
python task1_boards.py        # Task 1
python task2_ag.py AG2q5      # Task 2/4, AG(2,5)
python task2_ag.py AG2q7      # Task 2/4, AG(2,7)
python task2_pg.py            # Task 2/4, PG(2,9) (writes results/pg_max7_arcs.bin)
python task3_reps.py          # Task 3 (needs the arcs file)
python task4_pg.py            # Task 4 PG samples and published data
python task5_literal.py       # literal-wording counterexamples
python audit_consistency.py   # 48/48 cross-checks over the JSON artifacts
```

All outputs are written under `results/`. Runtime was about 2–3 minutes total
on one machine (PG orbit BFS ~73 s, six-subset hash ~21 s, AG(2,7) full DP
~22 s).

Files:

- [`g2common.py`](g2common.py) — board loader, validator, cap enumeration,
  addable-point test, Grundy DP.
- [`task1_boards.py`](task1_boards.py), [`task2_ag.py`](task2_ag.py),
  [`task2_pg.py`](task2_pg.py), [`task3_reps.py`](task3_reps.py),
  [`task4_pg.py`](task4_pg.py), [`task5_literal.py`](task5_literal.py),
  [`audit_consistency.py`](audit_consistency.py).
- Results: [`task1_boards.json`](results/task1_boards.json),
  [`task2_AG2q5.json`](results/task2_AG2q5.json),
  [`task2_AG2q7.json`](results/task2_AG2q7.json),
  [`task2_pg.json`](results/task2_pg.json),
  [`task3_reps.json`](results/task3_reps.json),
  [`task4_pg.json`](results/task4_pg.json),
  [`task5_literal.json`](results/task5_literal.json),
  [`pg_max7_arcs.bin`](results/pg_max7_arcs.bin).
