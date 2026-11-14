# 2026-11-14 class2-lane: cost-63e sweep — 8 WIN7-D10 (3 certificates verified), merged frontier 965 -> 970

Long-term lane session 12, continuing directly from the cost-61f result on the
same lane. Sweep target: the cost-63 child `00000000000000803202200000000000`
of the second class-2 target S5 `00000000000000803202000000000000`, named
cost-63e because the cost-63 band names are already occupied by the published
cost-63 / cost-63b / cost-63c / cost-63d sweeps (other targets' children).

During this sweep the concurrent session-11 lane published its merged frontier
recompute `class-frontier-merged-recompute-after61f-63a65e-20261114.json`
(commit `09e26e62`, solving 965 / 6,882 / 542,020 / 5,152/405,743 after folding
the cost-63a and cost-65e receipts of the first class-2 target). The cost-63e
frontier recompute below therefore extends the MERGED baseline, not the
after-cost-61f one — both lanes are now unified in a single chain.

## Claim and candidate enumeration

- Claim pushed before any sweep batch (commit `a27c0bfb`):
  `class2-lane-cost63e-inflight-20261114.json`, 63 candidates bit-exact with
  the published edge cost 63 (independent `legal_candidates.py` Bareiss
  enumeration).
- **Per the cost-61e correction lesson**, the child's membership among the
  parent's remaining children (23 orbits / 1,613 after cost-61f, cheapest at
  cost 63; the previously-listed cost-63 sibling
  `00000000000000803202000000000800` was covered by the cost-61f receipts) and
  its non-empty demand (c1=0, c2=2, c4=0) were re-verified from
  `class-frontier-top-candidates-s6-after-cost61f-20261114.csv` BEFORE the
  claim.
- Engine: the v16 runner, agreement-gated in cost-56a and the sweep engine for
  cost-58b / cost-60b / cost-61d / cost-61e / cost-61f. Pilot d6 control
  loss=false at exactly 3,402 nodes in all 8 batch invocations.

## Sweep result

**63/63 candidates: 8 WIN7-D10 + 55 REFUTED, 0 capped, 50,421,919 v16
nodes** (8 batches, raw JSONL pushed per batch, commit `6733b96c`; terminal
range [13,17] on every candidate).

- WIN7 bits: 28, 42, 73, 90, 97, 100, 116, 120.
- Heaviest candidates: bit 87 (3,370,406, REFUTED), bit 116 (2,390,779), bit 77
  (2,238,798, REFUTED), bit 120 (2,030,340), bit 6 (1,965,340, REFUTED), bit 4
  (1,552,806, REFUTED).
- Determinism: bits 116, 87 and 120 re-solved fresh in a separate process,
  node-exact identical
  (`class2-lane-cost63e-v16-determinism-rerun-20261114.jsonl`).
- v15 cross-engine anchors (pilot 5,949 PASS): bits 116/120/28 all loss=true at
  7,081,266 / 5,199,573 / 2,665,259 nodes and bit 87 loss=false at 8,510,530
  nodes — verdicts identical to v16
  (`class2-lane-cost63e-v15-crosscheck-20261114.jsonl`).

## Three WIN7 certificates — all verification PASS

The three cheapest WIN7 candidates were extracted with
`class4_child1_cert_extractor_exact.ts` (repo-verbatim), blind, FBS=1<<20;
every per-move extraction ok and uncapped, fbt_drops=0 on all three; rows
sorted unique; verified with `verify_bit7_win7_cert.ts` (root-check + all
sub-roots + consumed/rows union).

| bit | root hex | rows | extraction nodes | mobility | sub-roots | union miss/extra | md5 |
|---:|---|---:|---:|---:|---:|---|---|
| 28 | `00000000000000803202200010000000` | 30,830 | 5,270,260 | 47 | 47/47 | 0/0 | `653b6448...` |
| 90 | `00000000040000803202200000000000` | 26,272 | 4,881,302 | 49 | 49/49 | 0/0 | `8f591c83...` |
| 97 | `00000002000000803202200000000000` | 31,528 | 5,122,321 | 44 | 44/44 | 0/0 | `55c8d023...` |

- All three landed byte-exact with full paged reads (commits `c80f6d4d` /
  `6c85dda2` / `cedb8cc6`); remote md5 verified after a raw-CDN round-trip.
- **Reproducibility note**: the locally built certificate files were lost to an
  execution-environment reset mid-push; all three were regenerated from
  scratch with the repo-verbatim extractor and landed md5-identical to the
  recorded values (`653b6448713d4569b8ebad67451507bc` /
  `8f591c83fd83c09212825521b63b9eba` / `55c8d0236e3f5fcda39e506479c3bb9c`),
  an unplanned but complete independent reproduction of the extraction.
- Root absence: GitHub code search 0 hits each (all 8 WIN7 roots checked); the
  3 certificate roots were also matched against the published WIN7 receipt
  roots — no duplicates (the cost-61e bit-1 cross-child duplicate pattern does
  not occur here).
- The remaining 5 WIN7-D10 bits (42, 73, 100, 116, 120) stay warm
  certificate-rebuild candidates; bits 116/120 carry v15 loss=true
  cross-engine anchors.
- Terminal ranges within [13,17] on all three.

## Frontier recompute after cost-63e

`recompute_frontier_cost63e_20261114.py` (direct runpy extension of the
published merged recompute): every staged control through the merged
after-61f+63a+65e state reproduced exactly (asserted 965 / 6,882 / 542,020 /
5,152/405,743), the completed cost-63e sweep record, claim (status completed)
and receipts record are asserted, the child's remaining-membership and demand
(c1=0,c2=2,c4=0) are re-derived from the ACTUAL merged state and asserted
(fork reconciliation, not assumed — the demand held unchanged), then the three
receipts are added.

- cost-63e additions (covers / marginal / in-manifest): bit 28: 7/6/2,
  bit 90: 7/7/3, bit 97: 7/6/2 (net in-manifest +5).
- **after cost-63e: solved 970 · unique remaining 6,877 · sum 541,680 ·
  open 5,147 / 405,403.**
- Second class-2 target S5 `00000000000000803202000000000000`: 23 -> 21 orbits
  (1,613 -> 1,482), still the best coverable class-2 target. Best class-4
  unchanged (18 / 1,460).
- Records completed and pushed (commit `ed2dd6f2`: sweep record, receipts
  record, completed claim). Frontier recompute + script + rankings pushed in
  commit `e4f735c8`, remote md5 verified. Two consecutive recompute runs
  byte-identical (JSON + both CSVs).

## Operational notes

- Next cheapest remaining child of the second class-2 target after cost-63e:
  cost-64 `00000000000000803202000000100000` (per
  `class-frontier-top-candidates-s6-after-cost63e-20261114.csv`; verify
  membership + demand again before claiming).
- Session-12 lane totals: cost-56a (1 WIN7), cost-58b (3 WIN7), cost-60b
  (25 WIN7), cost-61d (14 WIN7), cost-61e (13 WIN7), cost-61f (11 WIN7),
  cost-63e (8 WIN7) on the second class-2 target's children; frontier
  924 -> 970 across the session's receipts (75 WIN7-D10 verdicts, 24
  certificates verified).

## Status

11x11 empty board: UNKNOWN. Two-stone root {49,60}: UNKNOWN. S2 {59,60}:
UNKNOWN. class 2 / class 4 blockers: UNKNOWN. WIN7 certificates prove only
individual 7-stone roots within depth 10; REFUTED-D10 sweeps prove only the
absence of such receipts.
