# crossrun-z20-z21 verification kit (2026-11-25)

Post-publication, cross-run verification of the two same-day census kits:

- the z=20 min>=15 (floor-15) census kit
  `research/experiments/strip-z20-min15-20261125/` (commit `2cc16d34`,
  frozen stdout `explore_z20f15.out` sha256
  `09e9026a436bf25aed05eabaf3629975971bd320a4c4c5ce5da122239f19f789`),
- the z=21 min>=16 (floor-16) census kit
  `research/experiments/strip-z21-min16-20261125/` (commit `8a106233`,
  frozen stdout `explore_z21f16.out` sha256
  `10f94100eb6240a807a32ac5d0e91f532800f86320a64d40e3ae47891dd2f643`),

plus the engine-free base-spot lattice parity lemma recorded as the
provisionally numbered knowledge item
`research/knowledge/items/K1332-base-spot-lattice-parity-closed-form.md`
(the K number is provisional per the concurrent-lane numbering
convention; the repo currently carries two distinct items numbered
K1330, so integration-time renumbering is expected; K1332 was taken
after a direct path check showed K1331 already claimed by the PG(2,9)
lane despite a minutes-earlier code search returning zero hits).

## Why this kit exists (collision record)

This lane built a z=20 floor-15 census kit in parallel with the other
hourly execution of the same recurring task. Immediately before pushing,
the mandatory latest-main refetch found the SAME census already
published (`2cc16d34` at 19:08:02Z, then the z=21 census `8a106233` at
19:17:52Z). The duplicate push was CANCELLED (collision protocol; no z=20
kit file was pushed by this lane), and the local measurements were
retained and are published here instead as an INDEPENDENT re-measurement.
The z=21 side was re-derived FRESH in this session against the pinned
engine, and both censuses were compared row-by-row against the published
frozen outputs. All shared rows agree (details below). The full record is
in `research/log/2026-11-25-z20-z21-crossrun-verification.md`.

## Provenance and independence

- `verify_z21_indep.py` (sha256
  `43aa03b2998c9ebe64b3fffa216239f6d2feb23fb6e26afa94303bae5c30f775`) is
  adapted from this lane's OWN z20 explorer
  `z20_crossrun/explore_z20f15.py` (sha256
  `d4df9769a87d1b4a475a7e40e6e329fefa0c1fcc9784e8558c73dbe0515294ac`),
  which was itself adapted from the published z19 kit
  `explore_z19f14.py` (commit `6a6832ce`, sha256 `e41138e2...`). It was
  NOT derived from the published z20/z21 kit scripts (`2cc16d34` /
  `8a106233`): the two derivations share the published z19 ancestry, but
  every z21 parameter set (floor 16, cell budget R=j+22, s-domain
  {0} u {16..46}, tail spots {47..54}, strip m in {16..20}, spot m in
  {21..24}, base spot (38;(16,16);21), below-band (22;Y;22), record rows
  m in {15,14,13,12}, identity domains {0} u {12..58}) was re-derived in
  this session from the lattice law R=m+z+1 and the published series
  conventions, not copied from the published z21 script.
- The engine block embedded in `verify_z21_indep.py` is byte-identical
  to the published chain engine (startup pin
  `bd5f22e415a78368c9b798296bc84948d5637decbf3c21a92404d45fb12e3a92`,
  standalone file sha256
  `582c93c17bcd4fa618bfb74c733c3d679e197e8749ec4bbcc8821d3a6610d5c0`; a
  standalone copy is included here as `engine_block.py`), asserted at
  startup by the script itself (engine_gate PASS in the frozen output).
- Both published frozen outputs were fetched AFTER publication and
  saved locally with sha verification: the local copies are
  byte-identical to the published pins (z21:
  `10f94100...`; z20: `09e9026a...`). The comparisons ran against those
  byte-verified copies.

## Determinism

- `verify_z21_indep.py`: FOUR runs byte-identical (default x2,
  PYTHONHASHSEED=1 same-cwd, env -i isolated directory with explicit
  `/usr/local/bin/python3`), each rc 0. The frozen
  `verify_z21_indep.out` (sha256
  `07ef7cd4872033fb804fc66d726efce92dc1db7ded43fe75e0ea5234577601e6`)
  IS that stdout.
- `z20_crossrun/z20_run1.out` (sha256
  `3576d0d7819f82241e04ac8a32d1945ecbce1dcabdf4045a3d8edf2f9c284566`):
  FIVE runs byte-identical in this lane's earlier same-day session
  (default, re-run, PYTHONHASHSEED=1, env -i x2), plus an ordered-engine
  cross-check in that session (`z20_ordered.out`).

## Comparison protocol

Both compare scripts take optional argv `(mine, theirs)` and otherwise
default to this kit's file and the PUBLISHED frozen output at its repo
path. Comparison is FULL-VALUE row equality, not count-level: deviant
dicts (s / value / collapse / direction / shapes), multivalue rows, cell
shape counts, tail-spot and strip-spot rows (shape / value / collapse /
match), strip per-m cumulative rows, record shapes + separation lists,
base-spot fields, below-band fields, and identity hold/break rows with
BOTH closed-form values. Label / anchor prose differs by design
(independence) and is not compared.

### z=21 (`compare_z21.py`, stdout captured in `compare_z21.out`)

330 rows / 436 field checks / 0 mismatches, rc 0. Sections compared:

- engine gate pin;
- 15 cells F21f16..A921f16 (96 shapes each, arity 0..4, s in
  {0} u {16..46}): deviant lists reproduce exactly — F {s=20 DOWN 1v2,
  conforming hole at s=21, tail s in {22..46} UP 2v0 with the shape-count
  column 1,1,...,9}, G {20 DOWN 0v1}, E {18 DOWN 1v2, 20 UP 2v0},
  D {18 DOWN 0v1}, C {16 DOWN 1v2, 18 UP 2v0}, B {16 DOWN 0v1},
  A {16 UP 2v0} (the A-rank break rebirth at s=16=z-5),
  A2..A9 fully collapsed; multivalue 0 everywhere;
- 120 tail-spot rows {47..54}: F 8/8 mismatch (value 2 vs collapse 0),
  all other cells 112/112 match;
- strip m in {16..20}: cumulative 44/79/107/130/150 shapes,
  0 violations;
- row records (published residual-band style): m=15 50 shapes 0 seps
  (+ arity<=4 cotoken extension 49/0), m=14 62/0, m=13 76/0,
  m=12 92/0 (the K1325 m=12 band closure entry);
- 12 strip spots m in {21..24}, all match;
- base spot H(38;(16,16);21) = 1 = v(32,21,38);
- below-band H(22;Y;22) vs v(s,22,22): 96 shapes, 0 deviants,
  0 multivalue;
- all three identity sections as FULL rows over s in {0} u {12..58}:
  twelfth (hold {0} u {12..21}, uniform 0v1 break s>=22), thirteenth
  (hold {0} u {12..21}, 0v2 at s=22, uniform 2v1 s>=23), fourteenth
  (hold {0} u {12..23}, uniform 0v1 s>=24).

### z=20 (`compare_z20.py`, stdout captured in `compare_z20.out`)

242 rows / 335 field checks / 0 mismatches, rc 0. Shared sections:
14 cells F20f15..A820f15 (105 shapes each), 112 tail spots
{46..53}, strip m in {15..19} (185 shapes, 0 violations,
cumulative 55/99/134/162/185), records m=14 62/0 (+ ext 61/0),
m=13 76/0, m=12 92/0, 12 strip spots {20..23}, base spot
H(36;(15,15);20) = 0 = v(30,20,36), below-band H(21;Y;21) 105/0/0,
and the eleventh + twelfth identity rows over the SHARED s-domain
{0} u {12..56} (the published kit extends its identity domains one step
further; those extra rows are outside this lane's z20 script and are
excluded from the count).

### Base-spot lattice parity (engine-free, NEW)

`verify_z21_indep.py` section (h) machine-checks, over z in
{11..200}, the closed-form lemma v(2z-10; z; 2z-4) = z (mod 2) with all
four K0832 branch invariants recorded per row: 190/190 consistent rows,
0 mismatches. The six published base-spot points z=16..21
(0/1/0/1/0/1) all sit on this collapse parity. Record and proof:
knowledge item K1332 (provisional number) and the log.

## Files

| file | role | sha256 |
|---|---|---|
| verify_z21_indep.py | verifier | 43aa03b2... |
| verify_z21_indep.out | data (frozen) | 07ef7cd4... |
| compare_z21.py | verifier | 008232f4... |
| compare_z21.out | data | 6812a61f... |
| compare_z20.py | verifier | 905b1165... |
| compare_z20.out | data | 0c1865cc... |
| z20_crossrun/explore_z20f15.py | data (this lane's own z20 script) | d4df9769... |
| z20_crossrun/z20_run1.out | data (frozen) | 3576d0d7... |
| engine_block.py | data (chain engine standalone) | 582c93c1... |

## Caveats

Everything here is finite machine observation (against the pinned raw
engine) plus pure closed-form checks. Nothing in this kit is a theorem;
no universal statement is claimed beyond the K0832-derived parity lemma
recorded in K1332; no verdict of any game position is consumed. Standard
11x11 empty board, two-stone roots {49,60}/{59,60}, S2 {59,60}, classes
1/2/4, and all central-reply roots: all UNKNOWN, unchanged. The
verification is cross-run and post-publication (same remote sandbox
environment class as the publishing run's, fresh session and fresh
derivation); it is not a third-party hardware verification.
