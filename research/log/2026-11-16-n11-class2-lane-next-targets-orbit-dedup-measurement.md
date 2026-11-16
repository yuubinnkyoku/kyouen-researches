# class2-lane: next-target S5 families orbit-dedup measurement (2026-11-16)

## What was done

- Input: `class-frontier-top-candidates-s6-after-cost65j-receipts-20261116.csv` (head 626ff5d3): the 4 next-target S5 families (best class4 = 18 children, audit-blocked class2 = 10, best coverable class2 = 3, second coverable class2 = 5; 36 children total).
- Independent third implementation (TypeScript sandbox): D4 canonical form + survival legality (7th stone must not be concyclic with any triple of the 6 stones, via 4x4 determinant).
- Correctness control: the recomputed legal-candidate count equals the published CSV `s6_s7_edge_cost` for **all 36 children**; the known 65f child re-enumerates to 65.
- An earlier in-session draft had a transcription bug in det3 (b[2]*b[0] instead of b[2]*c[0]) that inflated counts (73 -> 114 etc.); the CSV cross-check caught it and all numbers below come from the corrected determinant. The published JSON records this control.
- Measured family-internal candidate-orbit duplication: for each family, count distinct D4 orbits of (child | 7th-stone candidate) roots vs naive per-child enumeration.

## Results

- best_class4 S5 `00000000020000003800000080000000`: naive 1460 candidate searches, union 1170 distinct orbits, **290 redundant = 19.86%** (stabilizer: identity + rot180).
- audit_blocked class2 S5 `00000000000000809082000000000000`: naive 698, union 613, **85 redundant = 12.18%** (stabilizer: identity + vertical flip).
- best_coverable class2 S5 `00000000000000801202000000200000`: naive 209, union 206, **3 redundant = 1.44%**.
- second_coverable class2 S5 `00000000000000801202000040000000`: naive 364, union 354, **10 redundant = 2.75%** (children ci2-ci4 are win_pending rows already swept; reference values only).
- Cross-check on the completed 65f/65j sweeps: the 4 census-overlap bits consumed 36,043,714 of 402,603,616 nodes (**8.95%**) as re-searches an orbit-level transfer would have skipped.
- Structural: for all 36 children the D4 orbit image set contains the parent S5; family-internal collisions are systematic (mediated by the parent stabilizer), and per-child dup counts grow near-linearly with cumulative union size.

## Observations for the parallel lane

- Recommendation (priority 5, structural improvement): before the next engine sweep (class4 S5 18 children first), canonicalize each candidate root (child | 7th stone) under D4 at enumeration time and keep a family-level seen-orbit table with WIN/REFUTED verdict transfer (generalization of the K0863 bit-113 transfer). Expected saving: 19.86% of candidate searches on the class4 family, 12.18% on audit-blocked.
- K0865 checker violation (parallel lane item) remains unfixed; not touched here.
- bit-79 orbit (63a bit-97 root `00000002000000809102000800000000`) remains the only census overlap bit without a certificate; certificate extraction still needs an engine run on the physical device.

## Status

- 11x11 empty board, S2 {59,60}, class1/class2/class4 roots: **UNKNOWN** (unchanged; this measurement contains no verdicts).
- solved 1419 / remaining_s5 174 / unique_remaining_s6 6429 / needed 4702: manifest coverage bookkeeping only.

Output: `research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class2-lane-next-targets-orbit-dedup-measurement-20261116.json`
