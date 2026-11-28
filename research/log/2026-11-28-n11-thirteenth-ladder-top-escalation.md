# 2026-11-28 n11 thirteenth ladder-top escalation (class 16757)

Completion log of the escalation declared in
`2026-11-28-n11-thirteenth-ladder-top-escalation-declaration.md`
(declaration commit `07003c2a`, single owner, publish-then-execute).
Kit:
`research/experiments/n11-thirteenth-ladder-top-escalation-20261128/`.
Selection basis: the thirteenth ladder-top selection kit
(`fa4e6cb2`, log `2ca98e1c`): class 16757
`1153204079095185408:65536`, k01 `1153204147814662144:65536`
(s5_index 556117, legal 72), k02 `1152922672837951488:65792`
(s5_index 558553, legal 72), head of record `beecb024...`
(6,894 rows WIN 212 / LOSS 6,682).

## Result (k01 WIN at 15M; WIN-stop rule fired)

Declared order k01 then k02, stage-1 2M cold pair each, then 15M
escalation under the WIN-stop rule (runner jsreplay
`84585617...`, `--only=5 --memo=22`, cold, no shared TT):

- stage-1 2M: k01 UNKNOWN(0) nodes 2,000,000; k02 UNKNOWN(0)
  nodes 2,000,000; both cold pairs byte-identical (wall_s 9 each)
- 15M escalation: **k01 WIN(1) nodes 2,678,305** (wall_s 12), cold
  pair fully byte-identical; WIN-stop rule fired, k02 escalation
  suppressed, k02 stays 2M UNKNOWN
- calibration u01 at 2M (pre-declaration, disclosed): result 0,
  nodes 2,000,000, forbidden quadruples 95,670, wall_s 9, identical
  to the published u03/u04 escalation kits' calibration raws
- no other key was run at any budget in this Part

## Claim status

Batch bookkeeping only: NO verdict consumed. The k01 WIN row is
single-implementation (jsreplay replica) and needs the C++
second-implementation scrutiny gate plus third-implementation
corroboration (and, at adoption, the standing WIN-side flip-census
review) before any adoption Part. Class 16757 is NOT complete: k02
is still unknown (parking/L50M only under a future declaration), so
no free_now flip is claimed here.

## Next work

- k01 WIN pillars: C++ scrutiny gate (gate source `9193f5b6` + zig
  `d45312e6`; expected `72,15000000,1,2678305`, cold pair, anchors
  3/3, tamper 4/4 fail-closed) + third_impl `08ea958f` corroboration
  (cap 400M / wallcap 260 / memo 22, two runs), under a separate
  single-owner declaration (u04 pillars kits `378ec332` / `2691ac04`
  as templates).
- k02 resolution (parked or L50M) needs its own declaration; class
  16757 completion additionally requires Board-verified free_now at
  adoption time.

## Guards

The standard 11x11 empty board: UNKNOWN. All 19 central-reply roots:
UNKNOWN. Two-stone root {60,27}: UNKNOWN. Third-move pair {100,108}:
UNKNOWN. Nodes are bookkeeping, never verdicts.
kit commit `12d8359cbcfe14e7c0fdd49d5cdd27d1e64a8a81`
