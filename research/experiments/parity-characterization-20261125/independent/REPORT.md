# Independent verification — K1298 parity-graded Grundy theorem

Verifier: independent subagent (no shared code with the original experiment).
Date: 2026-11-25.
Scope: read-only inspection of `research/knowledge/items/K1298-parity-graded-grundy.md`
and the board file `research/experiments/projective-blocking-kyouen-20261125/output/board_pg2q5.txt`;
all new files are confined to
`research/experiments/parity-characterization-20261125/independent/`.
Nothing was committed and nothing outside this directory was modified.
Python standard library only.

## Verdict summary

| Task | Verdict |
|---|---|
| 1. Audit of the proof logic | **PASS** (sound; two expository notes, no mathematical gap) |
| 2. Exhaustive + random computational check | **PASS** (13,096 (board, s) instances; 0 violations) |
| 3. PG(2,5) cap game | **PASS** (board is a projective plane of order 5; all claimed counts reproduced exactly) |

No numerical discrepancy was found. The only discrepancies are two imprecise
sentences in the item's prose/evidence metadata, listed in
[Discrepancies](#discrepancies); neither affects the theorem.

---

## Task 1 — audit of the proof logic

The theorem (normal play, terminal position = no move = loss) is:

* **(a)** every position has Grundy value 0 or 1;
* **(b)** all maximal safe sets have the same size parity;
* **(c)** for every position `S`, all maximal extensions of `S` have the same
  size parity.

The item proves `(b) ⇒ (a) ⇒ (c) ⇒ (b)`. I checked each step.

### Useful lemma (used implicitly, valid)

For a safe set `S`, the maximal extensions of `S` (maximal elements of
`{T : S ⊆ T, T safe}`) are **exactly** the maximal safe sets containing `S`.
Indeed, if `T` is maximal among safe supersets of `S` and `T ⊊ T'` with `T'`
safe, then `T'` is also a safe superset of `S`, a contradiction; conversely a
globally maximal safe set containing `S` cannot be properly extended at all.
Consequently:

* `(b) ⇒ (c)` is immediate (all maximal extensions of every `S` have parity `p`);
* `(c) ⇒ (b)` is `(c)` at `S = ∅` (the empty set is safe since
  `|∅ ∩ B| = 0 ≤ s` for the non-negative `s` used by the theorem).

So the only non-trivial implications are `(b) ⇒ (a)` and `(a) ⇒ (c)`.

### `(b) ⇒ (a)`: valid

Assume all maximal safe sets have size `≡ p (mod 2)`. For every position `S`,
all maximal extensions of `S` are maximal safe sets (lemma), hence all have
size `≡ p`; therefore every complete play from `S` has length
`|T| − |S| ≡ p − |S| (mod 2)`. Only the **parity** is fixed; sizes themselves
may differ by even amounts.

Induction on `n − |S|` (equivalently, downward on the position lattice):

* children of `S` have size `|S| + 1` and are safe, so by induction each child
  `C` has `G(C) = (p − |S| − 1) mod 2`;
* if `(p − |S|)` is even, every child has value `1` (or there is no child, when
  `S` is maximal), hence `mex = 0 = (p − |S|) mod 2`;
* if `(p − |S|)` is odd, `S` is **not** maximal (a maximal set has size
  `≡ p`), so `S` has at least one child, every child has value `0`, and
  `mex = 1 = (p − |S|) mod 2`.

This is a complete induction; the base case (maximal `S`) is included. Valid.

### `(a) ⇒ (c)`: valid — yes, (a) really implies (c)

Under `(a)` every Grundy value lies in `{0,1}`. The mex characterisations used
are exactly:

* `G(T) = 0`: `0` does not occur among the children's values. Since all values
  are in `{0,1}`, **every** child has value `1`. (If `T` is maximal there are
  no children.)
* `G(T) = 1`: `mex = 1` means `0` occurs among the children's values and `1`
  does not. Since all values are in `{0,1}`, **every** child has value `0`.
  Also `G(T) = 1` is impossible for a terminal `T`, so at least one child
  exists.

Therefore along **every** play the values alternate
`G(S), 1−G(S), G(S), …`, and every terminal position (maximal safe set) has
Grundy value `0` (normal play: `mex ∅ = 0`). If `G(S) = 0` the number of
moves to any maximal extension `T` is even; if `G(S) = 1` it is odd. Thus
`|T| ≡ |S| + G(S) (mod 2)` for **every** maximal extension `T` of `S`, which is
exactly `(c)`. No gap.

On the specific question asked: the sentence "along any maximal play the Grundy
values alternate 0,1,0,1,… and end at 0" is **correct here, but only because
hypothesis (a) is in force**. It is not a general fact about games: without
(a), a position of Grundy 1 may have children with values `0, 2, 3, …`, and a
position of Grundy 0 may have children with values `2, 3, …`; parity of play
length is then not determined. In the item the sentence sits inside the
`(a) ⇒ (c)` proof, so its use is legitimate. The two implications of mex used
are exactly the mex-0 and mex-1 branches; both are needed.

### `(c) ⇒ (b)`: valid

Apply `(c)` to `S = ∅`; its maximal extensions are the maximal safe sets. Valid.

### Localized corollary: true, but its one-line justification is imprecise

The corollary says: for a position `S`, the subgame above `S` has all Grundy
values in `{0,1}` **iff** all maximal extensions of `S` have the same size
parity.

The **statement is true**:

* `⇐`: use the `(b) ⇒ (a)` induction inside the subgame. Every maximal
  extension of a position `T ⊇ S` (within the subgame) is again a maximal safe
  set containing `S` (lemma), hence has parity `p_S`; the induction gives
  `G(T) = (p_S − |T|) mod 2 ∈ {0,1}`.
* `⇒`: the `(a) ⇒ (c)` argument uses only "all values in `{0,1}`" and
  "terminal positions have value 0"; it applies verbatim to the subgame and
  yields parity uniformity of the maximal extensions of `S`.

However, the parenthetical justification "(部分ゲームに定理を適用)" — "apply the
theorem to the subgame" — is not literally immediate: the subgame's positions
are `T ⊇ S` with constraints `|T ∩ B| ≤ s`, i.e. block-dependent residual
capacities `|U ∩ B| ≤ s − |S ∩ B|` on `V \ S`, which is not a uniform-`s`
hypergraph game as defined in the item. The same **proof** goes through
verbatim (it only uses maximal-extension parity), so this is an expository
imprecision, not a correctness gap. My computation checks the localized
equivalence at **every position of every instance** (13,096 instances,
0 failures), so the statement itself is confirmed.

### Grundy / misère formula

Under `(b)` with common parity `p`, `G(S) = (p − |S|) mod 2` follows from the
`(b) ⇒ (a)` induction. For misère (no move **wins**) every maximal play from
`S` has length parity `L = (p − |S|) mod 2`. Induction on the game DAG gives
`W(S) = 1` iff `L` is even: if `S` is terminal then `L = 0` and `W(S) = 1`;
otherwise every child `C` has all its maximal plays of parity `L − 1`, so by
induction `W(C) = ((L − 1) even) = (L odd)`, and the misère recursion
`W(S) = any(¬W(C))` gives `W(S) = (L even)`. Hence `misere_win(S) = 1` iff
`(p − |S|)` is even. Valid. Note that `S` need not be maximal when `L` is
even (e.g. the unconstrained 2-point game has `p = 0`, `S = ∅`, and all plays
have even length 2); it is the parity of the play length, not maximality of
`S`, that determines the misère outcome. (My DP uses the standard misère
recursion "terminal = win" and reproduces this on all uniform instances.)

### Minor issues in the written item (not in the theorem)

1. The YAML `evidence:` field says "任意の完全プレイの長さが `p − |S|` に固定され"
   ("every complete play's length is fixed to `p − |S|`"). This is false when
   maximal sizes differ by even amounts (e.g. maximal sizes 4 and 6): only the
   **parity** is fixed. The Markdown body states it correctly
   ("常に `p − |S|` と同パリティ"). The induction only needs parity, so this is
   a wording error in the evidence field, not a gap.
2. The localized corollary's "apply the theorem to the subgame" wording
   discussed above (subgame is a residual-capacity game). Statement correct,
   justification should say "same induction".

**Task 1 verdict: PASS.** All three implications and the localized corollary
are logically sound; the two notes are expository.

---

## Task 2 — independent computational check

### Implementation (from scratch)

`independent/verify_boards.py` (own code, only Python stdlib) represents a
board as point bitmasks. For each `(n, blocks, s)` it:

1. marks the safe sets (`|S ∩ B| ≤ s` for every block; blocks with `|B| ≤ s`
   are dropped as inactive);
2. computes `Grundy(S)` for all positions by descending bitmask order
   (children are strict supersets, hence numerically larger) with
   `G = mex` of child values;
3. lists maximal safe sets (safe sets with no safe one-point extension);
4. checks (b): parity set of maximal sizes has size 1;
5. checks (c) for **all** `S`: via a superset zeta transform it counts even and
   odd maximal supersets of every `S`; (c) holds at `S` iff one count is zero;
6. checks the localized corollary for all `S`: superset count of positions with
   Grundy outside `{0,1}`, compared with (c) at `S`;
7. if (b) holds, compares `G(S)` with `(p − |S|) mod 2` for all `S`;
8. computes misère outcomes by the independent recursion
   `W(S) = True` if no moves, else `any(not W(child))`, and compares
   `W(S)` with `((p − |S|) even)` when (b) holds.

Families (seed `20261125`, `random.Random`):

| family | boards | description | s values | instances |
|---|---|---|---|---|
| `exhaustive_n4` | 1024 | all `2^10` families of 2- and 3-subsets of a 4-set | 2, 3 | 2048 |
| `exhaustive_n5` | 1024 | all `2^10` families of 3-subsets of a 5-set | 2, 3 | 2048 |
| `random_n6n7` | 3000 | 1500 boards on n=6, 1500 on n=7; every 2-,3-,4-block kept independently with probability 1/2 | 2, 3, 4 | 9000 |
| **total** | **5048** | | | **13096** |

Commands (run from the repository root; all exited 0):

```text
python research/experiments/parity-characterization-20261125/independent/verify_boards.py
python research/experiments/parity-characterization-20261125/independent/verify_pg2q5.py
python research/experiments/parity-characterization-20261125/independent/examples.py
```

Outputs: `independent/out/verification_boards.json`,
`independent/out/pg2q5_verification.json`, `independent/out/examples.json`.

### Results

Counts are per `(board, s)` instance.

| family | instances | uniform (b) | mixed | only-{0,1} (a) | uniform, non-constant maximal sizes | (a)⇔(b) violations | Grundy formula violations | misère formula violations | localized failures | (a)⇔(c) violations |
|---|---|---|---|---|---|---|---|---|---|---|
| exhaustive n=4 | 2048 | 1408 | 640 | 1408 | 0 | 0 | 0 | 0 | 0 | 0 |
| exhaustive n=5 | 2048 | 1288 | 760 | 1288 | 15 | 0 | 0 | 0 | 0 | 0 |
| random n=6,7 | 9000 | 4422 | 4578 | 4422 | 1 | 0 | 0 | 0 | 0 | 0 |
| **total** | **13096** | **7118** | **5978** | **7118** | **16** | **0** | **0** | **0** | **0** | **0** |

Per-`s` breakdown:

| family | s | instances | uniform | mixed |
|---|---|---|---|---|
| exhaustive n=4 | 2 | 1024 | 384 | 640 |
| exhaustive n=4 | 3 | 1024 | 1024 | 0 |
| exhaustive n=5 | 2 | 1024 | 264 | 760 |
| exhaustive n=5 | 3 | 1024 | 1024 | 0 |
| random n=6,7 | 2 | 3000 | 1115 | 1885 |
| random n=6,7 | 3 | 3000 | 307 | 2693 |
| random n=6,7 | 4 | 3000 | 3000 | 0 |

Key observations:

* `(a) ⇔ (b)` held in every instance: the count of only-`{0,1}` instances
  equals the count of parity-uniform instances exactly (7118), and the mixed
  count equals the not-only-`{0,1}` count exactly (5978). No instance had
  Grundy `2` while parities were uniform, nor vice versa.
* `(c)` held in exactly the same 7118 instances, so `(a) ⇔ (c)` also had
  0 violations (and `(b) ⇒ (c)` is immediate by the lemma above).
* The Grundy formula `G(S) = (p − |S|) mod 2` and the misère formula were
  checked at **every position** of every uniform instance: 0 violations.
* The localized corollary (subgame values in `{0,1}` ⇔ maximal extensions of
  `S` parity-uniform) was checked at every position of all 13,096 instances:
  0 failures.
* 16 uniform instances have **non-constant** maximal sizes, so the check
  exercises the genuinely parity-graded (not size-graded) case, e.g.:
  * n=5, s=2, blocks `{0,1,2}, {0,1,3}, {0,1,4}`: maximal sets
    `{0,1}` (size 2), `{0,2,3,4}`, `{1,2,3,4}` (size 4); p = 0; 25 positions;
    Grundy distribution `{0:13, 1:12}`; formula holds everywhere.
  * n=6, s=3, random board 381: maximal sizes `{3,5}` (same parity).

### Concrete mixed example

n=4, s=2, blocks `{0,1,2}, {0,1,3}` (a smallest mixed case in the exhaustive
n=4 family):

* maximal safe sets: `{0,1}` (size 2), `{0,2,3}`, `{1,2,3}` (size 3) — mixed
  parity;
* Grundy distribution over the 13 positions: `{0:5, 1:6, 2:2}`;
* `G({0}) = G({1}) = 2`.

So (a) fails exactly when (b) fails here, consistent with the theorem.

### Coverage caveat (honest limitation of the requested families)

A block with `|B| ≤ s` can never bind, because `|S ∩ B| ≤ |B| ≤ s` always.
Therefore in the requested exhaustive families:

* n=4, s=3 and n=5, s=3 have **no active blocks at all** (all block sizes
  ≤ 3): these 1024 + 1024 = 2048 instances are the unconstrained game, whose
  Grundy values are necessarily `(n − |S|) mod 2`;
* for s=2 the 2-blocks are inactive, so the n=4 exhaustive s=2 family contains
  only `2^4 = 16` distinct games (the 4 three-blocks), each repeated `2^6 = 64`
  times for the irrelevant 2-blocks; 64 of its 1024 instances have no 3-block
  at all (hence are unconstrained), and 1 of the 1024 n=5 s=2 cases has no
  block;
* the random family's s=4 cases (3000) are likewise unconstrained.

Exact count of instances with at least one active block: **7983** of the
13,096. Of the remaining 5113, 5048 come from the three all-inactive families
(n=4 s=3, n=5 s=3, random s=4) and 65 from the empty-3-block subfamilies of
the exhaustive s=2 families (64 with n=4, 1 with n=5). The counts above are
still valid for the exact families the task specified; this note only records
how much of the coverage is non-trivial.

**Task 2 verdict: PASS** (0 violations in 13,096 instances, including 16
parity-uniform non-constant-size cases).

---

## Task 3 — PG(2,5) cap game (s = 2)

Input: `research/experiments/projective-blocking-kyouen-20261125/output/board_pg2q5.txt`
(header `31 31`, then 31 lines `6 p0 … p5`).

### Board verification: it is PG(2,5)

`independent/verify_pg2q5.py` checks the incidence structure directly:

* 31 points, 31 distinct lines, every line has 6 distinct points;
* every point lies on exactly 6 lines (point degrees `{6}`);
* all `C(31,2) = 465` pairs of points are covered, each by **exactly one**
  line (465 pairs, multiplicity `{1}`);
* all `C(31,2) = 465` pairs of lines meet in **exactly one** point
  (intersection multiplicities `{1}`).

Thus the board is a projective plane of order 5, i.e. a `2-(31,6,1)` design.
Every projective plane of prime order is Desarguesian, and the projective
plane of order 5 is unique up to isomorphism, so the board is PG(2,5). As a
cross-check the standard PG(2,5) model over `F_5` was built explicitly
(normalised non-zero vectors of `F_5^3` for points, non-zero covectors for
lines): it also has 31 points, 31 lines, all of size 6.

### Cap enumeration (two independent methods)

A cap is a set `S` with `|S ∩ L| ≤ 2` for every line `L`.

* **DFS** adding points in increasing order, recording each cap once:
  41,572 caps.
* **Brute force** over all `k`-subsets of points for `k = 0..6`:
  `{0:1, 1:31, 2:465, 3:3875, 4:15500, 5:18600, 6:3100}`, total 41,572.
* **Downward closure of the maximal caps**: every cap extends to a maximal cap
  (finitely many positions), every maximal cap has size 6, and a set is a cap
  iff it is contained in a cap; the union of all subsets of the 3100 maximal
  caps is a set of exactly 41,572 masks and equals the DFS cap set.

The three descriptions agree exactly, and the two size distributions coincide.
No 7-cap exists because every 7-cap would contain a safe 6-subset, and every
one of the 3100 6-caps is maximal (checked: no 6-cap has a safe one-point
extension).

### Results versus the claims

| quantity | claimed | independently observed | match |
|---|---|---|---|
| number of caps | 41,572 | 41,572 | yes |
| size distribution | `{0:1, 1:31, 2:465, 3:3875, 4:15500, 5:18600, 6:3100}` | identical | yes |
| maximal caps | `{6: 3100}` | `{6: 3100}` (all 3100 six-caps are maximal) | yes |
| Grundy distribution | `{0:19066, 1:22506}` | identical | yes |
| `G(empty)` | 0 | 0 | yes |
| `misere(empty)` | 1 (first player wins) | 1 | yes |

The complete Grundy distribution was obtained by direct DP over all caps
(`G(S) = mex{G(S ∪ {x}) : x ∉ S, S ∪ {x} safe}`, computed in decreasing size
order), not by assuming the theorem. Since all maximal caps have size 6
(common parity `p = 6`, even), the theorem predicts
`G(S) = (6 − |S|) mod 2 = |S| mod 2`, and indeed
`G = 0` on the 19066 even-sized caps and `G = 1` on the 22506 odd-sized caps;
the parity check against the formula had **0 violations** over all 41,572
caps, and the misère formula `misere_win(S)` ⇔ `(6 − |S|)` is even also had
**0 violations**. Normal-play outcome of the empty position is a loss
(`G = 0`); misère outcome is a win, as expected for a game in which every
maximal play has exactly 6 moves.

**Task 3 verdict: PASS** — the board is PG(2,5), and every claimed cap count,
size distribution, maximal-cap datum and Grundy/misère value is reproduced
exactly.

---

## Discrepancies

No mathematical or numerical discrepancy was found.

1. **Wording, YAML `evidence:` field of K1298** — "任意の完全プレイの長さが
   `p − |S|` に固定され": with parity-uniform but non-constant maximal sizes
   (e.g. sizes 4 and 6), the length is not fixed, only its parity is. The
   Markdown body has the correct statement. Suggested fix: replace "長さが
   `p − |S|` に固定" by "長さが `p − |S|` と同じパリティ".
2. **Wording, localized corollary** — "(部分ゲームに定理を適用)": the subgame is a
   residual-capacity game (per-block capacities `s − |S ∩ B|`), not literally a
   uniform-`s` hypergraph game. The statement is true and the same induction
   proves it; the justification could say "同じ帰納を部分ゲームに適用".
3. **Not a discrepancy, for information**: the item's verification artifact
   (`parity-characterization-20261125/output/verification.json`, 8,360 boards)
   was not re-run or audited here; the independent check used its own,
   different families as requested by the task (5,048 boards / 13,096
   instances). The conclusions agree.

Nothing else in the theorem statement, proof, or the PG(2,5) claims required
correction.

---

## Artifacts

All inside `research/experiments/parity-characterization-20261125/independent/`:

* `REPORT.md` — this report;
* `verify_boards.py` — Task 2 verifier (exhaustive + random families);
* `verify_pg2q5.py` — Task 3 verifier (board design, caps, Grundy, misère);
* `examples.py` — extracts the concrete examples quoted above;
* `out/verification_boards.json` — full Task 2 results and zero-violation summary;
* `out/pg2q5_verification.json` — full Task 3 results;
* `out/examples.json` — the two concrete examples.

Reproduce with:

```text
python research/experiments/parity-characterization-20261125/independent/verify_boards.py
python research/experiments/parity-characterization-20261125/independent/verify_pg2q5.py
python research/experiments/parity-characterization-20261125/independent/examples.py
```
