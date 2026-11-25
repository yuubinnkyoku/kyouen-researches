# 2026-11-25 z=19 min>=14 (floor-14) pre-declaration census kit — exploration log

Lane: high-speed lane (this run). Status of this document: PRIMARY RECORD of
the pre-declaration census kit `research/experiments/strip-z19-min14-20261125/`.
No K slot is claimed, no universal statement is claimed. Everything below is
finite machine observation against the pinned raw engine, plus engine-free
closed-form pre-computations. The declaration lane (a later run) picks up from
here.

## 1. Context and trigger

The K1328 declaration note §5.1 registered the z=19 slice as the next primary
target (single-owner T-Z18 = K1328 in progress by its own lane; official runs
published at commit `6d40499c`):

- the z=19 min>=14 (floor-14) slice (T-Z19) pre-declaration census kit
  (13 rungs, Y >= 14) is the entry point;
- the F19f14 typology question: the alternation predicts hole+tail at odd z,
  with the supply datum to be taken from the MEASURED identity (the published
  z19 probe kit's tenth-tail identity: hold {0}∪{12..19}, uniform 0v1 break
  from s=20), NOT from the naive +2-shift prediction (already counterexampleed
  twice, at z=18 and z=19).

This run built and executed exactly that kit. No counter-publication of a
z=19-min14 census existed at push time (checked: no
`research/experiments/strip-z19-min14*` directory, no z=19 census log).

## 2. Kit construction (publish-then-execute, frozen before publication)

- `engine_block.py` — byte-clone of the published chain engine
  (sha256 `582c93c17bcd4fa618bfb74c733c3d679e197e8749ec4bbcc8821d3a6610d5c0`),
  fetched from the published z18-min13 kit (commit `f152a6f5`) and sha-verified
  before use. The embedded ENGINE_BLOCK startup pin `bd5f22e4…` is asserted by
  the script itself (engine_gate section, gate PASS in the frozen output).
- `explore_z19f14.py` (sha256
  `e41138e20d254922030c14b4bc07a06de838de9c51527967a3ec5029722ef325`)
  — adapted from the frozen published `explore_z18f13.py` (sha256
  `152fd2d8814f958e5aaef275f83b4abb1763b58929d375d7ec9cb864f2a94ff4`)
  by the disclosed textual diff (all changes machine-derivable from the
  published z18 kit; documented in the kit README):
  z 18→19; cell budget j+19→j+20; floor 13→14; rungs 12→13 with the
  provisional 13th-rank label `A7` (small token 13; FIFTH consecutive in-band
  base child, z*(13)=25>19); s domain {0}∪{14..44}; tail spots {45..52};
  strip sweep m∈{14..18}; strip spots m∈{19..22}; m=14 base spot (published
  z19 probe cross-check); below-band child H(20;Y;20) vs v(s,20,20);
  records: (d) m=13-row z=19 FIRST entry of the K1328 residual band
  m=13 z∈{19..24} in the published residual-band style (arity<=3 TOTAL)
  PLUS an arity<=4 co-token extension; (d2) m=12-row z=19 SECOND entry of
  the K1325 residual band m=12 z∈{18..21} in the SAME enumeration as the
  published z=18 entry; (d3) m=11-row z=19 THIRD entry of the K1322
  residual band m=11 z∈{17..20} in the SAME enumeration as the published
  z=17/z=18 entries; (g1) tenth-tail identity recheck v(s,20,20) vs
  v(s,19,20) over s∈{0}∪{12..56}; (g2) NEW eleventh-tail supply
  pre-computation v(s,21,21) vs v(s,20,21) over s∈{0}∪{12..56} with the
  predeclared candidate (break starts at s=20, constants not predeclared).
- Per-cell `H.cache_clear()` retained (z=13 shared-cache OOM lesson).
- Runtime ~19 s/run.

Determination protocol (frozen before the official runs, executed exactly):
default run + default re-run + PYTHONHASHSEED=1 same-cwd run + env -i
isolated-directory runs (explicit `/usr/local/bin/python3`, empty
environment). FIVE runs total were executed and all were byte-identical
(sha256
`3354dfc6c7f65dedc02aeb95fa257e8a19526e1a25fd45e040b287d9dd510f`, rc 0 each).
The frozen `explore_z19f14.out` IS that stdout.

Independent cross-check (same environment, not part of the frozen artifact):
the FULL census re-enumerated and re-evaluated with the ORDERED engine
(H_ordered) against the canonical engine: 1,521 cell shapes (all 13 cells ×
117), 104 tail spots, 230 strip shapes, 76+75+92+110 record shapes, 12 strip
spots, the base spot, 117 below-band shapes — 0 mismatches anywhere; every
frozen row (per-cell deviant lists, multivalue counts, shape counts,
separation lists, tail-spot rows, identity hold/break rows) reproduced
exactly.

## 3. Observations (all judgment-free)

### 3.1 Cell ladder (13 rungs, 117 shapes each, all s-only, multivalue 0)

Deviant position set = {14, 16, 18} ∪ {s>=20 (F tail)}; all deviant rows carry
`shapes: 1` (single decomposition class per in-window row) except the tail
rows at large s (multi-shape classes, listed explicitly in the .out).
Per-cell deviants (value vs published K0832 Sigma-collapse):

- F19f14: {18: DOWN 1 v 2, 19: HOLE (no row), 20..44: persistent tail UP 2 v 0}
  — the TENTH tail form, HOLE+TAIL: the z-relative profile is IDENTICAL to the
  z=15 (sixth) and z=17 (eighth) forms: DOWN:1 at z−1, hole at z, persistent
  UP:2 tail from z+1. Tail spots (45..52): F 8/8 mismatch (value 2 vs
  collapse 0); the other 96 rows match. The odd-z profile is now 3/3 odd
  slices; the typology alternation single@(even z)/hole+tail@(odd z) has
  FIVE consecutive consistent slices.
- G19f14: {18: DOWN 0 v 1}
- E19f14: {16: DOWN 1 v 2, 18: UP 2 v 0}
- D19f14: {16: DOWN 0 v 1}
- C19f14: {14: DOWN 1 v 2, 16: UP 2 v 0}
- B19f14: {14: DOWN 0 v 1}
- A19f14: {14: UP 2 v 0} — the FIRST A-rank deviant since z=17, at s=14 = z−5
  (the z=17 A break was at s=12 = z−5: same relative position)
- A2..A719f14: fully collapsed — SIX consecutive full collapses after the
  single A break. A7 (j=13, min=13) — the FIFTH consecutive in-band base
  child (z*(13)=25>19) — collapses over its full 117-shape domain: the T-Z19
  base m=14 trivial-absorption candidate.

Structure across positions: the ladder carries a repeating per-position
triplet {DOWN:1, DOWN:0, UP:2}:
- position 14: C DOWN:1, B DOWN:0, A UP:2;
- position 16: E DOWN:1, D DOWN:0, C UP:2;
- position 18: F DOWN:1, G DOWN:0, E UP:2;
- position 20+ (F only): persistent tail UP:2.
The triplet sits ONE RANK LOWER per position than at z=18 (z=18:
{D,C,B}@14, {G,E,D}@16, {F,G}@18 with triplet {DOWN:0, UP:1, UP:2}), and the
z=19 value multiset {DOWN:1, DOWN:0, UP:2} equals the z=17 base-position
triplet {C17f12 DOWN:1, B17f12 DOWN:0, A17f12 UP:2} exactly — the odd-z
ladder base triplet candidate now has 2/2 odd data points (z=17, z=19).
The full published z=18 deviant position set {14,16,18} survives floor 14
(all >= 14): the fourth consecutive floor shift triggers NO
definition-domain exclusion — contrast the z=17→z=18 shift (s=12 excluded).
No new position class appears in the census window besides the F tail.

### 3.2 Supply identities (engine-free, section g)

- TENTH-tail identity RECHECK (published z19 probe datum): v(s,20,20)=v(s,19,20)
  holds exactly on **{0}∪{12..19}**, breaks UNIFORMLY as 0-vs-1 for ALL
  s∈{20..56} (published over {0}∪{12..55}; rechecked and extended). The
  F19f14 hole sits at the identity's final hold point (s=19=z) and the tail
  starts exactly at the first break position (s=20) — supply-to-deviant
  alignment exact.
- ELEVENTH-tail identity (NEW): v(s,21,21)=v(s,20,21) holds exactly on
  **{0}∪{12..19}**, breaks at **s=20 as 0-vs-2**, then UNIFORMLY as **2-vs-1
  for ALL s∈{21..56}** — the EXACT z=18 even-z identity shape
  ({0v2@z, 2v1@(z+1)+}). Predeclared candidate "break starts at s=20"
  CONFIRMED; constants measured (not predeclared). The even-z supply-identity
  form now: z=16 uniform 1vs0 (published), z=18 and z=20 the {0v2@z +
  2v1@(z+1)+} form — 2/2 on the newest form. This is the z=20 slice's supply
  datum (z=20 census F-cell single-point candidate at s=20).

### 3.3 Strip and row records

- T-Z19 provisional claim position sweep m∈{14..18}: 230 shapes,
  **0 violations** (cumulative 68/123/167/202/230).
- m=13-row z=19 (R=33; K1328 residual band FIRST entry; published style):
  **76 shapes, 0 separations**; arity<=4 co-token extension: **75 shapes,
  0 separations** (75 = 76 − single-token row (13,): the co-token
  enumeration omits it and no arity-4 co-token shape fits S<=51; the
  relationship is machine-checked and analogous to the published z18 pair
  92/95, which additionally gained 4 arity-4 shapes in-domain); A719f14
  fully collapsed over its 117-shape domain → the T-Z19 base m=14 is the
  FIFTH consecutive trivial-absorption base candidate.
- m=12-row z=19 (R=32; K1325 residual band SECOND entry; SAME enumeration
  as the published z=18 record): **92 shapes, 0 separations**.
- m=11-row z=19 (R=31; K1322 residual band THIRD entry; SAME enumeration
  as the published z=17/z=18 records): **110 shapes, 0 separations**.
- Strip spots m∈{19..22}: 12/12 match.
- m=14 base spot H(34;(14,14);19) = 1 = v(28,19,34) — EXACTLY the published
  z19 probe value (cross-artifact consistency; base-spot sequence across
  floors 0/1/0/1 = four data points with the z=20 probe of this same session
  adding a fifth).
- Below-band child census H(20;Y;20) vs v(s,20,20): 117 shapes, **0
  deviants, 0 multivalue** — FIFTH consecutive full collapse of the
  below-band supply child.

## 4. Honest record (this run)

- All published bytes consumed during local build were fetched sha-pinned
  from the published kit commits (`f152a6f5` for engine_block.py +
  explore_z18f13.py; `9e955243` for the z19 probe README/log context), with
  the engine sha-verified (`582c93c1…`) before use.
- **Startup-pin defect caught and fixed before any run**: the first local
  build of the embedded ENGINE_BLOCK carried a leading
  `from functools import lru_cache` line (copied from the byte-clone
  engine_block.py FILE rather than the z18 script's embedded block, which
  starts at `def mex`), so the computed sha256 was `582c93c1…` ≠ PIN
  `bd5f22e4…` and the startup gate failed immediately with AssertionError
  before ANY computation. The block was corrected and re-verified
  (sha256 `bd5f22e4…`) before the first real run; the frozen .out is from
  the corrected script. The startup-pin gate did exactly its designed job.
- Section (d)/(d2)/(d3) enumeration styles follow the published
  residual-band style from the start (the z18 kit's own honest lesson);
  the arity<=4 version is kept as an explicitly labelled extension.
- The crosscheck script's identity comparison initially compared dict rows
  via positionally-guessed key indices and produced two false mismatch
  flags; fixed by explicit key names; recomputed MATCH on both identities.
  No frozen data was impacted (the frozen .out was never touched).
- A separate scratch verifier for the SAME SESSION's z=20 probe cross-check
  was OOM-killed once (rc 137, shared ordered-engine cache across records);
  resolved by per-S cache clearing in a per-record invoker. Not a census
  defect; recorded for the environment-facts file (memory ceiling is a
  real constraint of this sandbox, consistent with the published K1328
  check-machine OOM note).
- No wall-clock, no randomness, no hash-order dependence; the shape counts
  92/110 equal the published records' counts exactly because the
  enumerations are identical (machine-checked, not asserted).
- Push protocol: latest main re-fetched immediately before the push
  (hourly parallel-run hazard); the z19-min14 census slot confirmed
  unclaimed; kit + this log pushed in one commit; fetch-back byte
  verification to follow in the same session.

## 5. Handoff to the declaration lane

- The T-Z19 declaration dependencies are ALL published at push time: the
  K1328 item + completion log landed at `116e30b4` (the official runs had
  landed earlier at `6d40499c`). Child
  positions follow the engine rules exactly as in the K1322/K1325/K1328
  templates:
  - for the claim position H(m+20; X; 19) with min(X)=m>=14, the C-hand
    (z-decrement) child is H(m+19; X; 18) — the published T-Z18 claim
    position for min(X)=m>=14 (T-Z18 numbering R=m+19) and for the ladder
    rungs the published K1328 cells F18f13..A618f13;
  - the base claim position is H(34;{14}∪Y;19) (T-Z19 numbering R=m+20
    at m=14); its a=m child (token 14→13, R→33) is
    (33;{13}∪Y;19) = the A719f14 cell domain ITSELF (small token 13,
    z*(13)=25 > 19: the FIFTH consecutive in-band base child), fully
    collapsed over all 117 shapes in the frozen census; the m=13-row
    z=19 record (76 shapes by the published residual-band style + 75 by
    the arity<=4 co-token extension, 0 separations each) provides the
    row-style dossier over the same lattice position;
  - the j=13 rung A719f14's C-hand child is H(32;{13}∪Y;18) = the
    published T-Z18 m=13-row claim position EXACTLY (R=13+19=32,
    min(X)=13 inside T-Z18's universal domain min>=13): every rung's
    C-hand child lands on a published K1328 line (cell ladder floor 13,
    Y tokens >= 14 >= 13 — the same co-floor subset argument K1328 used
    against K1325).
- The supply story for the F19f14 tenth form must use the MEASURED
  tenth-tail identity (hold {0,12..19}, uniform 0v1 break s>=20) — the
  z19 probe's published datum, rechecked here — and the paper proof must
  reproduce the hole-at-s=19 (the identity's final hold point) / tail-from-
  s=20 (the first break position) alignment.
- The z=20 slice (floor-15) census entry point is next after T-Z19; its
  F-cell supply datum is the ELEVENTH-tail identity published here
  (0v2 break at s=20, uniform 2v1 from s=21) — even-z typology predicts a
  single-point F form at s=20; the z=20 F-cell census decides.
- The same session's z=20 beyond/frontier probe kit (published immediately
  after this kit) holds the z=20 base-spot value 0 (five-floor parity
  sequence), the m=11 residual band completion, and the twelfth-tail
  identity (z=21): the next-next slice's supply datum.

## 6. Standard caveats

Everything in this kit and log is FINITE machine observation against the
pinned raw engine, plus pure closed-form pre-computations for section (g).
Nothing here is a theorem; no universal statement is claimed; no verdict of
any game position is consumed. Standard 11×11 empty board, two-stone roots
{49,60}/{59,60}, S2 {59,60}, classes 1/2/4, and all central-reply roots:
all UNKNOWN, unchanged. The battery/spot counts are engine cross-checks,
not proof substitutes.
