# 2026-11-14 class2-lane: cost-73e sweep complete - sterile (session 10)

Long-term lane, 10th session. Started from HEAD 3fa5c6e8 (after-cost71 frontier:
solved 917, remaining 6,930, sum 545,301, open 5,197/408,797; class-2 target
12 orbits / 844). The parallel lane completed cost-73b and cost-73c (both
sterile) and claimed cost-73d; cost-73a (WIN7 bit81, certificate pending)
belongs to the parallel lane. This session claimed the fifth and last child of
the cost-73 band.

## cost-73e sweep

- S6 child `00000000000000809082000200000000` (cost 73, demand c1=2,c2=2,c4=0)
  of the best class-2 target S5 `00000000000000809082000000000000`.
  legal_candidates.py independent enumeration: 73 legal candidates, bit-exact
  with the published edge cost 73 (after-cost71 CSV row).
- **73 REFUTED-D10, 0 WIN7, 0 capped, 355,978,631 nodes** = 17th sterile child
  overall, third in the cost-73 band (73b, 73c, 73e).
- Pilot d6 control: loss=false at exactly 5,949 nodes in all 13 batch
  invocations. Terminal stone ranges: [13,17] everywhere except bit 45 [15,17].
- Heaviest bits: 48 (16,383,315), 26 (12,671,058), 30 (12,485,345),
  53 (12,226,656), 23 (9,954,345), 113 (9,396,208). Fresh re-solve of bits
  48/26/30 in separate processes: node-exact identical.
- Raw batches 0-12 + determinism rerun pushed verbatim under
  `research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/`.
- Frontier effect: none (sterile child, no WIN7 certificate). The class-2
  target remains 12 orbits / 844 pending the 73a bit81 and 73d outcomes.

## Cost-73 band state after this sweep

- 73a: parallel lane, in flight (64/73 done, 1 WIN7 bit81, cert pending).
- 73b: sterile (376,649,033 nodes). 73c: sterile (388,889,991 nodes).
- 73d: long-term lane session 9, in flight.
- 73e: sterile (this record). Next unclaimed class-2 child: cost-74
  `00000000000000809082000100000000`.

## Status

11x11 empty board: UNKNOWN. Two-stone root {49,60}: UNKNOWN. S2 {59,60}:
UNKNOWN. class 2 / class 4 blockers: UNKNOWN. (REFUTED-D10 decides nothing
about the child; WIN7 certificates prove only individual 7-stone roots.)
