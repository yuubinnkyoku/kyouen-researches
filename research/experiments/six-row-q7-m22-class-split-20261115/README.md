# six-row q=7 m=22 class-split sweep — pivoted away (negative calibration record)

Date: 2026-11-15 (UTC). Fast lane.

## Scope (originally claimed)

Full 35 row-mirror-canonical deficiency-class sweep of the **6x22 q=7** frontier width.
Machinery identical to K0818/K0819/K0829 (sat3.js class-split encoder on the K0810 census,
official kissat 4.0.4 linux-amd64 binary), positive control 6x21 q=7 class {2}
(1,904,706 conflicts) reproduced **bit-exact** before the sweep.

## Outcome: difficulty calibration — sweep abandoned at 240 s per-class caps

The class-split difficulty collapse that carried 6x19/6x20 q=8 and 6x21 q=7 does **not**
reach 6x22 q=7 under this lane's time budget:

- 6x21 q=7 class {2} positive control: bit-exact reproduction (1,904,706 conflicts) —
  machinery confirmed live.
- 6x22 q=7 singletons {0} and {1} and the all-rows class {0,1,2,3,4,5}: each INDET past
  240 s caps at >2.0M conflicts per class (per-class logs lost to a sandbox environment
  reset mid-session; conflict magnitudes observed pre-reset).
- Calibration reference: the **entire** 6x20 q=8 35-class sweep (K0819) consumed 16.4M
  conflicts total; here a single class exceeds 2M conflicts within 240 s without
  terminating — per-class difficulty is estimated at 15-30x the 6x20 q=8 total.
- Probe: 6x24 q=6 all-rows instance INDET at 220 s with 1,751,133 conflicts (log retained
  locally; not pushed — probe only).
- Conclusion: the six-row frontier (6,5)/(6,6)/(6,7) class-splits need either much longer
  per-class budgets, kxminpos-style decompositions per class, or the long-horizon lane.
  This fast-lane run pivoted to completing **five-row q=7 m=22** instead (takeover claim
  in ../five-row-q7-m22-class-split-20261114/README.md).

## Not claimed

- Any 6x22 resolution (all 35 classes remain UNDECIDED), any other (w,q),
  11x11 empty board / two-stone root / S2 / class 2 / class 4 (all remain UNKNOWN).

## Status

CLOSED (pivoted) by the fast lane. A future lane may re-open with decomposition-based
or long-budget plans; the positive-control reproduction above is reusable calibration.
