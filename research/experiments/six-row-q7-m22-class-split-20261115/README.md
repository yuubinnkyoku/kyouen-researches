# six-row q=7 m=22 class-split sweep — IN FLIGHT claim

Date: 2026-11-15 (UTC). Fast lane.

## Scope (claimed)

Full 35 row-mirror-canonical deficiency-class sweep of the **6x22 q=7** frontier width
(the unresolved witness-search frontier of M_{6,7} after the six-row-q7-m21-class-split
SAT witness at 6x21). Machinery identical to K0818/K0819/K0829 (sat3.js class-split encoder
on the K0810 census, byte-identical scripts from six-row-q7-m21-class-split-20261114,
official kissat 4.0.4 linux-amd64 binary), 2 parallel workers, per-class caps starting at
280 s with escalation (longer caps / --lex=H cross-encoding) for INDET classes.

Any outcome is in scope: all-UNSAT gives a witness-free width 22 (M_{6,7} in {22} or >= 23,
upper 402 unchanged); any SAT class decodes to a deficient maximal witness
(M_{6,7} >= 23). Positive control 6x21 q=7 class {2} (K0815/K0829-lane SAT witness,
1,904,706 conflicts) is re-run first and must reproduce bit-exact before the sweep.

## Not claimed

- 6x21 (already resolved SAT), any other (w,q), nonexistence at widths beyond 22,
  11x11 empty board / two-stone root / S2 / class 2 / class 4 (all remain UNKNOWN).

## Status

IN FLIGHT — computation starting; results to be pushed to this directory.
