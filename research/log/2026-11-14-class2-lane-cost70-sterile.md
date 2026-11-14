# 2026-11-14 class2-lane cost-70 sweep (sterile child)

Long-term lane, 8th session. S6 child `00000000000000809082000000000001`
(cost 70, demand c1=2,c2=2,c4=0) of the best class-2 target S5
`00000000000000809082000000000000` (after-cost69a: 15 orbits / 1,054).

Chosen to avoid collision with the hourly parallel lane, which declared
cost-69c (`00000000000000809082040000000000`) as its next target in the
cost-69b log. This child was claimed in the batches 1-5 commit.

## Result

- **All 70 candidates REFUTED-D10, 0 WIN7, 0 capped, 380,930,330 nodes =
  14th sterile child in the lane** (no WIN7 certificate candidates; the swept
  child contributes no new orbit covers).
- Independent enumeration (legal_candidates.py): 70 legal candidates, matching
  the published edge cost 70.
- Pilot d6 control: loss=false at exactly 5,949 nodes in all 9 batch invocations.
- Terminal stone range across all candidates: [13, 17].
- Heaviest candidates: bit 112 (24,933,747 nodes), bit 86 (20,457,811),
  bit 94 (14,411,457); fresh rerun of all three node-exact (determinism).

## Notes

- No frontier effect: sterile child (all REFUTED). Frontier stays at the
  after-cost69a control (solved 909 / remaining 6,938 / sum 545,893 / open
  5,199/408,942) plus any receipts the parallel lane pushes.
- Remaining cheapest unswept children of the target per after-cost69a ranking:
  cost-69c `00000000000000809082040000000000` (claimed by parallel lane),
  then cost-70 `00000000000000809082080000000000` (c1=2,c2=1),
  then the cost-71+ band.

## Status

11x11 empty board: UNKNOWN. Two-stone root {49,60}: UNKNOWN. S2 {59,60}: UNKNOWN.
class 2 / class 4 blockers: UNKNOWN. (A sterile child proves nothing about the
game-theoretic value of any position; it only removes this child from the
orbit-cover frontier.)
