# 2026-11-28 n11 fifteenth class 5804 k02/k03 re-escalation complete

Completion log of the Part declared in
`research/log/2026-11-28-n11-fifteenth-ladder-top-k02k03-reescalation-declaration.md`
(declaration commit `88a24418`, single owner, publish-then-execute;
the host calibration and both 15M cold pairs ran only after the
declaration was on main).

## Results

- Calibration (u01 `1153485622925590528:0` at 2M, run after the
  declaration): result 0, nodes 2,000,000, forbidden quadruples
  95,670, wall_s 9 - values identical to the published fifteenth
  escalation kit's calibration raw (only stdout footer line order
  differs per host buffering; this host's raw sha `1c82d7da`).
- **k02 `6052837899185946628:128` (s5 index 212115, legal 87) at
  15M: UNKNOWN(0), nodes 15,000,000 (budget exhausted)**, cold
  pair node-identical (wall_s 80/80, raws `6a3db900`/`ccb8a09d`).
  k02 stays UNKNOWN; parking/L50M only under a future declaration.
- **k03 `6053400849139367936:128` (s5 index 212536, legal 92) at
  15M: WIN(1), nodes 3,364,655**, cold pair fully byte-identical
  (wall_s 15/15, raws `58f2ad9d` both).
- WIN-stop rule re-affirmed but NOT fired: k02 did not resolve
  WIN(1), so k03 escalated per the declared order.
- Class-status bookkeeping unchanged: class 5804 was ALREADY
  excluded_now (k01 WIN win-hit, published reaudit `3395d0ec`); the
  k03 WIN changes no census quantity; the class is NOT complete
  (k02 remains unknown).
- Kit `n11-fifteenth-ladder-top-k02k03-reescalation-20261128`:
  batch-summary `b2fb5006` (schema
  `n11-fifteenth-ladder-top-k02k03-reescalation-summary-v1`),
  README `a3a1049b`, declaration mirror `dadc375e`, input CSVs
  byte-verified copies of the published fifteenth escalation kit
  inputs (k02 `fda5d01d`, k03 `cad75b29`, cal `52d79efc`), 5 raws.
  Runner jsreplay `84585617` sha-verified before the runs.

## Honest disclosures

- Both keys were verified FRESH to the head of record `b5f322dd`
  (6,898 rows WIN 216 / LOSS 6,682) before any run (exact (lo,hi)
  column probe: 0 rows each).
- Fetch-back verification window: the raw CDN served this private
  repository's commit-pinned files earlier in this execution (the
  reaudit kit 10/10 and completion log fetch-backs were byte-exact
  then), but went 404 for ALL raw paths (including previously
  verified ones) before this Part's pushes; the GitHub App read
  endpoints were also 404-flaky throughout. The declaration's
  byte-identity therefore rests on the push_files content route
  (proven byte-exact on every fetch-back that was possible this
  execution) plus the local sha `dadc375e`; the kit and this log's
  fetch-back verification is to be repeated at the next
  opportunity and is NOT claimed as done here.
- Wall-clock: cal 9s; k02 15M 80s/run x2; k03 15M 15s/run x2.

## Next

- k03 WIN(1) is single-implementation (jsreplay): a k03 adoption
  requires the C++ second-implementation scrutiny gate
  (expected gate row `92,15000000,1,3364655` @15M cap) plus a
  third-implementation corroboration, under fresh declarations.
- k02 parking/L50M escalation only under a future declaration.
- Class 5804 completion still blocked on k02 (15M UNKNOWN).

## Claim status

Re-escalation bookkeeping only: NO verdict is consumed, no
class-status change, no coverage claim. The standard 11x11 empty
board, all 19 central-reply roots, the two-stone root {60,27}, the
third-move pair {100,108} and every closure class stay UNKNOWN.
Nodes are bookkeeping, never verdicts.
(declaration `88a24418`, kit this commit)
