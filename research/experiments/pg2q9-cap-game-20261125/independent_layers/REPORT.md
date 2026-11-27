# Independent verification — K1351, PG(2,9) cap Grundy layers

**Verdict: PASS. Every numerical claim of K1351 is confirmed. No numerical
discrepancy was found.**

Verifier: independent subagent. Scope: only this directory
`research/experiments/pg2q9-cap-game-20261125/independent_layers/` was created
or modified; no file outside it was written, and nothing was committed.
Tools: Python 3.12.13, standard library only. The parent's board / census /
conic-layer files and the sixcap experiment's enumeration outputs were read
read-only.

All programs in this directory were written from scratch for this verification:

| file | purpose |
|---|---|
| `common.py` | GF(9), board loading, cap/upset/Grundy-DP primitives |
| `conics.py` | independent enumeration of all conics from quadratic forms |
| `step1_board_census.py` | board axioms, explicit isomorphism, census/arithmetic, independent cap census |
| `step2_grundy_samples.py` | full upset DP on >= 10 caps in every layer |
| `step3_global_checks.py` | 200-sample structural checks per layer |
| `step4_conic_uniqueness.py` | 5-cap conic uniqueness and conic k-subset addable sets |
| `step5_conic6.py` | conic 6-caps G=0; no maximal 7-arc contains a conic 6-subset |
| `make_summary.py` | aggregates the machine-readable results |

Machine-readable outputs are in `out/`:

* `out/step1_board_census.json`
* `out/step2_grundy_samples.json`
* `out/step3_global_checks.json`
* `out/step4_conic_uniqueness.json`
* `out/step5_conic6.json`
* `out/conics_summary.json`
* `out/verification_summary.json`

Reproduce at the end of this report.

---

## 0. The board is PG(2,9)

`python step1_board_census.py` (output `out/step1_board_census.json`).

* 91 points, 91 lines, all lines of size 10, distinct lines = 91;
* every point has degree 10;
* every one of the C(91,2) = 4,095 pairs of points lies on exactly one line;
* every pair of lines meets in exactly one point (4,095 intersections of size 1).

So the board is a projective plane of order 9. To identify it as the
Desarguesian plane, the board labels are mapped to homogeneous coordinates over
GF(9) = GF(3)[i]/(i^2+1) by the standard coordinate labelling

```
label 0        -> [0 : 0 : 1]
label 1+j      -> [0 : 1 : j]          (j = 0..8)
label 10+9p+j  -> [1 : p : j]          (p,j = 0..8)
```

(91 distinct canonical vectors). The standard PG(2,9) is independently built
from GF(9), with the 91 lines obtained as kernels of the 91 canonical non-zero
linear forms. Then:

```
board_lines_equal_standard_lines : True   (91 / 91)
line_map_bijective               : True
isomorphism                      : True
```

Every board line is exactly a standard line under this bijection, and the line
map is a bijection. This is an explicit incidence isomorphism to PG(2,9); the
plane axioms above are then automatic.

---

## 1. Task 1 — census and conic-layer numbers

### 1.1 Census table

Parsed from `output/census_pg2q9.txt` (SIZE lines) and cross-checked against
`output/analysis.json`:

| k | caps | maximal | claimed G distribution | sum | status |
|---:|---:|---:|---|---:|---|
| 5 | 14,859,936 | 0 | G=1: 14,859,936 | 14,859,936 | PASS |
| 6 | 52,009,776 | 707,616 | G=0: 37,857,456, G=2: 14,152,320 | 52,009,776 | PASS |
| 7 | 51,554,880 | 2,021,760 | G=0: 2,021,760, G=1: 49,533,120 | 51,554,880 | PASS |
| 8 | 7,960,680 | 5,307,120 | G=0: 7,960,680 | 7,960,680 | PASS |
| 9 | 589,680 | 0 | G=1: 589,680 | 589,680 | PASS |
| 10 | 58,968 | 58,968 | G=0: 58,968 | 58,968 | PASS |

Total caps 128,917,712; total maximal caps 8,095,464. `analysis.json` agrees
with the census exactly, including these totals.

### 1.2 Conic layer — exhaustive enumeration

`conics.py` enumerates all canonical homogeneous quadratic forms over GF(9)
(first non-zero coefficient equal to 1): 66,430 forms = (9^6-1)/8. Evaluating
each form on the 91 points gives:

```
canonical forms                 66,430
non-degenerate forms            58,968
degenerate forms                 7,462
distinct conic point sets       58,968
all conics are 10-caps          True
all conics are maximal          True   (no point outside is addable)
```

This equals 9^5 - 9^2 = 58,968. The parent's advertised conic
`{0,1,10,20,31,45,51,62,75,88}` is found in the enumeration. Conic subsets have
the expected sizes: `C(10,k) * 58,968` for every k.

The count identities used by K1351 then hold exactly:

| identity | value | census side |
|---|---:|---|
| 58,968 * C(10,5) | 14,859,936 | #5-caps |
| 58,968 * C(10,8) | 2,653,560 | conic 8-caps |
| 58,968 * C(10,9) | 589,680 | #9-caps |
| 58,968 * C(10,10) | 58,968 | #10-caps |
| 5,307,120 + 2,653,560 | 7,960,680 | #8-caps |

Because five points of PG(2,9) with no three collinear lie on a **unique** conic
(verified on 200 random 5-caps: `step4`, 200/200; the 5x6 linear system for the
quadratic form has a 1-dimensional kernel), these are counts of *distinct*
caps, so the equalities imply the structural statements:

* every 5-cap is a conic 5-subset (the count equals the total);
* every 9-cap is a conic 9-subset (the count equals the total);
* every 10-cap is a conic (the count equals the total);
* every 8-cap is either a maximal 8-cap (5,307,120) or a conic 8-subset
  (2,653,560).

### 1.3 Independent cap census (pure Python)

`step1_board_census.py --max-size 7` performs a DFS over caps in increasing
point order, with an incrementally maintained blocked/secant mask. It visits
every cap of size <= 7 exactly once and sums the number of addable points at
each size, from which the next size count follows by
`#(k+1)-caps = (sum of addable points over k-caps)/(k+1)`.

| k | independent count | census | status |
|---:|---:|---:|---|
| 0 | 1 | 1 | PASS |
| 1 | 91 | 91 | PASS |
| 2 | 4,095 | 4,095 | PASS |
| 3 | 110,565 | 110,565 | PASS |
| 4 | 1,769,040 | 1,769,040 | PASS |
| 5 | 14,859,936 | 14,859,936 | PASS |
| 6 | 52,009,776 | 52,009,776 | PASS |
| 7 | 51,554,880 | 51,554,880 | PASS |
| 8 | 7,960,680 (derived from ext[7] = 8*#8) | 7,960,680 | PASS |

The independent Python enumeration therefore reproduces the census through
size 8 (including the 6-cap and 7-cap counts). The remaining count 9 and 10 are
independently pinned by the conic enumeration
(589,680 = 10 * 58,968 and 58,968). The *maximal* counts 707,616 / 2,021,760 /
5,307,120 / 58,968 are taken from the census; the terminal-cap counts for 7, 8,
10 are also confirmed by the sampled DP (Sections 2-3).

### 1.4 Six-cap enumeration file

`research/experiments/pg2q9-sixcap-20261126/results.txt` was read and checked:

```
n          = 14152320 = 7 * 2021760
distinct   = 14152320
duplicates = 0
census reproduced: total caps 128917712, max7 2021760
```

All three key lines are present. This is the K1333 enumeration showing that the
6-subsets of the 2,021,760 maximal 7-caps are all distinct.

**Task 1 verdict: PASS.** Board is PG(2,9); census and conic-layer numbers
agree; independent Python counts reproduce sizes 0-7 and derive size 8; conic
counts are independently enumerated.

---

## 2. Task 2 — full Grundy DP on samples in every layer

Method: for a sampled cap `S`, the **whole upset** `{caps T : S subset T}` is
enumerated from the board incidence (no structural shortcut), and the Grundy
values are computed bottom-up by decreasing size, terminal positions = 0. The
maximal elements of the upset are exactly the maximal caps containing `S`;
their sizes give the maximal-extension profile. The mex of the immediate
children is recomputed and compared with the DP value for every sample.

`python step2_grundy_samples.py --per 12`; data in
`out/step2_grundy_samples.json`. All samples pass every stated check.

| category | n | G observed | maximal extension sizes (counts) | parity | claimed | verdict |
|---|---:|---|---|---|---|---|
| 5-caps | 14 | **1** | {7,8,10} x9, {6,8,10} x5 | mixed or even | G=1 | PASS |
| 6-caps, subset of a maximal 7-cap | 12 | **2** | {7,8} x12 | mixed | G=2 | PASS |
| 6-caps, no maximal-7 child | 13 | **0** | {8} x8, {8,10} x4, {6} x1 | even | G=0 | PASS |
| non-maximal 7-caps | 12 | **1** | {8} x11, {10} x1 | even | G=1, max ext in {8,10} | PASS |
| maximal 7-caps | 13 | **0** | {7} x13 | odd | terminal G=0 | PASS |
| conic 8-caps | 12 | **0** | {10} x12 | even | G=0, only 10 | PASS |
| maximal 8-caps | 13 | **0** | {8} x13 | even | terminal G=0 | PASS |
| conic 9-caps | 12 | **1** | {10} x12 | even | G=1, only 10 | PASS |
| conic 10-caps | 12 | **0** | {10} x12 | even | terminal G=0 | PASS |

Selected details:

* **5-caps.** 14 samples, upset 128-132 positions, exactly 21 children each.
  Nine have children `13 x G=0 + 8 x G=2` and maximal extensions `{7,8,10}`
  (mixed parity); five have 21 children all `G=0` and maximal extensions
  `{6,8,10}` (even). This exactly matches the two PGL(2,9) classes recorded in
  `output/conic_layer_parity.json` (`{0,1,10,20,31}` -> `{7,8,10}`;
  `{0,1,10,20,51}` -> `{6,8,10}`). In both cases `G=1`: a 0 child exists and
  there is no 1 child. Note that the mixed parity of the maximal extensions of
  the first class does **not** force `G=1` to fail: by K1298 the mixed parity
  only forces a Grundy value >= 2 somewhere in the upset, and here it appears
  at the 6-cap children.
* **6-caps with a maximal-7 child.** Each is `A - {p}` for a maximal 7-arc `A`.
  Upset always 11 positions, 7 children: one maximal 7-cap (`G=0`) and six
  non-maximal 7-caps (`G=1`); mex = 2. Maximal extensions `{7,8}` (mixed
  parity).
* **6-caps without a maximal-7 child.** Upset 1-22 positions; all children are
  non-maximal 7-caps (`G=1`), or the cap is a terminal maximal 6-cap (`G=0`);
  mex = 0. Maximal extensions are even (`{6}`, `{8}`, `{8,10}`).
* **non-maximal 7-caps.** One has 3 children (a conic 7-cap, maximal extension
  `10`), eleven have 1 child (a maximal or conic 8-cap). All children have
  `G=0`, so `G=1`; maximal extensions `{8}` or `{10}`, always even.
* **maximal 7-caps.** upset = 1 (terminal), G=0, maximal extension `{7}`.
* **conic 8-caps.** upset = 4, two 9-children with `G=1`, mex=0; the unique
  maximal extension is the conic 10-cap.
* **conic 9-caps.** upset = 2, one 10-child with `G=0`, G=1.
* **conic 10-caps / maximal 8-caps.** terminal, upset = 1, G=0.

All 88 primary samples (the seven requested categories) and the 25 additional
6-cap samples satisfy `grundy == mex(children)`, all maximal elements of every
upset have Grundy 0, and all claimed maximal-extension size sets / parities are
exact.

Cross-checks against caps named in the parent reports:

* the K1298/K1333 witness `{0,1,10,20,32,39}` independently gives `G=2`
  (upset 11, children `[0,1,1,1,1,1,1]`, maximal extensions `{7,8}`);
* the parent-listed complete 6-arc `{4,9,20,32,69,84}`, complete 7-arc
  `{16,47,51,56,60,80,82}` and complete 8-arc
  `{32,39,42,47,56,59,84,87}` are all terminal with `G=0` and sizes
  `{6}`, `{7}`, `{8}` respectively;
* the parent-listed conic `{0,1,10,20,31,45,51,62,75,88}` is found in the
  exhaustive conic enumeration.

---

## 3. Task 3 — local-parity claims

### 3.1 The four explicit claims

All four are confirmed both on the samples above and by the larger-sample
structural checks of `step3_global_checks.py --n 200`
(`out/step3_global_checks.json`, failures = []):

| claim | sample evidence | verdict |
|---|---|---|
| non-maximal 7-caps: every maximal extension has size in {8,10} | 100 non-maximal 7-caps (ext 1 or 3), full DP: maximal sizes always `{8}` or `{10}`, parity even | PASS |
| conic 8-caps extend only to 10 | 200 random conic 8-subsets: addable set = the 2 missing conic points; DP: maximal sizes `{10}` | PASS |
| conic 9-caps extend only to 10 | 200 random conic 9-subsets: addable set = the missing conic point; DP: maximal sizes `{10}` | PASS |
| maximal 7-caps are terminal | 100 random maximal 7-caps (random greedy) + 13 DP samples: 0 addable points, upset = 1 | PASS |

The 200-sample run additionally checked 200 random 5-caps (`G=1`, children
subset `{0,2}`, at least one 0 child), 200 random 8-caps (179 maximal terminal,
21 conic with addable pair and maximal extension 10; all `G=0`), and 200 random
6-caps (`G=2` exactly when a maximal-7 child exists: 55/200; all others `G=0`;
the only `(addable, has-max-7)` combinations seen were
`(0,no)`, `(4,no)`, `(6,no)`, `(7,yes)`, `(8,no)`).

### 3.2 Why these claims hold globally (proof)

**Conic pairing lemma.** Let `C` be a non-degenerate conic in PG(2,9) and
`p` a point not on `C`. The 10 lines through `p` meet `C` in one of two ways:

* `p` external: 2 tangent points + 4 secant pairs (2 + 4*2 = 10 points);
* `p` internal: 5 secant pairs (5*2 = 10 points).

Consequently every subset of `C` of size **>= 7** contains two points that are
collinear with `p`, so `p` is not addable. For a conic subset `S` with
`|S| >= 7`, the only addable points are therefore the missing points of `C`;
for 7-, 8- and 9-subsets these are exactly 3, 2 and 1 points. (At size 6 the
external case can avoid all pairs, and indeed conic 6-subset addable sets
sometimes contain outside points.)

This lemma was verified exhaustively for the full conics (all 58,968 are
maximal) and directly for 200 random subsets at each of k = 7, 8, 9
(`step4`: addable set = missing conic points, 200/200 at each k).

**Global chain.** Using the census counts and the structural identifications of
Section 1.2:

1. **k=10.** All 10-caps are conics (58,968 = 58,968) and every conic is
   maximal. Hence all 58,968 are terminal, `G=0`.
2. **k=9.** All 9-caps are conic 9-subsets (589,680 = 10 * 58,968). By the
   pairing lemma the only addable point is the missing conic point, so the only
   child is a conic 10-cap with `G=0`; mex = 1. Hence all 589,680 have `G=1`.
3. **k=8.** Every 8-cap is either a maximal 8-cap (5,307,120; terminal `G=0`)
   or a conic 8-subset (2,653,560). A conic 8-subset has exactly two addable
   points, both missing conic points, so its two children are 9-caps with
   `G=1`; mex = 0. Hence all 7,960,680 have `G=0`.
4. **k=7.** A maximal 7-cap is terminal, `G=0`. A non-maximal 7-cap has at
   least one 8-child; every 8-cap has `G=0`, so all children have `G=0` and
   mex = 1. Hence the 2,021,760 maximal 7-caps have `G=0` and the other
   49,533,120 have `G=1`.
   *Maximal extensions are in {8,10}:* let `T` be a maximal extension of a
   non-maximal 7-cap `S` and let `U` be an 8-child of `S`. If `U` is maximal
   then `T=U` has size 8. Otherwise `U` is a conic 8-subset and, by the pairing
   lemma, its only maximal extension is the conic 10-cap, so `T` has size 10.
5. **k=6.** Children of a 6-cap are 7-caps, whose Grundy values are only 0
   (maximal) and 1 (non-maximal). If a 6-cap has a maximal-7 child, it has one
   0 child and at least one 1 child, so mex = 2; if it has no maximal-7 child,
   all children are non-maximal 7-caps (`G=1`) and mex = 0 (or it is a terminal
   maximal 6-cap, `G=0`). See Section 4 for the exact count.
6. **k=5.** Every 5-cap is a conic 5-subset. Adding one of the five remaining
   conic points gives a conic 6-cap. A conic 6-cap has `G=0`: its children are
   7-caps containing it, and a maximal 7-child would make the 6-cap a conic
   6-subset of a maximal 7-arc. This does not occur — 0 of the 217 six-subsets
   of 31 maximal 7-arcs (including the known representative) lie on a conic,
   and all maximal 7-arcs form a single PGL(3,9) orbit (K1303/parent report,
   independently verified in that experiment). Equivalently, the two
   PGL(2,9) classes of conic 6-subsets both have `G=0` and maximal extensions
   `{8,10}` / `{10}` in `output/conic_layer_parity.json`. Hence all children of
   a conic 6-cap are non-maximal 7-caps with `G=1`, so mex = 0. Direct DP on
   100 random conic 6-subsets confirms `G=0`, no size-7 maximal extension and
   all children `G=1` (`step5_conic6.py`). Thus every 5-cap has at least one
   `G=0` child. Every 6-child is a 6-cap, hence has `G` in {0,2} by step 5, so
   there is no 1 child; mex = 1. Hence all 14,859,936 5-caps have `G=1`.

The k=10, 9, 8, 7 arguments are complete proofs from the census identities and
the conic enumeration. The k=6 argument is complete once one also uses the
full-enumeration fact that every 6-subset of a maximal 7-cap has exactly 7
addable points (K1333 / sixcap census, Section 4). The k=5 argument is complete
once one uses that no maximal 7-arc contains a conic 6-subset (verified for 217
six-subsets of 31 maximal 7-arcs, and by the single PGL(3,9) orbit of maximal
7-arcs this covers all; equivalently the two conic 6-classes are G=0 in
`conic_layer_parity.json`, and 100 random conic 6-subsets were checked directly
in `step5_conic6.py`).

**Task 3 verdict: PASS.**

---

## 4. Task 4 — the G=2 layer of 6-caps

### 4.1 Enumeration facts

`research/experiments/pg2q9-sixcap-20261126/results.txt` (K1333's enumeration):

```
n = 14152320 = 7 * 2021760
distinct = 14152320
duplicates = 0
=> every 6-cap is contained in at most one complete 7-arc
=> #6-caps with a complete 7-arc extension = 14152320 (27.2% of 52009776)
```

So there are exactly 14,152,320 distinct 6-subsets of maximal 7-caps, and no
6-cap lies in two of them.

The independent C census `research/experiments/pg2q9-sixcap-20261126/independent/census_out.txt`
(full enumeration of all 128,917,712 caps, run by the separate sixcap
verification) gives the complementary full counts:

```
k=6 ext histogram: 0:707616 4:1769040 6:14152320 7:14152320 8:21228480
6-cap joint (ext, has max-7 child):
  (0,0):707616 (4,0):1769040 (6,0):14152320 (7,1):14152320 (8,0):21228480
#6-caps with |addable|==1: 0
Grundy distribution g6: 0:37857456  1:0  2:14152320
```

In particular, every 6-cap with a maximal-7 child has **exactly 7 addable
points**: the removed point `p` (adding it gives the maximal 7-cap `A`) and six
points outside `A` (adding one of them gives a non-maximal 7-cap). No 6-cap has
exactly one addable point. Hence the child Grundy set is exactly `{0,1}` for
the 14,152,320 arc-subsets (mex 2), and exactly `{1}` (mex 0) for the
37,857,456 non-arc 6-caps; terminal maximal 6-caps are `G=0`.

This agrees with the direct DP samples: all 12 sampled `A-{p}` have one 0 child
and six 1 children (mex 2, maximal extensions `{7,8}`), all 13 sampled non-arc
6-caps have `G=0`, and in the 200 random 6-caps the equivalence
"`G=2` iff a maximal-7 child exists" held in all 200 cases.

### 4.2 Count

```
#6-caps with a maximal-7 child = 7 * #maximal-7-caps = 7 * 2,021,760
                              = 14,152,320        (results.txt, duplicates 0)
#6-caps G=2                    = 14,152,320
#6-caps G=0                    = 52,009,776 - 14,152,320 = 37,857,456
```

This is exactly K1351's k=6 row.

**Task 4 verdict: PASS.**

---

## 5. Task 5 — arithmetic

| k | G=0 | G=1 | G=2 | sum | census | status |
|---:|---:|---:|---:|---:|---:|---|
| 5 | 0 | 14,859,936 | 0 | 14,859,936 | 14,859,936 | PASS |
| 6 | 37,857,456 | 0 | 14,152,320 | 52,009,776 | 52,009,776 | PASS |
| 7 | 2,021,760 | 49,533,120 | 0 | 51,554,880 | 51,554,880 | PASS |
| 8 | 7,960,680 | 0 | 0 | 7,960,680 | 7,960,680 | PASS |
| 9 | 0 | 589,680 | 0 | 589,680 | 589,680 | PASS |
| 10 | 58,968 | 0 | 0 | 58,968 | 58,968 | PASS |

Additional identities checked:

* 14,152,320 = 7 * 2,021,760;
* 37,857,456 + 14,152,320 = 52,009,776;
* 2,021,760 + 49,533,120 = 51,554,880;
* 5,307,120 + 2,653,560 = 7,960,680;
* 589,680 = 10 * 58,968;
* 14,859,936 = 252 * 58,968;
* total caps 128,917,712 and total maximal 8,095,464 match `analysis.json`.

**Task 5 verdict: PASS.**

---

## 6. What is proved, what is sampled, what is cited

### Proved in this verification (exhaustive)

* The board is PG(2,9): plane axioms plus an explicit 91-point / 91-line
  incidence isomorphism to the standard GF(9) model.
* All 58,968 conics are 10-caps and are maximal; conic counts
  `C(10,k)*58,968`; every 5-cap lies on a unique conic.
* Independent cap counts for k = 0..7 (and k=8 derived from ext[7]) by a pure
  Python DFS: 1, 91, 4,095, 110,565, 1,769,040, 14,859,936, 52,009,776,
  51,554,880, 7,960,680.
* The conic pairing lemma and the local addable-set equalities for conic
  7-, 8-, 9-subsets (verified for 200 random subsets per k, and all full conics
  maximality is exhaustive).
* Given the census counts, the G classification follows by the induction in
  Section 3.2. This is a proof of all six layer claims, with two finite inputs
  taken from full enumeration / the parent's classification: (i) the ext=7
  property of the 14,152,320 six-subsets of maximal 7-caps (K1333 / sixcap
  census), and (ii) no maximal 7-arc contains a conic 6-subset (checked for 217
  six-subsets of 31 maximal 7-arcs and completed by the single PGL(3,9) orbit
  of maximal 7-arcs; the two conic 6-classes also have G=0 in
  `conic_layer_parity.json`).

### Sampled

* Full upset DP was run on 12-14 caps in each of the seven requested
  categories (plus 25 6-caps), and 200 additional random caps/structures per
  layer in `step3`. Every check passed.
* The samples confirm the claimed G values, maximal-extension size sets and
  parity profiles directly, including both 5-cap parity profiles
  `{6,8,10}` / `{7,8,10}`.

### Cited full enumerations (not recomputed in Python)

* The census counts k = 0..10 and the maximal counts are taken from
  `output/census_pg2q9.txt` / `output/analysis.json`. Sizes 0-7 (and 8 derived)
  were independently reproduced; sizes 9 and 10 are independently pinned by the
  conic enumeration.
* The ext histogram / joint histogram for 6-caps, in particular
  `(ext=7, has-max-7-child) = 14,152,320`, is from the independent C census of
  the sixcap experiment (`sixcap/.../independent/census_out.txt`), matching
  K1333. My samples corroborate it (no 6-cap with exactly one addable point was
  seen; all arc-subsets had 7 children).
* The 6-subset distinctness / count comes from
  `sixcap-20261126/results.txt` (K1333).

### Discrepancies

**No numerical discrepancy was found.** All counts, G values, maximal-extension
sizes, parity profiles and arithmetic sums match K1351 exactly.

Two minor expository remarks (not errors in the claimed values):

1. K1351's k=5 justification "children are 0/2, so mex{0,2}=1" needs the
   existence of at least one 0 child. The value is correct; the missing
   argument is supplied by the conic structure (every 5-cap has a conic 6-child
   with G=0, Section 3.2 step 6).
2. K1351's k=6 parenthetical "the 6-subsets of maximal 7-caps" is correct, but
   the count 14,152,320 also uses (a) distinctness of the six-subsets
   (`results.txt`) and (b) the fact that each such 6-cap has six further
   addable points (ext=7), which is in K1333's full enumeration. Without (b)
   the mex would not be 2. The values are unaffected.

---

## 7. Reproduce

Run from this directory
(`research/experiments/pg2q9-cap-game-20261125/independent_layers/`):

```text
python step1_board_census.py --max-size 7     # board + arithmetic + census (~10 min for size 7)
python conics.py                              # all conics, ~5 s
python step2_grundy_samples.py --per 12       # full DP samples, ~10 s
python step3_global_checks.py --n 200         # 200-sample structural checks, ~1 min
python step4_conic_uniqueness.py --n 200      # conic uniqueness / addable sets
python step5_conic6.py --n 100                # conic 6-caps G=0, max7/conic6 disjointness
python make_summary.py                        # aggregate JSON
```

All outputs are written under `out/` in this directory. No program writes
outside `independent_layers/`; the board, census, conic-layer, analysis and
sixcap files are opened read-only.
