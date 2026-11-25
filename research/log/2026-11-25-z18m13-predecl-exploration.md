# 2026-11-25 z=18 min>=13 (floor-13) pre-declaration census kit — exploration log

Lane: high-speed lane (this run). Status of this document: PRIMARY RECORD of
the pre-declaration census kit `research/experiments/strip-z18-min13-20261125/`.
No K slot is claimed, no universal statement is claimed. Everything below is
finite machine observation against the pinned raw engine, plus one engine-free
closed-form pre-computation. The declaration lane (a later run) picks up from
here.

## 1. Context and trigger

The published K1325 completion (item + log at commit `e3a2f749`) closed the
z=17 min>=12 (floor-12) slice and registered in its resume section (7):

- (a) the z=18 min>=13 (floor-13) slice (T-Z18) is the next primary target;
  all dependencies are published; the pre-declaration census kit
  (12 rungs, Y >= 13) is the entry point;
- the F-family NINTH tail form prediction question: whether the +2-shift law
  (sixth form z=15 → eighth form z=17) continues (predicted break of the
  supply identity v(s,19,19)=v(s,18,19) starting at s>=20 with 1-vs-0
  constants), with the closed-form pre-computation flagged as the key input.

This run built and executed exactly that kit.

Also relevant: this run started DURING the recovery of the accidental
main-tip empty-index commit `d0755ecc` (16:02Z; incident log `dcc39bab`).
The owner's RESTORE chunk sequence (chunks 1/21 restarted as 1..31/31,
16:44Z–16:59Z+) was in progress while the kit was built locally. All bytes
this kit was adapted FROM were fetched sha-pinned from the published kit
commit `2c74f1c6` (predecl census kit of K1325) per the incident guidance.
Nothing was pushed until the restore finished and the tree was spot-verified
(section 5 of this log; see also the separate restore spot-verification log
published in the same session).

## 2. Kit construction (publish-then-execute, frozen before execution)

- `engine_block.py` — byte-clone of the published chain engine
  (sha256 `582c93c17bcd4fa618bfb74c733c3d679e197e8749ec4bbcc8821d3a6610d5c0`),
  fetched from `2c74f1c6` and sha-verified before use. The embedded
  ENGINE_BLOCK startup pin `bd5f22e4…` is asserted by the script itself
  (engine_gate section, gate PASS in the frozen output).
- `explore_z18f13.py` (sha256
  `152fd2d8814f958e5aaef275f83b4abb1763b58929d375d7ec9cb864f2a94ff4`)
  — adapted from the frozen published `explore_z17m12.py` (sha256
  `410fea310b00da6733e6d336fa6b275890307ad16e6603683fc1f4500bdef7b0`)
  by the disclosed textual diff (all changes machine-derivable from the
  published z17 kit; documented in the kit README):
  z 17→18; cell budget j+18→j+19; floor 12→13; rungs 11→12 with the
  provisional 12th-rank label `A6` (small token 12; FOURTH consecutive
  in-band base child, z*(12)=22>18); s domain {0}∪{13..43}; tail spots
  {44..51}; strip sweep m∈{13..17}; strip spots m∈{18..21}; m=13 base spot;
  below-band child H(19;Y;19) vs v(s,19,19); records: (d) m=12-row z=18
  FIRST entry of the K1325 residual band m=12 z∈{18..21} in the published
  residual-band style (arity<=3 TOTAL) PLUS an arity<=4 co-token extension;
  (d2) m=11-row z=18 SECOND entry of the K1322 residual band m=11 z∈{17..20}
  in the SAME enumeration as the published z=17 entry; (d4) NEW m=10-row z=18
  FRONTIER record (z=18 = z*(10), first even-m frontier data point,
  published frontier style); (d3) m=9-row z=18 beyond record in the IDENTICAL
  published z=17 frontier enumeration (234 shapes); (d5) m=8-row z=18 beyond
  record in the IDENTICAL published 362-shape enumeration; (g) NEW
  engine-free ninth-tail supply pre-computation (pure K0832 closed form):
  v(s,19,19) vs v(s,18,19) over s∈{0}∪{12..55}, plus the z=17 partner
  identity recheck v(s,18,18) vs v(s,17,18) over the same domain.
- Per-cell `H.cache_clear()` retained (z=13 shared-cache OOM lesson).
- Runtime ~23.7 s/run.

Determination protocol (frozen before the official 3 runs, executed exactly):
default run + PYTHONHASHSEED=1 same-cwd run + env -i isolated-directory runs
(explicit `/usr/local/bin/python3`, empty environment). FIVE runs total were
executed and all were byte-identical (sha256
`c4e7757c587883bb41b0f297de336128cd6bafc55865ba10673b28c7338d0b0b`, rc 0 each).
The frozen `explore_z18f13.out` IS that stdout.

Independent cross-check (same environment, not part of the frozen artifact):
12 deviant/witness rows re-evaluated with the ORDERED engine
(H_ordered) against the canonical engine — 12/12 agreement, 0 mismatches.

## 3. Observations (all judgment-free)

### 3.1 Cell ladder (12 rungs, 133 shapes each, all s-only, multivalue 0)

Deviant position set = {14, 16, 18} exactly; all deviant rows carry
`shapes: 1` (a single decomposition class per row, as usual for the series).
Per-cell deviants (value vs published K0832 Sigma-collapse):

- F18f13: {18: UP 1 v 0} — SINGLE POINT, no hole at s=18, no tail
  anywhere in-window; tail spots (44..51) 0/96 mismatches series-wide.
- G18f13: {16: DOWN 0 v 2, 18: UP 2 v 1}
- E18f13: {16: UP 1 v 0}
- D18f13: {14: DOWN 0 v 2, 16: UP 2 v 1}
- C18f13: {14: UP 1 v 0}
- B18f13: {14: UP 2 v 1}
- A18f13..A618f13: fully collapsed — SIX consecutive A-rank full
  collapses, the longest collapse run of the series (z=17's A-rank break
  A17f12{12 UP:2} did not survive: s=12 is domain-excluded at floor 13 —
  the third recorded instance of definition-domain exclusion, after
  z=13→14 (s=8) and z=15→16 (s=10)).

Structure across positions — the z=17 UP-climb / DOWN-spread chains
generalize to a repeating per-position triplet
{DOWN:0, UP:1, UP:2}:
- position 14: D DOWN:0, C UP:1, B UP:2 (three ranks);
- position 16: G DOWN:0, E UP:1, D UP:2 (three ranks);
- position 18: F UP:1, G UP:2 (two ranks — the DOWN:0 slot at position 18
  is EMPTY; F's own deviant IS the position-18 UP:1 carrier).

The ninth F tail typology: SINGLE POINT (s=18 UP:1). Series data:
z=15 (odd) hole+tail, z=16 (even) single point, z=17 (odd) hole+tail,
z=18 (even) single point — the single@even-z / hole+tail@odd-z
ALTERNATION now has four consecutive consistent data points
(observation, not a law).

### 3.2 Ninth-tail supply pre-computation (engine-free, section g)

- Naive +2-shift prediction: hold {0}∪{13..19}, break 1v0 for s>=20.
- MEASURED: v(s,19,19)=v(s,18,19) holds exactly on **{0}∪{12..17}**;
  breaks at s=18 as **0 vs 2**; for ALL s∈{19..55} breaks uniformly as
  **2 vs 1**. Both elements of the naive prediction are contradicted.
  The F18f13 deviant sits exactly at the first break position (s=18);
  the uniform s>=19 break produces NO further F deviants (F matches the
  collapse there) — a qualitatively selective supply-to-deviant mapping.
- z=17 partner recheck: v(s,18,18)=v(s,17,18) holds on {0}∪{12..17},
  breaks for all s∈{18..55} uniformly, identity-order constants 0 vs 1
  (published K1325's "1 vs 0" constant pair is reproduced up to
  orientation; raw values are in the frozen .out).

### 3.3 Strip and row records

- T-Z18 provisional claim position sweep m∈{13..17}: 286 shapes,
  **0 violations** (cumulative 84/152/207/251/286).
- m=12-row z=18 (R=31; K1325 residual band first entry; published style):
  **92 shapes, 0 separations**; arity<=4 extension: **95 shapes,
  0 separations**; cell A618f13 fully collapsed over its 133-shape
  domain → the T-Z18 base m=13 is the FOURTH consecutive
  trivial-absorption base candidate.
- m=11-row z=18 (R=30; K1322 residual band second entry; SAME
  enumeration as the published z=17 record): **110 shapes,
  0 separations**.
- **m=10-row z=18 FRONTIER (z=18=z*(10); NEW, first even-m frontier
  data point)**: 170 shapes, **exactly 1 separation: X=(10,10), S=20,
  UP 2 v 1** — the DIAGONAL. Frontier parity structure now: m=8 (even)
  z=14 diagonal (8,8); m=9 (odd) z=17 off-diagonal (9,10); m=10 (even)
  z=18 diagonal (10,10) — candidate rule "even m → (m,m), odd m →
  (m,m+1)", 2/2 on even, 1/1 on odd (observation).
- m=9-row z=18 beyond (234 shapes, identical enumeration): **exactly 1
  separation: X=(9,10), S=19, UP 1 v 0** — same position as the z=17
  frontier separation (UP 2 v 0): persistence without reabsorption,
  value decay 2→1.
- m=8-row z=18 beyond (362 shapes, identical enumeration): **0
  separations** — the beyond set is EMPTY for the first time:
  {(8,8)UP}@z14 → {(8,8)DOWN}@z15 → {(8,8),(8,10)}@z16 → {(8,10)DOWN}@z17
  → {}@z18. (8,10) re-absorbs exactly two slices after (8,8) — the
  flip/reabsorb alternation continues with a per-position 2-slice lag.
- Strip spots m∈{18..21}: 12/12 match.
- m=13 base spot H(32;(13,13);18) = 0 = v(26,18,32). Base-spot sequence
  across floors: 0 (z16/m11), 1 (z17/m12), 0 (z18/m13) — z-parity
  alternation candidate (3 data points).
- Below-band child census H(19;Y;19) vs v(s,19,19): 133 shapes, **0
  deviants, 0 multivalue** — FOURTH consecutive full collapse of the
  below-band supply child.

## 4. Honest record (this run)

- All published bytes consumed during local build were fetched
  sha-pinned (kit commit `2c74f1c6`; engine and z17 explorer sha-verified
  before use) per the incident guidance in force since 16:02Z.
- The kit was developed DURING the owner's restore; nothing was pushed
  until (i) the chunk 31/31 restore sequence completed on main and
  (ii) a spot-verification of the restored tree passed (separate log).
- Before each push the latest main was re-fetched (hourly parallel-run
  hazard); the z18-min13 slot was confirmed unclaimed (no
  `strip-z18-min13*` directory, no counter-declaration).
- Section (d)/(d2) enumeration styles: initially built with the
  (m,)∪parts co-token style (arity<=4 TOTAL) which is NOT the published
  residual-band style; corrected to the published style (arity<=3 TOTAL,
  X[0]=m) for direct band comparability, keeping the arity<=4 version
  as an explicitly labelled extension section. The correction happened
  BEFORE any publication; the frozen .out is the corrected 5-run
  artifact. This note is recorded because the z=17 kit's own (d)/(d2)
  count table (110/130) is what the future z=19 census must match.
- No wall-clock, no randomness, no hash-order dependence; the m=11 z=18
  record's shape count 110 equals the published z=17 record's count
  exactly because the enumeration is identical (cross-slice
  comparability machine-checked, not asserted).

## 5. Restore spot-verification performed by this run before pushing

(Separate log:
`research/log/2026-11-25-restore-e5cc9f8e-spot-verification.md`.)
In brief: after the owner's 31/31 RESTORE chunks completed (final chunk
31/31 at 17:03:30Z, tip `567a84e4`), this run re-fetched main and
spot-verified the restored tree: root listing identity modulo the
owner's test-push residue, AGENTS.md and knowledge-README byte pins vs
`e5cc9f8e`, the three additive post-wipe publications (K1325 item,
K1325 completion log, incident report) at their published sha pins,
identical first-1000 directory windows for items/experiments/log, and
selected infrastructure probes. The verification and its limits (spot,
NOT a full-tree byte diff) are documented there; the restored tree was
used as the base for this kit's publication.

## 6. Handoff to the declaration lane

- The T-Z18 declaration has all dependencies published. Child positions
  follow the engine rules exactly as in the published K1322/K1325
  declaration templates:
  - for the claim position H(m+19; X; 18) with min(X)=m>=13, the
    C-hand (z-decrement) child is H(m+18; X; 17) — exactly the published
    T-Z17 claim position for min(X)=m (the T-Z17 numbering R=m+18);
  - the a=m (token-decrement) child lands on the (m−1)-row claim
    position of THIS slice (R=m+18 after the move);
  - the a>m children are covered by the published K1264 stair in the same
    role as in T-Z15/T-Z16/T-Z17;
  - for the LADDER cells Cell_j(s)=H(j+19; {j}∪Y; 18), the C-hand child
    of rung j is (j+18; {j}∪Y; 17): for j in 1..11 these are anchored by
    the published K1325 z=17 cell lemmas F17f12..A517f12 (same
    positions), and for j=12 it is H(30; {12}∪Y; 17) = the published
    T-Z17 m=12-row claim position. This is the same anchor topology the
    K1325 verification machine used (its D3 anchors = the published
    z=16 lines + T-Z16 C-hand anchors), and the z18 verify machine
    should mirror it with the published z=17 lines + T-Z17.
- The ladder for the paper proof: 12 s-only cells F18f13..A618f13 with
  the closed forms in the frozen .out; the repeating
  {DOWN:0, UP:1, UP:2} triplet structure at positions 14/16 and the
  missing DOWN slot at 18; the base m=13 trivial absorption via the
  fully collapsed A618f13 (FOURTH consecutive in-band base child) plus
  the 92-shape m=12-row record; the option-set-identity induction for
  m>=14 needs the published K1264 stair and the T-Z17 m-rows for the
  a>m and C-hand children.
- The supply story for the F ninth form must use the MEASURED identity
  (hold {0,12..17}, break 0v2@s=18, 2v1@s>=19) — NOT the naive +2-shift
  prediction (now contradicted by the closed form).
- The frontier parity rule (m even → diagonal; m odd → (m,m+1)) has
  2 even + 1 odd data points; the m=11 z=20 frontier (z*(11)=21-1=20)
  is the natural next probe.
- The beyond reabsorption sequence ({(8,10)}@z17 → {}@z18) suggests the
  m=9 (9,10) separation will reabsorb at z=19 — the m=9-row z=19 record
  is the discriminating probe (its z=18 value decayed 2→1 while NOT
  reabsorbing, so odd-m positions may follow the same 2-slice lag:
  reabsorb at z=19).
- The next census kit entry points after this one: z=19 min>=14
  (floor-14, z odd → hole+tail predicted by the typology alternation);
  m=11-row z∈{19,20} residual-band entries; m=12-row z∈{19..21}
  residual-band entries.

## 7. Standard caveats

Everything in this kit and log is FINITE machine observation against the
pinned raw engine, plus a pure closed-form pre-computation for section (g).
Nothing here is a theorem; no universal statement is claimed; no verdict of
any game position is consumed. Standard 11×11 empty board, two-stone roots
{49,60}/{59,60}, S2 {59,60}, classes 1/2/4, and all central-reply roots:
all UNKNOWN, unchanged. The battery/spot counts are engine cross-checks,
not proof substitutes.
