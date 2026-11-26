# newband m31/m32 frontier + m19..m30 ladder continuation + trio mid-ladder probes + m29/m30 below-frontier windows pre-declaration exploration kit (concurrent second census of the kit-7 registrations; executed blind, recovered, re-verified)

This directory is the publish-then-execute PRIMARY RECORD for the
pre-declaration census of the REGISTERED kit-7 S5 / frozen-section (d)
items. The kit was REGISTERED, FROZEN, EXECUTED and AUDITED in a first
sandbox (2026-11-26 ~10:30Z), lost in a sandbox environment reset
before its push, and RECOVERED + re-verified byte-exactly after the
reset (see the Recovery note). At its push time this census is the
SECOND publication of the same registered targets: a concurrent hourly
execution of the same lane has already published the same 28 binding
rows + 3 mid-slice probes + 16 windows + hole row as its own kit-8
(commit `7af915fb02d07793c8597108baee96f03f051929`, 10:54:57Z). The
value this kit adds on top is (a) a blind INDEPENDENT re-execution that
agrees on every shared measurement (below), (b) the sum-only value
witness (candidate law L8) with fresh probes, and (c) the recovery
record itself. Everything measured is finite machine observation.

## RECOVERY NOTE (dated 2026-11-26)

The original explorer and its verification scripts were lost in a
sandbox environment reset that happened AFTER the frozen run and BEFORE
the push. What survived, verified byte-exactly against the sha recorded
before the reset, is the FROZEN OUTPUT itself
(`explore_m31m32_laddercont_midtrio_windows.out`, sha256
`487970c9db06e44902eb625401348a8d37e33d49b19781aaaa42da9e2d6f081e`,
123,422 bytes). The published `explore_m31m32_laddercont_midtrio_windows.py`
is an analysis-time REBUILD: its tables (battery literal order, anchor
specifications, row labels/candidates/provenance strings, future
registrations, engine pin) are carried from the recovered frozen output,
while every MEASURED field (all 48 row sweeps, 180 anchor re-measurements,
769 battery checks, all collapse values) is re-executed LIVE at every
run; a successful run REGRESSES the frozen output byte-identically (the
script asserts the sha256 and exits nonzero on mismatch — verified rc 0
at recovery time, plus a PYTHONHASHSEED=random rerun, all
byte-identical). The pre-reset records (5 byte-identical determinism
runs, the original audit and derive checks) stand as executed history;
the post-recovery re-executions of the same checks are in the log S4.
See the log S6 for the full dated record.

## Files

- `engine_block.py` — byte-clone of the published chain engine, sha256
  `582c93c17bcd4fa618bfb74c733c3d679e197e8749ec4bbcc8821d3a6610d5c0`,
  byte-identical to the kit-4..kit-7 chain (re-fetched from the kit-7
  commit and sha-verified at recovery time); embedded ENGINE_BLOCK
  startup pin `bd5f22e4…` asserted (engine_gate PASS in the frozen
  output).
- `explore_m31m32_laddercont_midtrio_windows.py` — RECOVERY REBUILD of
  the lost frozen pre-declaration explorer (see the Recovery note),
  sha256
  `cbd521157b74006a27c300ff60d30daa3232964599709de5941e3d626028a8b1`
  (73,497 bytes). The LOST ORIGINAL explorer (sha256
  `38c6074247b234f90facc5cee22c8e5fb5aa5f5bd8741de67591c79f3d45b344`,
  77,379 bytes) is recorded here permanently; its bytes are not
  recoverable and are not claimed anywhere below to be. Full
  registration provenance, the dated z-corrections (see below), the two
  DISCLOSED smax extensions (m=19@z=57 and m=20@z=58, extended m+38 →
  z+2 so the registered birth seats are in sweep), and the
  skipped-stage contingency notes on the m=15/m=17 mid-slice probes are
  carried inside the registered candidate / registered_by strings,
  live in every run.
- `explore_m31m32_laddercont_midtrio_windows.out` — the frozen stdout,
  sha256
  `487970c9db06e44902eb625401348a8d37e33d49b19781aaaa42da9e2d6f081e`
  (123,422 bytes), rc 0, ~38 s. Deterministic: the pre-reset published
  run plus FOUR verification runs were byte-identical (default x2 +
  PYTHONHASHSEED=random + env-i isolated); post-recovery, the rebuild
  run plus a PYTHONHASHSEED=random rerun reproduced it byte-identically
  (and every field was re-executed live by the ordered-engine audit).
- `sumonly_probe.py`, `sumonly_probe_R1.out`, `sumonly_probe_R2.out` —
  post-recovery analysis-time diagnostic probes (NOT part of the frozen
  run; candidate law L8 witness, see below).

## Registered targets taken by this kit (before the fact)

1. The 28 binding kit-8 rows frozen verbatim in the published kit-7
   output section `future_slice_registration_constants` (commit
   `a62c5d2e…`): m=19..m=20 through depth d=10, m=21..m=22 d=6,
   m=23..m=24 d=5, m=25..m=26 d=4, m=27..m=28 d=2, m=29..m=30 d=1
   (plus their one-past/death companions), m=31@z=61 / m=32@z=62
   frontier first contacts.
2. The trio-tracker appendices (kit-7 log S5 item 10, NON-BINDING
   observation candidates with single-datum provenance): the
   {19,19,19} status at m=19 z=56 (mimic UP 1v0 or conform) and
   z=57 (mimic DOWN 1v2 or conform).
3. The three registered trio mid-ladder slice probes (kit-7 log S5
   item 12 proposals, counter-probed at the original build): m=13@z=37
   (d=6, S_birth=39), m=15@z=43, m=17@z=49 — registered binding seat
   candidates EXACTLY TWO (stick DOWN + birth UP) + the non-binding
   trio tracker. REGISTERED WITH THE DATED CORRECTION: the published
   kit-7 log S5 item 12 lists z=42 (m=15) and z=48 (m=17); the
   engine-free re-derivation z(birth) = z*(m) + 2·(m−1)/2 gives z=43
   and z=49; no datum was affected (those rows were never measured
   anywhere before the concurrent kits of 2026-11-26).
4. The 16 below-frontier window rows (kit-7 frozen section (d) window
   proposals + log S5 item 13): m=29 z in {49..56}, m=30 z in
   {50..57}, registered candidates 0 separations each.
5. The single hole row (kit-7 log S5 item 11): m=26@z=25, registered
   candidate 0 separations (if clean, the m=26 measured line closes
   to {25..56}).
6. Inherited anchor chain: 141 published anchors verbatim + the 39
   kit-7 separation spots re-anchored at this build
   (machine-verified 39/39 on the published canonical engine BEFORE
   any row of this kit ran, before the reset).

## Measured outcome (machine observation, no claim)

- Battery 769/769 all-match; anchors 180/180 exact.
- 48 rows executed, 760 shapes, 54 separations: 46 registered seat
  separations ALL HIT and 8 UNREGISTERED stack-class separations
  (every deviation below is of the stack class; the two-token seat
  scaffold survived 100% here).
- Row verdicts (the 31 template rows): 25 FULL HIT + 6 DEVIATION (all
  stack-class), plus 17 clean plain-scan rows (16 windows + the hole
  row, 0 separations each):
  - m=19 z=56: registered EXACTLY ONE ({19,38} UP 1v0) HIT + extra
    {19,19,19}@S=57 UP 1v0 — the trio LIFECYCLE CONTINUES: the
    tracker's mimic candidate (UP 1v0) measured exactly.
  - m=19 z=57: registered EXACTLY TWO (stick {19,38} DOWN 1v2 + NEW
    {19,40}@S=59 UP 2v0) both HIT, plus THREE stack-class extras:
    {19,19,19}@S=57 DOWN 1v2 (the tracker's stick-mimic candidate
    measured exactly), and the birth-S=59 family members {19,19,21}
    and {19,20,20} (both UP 2v0). At this slice the ENTIRE in-sweep
    birth-sum family separates with identical signatures.
  - m=20 z=58: registered EXACTLY TWO both HIT, plus extra
    (20,20,20)@S=60 — the EVEN-m mid-slice (d=m/2=10, S_birth=3m=60)
    trio separates, exactly mirroring the odd-m mid-slice structure.
  - m=13 z=37, m=15 z=43, m=17 z=49: all three registered seat
    candidates HIT (stick DOWN 1v2 + NEW birth UP 2v0 each), plus the
    trio {m,m,m}@S=3m UP 2v0 separating at EVERY probe — the odd-m
    mid-slice trio separation now has FOUR witnesses (m ∈ {13,15,17,19})
    plus the even-m witness (m=20).
  - The other 22 registered template rows and the frontier 19th/20th
    datum candidates: FULL HIT exactly as registered. The m=29 z=58 /
    m=30 z=59 one-past rows add the first m=29/m=30 frontier decay
    datums of this census (odd 2→1 count -> 33, even 2→0 count -> 32).
- Frontier parity scaffold: m=31@z=61 {31,32}@S=63 UP 2v0 and
  m=32@z=62 (32,32)@S=64 UP 2v1 both HIT — the scaffold holds 20/20
  (m=13..32, per-row observations). DATED NOTE: publication priority
  for the m=31/m=32 datums belongs to the concurrent kit (7af915fb,
  10:54:57Z); this census was executed blind before that publication
  and agrees with it verbatim.
- Windows: all 16 rows clean — the below-frontier history of m=29 and
  m=30 opens with 16 clean rows. Hole row clean — the m=26 measured
  line CLOSES to {25..56} (the second fully-swept line of the series,
  after m=25 {25..55} by kit-7).
- Deaths witnessed: 10 NEW death datums (m=19/m=20 d=8, m=21/m=22 d=4,
  m=23/m=24 d=3, m=25/m=26 d=2, m=29/m=30 d=0 — the first m=29 and
  m=30 deaths) plus TWO re-verified duplicates (see the
  double-registration disclosure below).
- DATED DISCLOSURE (2026-11-26, discovered at audit time of this
  kit): the published kit-7 frozen section (d) double-registered TWO
  rows that kit-7 itself had already measured — m=27@z=56 and m=28@z=57
  (each registered verbatim by kit-6 S5 items 21/24, measured by kit-7
  as its items 21/24, then re-registered in kit-7's own section (d)).
  This kit took them as the kit-8 binding candidates they were frozen
  as; both measured EXACTLY the published kit-7 values ({27,30}@S=57 UP
  1v0 and (28,30)@S=58 DOWN 0v1), so the duplicate registration acts as
  a blind re-verification, not a new datum. Counted above as
  re-verified duplicates, NOT as new deaths (the first m=27/m=28 death
  datums remain kit-7's).
- The m=19 trio now has a THREE-SLICE measured lifecycle (birth UP 2v0
  at z=55 [kit-7] → one-past UP 1v0 at z=56 → stick DOWN 1v2 at z=57 —
  an exact mimic of the co-token seat's life at the same S), and the
  S=57 family (both in-sweep members) and the S=59 family (all three
  in-sweep members) separate with IDENTICAL per-sum signatures at
  every measured slice.

## Concurrent double-census cross-verification (dated)

The concurrent kit (7af915fb, dir
`strip-newband-m31m32-ladders-trio-20261126`) and this kit measured
the same 48 (m,z) rows from the same kit-7 registrations with
independently written explorers, independent battery chains (theirs
1004 literals, mine 769) and slightly different sweep domains (theirs
S in {m..max(m+38,z+2)} everywhere; mine m+38 except the two disclosed
birth-seat extensions). Blind comparison of the two published outputs:

- All 48/48 common rows have IDENTICAL separation sets (shape, S,
  value, collapse, direction — 54/54 separations agree exactly,
  including every stack-class deviation).
- All 180 published anchor spots re-measured by BOTH censi value-agree
  (179 distinct (R,X,z) spots; the duplicate key is a registered
  double-mention, disclosed above).
- Dead shape conformance, windows/hole cleanliness, and the frontier
  19th/20th datums agree verbatim.

Two blind independent executions of the same registered targets
agreeing measure-for-measure is the strongest reproducibility record of
the series so far. No universal claim is made from it.

## The sum-only value witness (candidate law L8)

The six deviation rows all share one numeric signature: shapes with the
same (S, z, R) measured the same value while separating from the
collapse. This motivated the candidate law L8 (falsifiable by any
future row recording an in-sweep same-S family disagreement): on
x0-style rows the measured engine value is a function of (S, z, R)
alone — seats ARE sums; the stacked-trio and stack-variant shadows are
then NECESSARY seats of their sums, and future registered birth-row
candidates on m ≤ 20 lines should count the whole in-sweep birth-S
FAMILY, not the co-token shape alone.

Post-recovery re-probe evidence (fresh, published in this directory;
the pre-reset probe artifacts are lost and none of their numbers is
claimed):

- In-row (audit re-check): 32 multi-shape sum-families inside the 48
  frozen rows, 32 agree, 0 violations.
- `sumonly_probe.py` R1: m ∈ {13..19}, z ∈ {25..66}, R=z+m+1, sweep
  m ≤ S ≤ min(m+38, z+2): 7,293 positions, 994 multi-shape sum-families,
  994 agree, 0 violations.
- `sumonly_probe.py` R2: the measured mid-ladder slices m ∈
  {13,15,17,19,20}, trio {m,m,m} vs the same-S birth seat under R
  offsets {-3,-2,-1,+1,+2,+3}: 30 checks, 30 agree, 0 violations.

L8 is a finite-observation candidate law, NOT a theorem; the K0832
closed form remains the only PROVED statement. Non-binding L8
family-count trackers for the frozen kit-9 rows are registered in the
log S5 (m=19 z=59 expected in-sweep birth-S=61 family size 4;
m=20 z=60 expected family size 3; the binding registered rows stay
verbatim two-separation candidates).

## Next-kit handoff (reconciled)

The OPERATIVE kit-9 bindings are the ones published by the concurrent
kit (7af915fb; 34 binding rows incl. the d=11 stack-split candidates +
m=33@z=65 / m=34@z=66 frontier 21st/22nd candidates + m=31/m=32
window proposals). The frozen output section
`future_slice_registration_constants` of THIS kit registers the same 32
core binding rows (blind, identical targets where they overlap); this
kit's log S5 adds NON-BINDING supplementary trackers on top (L8
family-size expectations, even-m mid-slice probe proposals m=14 z=40 /
m=16 z=46 / m=18 z=52 — counter-probe before registering — and the
trio death expectation at m=19 z=58). See
`research/log/2026-11-26-m31m32-laddercont-midtrio-windows-predecl-microkit.md`.

No K slot is claimed here, no residual verdict is consumed, and no
universal claim is made; the standard 11x11 cell remains UNKNOWN at all
times; this kit does not touch it.
11x11 cell remains UNKNOWN at all
times; this kit does not touch it.
