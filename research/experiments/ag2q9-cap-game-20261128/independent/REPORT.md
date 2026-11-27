# Independent verification of K1354 — AG(2,9) s=2 cap-game Grundy spectrum

**Verdict: CLAIM VERIFIED.** Every number in the claimed size-layer spectrum was
reproduced exactly. No numerical discrepancy was found. One purely notational
ambiguity in the naming of the base 3-cap `F` is noted in §7; it is immaterial
(the two candidate triangles are in the same AGL orbit and give identical cone
statistics).

- Verifier: independent subagent (no access to the parent's reasoning/transcript;
  only the parent's *output files* were read).
- Workspace: everything below lives in
  `research/experiments/ag2q9-cap-game-20261128/independent/`.
  Nothing outside that directory was modified; nothing was committed.
- Environment: Python 3.12.13 (CPython), standard library only.
- Inputs (read-only):
  - `../output/board_ag2q9.txt` — SHA-256 `fa78bcb1f9a8965f00acd44971d681a1e04720e61f9d66d5525eedcd2dda9bb3`
  - `../output/ag2q9_spectrum.json` — SHA-256 `522b701c542111b87eee5b52329c01de88fc1af5705314b0e5430b97806d6f0d`
- Claim under test: K1354 (21,353-position cone + AGL(2,9) triangle transitivity
  + double counting), including all per-size Grundy counts and the totals.

---

## 1. Board and parent indexing (task 1)

### 1.1 Independent construction

`common.py` builds AG(2,9) from scratch over

```
GF(9) = GF(3)[i]/(i^2 + 1),   element (a,b) = a + b*i,   enc(a,b) = 3a + b
```

with its **own** point order `idx(x,y) = 9*enc(y) + enc(x)` (y-major; the parent
uses x-major) and its own line order (9 verticals `x=c`, then 81 lines
`y = m*x + b`). No parent code was used.

Verified axioms (all pass):

| check | result |
|---|---|
| 81 points, 90 lines, 9 distinct points per line | yes |
| every unordered pair of points on exactly one line | yes (all 3,240 pairs) |
| any two distinct lines meet in at most one point | yes |
| number of disjoint line pairs = 90·8/2 | 360 |
| every point on exactly 10 lines | yes |
| 10 parallel classes, each 9 disjoint lines covering all 81 points | yes |

The parent board passes exactly the same axiom package.

### 1.2 Parent point indexing (determined)

The parent's index is

```
parent_index(x, y) = 9*enc(x) + enc(y),        enc(a+bi) = 3a + b
```

(in the parent's field labelling `0,1,2,i,1+i,1+2i,2,2+i,2+2i` for 0..8), and its
line order is

```
lines 0..8   : vertical lines  x = c          (c in element order 0..8)
lines 9..89  : lines            y = m*x + b   (m in element order 0..8,
                                               then b in element order 0..8)
```

Evidence (all true in the data):

- lines 0..8 are exactly the consecutive blocks `{9t,…,9t+8}`, partitioning the points;
- lines 9..17 are exactly the transversals `{9t+j : t}` (`j = 0..8`);
- **exact reconstruction**: building the 90 lines from the formula with
  `point i ↔ (x,y) = (dec(i//9), dec(i%9))` reproduces all 90 parent lines
  **including their order** (90/90 lines; also 90/90 as sets);
- the digit-swap permutation `i ↦ 9*(i mod 9) + i//9` maps my independently built
  board onto the parent board line-by-line in the same order.

### 1.3 Board equality

My board and the parent board are therefore the same labelled design under the
explicit index map above; all later computations were also repeated on my own
board and gave identical results (§3.4).

---

## 2. AGL(2,9) transitivity on triangles (task 2)

Fix the ordered triangle `T0 = ((0,0),(1,0),(0,1))`. For every ordered triangle
`T = (a,b,c)` put

```
phi_T(x,y) = a + x*(b-a) + y*(c-a)          (columns b-a, c-a)
```

which is the unique affine map with `phi_T(T0) = T`.

| quantity | value |
|---|---|
| ordered triangles (81·80·72) | **466,560** |
| distinct maps `phi_T` | **466,560** (injective) |
| `phi_T` sends `T0` to `T`, all T | yes |
| all `phi_T` invertible (`det ≠ 0`) | yes |
| `|GL(2,9)|` (ordered bases: 80·72) | **5,760** |
| `|AGL(2,9)| = 5760·81` | **466,560** |
| unordered triangles (non-collinear 3-subsets) | **77,760** = C(81,3) − 90·C(9,3) |

Since the 466,560 maps `phi_T` are distinct elements of AGL(2,9) and
`|AGL(2,9)| = 466,560`, they are *all* of AGL(2,9). Hence the action on ordered
triangles is **simply transitive**, and on unordered triangles **transitive**
(77,760 = 466,560/6). Additional checks with zero failures: 500 random ordered
triangle pairs were mapped by `phi_{T'} ∘ phi_T^{-1}`; 2,000 random compositions
of the maps stayed inside the map set; 300 random maps sent every line of the
board to a line.

**Consequence used below.** Every `m`-cap with `m ≥ 3` contains a triangle (a cap
has at most 2 points on a line), and every triangle is an AGL image of `F`; an
affine map is a bijection of the point set with lines ↦ lines, hence a game
isomorphism and preserves Grundy values. Therefore *every* cap is an affine image
of a cap in the cone of `F`, with the same size and Grundy value.

---

## 3. Cone of F, full Grundy DP, and double counting (task 3)

Main object: `F = {0, 9, 1}` in parent indexing = `{(0,0), (i,0), (0,i)}` in field
coordinates (`(0,0),(1,0),(0,1)` in the parent's *element-index* notation).

### 3.1 Cone enumeration (exhaustive, two ways)

| check | result |
|---|---|
| cone size | **21,353** (claim 21,353) |
| every element contains `F` and is a cap | yes |
| **closure/completeness**: for every cone cap and every point `p` (21,353 caps × 81 points), `p` is safe ⇔ `cap ∪ {p}` is in the cone | **0 failures** |
| independent re-enumeration: from-scratch safety test + shuffled point order | 21,353, **same set** |
| maximal caps in cone = caps with no safe extension | yes |

The closure property is a *proof* of completeness: every subset of a cap is a cap,
so any cap `C ⊇ F` is reached from `F` by repeatedly adding one of its points;
each intermediate set is a cap, hence a safe child, hence (by closure) in the
enumerated set. So the enumerated set is exactly the set of all caps containing
`F`.

### 3.2 Per-size counts `T_m` (caps containing F) and Grundy distribution `T_m(g)`

| m | `T_m` | Grundy distribution in the cone |
|---:|---:|---|
| 3 | 1 | G1: 1 |
| 4 | 57 | G0: 57 |
| 5 | 1,071 | G1: 1,011 / **G3: 60** |
| 6 | 6,762 | G0: 3,142 / G1: 20 / G2: 3,600 |
| 7 | 10,710 | G0: 1,155 / G1: 9,555 |
| 8 | 2,457 | G0: 2,415 / G1: 42 |
| 9 | 259 | G0: 7 / G1: 252 |
| 10 | 36 | G0: 36 |
| **Σ** | **21,353** | |

This matches the parent's `ag2q9_spectrum.json` (`T`, `T_g`) exactly, and the
claimed cone table exactly. Additional consistency: for every `m ∈ {3..9}`,
`Σ_{|S|=m} #safe extensions = (m−2)·T_{m+1}`
(57, 2142, 20286, 42840, 12285, 1554, 252 — all match). Max Grundy in the cone
is **3** (the 60 five-caps of class (5,3)).

### 3.3 Double counting (the claim's method)

`N_3 = number of triangles = C(81,3) − 90·C(9,3) = 85,320 − 7,560 = 77,760`.

For a fixed triangle `T` let `T_m(g)` be the number of size-`m` caps containing
`T` with Grundy `g`; by §2 this is independent of `T`. Counting pairs
`(m-cap C, triangle T ⊆ C)` two ways:

```
N_m(g) · C(m,3)  =  N_3 · T_m(g)          ⇒   N_m(g) = N_3 · T_m(g) / C(m,3).
```

This is the `k0 = 3` instance of the K1353 cone/frame lemma (the general `k0`
form is in K1353; its two premises — transitivity on the `k0`-caps and Grundy
invariance — are verified in §2). All 14 divisions are exact (verified). The
resulting global table:

| k | N_m | Grundy distribution |
|---:|---:|---|
| 0 | 1 | G0: 1 |
| 1 | 81 | G1: 81 |
| 2 | 3,240 | G0: 3,240 |
| 3 | 77,760 | G1: 77,760 |
| 4 | 1,108,080 | G0: 1,108,080 |
| 5 | 8,328,096 | G1: 7,861,536 / **G3: 466,560** |
| 6 | 26,290,656 | G0: 12,216,096 / G1: 77,760 / G2: 13,996,800 |
| 7 | 23,794,560 | G0: 2,566,080 / G1: 21,228,480 |
| 8 | 3,411,720 | G0: 3,353,400 / G1: 58,320 |
| 9 | 239,760 | G0: 6,480 / G1: 233,280 |
| 10 | 23,328 | G0: 23,328 |

Totals: `G0 = 19,276,705`, `G1 = 29,537,217`, `G2 = 13,996,800`,
`G3 = 466,560`, **total 63,277,282** — all identical to the claim.

### 3.4 Robustness checks

The full cone DP was repeated for two other triangles on the parent board
(`{0,27,3}` = the README field-coordinate `F`, and `{0,30,55}`) and for `F` on my
independently built board. All four computations give **identical** cone size and
identical `T_m(g)` tables. This is a direct computational confirmation of
triangle transitivity + Grundy invariance on the relevant object.

---

## 4. Independent Grundy values by full upset DP (task 4)

For a cap `S`, its *upset* is the set of all caps containing `S`. `G(S)` was
recomputed from scratch: enumerate the upset with a from-scratch safety test
(`|S∩L| ≤ 2` checked directly, shuffled point order), then run a fresh
descending-size mex DP on that upset and read off `G(S)`. This uses neither the
cone enumeration nor the cone DP.

| coverage | count | mismatches |
|---|---:|---:|
| **every** cone cap of size ≥ 4 | **21,352** | **0** |
| `F` + 10 random AGL images of `F` (10 further triangles) | 11 | 0 (all G=1) |
| random global affine images, 12 per claimed class | 168 | **0** |

All 14 claimed nonzero classes were sampled (the affine images are genuinely
different caps not containing `F`, so they test global positions and invariance):

| class | claim | cone caps re-verified | global images verified |
|---|---:|---:|---:|
| (3,1) | 77,760 | 1 (`F`, separately) | 12/12 |
| (4,0) | 1,108,080 | 57 | 12/12 |
| (5,1) | 7,861,536 | 1,011 | 12/12 |
| **(5,3)** | **466,560** | **60** | **12/12** |
| (6,0) | 12,216,096 | 3,142 | 12/12 |
| (6,1) | 77,760 | 20 | 12/12 |
| **(6,2)** | **13,996,800** | **3,600** | **12/12** |
| (7,0) | 2,566,080 | 1,155 | 12/12 |
| (7,1) | 21,228,480 | 9,555 | 12/12 |
| (8,0) | 3,353,400 | 2,415 | 12/12 |
| (8,1) | 58,320 | 42 | 12/12 |
| (9,0) | 6,480 | 7 | 12/12 |
| (9,1) | 233,280 | 252 | 12/12 |
| (10,0) | 23,328 | 36 | 12/12 |

So the whole cone Grundy table is confirmed cap-by-cap by a second, structurally
different computation, and every claimed class is confirmed to exist globally
with the claimed value (in particular the rare `G=3` 5-caps and `G=2` 6-caps).
Every claimed class has at least **12** independently computed global exemplars
(and, for `m ≥ 4`, all of its cone representatives as well). Random upsets of
triangle images all had exactly 21,353 caps, as predicted. The class *counts*
themselves are not estimated by sampling; they come from the exhaustive cone
table and the proved formula in §3 — the samples confirm the labels globally.

---

## 5. k = 0,1,2 mex chain, independent global counts, arithmetic (task 5)

### 5.1 Direct global cap counts (no cone, no Grundy table)

A single increasing-order DFS over caps (unique largest point) gives:

| quantity | independent count | claim |
|---|---:|---:|
| `N_3 = C(81,3) − 90·C(9,3)` | 77,760 | 77,760 |
| `N_3` by DFS | 77,760 | — |
| `N_4` by DFS | **1,108,080** | 1,108,080 |
| `N_5` by DFS | **8,328,096** | 8,328,096 |

Via `T_m = N_m·C(m,3)/N_3` this independently gives `T_3 = 1`, `T_4 = 57`,
`T_5 = 1,071` — exactly the cone counts of §3.2, without using the cone.

### 5.2 The mex chain for k = 0,1,2

- `G(∅)`: no moves ⇒ `0`.
- Every 2-subset of points is a cap (a line meets it in ≤ 2 points), so
  `N_2 = C(81,2) = 3,240`. From a 2-cap every legal move adds one point and
  reaches a 3-cap; all 3-caps have `G = 1` (every triangle is an AGL image of
  `F` by §2, and `G(F)=1` by §3/§4; Grundy values are affine-invariant). Hence
  `G(2-cap) = mex{1} = 0`.
- A 1-point position has the 80 two-caps through it as options; all have `G=0` ⇒
  `G = mex{0} = 1`.
- The empty position has the 81 one-point positions as options; all have `G=1` ⇒
  `G = mex{1} = 0`.

Counts: `N_0 = 1`, `N_1 = 81`, `N_2 = 3,240` — exactly the claim.

### 5.3 Arithmetic

- Per-size Grundy counts sum to `N_m` for every `m`, and `Σ_m N_m = 63,277,282`.
- Grundy totals `19,276,705 / 29,537,217 / 13,996,800 / 466,560` (Σ = 63,277,282).
- The parent's `ag2q9_spectrum.json` (`N`, `N_g`, `T`, `T_g`, `cone_size`,
  `N3`) is internally consistent and equals the claim and my recomputation.

---

## 6. What is proved, what is computed, what is not

**Proved (with the verified premises below):**

1. AGL(2,9) is simply transitive on ordered triangles (counting + injectivity);
   transitive on the 77,760 triangles. *(verified exhaustively)*
2. Every cap is an affine image of a cap containing `F`, and affine maps preserve
   the game (they are point bijections with lines ↦ lines), hence preserve
   Grundy values. *(elementary proof; transitivity verified, line preservation
   sampled)*
3. Therefore the global spectrum is `N_m(g) = N_3·T_m(g)/C(m,3)`; the numbers in
   §3.3 follow from the exhaustive cone table. *(double counting proof)*
4. Max Grundy globally = 3 and max cap size = 10: no 11-cap exists, and every
   cap with ≥ 3 points is an affine image of a cone cap.
5. The k=0,1,2 mex chain of §5.2.

**Exhaustively computed (independent of the parent's code):**

- board axioms and the parent indexing (§1);
- ordered-triangle ↔ AGL bijection (§2);
- cone of `F`: exactly 21,353 caps, complete by the closure argument and
  reproduced by a second from-scratch DFS (§3.1);
- `T_m` and `T_m(g)` for all `m = 3..10` (§3.2), and again cap-by-cap for all
  21,352 caps of size ≥ 4 by fresh upset DPs (§4);
- `N_3`, `N_4`, `N_5` by direct global DFS (§5.1);
- consistency on two other triangles and on the independently built board (§3.4).

**Not independently enumerated (and why this is not a gap):**

- `N_6, …, N_10` were not obtained by a direct global enumeration of 26M/24M/…/23K
  caps; they follow from the *proved* double-counting formula and the
  exhaustively verified cone table. (A direct global enumeration of, e.g., all
  6-caps is feasible in principle but adds no logical strength.)
- `G` for the k=0,1,2 positions was proved by the mex chain rather than by a
  per-position upset DP (the upset of a 2-cap has ≈ 3.4·10^5 caps). The chain is
  rigorous given the exhaustively verified fact that all 3-caps have `G = 1`.
- Random sampling in §4 is not itself a proof; the proof rests on the exhaustive
  cone computation plus the orbit argument. The samples are global cross-checks
  of the claimed class labels.

---

## 7. Discrepancies and notes

1. **F naming (notational only, immaterial).** The parent's script uses
   `F = bits {0,9,1}`. With the parent's own indexing that is
   `{(0,0), (i,0), (0,i)}` in field coordinates, i.e. `(0,0),(1,0),(0,1)` if the
   numbers 0..8 denote *field-element indices* (element 1 = `i`). Read instead as
   literal field coordinates, `F = {(0,0),(1,0),(0,1)}` would be bits
   `{0,27,3}`. Both sets are genuine 3-caps (checked against all 90 lines), both
   lie in the single AGL orbit of triangles, and both give **identical** cone
   size and `T_m(g)` table (§3.4). The claim's numbers are therefore unaffected.
2. No numerical discrepancy was found anywhere: every claimed count, every
   per-size distribution, the cone size, `N_3`, and both totals match exactly.
3. The README's "0.03% of 63.28M positions" is accurate:
   21,353 / 63,277,282 = 0.0337%.
4. The `G3` field in `ag2q9_spectrum.json` is `G(F) = 1` (a Grundy value, not a
   count); it is consistent with the computation.
5. Out of scope: the comparative statements attached to K1354 ("`q = 9` is the
   first `q` with max Grundy 3", comparison with PG(2,9)/K1352, the K1300 series
   claim) refer to other boards/items and were **not** checked here. This report
   verifies the AG(2,9) spectrum itself and the stated method.

---

## 8. Reproduction

All commands are run from this directory (`independent/`), standard library only:

```
python task1_board.py     # board axioms + parent indexing        (~2 s)
python task2_agl.py       # AGL transitivity on triangles         (~10 s)
python task3_cone.py      # cone + full Grundy DP + formula       (~30 s)
python task4_upset.py     # per-cap independent upset DPs         (~3 min)
python task5_mex.py       # mex chain + global counts k<=5 + sums (~40 s)
# or simply
python run_all.py
```

Each script exits 0 on success and writes a JSON report under `out/`:

| file | contents |
|---|---|
| `out/task1_board.json` | board axioms, parent indexing determination, F analysis |
| `out/task2_agl.json` | triangle/AGL counts, transitivity and closure checks |
| `out/task3_cone.json` | cone size, `T_m`, `T_m(g)`, formula values, totals |
| `out/cone_by_class.json` | every cone cap grouped by (size, Grundy) |
| `out/task4_upset.json` | per-cap upset DP results and global class samples |
| `out/task5_mex.json` | global counts `N_3,N_4,N_5`, mex chain, arithmetic |

Source: `common.py` (field/board), `caplib.py` (two independent enumerators +
Grundy DP), `task1_board.py` … `task5_mex.py`.
