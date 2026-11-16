# class2-lane: frontier-wide S5 stabilizer census + ranking bookkeeping audit (2026-11-16)

## What was done

- Input: `class-frontier-s5-ranking-after-reconciled-canonical1400-cost70g-20261116.csv` (174 remaining S5 rows, head-1419 frontier snapshot).
- Independent third implementation: D4 (order 8) canonical form + stabilizer computation for every remaining S5.
- Bookkeeping audit: popcount, canonical-form fixed-point check, and duplicate-canonical scan over all 174 rows.
- Cross-check against the same-session orbit-dedup measurement (4 measured families).

## Results

- All 174 rows: popcount 5, all are fixed points of the third implementation's D4-canonical form, no duplicate canonical forms. The ranking's canonical convention matches the independent implementation exactly.
- Stabilizer census: 166 identity-only, **8 nontrivial** (all order 2 except one):
  - class4 S5 `00000000020000003800000080000000` {id, rot180} - measured family dup 19.86%
  - audit_blocked S5 `00000000000000809082000000000000` {id, y_flip} - measured family dup 12.18%
  - **S5 Q `00000000000000821082000000000000` (class-1, 18 children / cost 1238): Klein four-group {id, x_flip, y_flip, rot180}** - the largest stabilizer among all remaining S5s; Q is on the engine task list
  - 5 further order-2 stabilizer S5s (all class-1: 805082/2526, 380200020/2679, 811082/2821, 380040000020/2870, 38000000010020/3143)
- Nontrivial-stabilizer cost share is 1.8% of ranked cost (17,435 / 971,026); stabilizer order is the leading structural predictor of family-internal redundancy (order-2: 12-20% measured dup; trivial: 1.4-2.8%).
- Bookkeeping consistency: ranking sums with multiplicity are 971,026 (cost) / 12,284 (children); head-1419 unique aggregates are 508,474 / 6,429. Ratios match (0.5236 vs 0.5232), consistent with S6-level multiplicity dedup (indication, not an independent verification of 508474).

## Observations for the parallel lane

- When the Q sweep (`00000000000000821082000000000000`, class-1, 18 children / 1238) runs, apply family-level orbit dedup at candidate-enumeration time: the order-4 stabilizer gives Q the highest expected family-internal duplication of all remaining S5s, likely above the 19.86% measured for the class4 family.
- Family-internal orbit transfer pays off mainly for the 8 nontrivial-stabilizer S5s (1.8% of ranked cost). For the rest, the global cross-family seen-orbit table (cf. the 8.95% re-search redundancy in the 65f/65j census) matters more.
- K0865 checker violation (parallel lane item) remains unfixed; not touched here.
- bit-79 orbit (63a bit-97 root `00000002000000809102000800000000`) remains the only census overlap bit without a certificate; certificate extraction still needs an engine run on the physical device.

## Status

- 11x11 empty board, S2 {59,60}, class1/class2/class4 roots: **UNKNOWN** (unchanged; this census contains no verdicts).
- solved 1419 / remaining_s5 174 / unique_remaining_s6 6429 / needed 4702: manifest coverage bookkeeping only.

Output: `research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class2-lane-frontier-s5-stabilizer-census-20261116.json`
