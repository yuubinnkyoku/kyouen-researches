# 2026-11-14 class2-lane: cost-61d sweep — 14 WIN7-D10 (3 certificates verified), frontier 946 -> 951

Long-term lane session 12, continuing directly from the cost-60b result on the
same lane (after-cost-60b frontier solved 946; commits `dda2a040` +
`7cb1af87`). The cheapest remaining unswept child of the second class-2 target
S5 `00000000000000803202000000000000` (29 orbits / 2,005 after cost-60b) was
the cost-61 child `00000000000000803202000000000002`. Named cost-61d because
the cost-61 band names are already occupied by the published cost-61 /
cost-61b / cost-61c sweeps of other targets' children.

## Claim and candidate enumeration

- Claim pushed before any sweep batch (commit `27878b27`):
  `class2-lane-cost61d-inflight-20261114.json`, 61 candidates bit-exact with
  the published edge cost 61 (independent `legal_candidates.py` Bareiss
  enumeration); demand classes c1=0, c2=2, c4=0.
- Engine: the v16 runner, agreement-gated in cost-56a and already the sweep
  engine for cost-58b / cost-60b. Pilot d6 control loss=false at exactly 3,402
  nodes in all 8 batch invocations.

## Sweep result

**61/61 candidates: 14 WIN7-D10 + 47 REFUTED, 0 capped, 50,848,724 v16
nodes** (8 batches, raw JSONL pushed per batch, commit `f360ca05`; terminal
range [13,17] on every candidate).

- WIN7 bits: 2, 8, 22, 23, 30, 53, 74, 75, 84, 94, 102, 114, 116, 119.
- Heaviest candidates: bit 114 (3,493,610), bit 102 (3,471,936), bit 75
  (2,964,686), bit 119 (2,009,100), bit 116 (2,008,333), bit 22 (1,955,533).
- Determinism: bits 114, 102 and 75 re-solved fresh in a separate process,
  node-exact identical
  (`class2-lane-cost61d-v16-determinism-rerun-20261114.jsonl`).
- v15 cross-engine anchors (pilot 5,949 PASS): bits 114/102/75/30 all
  loss=true at 7,110,338 / 5,276,136 / 5,440,676 / 1,660,324 nodes and bit 32
  (heaviest REFUTED) loss=false at 4,206,190 nodes — verdicts identical to
  v16 (`class2-lane-cost61d-v15-crosscheck-20261114.jsonl`).

## Three WIN7 certificates — all verification PASS

The three cheapest WIN7 candidates were extracted with
`class4_child1_cert_extractor_exact.ts` (repo-verbatim), blind, FBS=1<<20;
every per-move extraction ok and uncapped, fbt_drops=0 on all three; rows
sorted unique; verified with `verify_bit7_win7_cert.ts` (root-check + all
sub-roots + consumed/rows union); root hexes absent from all published
win7-certificates records (GitHub code search: 0 hits each).

| bit | root hex | rows | extraction nodes | mobility | sub-roots | union miss/extra | md5 |
|---:|---|---:|---:|---:|---:|---|---|
| 30 | `00000000000000803202000040000002` | 23,348 | 2,808,588 | 44 | 44/44 | 0/0 | `93bc0a6a...` |
| 74 | `00000000000004803202000000000002` | 26,090 | 2,464,620 | 49 | 49/49 | 0/0 | `23d3ef0e...` |
| 94 | `00000000400000803202000000000002` | 23,982 | 3,984,132 | 45 | 45/45 | 0/0 | `85784c48...` |

- All three landed byte-exact on the first push using full paged reads
  (commits `904a7676` / `affa984a` / `9f31705a`); remote md5 verified.
- The remaining 11 WIN7-D10 bits (2,8,22,23,53,75,84,102,114,116,119) stay
  warm certificate-rebuild candidates; bits 114/102/75 carry v15 loss=true
  cross-engine anchors.
- Terminal ranges within [13,17] on all three.

## Frontier recompute after cost-61d

`recompute_frontier_cost61d_20261114.py` (direct runpy extension of the
published cost-60b script): every staged control through after-cost-60b
reproduced exactly (asserted 946 / 6,901 / 543,316 / 5,171/407,039), the
completed cost-61d sweep record, claim (status completed) and receipts record
are asserted, the child's demand (c1=0,c2=2,c4=0) is re-derived from the
frontier and matched, then the three receipts are added.

- cost-61d additions (covers / marginal / in-manifest): bit 30: 7/6/2,
  bit 74: 7/7/3, bit 94: 7/6/2 (each includes the swept child's own orbit
  `00000000000000803202000000000002`; net in-manifest +5).
- **after cost-61d: solved 951 · unique remaining 6,896 · sum 542,952 ·
  open 5,166 / 406,675.**
- Second class-2 target S5 `00000000000000803202000000000000`: 29 -> 27 orbits
  (2,005 -> 1,876), still the best coverable class-2 target. Best class-4
  unchanged (18 / 1,460).
- Two consecutive runs byte-identical (JSON + both CSVs).

## Operational notes

- Full paged reads (offset/limit=4000, next_offset loop, joined-length
  asserted) landed all three ~0.85-0.94MB certificates byte-exact on the
  first push — the paging protocol is now reliable; remote md5 still
  verified after every push.
- Session-12 lane totals so far: cost-56a (1 WIN7), cost-58b (3 WIN7),
  cost-60b (25 WIN7), cost-61d (14 WIN7) on the second class-2 target alone;
  frontier 924 -> 951 across the session's receipts.

## Status

11x11 empty board: UNKNOWN. Two-stone root {49,60}: UNKNOWN. S2 {59,60}:
UNKNOWN. class 2 / class 4 blockers: UNKNOWN. WIN7 certificates prove only
individual 7-stone roots within depth 10; REFUTED-D10 sweeps prove only the
absence of such receipts.
