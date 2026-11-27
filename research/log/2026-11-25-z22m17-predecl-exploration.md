# 2026-11-25 z=22 min>=17 (floor-17) pre-declaration census kit — exploration log

Lane: high-speed lane (this run). Status of this document: PRIMARY RECORD of
the pre-declaration census kit `research/experiments/strip-z22-min17-20261125/`.
No K slot is claimed, no universal statement is claimed. Everything below is
finite machine observation against the pinned raw engine, plus engine-free
closed-form pre-computations. The declaration lane (a later run) picks up from
here.

## 1. Context, prior-lane state and slot check

This is the SAME-SESSION THIRD kit of this run: the z20-min15 census kit was
pushed first (commit `2cc16d34`), then the z21-min16 census kit (commit
`8a106233`), and BOTH fetch-back byte verifications were completed in this
session before this kit was started — all FIVE z21 files (engine_block.py,
explore_z21f16.py, explore_z21f16.out, README.md, the z21 predecl log)
byte-identical between the pushed commit and the local kit copies; the z20
five likewise earlier. Main tip at this kit's start: `8a106233` (this run's
own z21 push; the separate K1331 PG(2,9) lane commit `1a6cd1ce` landed during
the z21 build with no path conflicts and is used by the PG lane only).

No counter-publication of a z=22-min17 census existed at kit-build time
(checked: no `research/experiments/strip-z22-min17*` directory; the published
kits cover z<=21; the z=22 slice cell ladder, row records, base spot and the
fifteenth-tail pre-computation were all unmeasured).

## 2. Kit construction (publish-then-execute, frozen before publication)

- `engine_block.py` — byte-clone of the published chain engine (sha256
  `582c93c17bcd4fa618bfb74c733c3d679e197e8749ec4bbcc8821d3a6610d5c0`),
  copied from the local z21 kit directory (whose bytes were themselves
  fetch-back verified against `8a106233` immediately before this kit's
  build) and sha-verified. The embedded ENGINE_BLOCK startup pin
  `bd5f22e4…` is asserted by the script itself (engine_gate PASS in the
  frozen output).
- `explore_z22f17.py` (sha256
  `9e8ab7073a5d9d119af7928a19953efa1ac409df15b5878c9dab473af2e5c3c9`)
  — adapted from the frozen published `explore_z21f16.py` (sha256
  `edb31ad07c83f43cf742a3cf3b139edbe16f9c797d6ce606f475010d624c1a81`,
  fetch-back verified against `8a106233` immediately before the
  adaptation) by the disclosed textual diff: z 21→22; cell budget
  j+22→j+23; floor 16→17; rungs 15→16 with the provisional 16th-rank label
  `A10` (small token 16; z*(16)=30>22; EIGHTH consecutive in-band base
  child); s domain {0}∪{17..47}; tail spots {48..55}; strip sweep
  m∈{17..21}; strip spots m∈{22..25}; m=17 base spot (NEW measurement,
  candidate 0); below-band child H(23;Y;23) vs v(s,23,23); records:
  (d) m=16-row z=22 CANDIDATE FIRST entry of the future T-Z21 residual
  band m=16 z∈{22..29} (frontier z*(16)=30; band pending the T-Z21
  declaration lane) in the published residual-band style (arity<=3 TOTAL)
  PLUS an arity<=4 co-token extension; (d2) m=15-row z=22 SECOND entry of
  the future T-Z20 residual band m=15 z∈{21..28} (SAME enumeration -> same
  50 shapes expected); (d3) m=14-row z=22 THIRD entry of the K1330
  published band m=14 z∈{20..25} (same 62); (d4) m=13-row z=22 FOURTH
  entry of the K1328 band m=13 z∈{19..24} (same 76); the m=12-row NOT
  swept (the K1325 band m=12 z∈{18..21} CLOSED at z=21); (g1)
  thirteenth-tail identity recheck over s∈{0}∪{12..59} (EXTENDED domain);
  (g2) fourteenth-tail identity recheck over s∈{0}∪{12..59}; (g3) NEW
  fifteenth-tail supply pre-computation v(s,25,25) vs v(s,24,25) over
  s∈{0}∪{12..59} with BOTH break components predeclared (the
  z=24-slice supply datum; even-z supply form being 3/3 at
  z=18/z=20/z=22, this is the first fully-predeclared even-slice
  identity, the third fully-predeclared identity of the series after the
  thirteenth and fourteenth).
- THE FULL PREDECLARED CANDIDATE (in the file docstring, written before the
  first run): derived from the published z=20 EVEN profile (the z20-min15
  census kit, commit `2cc16d34`, whose frozen deviant lists were fetch-back
  verified byte-identical against the push in this session) shifted +2 in
  position — WITH THE COMPLETE PER-CELL 8-CLASS DEVIANT LIST SPELLED OUT
  (the z21 C-cell disclosure lesson applied: F {22: UP 1v0} single point;
  G {20: DOWN 0v2, 22: UP 2v1}; E {20: UP 1v0}; D {18: DOWN 0v2,
  20: UP 2v1}; C {18: UP 1v0}; B {18: UP 2v1}; A..A10 all fully collapsed
  (z=22 even, would-be A-break position z−5=17 odd)), plus: (i) deviant
  position set candidate {18,20,22} = z=21's {16,18,20} shifted +2 with
  the position-16 classes falling below floor 17 (FIFTH definition-domain
  exclusion event); (ii) F single-point even form, tail spots 128/128
  match; (iii) all cells s-only; (iv) strip 0 violations; (v) all row
  records 0 separations; (vi) below-band EIGHTH consecutive full
  collapse; (vii) base spot 0 (seventh parity point); (viii)-(x) the
  three identity constants as published/predeclared.
- Per-cell `H.cache_clear()` retained (z=13 shared-cache OOM lesson).
- Runtime ~24 s/run (one rung deeper than the z21 kit, one s-step more per
  cell).

Determination protocol (frozen before the official runs, executed exactly):
default run + default re-run ×2 + PYTHONHASHSEED=1 same-cwd run + env -i
isolated-directory runs (explicit `/usr/local/bin/python3`, empty
environment). SIX runs total were executed and all were byte-identical
(sha256
`f16a87d447d61b631cca153665b4a577d844ab5fe96eb9f740a74e400c82c7ac`,
rc 0 each). The frozen `explore_z22f17.out` IS that stdout.

Independent cross-check (same environment, not part of the frozen artifact):
the FULL census re-enumerated and re-evaluated with the ORDERED engine
(`xcheck_z22f17.py`, H_ordered; sha256
`b362a1ca5d597de6b40b301726b4c3e00daa7ac8ea0a7a82afb49984086ac821`,
adapted from the z21 xcheck by the same disclosed diff) against the frozen
canonical-engine output: 1,408 cell shapes (all 16 cells × 88), 128 tail
spots, 125 strip shapes, 40+39+50+62+76 record shapes, 12 strip spots, the
base spot, 88 below-band shapes, and ALL identity hold/break rows compared
as FULL rows (values included): **0 mismatches**; every frozen row
reproduced exactly. rc 0, ~41 s. Per-record cache clearing retained.

## 3. Observations (all judgment-free)

### 3.1 Cell ladder (16 rungs, 88 shapes each, all s-only, multivalue 0)

Deviant position set = **{18, 20, 22}** — the predeclared candidate: the +2
shift of z=21's {16, 18, 20} with the position-16 classes (z=21's odd triplet
{C,B,A}@16 and the z=21 A-rank break rebirth at s=16) falling BELOW the
floor-17 domain — the FIFTH definition-domain exclusion event, exactly
predeclared. Per-cell deviants (value vs published K0832 Sigma-collapse),
the exact +2 shift of the published z=20 even profile:

- F22f17: **{22: UP 1v0}** — the single-point even form at s=22=z, NO hole,
  NO tail; conforms everywhere else. The single@(even z)/hole+tail@(odd z)
  typology alternation: **EIGHT consecutive consistent slices (z15..z22)**.
  Tail spots (48..55): **128/128 match, all 16 cells** (even-form
  signature, contrast z=21's F 8/8 mismatch).
- G22f17: {20: DOWN 0v2, 22: UP 2v1}; E22f17: {20: UP 1v0};
  D22f17: {18: DOWN 0v2, 20: UP 2v1}; C22f17: {18: UP 1v0};
  B22f17: {18: UP 2v1}; A22f17..A1022f17: fully collapsed.
- **THE FULL PREDECLARED 8-CLASS PER-CELL LIST HIT 8/8 WITH ZERO
  UNDISCLOSED CLASSES** — the first slice of the series whose complete
  per-cell predeclaration matched the measurement class for class
  (the z21 kit's one-class docstring gap did not recur). The even station
  structure {D,C,B}@18 → {G,E,D}@20 → {F,G}@22 (values DOWN 0v2 / UP 1v0 /
  UP 2v1 at consecutive even stations) is the exact +2 successor of the
  published z=20 stations {D,C,B}@16 → {G,E,D}@18 → {F,G}@20: the
  even→even full-profile +2-shift orbit is now value-exact on consecutive
  steps z=18→z=20→z=22 (3 slices), mirroring the odd orbit z=17→z=19→z=21
  verified value-exact by the z21 kit against the published z17 kit.
- **A22f17 FULLY COLLAPSED — the A-break extinction/rebirth alternation
  continues**: extinct at z=20, reborn at z=21 (s=16=z−5 UP 2v0), extinct
  again at z=22 (the would-be break position z−5=17 is an odd s; no odd-s
  A-rank deviant class has ever been observed in any published census).
  The even-z A-break exclusion mechanism is now 5/5 even slices
  (z=16..z=22 A-ranks all collapsed); the candidate law "A-break iff z odd,
  at s=z−5, UP 2v0" is now 3/3 odd + 0/5 even.
- A2..A10: NINE consecutive full collapses past the A-boundary rung.
- A10 (j=16, min=16, z*(16)=30>22) — EIGHTH consecutive in-band base child,
  fully collapsed over its 88-shape domain: the T-Z22 base-m=17
  trivial-absorption candidate.

### 3.2 Supply identities (engine-free, section g)

- THIRTEENTH-tail identity RECHECK: v(s,23,23)=v(s,22,23) holds exactly on
  {0}∪{12..21}, breaks 0v2 at s=22, uniformly 2v1 for ALL s∈{23..59}
  (published z20/z21 values reproduced, extended by one).
- FOURTEENTH-tail identity RECHECK: v(s,24,24)=v(s,23,24) holds exactly on
  {0}∪{12..23}, uniform 0v1 break for ALL s∈{24..59} (published z21 census
  constants reproduced, extended by one). The odd-z supply form is 3/3
  (z=19, z=21, z=23-supply).
- FIFTEENTH-tail identity (NEW): v(s,25,25)=v(s,24,25) holds exactly on
  **{0}∪{12..23}**, breaks at **s=24 as 0v2**, then **uniformly 2v1 for
  ALL s∈{25..59}**. BOTH predeclared components CONFIRMED (break start
  s=24=z at z=24; the 0v2-then-uniform-2v1 shape). The even-z
  supply-identity form is now **4/4** (z=18, z=20, z=22 measured; z=24
  closed-form pre-computed) — the first even-slice
  fully-predeclared-and-confirmed identity (third of the series overall,
  after the thirteenth and fourteenth). This is the z=24 slice's supply
  datum.

### 3.3 Strip and row records

- T-Z22 provisional claim position sweep m∈{17..21}: 125 shapes,
  **0 violations** (cumulative 35/63/86/106/125) — as predeclared.
- m=16-row z=22 (R=39; EIGHTH consecutive in-band base child; CANDIDATE
  FIRST entry of the future T-Z21 residual band m=16 z∈{22..29}, frontier
  z*(16)=30): **40 shapes, 0 separations**; arity<=4 co-token extension:
  **39 shapes, 0 separations**. (The 40/39 counts are new measured lattices
  at m=16 — the predeclaration promised 0 separations, not a count.)
- m=15-row z=22 (R=38; future T-Z20 residual band SECOND entry):
  **50 shapes, 0 separations** — exactly the published z21 census entry
  count (cross-artifact shape-for-shape consistency machine-checked).
- m=14-row z=22 (R=37; K1330 residual band THIRD entry): **62 shapes,
  0 separations** — exactly the published z20/z21 entries.
- m=13-row z=22 (R=36; K1328 residual band FOURTH entry): **76 shapes,
  0 separations** — exactly the published entries.
- Strip spots m∈{22..25}: 12/12 match.
- m=17 base spot H(40;(17,17);22) = **0**, conforming (= v(34,22,40)) —
  the predeclared candidate (base-spot z-parity sequence now
  0,1,0,1,0,1,0 over z∈{16..22}: SEVEN data points; z=23 candidate: 1).
- Below-band child census H(23;Y;23) vs v(s,23,23): 88 shapes, **0
  deviants, 0 multivalue — EIGHTH consecutive full collapse** of the
  below-band supply child.

## 4. Honest record (this run)

- All published bytes consumed during the build were the local z21 kit
  copies fetch-back verified byte-identical against `8a106233` immediately
  before this kit was started (engine_block.py, explore_z21f16.py); the
  predeclaration constants were taken from the published z=20 profile
  (kit `2cc16d34`, fetch-back verified in this session) and written into
  the docstring BEFORE the first run. The engine was sha-verified
  (`582c93c1…`) and the embedded block pin asserted (gate PASS) before
  use; the adaptation source was verified identical to the published pin
  `edb31ad0…` before the adaptation.
- **No predeclaration text gap this time**: the docstring spelled out the
  complete 8-class per-cell candidate list and the measurement produced
  exactly those 8 classes, no more (contrast the disclosed z21 one-class
  gap). The z=22 ladder is the first fully-closed pre→measure cycle of
  the series.
- No wall-clock, no randomness, no hash-order dependence. The cell shape
  count 88 (vs z21's 96, z20's 105) is a domain artifact of the floor-17
  window {0}∪{17..47}, not a sweep defect; the strip total 125 likewise.
- The ordered-engine cross-check ran clean on the first invocation
  (per-record cache clearing; no rc-137 event).
- Push protocol: latest main re-fetched immediately before the push (hourly
  parallel-run hazard); the z22-min17 census slot confirmed unclaimed;
  kit + this log pushed in one commit; fetch-back byte verification to
  follow in the same session.
- Session-level honesty note: this log and kit were built and executed in
  the same session as the z20 and z21 kit pushes; both earlier kits'
  deferred fetch-back verifications were completed BEFORE this kit was
  started, with results recorded in §1.

## 5. Handoff to the declaration lane

- T-Z22 declaration dependencies (forward-looking; neither T-Z20 nor
  T-Z21 declarations have landed — the published inputs so far are the
  z20/z21/z22 census kits and the K1330 (T-Z19) chain): the T-Z22 claim
  positions are H(m+23; X; 22) with min(X)=m>=17, and the C-hand
  (z-decrement) children H(m+22; X; 21) have min(X)>=17 >= 16, i.e. they
  are co-floor subsets of the future T-Z21 universal claim domain
  (min>=16 at z=21) — the same co-floor subset argument chain
  K1330→(T-Z20)→(T-Z21)→(T-Z22). The T-Z20 and T-Z21 declarations must
  therefore complete before T-Z22's slot claim.
- The base claim position is H(40;{17}∪Y;22) (T-Z22 numbering R=m+23 at
  m=17); its a=17 child (token 17→16, R→39) is (39;{16}∪Y;22) = the
  A1022f17-style A10 cell domain ITSELF (small token 16, z*(16)=30>22;
  the EIGHTH consecutive in-band base child), fully collapsed over all
  88 shapes; the m=16-row z=22 record (40 shapes + 39 ext, 0 separations)
  provides the row-style dossier over the same lattice position, and is
  simultaneously the candidate FIRST entry of the future T-Z21 residual
  band m=16 z∈{22..29}.
- The supply story for the F22f17 single-point form at z=22 (even) has no
  tail term; the fourteenth-tail (z=23-supply) and fifteenth-tail
  (z=24-supply) identities published/rechecked here are the forward
  supply datums for the z=23 and z=24 slices respectively.
- The z=23 census question this kit raises for the next odd slice: the
  position-set inherit candidate is {18,20,22} (the (even, following-odd)
  pair rule: no shift, no new exclusion at the odd step — z=22/z=23 would
  be the 4th pair), the F hole+tail odd form (DOWN 1v2 at s=22=z−1,
  conforming hole at s=23=z, persistent tail UP 2v0 for s>=24; tail spots
  8/8 mismatch candidate), the A-RANK BREAK REBIRTH candidate at s=18=z−5
  (UP 2v0; the 4/4 odd candidate), the odd station triplet
  {DOWN:1, DOWN:0, UP:2} as the +2 shift of the published z=21 odd
  stations ({E,D}@18, {F,G,E}@20, ... per the z=21 → z=23 +2 orbit),
  base spot candidate 1 (eighth parity point), below-band ninth
  consecutive collapse, and the sixteenth-tail supply pre-computation
  v(s,26,26) vs v(s,25,26) with the predeclared odd-z candidate
  (hold {0}∪{12..25}, break start s=26=z+1 at z=25, shape UNIFORM 0v1).
- The m=15-row z=23, m=14-row z=23 (FOURTH entry of K1330, band
  z∈{20..25}), m=13-row z=23 (FIFTH entry of K1328 m=13 z∈{19..24}) and
  m=16-row z=23 (SECOND entry of the future T-Z21 band m=16) records are
  the natural next row-record targets, plus the m=14-row band's remaining
  z=24, z=25 entries for K1330's closure at frontier z*(14)=26.

## 6. Standard caveats

Everything in this kit and log is FINITE machine observation against the
pinned raw engine, plus pure closed-form pre-computations for section (g).
Nothing here is a theorem; no universal statement is claimed; no verdict of
any game position is consumed. Standard 11×11 empty board, two-stone roots
{49,60}/{59,60}, S2 {59,60}, classes 1/2/4, and all central-reply roots:
all UNKNOWN, unchanged. The battery/spot counts are engine cross-checks,
not proof substitutes.
