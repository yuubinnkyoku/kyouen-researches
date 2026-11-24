# Independent verification — PG(2,9), s=2 cap census

Date: 2026-11-25.  Verifier: independent sub-agent.  Scope: only
`research/experiments/pg2q9-cap-game-20261125/independent/` was written.
Nothing was committed; nothing outside this directory was modified.

Board under test (produced by the parent experiment):
`research/experiments/pg2q9-cap-game-20261125/output/board_pg2q9.txt`.

Everything below was recomputed from the board file with code written from
scratch for this verification.  The parent's C program
(`pg2q8-cap-game-20261125/scripts/cap_census.c`), its Python builder and its
results were **not** used or imported.

---

## Verdict

| Task | Verdict | One-line result |
|---|---|---|
| 1. Board is PG(2,9) | **PASS** | all plane axioms hold; rebuilt from GF(9)=GF(3)[x]/(x²+1); explicit relabeling maps the 91 GF(9) lines onto the 91 board lines |
| 2. Full cap enumeration | **PASS** | 128,917,712 caps, size distribution matches every entry; enumerator validated on PG(2,3) and PG(2,8) (and PG(2,5), PG(2,7)) |
| 3. Maximal-cap counts, two tests | **PASS** | 6: 707,616 / 7: 2,021,760 / 8: 5,307,120 / 9: 0 / 10: 58,968; test 1 ≡ test 2 on all 128,917,712 caps |
| 4. Structural identities | **PASS** | conics = 9⁵−9² = 58,968 = 10-caps (set equality); 9-caps = 58,968×10 (set equality); non-max-8 = 58,968×C(10,8) (set equality); mixed parity confirmed, and a concrete position with Grundy 2 was found by exact computation |
| 5. 250 sampled caps | **PASS** | 50/50 in each of the five classes, checked by an independent Python implementation |

**Discrepancies found: none.**  The claimed numbers are reproduced exactly.

---

## Environment / how to reproduce

```
windows, pwsh;  Python 3.12.13 (stdlib only);  gcc 15.2.0 (MSYS2, x86_64-w64-mingw32)
working dir: research/experiments/pg2q9-cap-game-20261125/independent/
```

Build and run, in this order (all artifacts land in `out/`):

```powershell
gcc -O2 -o capcensus.exe capcensus.c        # census (u128 point masks, n <= 128)
gcc -O2 -o setcmp.exe    setcmp.c           # binary mask-set comparison
gcc -O2 -o arcscan.exe   arcscan.c          # frame-based 4/5-cap count

python make_boards.py                       # PG(2,q) boards q=3,5,7,8,9 (independent construction)
python task1_board.py                       # Task 1: axioms + GF(9) rebuild + isomorphism
./capcensus.exe out/board_pg2q3.txt > out/census_pg2q3.txt
./capcensus.exe out/board_pg2q5.txt > out/census_pg2q5.txt
./capcensus.exe out/board_pg2q7.txt > out/census_pg2q7.txt
./capcensus.exe out/board_pg2q8.txt > out/census_pg2q8.txt
python validate_reference.py                # reference distributions

# main run (75.9 s): dumps of 9-caps, 10-caps, non-maximal 8-caps + reservoirs
./capcensus.exe ../output/board_pg2q9.txt --dump9 out/caps9.bin --dump10 out/caps10.bin `
    --dump-nonmax8 out/nonmax8.bin --samples out/samp > out/census_pg2q9.txt 2> out/census_pg2q9.err
python summarize.py                         # claimed vs observed, both maximality tests

python permute_board.py                     # random point permutation (seed 12345)
./capcensus.exe out/board_pg2q9_perm.txt > out/census_pg2q9_perm.txt   # 74.2 s

python conics.py                            # Task 4: conics, subsets, mapped to board labels
./setcmp.exe out/caps10.bin   out/conic10_board.bin
./setcmp.exe out/caps9.bin    out/conic9_board.bin
./setcmp.exe out/nonmax8.bin  out/conic8_board.bin

python grundy_witness.py                    # exact Grundy of a residual game (witness)
python verify_samples.py                    # Task 5
./arcscan.exe ../output/board_pg2q9.txt     # independent 4/5-cap counts
```

Machine-readable results: `out/task1.json`, `out/checks.json`,
`out/task4_conics.json`, `out/task4_grundy_witness.json`,
`out/task5_samples.json`, `out/validate_reference.json`, `out/census_pg2q*.txt`.

A final end-to-end re-run of every check (Task 1, reference planes, census
comparison, conics, the three set comparisons, Grundy witness, samples,
frame-based arc scan) is captured verbatim in `out/final_sweep.txt`; all of
them pass.

---

## Task 1 — the board is PG(2,9)

`task1_board.py`, `pgcore.py`.  The board file is parsed as
`n lines / k p1..pk` and checked against the axioms of a projective plane of
order q = k−1:

```
n = 91, nlines = 91, line sizes = {10}        (q = 9, 9²+9+1 = 91)
point degrees = {10}
point pairs: 4095 = C(91,2) distinct pairs, bad pairs 0   (every pair on exactly one line)
line pairs: every pair of the 91 lines meets in exactly one point (bad = 0)
```

`pgcore.py` builds GF(9) = GF(3)[x]/(x²+1) from scratch (full field-axiom
check: associativity, commutativity, distributivity, inverses for all 729
triples) and constructs PG(2,9) **from the zero sets of the 91 nonzero normal
vectors** `{v : u·v = 0}` — a different construction from the parent builder,
which used spans of point pairs.  The model also satisfies all axioms.

**Relabeling.**  The 91 points of the model and the 91 point labels of the
board are *different* orderings (72 of 91 line label-sets differ), so an
explicit isomorphism is needed.  `find_isomorphism` uses constraint
propagation (a source line with ≥2 mapped points fixes a target line and
confines its unmapped points to the unused points of that line; singleton
supports are forced) plus guesses on the most constrained point.  Since the
collineation group of PG(2,9) acts sharply transitively on ordered frames
(|PGL(3,9)| = 42,456,960 = number of ordered frames), the solution is unique;
the search found it after **2 nodes**:

```
frame model (0,0,1),(0,1,0),(1,0,0),(1,1,1)  ->  board 0,1,10,20
all 91 model lines map onto board lines, the 91 images are exactly the board line set
=> out/iso_model_to_board.json
```

The permutation is reused in Task 4 to express conics in board labels.
Side remark: `arcscan.exe` independently counts 42,456,960 ordered frames,
which equals |PGL(3,9)| = 9³(9³−1)(9²−1)/(9−1) — the expected sharp
transitivity figure.

## Task 2 — full cap enumeration

`capcensus.c`: depth-first enumeration of every cap exactly once by increasing
point sequence.  State = `blocked` = union of all secant lines of the current
cap (a 128-bit mask); a point may be added iff it is not in `blocked`.  The
candidate list is **snapshotted as a local 128-bit mask (`rest`) before
iteration**; the loop consumes only the snapshot (`rest &= ~bit`) and never
mutates the array being iterated.  Per child, `blocked` is rebuilt from the
`|S|` lines joining the new point to the cap.

Main run on the published board: **128,917,712 nodes in 75.9 s**
(`out/census_pg2q9.txt`), sizeof counters `long long`, dumps of the 9-caps,
10-caps and non-maximal 8-caps for Task 4.

| k | caps (observed) | claim | maximal (test1) | maximal (test2) | claim |
|---:|---:|---:|---:|---:|---:|
| 0 | 1 | 1 | 0 | 0 | 0 |
| 1 | 91 | 91 | 0 | 0 | 0 |
| 2 | 4,095 | 4,095 | 0 | 0 | 0 |
| 3 | 110,565 | 110,565 | 0 | 0 | 0 |
| 4 | 1,769,040 | 1,769,040 | 0 | 0 | 0 |
| 5 | 14,859,936 | 14,859,936 | 0 | 0 | 0 |
| 6 | 52,009,776 | 52,009,776 | **707,616** | **707,616** | 707,616 |
| 7 | 51,554,880 | 51,554,880 | **2,021,760** | **2,021,760** | 2,021,760 |
| 8 | 7,960,680 | 7,960,680 | **5,307,120** | **5,307,120** | 5,307,120 |
| 9 | 589,680 | 589,680 | **0** | **0** | 0 |
| 10 | 58,968 | 58,968 | **58,968** | **58,968** | 58,968 |
| total | **128,917,712** | 128,917,712 | 8,095,464 | 8,095,464 | 8,095,464 |

### Enumerator validation before use (required)

Boards built independently by `make_boards.py` and fed to the same binary:

| plane | caps | expected | distribution | maximal |
|---|---:|---:|---|---|
| PG(2,3) | 560 | 560 | {0:1,1:13,2:78,3:234,4:234} exact | 4: 234 |
| **PG(2,8)** | **19,550,350** | 19,550,350 | **{0:1,1:73,2:2628,3:56064,4:686784,5:4120704,6:8928192,7:3924480,8:1471680,9:327040,10:32704} exact** | 6: 2,060,352 / 10: 32,704 |
| PG(2,5) (extra) | 41,572 | 41,572 | exact | 6: 3,100 |
| PG(2,7) (extra) | 2,446,460 | 2,446,460 | exact | 6: 625,632 / 8: 16,758 |

The PG(2,8) distribution matches the requested reference distribution entry by
entry (`out/validate_reference.json`, PASS).  The PG(2,5)/PG(2,7) maxima also
match the figures recorded independently in the repo's knowledge base.

### Additional independent checks on the size counts

* **Edge/node identity** (`summarize.py`): with `ext[k] = Σ_{k-caps} #addable`
  the identity `ext[k] = (k+1)·cnt[k+1]` holds for every k = 0..10 (for k = 1
  the size-1 blocked mask is empty, so the cap point itself is counted in
  `avail`; subtracting those 91 self-counts gives 8,190 = 2·4,095).  This is a
  different arithmetic route to every size count (extension counting rather
  than child counting).
* **Frame construction** (`arcscan.c`, no DFS at all): the 42,456,960 ordered
  non-collinear quadruples give 1,769,040 4-caps (= frames/4!), and **every**
  4-cap has exactly 42 addable points (the addable histogram is a single
  spike), so #5-caps = 1,769,040·42/5 = **14,859,936** — both 4- and 5-cap
  counts confirmed without the census walk.  (42 addable points per 4-arc is
  the expected PGL-transitivity of quadrangles.)
* **Order independence**: a random relabeling of the 91 points (seed 12345,
  `permute_board.py`) changes the whole DFS traversal order; the census gives
  *identical* counts on all 39 statistics (`cnt`, `max1`, `max2`), including
  128,917,712 total and 8,095,464 maximal.  No order-dependent artifact.
* Low sizes also agree with closed formulas: C(91,2) = 4,095 for 2-caps;
  C(91,3) − 91·C(10,3) = 110,565 for 3-caps; 91·90·81·64/4! = 1,769,040 for
  4-caps.

## Task 3 — two maximality tests

Both tests are evaluated for **every one of the 128,917,712 caps**, and they
agree on every single one (`max1 == max2` for all sizes; `out/checks.json`
`max_tests_agree: true`):

1. **blocked / addable-mask test** — `blocked` = union of the secant lines;
   the cap is maximal iff `~blocked == 0`.  This is the same structure the DFS
   descends by, so it costs nothing.
2. **secant-through-the-outside-point test** — for every point q outside the
   cap, q is addable iff q lies on *no* secant of the cap; implemented as
   "s ↦ line(q,s) is injective on the cap".  `maximal2()` never looks at
   `blocked`; it re-derives addability point by point (O(|cap|²) per outside
   point, early exit once an addable point is found).

Results: sizes 6, 7, 8, 10 maximal; **no maximal 9-cap** (and no maximal
0..5-cap).  Counts as in the table above.  In particular:

* size 6: 707,616 = 52,009,776 − 51,302,160 non-maximal 6-caps;
* size 7: 2,021,760;
* size 8: 5,307,120 = 7,960,680 − 2,653,560 (and 2,653,560 = 58,968·45, see Task 4);
* size 10: 58,968 = **all** 10-caps (every conic is maximal; see Task 4);
* size 9: 0 maximal — independently, every 9-cap is a 9-subset of a conic and
  the conic's 10th point is addable (set equality in Task 4 plus the 50
  samples), so 9-caps are never maximal.

The 10-caps maximality was also proved structurally without the census:
for all 58,968 conics the union of the 45 secants covers **all 81 outside
points**, so no point can be added.

## Task 4 — structural identities

`conics.py`: conics of PG(2,9) are enumerated from scratch as zero sets of
non-degenerate quadratic forms, i.e. symmetric 3×3 matrices over GF(9) up to
scalar (6 coefficients, leading coefficient normalised to 1):

```
canonical form classes       66,430 = (9⁶−1)/8
non-degenerate classes       58,968 = 9⁵ − 9²      <- claimed conic count
degenerate classes            7,462
distinct conic point sets    58,968 (no two forms share a point set)
every conic is a 10-cap; per conic: 10 tangents, 45 secants, 36 exterior lines
```

Every conic was then mapped to board labels through the Task-1 isomorphism and
the resulting mask sets compared with the census dumps (`setcmp.exe`, 128-bit
masks, sort + dedupe, exact set equality):

| comparison | census | conic-derived | raw / distinct | set equality |
|---|---|---:|---:|---|
| 10-caps vs conics | 58,968 | 58,968 | 58,968 / 58,968 | **YES** (onlyA 0, onlyB 0) |
| 9-caps vs 9-subsets of conics | 589,680 | 589,680 | 589,680 / 589,680 | **YES** |
| non-maximal 8-caps vs 8-subsets of conics | 2,653,560 | 2,653,560 | 2,653,560 / 2,653,560 | **YES** |

Consequences (all proved by set equality, not by sampling):

* 10-caps = conics, count 9⁵−9² = 58,968, all maximal.
* every 9-cap is contained in a conic and the 589,680 9-subsets of the 58,968
  conics are all distinct, so each 9-cap lies in **exactly one** conic and has
  exactly one addable point (the missing conic point).  Hence
  9-caps = 58,968·10 and no 9-cap is maximal.
* the 2,653,560 8-subsets of conics are distinct and equal (as a set) to the
  non-maximal 8-caps, so each non-maximal 8-cap lies in exactly one conic and
  is exactly a conic minus 2 points; non-max-8 = 58,968·C(10,8) = 2,653,560.
* maximal 8-caps = 7,960,680 − 2,653,560 = 5,307,120.

### Parity and the Grundy consequence

Maximal sizes and parities: 6 even, 7 **odd**, 8 even, 10 even → **mixed
parity**, as claimed.  By the repo's parity characterization (K1298: all
Grundy values in {0,1} ⇔ all maximal safe sets have one parity — quoted, not
re-proved here) mixed parity implies that some position has Grundy ≥ 2.

Because a theorem citation is weaker than a computation, I also produced a
**direct witness** (`grundy_witness.py`): take the 4-cap S = {0,1,10,20},
whose maximal extensions already have mixed parity (sizes 6, 7, 8, 10).
Enumerate the *entire* residual game under S (all 1,868 caps containing S),
compute every Grundy value bottom-up, and:

```
residue of S = {0,1,10,20}:  1,868 positions, maximal extension sizes {6,7,8,10}
Grundy distribution: {0: 684, 1: 1064, 2: 120},   max = 2
witness position {0,1,10,20,32,39} has Grundy value 2
```

The game tree below a position only contains supersets of it, so this is the
true Grundy value of that position in the full game: **Grundy ≥ 2 exists,
demonstrated explicitly** (not merely inferred).  As a cross-check of the
Grundy implementation, K1298's formula `G(T) = (p − |T|) mod 2` was tested on
the 1,717 positions of this residue whose reachable maximal extensions have a
single parity: **0 violations** (the other 151 positions have mixed-completion
parity, where the formula does not apply).

## Task 5 — sampled caps

`verify_samples.py` reads 50 reservoir-sampled caps per class (fixed-seed
xorshift64 reservoir inside the C census, `out/samp_*.txt`) and re-verifies
them with an independent Python implementation, using **two formulations of
addability** that must agree (`secant-line union` and `injective pencil`):

| class | sampled | size | addable points observed | expected | verified |
|---|---:|---:|---|---:|---:|
| 9-caps | 50 | 9 | exactly 1 (the conic's 10th point; S+q is a census 10-cap and maximal) | 1 | 50/50 |
| maximal 6-caps | 50 | 6 | 0 | 0 | 50/50 |
| maximal 7-caps | 50 | 7 | 0 | 0 | 50/50 |
| maximal 8-caps | 50 | 8 | 0 | 0 | 50/50 |
| non-maximal 8-caps | 50 | 8 | exactly 2 (the two missing conic points) | 2 | 50/50 |

All 250 caps pass the cap test, and the two addability computations agree on
every one of them (`out/task5_samples.json`, PASS).

---

## Notes, limitations, non-findings

* **No discrepancies.**  Every claimed number and identity was reproduced
  exactly.
* The census enumerator assumes the board's line list; the board axioms were
  verified in full (Task 1), so this is not a weak point.  The binary uses
  128-bit point masks, which covers all planes tested (n = 13, 31, 57, 73, 91).
* I did **not** recompute the full Grundy distribution of the 128.9M-position
  game (out of scope, and the parent states it as future work).  The claim
  "Grundy ≥ 2 exists" is now backed both by the parity theorem and by an
  explicit computed position with Grundy 2.
* The parity theorem K1298 itself is taken as quoted from
  `research/knowledge/items/K1298-parity-graded-grundy.md` (status: proved);
  its hypothesis (mixed maximal parity) and its local formula were checked
  here, its proof was not re-derived.
* One benign detail of my own internal cross-check (not a discrepancy in the
  claims): for 1-caps the blocked mask is empty, so "addable points" computed
  from the mask include the cap point itself; the enumerator never revisits it
  (candidates are restricted to points with larger index).  The edge/node
  identity is stated with that correction (8,281 − 91 = 8,190 = 2·4,095).
* `README.md`/`report.md` of the parent experiment state "所要は約 3 分"; my
  equivalent run takes 76 s, consistent in order of magnitude.

## File inventory

```
independent/
  pgcore.py             GF(q) + PG(2,q) construction, board I/O, axiom checks
  task1_board.py        Task 1 (axioms, GF(9) rebuild, isomorphism search)
  make_boards.py        PG(2,q) boards q=3,5,7,8,9
  capcensus.c           independent enumerator (two maximality tests, dumps, sampling)
  setcmp.c              exact binary mask-set comparison
  arcscan.c             frame-based independent 4/5-cap count
  conics.py             Task 4 (conics, subsets, board-label mapping)
  grundy_witness.py     exact Grundy of residual games, witness G = 2
  verify_samples.py     Task 5
  summarize.py          claimed vs observed, extension identity
  permute_board.py      relabeling for the order-independence run
  validate_reference.py reference distributions for q=3,5,7,8
  REPORT.md             this report
  out/                  all machine-readable results, dumps and logs
```
