# 2026-11-14 class2-lane cost-68 sweep + 17 WIN7 certificates

## What ran

- S6 child `00000000000000801a02000080000000` (class-2 blocker remaining child, cost 68)
  — all 68 legal 7th-stone candidates, v15 verbatim engine (close-first AND d>=8),
  depth 10 single-shot, cap 100M/candidate, 4 workers on a shared 2-core host.
- Result: **17 WIN7-D10 + 51 REFUTED-D10, 0 capped, 363,926,743 nodes**.
  WIN7 bits: 0, 4, 7, 8, 9, 12, 20, 24, 40, 42, 50, 52, 78, 87, 96, 110, 112.
  This is the largest single-orbit WIN7 harvest on the class-2 lane so far
  (previous record 19 on cost-60's 60 candidates; here 17/68 = 25%).
- Controls: pilot d6 = 5,949 (loss=false) PASS in all 68 worker invocations
  (the runner aborts otherwise). Fresh independent re-runs of the five heaviest
  candidates (bit 87/77/78/92/25) reproduced node counts bit-exactly
  (17,457,204 / 15,798,996 / 13,318,869 / 12,207,082 / 12,322,965).
  Nodes are deterministic; wall ms varies with host load and is not compared.

## Certificates

- All 17 WIN7 roots extracted blind (kill-table-free, pref=null) with the repo
  extractor: 686,816 rows total, 199,870,348 extraction nodes.
- Independent verification (engine-free Bareiss-det4 verifier): every root
  PASS (7 stones, no 4 cocircular), all sub-root decompositions PASS
  (48-61 sub-roots per root), consumed winner-state union == certificate
  row set exactly (0/0 both directions, all 17), terminals within [13,17].
- Files: output/class2-lane-cost68-certificates/n11_s7_<root>.cert
  Record: output/class2-lane-cost68-win7-certificates-20261114.json

## Interpretation guard

WIN7-D10 is a win-within-depth-10 fact from each individual 7-stone root only.
REFUTED-D10 is only the absence of a WIN7-D10 in that subtree.
The 11x11 empty root, the two-stone root {49,60}, S2 {59,60}, class 2 and
class 4 remain UNKNOWN.

## Frontier effect

The class-2 blocker S5 `00000000000000003802000008000000` had 2 remaining
orbits after cost-65: this cost-68 child and the cost-75 child
`00000000000000801a02040000000000`. The cost-68 sweep with certificates
removes this child from the blocker's remaining demand; the blocker is now
down to the single cost-75 child (formal frontier recompute to follow with
the cost-75 additions in the same recompute script).
