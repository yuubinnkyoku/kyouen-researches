# class2-lane: Q family (Klein-four S5) full orbit-dedup measurement + superset-orbit structure verification (2026-11-16)

## What was done

- Enumerated, with the independent third implementation, the complete S6 superset orbits of three S5 families: Q `00000000000000821082000000000000` (class-1, Klein-four stabilizer, engine task list), class4 `00000000020000003800000080000000` (rot180), audit_blocked `00000000000000809082000000000000` (y_flip).
- For every superset orbit: recomputed legal 7th-stone candidate counts (survival rule, verified det3; 65f control re-enumerates to 65) and measured family-internal candidate-orbit duplication (D4-canonical candidate roots).
- Cross-checked the published remaining-children CSV: all 18 class4 and all 10 audit_blocked remaining children matched a unique canonical superset orbit, and every published edge cost equaled the recomputed legal count of the canonical representative.

## Results

- Q family: 33 superset orbits; full-family naive 2299 candidate searches, union 1347 orbits, **952 redundant = 41.41%** - the highest measured family-internal duplication, consistent with its order-4 stabilizer.
- class4: 58 orbits; naive 4581, union 2840, 1741 redundant = 38.0% (remaining-18 subset: 19.86%).
- audit_blocked: 62 orbits; naive 4207, union 2619, 1588 redundant = 37.75% (remaining-10 subset: 12.18%).
- Superset-orbit count structure: the number of S6 superset orbits of an S5 equals the number of stabilizer(S5)-orbits of the 116 free cells (33/58/62 measured), not 116/|stab| - cells on stabilizer fixed lines form smaller orbits.
- Published-worklist validation: the CSV children are exactly canonical superset orbits with orbit-invariant costs (28/28 matched).

## Observations for the parallel lane

- When the Q sweep (18 remaining children / cost 1238) runs, apply orbit-level verdict transfer at candidate enumeration: expected remaining-subset saving on the order of the class4 measurement (19.86%) or higher. Per-orbit legal counts for all 33 Q orbits are in the JSON for cost estimation.
- Full-family dup (37-41%) overstates the sweep saving because the engine only searches the remaining subsets; use the remaining-subset reference values.
- Which 18 of Q's 33 orbits remain was not re-derived here (engine worklist knows); the published per-orbit table applies to any subset.
- K0865 checker violation (parallel lane item) remains unfixed; not touched here.
- bit-79 orbit (63a bit-97 root `00000002000000809102000800000000`) remains the only census overlap bit without a certificate; needs an engine run on the physical device.

## Status

- 11x11 empty board, S2 {59,60}, class1/class2/class4 roots: **UNKNOWN** (unchanged; this measurement contains no verdicts).
- solved 1419 / remaining_s5 174 / unique_remaining_s6 6429 / needed 4702: manifest coverage bookkeeping only.

Output: `research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class2-lane-q-family-full-orbit-dedup-measurement-20261116.json`
