# 2026-11-25 z=20 min>=15 (floor-15) pre-declaration census kit — exploration log

Lane: high-speed lane (this run). Status of this document: PRIMARY RECORD of
the pre-declaration census kit `research/experiments/strip-z20-min15-20261125/`.
No K slot is claimed, no universal statement is claimed. Everything below is
finite machine observation against the pinned raw engine, plus engine-free
closed-form pre-computations. The declaration lane (a later run) picks up from
here.

## 1. Context and trigger

The z19-min14 census log §5 registered the z=20 slice (floor-15) as the next
census entry point after T-Z19, with the F-cell supply datum being the
ELEVENTH-tail identity (0v2 break at s=20, uniform 2v1 from s=21) and the
even-z typology predicting a single-point F form at s=20. The K1330 (T-Z19)
declaration lane completed its machine + official runs at `ca6d12bc` /
`25aafdda` (OFFICIAL-PASS, battery 16,267 pts, overall_bad 0) while this run
was building; the slot claim / declaration / machine / official runs all
belong to that lane and were not touched.

This run built and executed exactly the z=20 floor-15 census. No
counter-publication of a z=20-min15 census existed at push time (checked: no
`research/experiments/strip-z20-min15*` directory, no z=20 census log; the
published z20 beyond/frontier probe kit `0906ff21` covers row records at
z=20 for m∈{8..13} but not the 14-rung floor-15 cell ladder, the m=14-row
band entry, or the thirteenth-tail pre-computation).

## 2. Kit construction (publish-then-execute, frozen before publication)

- `engine_block.py` — byte-clone of the published chain engine
  (sha256 `582c93c17bcd4fa618bfb74c733c3d679e197e8749ec4bbcc8821d3a6610d5c0`),
  fetched from the published z19-min14 kit (commit `6a6832ce`) and
  sha-verified before use. The embedded ENGINE_BLOCK startup pin `bd5f22e4…`
  is asserted by the script itself (engine_gate section, gate PASS in the
  frozen output).
- `explore_z20f15.py` (sha256
  `d46483016507bbc6e99d778baa528a053e57b325ded3d236564355eee13a2897`)
  — adapted from the frozen published `explore_z19f14.py` (sha256
  `e41138e20d254922030c14b4bc07a06de838de9c51527967a3ec5029722ef325`)
  by the disclosed textual diff (all changes machine-derivable from the
  published z19 kit; documented in the kit README):
  z 19→20; cell budget j+20→j+21; floor 14→15; rungs 13→14 with the
  provisional 14th-rank label `A8` (small token 14; SIXTH consecutive
  in-band base child, z*(14)=26>20); s domain {0}∪{15..45}; tail spots
  {46..53}; strip sweep m∈{15..19}; strip spots m∈{20..23}; m=15 base spot
  (published z20 probe cross-check); below-band child H(21;Y;21) vs
  v(s,21,21); records: (d) m=14-row z=20 FIRST entry of the K1330 residual
  band m=14 z∈{20..25} in the published residual-band style (arity<=3
  TOTAL) PLUS an arity<=4 co-token extension; (d2) m=13-row z=20 SECOND
  entry of the K1328 residual band m=13 z∈{19..24} in the SAME enumeration
  as the published z19-census / z20-probe entries (cross-artifact
  consistency); (d3) m=12-row z=20 THIRD entry of the K1325 residual band
  m=12 z∈{18..21} in the SAME enumeration; (m=11 z=20 NOT re-swept: its
  K1322 band was closed by the published z20 probe kit); (g1) eleventh-tail
  identity recheck v(s,21,21) vs v(s,20,21) over s∈{0}∪{12..57}; (g2)
  twelfth-tail identity recheck v(s,22,22) vs v(s,21,22) over s∈{0}∪{12..57};
  (g3) NEW thirteenth-tail supply pre-computation v(s,23,23) vs v(s,22,23)
  over s∈{0}∪{12..57} with the predeclared candidate (break starts at s=22
  AND shape 0v2@22 + uniform 2v1@>=23; both components predeclared for the
  first time in the series after the 2/2 accumulation at z=18/z=20).
- Per-cell `H.cache_clear()` retained (z=13 shared-cache OOM lesson).
- Runtime ~21 s/run.

Determination protocol (frozen before the official runs, executed exactly):
default run + default re-run + PYTHONHASHSEED=1 same-cwd run + env -i
isolated-directory runs (explicit `/usr/local/bin/python3`, empty
environment). FIVE runs total were executed and all were byte-identical
(sha256 `09e9026a436bf25aed05eabaf3629975971bd320a4c4c5ce5da122239f19f789`,
rc 0 each). The frozen `explore_z20f15.out` IS that stdout.

Independent cross-check (same environment, not part of the frozen artifact):
the FULL census re-enumerated and re-evaluated with the ORDERED engine
(H_ordered) against the frozen canonical-engine output: 1,470 cell shapes
(all 14 cells × 105), 112 tail spots, 185 strip shapes, 62+61+76+92 record
shapes, 12 strip spots, the base spot, 105 below-band shapes, and both
identity recheck rows — 0 mismatches anywhere; every frozen row
(per-cell deviant lists, multivalue counts, shape counts, separation
lists, tail-spot rows, identity hold/break rows) reproduced exactly.
Per-record cache clearing retained (the published rc-137 OOM lesson).

## 3. Observations (all judgment-free)

### 3.1 Cell ladder (14 rungs, 105 shapes each, all s-only, multivalue 0)

Deviant position set = {16, 18, 20}; every deviant row carries
`shapes: 1`. Per-cell deviants (value vs published K0832 Sigma-collapse):

- F20f15: {20: UP 1 v 0} — the ELEVENTH tail form, SINGLE POINT at s=z:
  no hole, no tail. The even-z single-point form is now 3/3 (z=16 s=16,
  z=18 s=18, z=20 s=20, all UP 1v0) and the single@(even z)/hole+tail@(odd
  z) typology alternation has SIX consecutive consistent slices (z15..z20).
  Tail spots (46..53): 112/112 match — the absence of a piercing tail is
  itself the even-form signature (contrast z=19: F 8/8 mismatch).
- G20f15: {18: DOWN 0 v 2, 20: UP 2 v 1}
- E20f15: {18: UP 1 v 0}
- D20f15: {16: DOWN 0 v 2, 18: UP 2 v 1}
- C20f15: {16: UP 1 v 0}
- B20f15: {16: UP 2 v 1}
- A20f15..A820f15: fully collapsed — EIGHT consecutive full collapses, the
  longest A-family collapse run of the series. The z=19 A-rank deviant
  (s=14=z−5) falls below floor 15. Parity note (observation, not a claim):
  at even z the A-break position z−5 is ODD, and every deviant class ever
  observed in the series sits at an even s — an A-break at even z would
  require the first odd-s deviant class; the z=17/z=19 A-breaks were both
  at even s=z−5, and z=21 (odd) puts z−5=16 back in the even classes =
  the z=21 census decides the A-break parity law candidate.
- A8 (j=14, min=14) — the SIXTH consecutive in-band base child
  (z*(14)=26>20) — collapses over its full 105-shape domain: the T-Z20
  base m=15 trivial-absorption candidate.

Structure across positions: the ladder carries the even-z station triplet
{DOWN:0, UP:1, UP:2} at three positions:
- position 16: D DOWN:0, C UP:1, B UP:2;
- position 18: G DOWN:0, E UP:1, D UP:2;
- position 20: F UP:1 (the single point), G UP:2 (the position-20 triplet
  has only the two UP members in the census window).
This is the EXACT z=18 station pattern ({D,C,B}@14, {G,E,D}@16, {F,G}@18)
shifted +2 in position, with the same rank heads D(j=4), G(j=2), F(j=1):
the even-z station form is now 2/2 (z=18, z=20).
Position-set law observation (3 consecutive pairs, judgment-free): the
deviant position set is shared by adjacent (even, following-odd) pairs —
{12,14,16} at z=16/z=17, {14,16,18} at z=18/z=19 — and shifts +2 at each
even step; the z=20 set {16,18,20} is the +2 shift of the z=18 set, and it
triggers the **4th recorded definition-domain exclusion** (the position-14
classes fall below floor 15; cf. the s=12 exclusion at z=17→18, the
no-exclusion shifts at z=18→19).
The z=18-vs-z=20 station identity also leapfrogs the z=19 profile entirely:
the odd-z ladder rotates DOWN:1–DOWN:0–UP:2 triplets one rank, the even-z
ladder plants DOWN:0–UP:1–UP:2 at fixed ranks.

### 3.2 Supply identities (engine-free, section g)

- ELEVENTH-tail identity RECHECK: v(s,21,21)=v(s,20,21) holds exactly on
  {0}∪{12..19}, breaks at s=20 as 0v2, then uniformly 2v1 for ALL
  s∈{21..57} (published {0}∪{12..56} rechecked + extended by one). The
  F20f15 single point sits exactly at the identity's first break position
  (s=20) — supply-to-deviant alignment exact (the even-z analogue of the
  z=19 hole-at-final-hold / tail-from-first-break alignment).
- TWELFTH-tail identity RECHECK: v(s,22,22)=v(s,21,22) holds exactly on
  {0}∪{12..21}, uniform 0v1 break for all s∈{22..57} — the published z20
  probe values reproduced exactly (cross-artifact consistency).
- THIRTEENTH-tail identity (NEW): v(s,23,23)=v(s,22,23) holds exactly on
  **{0}∪{12..21}**, breaks at **s=22 as 0-vs-2**, then **uniformly 2-vs-1
  for ALL s∈{23..57}**. BOTH predeclared components CONFIRMED (break start
  s=22=z; break shape 0v2@z + uniform 2v1@(z+1)+). The newest even-z
  supply-identity form is now 3/3 (z=18, z=20, z=22 supply) — the 0v2+2v1
  shape graduates from 2-data-point coincidence to stable-form candidate
  (3/3, first predeclared-and-confirmed instance). This is the z=22 slice's
  supply datum.

### 3.3 Strip and row records

- T-Z20 provisional claim position sweep m∈{15..19}: 185 shapes,
  **0 violations** (cumulative 55/99/134/162/185).
- m=14-row z=20 (R=35; K1330 (T-Z19) residual band FIRST entry, m=14
  z∈{20..25}, frontier z*(14)=26): **62 shapes, 0 separations**;
  arity<=4 co-token extension: **61 shapes, 0 separations**. A820f15 fully
  collapsed over its 105-shape domain → the T-Z20 base m=15 is the SIXTH
  consecutive trivial-absorption base candidate.
- m=13-row z=20 (R=34; K1328 residual band SECOND entry): **76 shapes,
  0 separations** — exactly the published z20 probe values (cross-artifact
  shape-for-shape consistency machine-checked).
- m=12-row z=20 (R=33; K1325 residual band THIRD entry): **92 shapes,
  0 separations** — exactly the published entries.
- Strip spots m∈{20..23}: 12/12 match.
- m=15 base spot H(36;(15,15);20) = 0 = v(30,20,36) — EXACTLY the
  published z20 probe value; the base-spot z-parity sequence 0/1/0/1/0 is
  now FIVE data points (z=21 candidate: 1).
- Below-band child census H(21;Y;21) vs v(s,21,21): 105 shapes, **0
  deviants, 0 multivalue — SIXTH consecutive full collapse** of the
  below-band supply child.

## 4. Honest record (this run)

- All published bytes consumed during local build were fetched sha-pinned
  from the published kit commits (`6a6832ce` for engine_block.py +
  explore_z19f14.py; `0906ff21` for the z20 probe .py README context;
  `25aafdda` tip for the z19 predecl log), with the engine sha-verified
  (`582c93c1…`) before use; the adoption source `explore_z19f14.py` was
  verified byte-identical to the published pin `e41138e2…` before the
  adaptation, and `engine_block.py` verified identical to `582c93c1…`.
- The embedded ENGINE_BLOCK was transplanted verbatim from the published
  script (startup pin `bd5f22e4…` PASS on the first run — the z19 kit's
  leading-import defect was avoided by design this time).
- K1330 (T-Z19) official runs landed (OFFICIAL-PASS, `25aafdda`) while this
  kit was being built; this lane did not touch the K1330 chain, and the
  (d) band-entry label cites the published K1330 declaration note. The
  K1330 K item / completion log remain that lane's residual work; the
  T-Z20 declaration lane should confirm their landing before its own
  slot claim.
- The ordered-engine cross-check ran clean on the first invocation this
  time (per-record cache clearing; no rc-137 event).
- No wall-clock, no randomness, no hash-order dependence; the shape counts
  76/92 equal the published records' counts exactly because the
  enumerations are identical (machine-checked, not asserted). The cell
  shape count is 105 (not 117) because the floor-15 domain
  {0}∪{15..45} is a different exhaustive window than floor-14's
  {0}∪{14..44}; the count is a domain artifact, not a sweep defect.
- Push protocol: latest main re-fetched immediately before the push
  (hourly parallel-run hazard); the z20-min15 census slot confirmed
  unclaimed; kit + this log pushed in one commit; fetch-back byte
  verification to follow in the same session.

## 5. Handoff to the declaration lane

- The T-Z20 declaration dependencies at push time: K1330 declaration note
  (published `e07d8f3d`), machine (`ca6d12bc`), official runs OFFICIAL-PASS
  (`25aafdda`); the K1330 K item + completion log follow from that lane.
  Child positions follow the engine rules exactly as in the
  K1322/K1325/K1328/K1330 templates:
  - for the claim position H(m+21; X; 20) with min(X)=m>=15, the C-hand
    (z-decrement) child is H(m+20; X; 19) — the published T-Z19 claim
    position for min(X)=m>=14 (T-Z19 numbering R=m+20) and for the ladder
    rungs the published F19f14..A719f14 cells (Y tokens >= 15 >= 14: the
    same co-floor subset argument K1330 used against K1328);
  - the base claim position is H(36;{15}∪Y;20) (T-Z20 numbering R=m+21
    at m=15); its a=m child (token 15→14, R→35) is
    (35;{14}∪Y;20) = the A820f15 cell domain ITSELF (small token 14,
    z*(14)=26 > 20: the SIXTH consecutive in-band base child), fully
    collapsed over all 105 shapes in the frozen census; the m=14-row
    z=20 record (62 shapes published residual-band style + 61 arity<=4
    co-token extension, 0 separations each) provides the row-style
    dossier over the same lattice position;
  - the j=14 rung A820f15's C-hand child is H(33;{14}∪Y;19) = a
    co-floor subset of the published T-Z19 m=14-row claim position
    (R=14+19=33, min(X)=14 inside T-Z19's universal domain min>=14)
    — every rung's C-hand child lands on the published T-Z19 lines.
- The supply story for the F20f15 eleventh form must use the MEASURED
  eleventh-tail identity (hold {0,12..19}, 0v2@20, uniform 2v1@>=21) —
  rechecked and extended here — and the paper proof must reproduce the
  single-point-at-first-break-position (s=20) alignment, including the
  ABSENCE of a persistent tail (the z=16/z=18/z=20 single-point proofs
  are the templates).
- The z=21 census question this kit raises for the next odd slice:
  odd-z predicts hole+tail at F (hole at s=21, tail s>=22, twelfth-tail
  supply datum hold {0,12..21} + uniform 0v1 break s>=22 rechecked here),
  the A-break parity candidate (s=16=z−5 even class back in domain at
  floor 16: the z=17/z=19 pattern predicts A-rank rebirth), and the
  position-set law candidate (z=21 should INHERIT {16,18,20} rather than
  shift, per the z=16/z=17 and z=18/z=19 pair pattern).

## 6. Standard caveats

Everything in this kit and log is FINITE machine observation against the
pinned raw engine, plus pure closed-form pre-computations for section (g).
Nothing here is a theorem; no universal statement is claimed; no verdict of
any game position is consumed. Standard 11×11 empty board, two-stone roots
{49,60}/{59,60}, S2 {59,60}, classes 1/2/4, and all central-reply roots:
all UNKNOWN, unchanged. The battery/spot counts are engine cross-checks,
not proof substitutes.
