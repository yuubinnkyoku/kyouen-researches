# 2026-11-25 z=19 min>=13 (floor-13) pre-declaration census kit — exploration log

Lane: high-speed lane (this run). Status of this document: PRIMARY RECORD of
the pre-declaration census kit `research/experiments/strip-z19-min13-20261125/`.
No K slot is claimed, no universal statement is claimed. Everything below is
finite machine observation against the pinned raw engine, plus engine-free
closed-form pre-computations. The declaration lane (a later run) picks up
from here (candidate T-Z19(min>=13)).

## 1. Context, prior-lane state and slot check

Floor-(z−6) series state at kit-build time: z=15 min>=9 (K1321, proved);
z=16 min>=10 (kit `059c531e`, the s=10 even-floor class REVIVAL); z=17
min>=11 (kit `82f98ef4`, the s=11 odd domain entry EMPTY — the first
odd-s datum); z=18 min>=12 UNMEASURED (built as this run's second kit);
z=19 min>=13 = THIS KIT (the second odd-s domain-entry test). The T-Z19
floor-14 chain (K1330) and the z19-min14 kit (`e07d8f3d` family) are the
floor-14 reference profiles. Main tip at build: `4761668e` (the z22-min17
census kit of the earlier same-lane session had landed at `115c0bb9`; no
floor-13 z=19 census existed anywhere: checked no
`research/experiments/strip-z19-min13*` directory and no z19m13 log).

## 2. Kit construction (publish-then-execute, frozen before publication)

- `engine_block.py` — byte-clone of the published chain engine (sha256
  `582c93c17bcd4fa618bfb74c733c3d679e197e8749ec4bbcc8821d3a6610d5c0`),
  sha-verified against the published kit chain; the embedded ENGINE_BLOCK
  startup pin `bd5f22e4…` is asserted by the script itself (engine_gate
  PASS in the frozen output).
- `explore_z19f13.py` (sha256
  `f83b7955ca59d4325cf077f6bea3fee47bd35637a10cd9859cd4231fcdc3ad0e`)
  — adapted from the frozen published `explore_z18f13.py`/`explore_z19f14.py`
  pattern by the disclosed diff: 14 floor-13 cells Cell_j(s) :=
  H(j+20;{j}∪Y;19) (Y>=13, s∈{0}∪{13..44}, arity<=4; provisional 14th-rung
  label A8, small token 14 — one rank beyond the published T-Z19 table),
  tail spots {45..52}, strip m∈{13..17} at the candidate T-Z19(min>=13)
  claim position (m=13 column NEW; m=14..17 re-measure the published
  z19f14 sweep), boundary s=13 special children (d1/d2/d3 — the three
  positions outside published cover), strip spots m∈{18..21}, the m=13 base
  spot, the below-band child census H(20;Y;20) vs v(s,20,20), and the
  TENTH-tail supply identity recheck (engine-free) over s∈{0}∪{12..56}.
- THE FULL PREDECLARED CANDIDATE (docstring (n1)-(n4), written before the
  first run): (n1) the full floor-14 deviant profile {14,16,18} ∪ {F tail
  s>=20} survives with NO s=13 class — the odd-s class absence candidate
  2/2; (n4) an ENGINE-FREE cascade (pure published K0832 closed form,
  `precascade.py`, no raw-engine values used) deriving rung-by-rung
  conform at j=1..12, the j=13 coincide-with-record CONFORM, and the SHARP
  j=14 OPEN CASE (two unknown children; conforms unless one injects
  exactly the value 1). Per-cell `H.cache_clear()` retained.
- Determination protocol (executed exactly): default run + default
  re-run ×2 + PYTHONHASHSEED=1 same-cwd + env -i isolated dirs ×2
  (explicit `/usr/local/bin/python3`). SIX runs, all byte-identical
  (sha256
  `4e9c668c711e9accf7beb6d75c526acc2eaad242c4bde5cfeda16c175d2db275`,
  rc 0, ~27-30 s each). The frozen `explore_z19f13.out` IS that stdout.
- Independent ordered-engine cross-check (outside the frozen artifact):
  16 key positions (the full deviant set of F/G/E/C/B/A, d1/d2/d3, the
  base spot, the A7/A8 rung rows) recomputed with H_ordered: 0 mismatches
  (part of the 37/37 three-kit crosscheck of this run).

## 3. Observations (all judgment-free)

- 14 cells, 149 shapes each, ALL s-only (multivalue 0).
- **NO s=13 class anywhere** — the (n1)/(n4) candidate CONFIRMED; the
  odd-s domain entry is EMPTY; the odd-s class absence rule is now 2/2
  (z=17 s=11, z=19 s=13), against the even-floor revival rule 3/3
  (z=16 s=10, z=18 s=12 — the latter engine-free-predeclared and confirmed
  in this run's z18-min12 kit).
- The deviant structure is EXACTLY the published floor-14 profile:
  F {18: DOWN 1v2} + hole@19 + tail UP 2v0 for s∈{20..44} (shape counts
  1..16 growing), tail spots 8/8 mismatch (F) vs 104/104 match (the other
  13 cells); G {18: DOWN 0v1}; E {16: DOWN 1v2, 18: UP 2v0}; D
  {16: DOWN 0v1}; C {14: DOWN 1v2, 16: UP 2v0}; B {14: DOWN 0v1}; A
  {14: UP 2v0}; A2..A8 fully collapsed. Station triplets
  {C,B,A}@14 / {E,D}@16 / {F,G,E}@18, values {DOWN:1, DOWN:0, UP:2} —
  identical rank heads and constants to the published z=17/z=19/z=21 odd
  slices: the z=19 ladder is profile-invariant under the floor 14→13 drop.
- Rungs 13/14 (A7/A8) FULLY COLLAPSED — the j=13 record-coincidence CONFORM
  and the SHARP j=14 OPEN CASE both resolved CONFORM. The two UNPUBLISHED
  boundary children measured: d2 H(33;{14,12};19) = 0 = collapse (the
  (i)-child injects 0, not the rung-breaking 1); d3 H(33;{14,13};18) = 1 =
  collapse (also a min-drop probe one above the proved T-Z18 m=13 claim
  position); d1 H(32;{13,12};19) = 1 = collapse, cross-artifact with the
  published m=12-row z=19 record member.
- Strip m∈{13..17}: 286 shapes, **0 violations** (84/152/207/251/286) —
  the m=13 column is the NEW candidate T-Z19(min>=13) base-claim dossier;
  m=14..17 columns reproduce the published z19f14 sweep.
- m=13 base spot H(33;(13,13);19) = 0 = collapse — the K1334 lemma-S
  candidate (13+1)%2 = 0 CONFIRMED. Strip spots m∈{18..21}: 12/12 match.
- Below-band child H(20;Y;20) vs v(s,20,20): 149 shapes, 0 deviants,
  0 multivalue (the floor-13 edition; s>0 trivially in the K1264 stair,
  s=0 the empty position — the universal statement belongs to the
  declaration lane).
- TENTH-tail recheck: hold {0}∪{12..19}, uniform 0v1 break s∈{20..56} —
  published z19 constants reproduced, extended.

## 4. Honest record (this run)

- The (n4) predeclaration was derived ENGINE-FREE from the published K0832
  closed form only (`precascade.py`, executed before the first frozen run);
  the frozen artifact then matched every component (no text gap, no
  undisclosed class).
- Crosscheck disclosure: this run's shared ordered-engine crosscheck
  script had an R-offset bug in its FIRST DRAFT for the z18-min12 rows
  (kit-2 cells mapped at R=j+20 instead of j+19); three rows printed FAIL
  against wrong-R expectations before the correction; after the fix all
  37 rows across the three kits pass. The kits' own frozen outputs were
  never affected (their internal R=j+19 was correct from the start).
- Push protocol: latest main re-fetched immediately before the push
  (hourly parallel-run hazard); the z19-min13 slot confirmed unclaimed.
- No wall-clock, no randomness, no hash-order dependence.

## 5. Handoff to the declaration lane

- The candidate T-Z19(min>=13) declaration now has all its published
  dependency rungs measured and conforming: the 14-cell ladder collapse
  (this kit), the strip m=13 dossier (84/0), the base spot (lemma-S),
  the boundary children (d1/d2/d3), the below-band child census, and the
  T-Z18 (floor-13) C-hand story (published kit). Discovering a proof
  structure, building the K-item and the verification machine, and running
  the official battery remain the declaration lane's work; nothing here
  claims the slot.
- The third odd-s domain-entry test (z=21 floor-15, s=15 entry) is the
  natural next datum for the floor-necessity rule candidate; the even side
  (z=20 floor-14, s=14 revival profile {B,A,A2}) is predicted by the 3/3
  even revival rule with the z=16/z=18 constants.

## 6. Standard caveats

Everything in this kit and log is FINITE machine observation against the
pinned raw engine, plus pure closed-form pre-computations for the identity
and cascade sections. Nothing here is a theorem; no universal statement is
claimed; no verdict of any game position is consumed. Standard 11×11 empty
board, two-stone roots {49,60}/{59,60}, S2 {59,60}, classes 1/2/4, and all
central-reply roots: all UNKNOWN, unchanged.
