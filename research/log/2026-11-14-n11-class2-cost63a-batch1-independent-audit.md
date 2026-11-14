# 2026-11-14 n11 class2 cost-63a: independent audit of raw batch 1

Audit base: main = 94e886a276c58994f2732350fe0ef01844673054.

Target S6 child:
00000000000000809102000800000000
(cost 63, demand c1=0,c2=2,c4=0), under S5
00000000000000809102000000000000.

## Candidate-set audit

The in-flight claim lists 63 legal seventh moves. I independently re-enumerated
them using BigInt exact determinants from det([x^2+y^2,x,y,1]), with a
3x3-minor Laplace expansion rather than the claim's Bareiss implementation.
The six-stone child is safe, and the independently enumerated legal candidate
list matches the claim's 63 bits exactly.

## Raw batch 1 audit

The raw JSONL contains one pilot control and eight candidate rows:

- Candidate bits: 0, 1, 2, 4, 6, 7, 9, 10.
- They are unique and form the exact sorted prefix of the 63-candidate list.
- Pilot d6 control: loss=false, 5,949 nodes, uncapped.
- Candidate rows: all uncapped; every terminal range is [13,17].
- Exactly one WIN7-D10 search candidate so far: bit 2, root
  00000000000000809102000800000004, 12,280,257 nodes.
- The other seven rows are REFUTED-D10 only: they did not find a winner win
  within depth 10 from those seven-stone roots.
- Candidate node total: 39,419,093; including the pilot control: 39,425,042.
- Remaining candidates: 55.

This independently confirms the published claim's candidate set and the first
raw batch's accounting. The commit message reports that batch 1 was re-run
node-exact after an environment reset, but the earlier pre-reset batch is not
present in this raw artifact, so that cross-restart comparison is not
independently checked here.

## Interpretation guard

The sweep is incomplete (8/63). Bit 2 is only a WIN7-D10 search candidate until
a strategy certificate is extracted and independently verified. The seven
REFUTED-D10 rows are not LOSS7 proofs. No S6 verdict or S5 blocker is closed by
this batch alone; no frontier count is updated.

The standard 11×11 empty root, two-stone root {49,60}, S2 {59,60}, class 2,
and class 4 remain UNKNOWN.

## Artifacts

- In-flight claim: research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class2-lane-cost63a-inflight-20261114.json
- Raw batch: research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class2-lane-cost63a-raw-batch1-20261114.jsonl
- Machine-readable audit: research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class2-lane-cost63a-batch1-independent-audit-20261114.json
