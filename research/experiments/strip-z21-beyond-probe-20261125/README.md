# z21/z22 beyond-frontier probe kit (frozen)

This directory is the publish-then-execute PRIMARY RECORD for the
z=21/z=22 beyond/frontier spot-probe — the THIRD edition of the
beyond-probe series (after the published `strip-z19-beyond-probe-20261125`
and `strip-z20-beyond-probe-20261125` kits), and the discriminating
companion measurement of this run's z19-min13/z18-min12 census kits. No K
slot is claimed by this kit and no claim is made here: everything below is
finite machine observation against the pinned engine. No verdict is
consumed.

## Contents

- `engine_block.py` — sha256
  `582c93c17bcd4fa618bfb74c733c3d679e197e8749ec4bbcc8821d3a6610d5c0`
  (the pinned engine block, byte-identical to the K1282..K1335 chain; sha256
  of the embedded block itself is the startup pin `bd5f22e4…`).
- `beyond_z21.py` — sha256
  `945fda07b999ced47b7314cdfd051e099440168728e67e9131f5eb69f948e7da`
  (adapted from the frozen published `beyond_z20.py` `17974ab0…` by the
  disclosed scope: eight sections — m=11-row z=21 FRONTIER record (z*(11)=21
  by the published K1268 formula z*(m)=2m−2+(m mod 2)), m=12-row z=22
  FRONTIER record (z*(12)=22), m=10-row z=21 (+3 beyond), m=9-row z=21
  (+4 beyond), m=8-row z=21 (+7 beyond), m=11-row z=22 (FIRST beyond slice
  of the m=11 arc), the FIFTEENTH-tail supply identity recheck (k=24) over
  s∈{0}∪{12..60}, and the NEW engine-free SIXTEENTH-tail supply
  pre-computation (k=25) over s∈{0}∪{12..61}. All predeclared candidates
  are in the file docstring, written before the first run. Row-record
  style: arity<=4 total tokens, co-token m allowed, identical enumeration
  to the published frontier records.)
- `beyond_z21.out` — sha256
  `2854595747472b82ddc370431be2cd5712294afc4908f3468649ef6e036228dd`
  (the frozen stdout; deterministic — SIX runs: default ×3,
  PYTHONHASHSEED=1 same-cwd, env -i isolated dirs ×2 (explicit
  `/usr/local/bin/python3`), all byte-identical, rc 0, ~15 s per run;
  no randomness, no wall-clock, no hash-order dependence).

## What the probe recorded (observation, judgment-free; see the predecl log)

### Frontier slices (the m-row separations AT z=z*(m))

- **m=11-row z=21 FRONTIER (125 shapes): exactly ONE separation
  X=(11,12) UP 2v0 at S=23** — the predeclared odd-m frontier candidate
  CONFIRMED with the z=17 constants (m=9: (9,10) UP 2v0). The odd-m
  frontier rule is now **2/2**.
- **m=12-row z=22 FRONTIER (95 shapes): exactly ONE separation
  X=(12,12) UP 2v1 at S=24** — the predeclared even-m frontier candidate
  CONFIRMED with the z=18 constants (m=10: (10,10) UP 2v1). The even-m
  frontier rule is now **2/2**. This is simultaneously the m=12 arc's
  EXIT datum: the K1325 published residual band m=12 z∈{18..21} closed
  0-separation at z=21 in the z21 census kit, and the frontier separation
  at z=22 = z*(12) is where the quiet band ends.
- The four measured frontier separations (z=17/18/21/22) are singleton in
  every case; the candidate law "z*(m)=2m−2+(m mod 2) carries exactly one
  separation, singleton (m,m+1) UP 2v0 at odd m, singleton (m,m) UP 2v1
  at even m" is now a
  4/4 finite candidate (next testable: m=13 z=24, m=14 z=26).

### Beyond slices (arc continuation)

- **m=10-row z=21 (+3): 170 shapes, the (10,10) diagonal DIED (reabsorbed)
  and the z=20-born (10,12) FLIPPED DOWN 0v1** — singleton (10,12) DOWN
  0v1. The (8,8)-arc precedent (diagonal death at +3) held; the m=10 arc
  at z=21 structurally matches the m=8 arc at its singleton stage.
- **m=9-row z=21 (+4): 234 shapes, TWO separations: (9,12) DOWN 1v2 (flip
  from the z=20 UP 1v0) and (9,14) UP 2v0 BORN — a co-token-+2 birth
  continuing the m=9 arc's (9,12)-era, the first gap+5 birth ever observed
  (published births: gap+2 (8,10), gap+3 (9,12), gap+4 (8,12), gap+6
  (8,14))** — the intra-arc co-token +2 cadence (m=8: 10→12→14; m=9:
  12→14) survives as the organizing rule across both parities.
- **m=8-row z=21 (+7): 362 shapes, ONE separation: (8,14) DOWN 0v1** —
  the z=20 re-emergent pair {(8,12) DOWN 0v2, (8,14) UP 2v1} became a
  singleton: (8,12) reabsorbed, (8,14) flipped DOWN. The second
  post-re-emergence datum of the series (no second re-emergence event).
- **m=11-row z=22 (the FIRST beyond slice of the m=11 arc): 125 shapes,
  exactly ONE separation (11,12) UP 1v0** — the frontier separation DECAYED
  2v0→1v0 and PERSISTED, identical to the m=9 arc's z=17→18 decay. The
  +1-beyond rule candidate: odd-m arcs decay-persist (**2/2**: m=9, m=11),
  even-m arcs flip (**1/1**: m=10). The m=11 arc structure is now measured
  at every slice z∈{17..22}.

### Supply identities (engine-free, pure published K0832)

- FIFTEENTH-tail recheck (v(s,25,25) vs v(s,24,25)): holds exactly on
  {0}∪{12..23}, breaks 0v2 at s=24, uniformly 2v1 for ALL s∈{25..60} —
  the published z22-min17 census constants reproduced and extended by one.
- **SIXTEENTH-tail (NEW, k=25): v(s,26,26) vs v(s,25,26) holds exactly on
  {0}∪{12..25}, breaks UNIFORMLY 0v1 for ALL s∈{26..61}** — EXACTLY the
  predeclared candidate (K1334 theorem A k=25 odd instance, engine-free,
  machine-checked k<=140 at the theorem level; this is the measured
  z=25-slice supply datum, the odd-z supply form's fifth instance:
  z=17, z=19, z=21, z=23, z=25).

## Independent ordered-engine cross-check (outside the frozen artifact)

All SEVEN separation positions of the frozen output recomputed with the
independent H_ordered engine: **0 mismatches**
(`ordered_crosscheck_final.log`, 37/37 across this run's three kits).

## Honesty notes

- Everything is finite observation over the swept domains; the frontier
  parity rules, the +1-beyond rule and the co-token +2 cadence are FINITE
  CANDIDATES (4/4, 3 datums, 2 arcs), not theorems. No universal statement
  is claimed; no verdict of any game position is consumed. Standard 11×11
  empty board and all central-reply roots: UNKNOWN, unchanged. The heavy
  m=13/m=14 frontier tests (z=24/z=26) are left to a later run.
