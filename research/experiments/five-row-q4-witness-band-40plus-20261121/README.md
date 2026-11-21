# five-row q=4: witness band extended to m=40 by bounded-edit surgery (fixed-width lane)

Date of experiment: 2026-11-21 (surgery and criterion runs 17:2xZ-17:4xZ;
criterion/determinant verification re-executed after two execution-environment
resets, totals identical).

Lane: standard-rule fixed-width q=4 family, five-row band.
Single-owner declaration:
`research/log/2026-11-21-five-row-q4-witness-band-40plus-single-owner-note.md`
(commit `6604dbe2`, declared 2026-11-21T17:16Z at HEAD `047d3d51`).
Acceptance conditions of the declaration: independent verification by at least
two integer-implementation families, publication of the lower-bound update
only, the general upper bound T_5 = 567 unchanged.

## Results (machine-verified finite claims; no universal claim beyond them)

### 1. Frontier R(S) census of the published (5,4) band-top witnesses

`append_criterion.py` (exact Fraction circle equations, scan limit 200) on the
published witnesses of `four-six-row-q4-q5-band-extension-20261115`:

| witness | maxx | R(S) | first unblocked cell | witness widths |
|---|---|---|---|---|
| m=37 (rowY0, HVHV) | 36 | 37 | (37,0) | [37,37] |
| m=38 (HVHV) | 36 | 39 | (39,0) | [37,39] |
| m=39 (rowY1, HVHV) | 37 | 39 | (39,1) | [38,39] |

All three are safe (maxline=3, maxcirc=3) with complete old-column coverage.
None covers width 40, so m=40 was a genuine frontier of the band.

### 2. Bounded-edit surgery on the 5x40 board

`surgery.js` (deterministic, seedless, safe-integer canonical curve census)
from the 12 D4 images (id/H/V/HV) of the three published witnesses.
Stone-count conservation: at w=5, q=4, a def-mode witness has <= 14 stones
(15 stones saturate all rows to 3 and lose the deficiency), and every
published base has exactly 14 stones, so pure-add surgery is impossible;
edit budget: single-move, remove-2/add-1, remove-2/add-2.

- Single-move (2,604 candidates per base): 0 witnesses on all 12 bases.
- Remove-2/add-1: 0 witnesses on all 12 bases.
- Remove-2/add-2 (1,565,655 candidates per base): 16 witnesses per m=39-family
  base (id/H/V/HV), 0 from all m=37/m=38 bases.
- Total: **64 hits = 16 distinct stone sets x 4 D4 images each** (all 16
  orbits have size exactly 4; the 16 are pairwise distinct mod D4,
  re-counted independently in the session). All hits: kind rem2add2,
  14 stones, rows [3,2,3,3,3] (deficient row has 2), maxx in
  {31, 34 (x9), 35, 36 (x2), 37, 38, 39}, safe (maxline=maxcirc=3).
- Every hit was verified safe + maximal on the FULL 5x40 board at search
  time (all 186 empty cells blocked).

### 3. Independent verification of the 16 distinct sets (three systems)

1. `surgery.js` discovery-time check (safe-integer canonical line/circle
   census, membership `A*x+B*y+C+D*(x^2+y^2) === 0`).
2. `append_criterion.py` (Fraction circle equations): 16/16 safe,
   `old_uncovered=0`, free-append reach R=40, first unblocked cell (40,1)
   for every set. `witness_widths = [maxx+1, 40]` per set: the staircase is
   [32,40] (1 set, maxx=31), [35,40] (9 sets, maxx=34), [36,40],
   [37,40] (x2), [38,40], [39,40], [40,40].
3. `det_witness_verify.py` (new third implementation: 4x4 integer determinant
   degenerate-concyclicity via Leibniz expansion; a 4-set violates iff the
   determinant of [x, y, x^2+y^2, 1] vanishes): 16/16 safe+maximal at width
   40 (186 empty cells each). Positive control: the published m=38 witness
   at width 39 PASS. Negative tamper control: moving one stone fails loudly
   with the offending 4-set (rc=1).

Cross-implementation disagreement: none, on any of the 16 sets.

### 4. Band update

With the published witnesses at widths 5..39 (K1207 re-verified bank
m=5..36; the m=37/38/39 band-extension witnesses reconfirmed above), the
(5,4) def-mode witness band now includes m=40:

**M_{5,4} in [41, 567]** (lower bound = width 40 witnessed; upper bound
T_5 = 567 = B_max(5)+1 from the K1207 demand-supply inequality, unchanged).

Structure note: R(S)=40 for all 16 sets, so none of them extends to width 41
(each leaves exactly the free cell (40,1) unblocked); the frontier moves to
m=41. The single set with maxx=31 witnesses nine consecutive widths
32..40 on its own, the widest single-set staircase recorded for (5,4).

### 5. Six-row frontier R(S) census (same criterion, published witnesses)

Witnesses fetched back byte-exact from main (sources in `witnesses/`):

| band | witness source | maxx | R(S) | stop cell | witness widths | true frontier |
|---|---|---|---|---|---|---|
| (6,5) | K1201 records `s6x28q5_rowY0` | 23 | 28 | (28,0) | [24,28] | m=29 |
| (6,6) | K1201 records `s6x24q6_def` | 23 | 24 | (24,1) | [24,24] | m=25 |
| (6,7) | `six-row-q7-m21-class-split-20261114` `w67_21.json` | 19 | 21 | (21,2) | [20,21] | m=22 |

No published six-row frontier witness extends by even one width: all three
front lines are genuine (the (6,7) m=21 set additionally witnesses width 20,
already known). R(S)=m0 means only that *this set* stops at m0; nothing is
claimed about other candidate sets at the frontier.

## Honesty record

- Implementation bugs caught by cross-implementation comparison before any
  claim: (a) the local first draft of the reach convention; (b) `surgery.js`
  circle membership written `A*x+B*y+C === D*(x^2+y^2)` (correct:
  sum form `=== 0`), caught by the Fraction second implementation on cell
  (0,1) of the published m=39 witness; (c) `det_witness_verify.py` first
  draft mixed indices with points (fixed immediately, no published result
  was affected).
- Two execution-environment resets during the session. All artifacts here
  were regenerated deterministically after the resets: the surgery is
  seedless; criterion/determinant totals identical; scripts pinned by
  sha256 in `output/sha256s.txt`.
- **No completeness claim for m=40**: the search covers only the declared
  bounded-edit neighborhoods of the published m=37/38/39 witnesses on the
  5x40 board. The 16 sets are a machine-verified subset of the width-40
  witness population, not a census of it.
- **No claim at m=41+**: existence or absence of a width-41 witness is
  UNDETERMINED.
- `results/fixed-width/mwq_stabilization.csv` is NOT modified (K1201
  precedent); the band value is recorded here, in the session log, and in
  K1209.
- checked-counts / candidate counts / run seconds are evidence of machine
  effort, never wins or losses; the standard 11x11 empty board is untouched
  by this lane and remains UNKNOWN.

## Reproduction

```
node   scripts/surgery.js main 40        # 64 hits, surgery-main-m40.json
node   scripts/surgery.js control 39     # positive control, 5x39 board
python3 scripts/append_criterion.py 5 200 4 < witnesses/s5x39q4.json
jq -c '.[0]' output/distinct-m40-witnesses.json | python3 scripts/det_witness_verify.py 5 40
jq -c '.[3]' output/distinct-m40-witnesses.json | python3 scripts/append_criterion.py 5 200 4
python3 scripts/append_criterion.py 6 100 5 < witnesses/s6x28q5_rowY0.json   # six-row census
```

Outputs are in `output/`; every published file is pinned in
`output/sha256s.txt`. The published bytes were fetch-back verified
against the local artifacts after the push commits.

## Structure

```
README.md                                  this report
scripts/surgery.js                          surgery engine (Node, deterministic)
scripts/append_criterion.py                 Fraction free-append criterion (K0853 lineage)
scripts/det_witness_verify.py               4x4-determinant third verifier (new)
witnesses/s5x37q4.json                      published input witnesses (+ s5x38q4, s5x39q4)
witnesses/s6x28q5_rowY0.json                 six-row frontier witnesses (+ s6x24q6, s6x21q7)
output/surgery-main-m40.json                64 raw hits
output/surgery-main-m40.log                 per-base run log
output/surgery-control-m39.json             positive control (5x39 rediscovery)
output/distinct-m40-witnesses.json          the 16 distinct sets (mod D4)
output/criterion-published-frontier.txt     R(S) census of m=37/38/39
output/criterion-published-frontier-sixrow.txt  R(S) census of (6,5)/(6,6)/(6,7)
output/criterion-m40-witnesses.txt          criterion on the 16 sets
output/det-verify-m40.txt                   determinant verifier on the 16 sets
output/sha256s.txt                          pins of all files above
```
