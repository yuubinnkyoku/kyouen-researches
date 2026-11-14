# 2026-11-14 class2-lane: cost-74 sweep complete - sterile (session 10)

Long-term lane, 10th session, second sweep of the run (after cost-73e, sterile).
Child `00000000000000809082000100000000` (cost 74, demand c1=2,c2=2,c4=0) of the
best class-2 target S5 `00000000000000809082000000000000` — the next cheapest
unswept child after the fully-claimed cost-73 band.

## cost-74 sweep

- legal_candidates.py independent enumeration: 74 legal candidates, bit-exact
  with the published edge cost 74.
- **74 REFUTED-D10, 0 WIN7, 0 capped, 490,965,731 nodes** = 18th sterile child
  overall. Terminal stone range uniformly [13,17].
- Pilot d6 control: loss=false at exactly 5,949 nodes in all 14 batch
  invocations.
- Heaviest bits: 15 (27,452,305), 70 (19,146,135), 20 (18,131,025),
  12 (15,359,133), 23 (13,783,873), 9 (13,772,045). Fresh re-solve of bits
  15/70/20 in separate processes: node-exact identical.
- Raw batches 1-13 + determinism rerun pushed verbatim under
  `research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/`.
- Frontier effect: none (sterile child, no WIN7 certificate).

## Lane state after this sweep

- cost-73 band: 73a (parallel, in flight, WIN7 bit81 cert pending),
  73b/73c/73e sterile, 73d (session 9, in flight).
- cost-74 (this child): sterile.
- Both sweeps of this session are sterile: the target S5's cheapest 7
  unswept children produced no WIN7 certificate today; the class-2 frontier
  still moves only through 73a/73d outcomes.

## Status

11x11 empty board: UNKNOWN. Two-stone root {49,60}: UNKNOWN. S2 {59,60}:
UNKNOWN. class 2 / class 4 blockers: UNKNOWN. (REFUTED-D10 decides nothing
about the child; WIN7 certificates prove only individual 7-stone roots.)
