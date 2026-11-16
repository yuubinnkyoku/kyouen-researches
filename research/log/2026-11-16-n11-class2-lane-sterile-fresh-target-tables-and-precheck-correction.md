# class2-lane: sterile-row fresh-target tables + cost-62 pre-check CORRECTION (2026-11-16)

## Correction (supersedes the earlier pre-check log)

- The earlier cost-62 pre-check claimed both 70j-covering roots of the record's candidate 00000000000000801282020000000000 (bits 21/109) are fresh targets. **WRONG**: the covering roots are 70j+bit41 and yflip(70j)+bit41; bits 41/85 are legal for the 70j row itself, so both roots are own-sweep tier - already swept with the 70j child and REFUTED-D10 by its STERILE classification. The v1 freshness check only compared against the known REFUTED bit-119 root and missed the own-sweep tier entirely.
- Consequence: **sweeping the record's cost-62 neighbor cannot close the 70j row**. If 70j closure is the goal, the correct cost-62 target is the OTHER one-stone-replacement neighbor 00000000000000805282000000000000 (= 70j - 21 + 62), whose covering root 70j+bit62 is fresh (bit 62 not legal for the row).

## Orbit-aware fresh-target tables (all three open STERILE rows)

- Method: all 8 D4 images; covering root orbits = image + one stone; tier per root orbit: own-sweep (swept with the row's own child - all REFUTED since the row is STERILE) / unreachable (not a legal root of any child - can never be tested) / fresh (testable via generator children = one-stone-replacement neighbors).
- Internal consistency: legal-bit counts 65/70/74 match the row-name costs 65k/70j/74h exactly; own-sweep tier sizes equal the legal-bit counts (65/70/74).
- 65k: 49 fresh root orbits; cheapest generator child 00000000000000003802000008002000 (cost 61) testing fresh root 00000000020000801a02000000200000. One unreachable covering root orbit exists (unique to 65k).
- 70j: 45 fresh root orbits; cheapest generator child 00000000000000805282000000000000 (cost 62) testing fresh root 00000000000000805282000000200000.
- 74h: 41 fresh root orbits; cheapest generator child 00000000000000803202000000200000 (**cost 60 - the cheapest sterile-row attack overall**) testing fresh root 00000000000000889802000000000800.
- Full ranked tables with all generator children in the output JSON.

## Caveats for the engine lane

- "Fresh" = not in the row's own sweep. A fresh root may still have been swept as another candidate's root - then it is necessarily REFUTED (it cannot be WIN7 or the row would be closed). Check the fresh roots against the global swept-root registry before sweeping their generator children.
- Generator children are canonical forms; openness at 1419 and swept status must be checked by the engine lane.

## Status

- 11x11 empty board, S2 {59,60}, class1/class2/class4 roots: **UNKNOWN** (unchanged; geometry and bookkeeping only).
- Closing a STERILE row still requires a WIN7-D10 certificate on a fresh covering root.

Output: `research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class2-lane-sterile-rows-orbit-aware-fresh-target-tables-20261116.json`
Output (corrected pre-check): `research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class2-lane-cost62-neighbor-70j-coverage-precheck-20261116.json`
