# n11 eighteenth ladder-top escalation 2026-11-28

Execution kit of the escalation declared in
`research/log/2026-11-28-n11-eighteenth-ladder-top-escalation-declaration.md`
(publish-then-execute, declaration commit `53749821`, single
owner). Escalates the three remaining keys of the published
sixteenth ladder-top selection (class 20421
`1155173304420536320:131072`) against the canonical head of
record `e56ca5ca...` (6,902 rows WIN 220 / LOSS 6,682, the
seventeenth k02 adoption head).

## Result

Declared order k03 -> k04 -> k05, WIN-stop at the first WIN(1).

| key | stage-1 2M (published sixteenth kit) | 15M escalation | pair |
|---|---|---|---|
| k03 `1155173441859489792:131072` (s5 605961, legal 73) | UNKNOWN(0), nodes 2,000,000 | **WIN(1), nodes 5,266,012** (35.1% of budget), wall_s 26/26 | node-identical (raws byte-identical `a80c2dcb`) |
| k04 `1153062242096250880:540672` (s5 620742, legal 83) | UNKNOWN(0), nodes 2,000,000 | not escalated (WIN-stop) | - |
| k05 `1152921642046849024:68719477248` (s5 625899, legal 78) | UNKNOWN(0), nodes 2,000,000 | not escalated (WIN-stop) | - |

The WIN-stop rule fired at k03 (WIN(1) at 15M, cold pair
node-identical); k04-k05 stay at their published stage-1 2M
UNKNOWN(0).

Calibration (after the declaration, before the runs): u01
`1153485622925590528:0` at 2M reproduces the published
calibration VALUES exactly (result 0, nodes 2,000,000, forbidden
quadruples 95,670, wall_s 9); the input csv is byte-identical to
the published calibration (`52d79efc`).

Freshness to the current head (disclosed, host-measured): direct
row scan of `e56ca5ca...` (6,902 rows) gives 0 rows for each of
k03/k04/k05; the only delta from the sixteenth k01 head
`dbc1d950...` (6,901 rows) is the adopted k02 WIN row, present
exactly once.

Owner-union precheck (identical to the published seventeenth
precheck, frozen graph `54f9c364`): k03 [18136, 18143, 20128,
20421] / k04 [18534, 18554, 19885, 20421] / k05 [18683, 18710,
20421]; serving class 20421 is ladder rank 1 (unknown_now 3
after the k02 adoption).

## Claim status

This kit is escalation bookkeeping only: NO verdict is consumed.
The k03 WIN(1) row is single-implementation (jsreplay replica,
cold pair) and requires the C++ second-implementation scrutiny
gate plus a third-implementation corroboration before any
adoption Part; a k03 adoption would additionally require the
standing WIN-side flip-census review. Class 20421 is NOT complete
(k04-k05 remain unknown). The standard 11x11 empty board, all 19
central-reply roots, the two-stone root {60,27} and third moves
100/108 remain UNKNOWN. Nodes, expansions and wall_s are
bookkeeping, never verdicts.

## Files

- DECLARATION.md - the Part declaration (copy of the published log).
- batch-summary.json - machine summary (schema
  `n11-eighteenth-ladder-top-escalation-summary-v1`).
- cal-u01.input.csv / k03.input.csv / k04.input.csv /
  k05.input.csv - byte-identical copies of the published
  seventeenth escalation kit inputs (`52d79efc` / `ff63ed29` /
  `5ee6e813` / `565a6505`).
- raws/cal-u01-at2m.raw / raws/at15m-k03-p1.raw /
  raws/at15m-k03-p2.raw - run raws (k03 pair byte-identical).
- MANIFEST-sha256.txt - sha256 of every published file.

## Run environment

Node.js v22.20.0 on the lane host; runner jsreplay.js sha256
`84585617...` (published pinned replica of the C++ standalone
exact-replay path at commit `154f3b7a`), re-fetched this session
from the published twelfth-cost kit and sha-verified. This lane
runs without access to the user's computer (scheduled task);
publication is via the GitHub API only.
