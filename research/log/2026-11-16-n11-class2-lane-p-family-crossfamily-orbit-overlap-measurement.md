# class2-lane: P family full orbit-dedup + frontier-top cross-family overlap measurement (2026-11-16)

## What was done

- Measured, with the independent third implementation, the complete family-internal candidate-orbit duplication of P `00000000000000403800000008000000` (class-2 own_closable, identity-only stabilizer, engine task list): 116 superset orbits.
- Measured cross-family candidate-orbit overlap among the frontier-top families: the 4 remaining top families (36 children, from the published CSV) and the 4 full families (class4 58 / audit_blocked 62 / Q 33 / P 116 orbits).
- Control: the 65f child re-enumerates to 65 legal candidates (verified det3).

## Results

- P family: 116 superset orbits; full-family naive 8308 candidate searches, union 5261, **3047 redundant = 36.68%** - despite the identity-only stabilizer.
- Full-family comparison: Q (33 orbits) 41.41% > class4 (58) 38.0% > audit_blocked (62) 37.75% > P (116) 36.68%.
- **Interpretation correction (supersedes the stabilizer census reading):** family-internal duplication is driven primarily by family size (cumulative union overlap), not stabilizer order. The earlier 1.4-2.75% trivial-family values were small-remaining-subset artifacts (3 and 5 children). Stabilizer order is a real but modest secondary modifier (Q above the size trend, P lowest).
- Cross-family overlap: remaining top-4 families share only 2 candidate orbits (2343 -> 2341, 0.09%); the 4 full families share 118 orbits (12067 -> 11949, ~1%), concentrated in the P-audit_blocked pair (81) and audit-Q pair (34).

## Observations for the parallel lane

- Family-level orbit transfer should be applied to ALL families, not only the 8 nontrivial-stabilizer S5s; expected savings scale with the number of children searched in the sweep.
- Per-family seen-orbit tables capture almost all redundancy at the current frontier; the global cross-family table adds only ~0.1-1% - implement it second.
- When the P sweep (24 remaining children / cost 1704) and the Q sweep (18 / 1238) run, both should use family-level transfer (full-family structures: 36.68% / 41.41%).
- K0865 checker violation (parallel lane item) remains unfixed; not touched here.
- bit-79 orbit (63a bit-97 root `00000002000000809102000800000000`) remains the only census overlap bit without a certificate; needs an engine run on the physical device.

## Status

- 11x11 empty board, S2 {59,60}, class1/class2/class4 roots: **UNKNOWN** (unchanged; this measurement contains no verdicts).
- solved 1419 / remaining_s5 174 / unique_remaining_s6 6429 / needed 4702: manifest coverage bookkeeping only.

Output: `research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class2-lane-p-family-crossfamily-orbit-overlap-measurement-20261116.json`
