# (4,4) m=35/36 bounded-neighborhood witness engine and its validation battery (part 2 of the four-row q4 m35 lane)

Date of experiment: 2026-11-21
Lane: standard-rule fixed-width q=4 family, declared in
`research/log/2026-11-21-four-row-q4-m35-witness-hunt-counting-single-owner-note.md`
(commit `a423c2f01c4e23874a2bf668cfa019bc244d188d`). Part 1 (counting-class
tables, verifier, C1-C4) is
`research/experiments/four-row-q4-m35-witness-hunt-counting-20261121/`
(K1207). THIS directory is part 2: the Node.js bounded-neighborhood witness
engine and, in this first commit, its full validation battery. The m=35/36
hunt runs themselves are executed with this engine and their ledgers and
summaries are pushed in later commits of this directory; this commit makes
**no absence or existence claim at (4,4) m=35 or m=36**.

## What the engine searches

- **Bases**: all published (4,4) def-mode witnesses m=4..34
  (`input/witnesses_44_m4_34.json`, byte-identical copy of the part-1 pinned
  snapshot; 31 records, 28 distinct stone sets: m=29,31,33 duplicate the
  stone sets of m=28,30,32).
- **Placements**: each base is placed into the 4 x m board by the 4
  reflections (x -> -x, y -> -y) with all translations that keep it inside;
  images that coincide as cell sets are deduplicated.
- **Neighborhood of one placement**: removals R of at most 2 base stones
  (every subset of size 0,1,2 exactly once), then additions A of at most 2
  stones. The **target set of one placement** is

      T = { S-R+A : |R| <= 2, |A| <= 2, S-R+A is a witness },

  where *witness* means: SAFE (no 4 stones on a common line or circle),
  MAXIMAL (every free cell lies on a curve carrying exactly 3 stones),
  row-DEFICIENT (some row holds <= 2 stones), and its capped class
  (per-row counts min(3,r), sorted) is ALIVE at the board m, i.e. B >= m in
  the part-1 verified class table (15/34 classes alive at m=35 and m=36).
  Deliberately broader than "essential additions": maximality is preserved
  when adding further safe stones, so supersets of an A0 (R-exhausted)
  witness are also witnesses and are enumerated. The brute battery below
  enumerates exactly this same target set with no pruning, and the layered
  engine must match it exactly.

- **Layered completeness argument** (per R-config, U = free cells uncovered
  by S-R, i.e. not on any cnt==3 curve). A cell u in U ends up blocked in
  S-R+A iff (a) a stone lands on u, or (b) some added stone lies on a
  cnt==2 curve through u (2+1=3), or (c) both added stones lie on one
  cnt==1 curve through u (1+2=3). cnt==0 curves cannot reach 3 with <= 2
  stones. Singles are enumerated over all free cells a with
  vote(a)+coverExtra(a) >= |U| (distinct-u vote counting; the self-cover of
  a in U is credited exactly once). Pairs enumerate a1 over the helper pool
  of an anchor cell u* (free cells on cnt==2 curves through u*, free cells
  on cnt==1 curves through u*, plus u* itself: every covering pair for u*
  has an element there) and a2 over the per-u allowed-set intersection
  A1(u) n {u} n {free cells on cnt==1 curves through u that contain a1},
  taken over u in U not already covered by a1 alone (or equal to a1).
  The only pair prunes are witness-impossible cases: a stone on a cnt==3
  curve (unsafe in every extension), two stones sharing a cnt==2 curve
  (jointly unsafe), and single-nondef supersets (rows only grow). U==empty
  R-configs enumerate singles and pairs over all free cells so that
  extended witnesses (S-R plus one or two extra stones) are found. A dead
  R-config (some u with no A1, no P1, and u itself not even solo-safe) is
  abandoned for additions. Every accepted candidate passes `verifyConfig`
  (independent exact-integer recompute of safety, maximality, deficiency).

## Validation results (this commit)

Reproduce with the commands inside `output/validation_battery.log`.

**V1 (census anchors):** first-principles census build reproduces all 8
cases of the surgery cross-check pin, in particular
**(4,35,4): 413 lines + 41,194 circles = 41,607 curves**, (3,24,4): 3+6,410,
and both q=5 semantics cases. 8/8 PASS.

**V2 (published witnesses):** all 31 published (4,4) def-mode witnesses
m=4..34 re-verified on their own boards: header consistency, safety,
maximality, deficiency, row histogram, stone count, capped-class alive,
m <= B(class). 31/31 PASS. The m>=10 witnesses are all class (2,3,3,3);
m=4..9 are smaller classes.

**V3 (layered-vs-brute battery):** for 20 placements across boards
4x10 (bases m=9 and m=8, 8 placements; brute enumerated 25,490 (R,A) configs
per placement), 4x12 (bases 11,10; 6 placements; 51,821 configs), 4x14
(bases 13,12; 4 placements; 75,033 configs) and 4x16 (bases 13,12; 2
placements; 102,533 configs), the brute force enumerated every (R,A) pair
(|R|<=2, |A|<=2, no pruning, verifyConfig + class gate) and the witness
SETS were **identical to the layered engine's in all 20 placements**
(120-193 witnesses per placement at m=10, incl. extended witnesses).
ALL EQUIV; any DIFF would abort with exit 1.

**V4 (determinism caveat, honestly recorded):** this engine was rebuilt
byte-fresh in a fresh execution environment after a sandbox reset destroyed
the working tree mid-lane (the lost build had its own battery pass; nothing
from the lost build is cited as evidence). Everything claimed here is from
the current build, from the byte-pinned inputs, in this session. The
validation battery (V1-V3) is the acceptance gate for the rebuilt engine; no
hunt result is inherited from the lost build.

## Hunt runs (later commits)

`engine/hunt_driver.js` (default mode) runs the bounded-neighborhood hunt on
a target board with a resumable JSONL ledger (`--board`, `--base-min`,
`--budget-seconds`, `--ledger`). A completed negative run yields only the
finite local statement "no witness inside the enumerated neighborhoods";
absence at m=35 is NOT claimed unless a full class-split sweep closes it.

## Structure

```
README.md                                  (this report)
engine/hunt_44.js                          census, verifyConfig, placements, layered engine
engine/hunt_driver.js                      driver: --census-anchors / --verify-published / --battery / hunt
input/witnesses_44_m4_34.json              published witness snapshot (byte-copy of part-1 pin)
input/pin_census4_check_output.txt          published 8-case census pin (byte-copy of part-1 pin)
output/captable_q4.json                     verified class tables (byte-copy of part-1 output)
output/validation_battery.log               V1-V3 commands and outputs (this commit)
```

sha256 pins (of this commit's files):

- `engine/hunt_44.js` f18bef55053e310c2df147cdb5a3744bc67f303eed6d055c07106cb3fa02f108
- `engine/hunt_driver.js` cf4eb0042dc4242ba3cea64354fb13c8c839bf286afa9de7b5ad1425f47fafd2
- `input/witnesses_44_m4_34.json` 7689e4df99be22179ccd50c0c197cde2ad8d8d2dfe486212eef898a090dde1ae
- `input/pin_census4_check_output.txt` 8b841eb202f907683fcb9a5fbda43878cfbed280c662e754bda1573acd101d01
- `output/captable_q4.json` 5c749a5bcf76ac3632fd461f9085b8976cf4cb177033ae54cb73719277a6825e
- `output/validation_battery.log` a809d3d642a19542e4531042183443840681674d0f4ae08f7472df678f38d8b3

## What this is not

- No claim of witness existence or absence at (4,4) m=35/36: m=35 is
  UNDETERMINED. The bounded-neighborhood record is a finite local negative
  (or a witness for M_{4,4} >= 36) only, once the hunts are published.
- The m <= B(class) inequality is K1207's verified table used as proven
  input (alive-class gate B >= m); the engine certifies the enumeration, not
  the theory.
- The stalled `four-row-q4-m35-class-split-20261115` lane is another owner's
  IN FLIGHT work and is not touched. No kissat/SAT solving and no 11x11 work
  of any kind happens here; standard 11x11 root/first-move status is
  unaffected.
