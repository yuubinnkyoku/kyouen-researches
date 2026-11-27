# n11 ultra-cheap u02/u03/u04 escalation completion (2026-11-27)

Completion log of the single-owner escalation declared in
`research/log/2026-11-27-n11-ultra-cheap-u02u03u04-escalation-declaration.md`
(commit `37f1e9f6`).  Kit:
`research/experiments/n11-ultra-cheap-u02-escalation-15m-20261127/`.

## Outcome

- Declared order u02 -> u03 -> u04, 15,000,000 budget, cold pair per key,
  WIN-stop rule active, runner jsreplay.js `84585617...` (byte-verified
  clone of the published twelfth selection kit script), head basis
  `0ec4080d` (6,891 rows WIN 209 / LOSS 6,682, fetched from main,
  sha-verified; u02/u03/u04 verified fresh/absent, u01 WIN row verified
  present).
- **u02 `1297036830121656320:131074` (class 2251, legal 80, s5 index
  93815) resolves WIN(1) at nodes 3,167,121** - cold pair node-identical
  and fully byte-identical (both passes wall_s 15).  Execution wall:
  ~15s per pass.
- WIN-stop rule fired at u02: u03 (`1153202979851993088:272`, class
  16371) and u04 (`1152921505747697664:1032`, class 23101) stay
  **UNKNOWN at 2M**; they were NOT run at any budget in this Part (no
  overreach).  Parking/L50M for them only under a future declaration.
- Pre-declaration calibration (disclosed in the declaration): u01 at 2M
  reproduces the published batch raw exactly (result 0, nodes 2,000,000,
  wall_s 9); published as `raws/cal-u01-at2m.raw`.

## Status guard

The u02 row is a single-implementation (replica) cache-bookkeeping row:
NOT a class closure, NOT a root verdict, transfers nothing.  Before any
adoption it requires the C++ second-implementation scrutiny gate plus a
third-implementation corroboration (separate Parts), and a u02 adoption
would additionally require the standing WIN-side flip-census review
(class 2251 would be Board-verified free_now at adoption time).  The
standard 11x11 empty board, the two-stone root {60,27} and its remaining
third moves 100/108 stay UNKNOWN.

## Follow-up ownership

The u02 WIN-row pillars (C++ gate expected `80,15000000,1,3167121` +
third-impl corroboration) are the immediate next Part of this lane
(single-owner, fresh declaration).  After 3/3 pillars: the adoption Part
(BASE `0ec4080d`, fresh single-owner declaration, WIN/LOSS conflict
review, merger `90711961`, flip-census/reaudit) - same flow as the u01
adoption completed at commit `d4a9486f`.
