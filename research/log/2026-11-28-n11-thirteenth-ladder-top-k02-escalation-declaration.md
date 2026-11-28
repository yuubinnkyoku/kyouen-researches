# 2026-11-28 n11 thirteenth ladder-top k02 escalation declaration

Single-owner declaration (publish-then-execute) for resolving k02
`1152922672837951488:65792` (class 16757, legal 72, s5_index 558553),
the second and last remaining unknown S5 key of the thirteenth
ladder-top selected class 16757
(`1153204079095185408:65536`, selection kit `fa4e6cb2`, escalation
kit `12d8359c`).  k02 is currently stage-1 2M UNKNOWN (cold pair
byte-identical, escalation suppressed by the k01 WIN-stop rule).
k01 is pillar-complete (cppgate GATE-PASS + thirdimpl
CORROBORATION-PASS, kits commit `f1f5c49d`, log `8dcb00fd`); k02
resolution is required for class 16757 completion (a candidate
free_now flip, Board-verified at adoption time).

## Declared procedure (publish-then-execute)

Runner: jsreplay.js `84585617...`, `--only=5 --memo=22`, cold solver
per row, no shared TT, cold pair (two passes, byte-identical
acceptance), head of record `beecb024...` (6,894 rows WIN 212 /
LOSS 6,682; k02 verified fresh/absent by the selection Part).

1. Stage-2 15M: cold pair at `--exact-replay-budget=15000000`.
2. If UNKNOWN at 15M: stage-3 L50M: cold pair at
   `--exact-replay-budget=50000000`.
3. Any result (WIN/LOSS/UNKNOWN at either budget) is recorded as
   measured; no parking beyond L50M in this Part.

Only key `1152922672837951488:65792` may be run in this Part, at the
declared budgets.  NO verdict is consumed by this Part; any WIN/LOSS
row is single-implementation (jsreplay replica) until the two-pillar
requirement (C++ scrutiny gate + third-impl corroboration) is closed
under a separate declaration, and class 16757 adoption additionally
requires the standing WIN-side flip-census review and Board-verified
free_now at adoption time.  The standard 11x11 empty board, the
two-stone root {60,27} and its remaining third moves 100/108 stay
UNKNOWN.  Nodes are bookkeeping, never verdicts.

The k02 runs happen only AFTER this declaration is on main.
