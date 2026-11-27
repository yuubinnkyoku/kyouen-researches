# 2026-11-25 z=21 min>=16 (floor-16) pre-declaration census kit — exploration log

Lane: high-speed lane (this run). Status of this document: PRIMARY RECORD of
the pre-declaration census kit `research/experiments/strip-z21-min16-20261125/`.
No K slot is claimed, no universal statement is claimed. Everything below is
finite machine observation against the pinned raw engine, plus engine-free
closed-form pre-computations. The declaration lane (a later run) picks up from
here.

## 1. Context, prior-lane state and slot check

This is the SAME-SESSION second kit of this run: the z20-min15 census kit was
pushed first (commit `2cc16d34`), its fetch-back byte verification was then
completed in this session — all FIVE files (engine_block.py,
explore_z20f15.py, explore_z20f15.out, README.md, the z20 predecl log)
byte-identical between the pushed commit and the local kit copies, and the
K1330 (T-Z19) K item + completion log have landed (`2b1423eb`, checked).
Main tip at this kit's start: `2cc16d34` (this run's own z20 push); no other
lane pushed meanwhile.

No counter-publication of a z=21-min16 census existed at kit-build time
(checked: no `research/experiments/strip-z21-min16*` directory, no z=21 census
log; the published beyond_z20 probe kit `0906ff21` covers z=20 rows
m∈{8..13} and z=20 spots only; the z21 slice cell ladder, row records and the
fourteenth-tail pre-computation were all unmeasured).

## 2. Kit construction (publish-then-execute, frozen before publication)

- `engine_block.py` — byte-clone of the published chain engine (sha256
  `582c93c17bcd4fa618bfb74c733c3d679e197e8749ec4bbcc8821d3a6610d5c0`),
  copied from the local z20 kit directory (whose bytes were themselves
  fetch-back verified against `2cc16d34` minutes earlier) and sha-verified.
  The embedded ENGINE_BLOCK startup pin `bd5f22e4…` is asserted by the
  script itself (engine_gate PASS in the frozen output).
- `explore_z21f16.py` (sha256
  `edb31ad07c83f43cf742a3cf3b139edbe16f9c797d6ce606f475010d624c1a81`)
  — adapted from the frozen published `explore_z20f15.py` (sha256
  `d46483016507bbc6e99d778baa528a053e57b325ded3d236564355eee13a2897`, the
  local copy fetch-back verified identical to the published pin
  `2cc16d34` before the adaptation) by the disclosed textual diff:
  z 20→21; cell budget j+21→j+22; floor 15→16; rungs 14→15 with the
  provisional 15th-rank label `A9` (small token 15; z*(15)=29>21; SEVENTH
  consecutive in-band base child); s domain {0}∪{16..46}; tail spots
  {47..54}; strip sweep m∈{16..20}; strip spots m∈{21..24}; m=16 base spot
  (NEW measurement, candidate 1); below-band child H(22;Y;22) vs
  v(s,22,22); records: (d) m=15-row z=21 CANDIDATE FIRST entry of the
  future T-Z20 residual band m=15 z∈{21..28} (frontier z*(15)=29; band
  pending the T-Z20 declaration lane) in the published residual-band style
  (arity<=3 TOTAL) PLUS an arity<=4 co-token extension; (d2) m=14-row z=21
  SECOND entry of the K1330 published residual band m=14 z∈{20..25} (SAME
  enumeration -> same 62 shapes expected); (d3) m=13-row z=21 THIRD entry
  of the K1328 band m=13 z∈{19..24} (same 76); (d4) m=12-row z=21 FOURTH
  AND FINAL entry of the K1325 band m=12 z∈{18..21} (same 92; band closes
  if 0 seps); (g1) twelfth-tail identity recheck over s∈{0}∪{12..58};
  (g2) thirteenth-tail identity recheck over s∈{0}∪{12..58}; (g3) NEW
  fourteenth-tail supply pre-computation v(s,24,24) vs v(s,23,24) over
  s∈{0}∪{12..58} with BOTH break components predeclared (hold {0}∪{12..23},
  break start s=24=z+1 at z=23, shape UNIFORM 0v1 — the odd-z supply form
  being 2/2 at z=19/z=21, this is the first fully-predeclared odd-slice
  identity, the second fully-predeclared identity of the series after the
  thirteenth).
- THE FULL PREDECLARED CANDIDATE (in the file docstring, written before the
  first run): derived from the published z=19 odd profile (fetched from
  the published z19 kit commit `6a6832ce`, parsed, NOT recomputed — the
  z=19 frozen `explore_z19f14.out` deviant lists: F 18:DOWN:1v2 + tail
  20..44 UP:2v0; G 18:DOWN:0v1; E 16:DOWN:1v2 + 18:UP:2v0; D
  16:DOWN:0v1; C 14:DOWN:1v2 + 16:UP:2v0; B 14:DOWN:0v1; A 14:UP:2v0;
  A2..A7 collapsed; F tail spots 8/8 mismatch) shifted +2 in position:
  (i) deviant position set {16,18,20} inherited from z=20 (pair rule);
  (ii) station triplet {DOWN:1, DOWN:0, UP:2}: {C,B,A}@16, {E,D}@18,
  {F,G,E}@20; (iii) F twelfth-tail form: DOWN 1v2 at s=20=z−1, conforming
  HOLE at s=21=z, tail UP 2v0 for all s>=22 (window {22..46}, spots 8/8
  mismatch); (iv) A2..A9 fully collapsed; (v) all cells s-only;
  (vi) strip 0 violations; (vii) all row records 0 separations;
  (viii) below-band full collapse (SEVENTH consecutive); (ix) base spot
  candidate 1; (x) twelfth recheck exact as published; (xi) thirteenth
  recheck exact as published; (xii) fourteenth as in (g3).
- Per-cell `H.cache_clear()` retained (z=13 shared-cache OOM lesson).
- Runtime ~22 s/run (one rung and one row record deeper than the z20 kit).

Determination protocol (frozen before the official runs, executed exactly):
default run + default re-run ×2 + PYTHONHASHSEED=1 same-cwd run + env -i
isolated-directory runs (explicit `/usr/local/bin/python3`, empty
environment). SIX runs total were executed and all were byte-identical
(sha256
`10f94100eb6240a807a32ac5d0e91f532800f86320a64d40e3ae47891dd2f643`,
rc 0 each). The frozen `explore_z21f16.out` IS that stdout.

Independent cross-check (same environment, not part of the frozen artifact):
the FULL census re-enumerated and re-evaluated with the ORDERED engine
(`xcheck_z21f16.py`, H_ordered) against the frozen canonical-engine output:
1,440 cell shapes (all 15 cells × 96), 120 tail spots, 150 strip shapes,
50+49+62+76+92 record shapes, 12 strip spots, the base spot, 96 below-band
shapes, and ALL three identity sections compared as FULL rows (hold/break
VALUES included — stronger than the z20 xcheck, since the break-row value
columns differ between identities): **0 mismatches**; every frozen row
reproduced exactly. rc 0, ~36 s. Per-record cache clearing retained.

## 3. Observations (all judgment-free)

### 3.1 Cell ladder (15 rungs, 96 shapes each, all s-only, multivalue 0)

Deviant position set = **{16, 18, 20}** — the predeclared INHERIT candidate
(pair rule now 3/3 pairs: z16/z17 {12,14,16}, z18/z19 {14,16,18},
z20/z21 {16,18,20}). Per-cell deviants (value vs published K0832
Sigma-collapse), all exactly the +2 shift of the published z=19 profile:

- F21f16: {20: DOWN 1v2} + hole@21 (conforming) + tail {22..46}: UP 2v0 —
  the TWELFTH-tail hole+tail form, predeclared on every component. z=19
  analogue: DOWN@18, hole@19, tail 2v0@s>=20. The
  single@(even z)/hole+tail@(odd z) typology alternation: SEVEN consecutive
  consistent slices (z15..z21). Tail spots (47..54): F 8/8 mismatch, all
  other cells 112/112 match.
- G21f16: {20: DOWN 0v1}; E21f16: {18: DOWN 1v2, 20: UP 2v0};
  D21f16: {18: DOWN 0v1}; C21f16: {16: DOWN 1v2, 18: UP 2v0};
  B21f16: {16: DOWN 0v1}; A21f16: **{16: UP 2v0}**;
  A221f16..A921f16: fully collapsed (EIGHT consecutive full collapses
  past the A rung).
- **A21f16 UP 2v0 at s=16=z−5: the A-RANK BREAK REBIRTH, the parity-law
  candidate predeclared both in the z20 kit §5 and in this kit's docstring,
  CONFIRMED.** A-break series: 3/3 odd slices (z=17 s=12, z=19 s=14,
  z=21 s=16, all UP 2v0 at even s=z−5); even-slice exclusion mechanism:
  position z−5 is ODD at even z, and no odd-s deviant class exists in any
  published census of the series (A-break candidates 0/3 at even z; the
  z=18 and z=20 A-ranks are fully collapsed in the published censuses).
  The candidate law: A-break iff z odd, at s=z−5, UP 2v0 — now a
  3/3 odd + 0/3 even parity candidate.
- Station structure: the odd-z station triplet {DOWN:1, DOWN:0, UP:2} at
  {C,B,A}@16, {E,D}@18, {F,G,E}@20 — the EXACT +2 shift of the published
  z=19 stations ({C,B,A}@14, {E,D}@16, {F,G,E}@18), same rank heads
  (C j=5, E j=3, F j=1). Odd-z station form now 3/3 (z=17, z=19, z=21);
  the z=17 leg was verified directly against the published z17-min12 kit
  frozen output (commit `2c74f1c6`, fetched and parsed after this run's
  freeze, before this push): {C,B,A}@12 (C DOWN:1v2, B DOWN:0v1,
  A UP:2v0), {E,D}@14, {F,G,E}@16, F DOWN@16=z−1 + hole@17 + tail
  2v0@s>=18 — identical rank heads and constants, so the three odd
  slices are one +2-shift orbit of the SAME profile (9 class-positions
  + F structure, value-for-value);
  even-z station form {DOWN:0, UP:1, UP:2} 2/2 (z=18, z=20). The two
  parity-dual station forms and the +2 shift law together predict the
  ENTIRE z=22 ladder profile from z=20 (position set candidate {18,20,22}
  with the position-16 classes below floor 17 = the 5th definition-domain
  exclusion candidate, stations {D,C,B}@18, {G,E,D}@20, {F,G}@22, F single
  point UP 1v0@22, A..A9 all collapsed (z=22 even, z−5=17 odd class).
- A9 (j=15, min=15, z*(15)=29>21) — SEVENTH consecutive in-band base child,
  fully collapsed over its 96-shape domain: the T-Z21 base-m=16
  trivial-absorption candidate.

### 3.2 Supply identities (engine-free, section g)

- TWELFTH-tail identity RECHECK: v(s,22,22)=v(s,21,22) holds exactly on
  {0}∪{12..21}, uniform 0v1 break for ALL s∈{22..58} (published
  {0}∪{12..57} rechecked + extended by one). Alignment with the F21f16
  form: hole at the final hold (s=21), tail from the first break (s=22) —
  exact, the same alignment pattern as z=19.
- THIRTEENTH-tail identity RECHECK: v(s,23,23)=v(s,22,23) holds on
  {0}∪{12..21}, breaks 0v2 at s=22, uniformly 2v1 for ALL s∈{23..58} —
  the published z20 census values reproduced exactly, extended by one.
- FOURTEENTH-tail identity (NEW): v(s,24,24)=v(s,23,24) holds exactly on
  **{0}∪{12..23}**, breaks at **s=24 as 0v1**, then **uniformly 0v1 for ALL
  s∈{24..58}**. BOTH predeclared components CONFIRMED (break start
  s=24=z+1 at z=23; shape uniform 0v1). The odd-z supply-identity form is
  now 3/3 (z=19 tenth, z=21 twelfth, z=23 fourteenth) — the first
  odd-slice fully-predeclared-and-confirmed identity (second of the series
  overall, after the thirteenth). This is the z=23 slice's supply datum.

### 3.3 Strip and row records

- T-Z21 provisional claim position sweep m∈{16..20}: 150 shapes,
  **0 violations** (cumulative 44/79/107/130/150) — as predeclared.
- m=15-row z=21 (R=37; SEVENTH consecutive in-band base child; CANDIDATE
  FIRST entry of the future T-Z20 residual band m=15 z∈{21..28}, frontier
  z*(15)=29): **50 shapes, 0 separations**; arity<=4 co-token extension:
  **49 shapes, 0 separations**. (The 50/49 counts are new measured lattices
  at m=15 — the predeclaration promised 0 separations, not a count; the
  62-shape m=14-row and 92-shape m=12-row counts DID reproduce the
  published enumerations exactly.)
- m=14-row z=21 (R=36; K1330 residual band SECOND entry): **62 shapes,
  0 separations** — exactly the published z20 census entry count
  (cross-artifact shape-for-shape consistency machine-checked).
- m=13-row z=21 (R=35; K1328 residual band THIRD entry): **76 shapes,
  0 separations** — exactly the published entries.
- m=12-row z=21 (R=34; K1325 residual band FOURTH AND FINAL entry):
  **92 shapes, 0 separations** — the published m=12 residual band
  m=12 z∈{18..21} **CLOSES** at its frontier z*(12)=22 (z=18 92/0,
  z=19 92/0, z=20 92/0, z=21 92/0; second band closure of the series
  after K1322's m=11).
- Strip spots m∈{21..24}: 12/12 match.
- m=16 base spot H(38;(16,16);21) = **1** = v(32,21,38) — the predeclared
  candidate (base-spot z-parity sequence 0/1/0/1/0/1, SIX data points;
  z=22 candidate: 0).
- Below-band child census H(22;Y;22) vs v(s,22,22): 96 shapes, **0
  deviants, 0 multivalue — SEVENTH consecutive full collapse** of the
  below-band supply child.

## 4. Honest record (this run)

- All published bytes consumed during the build were either (a) the local
  z20 kit copies fetch-back verified byte-identical against `2cc16d34`
  minutes earlier in this same session (engine_block.py,
  explore_z20f15.py), or (b) fetched sha-pinned from the published z19 kit
  commit `6a6832ce` (explore_z19f14.out, parsed for the predeclaration
  constants). The engine was sha-verified (`582c93c1…`) before use; the
  adaptation source explore_z20f15.py was verified identical to the
  published pin `d4648301…` before the adaptation.
- **Predeclaration text gap (disclosed)**: the docstring's station
  enumeration listed TEN deviant classes and the measured profile has
  ELEVEN: C21f16's second deviant {18: UP 2v0} was not spelled out in the
  predeclared station list. The omission is a text gap in the docstring's
  (ii) clause, not a candidate failure: the same docstring derives its
  candidate from "the published z=19 odd profile shifted +2", and the
  published z=19 C-cell carries exactly two deviants
  (14: DOWN 1v2 + 16: UP 2v0), whose +2 shift is the measured C21f16 pair
  (16: DOWN 1v2 + 18: UP 2v0) class for class. The +2-shift law itself is
  UNBROKEN (11/11 classes matched the shift of the published z=19
  per-cell deviant lists).
- No wall-clock, no randomness, no hash-order dependence. The cell shape
  count 96 (vs z20's 105, z19's 117) is a domain artifact of the floor-16
  window {0}∪{16..46}, not a sweep defect. The strip total 150 (vs z20's
  185, z19's 230) likewise: the m∈{16..20} sweep at floor 16 enumerates
  fewer shapes than m∈{15..19} at floor 15.
- The ordered-engine cross-check ran clean on the first invocation
  (per-record cache clearing; no rc-137 event).
- Push protocol: latest main re-fetched immediately before the push (hourly
  parallel-run hazard); the z21-min16 census slot confirmed unclaimed;
  kit + this log pushed in one commit; fetch-back byte verification to
  follow in the same session (recorded below after completion).
- Session-level honesty note: this log and kit were built and executed
  in the same session as the z20 kit push; the z20 kit's own deferred
  fetch-back verification was completed BEFORE this kit was started, and
  the verification result is recorded in §1.
- Post-freeze verification fetch (disclosed): the published z17-min12
  kit frozen output (`2c74f1c6`, `explore_z17m12.out`) was fetched and
  parsed READ-ONLY after this kit's frozen runs, to verify the z=17 leg
  of the odd-z station triple. It did NOT feed the predeclaration (which
  derived only from the z=19 kit constants written into the docstring
  before the first run); the frozen artifact was not regenerated and the
  z17 values are cited only as post-freeze corroboration in §3.1 and the
  kit README.

## 5. Handoff to the declaration lane

- T-Z21 declaration dependencies (forward-looking; the T-Z20 declaration
  itself has NOT landed yet — its published inputs are the z20-min15
  census kit `2cc16d34` and the K1330 (T-Z19) chain `e07d8f3d` /
  `ca6d12bc` / `25aafdda` / `2b1423eb`): the T-Z21 claim positions are
  H(m+22; X; 21) with min(X)=m>=16, and the C-hand (z-decrement) children
  H(m+21; X; 20) have min(X)>=16 >= 15, i.e. they are co-floor subsets of
  the future T-Z20 universal claim domain (min>=15 at z=20) — the same
  co-floor subset argument K1330 used against K1328. The T-Z20 declaration
  lane must therefore complete before T-Z21's slot claim (its paper proof
  scaffolding expects the published T-Z20 lines; the interim strips
  m∈{16..19} at z=20 are already published as the z20 census strip sweep
  with 0 violations, and the m=20-row z=20 lattice is covered neither by
  the z20 census strip (m∈{15..19}) nor its spots beyond 3 shapes: if the
  T-Z21 declaration needs the m=20-row z=20 record before T-Z20 lands, it
  must sweep it itself).
- The base claim position is H(38;{16}∪Y;21) (T-Z21 numbering R=m+22 at
  m=16); its a=16 child (token 16→15, R→37) is (37;{15}∪Y;21) = the
  A921f16 cell domain ITSELF (small token 15, z*(15)=29>21;
  the SEVENTH consecutive in-band base child), fully collapsed over all
  96 shapes; the m=15-row z=21 record (50 shapes + 49 ext, 0 separations)
  provides the row-style dossier over the same lattice position, and is
  simultaneously the candidate FIRST entry of the future T-Z20 residual
  band m=15 z∈{21..28}.
- The j=15 rung A921f16's C-hand child is H(36;{15}∪Y;20) = a co-floor
  subset of the future T-Z20 m=15-row universal domain (z=20, min>=15).
- The supply story for the F21f16 twelfth form must use the MEASURED
  twelfth-tail identity (hold {0,12..21}, uniform 0v1@s>=22) — rechecked
  and extended here — and the paper proof must reproduce the
  hole-at-final-hold (s=21) / tail-from-first-break (s=22) alignment
  (the z=17/z=19 hole+tail proofs are the templates).
- The z=22 census question this kit raises for the next even slice:
  the position-set shift law predicts {18,20,22} (5th definition-domain
  exclusion candidate: the position-16 classes fall below floor 17), the
  F single-point form at s=22 (even-z single-point 4th instance), the
  even-z station identity with z=20 (stations {D,C,B}@18, {G,E,D}@20,
  {F,G}@22 — the +2 shift of the published z=20 stations, which would
  make the even-z station identity 3/3: z=18, z=20, z=22),
  A..A9 all collapsed (z=22 even, A-break position z−5=17 odd), base spot
  candidate 0 (seventh parity point), and the fifteenth-tail
  supply pre-computation v(s,25,25) vs v(s,24,25) with the predeclared
  even-z candidate (hold {0}∪{12..23}, 0v2@24, uniform 2v1 s>=25).

## 6. Standard caveats

Everything in this kit and log is FINITE machine observation against the
pinned raw engine, plus pure closed-form pre-computations for section (g).
Nothing here is a theorem; no universal statement is claimed; no verdict of
any game position is consumed. Standard 11×11 empty board, two-stone roots
{49,60}/{59,60}, S2 {59,60}, classes 1/2/4, and all central-reply roots:
all UNKNOWN, unchanged. The battery/spot counts are engine cross-checks,
not proof substitutes.
