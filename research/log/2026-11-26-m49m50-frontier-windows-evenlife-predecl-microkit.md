# 2026-11-26 kit-17: strip-newband m49/m50 frontier first-contact + m47/m48 in-band windows + even-m z=3m+14 + ladder next-depth pre-declaration micro-kit (log)

## S1 Scope

High-speed lane, self-execution. Resume point taken from the kit-16 record
of record at main commit f997daca (frozen .out sha256 85c04e43...,
442,100 bytes): the 34 future_slice_registration_constants were the sole
registration authority (28 ladder m=19..32 one-past/birth pairs at the next
depth, frontier 36th/37th m=49@z=97 / m=50@z=98, window proposals m=47
z{85..92} / m=48 z{86..93}, even-m z=3m+14 contingent continuation,
odd-m close-out note). Latest main was re-fetched before build and again
before every push; the kit-17 territory (m49/m50, kit-17 dir, frontier_m49
probes) was free of counter-probes at build time and at every push time
(the concurrent activity in the 21:15-21:42Z window was the part-SV
long-lane adoption series, disjoint territory).

## S2 Registration (register-before-measure, intact)

The kit-16 frozen .out is a PUBLISHED pre-declaration: every binding row
measured here was machine-derived from its constants before the frozen
run. gen_kit17.py (generator, not published; re-runnable from the kit-16
published bytes; transform_lib extended with the 36th/37th ordinal labels)
asserts the full kit-16 record of record as a precondition (49 rows /
183 separations / 30 binding FULL HIT / evenlife 3/3 EXACT / trio conform)
and the zero-overlap property (all 49 kit-16 row names absent from the
kit-17 row list) BEFORE emitting a single row. Standing rule v2 is applied
to EVERY 2-token seat with co >= 2m (boundary co = 2m included), both
sides (one-past / stick / NEW) wherever admissible.

## S3 Frozen census (49 rows, 211 separations, all finite observations)

- explorer explore_m49m50_frontier_windows_evenlife.py sha256 32f1c683...
  (259,918 bytes); frozen official output .out sha256 420d1c83...
  (496,038 bytes, one JSON line).
- 30 binding rows ALL FULL HIT, ZERO unregistered separations (154
  separations in the binding rows, every one a registered seat or an
  exact-mimic rule-v2 shadow).
- frontier 36th/37th parity datums BOTH EXACT, FIRST-EVER m>48 rows:
  m=49@z=97 {49,50}@S=99 UP 2v0 (v(99,97,147)=0) / m=50@z=98
  (50,50)@S=100 UP 2v1 (v(100,98,149)=1). Scaffold count 38/38 (m=13..50).
- windows m=47 z{85..92} / m=48 z{86..93}: 16/16 CLEAN. Measured bands
  now m=47 {85..93}, m=48 {86..94}.
- even-m z=3m+14 (m=14/16/18): 3/3 EXACT. stick {m,2m+14}@S=3m+14 DOWN
  0v2 + NEW {m,2m+16}@S=3m+16 UP 2v1 + 17 exact-mimic shadows per row
  (8 stick + 9 NEW splits) + trio conform. Chain z=3m-1..3m+14.
- early-follow 7th consecutive pre-registered confirmation: m19 z74
  one-past full 10-split shadow set of co=56 (host UP 1v0, value 1);
  m20 z75 full 9-split set (host DOWN 0v1, value 0).
- boundary equistack 3rd observation, one-past side, co=2m exactly, first
  at odd m: m=25 one-past seat {25,50}@S=75 co=50=2m; the single admissible
  split {25,25,25} separates as an exact mimic (both value 1, UP).
- ladder m19/m20 now at birth z=75/76 (new series-deepest); m21..m32 at
  their registered next depths.
- battery 2,162/2,162 (2,098 kit-16 carried + 64 new, closed == vC == vO).
- anchors 1,210/1,210 (1,027 kit-16 anchors byte-carried + 183 kit-16
  census separation spots first-anchored here), all reproduce exactly.
- total separations 211 == the data-driven registered count (audit G8).

## S4 Verification

- determinism: 4 byte-identical runs (default x2, PYTHONHASHSEED=random,
  PYTHONHASHSEED=12345), all sha256 420d1c83... on the FINAL explorer
  bytes 32f1c683....
- derive_check_kit17.py: 3,205 checks DERIVE-PASS (engine-free, closed
  form only), including FRESH-label assertions, rule-v2 completeness per
  seat, K1268 z* arithmetic, the kit-18 frontier/window arithmetic, and
  the carried-battery/new-literal v/vC/vO equality.
- audit_kit17.py: 20/20 gates PASS, two runs byte-identical JSON
  (4536f75b...). Gates: engine pin, battery count/recompute, anchor
  count/recompute, row-count-49, full row sweep recompute, registered-count
  equality, both frontier datums, 16 window rows clean, evenlife template,
  rule-v2/early-follow/boundary-equistack, no-unregistered-separations +
  seat-value checks, future constants 34 + frontier 38th/39th + window
  arithmetic, kit-16 duplicate guard (49 names), dead-seat conform.
- tamper battery 3/3 fail-closed on scratch copies (frozen bytes never
  touched, byte-verified unchanged after the battery): T1 battery closed
  flip -> G3; T2 frontier m49 datum value flip -> G7+G9+G14; T3 anchor
  published_value flip -> G4. Clean control AUDIT-PASS on the frozen
  bytes afterwards.

## S5 Registration for kit-18 (frozen, engine-free, NOT measured here)

34 future constants in the frozen .out section
future_slice_registration_constants: 28 ladder next-depth one-past/birth
pairs m=19..m=32 (rule-v2 stack lists FRESH), frontier 38th/39th
m=51@z=101 {51,52}@S=103 UP 2v0 (v(103,101,153)=0) / m=52@z=102
(52,52)@S=104 UP 2v1 (v(104,102,155)=1), window proposals m=49 z{89..96}
/ m=50 z{90..97} (z*(m)=2m-2+(m mod 2)), even-m z=3m+16 contingent
continuation, odd-m close-out note. The kit-18 registration authority is
this published frozen .out at the wave-C commit.

## S6 Honest disclosure

1. PRE-FREEZE arithmetic error caught by derive_check (fail-closed as
   designed): the first explorer build (sha256 03f04f31...) mis-registered
   the kit-18 window proposals as m=49 z{91..98} / m=50 z{92..99}; the
   correct z*(m)-8..-1 arithmetic is {89..96} / {90..97}. The error was in
   the UNMEASURED future-constants section only (the first build's 4-run
   determinism battery, 211 separations and all measured values were
   byte-identical to the final build's). The explorer was regenerated
   (32f1c683...) and the ENTIRE battery (4 determinism runs, derive,
   audit x2, tamper 3/3, clean control) was re-executed on the final
   bytes. derive_check now gates the window arithmetic explicitly.
2. Sandbox resets during the determinism battery: a two-run single
   command exceeded the 290 s wall (lesson reconfirmed: ONE heavy command
   per shell call, eighth occurrence); a follow-up run in the same shell
   was OOM-killed (rc 137) and was re-run cleanly in a fresh command. All
   work products live in the persistent knowledge mount; no bytes were
   lost, no measurement was redone after the freeze.
3. Registration-source discipline: the K17 future texts embedded in the
   kit-16 frozen .out carry FRESH seat labels (kit-16 emitted FRESH),
   asserted at generation and re-asserted by derive_check; the kit-18
   texts emitted here are composed FRESH likewise.
4. transform_lib (generator-side, unpublished) was extended with the
   36th/37th frontier ordinal labels; no published artifact depends on
   the extension.
5. All pins in this log were machine-extracted; no hand-typed 64-hex
   strings anywhere in the publish path (verified by construction: the
   push payload was assembled programmatically with the shas printed by
   the generation/verification runs).

## S7 Standing caveats

Finite observations only; no universal claim. The frontier parity count
38/38 (m=13..50), the rule-v2 shadow mimic observations (early-follow
7/7, boundary equistack 3 observations), and the even-m lifecycle template
(through z=3m+14) are observation counts, not laws. The standard 11x11
empty board, all 19 central-reply roots, the two-stone root {60,27}, the
third-move {100,108}, S2, and closure classes 1/2/4 remain UNKNOWN at all
times. No verdict is consumed. Nodes and shape counts are bookkeeping.
