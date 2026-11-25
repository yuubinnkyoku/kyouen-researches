# 2026-11-14 class2-lane cost-70b sweep (1 WIN7-D10, certificate fully verified)

Long-term lane, 8th session, second result. S6 child `00000000000000809082080000000000`
(cost 70, demand c1=2,c2=1,c4=0) of the best class-2 target S5
`00000000000000809082000000000000`.

## Sweep result

- **1 WIN7-D10 (bit 37) + 69 REFUTED-D10, 0 capped, 404,797,576 nodes.**
- Independent enumeration (legal_candidates.py): 70 legal candidates, matching the
  published edge cost 70.
- Pilot d6 control: loss=false at exactly 5,949 nodes in all 9 batch invocations.
- Terminal stone range across all candidates: [13, 17].
- Heaviest bits 12/13/14 fresh rerun node-exact; WIN7 bit 37 fresh rerun node-exact
  (8,135,396 nodes).

## WIN7 certificate bit37 (root 00000000000000809082082000000000)

- Blind extraction (empty kill table, FBS=1<<20, probe96): 30,551 rows,
  11,569,428 extraction nodes, fbt_drops=0, fatal=null, all 50 per-move
  extractions ok and uncapped.
- Rows sorted unique before push (extractor emits unsorted rows).
- Root check: 7 stones, loser mobility 50, matching the independent enumeration.
- Full verification: 50/50 sub-roots PASS; union of consumed winner states equals
  the full row set exactly (0 missing / 0 extra); terminals [13,17].
- Root not among the existing certificate roots (checked against all 157
  certificate files in the experiment output).

## Notes

- Cost-70 (first child) was sterile (14th), pushed earlier this session;
  cost-69c was claimed by the hourly parallel lane.
- Frontier effect of this child: receipt = the WIN7 root; recompute belongs to
  the next frontier pass (after-cost69a control 909/6,938/545,893/5,199/408,942,
  extended by this receipt and the parallel lane's receipts).

## Status

11x11 empty board: UNKNOWN. Two-stone root {49,60}: UNKNOWN. S2 {59,60}: UNKNOWN.
class 2 / class 4 blockers: UNKNOWN. (A WIN7 certificate proves only that this
individual 7-stone root is a first-player win within depth 10; it decides
nothing about the above positions.)
