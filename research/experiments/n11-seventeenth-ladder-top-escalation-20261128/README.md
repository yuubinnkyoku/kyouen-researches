# n11 seventeenth ladder-top escalation 2026-11-28

Execution kit of the escalation declared in
`research/log/2026-11-28-n11-seventeenth-ladder-top-escalation-declaration.md`
(publish-then-execute, declaration commit `207339c8`, single owner).
Escalates the four remaining keys of the published sixteenth
ladder-top selection (class 20421 `1155173304420536320:131072`)
against the canonical head of record `dbc1d950...` (6,901 rows
WIN 219 / LOSS 6,682, the sixteenth k01 adoption head).

## Result

Declared order k02 -> k03 -> k04 -> k05, WIN-stop at the first
WIN(1).

| key | stage-1 2M (published sixteenth kit) | 15M escalation | pair |
|---|---|---|---|
| k02 `1156299204327378944:131072` (s5 543795, legal 73) | UNKNOWN(0), nodes 2,000,000 | **WIN(1), nodes 4,997,146** (33.3% of budget), wall_s 24/25 | node-identical |
| k03 `1155173441859489792:131072` (s5 605961, legal 73) | UNKNOWN(0), nodes 2,000,000 | not escalated (WIN-stop) | - |
| k04 `1153062242096250880:540672` (s5 620742, legal 83) | UNKNOWN(0), nodes 2,000,000 | not escalated (WIN-stop) | - |
| k05 `1152921642046849024:68719477248` (s5 625899, legal 78) | UNKNOWN(0), nodes 2,000,000 | not escalated (WIN-stop) | - |

The WIN-stop rule fired at k02 (WIN(1) at 15M, cold pair
node-identical); k03-k05 stay at their published stage-1 2M
UNKNOWN(0).

Calibration (after the declaration, before the runs): u01
`1153485622925590528:0` at 2M reproduces the published
calibration VALUES exactly (result 0, nodes 2,000,000, forbidden
quadruples 95,670, wall_s 9); the input csv is byte-identical to
the published calibration (`52d79efc`).

Freshness to the current head (disclosed, host-measured): the only
delta between `58110025...` (6,900 rows) and `dbc1d950...`
(6,901 rows) is the adopted k01 WIN row; k02-k05 are measured
fresh to `dbc1d950...`.

Owner-union precheck (re-derived on this host from the frozen
graph `54f9c364`, identical to the published sixteenth precheck):
k02 [16104, 16132, 16656, 20421] / k03 [18136, 18143, 20128,
20421] / k04 [18534, 18554, 19885, 20421] / k05 [18683, 18710,
20421]; serving class 20421 is ladder rank 1 (unknown_now 4
after the k01 adoption).

## Claim status

This kit is escalation bookkeeping only: NO verdict is consumed.
The k02 WIN(1) row is single-implementation (jsreplay replica,
cold pair) and requires the C++ second-implementation scrutiny
gate plus a third-implementation corroboration before any
adoption Part; a k02 adoption would additionally require the
standing WIN-side flip-census review.  Class 20421 is NOT
complete (k03-k05 remain unknown).  The standard 11x11 empty
board, all 19 central-reply roots, the two-stone root {60,27}
and third moves 100/108 remain UNKNOWN.  Nodes, expansions and
wall_s are bookkeeping, never verdicts.
