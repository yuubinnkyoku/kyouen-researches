# 2026-11-25 z=23 min>=18 (floor-18) pre-declaration census kit — exploration log

Lane: high-speed lane (this run). Status of this document: PRIMARY RECORD of
the pre-declaration census kit `research/experiments/strip-z23-min18-20261125/`.
No K slot is claimed, no universal statement is claimed. Everything below is
finite machine observation against the pinned raw engine, plus engine-free
closed-form pre-computations. The declaration lane (this same session's
continuation, or a later run) picks up from here.

## 1. Context, prior-lane state and slot check

The fast lane's previous chain completed K1339 (z=22 min>=17, publication
chain closed at `28b8dd39`, item at `70b409c5`): the z=22 slice is fully
closed at min>=17 and the K1339 completion note §5/§7 registered the
z=23 (floor-18) slice as the next 本命, with ALL of its C-hand dependencies
already published (the K1339 z=22 16-cell ladder F22f17..A1022f17 plus the
theorem T-Z22 rows m>=17) and the fourteenth-tail supply identity
(v(s,24,24)=v(s,23,24), hold {0}∪{12..23}, uniform 0v1 break s>=24) already
measured by the published z21/z22 census kits and universally fixed by
K1334 Theorem A (k=23 odd instance).

At kit-build time (HEAD `3683bf7d`, 2026-11-25T22:10Z): no z=23-min18
census existed (checked: no `research/experiments/strip-z23-min18*`
directory; no `strip-z23` log entry in code search; the published strip
kits cover z<=22). No declaration note for T-Z23 exists. K-slot state at
build time: K1333..K1343 all taken (K1338/K1341/K1342/K1343 by the parallel
conic lane, K1335 fast lane, K1337 fast lane, K1339 fast lane, K1340
conic, K1336 conic); K1344 free at build time (code search 0 hits) — the
declaration lane must re-probe before claiming.

The z22-min17 predecl log §5 (published, commit `115c0bb9` chain) already
registered the complete z=23 census candidate list: position-set inherit
{18,20,22} (pair rule 4th pair, no exclusion), the F hole+tail odd form
(DOWN 1v2 at s=22=z−1, conforming hole at s=23=z, persistent tail UP 2v0
for s>=24, tail spots 8/8 mismatch), the A-RANK BREAK REBIRTH at s=18=z−5
(UP 2v0, odd candidate 4/4), the odd station triplet {DOWN:1, DOWN:0,
UP:2}, base spot candidate 1 (eighth parity point), below-band ninth
consecutive collapse, and the sixteenth-tail pre-computation with the
predeclared odd-z candidate. This kit executes exactly that registered
program, with the full per-cell deviant list written into the file
docstring BEFORE the first run (the z21 C-cell disclosure lesson
applied).

## 2. Kit construction (publish-then-execute, frozen before publication)

- `engine_block.py` — byte-clone of the published chain engine (sha256
  `582c93c17bcd4fa618bfb74c733c3d679e197e8749ec4bbcc8821d3a6610d5c0`),
  copied from the local copy of the published z22-min17 kit
  `strip-z22-min17-20261125/engine_block.py` (fetch-back verified against
  its published sha) and sha-verified. The embedded ENGINE_BLOCK startup pin
  `bd5f22e4…` is asserted by the script itself (engine_gate PASS in the
  frozen output).
- `explore_z23f18.py` (sha256
  `eddd5e90825b0b38a51982ebd26e9e2e7a15390e0ae9916650dad7dddf8385f3`)
  — adapted from the frozen published `explore_z22f17.py` (sha256
  `9e8ab7073a5d9d119af7928a19953efa1ac409df15b5878c9dab473af2e5c3c9`,
  fetch-back verified against main before the adaptation) by the disclosed
  textual diff: z 22→23; cell budget j+23→j+24; floor 17→18; rungs 16→17
  with the provisional 17th-rank label `A11` (small token 17; z*(17)=33>23;
  NINTH consecutive in-band base child); s domain {0}∪{18..48}; tail spots
  {49..56}; strip sweep m∈{18..22}; strip spots m∈{23..26}; m=18 base spot
  (NEW measurement, candidate 1); below-band child H(24;Y;24) vs
  v(s,24,24); records: (d) m=17-row z=23 CANDIDATE FIRST entry of the future
  T-Z22 residual band m=17 z∈{23..32} (frontier z*(17)=33; band pending the
  T-Z22-completion bookkeeping) in the published residual-band style
  (arity<=3 TOTAL) PLUS an arity<=4 co-token extension; (d2) m=16-row z=23
  SECOND entry of the future T-Z21 residual band m=16 z∈{22..29} (SAME
  enumeration → same 40 shapes); (d3) m=15-row z=23 THIRD entry of the
  future T-Z20 residual band m=15 z∈{21..28} (same 50); (d4) m=14-row z=23
  FOURTH entry of the K1330 published band m=14 z∈{20..25} (same 62);
  (d5) m=13-row z=23 FIFTH entry of the K1328 band m=13 z∈{19..24} (same
  76); the m=12-row NOT swept (the K1325 band m=12 z∈{18..21} CLOSED at
  z=21); (g1) fourteenth-tail identity recheck over s∈{0}∪{12..60}
  (EXTENDED domain; the z=23 slice supply datum); (g2) fifteenth-tail
  identity recheck over s∈{0}∪{12..60}; (g3) NEW sixteenth-tail supply
  pre-computation v(s,26,26) vs v(s,25,26) over s∈{0}∪{12..60} with BOTH
  break components predeclared (the z=25-slice supply datum; the fourth
  fully-predeclared identity of the series after the thirteenth,
  fourteenth and fifteenth).
- THE FULL PREDECLARED CANDIDATE (in the file docstring, written before the
  first run): derived from the published z=21 ODD profile (the declared
  K1337 cell lemmas F21f16..A921f16, anchor-transcribed in the published
  verify_k1339.py D3 set and re-anchored by its battery) shifted +2 in BOTH
  position and ladder budget — WITH THE COMPLETE PER-CELL 8-CLASS DEVIANT
  LIST SPELLED OUT (F {22: DOWN 1v2; hole@23 conforming; tail s>=24 UP 2v0};
  G {22: DOWN 0v1}; E {20: DOWN 1v2, 22: UP 2v0}; D {20: DOWN 0v1};
  C {18: DOWN 1v2, 20: UP 2v0}; B {18: DOWN 0v1}; A23f18 {18: UP 2v0}
  = A-break rebirth at even s/odd z; A2..A11 all fully collapsed), plus:
  (i) deviant position set candidate {18,20,22} INHERITED from z=22
  unchanged (the pair-rule 4th pair; NO definition-domain exclusion —
  the third consecutive even→odd non-exclusion); (ii) the odd station
  triplet {DOWN 1v2, DOWN 0v1, UP 2v0} at {C,B,A}@18/{E,D,C}@20/
  {F,G,E}@22 (candidate 4/4 with z=17/z=19/z=21); (iii) F odd-form
  hole+tail, tail spots exactly 8 F-mismatches; (iv) all cells s-only;
  (v) strip 0 violations; (vi) all row records 0 separations with the
  cross-artifact shape counts; (vii) below-band NINTH consecutive full
  collapse; (viii) base spot 1 (eighth parity point); (ix)-(xi) the three
  identity constants as published/predeclared.
- Per-cell `H.cache_clear()` retained (z=13 shared-cache OOM lesson).
- Runtime ~29 s/run (one rung deeper than the z22 kit).

Determination protocol (frozen before the official runs, executed exactly):
default run + default re-run ×2 + PYTHONHASHSEED=1 same-cwd run + env -i
isolated-directory runs (explicit `/usr/local/bin/python3`, empty
environment). SIX runs total were executed and all were byte-identical
(sha256
`bb456e85bdf248484bcf035ffd35c3bc39842f3524399851bc0e7c62f84834ca`,
rc 0 each). The frozen `explore_z23f18.out` IS that stdout.

Independent cross-check (same environment, not part of the frozen artifact):
the FULL census re-enumerated and re-evaluated with the ORDERED engine
(`crosscheck_z23.py`, session-local, sha256
`ec3a793c8d9bf65a3e0b5d83534c6dde494ed078591c52a3b9de0b71617dc9e3`)
against the frozen canonical-engine
output: 1,377 cell shapes (all 17 cells × 81), 136 tail spots, 108 strip
shapes, 32+31+40+50+62+76 record shapes, 12 strip spots, the base spot,
81 below-band shapes, and ALL identity hold/break rows compared as FULL
rows (values included): **0 mismatches**; every frozen row reproduced
exactly. rc 0, ~45 s. Per-record cache clearing retained.

(The crosscheck script had two session-local iteration bugs during its
construction — a cell-name list index bug and an identity-row key-name
derivation bug, both caught by the script's own comparison failures and
fixed before the recorded PASS run; every counted failure was a key-name
or label mismatch, never a value mismatch.)

## 3. Observations (all judgment-free)

### 3.1 Cell ladder (17 rungs, 81 shapes each, all s-only, multivalue 0)

Deviant position set = **{18, 20, 22}** — the predeclared candidate:
INHERITED from z=22 without shift (the (even, following-odd) pair rule
graduates to 4/4: {(16,18,20),(14,16,18),(12,14,16)} were the three
preceding pairs), with NO definition-domain exclusion event — z=22's
classes {18, 20, 22} all survive the floor-17→18 raise. Even→odd
non-exclusion is now 3/3 (z=18→19, z=20→21, z=22→23), against odd→even
oldest-class death 2/2 (z=19→20 s=14, z=21→22 s=16).

Deviant classes, measured (all 8 predeclared components hit exactly):
- **F23f18 {s=22: DOWN 1v2; s=23: conforming HOLE (value 0 = the mirror
  v(24,23,25)); s>=24: tail UP 2v0}** — the FOURTEENTH tail form (odd-z
  HOLE+TAIL, z-relative profile identical to z=15/z=17/z=19/z=21). The
  single@(even z)/hole+tail@(odd z) typology alternation is NINE consecutive
  consistent slices (z15..z23): odd form 5/5, even form 4/4.
- **G23f18 {22: DOWN 0v1}**; **E23f18 {20: DOWN 1v2, 22: UP 2v0}**;
  **D23f18 {20: DOWN 0v1}**; **C23f18 {18: DOWN 1v2, 20: UP 2v0}**;
  **B23f18 {18: DOWN 0v1}**; **A23f18 {18: UP 2v0} — the A-RANK BREAK
  REBIRTH**, birth position s=18=z−5 (even s, odd z); the odd-z birth
  sequence is 4/4 (z=17 s=12, z=19 s=14, z=21 s=16, z=23 s=18) against
  the even-z annihilation 5/5 (z=14, z=16, z=18, z=20, z=22). The
  A-rank full odd/even split now holds over NINE slices.
- Odd station triplet {DOWN 1v2, DOWN 0v1, UP 2v0} at
  **{C,B,A}@18, {E,D,C}@20, {F,G,E}@22 — 4/4** with z=17/z=19/z=21
  (the exact two-step successor of the published z=21 stations; the
  odd-form station values differ from the even form
  {DOWN 0v2, UP 1v0, UP 2v1} at every rank, completing nine slices of
  the two-form station taxonomy).
- **A223f18..A1123f18 fully collapsed** — TEN consecutive full collapses
  past the A-boundary rung. **A1123f18 (small token 17, z*(17)=33>23)
  is the NINTH consecutive in-band base child**; its C-hand child
  (40;{17}∪Y;22) is the published T-Z22 m=17 row claim position
  (R=(m)+23 at m=17) — the base-rung supply for the T-Z23 declaration
  is fully published.
- Tail spots {49..56}: exactly the 8 F-cell spots mismatch (value 2 vs
  collapse 0); all other 128 match — the odd-form signature measured.

### 3.2 Strip sweep and records

- Strip m∈{18..22}: 108 shapes (28/51/71/90/108 cumulative), 0 violations.
- m=17-row z=23 (R=41): 32 shapes 0 seps; arity<=4 ext 31/0. FIRST
  entry candidate of the future T-Z22 residual band m=17 z∈{23..32}.
- m=16-row z=23 (R=40): 40/0 (matches the published z=22 entry
  shape-for-shape). m=15-row: 50/0 (z=21/z=22 entries). m=14-row: 62/0
  (z=20/z=21/z=22 entries; K1330 band, remaining z=24/z=25 entries).
  m=13-row: 76/0 (z=19..z=22 entries; K1328 band, remaining z=24 entry).
- Strip spots m∈{23..26}: 12/12 match.
- m=18 base spot H(42;(18,18);23) = **1** = v(36,23,42) conforming —
  the eighth base-spot parity point (0,1,0,1,0,1,0,1 alternating by z).

### 3.3 Below-band and supply identities

- Below-band H(24;Y;24) vs v(s,24,24): 81 shapes, 0 deviants, 0
  multivalue — NINTH consecutive below-band full collapse.
- FOURTEENTH tail (z=23 supply): hold {0}∪{12..23} (13 rows), uniform
  0v1 break s∈{24..60} (37 rows) — published constants reproduced and
  extended by one row; odd-z supply form 3/3 (z=19/z=21/z=23).
- FIFTEENTH tail (z=24 supply): hold {0}∪{12..23}, 0v2 at s=24, uniform
  2v1 s∈{25..60} — published z22-kit constants reproduced, extended;
  even-z supply form 4/4 (z=18/z=20/z=22/z=24-supply).
- **SIXTEENTH tail (NEW, k=25 odd, z=25 supply): hold {0}∪{12..25} (15
  rows), UNIFORM 0v1 break s∈{26..60} (35 rows) — BOTH predeclared
  components CONFIRMED**; the odd-z supply form graduates to 4/4
  (z=19/z=21/z=23/z=25-supply).

## 4. Honest session record

- This kit was built and executed in a single session run of the
  high-speed lane, immediately after fetching the published z22 kit bytes
  and declaration/machine transcripts from main (fetch verified sha256
  against the published values for explore_z22f17.py `9e8ab707…`,
  verify_k1339.py `566543f7…`, engine_block.py `582c93c1…`,
  explore_z22f17.out `f16a87d4…`).
- The predeclared candidate list in the file docstring was composed
  BEFORE the first run of explore_z23f18.py, from PUBLISHED sources only
  (the K1337 declared z=21 profile, the K1339 declaration note §5
  handoffs, the K1334 Theorem A break constants, and the z22-min17
  predecl log §5 candidate registration). No engine execution on any
  z=23 position happened before the docstring was frozen in the file
  (the only pre-run computations were hand K0832 branch evaluations).
- Session-local iterations (disclosed, none affecting the frozen
  artifact): the crosscheck script's two label-derivation bugs (§2), and
  one throwaway checker one-liner with a KeyError — all fixed before the
  recorded PASS.

## 5. Handoff to the declaration lane

- **T-Z23 (z=23, floor-18) is now fully prepared**: the C-hand children
  of the 17-rung ladder are all published (j=1..16 → the K1339 cell
  lemmas F22f17..A1022f17; j=17 → the T-Z22 m=17 row), the j=1 below-band
  child collapses universally via the stair lemma (candidate BB7,
  H(24;Y;24)=v(s,24,24) for floor-18 Y since R=24 <= z'+min(Y)), the
  fourteenth-tail absorption identity v(s,24,24)=v(s,23,24) is
  K1334-Theorem-A-universal (k=23: hold [0..23], uniform (0,1) break
  s>=24 — the F23 tail supply), and the census provides the
  candidate-measured ladder F23f18..A1123f18 for paper-proof
  re-derivation (the declaration lane must derive §2 from the paper,
  not from the census, per the K1339 lesson).
- Expected declaration content: 17 cell lemmas (F,G,E,D,C,B,A + A2..A11,
  with A23f18 carrying the reborn A-break {18: UP 2v0} and A1123f18 the
  ninth in-band base child), T-Z23 (H(m+24;X;23) = v(S,23,m+24) for
  min(X)=m>=18; base m=18 trivial absorption through the fully
  collapsing A1123f18), 系1/系2 closing z=23 for min>=18 with residual
  band z∈{24..33} (frontier z*(18)=34).
- K slot: K1344 was free at kit-build time; re-probe at claim time
  (the conic lane is minting numbers rapidly — K1338/K1340/K1341/
  K1342/K1343 are all conic).
- The z=24 (floor-19) census inputs are in place (position-set inherit
  candidate {20,22,24}+single-point-F form hole; the FIFTEENTH-tail
  identity already measured here for the z=24 supply; the SEVENTEENTH-
  tail pre-computation v(s,27,27) vs v(s,26,27) is the natural next
  predeclaration).
- Remaining row-record targets: m=14 band z=24/z=25 (K1330 closure at
  frontier z*(14)=26), m=13 band z=24 (K1328 closure), m=15 band
  z=24..28, m=16 band z=24..29, m=17 band (this kit's z=23 entry is the
  first) z=24..32, and the m=11 FRONTIER z=21/z=22 side records
  (never swept beyond the beyond-kit probe).

## 6. Standard caveats

Everything in this kit and log is FINITE machine observation against the
pinned raw engine, plus pure closed-form pre-computations for section (g).
Nothing here is a theorem; no universal statement is claimed; no verdict of
any game position is consumed. Standard 11×11 empty board, two-stone roots
{49,60}/{59,60}, S2 {59,60}, classes 1/2/4, and all central-reply roots:
all UNKNOWN, unchanged. The battery/spot counts are engine cross-checks,
not proof substitutes.
