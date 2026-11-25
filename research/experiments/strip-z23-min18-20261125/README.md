# z23-min18 pre-declaration exploration kit (frozen)

This directory is the publish-then-execute PRIMARY RECORD for the pre-declaration
census of the z=23 min>=18 (floor-18) slice — the next slice of the vertical-fiber
strip series after the z22-min17 census kit (`115c0bb9`) and the K1339 (T-Z22)
declaration chain. No K slot is claimed by this kit and no claim is made here:
everything below is machine observation. The declaration lane (this same
session's continuation, or a later run) picks up the slot claim, the paper
proof, the verification machine and the official runs.

## Contents

- `engine_block.py` — sha256 `582c93c17bcd4fa618bfb74c733c3d679e197e8749ec4bbcc8821d3a6610d5c0`
  (the pinned engine block, byte-identical to the K1282..K1339 chain; sha256 of the
  embedded block itself is the startup pin `bd5f22e4…`).
- `explore_z23f18.py` — sha256
  `eddd5e90825b0b38a51982ebd26e9e2e7a15390e0ae9916650dad7dddf8385f3`
  (adapted from the frozen published `explore_z22f17.py`
  `9e8ab7073a5d9d119af7928a19953efa1ac409df15b5878c9dab473af2e5c3c9` by the
  disclosed textual diff: z 22→23, cell budget j+23→j+24, floor 17→18, rungs
  16→17 with the provisional 17th-rank label `A11` (small token 17 — the NINTH
  consecutive in-band base child; z*(17)=33 > 23), s domain {0}∪{18..48},
  tail spots {49..56}, strip m∈{18..22} at the provisional T-Z23 claim
  position, an IN-BAND m=17-row record at z=23 (R=41, the T-Z23 base-child
  position AND the CANDIDATE FIRST entry of the future T-Z22 residual band
  m=17 z∈{23..32}, frontier z*(17)=33; published residual-band style arity<=3
  TOTAL, plus an arity<=4 co-token extension sweep), an IN-BAND m=16-row
  record at z=23 (R=40, the SECOND entry of the future T-Z21 residual band
  m=16 z∈{22..29}; same enumeration as the published z=22 census entry → same
  40 shapes, cross-artifact consistency), an IN-BAND m=15-row record at z=23
  (R=39, the THIRD entry of the future T-Z20 residual band m=15 z∈{21..28};
  same 50 shapes), an IN-BAND m=14-row record at z=23 (R=38, the FOURTH entry
  of the K1330 published residual band m=14 z∈{20..25}; same 62 shapes), an
  IN-BAND m=13-row record at z=23 (R=37, the FIFTH entry of the K1328
  published residual band m=13 z∈{19..24}; same 76 shapes), strip spots
  m∈{23..26}, the m=18 base spot (never measured by any published kit;
  candidate 1 from the base-spot z-parity sequence — the EIGHTH point), the
  below-band bottom-rung child census `H(24;Y;24)` vs `v(s,24,24)`, and
  section (g): the FOURTEENTH-tail supply identity RECHECK `v(s,24,24)` vs
  `v(s,23,24)` (the z=23 slice supply datum; published by the z21 census +
  z22 census kits; rechecked and extended over s∈{0}∪{12..60}), the
  FIFTEENTH-tail supply identity RECHECK `v(s,25,25)` vs `v(s,24,25)`
  (published by the z22 census kit; rechecked extended), plus the NEW
  engine-free SIXTEENTH-tail supply pre-computation `v(s,26,26)` vs
  `v(s,25,26)` with BOTH break components predeclared. The FULL predeclared
  per-cell deviant profile (derived from the published z=21 ODD profile
  (K1337 declared cells) shifted +2 — exactly the candidate registered in
  the z22-min17 predecl log §5 — with the complete 8-class deviant list
  spelled out per cell) is in the file docstring, written before the first
  run. The m=12-row is NOT swept (the K1325 band m=12 z∈{18..21} closed at
  z=21). Per-cell `H.cache_clear()` retained (z=13 shared-cache OOM lesson).
- `explore_z23f18.out` — sha256
  `bb456e85bdf248484bcf035ffd35c3bc39842f3524399851bc0e7c62f84834ca`
  (the frozen stdout; deterministic — SIX runs: default ×3, PYTHONHASHSEED=1
  same-cwd, env -i isolated dirs ×2, all byte-identical, rc 0, ~29 s per
  run; no randomness, no wall-clock, no hash-order dependence).

## What the census recorded (observation, judgment-free; see the predecl log)

- 17 floor-18 cells at z=23 (`Cell_j(s) := H(j+24;{j}∪Y;23)`, Y tokens >= 18):
  ALL cells s-only (multivalue rows 0) over 81 shapes each
  (s ∈ {0}∪{18..48}, arity 0..4). Deviant structure — the deviant position
  set is **{18, 20, 22}, IDENTICAL to z=22's {18, 20, 22} — the
  (even, following-odd) pair rule graduates to 4/4 with NO shift and NO
  definition-domain exclusion event** (z=22's classes all survive the
  floor-17→18 raise: the THIRD consecutive even→odd non-exclusion, after
  z=18→19 and z=20→21; contrast the odd→even steps z=19→20 and z=21→22
  which each killed the oldest z-relative class).
  - The FULL predeclared 8-class per-cell deviant list (written from the
    published z=21 odd profile +2, before the first run) hit **class for
    class, value for value, 8/8 with ZERO undisclosed extra classes**:
    **F23f18 {s=22 DOWN 1v2, s=23 conforming HOLE (the mirror 0 point),
    tail s>=24 UP 2v0}** (the FOURTEENTH tail form: odd-z HOLE+TAIL, the
    z-relative profile identical to z=15/z=17/z=19/z=21),
    **G23f18 {s=22 DOWN 0v1}**, **E23f18 {s=20 DOWN 1v2, s=22 UP 2v0}**,
    **D23f18 {s=20 DOWN 0v1}**, **C23f18 {s=18 DOWN 1v2, s=20 UP 2v0}**,
    **B23f18 {s=18 DOWN 0v1}**, **A23f18 {s=18 UP 2v0} = the A-RANK BREAK
    REBIRTH at s=18=z−5** (an even s at an odd z; the odd-z birth sequence
    is now **4/4**: z=17 s=12, z=19 s=14, z=21 s=16, z=23 s=18, all
    UP 2v0, the birth position z−5 always even — against the even-z
    annihilation 5/5). The odd station triplet
    {DOWN 1v2, DOWN 0v1, UP 2v0} at **{C,B,A}@18, {E,D,C}@20, {F,G,E}@22**
    (4/4 with z=17/z=19/z=21; the exact two-step successor of the z=21
    stations).
  - **F HOLE+TAIL form at z=23 (odd)**: the single@(even z)/hole+tail@(odd z)
    typology alternation reaches **NINE consecutive consistent slices
    (z15..z23)** (odd-z form 5/5, even-z form 4/4). Tail spots s∈{49..56}:
    **exactly the 8 F-cell spots mismatch (value 2 vs collapse 0), all other
    128 match** (the odd-form signature; contrast z=22's 128/128 all-match).
  - A223f18..A1123f18: fully collapsed — TEN consecutive full collapses past
    the A-boundary rung.
  - **A1123f18 (j=17, min=17, z*(17)=33 > 23) fully collapsed over its
    81-shape domain — the NINTH consecutive in-band base child** = the
    T-Z23 base-m=18 trivial-absorption candidate.
- Strip sweep at the provisional T-Z23 claim position m∈{18..22}:
  **108 shapes, 0 violations** (cumulative 28/51/71/90/108).
- m=17-row z=23 record (R=41; NINTH consecutive base child; candidate FIRST
  entry of the future T-Z22 residual band m=17 z∈{23..32}): **32 shapes,
  0 separations**; arity<=4 co-token extension: **31 shapes, 0 separations**.
- m=16-row z=23 record (R=40; future T-Z21 residual band SECOND entry):
  **40 shapes, 0 separations** — exactly the published z=22 census count
  (cross-artifact shape-for-shape consistency machine-checked).
- m=15-row z=23 record (R=39; future T-Z20 residual band THIRD entry):
  **50 shapes, 0 separations** — exactly the published z=21/z=22 entries.
- m=14-row z=23 record (R=38; K1330 residual band FOURTH entry):
  **62 shapes, 0 separations** — exactly the published entries.
- m=13-row z=23 record (R=37; K1328 residual band FIFTH entry):
  **76 shapes, 0 separations** — exactly the published entries.
- Strip spots m∈{23..26}: **12/12 match**.
- m=18 base spot `H(42;(18,18);23)` = **1**, conforming (= `v(36,23,42)`),
  the predeclared parity candidate; the base-spot z-parity sequence is now
  **0 (z16), 1 (z17), 0 (z18), 1 (z19), 0 (z20), 1 (z21), 0 (z22), 1 (z23)**
  — eight data points, alternating by z parity.
- Below-band child census `H(24;Y;24)` vs `v(s,24,24)`: 81 shapes,
  **0 deviants, 0 multivalue — NINTH consecutive full collapse** of the
  below-band supply child.
- FOURTEENTH-tail identity recheck: `v(s,24,24)=v(s,23,24)` holds exactly on
  **{0}∪{12..23}**, breaks uniformly (0,1) for all s∈{24..60} (published z21/z22
  census constants reproduced, extended by one; the odd-z supply form stays
  3/3 — this is the z=23 slice supply datum).
- FIFTEENTH-tail identity recheck: `v(s,25,25)=v(s,24,25)` holds exactly on
  **{0}∪{12..23}**, breaks at s=24 as 0v2, then uniformly 2v1 for all
  s∈{25..60} (published z22 census constants reproduced, extended by one;
  even-z supply form 4/4).
- **SIXTEENTH-tail identity (NEW)**: `v(s,26,26)=v(s,25,26)` holds exactly on
  **{0}∪{12..25}**, breaks **uniformly (0,1) for all s∈{26..60}** — BOTH
  predeclared components (hold domain AND the uniform 0v1 shape)
  **CONFIRMED**; the odd-z supply form graduates to 4/4
  (z=19, z=21, z=23, z=25-supply). This is the z=25 slice's supply datum.

## Independent ordered-engine cross-check (outside the frozen artifact)

The FULL census re-enumerated and re-evaluated with `H_ordered` against the
frozen canonical-engine output (`crosscheck_z23.py`, local to this session's
workspace): 1,377 cell shapes (17 cells × 81), 136 tail spots, 108 strip
shapes, 32+31+40+50+62+76 record shapes, 12 strip spots, the base spot, 81
below-band shapes, and ALL identity hold/break rows compared as full rows
(values included): **0 mismatches**; every frozen row reproduced exactly.
Per-record `H.cache_clear()` (published OOM lesson). rc 0, ~45 s.

See `research/log/2026-11-25-z23m18-predecl-exploration.md` for the
primary-source timeline and handoff instructions.

## Standard caveats

Everything in this kit is a FINITE machine observation against the pinned raw
engine. Nothing here is a theorem, nothing universal is claimed, and no verdict
of any game position (11x11 standard board, two-stone roots, S2, class 1/2/4 —
all UNKNOWN) is consumed. Battery/point counts are engine cross-checks, not
proofs. The paper proofs, the slot claim and the verification machine belong
to the declaration lane. Section (g) is a pure closed-form pre-computation: it
uses no engine recursion at all and inherits only the published K0832
single-token closed form.
