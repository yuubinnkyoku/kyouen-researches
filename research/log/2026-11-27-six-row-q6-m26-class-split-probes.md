# 2026-11-27 Six-row q=6, 6x26: class {2} krow/minpos probes — 4 INDET honest negatives

## Status

Complete, published. Declaration `02e40e9e`
(`research/log/2026-11-27-six-row-q6-m26-class-split-declaration.md`),
kit `c4d2e9dbb0`
(`research/experiments/six-row-q6-m26-class-split-20261127/`,
fetch-back 17/17 byte-identical; csv byte-verified against main).

## Result

Motivated by the same-day (6,7) 6x22 SAT resolution
(`six-row-q7-m22-class-split-20261127`, M_{6,7} >= 23), the krow/minpos
decomposition was applied to the (6,6) frontier 6x26, class {2} krow=2:4
(the 29-stone single-deficiency family of the m=24/m=25 witnesses):

- minpos 10/11/12/13: all **INDET** at 272s caps — 3,729,885 /
  3,969,268 / 3,862,795 / 4,123,449 conflicts. Honest negatives, not
  absence.
- **M_{6,6} stays in [26, 495]; the frontier stays 6x26.** The
  near-uniform ~3.7-4.1M resistance band suggests (6,6) 6x26 does not
  crack as easily as (6,7) 6x22 did at the same caps.
- Positive control: 6x25 class {2} krow=2:4 minpos=11 SAT, 3,574,244
  conflicts — the published K1217 value reproduced bit-exactly.

Remaining: minpos P = 0..9, 14..22, class {1} krow splits, other canonical
classes, three-edit surgery of the m=25 K1217 witness on 6x26.

## Scope

Honest negatives only; no absence claim at any width. Standard 11x11 empty
board, two-stone roots, third move, S2, closure classes: UNKNOWN at all
times; verdicts not consumed.
