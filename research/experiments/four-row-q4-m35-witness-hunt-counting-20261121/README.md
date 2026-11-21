# (4,4) m=35 witness hunt lane, part 1: w-general (q=4) counting-class tables w=3..7 and a fail-closed machine verifier

Date of experiment: 2026-11-21
Lane: standard-rule fixed-width q=4 family, declared in
`research/log/2026-11-21-four-row-q4-m35-witness-hunt-counting-single-owner-note.md`
(commit `a423c2f01c4e23874a2bf668cfa019bc244d188d`; declaration HEAD
`0a76535f98f9df883b376b2987fd44780b542fc3`). This directory is part 1 of the
lane: the counting-class theorem and verifier. The m=35/36 neighborhood
witness engine itself is planned as part 2 and is NOT run here; this part
makes no absence or existence claim at m=35.

## Claims

**C1 (class tables).** The K1202 blocking-counting mechanism, extended from
w=3 to w>=4 rows, yields for each multiset class of per-row stone counts
(r_1<=...<=r_w, entries 0..3, not all 3) a supply

  CAPS(r) = sum over non-horizontal stone triples T of
            sum_{i : r_i <= 2} max(0, 2 - u_i(T)),

and the demand/supply inequality for a row-deficient maximal safe
configuration on the w x m slab (K1202's theory, w-general form):

  d*m - sum_{i def} r_i  <=  CAPS(r),   d = #{i : r_i <= 2},

hence  m <= B(r) := (CAPS(r) + sum_def r_i) / d  (floored; B=0 iff the class
is impossible at every m for which the demand applies). For w>=4,
non-horizontal lines can also block (a line carries one point per row), but
the per-row coverage bound max(0, 2-u_i) is unchanged: a line meets a row
at most once and carries u_i = 0 on a deficient row's cells, a circle meets a
row in at most 2 points; 3-on-one-row triples (a full row's own horizontal
line) never cover deficient-row cells and are excluded. The complete tables
are published here: 34 classes (w=4), 55 (w=5), 83 (w=6), 119 (w=7); see
`output/captable_q4.json` (computed by `scripts/captable_q4.py`, two
implementations, assert-equal) and `input/expected_tables_w3_w7.json`
(byte-pinned expected value table for the verifier).

**C2 (upper bounds, self-contained second certificate).** The top class is
(2,3,3,3) for w=4 ((2,3^{w-1}) generally) with B = 236 / 566 / 1112 / 1928
for w = 4 / 5 / 6 / 7, hence

  M_{4,4} <= 237, M_{5,4} <= 567, M_{6,4} <= 1113, M_{7,4} <= 1929.

These match K0068's all-position parity thresholds T_w exactly
(B_max(w) + 1 = T_w for w = 3..7; w=3 verified against the K1202-published
w=3 table, top B=68, T_3=69). The counting-class route therefore re-derives
T_4..T_7 by a self-contained supply/demand computation, independent of
K0068's parity mechanism (and of K0318's curve-packing route, which gives the
same values). This is a certificate of already-published bounds, not an
improvement.

**C3 (band corollaries, new per-class resolution at depth).** For w=4 the
class table resolves which classes can host a maximal safe configuration at
a given m (class alive at threshold t iff B >= t), exact lists pinned and
machine-checked:

| threshold | alive classes at m >= t |
|---|---|
| 200 | (2,3,3,3) — single-deficiency monopoly above all others |
| 167 | + (1,3,3,3) |
| 163 | + (2,2,3,3) |
| 124 | + (0,3,3,3) |
| 113 | + (1,2,3,3) |
| 89  | + (2,2,2,3) |
| 73  | + (0,2,3,3), (1,1,3,3), (1,2,2,3) |
| 50  | + (2,2,2,2), (0,1,3,3) |
| 37  | + (0,2,2,3), (1,1,2,3), (1,2,2,2) |
| 36  | + (0,0,3,3) |
| 35  | same 15 classes as 36 |

At the (4,4) witness-band frontier: **at m=35 (and m=36) only 15 of the 34
classes are alive**, so any m=35/36 maximal safe witness must have row
profile among these 15 (the m=34 band witness is class (2,3,3,3)); at
m >= 200 the profile is forced to (2,3,3,3). These eliminations are ready
input for class-split sweeps: 19 of 34 classes can be skipped for any
future (4,4) m >= 35 work.

**C4 (independent machine verifier, fail-closed).**
`scripts/verify_counting_wq4_20261121.py` (stdlib only, deterministic,
exit 0 + `output/audit.json` only on full pass) recomputes everything from
byte-pinned inputs:

- g_pin: 7 input files sha256-pinned inside the verifier.
- g_census: an independent curve census (primitive-direction line
  enumeration including descending slopes; circles discovered as reduced
  integer circumcenters of point triples, concentric circles separated by
  the scaled squared radius) reproduces every published board census it is
  pinned to: all 8 cases of the four-row m35 surgery cross-check file
  (`pin_census4_check_output.txt`), including **(4,35,4): 413 lines +
  41,194 circles = 41,607 curves**, (3,24,4): 3 lines + 6,410 circles =
  6,413, and the q=5 semantics cases (4,10,5)=89, (4,20,5)=491; plus every
  record-embedded board census of the four pinned records banks (91 boards
  recomputed in full mode, 14 deferred boards with w*m>140 listed honestly
  in the audit with their published counts, self-consistency across
  duplicate records still checked).
- g_captable: CAPS computed by two structurally different implementations
  (A: closed-form sums over occupancy patterns {1,1,1} and {1,2}; B:
  literal enumeration of labeled stone triples) must agree for every class
  of every width, be invariant under all adjacent-transposition-generated
  row permutations, match the pinned expected tables for all classes of
  w=3..7, reproduce the K1202-published w=3 bounds (19 classes), reproduce
  the pinned top-class claims, and satisfy B_max+1 = T_w for w=3..7.
- g_witness: all **105 published def-mode witnesses** in the four pinned
  banks ((4,4) m=4..34, (5,4) m=5..36, (6,4) m=6..31, (4,5) m=5..20)
  re-verified with exact integer geometry: header consistency, in-bounds,
  no duplicate stones, claimed row histogram, safety (no q stones on any
  common line or circle), maximality (every free cell completes some q-curve
  through existing stones, lines and circles with canonical integer circle
  keys), and for q=4 the class inequality m <= B(class). The published
  extraction snapshot `witnesses_44_m4_34.json` is additionally checked to
  appear verbatim inside the pinned records.
- g_bands: the alive-class lists of C3 reproduced from the verified table;
  a deliberately wrong list must be rejected (in-run negative control).
- --tamper: corrupted table values, corrupted band list, corrupted census
  anchor and corrupted witness stones are each required to make the
  verifier fail; no audit is written in tamper mode.

Reproduction (`output/reproduction.log`): full run twice (second in an
isolated cwd) give identical content digests
`cd7631a5c05221da42b5789f16db1f2e2d6dc6c22c5cbd83c0a73f67cecd5c70`; a
PYTHONHASHSEED=random fast run reproduces the fast digest
`c253138f0168f461948a4b3971b807896427827fc33a52456c01d1cf1edcdf42`; the
class tables hash to table_digest
`55f9df703da68ba2eb283d3b44ac7565d2e7eb84dabdc4bd08c77faaf766a7e4`. Full
run ~136s, fast run ~5s, tamper ~6s (CPython 3.12.14, single process, no
network at runtime).

## What this is not

- No claim of witness existence or absence at (4,4) m=35 or 36: the
  neighborhood witness engine is part 2 of the lane and not run here. The
  m <= B(class) inequality is K1202's theory used as proven input; the
  verifier certifies its arithmetic (two implementations), its instances on
  all 105 published witnesses, and its corollaries — not the theory itself.
- The 34-class table enumerates profiles with entries 0..3, the K1202/SSOT
  convention (a row with >= 3 stones normalizes to 3); `defrows` = rows
  with <= 2 stones. Classes with no deficient row (all-3) have no bound and
  are out of scope by construction.
- The stalled `four-row-q4-m35-class-split-20261115` lane is another
  owner's IN FLIGHT work and is not touched; this lane only supplies the
  C3 pruning corollary for whoever runs such sweeps. No kissat/SAT solving
  and no 11x11 work of any kind happens here; standard 11x11 root/first-move
  status is unaffected.

## Structure

```
README.md                                  (this report)
scripts/verify_counting_wq4_20261121.py     fail-closed machine verifier (stdlib only)
scripts/captable_q4.py                      class-table producer (two impls, asserts)
input/expected_tables_w3_w7.json            pinned expected class tables (w=3..7)
input/pin_q4w4_records.jsonl                published (4,4) def-search records (32 lines)
input/pin_q4w5_records.jsonl               published (5,4) def-search records
input/pin_q4w6_records.jsonl               published (6,4) def-search records
input/pin_q5w4_records.jsonl               published (4,5) def-search records
input/pin_census4_check_output.txt         published 8-case census cross-check
input/witnesses_44_m4_34.json               published (4,4) witness extraction snapshot
output/audit.json                           full-mode audit (all gates PASS, digests inside)
output/reproduction.log                    battery: 2x full, hashseed-random fast, tamper
output/captable_q4.json                     computed class tables (w=3..7)
```

All seven input files carry their sha256 pins inside the verifier (g_pin);
every published file was copied verbatim from `main` at HEAD `0a76535f9...`
(records: `four-six-row-q4-q5-witness-search-20261114/output/.../records.jsonl`,
census check: `four-row-q4-m35-surgery-20261115/output/census4_check_output.txt`).

## Next steps (part 2 of the lane)

- Node.js neighborhood witness engine for (4,4) m=35 (then m=36): bases from
  the published m<=34 witnesses, translations and D4 images, essential-reduce
  layer composition, using C3's alive-15-class pruning and the canonical
  circle-key geometry validated here.
- Cross-reference from/toward the class-split sweep lane when it resumes:
  19 classes can be skipped for m >= 35 sweeps.
- If part 2 finds an m=35 witness: 3-system verification (Node BigInt +
  Python verifier geometry + published sat.js verifyConfig) as usual, and the
  witness band M_{4,4} >= 36 update; if the neighborhood prunes to empty, that
  remains a local negative only, no absence claim (m=35 UNDETERMINED unless a
  full class-split sweep closes it).
