# Independent verification — PG(2,9) six-cap claims (2026-11-26)

Verifier: independent subagent. Scope: only this directory
`research/experiments/pg2q9-sixcap-20261126/independent/` was created/modified;
nothing outside it was touched and nothing was committed. All programs below
were written from scratch for this verification (the parent's `sixsub.c` /
`sortcount.c` were additionally compiled and rerun as an audit, output only in
this directory).

Board: `research/experiments/pg2q9-cap-game-20261125/output/board_pg2q9.txt`
(read-only). Tools: gcc 15.2.0 (MSYS2 UCRT64), Python 3.12.13 (stdlib only).

## Verdict summary

| Task | Claim | Verdict |
|---|---|---|
| 1 | board is PG(2,9); 2,021,760 complete 7-arcs; 14,152,320 six-subsets all distinct | **PASS** |
| 2 | each six-subset `X = A - {p}` has exactly 7 addable points | **PASS** (the number 7) |
| 2 | the 7 addable points are the 7-arc `A` | **FAIL** — see discrepancy D1 |
| 3 | the children have Grundy values `{0,1}` and `G(X) = mex = 2` | **PASS** (full upset DP) |
| 3 | “six `X+q` with `q ∈ A - {p}`” | **FAIL** as a description — see discrepancy D2 (the mex conclusion is unaffected) |
| 4 | `#G=2 = 14,152,320`, `#G=0 = 37,857,456`, arithmetic | **PASS** |
| 5 | no 6-cap without a complete 7-arc extension has G=2 | **PASS** |

No numerical discrepancy was found anywhere. The two discrepancies are
descriptive errors in the justification of (B)/(C); the quantitative
conclusions (A), (C-mex), (D) are all correct.

---

## 0. Board is PG(2,9)

Command: `python verify_board.py` → `out_board.txt`

```
n_points 91, n_lines 91, line_sizes [10], distinct_lines 91, point_degrees [10]
all_pairs_on_a_line True, pair_line_unique True,
pairwise_line_intersection_sizes [1]
```

So the board is a projective plane of order 9. A projective plane of order 9
need not be Desarguesian (there are four planes of order 9), so plane axioms
alone are not enough. We construct an **explicit incidence isomorphism** to
`PG(2,9)`:

* build the standard `PG(2,9)` from `GF(9) = GF(3)[i]/(i^2+1)`: 91 projective
  points, 91 lines (10 points each);
* map the board quadrangle `[0, 1, 10, 20]` (no three collinear) to the standard
  frame `e1, e2, e3, (1,1,1)`;
* close under forced images (line through two mapped points; intersection of two
  mapped lines). This yields the 13-point/13-line `PG(2,3)` subplane;
* map one further point `2` and close again; the 25th of the 78 candidates
  (`2 -> 37`) closes consistently on all 91 points and 91 lines, and for every
  board line the image point set equals the image line.

`isomorphism test: PASS`, `points_mapped 91`, `lines_mapped 91`,
`isomorphism_ok True`. An explicit isomorphism is a proof that the board is
`PG(2,9)`.

---

## 1. Task 1 — complete 7-arcs and the six-subsets

### 1.1 Exhaustive cap census (independent DFS, `census.c`)

`census.c` was written from scratch: DFS over caps in increasing point order
(blocked = union of secant lines), which visits each cap exactly once.

Command:
```
gcc -O3 -march=native -o census.exe census.c
.\census.exe ..\..\pg2q9-cap-game-20261125\output\board_pg2q9.txt > census_out.txt 2>&1
```

Result (9.5 s): `nodes 128917712`, total caps **128,917,712**, maximal caps
**8,095,464**. Size table (caps / maximal):

| k | caps | maximal |
|---:|---:|---:|
| 0 | 1 | 0 |
| 1 | 91 | 0 |
| 2 | 4,095 | 0 |
| 3 | 110,565 | 0 |
| 4 | 1,769,040 | 0 |
| 5 | 14,859,936 | 0 |
| 6 | 52,009,776 | 707,616 |
| 7 | 51,554,880 | **2,021,760** |
| 8 | 7,960,680 | 5,307,120 |
| 9 | 589,680 | 0 |
| 10 | 58,968 | 58,968 |

These agree with the parent's census `output/census_pg2q9.txt` and with its
independent verification. The extension identities `ext[k] = (k+1)*cnt[k+1]`
hold for every `k >= 2` (for `k = 0,1` the blocked-mask convention also counts
the cap's own point(s), giving `ext[1] = 8281`; this is the same convention as
in the parent's `sixsub.c` and is not an error in the census counts).

### 1.2 Second enumeration of the 6-caps: brute force over all C(91,6) subsets (`brute6.c`)

Completely different algorithm: six nested loops over **all**
`C(91,6) = 666,563,898` point subsets, testing each with 15 explicit
“line contains exactly two of the six points” checks.

Command:
```
gcc -O3 -march=native -o brute6.exe brute6.c
.\brute6.exe ..\..\pg2q9-cap-game-20261125\output\board_pg2q9.txt > brute6_out.txt 2>&1
```

Result (20.7 s):

```
scanned 666563898 (expected 666563898) OK
6-caps 52009776  maximal6 707616
ext histogram: 0:707616 4:1769040 6:14152320 7:14152320 8:21228480
max-child histogram: 0:37857456 1:14152320
Grundy: g0=37857456 g1=0 g2=14152320 g3+=0 sum=52009776
#6-caps with a maximal 7-child = 14152320
#6-caps with ext==1 = 0
```

`#maximal 7-caps = #(6-cap, maximal-7-child) pairs / 7 = 14,152,320 / 7 =
2,021,760`, which independently reproduces the complete-7-arc count without
enumerating 7-caps. It also shows that every 6-cap has **at most one** maximal
7-child (histogram bins 0 and 1 only), i.e. no two complete 7-arcs share six
points — a second, independent proof of the distinctness of the 14,152,320
six-subsets.

Small-size sanity checks (`brute_small.c`, direct subset iteration for k=1..5)
reproduce exactly: 91 / 4,095 / 110,565 / 1,769,040 / 14,859,936 caps and the
same `|addable|` histograms (91, 81, 64, 42, 21). `rank_check.py` verifies that
the combinatorial-number-system rank used by the bitmap is a bijection for
n=10,12 and has no collisions on 200,000 random 6-subsets of 91 points.

Command/outputs: `python rank_check.py` → `out_rank.txt`;
`.\brute_small.exe ...` → `out_brute_small.txt`.

### 1.3 Six-subsets of complete 7-arcs: distinctness by an 81 MB bitmap

`census.c` marks, for every maximal 7-arc, the combinatorial rank
`r = sum_i C(x_i, i+1)` of each of its 7 six-subsets in a bitmap of
`C(91,6) = 666,563,898` bits, and checks for collisions.

```
six-subsets of maximal 7-arcs:
  arcs 2021760  six_subsets 14152320  bad_add_inter 0
  arcAllSeven 2021760  arcAnyNotSeven 0
  ext histogram: 7:14152320
  marks 14152320  distinct(sbm popcount) 14152320  dups 0
  marks == 7*maxcnt7 ? yes
  distinct == marks ? yes
```

So exactly **14,152,320** six-subsets, all **distinct, duplicates 0**;
every one of them has exactly 7 addable points (`ext histogram: 7:14,152,320`).

### 1.4 Conic cross-check of the 8/9/10-cap layer (`conics.py`)

`conics.py` builds the standard `PG(2,9)` from GF(9) directly (no board file),
enumerates the zero sets of all non-degenerate homogeneous quadratics
(canonical 6-tuples up to GF(9)^*), and verifies:

```
canonical nonzero symmetric 6-tuples: 66430
non-degenerate conics: 58968 (expected 58968)
degenerate forms: 7462; bad size/cap/maximal: 0/0/0
distinct conic point sets: 58968

conic 9-subsets: 589680 (expected 589680) PASS
  9-subset addable-set==missing sample: 3000 checked, bad 0
conic 8-subsets: 2653560 (expected 2653560) PASS
  8-subset addable-set==missing-pair sample: 13500 checked, bad 0
```

i.e. every conic is a maximal 10-cap; the 589,680 conic 9-subsets are distinct
9-caps, and the 2,653,560 conic 8-subsets are distinct non-maximal 8-caps. On
the sampled subsets the addable set is exactly the missing conic point(s)
(3,000 nine-subsets and 13,500 eight-subsets checked); moreover these counts
equal the census `cnt[9]` and `cnt[8]-maxcnt[8]`, and the census says every
non-maximal 8-cap has exactly 2 addable points and every 9-cap exactly 1, so
the property holds for all of them. This matches `cnt[10] = maxcnt[10] =
58,968`, `cnt[9] = 589,680`, `cnt[8]-maxcnt[8] = 2,653,560`, and pins
`G(10)=0`, `G(9)=1`, `G(8)=0`.

Command/output: `python conics.py` → `out_conics.txt`.

### 1.5 Audit + rerun of the parent's programs

The parent's `sixsub.c` / `sortcount.c` were read and audited: the DFS over
caps, the `blocked` secant mask, the `is_max` test, the dump of the 7
six-subsets of every maximal 7-arc (128-bit masks), and the 128-bit sort/count
are all logically correct. Rerun in this directory:

```
gcc -O3 -o parent_sixsub.exe ..\sixsub.c
gcc -O3 -o parent_sortcount.exe ..\sortcount.c
.\parent_sixsub.exe ..\..\pg2q9-cap-game-20261125\output\board_pg2q9.txt --dump6sub parent_sixsub_masks.bin
.\parent_sortcount.exe parent_sixsub_masks.bin
```

```
nodes 128917712      (# all caps)
max1 6 707616
max1 7 2021760
total 128917712
max_total 8095464
n 14152320 distinct 14152320 duplicates 0
```

Identical to the parent's reported result. (The 226 MB dump file was deleted
after counting; it is regenerable.) Outputs: `parent_sixsub_out.txt`,
`parent_sortcount_out.txt`.

### Task 1 verdict: **PASS**

* board is PG(2,9) (explicit isomorphism);
* complete 7-arcs = 2,021,760 (two independent computations: DFS census and
  brute-force 6-subset pair count / 7);
* 14,152,320 six-subsets, all distinct, duplicates 0 (two independent
  computations: rank bitmap and the brute-force max-child histogram).

---

## 2. Task 2 — claim (B): 7 addable points, “namely the points of A”

Method: 25 complete 7-arcs found by random greedy + maximality check
(677 greedy runs) plus 3 complete 7-arcs known from the parent reports, all 7
six-subsets each = 196 six-subsets. For every `X = A - {p}` the full addable
set `{q : X ∪ {q} is a cap}` was computed from the board incidence. The
exhaustive census repeats the same computation for **all 14,152,320** six-subsets
of all 2,021,760 complete 7-arcs.

Command: `python verify_b.py` → `out_verify_b.txt`

Summary over the 196 sampled six-subsets:

```
|addable(X)| == 7                                    196/196  PASS
addable(X) == A  (literal claim B)                   0/196  FAIL
1 maximal + 6 non-maximal 7-children                 196/196  PASS
structural mex (child G in {0,1}) == 2               196/196  PASS
addable-set-is-a-cap: 196/196
```

Exhaustive census: `|addable| = 7` for all 14,152,320 six-subsets
(`ext histogram: 7:14152320`), and for every one of them the addable set meets
`A` in exactly the removed point (`bad_add_inter 0`, i.e.
`addable(X) ∩ A = {p}` always).

**Discrepancy D1.** The count “exactly 7 addable points” is correct, but the
identification “namely the points of A” is false: the addable set is
`{p} ∪ {6 points outside A}`. The 6 points of `X` itself are on secant lines
and are never addable. (A plausible origin of the parent's wording, stated as a
hypothesis since the sampling script is not in the repo: an addability test that
does not exclude the points of `X` returns the 6 points of `X` trivially plus
`p`, i.e. exactly the 7 points of `A`.)

Additional observation (not needed for the claims): in all 196 sampled
six-subsets the 7-point addable set is itself a 7-cap; for the 28 six-subsets
of 4 complete 7-arcs it was checked further to be a conic 7-subset
(non-maximal, exactly 3 addable points, union a 10-cap). This is consistent
with, and explains, the “7” in the parent's observation while refuting the
“= A” part.

**Task 2 verdict: numerical part PASS, literal set identification FAIL.**

---

## 3. Task 3 — claim (C): full Grundy value by upset DP

For a position `S`, the upset `{caps containing S}` was enumerated and its
Grundy values computed bottom-up by decreasing size (terminal = no move = 0),
with the legality of every move re-derived from the board incidence (no
structural shortcut). Command: `python verify_c.py` → `out_verify_c.txt`.

25 six-subsets of complete 7-arcs were evaluated: all 7 subsets of three
complete 7-arcs, one subset of three further complete 7-arcs, and the parent's
earlier witness `{0,1,10,20,32,39}`. For every one:

```
upset positions = 11      G(X) = 2
child Grundy values = [0, 1, 1, 1, 1, 1, 1]   (mex = 2)
maximal caps in upset: 4, sizes {7,8}, all G=0
```

So every `X = A - {p}` has exactly `1 + 6 = 7` children: `A` (terminal,
G=0) and six non-maximal 7-caps (G=1), and `mex{0,1} = 2`. The maximal
extensions are `A` (7-cap) and three maximal 8-caps (each 8-cap contains `X`
and two of the six addable points); the parity is mixed `{7,8}`.

**Discrepancy D2.** The stated “six `X+q`, `q ∈ A - {p}`” is wrong: those `q`
are already points of `X`, so `X+q = X` (a 6-cap), not a 7-cap. The six
non-maximal 7-children are `X+q` for the six addable points `q` **outside** `A`;
each has exactly one addable point (a non-conic non-maximal 7-cap), and pairs of
them share one of the three maximal 8-caps. The conclusion
`children G values {0,1} ⇒ mex 2` is nevertheless correct.

Global confirmation (`census.c`, `brute6.c`): exactly 14,152,320 6-caps have a
maximal 7-child; all of them have `|addable| = 7`, exactly one maximal child and
six non-maximal children, hence G=2. All other 6-caps have only non-maximal
7-children (G=1) and hence `mex{1} = 0`. The complete Grundy distribution of
the 6-caps is

```
G=0: 37,857,456   G=1: 0   G=2: 14,152,320   (sum 52,009,776)
```

**Task 3 verdict: PASS (conclusion G=2), with descriptive discrepancy D2.**

---

## 4. Task 4 — claim (D): the counts and arithmetic

Two independent enumerations (`census.c` DFS and `brute6.c` all-subsets brute
force) both give:

```
#6-caps                 = 52,009,776
#6-caps with a maximal 7-child = 14,152,320   (= #complete 7-arcs × 7)
#6-caps with G=2        = 14,152,320
#6-caps with G=1        = 0
#6-caps with G=0        = 37,857,456
52,009,776 - 14,152,320 = 37,857,456          (exact)
```

The decomposition of the G=0 class is: 707,616 maximal 6-caps (terminal) plus
37,149,840 non-maximal 6-caps whose 7-children are all non-maximal 7-caps
(G=1, so `mex{1}=0`). There are no 6-caps with exactly one addable point
(`ext==1` count is 0 in both enumerations), which is why G=1 does not occur.

**Task 4 verdict: PASS** — both counts and the arithmetic are exactly as
claimed.

---

## 5. Task 5 — 6-caps without a complete 7-arc extension have G=0

Command: `python verify_e.py` → `out_verify_e.txt`.

* 25 random non-maximal 6-caps with **no** maximal 7-child (i.e. no complete
  7-arc extension), and 10 random maximal 6-caps;
* full upset DP for each (35 upsets, sizes 1–22 positions).

Result:

```
G values observed: [0]
every sampled cap has G=0: PASS
every maximal extension even-sized (6, 8 or 10) and G=0: PASS
=> no 6-cap without a complete 7-arc extension has G=2: PASS
```

The maximal extensions of the non-maximal sampled caps were all 8-caps or
10-caps (even), and all had Grundy 0. Globally, `brute6.c` shows that every
6-cap has 0 or 1 maximal 7-children, and the G=2 class is exactly the 14,152,320
six-subsets; the remaining 37,857,456 all have G=0.

**Task 5 verdict: PASS.**

---

## 6. Discrepancies

1. **D1 (claim B, bookkeeping error).** For `X = A - {p}` the addable set is
   `{p} ∪ (6 points outside A)`, not `A`. The number 7 is correct
   (14,152,320/14,152,320 six-subsets; 196/196 sampled). In the full census the
   addable set always meets `A` in exactly `{p}`. Likely cause: an addability
   test that counts the points of `X` themselves as addable (they pass
   trivially), giving `6 + 1 = 7 = A`; the sampling script is not in the
   repository, so this cannot be audited directly.
2. **D2 (claim C, description).** “six `X+q` with `q ∈ A - {p}`” is impossible
   because those `q` belong to `X`; the six non-maximal 7-children correspond to
   the six addable points outside `A`. The mex computation
   (`{0,1} → 2`) and therefore `G(X)=2` are correct.
3. **No numerical discrepancy.** Board isomorphism, complete-7-arc count,
   six-subset count/distinctness, `G=2`/`G=0` counts, and the arithmetic all
   match the claims exactly. In particular the conclusions of K1333
   (`G=2 = 14,152,320`, `G=0 = 37,857,456`) are correct; only the supporting
   wording in K1333 (line 55: “追加可能集合 = その完全 7-アーク自身” and
   “q ∈ A - p”) is wrong.

---

## 7. Reproduce

All commands are run from
`research/experiments/pg2q9-sixcap-20261126/independent/`.
The board file is read via the relative path
`..\..\pg2q9-cap-game-20261125\output\board_pg2q9.txt`.

```
# board axioms + explicit isomorphism to PG(2,9)
python verify_board.py

# full independent census (caps by size, maximal, 6-cap Grundy distribution,
# six-subset bitmap distinctness); ~10 s
gcc -O3 -march=native -o census.exe census.c
.\census.exe ..\..\pg2q9-cap-game-20261125\output\board_pg2q9.txt > census_out.txt 2>&1

# independent all-6-subsets brute force; ~21 s
gcc -O3 -march=native -o brute6.exe brute6.c
.\brute6.exe ..\..\pg2q9-cap-game-20261125\output\board_pg2q9.txt > brute6_out.txt 2>&1

# brute-force k=1..5 caps
gcc -O3 -march=native -o brute_small.exe brute_small.c
.\brute_small.exe ..\..\pg2q9-cap-game-20261125\output\board_pg2q9.txt

# combinatorial rank sanity
python rank_check.py

# claim B sample: 25 random-greedy + 3 known complete 7-arcs × 7 six-subsets
python verify_b.py

# claim C: full upset Grundy DP on 25 six-subsets (+ witness)
python verify_c.py

# task 5: 25 non-maximal 6-caps without a complete 7-arc extension + 10
# random maximal 6-caps
python verify_e.py

# structural G formula vs full upset DP on 200 random 6-caps
python random_consistency.py

# independent conic enumeration (8/9/10-cap layer)
python conics.py

# audit: rerun the parent's programs (optional; needs ~230 MB for the dump)
gcc -O3 -o parent_sixsub.exe ..\sixsub.c
gcc -O3 -o parent_sortcount.exe ..\sortcount.c
.\parent_sixsub.exe ..\..\pg2q9-cap-game-20261125\output\board_pg2q9.txt --dump6sub parent_sixsub_masks.bin
.\parent_sortcount.exe parent_sixsub_masks.bin
```

## 8. Files

| file | content |
|---|---|
| `boardlib.py` | board loading/validation, explicit PG(2,9) model over GF(9), constructive isomorphism test |
| `capgame.py` | cap primitives + full upset Grundy DP |
| `census.c` | independent DFS census, six-subset bitmap, 6-cap Grundy distribution |
| `brute6.c` | brute force over all C(91,6) six-subsets; second independent 6-cap enumeration |
| `brute_small.c` | brute force caps of size 1..5 |
| `verify_board.py` | board axioms + isomorphism, output `out_board.txt` |
| `verify_b.py` | claim B sample, output `out_verify_b.txt` |
| `verify_c.py` | claim C upset DP, output `out_verify_c.txt` |
| `verify_e.py` | Task 5 sampling, output `out_verify_e.txt` |
| `random_consistency.py` | structural G vs full DP, `out_random_consistency.txt` |
| `rank_check.py` | combinatorial rank sanity, `out_rank.txt` |
| `conics.py` | conic enumeration, `out_conics.txt` |
| `quick_check.py` | early reconnaissance (board + known 7-arcs) |
| `census_out.txt`, `brute6_out.txt`, `out_brute_small.txt` | raw program outputs |
| `parent_sixsub_out.txt`, `parent_sortcount_out.txt` | rerun of the parent's programs |
