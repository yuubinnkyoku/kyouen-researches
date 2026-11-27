# Independent verification of K1356 — complete Grundy spectrum of the PG(2,3) s=3 game

**Verdict: the claim is confirmed exactly. No numerical discrepancy.**
All 132 automated checks pass (`verification.json`, `failures: []`).

Two *wording* caveats are recorded in §6. Neither changes any claimed number.

- Board (read-only): `research/experiments/projective-blocking-kyouen-20261125/output/board_pg2q3.txt`
- Claim: K1356 as transcribed in the task, cross-checked at the end against the claim
  artifact `research/experiments/pg2q3-s3-20261128/output/pg2q3_s3_spectrum.json` (all compared
  fields match).
- Work is confined to `research/experiments/pg2q3-s3-20261128/independent/`; no file outside
  that directory was modified, and nothing was committed.
- Game interpreted exactly as stated: positions are safe sets `S` (`|S ∩ L| ≤ 3` for every
  line `L`); a move adds one point while preserving safety; normal play; therefore
  `G(S) = mex{ G(S ∪ {p}) : p ∉ S, S ∪ {p} safe }`, terminal positions have `G = 0`.
- Implementation: Python 3.12.13, standard library only. The original experiment's code is
  **not** imported. The board is re-read and the Grundy function is recomputed from scratch.

---

## 1. Board verification (is it PG(2,3)?)

Parsed header `13 13`; 13 line rows, each `4 p1 p2 p3 p4`, 0-based.

| Property | Result |
|---|---|
| 13 points, 13 lines | yes |
| every line has 4 distinct in-range points | yes |
| the 13 lines are pairwise distinct | yes |
| every point lies on exactly 4 lines | yes (all 13 points) |
| every pair of points lies on exactly one line | yes, 78/78 pairs |
| every pair of lines meets in exactly one point | yes (all 78 pairs, intersection size 1) |

So the board is a projective plane of order 3. Since the projective plane of order 3 is
unique up to isomorphism (`PG(2,F_3)`), this already identifies it with PG(2,3). In addition
an **explicit coordinate isomorphism** was verified:

```
point 4..12  ->  (x, y, 1)  with x = (p-4) mod 3, y = (p-4)//3
point 0      ->  (1, 0, 0)
point 1      ->  (0, 1, 0)
point 2      ->  (1, 1, 0)
point 3      ->  (1, 2, 0)
```

The 13 board lines are **exactly** the zero sets of the 13 non-zero linear forms over `F_3`
(all 13 standard projective lines of 4 points arise, both directions checked).

---

## 2. Exhaustive census and Grundy spectrum

All `2^13 = 8192` subsets were tested against all 13 lines; the Grundy value of every safe
position was computed by a full bottom-up DP over decreasing set size.

| k | safe sets | G=0 | G=1 | claim count | claim G | match |
|---:|---:|---:|---:|---:|---:|:---:|
| 0 | 1 | 0 | 1 | 1 | 1 | yes |
| 1 | 13 | 13 | 0 | 13 | 0 | yes |
| 2 | 78 | 0 | 78 | 78 | 1 | yes |
| 3 | 286 | 286 | 0 | 286 | 0 | yes |
| 4 | 702 | 0 | 702 | 702 | 1 | yes |
| 5 | 1,170 | 1,170 | 0 | 1,170 | 0 | yes |
| 6 | 1,248 | 0 | 1,248 | 1,248 | 1 | yes |
| 7 | 702 | 702 | 0 | 702 | 0 | yes |
| 8 | 117 | 0 | 117 | 117 | 1 | yes |
| 9 | 13 | 13 | 0 | 13 | 0 | yes |
| 10–13 | 0 | – | – | – | – | yes |

- **Total 4,330 safe positions; G=0: 2,184; G=1: 2,146.** Exactly as claimed.
- **No safe 10-set exists**, so the maximum safe size is 9.
- Only Grundy values 0 and 1 occur; every layer is Grundy-uniform, with
  `G(k) = (k+1) mod 2` for k = 0..9.

Independent cross-checks of the census and of the DP:

- a second enumeration (DFS from the empty set, adding points in any order) reproduces
  exactly the same 4,330 safe sets;
- a top-down recursive Grundy computation (re-testing safety from the line definition)
  reproduces all 4,330 bottom-up values;
- the counts also agree with elementary inclusion–exclusion for k = 4..7
  (`13`, `117`, `468`, `1014` unsafe sets), and with the structural characterisations below;
- the incidence identity `Σ_{|S|=k} #moves(S) = (k+1)·N_{k+1}` holds for every k = 0..8.

Structural characterisations confirmed by the census:

- the 13 safe 9-sets are exactly the complements of the 13 lines;
- the 117 safe 8-sets are exactly `(complement of a line) minus one point`;
- the 13 unsafe 4-sets are exactly the 13 lines.

---

## 3. Mex chain and per-layer move statistics

`option-counts` is `{number of legal moves : number of positions}`; `option G` is the set of
Grundy values reachable in one move.

| k | positions | option-counts | option G | G(k) |
|---:|---:|---|---|---:|
| 0 | 1 | {13: 1} | {0} | 1 |
| 1 | 13 | {12: 13} | {1} | 0 |
| 2 | 78 | {11: 78} | {0} | 1 |
| 3 | 286 | {9: 52, 10: 234} | {1} | 0 |
| 4 | 702 | {8: 468, 9: 234} | {0} | 1 |
| 5 | 1,170 | {6: 702, 7: 468} | {1} | 0 |
| 6 | 1,248 | {3: 234, 4: 936, 6: 78} | {0} | 1 |
| 7 | 702 | {0: 234, 2: 468} | ∅ (234), {1} (468) | 0 |
| 8 | 117 | {1: 117} | {0} | 1 |
| 9 | 13 | {0: 13} | ∅ | 0 |

The **k = 0,1,2 mex chain** is verified explicitly: `mex{0}=1`, `mex{1}=0`, `mex{0}=1`;
the same mechanism continues at k = 3 (`mex{1}=0`) and at k = 4..6, 8. At **k = 7** the layer
is mixed: 234 positions have no move (`mex ∅ = 0`) and 468 have exactly two moves, both to
G=1 positions (`mex{1} = 0`). Hence all 702 positions of size 7 have G=0, as claimed.

The incidence totals `Σ moves over k-sets = (k+1)·N_{k+1}` are, for k = 0..8:
13, 156, 858, 2,808, 5,850, 7,488, 4,914, 936, 117 — all matched.

---

## 4. Three-point layer ("3-caps")

- `C(13,3) = 286` three-point sets; **all 286 are safe**.
- **52** are collinear (each lies on exactly one line); **234** are non-collinear (triangles).
- **All 286 have G = 0**, so both orbits have G=0 as claimed.

The claim's term "3-cap" here means "3-point safe set" (every triple, since a line holds 4
points). See the terminology caveat in §6.

---

## 5. Cones, T/U tables and the double-count identity

Representatives: `{0,1,4}` (non-collinear triangle) and `{0,1,2}` (collinear).

| cone | positions | claimed | result |
|---|---:|---:|:---:|
| triangle `{0,1,4}` | 260 | 260 | match |
| collinear `{0,1,2}` | 214 | 214 | match |

- `G({0,1,4}) = G({0,1,2}) = 0`.
- **Orbit uniformity is verified exhaustively**, not merely by group transitivity: all 234
  triangles have the *identical* size/G cone histogram (the T table), and all 52 collinear
  triples have the identical histogram (the U table).
- A second (DFS) cone enumeration and a **cone-local DP** reproduce exactly the filter
  census and the global Grundy values on all 260 + 214 positions.

### T/U tables (computed; identical to the claim's artifact)

| m | T_m(0) | T_m(1) | T_m | U_m(0) | U_m(1) | U_m |
|---:|---:|---:|---:|---:|---:|---:|
| 3 | 1 | 0 | 1 | 1 | 0 | 1 |
| 4 | 0 | 10 | 10 | 0 | 9 | 9 |
| 5 | 42 | 0 | 42 | 36 | 0 | 36 |
| 6 | 0 | 90 | 90 | 0 | 75 | 75 |
| 7 | 89 | 0 | 89 | 72 | 0 | 72 |
| 8 | 0 | 24 | 24 | 0 | 18 | 18 |
| 9 | 4 | 0 | 4 | 3 | 0 | 3 |
| **Σ** | | | **260** | | | **214** |

### Identity `234·T_m(g) + 52·U_m(g) = C(m,3)·N_m(g)`

Only the non-zero rows are shown; every row (including the zero rows) was checked.

| m | g | 234·T_m(g) | 52·U_m(g) | LHS | C(m,3) | N_m(g) | RHS |
|---:|---:|---:|---:|---:|---:|---:|---:|
| 3 | 0 | 234 | 52 | 286 | 1 | 286 | 286 |
| 4 | 1 | 2,340 | 468 | 2,808 | 4 | 702 | 2,808 |
| 5 | 0 | 9,828 | 1,872 | 11,700 | 10 | 1,170 | 11,700 |
| 6 | 1 | 21,060 | 3,900 | 24,960 | 20 | 1,248 | 24,960 |
| 7 | 0 | 20,826 | 3,744 | 24,570 | 35 | 702 | 24,570 |
| 8 | 1 | 5,616 | 936 | 6,552 | 56 | 117 | 6,552 |
| 9 | 0 | 936 | 156 | 1,092 | 84 | 13 | 1,092 |

Total: `234·260 + 52·214 = 71,968 = Σ_m C(m,3)·N_m`. All identities hold.

---

## 6. Terminal positions — important structural note (not a numerical discrepancy)

The full DP shows that positions with no legal move occur at **two sizes**:

| size | terminal positions | characterisation |
|---:|---:|---|
| 7 | 234 | `T ∪ Q(T)`: a triangle `T` plus the 4 points `Q(T)` off its 3 side lines |
| 9 | 13 | complements of the 13 lines |
| ≤6, 8 | 0 | every such safe position has a move |

Total **247 terminal positions**. Each of the 234 terminal 7-sets has exactly **6 three-secant
lines**, whose fourth points are precisely the 6 points outside the set. Equivalently, the
complement of a terminal 7-set is the 6-point **side set of a triangle**, i.e. a **Pasch
configuration** (6 points, 4 three-secant lines, each point on 2 of them); equivalently the 6
pairwise intersections of 4 lines in general position (234 such 4-line sets). There is a
bijection between the 234 triangles and the 234 terminal 7-sets. Example:
`S = {0,1,2,4,5,7,8}` is terminal, with 3-secant lines
`{0,1,2,3}, {0,4,5,6}, {0,7,8,9}, {1,4,7,10}, {1,5,8,11}, {2,4,8,12}` and outside points
`{3,6,9,10,11,12}`. The 468 non-terminal 7-sets each have exactly 2 moves (to 8-sets); the
117 safe 8-sets each have exactly 1 move (to a 9-set).

**Consequences:**

1. "Max safe size 9" is correct **as a maximum**, but it does **not** mean that every maximal
   safe position has size 9. The game tree also has terminal positions after 7 moves, so game
   length is not fixed at 9.
2. The claim's Grundy numbers are **not** affected: terminal 7-sets have `G = mex ∅ = 0`, and
   the other 468 moves from size 7 all lead to G=1 positions, so every 7-set has G=0. The
   claim's cone DP correctly handles these terminal positions (verified: cone-local DP equals
   the global DP on every cone position, including the terminal 7-sets).
3. What is **false** (and is not asserted in the claim as given) is any reasoning of the form
   "every safe position of size ≤ 8 extends, hence the layers alternate". The alternation is
   a fact here, but its mechanism at k=7 includes the 234 terminal positions.

### Terminology caveat

The claim calls the 3-point seeds "3-caps". In the standard finite-geometry sense a *cap* has
no 3 collinear points, which would exclude the 52 collinear triples. Here "3-cap" evidently
means a 3-point safe set (all 286 triples, under the `≤3`-per-line condition). The orbit split
234 + 52 and the cone/T-U computation are correct; only the word "cap" is non-standard.

---

## 7. What is proved, and what is not

**Proved (by exhaustive computation on this board):**

- The board is PG(2,3): axioms verified; explicit `F_3^3` coordinate isomorphism verified.
- The complete safe-set census: 4,330 positions with the per-size distribution above, no
  safe 10-set.
- Every claimed Grundy value: computed by a full DP over all safe positions and cross-checked
  by an independent top-down recursion; the per-size spectrum and the G0/G1 totals match.
- The two 3-point orbits (234 triangles, 52 collinear), all G=0.
- The two cone sizes (260 / 214), the exact T/U tables, their uniformity over all 286
  triples, the cone-local DPs, and the double-count identity for every `(m,g)`.
- The mex chain at k=0,1,2, the mixed k=7 layer, and the totals.

**Not proved here:**

- No general statement for other boards/parameters (`PG(2,q)`, other `s`) is addressed; this
  is a finite verification for the given 13-point board.
- No proof-assistant formalisation and no claim that the "cone + double counting" method is a
  theorem in general; it is validated here, on this board, including the orbit-uniformity step.
- The general combinatorial/group-theoretic reasoning behind the orbit counts was not needed
  for the verdict: all 286 triples were checked individually.

**Discrepancy:** none in the numerical claim. The only corrections are the two wording
caveats: (a) terminal positions also occur at size 7 (247 terminal positions total, 234 at
size 7), and (b) the claim's "3-cap" includes the 52 collinear triples, which standard cap
terminology would not.

---

## 8. Reproduction

```sh
python research/experiments/pg2q3-s3-20261128/independent/verify_pg2q3_s3.py
```

- Python 3.12.13, standard library only; runtime a few seconds.
- Outputs `independent/verification.json` (all 132 checks, `verdict: PASS`,
  `failures: []`) and prints the full log (`independent/verify_stdout.txt` is the captured
  run).
- Files in this directory:
  - `verify_pg2q3_s3.py` — the independent verifier;
  - `verification.json` — machine-readable results (counts, Grundy distributions, T/U,
    identity rows, terminal structure, all checks);
  - `verify_stdout.txt` — captured stdout of the passing run;
  - `REPORT.md` — this report.
