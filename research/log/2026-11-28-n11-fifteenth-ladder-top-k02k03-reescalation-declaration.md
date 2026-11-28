# Declaration: n11 fifteenth class 5804 k02/k03 re-escalation (single-owner, publish-then-execute)

Single-owner declaration by the long-term 11x11 lane. Published BEFORE
any 15M run of this Part. Any parallel lane must not run these keys at
any budget above the published stage-1 2M until this Part's completion
log appears. Declaration HEAD pin: current main at push time.

## Scope

Re-escalation of the two WIN-stop-suppressed keys of the published
fifteenth ladder-top escalation (kit `n11-fifteenth-ladder-top-escalation-20261128`,
commit `a33217ca`, log `73b1610f`), whose WIN-stop fired on the k01
WIN(1) at 15M:

- k02 `6052837899185946628:128` (s5_index 212115, legal 87, stage-1
  2M UNKNOWN, raws `55ea4986`/`03c3af56`)
- k03 `6053400849139367936:128` (s5_index 212536, legal 92, stage-1
  2M UNKNOWN, raws `07f6b1be`/`07f6b1be`, byte-identical pair)

Head basis: current canonical head of record `b5f322dd...`
(6,898 rows WIN 216 / LOSS 6,682, adopted at `53f6a8f5`+`218ba20d`);
both keys verified fresh to the head before any run. Class 5804 is
ALREADY excluded_now (k01 WIN win-hit, measured by the published
fifteenth reaudit kit `3395d0ec`, census unknown 34,369 / excluded_now
151); these re-escalations are class-completion bookkeeping only.

## Method (publish-then-execute)

1. Host calibration BEFORE the declared runs: jsreplay
   `84585617...` at 2M on cal-u01 `1153485622925590528:0` must
   reproduce the published calibration raw VALUES (result 0, nodes
   2,000,000, forbidden quadruples 95,670; stdout footer line order
   may differ per host buffering, raw sha may differ, values must
   not).
2. Declared order: k02 first, then k03 only if k02 does NOT resolve
   WIN(1). Budget 15,000,000, cold pair (two sequential fresh runs)
   per escalated key; pair must be node-identical (WIN/LOSS/UNKNOWN
   and nodes equal; wall_s may differ). Re-affirmed batch WIN-stop:
   if k02 resolves WIN(1) at 15M, k03 stays suppressed (2M UNKNOWN).
3. Runner: node jsreplay.js `--n=11 --memo=22 --only=5
   --exact-replay=<csv> --exact-replay-budget=15000000`; input CSVs
   byte-identical to the published escalation kit's `k02.input.csv`
   (`fda5d01d`) / `k03.input.csv` (`cad75b29`).

## Non-meaning

NO verdict is consumed. Class-status does not change (5804 is
already excluded_now; a LOSS on k02/k03 does not free the class
while k01's WIN stands). No root freed, no coverage claim. The
standard 11x11 empty board, all 19 central-reply roots, the two-stone
root {60,27}, the third-move pair {100,108} and every closure class
stay UNKNOWN. Nodes are bookkeeping, never verdicts.

## Disclosures

- This lane runs without access to the user's computer (scheduled
  task); publication is via the GitHub API only.
- The GitHub App read endpoints were flaky (404) in the preceding
  execution; all pre-run pin verification uses local byte-verified
  copies of the published kit plus commit-pinned raw CDN where full
  commit shas are known.
- Any WIN at 15M is single-implementation (jsreplay) and requires the
  C++ second-implementation scrutiny gate plus third-implementation
  corroboration before any adoption Part.
