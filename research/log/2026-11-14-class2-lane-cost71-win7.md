# 2026-11-14 class2-lane cost-71 sweep (2 WIN7-D10, both certificates fully verified)

Long-term lane, 8th session, fourth result. S6 child `00000000000000809082000000000004`
(cost 71, demand c1=2,c2=2,c4=0) of the best class-2 target S5
`00000000000000809082000000000000`. Cheapest unswept child per the
after-cost70b ranking; claimed in the batch-1 commit.

## Sweep result

- **2 WIN7-D10 (bits 9, 70) + 69 REFUTED-D10, 0 capped, 385,100,613 nodes.**
- Independent enumeration: 71 legal candidates, matching the published edge cost 71.
- Pilot d6 control: loss=false at exactly 5,949 nodes in all 9 batch invocations.
- Terminal stone range across all candidates: [13, 17].
- Heaviest bits 100/110/94 and both WIN7 bits fresh rerun node-exact.

## WIN7 certificates

- **bit9 root `00000000000000809082000000000204`**: blind extraction 55,430 rows,
  15,804,988 extraction nodes, fbt_drops=0, fatal=null; root check 7 stones /
  loser mobility 59 = independent enumeration; **59/59 sub-roots PASS, union
  0/0, terminals [13,17]**. md5 98c76fea...
- **bit70 root `00000000000000c09082000000000004`**: blind extraction 39,264 rows,
  8,817,182 extraction nodes, fbt_drops=0, fatal=null; root check 7 stones /
  loser mobility 52 = independent enumeration; **52/52 sub-roots PASS, union
  0/0, terminals [13,17]**. md5 0cb59138...
- Both roots not among the existing certificate roots.
- Note: the naive "child + bit" root hex must be computed with OR on the full
  child mask (bit9 root is ...0204, not ...0200); caught by the 6-stone
  occupancy check in legal_candidates.py before extraction.

## Notes

- Certificate transport: bit9 certificate is 2.0 MB and exceeds the single-run
  push limit; pushed as part1of2/part2of2 with a README (concatenation md5
  must reproduce 98c76fea...). bit70 certificate is 1.4 MB, single push.
- Frontier effect: 2 WIN7 receipts; recompute extends after-cost70b (913/6,934/
  545,596/5,198/408,868).

## Status

11x11 empty board: UNKNOWN. Two-stone root {49,60}: UNKNOWN. S2 {59,60}: UNKNOWN.
class 2 / class 4 blockers: UNKNOWN. (WIN7 certificates prove only individual
7-stone roots' depth-10 wins.)
