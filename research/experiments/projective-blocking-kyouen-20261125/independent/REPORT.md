# Independent verification — projective blocking Kyouen experiment (2026-11-25)

Scope: independent audit of
`research/experiments/projective-blocking-kyouen-20261125/` and of the lemma in
the parity-graded item `K1294-parity-graded-grundy.md` (renumbered to
`K1298-parity-graded-grundy.md` by a concurrent commit during this audit).

Everything in this directory was written from scratch for the audit:
standard library only, no `grundy_full.exe`, no import of the experiment's
`scripts/`, no ILP solver.  Files outside `independent/` were only **read**.

* Python 3.12.13 (Windows), `python` on `PATH`.
* Confirmed to be reproduced by running the commands below from this directory.

## Commands

```powershell
cd research/experiments/projective-blocking-kyouen-20261125/independent
python task1_boards.py               # task 1
python task2_grundy.py               # task 2 (q=2,3)
python task2b_grundy_q4.py           # extra: complete Grundy/misere for q=4
python task3_maximal.py              # task 3
python q4_profile_representatives.py # task 3 discrepancy detail (q=4 size 9)
python task4_k3.py                   # task 4
python task5_lemma.py                # task 5
```

`run_all.ps1` runs exactly this sequence.  Machine-readable outputs are written
to `out/*.json`.

## Verdict at a glance

| Task | Content | Result |
|---|---|---|
| 1 | boards q=2,3,4 are PG(2,q) | **PASS** |
| 2 | complete Grundy + misere, q=2,3 | **PASS** (q=4 also PASS, extra) |
| 3 | maximal safe sets + complement profiles | q=3 **PASS**; q=4 counts **PASS**; q=4 size-9 profile **FAIL** (see D1) |
| 4 | K_3 = 7, 9, 9 | **PASS** |
| 5 | parity-graded lemma audit | statement **CORRECT**; applications (i),(ii) **PASS**; (iii) substance **PASS**, q=13 witness was stale (D2, now corrected); no counterexample found |

Numerical claims that were checked and **match exactly**: all of task 1, all
q=2/q=3/q=4 safe-set counts, Grundy distributions, root and misere values,
maximal-size counts, the q=3 complement profiles, the q=4 size-7 complement
profile, and K_3 = 7/9/9.

### Note on the artifact state

The audit computations were run against the experiment as it stood when the
audit started (`report.md` at commit `dfb38f6ba`, `output/structure.json`, and
the item `K1294-parity-graded-grundy.md`).  While the audit was running, a
concurrent commit/working-tree change (a) renumbered the lemma item K1294 ->
K1298 and (b) corrected `report.md` for exactly the two discrepancies found
here (the three q=4 size-9 profiles, and the M(q) witness q=13 -> q=5).
`output/structure.json` still records a single `complement_profile` for the
11,480 size-9 sets (the profile of the stored representative), so D1 remains
visible there.  The numeric results below are unaffected by these renames and
edits.

---

## Task 1 — the three boards are PG(2,q)

Boards read: `output/board_pg2q{2,3,4}.txt` (0-based points).  Checks performed
for each board:

* `n = q^2+q+1`, `b = n`, and the header agrees with the number of rows;
* every block has exactly `q+1` distinct points, all blocks distinct, all
  points in range;
* every point lies on exactly `q+1` blocks (incidence count `n(q+1)`);
* every pair of points lies on exactly one block (`C(n,2)` pairs, all
  multiplicities exactly 1);
* dual checks: every pair of blocks meets in exactly one point, and
  `b*C(q+1,2) = C(n,2)`.

| q | n | b | block size | incidences | pair multiplicities | points/block-degree | result |
|---:|---:|---:|---:|---:|---|---|---|
| 2 | 7 | 7 | 3 | 21 | all 1 (21 pairs) | all 3 | PASS |
| 3 | 13 | 13 | 4 | 52 | all 1 (78 pairs) | all 4 | PASS |
| 4 | 21 | 21 | 5 | 105 | all 1 (210 pairs) | all 5 | PASS |

For q = 2, 3, 4 the projective plane of order q is unique up to isomorphism
(the smallest non-Desarguesian plane has order 9), so these axioms certify
that each board is PG(2,q).  All checks passed with no exception.

## Task 2 — complete Grundy values and misere outcome, q = 2, 3

Two independent enumerations per board agree: a literal scan of all `2^n`
subsets and a DFS over safe sets.  Grundy values are computed by decreasing
size; misere win/lose by the recursion "terminal position is a win for the
mover".

| q | n | safe sets | safe sets by size (sizes 0..n) | Grundy 0 | Grundy 1 | root Grundy | root misere | maximal safe sets |
|---:|---:|---:|---|---:|---:|---:|---|---|
| 2 | 7 | **128** | 1,7,21,35,35,21,7,1 | **64** | **64** | **1** | **0** | **{7: 1}** |
| 3 | 13 | **4330** | 1,13,78,286,702,1170,1248,702,117,13 | **2184** | **2146** | **1** | **0** | **{7: 234, 9: 13}** |

Misere convention: `0` = first player loses (same convention as the engine's
`ROOT` line; verified by hand for q=2, where every play lasts exactly 7 moves).
Every `SIZE k total maximal grundy0` line of the experiment's
`output/grundy_pg2q{2,3}.txt` matches our recomputation exactly, as do
`SAFE`, `GRUNDY` and `ROOT`.

* q=2: maximal safe sets: only `V` itself (size 7, unique).
* q=3: maximal sizes 7 and 9; both odd; Grundy values only 0/1; the formula
  `Grundy(S) = (1-|S|) mod 2` holds for **all 4330** safe sets (0 mismatches).

**Extra, q=4** (`task2b_grundy_q4.py`, not required but it checks the report's
q=4 claims): a literal scan of all `2^21 = 2,097,152` subsets gives exactly
**180,058** safe sets (same masks as the DFS), and the DP over them gives

| q | safe sets | Grundy 0 | Grundy 1 | root Grundy | root misere | maximal safe sets |
|---:|---:|---:|---:|---:|---|---|
| 4 | **180058** | **89799** | **90259** | **1** | **0** | **{7: 360, 9: 11480}** |

All `SIZE`/`GRUNDY`/`ROOT` lines of `output/grundy_pg2q4.txt` match, and
`Grundy(S) = (9-|S|) mod 2` holds for all 180,058 safe sets (0 mismatches).

## Task 3 — maximal safe sets and complement profiles

DFS enumerating every safe set exactly once (`task3_maximal.py`); maximality is
re-checked point by point (no safe extension exists), and every complement is
checked to be an inclusion-minimal `(q-2)`-fold blocking set.

### q = 3

* safe sets: 4330; maximal: **{7: 234, 9: 13}** — matches the claim.
* complement profiles (uniform within each size class):
  * size 9 (13 sets): complement 4 points, profile **{1:12, 4:1}** (a line);
  * size 7 (234 sets): complement 6 points, profile **{1:6, 2:3, 3:4}**.
* every complement is an inclusion-minimal 1-fold (ordinary) blocking set.
* matches `output/structure.json` and the report table.

### q = 4

* safe sets: **180,058**; maximal: **{7: 360, 9: 11480}** — matches the claim.
* complements are inclusion-minimal 2-fold blocking sets (all blocks meet the
  complement in >= 2 points, and every complement point lies on a block with
  exactly 2 complement points).
* size 7 (360 sets): complement 14 points, profile **{2:7, 4:14}** — uniform,
  matches the claim.
* **size 9 (11,480 sets): the claimed single profile is wrong.**  The
  complements fall into **three** distinct line profiles:

| complement line profile | number of maximal sets |
|---|---|
| {2:10, 3:6, 4:3, 5:2} (the claimed one) | 10,080 |
| {2:9, 3:9, 5:3} | 1,120 |
| {2:12, 4:9} | 280 |

  Counts sum to 11,480.  Each profile satisfies the incidence identity
  `sum_s s*count(s) = |X|*(q+1) = 12*5 = 60`, so this is not an arithmetic
  artefact.  Representatives (verified line by line against the board file by
  hand) are printed by `q4_profile_representatives.py`:

  * `{2:10,3:6,4:3,5:2}`: `S = {0,1,2,5,6,9,11,14,15}` (this is the
    representative stored in `structure.json`);
  * `{2:9,3:9,5:3}`: `S = {0,1,2,5,6,11,12,13,19}`;
  * `{2:12,4:9}`: `S = {0,1,2,5,6,13,16,18,20}`.

  All three sets are safe, have size 9, and admit no safe extension.  See
  discrepancy **D1**.

## Task 4 — K_3(PG(2,q)) = 7, 9, 9

Exact searches only (`task4_k3.py`), using heredity of safety (any safe set of
size >= 10 contains a safe 10-subset):

| q | K_3 (recomputed) | claimed | witness | safe 10-subsets | safe k-subsets, k>10 | branch-and-bound |
|---:|---:|---:|---|---:|---|---:|
| 2 | **7** | 7 | all 7 points | 0 (no 10-subsets) | — | 7 |
| 3 | **9** | 9 | {1,2,3,4,5,6,7,8,9} | 0 of 286 | 0 (k=11,12,13) | 9 |
| 4 | **9** | 9 | {1,2,3,5,6,7,9,10,11} | 0 of 352,716 | 0 (k=11..21) | 9 |

For q=4 this is a complete exhaustive proof: all `C(21,10)=352,716` ten-subsets
are unsafe, and all `C(21,k)` for k=11..21 contain no safe set; an explicit
safe 9-set exists.  Maximal safe set size also equals 9 (task 3).  q=2 is
trivial because every line has exactly 3 points; q=3 was brute-forced over all
8192 subsets.

## Task 5 — audit of the parity-graded lemma (K1294 -> K1298)

**Statement.** For a finite hypergraph board with the "at most 3 points per
block" rule, if all inclusion-maximal safe sets have the same size parity `p`,
then `Grundy(S) = (p-|S|) mod 2` for every safe `S` (normal play), hence all
Grundy values are in {0,1}.

**Proof audit: the statement is correct as written.**  The induction on `|S|`
descending is valid:

* maximal `S`: no move, `Grundy(S)=0`, and `|S| ≡ p`, so the formula gives 0;
* non-maximal `S`: it has at least one legal move.  Every child `S∪{x}` is safe
  (safety is downward closed), hence is contained in some maximal safe set, all
  of which have size `≡ p`.  By induction on the (larger) child,
  `Grundy(S∪{x}) = (p-(|S|+1)) mod 2`, the same value `b ∈ {0,1}` for every
  child.  Then `mex{b} = 1-b = (p-|S|) mod 2`.

No logical gap: the argument uses only finiteness, downward closure of safety,
and the parity hypothesis; it does not use the board's geometry.  The following
are expository (non-logical) gaps in the written proof:

1. the sentence "`S∪{x}` を含む極大集合はすべて `S` を含むのでサイズは `≡ p`"
   gives the wrong reason: the size congruence comes from the hypothesis, not
   from containment; and one must note that every safe set is contained in a
   maximal safe set (finiteness);
2. it should be said explicitly that a non-maximal safe set has at least one
   legal move, and that `mex` of the singleton `{b}` is `1-b`;
3. the lemma is a **normal-play** statement; it does not apply to misere play
   (and the K1294 applications are normal-play).  Applying it to misere would be
   wrong, e.g. AG(3,2) has normal root 0 but misere root 1.

### Application (i): design boards with even K (AG(3,2) K=4, AG(4,2) K=6)

Recomputed directly from the design experiment's board files, with all seven
design boards (they are the boards K1294 cites):

| board | n | safe sets | maximal by size | uniform parity | p | Grundy distribution | root (normal/misere) | formula mismatches |
|---|---:|---:|---|---|---:|---|---|---:|
| AG(3,2) | 8 | 149 | {4: 56} | yes (K=4 even) | 0 | {0:85, 1:64} | 0 / 1 | 0 |
| AG(4,2) | 16 | 5513 | {6: 448} | yes (K=6 even) | 0 | {0:2249, 1:3264} | 0 / 1 | 0 |
| W_11 | 11 | 232 | {3: 165} | yes | 1 | {0:176, 1:56} | 1 / 0 | 0 |
| W_12 | 12 | 299 | {3: 220} | yes | 1 | {0:232, 1:67} | 1 / 0 | 0 |
| W_22 | 22 | 18162 | {7: 352} | yes | 1 | {0:9306, 1:8856} | 1 / 0 | 0 |
| W_23 | 23 | 2048 | {3: 1771} | yes | 1 | {0:1794, 1:254} | 1 / 0 | 0 |
| W_24 | 24 | 2325 | {3: 2024} | yes | 1 | {0:2048, 1:277} | 1 / 0 | 0 |

All seven boards are **graded** (a single maximal-safe-set size K), so the
lemma applies with `p = K mod 2`; `Grundy(S) = (K-|S|) mod 2` holds for every
safe set (0 mismatches on all boards), the even-K boards have root Grundy 0
(P-position), and every value matches `output/summary.json` and the
`grundy_*.txt` engine outputs.  Application (i) is correct.

### Application (ii): PG(2,q), q <= 4

Maximal safe sizes `{7}`, `{7,9}`, `{7,9}` — all odd.  Complete Grundy values
(above) are in {0,1} only, root Grundy 1 for all three, and the formula
`Grundy(S) = (1-|S|) mod 2` holds for every safe set (0 mismatches among
128 / 4330 / 180,058 sets).  Application (ii) is correct.

### Application (iii): M(q) (inversive plane) mixed parity

The hypothesis indeed fails for M(q), and Grundy values >= 2 do occur there —
so the contrast drawn by K1294 is substantively correct.  The best witnesses
are q=5..9 in K1253 (the reference K1294 cites):

* K1253 table: q=5: K=6, s=5 (maximal sizes 5 and 6 both occur), Grundy
  distribution includes `2: 11,700`; q=7: maximal sizes {5,6}, `2: 29,400`;
  q=8: {5,6,7}, `2: 3,931,200`; q=9: K=9, s=6, Grundy value `3` appears.
  Thus mixed parity **and** Grundy >= 2 are already exhibited at q=5.

**Discrepancy D2 (documentation only).**  As read at audit start, the item
(K1294, now K1298) said "反転平面 M(q) は s(q)<K(q) で **q=13 では 7 と 8 が
混在**する".  That was stale:

* K1253 only computes q <= 9, so it cannot support a q=13 statement;
* the current SSOT K1058 (§10co of the 2026-11-20 correction, "記録された K は
  q ≥ 13 で誤りだった") retracts `K(13)=8` and proves `K(13) >= 10` with a
  verified arc (the old "8" is wrong; the pre-artifact value 10 is right);
  `s(13)=7` is only a randomized measurement (K1058 §10i explicitly says it is
  not an existence proof).

Even so, the conclusion "M(q) violates the hypothesis" remains true, with q=5
(or 7, 8, 9) as the correct witness; after the audit both the item K1298 and
`report.md` were corrected to the q=5 witness, so D2 is resolved in the current
tree (it is recorded here because it was present in the audited revision).  The
lemma itself is unaffected.

### Counterexample search on small artificial hypergraphs

Exhaustive and random boards, all analysed by full enumeration of `2^n`
subsets (`task5_lemma.py`, part B).  For every board whose maximal safe sets
have a uniform size parity `p` we checked the formula on **every** safe set and
looked for a Grundy value >= 2.

| family | boards | uniform parity | uniform with G>=2 | formula violations | mixed parity with G>=2 |
|---|---:|---:|---:|---:|---:|
| exhaustive n=4, all block sets of size 3 and 4 | 32 | 32 | 0 | 0 | 0 |
| exhaustive n=5, all block sets of size 3 and 4 | 32,768 | 7,168 | **0** | **0** | 25,600 |
| exhaustive n=6, all 4-uniform block sets | 32,768 | 4,019 | **0** | **0** | 28,749 |
| random n=6, 400 boards, blocks of size 3–5 | 400 | 123 | **0** | **0** | 277 |
| random n=7, 400 boards, blocks of size 3–5 | 400 | 108 | **0** | **0** | 292 |
| random n=8, 400 boards, blocks of size 3–5 | 400 | 111 | **0** | **0** | 289 |
| **total** | **66,768** | **11,561** | **0** | **0** | 55,207 |

**No counterexample was found**: on all 11,561 uniform-parity boards the formula
holds for every safe set and the maximal Grundy value is 1.  This is consistent
with the proof (which shows no counterexample can exist).  In these search
families, *every* mixed-parity board had some Grundy value >= 2 (55,207/55,207),
so the parity hypothesis is not vacuous and the lemma's contrapositive is
visible in the data.  Note that a block of size 3 can never violate "at most 3
points per block", so only blocks of size >= 4 constrain the game; nevertheless
the n=4 and n=5 exhaustive runs include all 3-blocks as requested.

## Discrepancies

**D1 (substantive, affects a stated numeric claim in task 3).**
As audited, the report (`report.md` section 3) and `output/structure.json` gave
a single complement line profile `{2:10, 3:6, 4:3, 5:2}` for all 11,480 maximal
safe sets of size 9 in PG(2,4).  This is not a class-wide profile: there are
three profiles, `{2:10,3:6,4:3,5:2}` (10,080 sets), `{2:9,3:9,5:3}` (1,120 sets)
and `{2:12,4:9}` (280 sets).  The quoted profile is the one of the
representative stored in `structure.json` (and of the majority class); it
should either be attributed to that representative/majority class, or all three
profiles should be listed.  The *count* (11,480) and the 14-point profile
`{2:7,4:14}` for the size-7 class are correct, as is the general statement that
the complements are minimal 2-fold blocking sets.  The report already noted
("q=4 の 12 点 2 重ブロッキング集合 11,480 個の構造・分類は未調査"), so this was
a profile claim that outran its data rather than a computational error.
`report.md` has since been corrected to list the three profiles; the single
`complement_profile` in `output/structure.json` still stands (it matches the
stored representative), so that data file should be read as representative-only.

**D2 (minor, documentation only).**  As audited, the lemma item's application
example said "q=13 で 7 と 8 混在".  That was stale: K1253 covers only q <= 9,
and the current K1058 retracts `K(13)=8` (now `K(13) >= 10`); `s(13)=7` is a
randomized measurement, not an exhaustive fact.  Use q=5 (maximal sizes 5 and 6,
Grundy 2 present) or q=7/8 from K1253 instead.  The lemma and its application
are unaffected.  After the audit the item (K1298) and `report.md` were corrected
to the q=5 witness, so D2 is resolved in the current tree.

No other discrepancy was found: all other numeric claims checked here match.

## Limitations

* Only q=2,3,4 boards were in scope (the q=5, q=7 board files were not checked).
* The PGL orbit claims of the experiment (q=3 single orbits, q=4 unclassified)
  were not re-verified (out of scope for this audit).
* No ILP was used anywhere; q=4 maxima are proved by exhaustive 10-subset
  enumeration plus branch and bound, which is a complete proof.
* The independent scripts are pure Python and by construction share no code
  with the experiment's implementation.

## Files

| file | role |
|---|---|
| `common.py` | board parser, safe-set DFS, Grundy/misere DP, profile helpers |
| `task1_boards.py` | task 1 |
| `task2_grundy.py` | task 2 (q=2,3) |
| `task2b_grundy_q4.py` | extra: q=4 complete Grundy via 2^21 scan |
| `task3_maximal.py` | task 3 (q=3,4 maximal sets and profiles) |
| `q4_profile_representatives.py` | D1 detail: representatives of the 3 q=4 size-9 profiles |
| `task4_k3.py` | task 4 |
| `task5_lemma.py` | task 5 (applications + counterexample search) |
| `run_all.ps1` | runs all of the above |
| `out/*.json` | machine-readable results |
