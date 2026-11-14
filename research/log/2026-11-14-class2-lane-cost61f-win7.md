# 2026-11-14 class2-lane: cost-61f sweep — 11 WIN7-D10 (3 certificates verified), frontier 954 -> 959

Long-term lane session 12, continuing directly from the cost-61e result on the
same lane (after-cost-61e frontier solved 954; commits `d2c2244b` + `86304039`).
Sweep target: the cost-61 child `00000000000000803202000080000000` of the
second class-2 target S5 `00000000000000803202000000000000`, named cost-61f
because the cost-61 band names are already occupied by the published cost-61 /
cost-61b / cost-61c / cost-61d / cost-61e sweeps.

## Claim and candidate enumeration

- Claim pushed before any sweep batch (commit `86dd4dab`):
  `class2-lane-cost61f-inflight-20261114.json`, 61 candidates bit-exact with
  the published edge cost 61 (independent `legal_candidates.py` Bareiss
  enumeration).
- **Per the cost-61e correction lesson**, the child's membership among the
  parent's remaining children (26 orbits / 1,809 after cost-61e, cheapest at
  cost 61) and its non-empty demand (c1=0, c2=2, c4=0) were re-verified from
  `class-frontier-top-candidates-s6-after-cost61e-20261114.csv` BEFORE the
  claim.
- Engine: the v16 runner, agreement-gated in cost-56a and the sweep engine for
  cost-58b / cost-60b / cost-61d / cost-61e. Pilot d6 control loss=false at
  exactly 3,402 nodes in all 8 batch invocations.

## Sweep result

**61/61 candidates: 11 WIN7-D10 + 50 REFUTED, 0 capped, 45,925,702 v16
nodes** (8 batches, raw JSONL pushed per batch, commit `9210e199`; terminal
range [13,17] on every candidate).

- WIN7 bits: 0, 23, 26, 43, 66, 67, 75, 77, 84, 99, 102.
- Heaviest candidates: bit 74 (4,425,763, REFUTED), bit 102 (4,395,138), bit 44
  (2,361,964, REFUTED), bit 76 (2,019,770, REFUTED), bit 77 (1,962,953), bit
  66 (1,592,043).
- Determinism: bits 102, 74 and 77 re-solved fresh in a separate process,
  node-exact identical
  (`class2-lane-cost61f-v16-determinism-rerun-20261114.jsonl`).
- v15 cross-engine anchors (pilot 5,949 PASS): bits 102/77/0 all loss=true at
  18,359,097 / 11,560,823 / 7,054,490 nodes and bit 74 loss=false at
  22,086,433 nodes — verdicts identical to v16
  (`class2-lane-cost61f-v15-crosscheck-20261114.jsonl`).

## Three WIN7 certificates — all verification PASS

The three cheapest WIN7 candidates were extracted with
`class4_child1_cert_extractor_exact.ts` (repo-verbatim), blind, FBS=1<<20;
every per-move extraction ok and uncapped, fbt_drops=0 on all three; rows
sorted unique; verified with `verify_bit7_win7_cert.ts` (root-check + all
sub-roots + consumed/rows union).

| bit | root hex | rows | extraction nodes | mobility | sub-roots | union miss/extra | md5 |
|---:|---|---:|---:|---:|---:|---|---|
| 23 | `00000000000000803202000080800000` | 26,256 | 7,119,554 | 47 | 47/47 | 0/0 | `6c8145b7...` |
| 26 | `00000000000000803202000084000000` | 30,764 | 7,843,548 | 49 | 49/49 | 0/0 | `e98f72ba...` |
| 99 | `00000008000000803202000080000000` | 26,575 | 8,974,908 | 45 | 45/45 | 0/0 | `ac1e52f7...` |

- All three landed byte-exact with full paged reads (commits `44a7d08d` /
  `3d057aef` / `53b02b6b`); remote md5 verified.
- Root absence: GitHub code search 0 hits each; in addition all 11 WIN7 root
  hexes were checked against the 247 published WIN7 receipt roots in the
  experiment records — no duplicates (the cost-61e bit-1 cross-child
  duplicate pattern does not occur here).
- The remaining 8 WIN7-D10 bits (0,43,66,67,75,77,84,102) stay warm
  certificate-rebuild candidates; bits 102/77/0 carry v15 loss=true
  cross-engine anchors.
- Terminal ranges within [13,17] on all three.

## Frontier recompute after cost-61f

`recompute_frontier_cost61f_20261114.py` (direct runpy extension of the
published cost-61e script): every staged control through after-cost-61e
reproduced exactly (asserted 954 / 6,893 / 542,756 / 5,163/406,479), the
completed cost-61f sweep record, claim (status completed) and receipts record
are asserted, the child's remaining-membership and demand (c1=0,c2=2,c4=0)
are re-derived from the frontier and asserted, then the three receipts are
added.

- cost-61f additions (covers / marginal / in-manifest): bit 23: 7/6/2,
  bit 26: 7/6/2, bit 99: 7/7/3 (net in-manifest +5).
- **after cost-61f: solved 959 · unique remaining 6,888 · sum 542,417 ·
  open 5,158 / 406,140.**
- Second class-2 target S5 `00000000000000803202000000000000`: 26 -> 23 orbits
  (1,809 -> 1,613), still the best coverable class-2 target. Best class-4
  unchanged (18 / 1,460).
- Records completed and pushed (commit `2458842a`: sweep record, receipts
  record, completed claim). Frontier recompute + script + rankings pushed in
  commit `89f01f1c`, remote md5 verified. Two consecutive recompute runs
  byte-identical (JSON + both CSVs).

## Operational notes

- Next cheapest remaining child of the second class-2 target after cost-61f:
  cost-63 `00000000000000803202000000000800` (per
  `class-frontier-top-candidates-s6-after-cost61f-20261114.csv`; verify
  membership + demand again before claiming).
- Session-12 lane totals: cost-56a (1 WIN7), cost-58b (3 WIN7), cost-60b
  (25 WIN7), cost-61d (14 WIN7), cost-61e (13 WIN7), cost-61f (11 WIN7) on the
  second class-2 target's children; frontier 924 -> 959 across the session's
  receipts (67 WIN7-D10 verdicts, 21 certificates verified).

## Status

11x11 empty board: UNKNOWN. Two-stone root {49,60}: UNKNOWN. S2 {59,60}:
UNKNOWN. class 2 / class 4 blockers: UNKNOWN. WIN7 certificates prove only
individual 7-stone roots within depth 10; REFUTED-D10 sweeps prove only the
absence of such receipts.
