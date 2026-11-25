# 2026-11-14 class2-lane: cost-58b sweep — 3 WIN7 certificates (bits 18/77/120) fully verified; frontier 927 -> 935

Long-term lane session 12, continuing directly from the cost-56a result on the
same lane (after-cost-56a frontier solved 927; commit `8e43b4cc`). The
second-cheapest remaining unswept child of the second class-2 target S5
`00000000000000803202000000000000` (39 orbits / 2,657 after cost-56a) was the
cost-58 child `00000000000000803202000000002000`. Named cost-58b because the
cost-58 band name is already occupied by the published child
`00000000000000809082000080000000`. While this sweep ran, the parallel lanes
advanced raw batches of cost-63a (class-2) and cost-86e (class-4) on main; no
new certificates from those lanes landed before this recompute.

## Claim and candidate enumeration

- Claim pushed before any batch (commit `6b23ef46`):
  `class2-lane-cost58b-inflight-20261114.json`, 58 candidates bit-exact with the
  published edge cost (independent `legal_candidates.py` Bareiss enumeration);
  demand classes c1=0, c2=1, c4=1.
- Engine: the v16 runner (`class4_child1_runner_v16.ts`), already validated this
  session by the depth-10 verdict-agreement gate against the published v15
  cost-73a record (bit81 WIN7 + 3 REFUTED reproduced, 3.24x aggregate node
  reduction; `class2-lane-cost56a-v16-agreement-gate-20261114.jsonl`). Pilot d6
  control loss=false at exactly 3,402 nodes in all 8 batch invocations.

## Sweep result

**58/58 candidates: 3 WIN7-D10 (bits 18, 77, 120) + 55 REFUTED, 0 capped,
30,690,766 v16 nodes** (8 batches of 8, raw JSONL pushed per batch; commits
`eb4d29c1` … `4731742c`; terminal range [13,17] on every candidate).

- WIN7 roots:
  - bit 18 `00000000000000803202000000042000`
  - bit 77 `00000000000020803202000000002000`
  - bit 120 `01000000000000803202000000002000`
- Heaviest candidates: bit 120 (2,245,381), bit 43 (2,736,745), bit 77
  (1,270,795), bit 66 (1,244,351), bit 18 (1,254,557).
- Determinism: bits 120, 43 and 18 re-solved fresh in a separate process after
  the sweep, node-exact identical
  (`class2-lane-cost58b-v16-determinism-rerun-20261114.jsonl`).
- v15 cross-engine anchors on this child (pilot 5,949 PASS): bits 18/77/120 all
  loss=true at 2,928,682 / 3,472,004 / 7,495,218 nodes and bit 43 loss=false at
  7,175,852 nodes — verdicts identical to v16 on all four
  (`class2-lane-cost58b-v15-crosscheck-20261114.jsonl`).

## The three WIN7 certificates — all verification PASS

All extracted with `class4_child1_cert_extractor_exact.ts` (repo-verbatim),
blind (empty kill table), FBS=1<<20; every per-move extraction ok and uncapped,
fbt_drops=0, fatal=null on all three; rows sorted with no duplicates before
verification; verified with the independent `verify_bit7_win7_cert.ts`
(root-check + all sub-roots + consumed/rows union); root hex absent from all
published win7-certificates records (GitHub code search: 0 hits each).

| bit | root hex | rows | extraction nodes | mobility | sub-roots | union miss/extra | md5 |
|---:|---|---:|---:|---:|---:|---|---|
| 18 | `00000000000000803202000000042000` | 33,459 | 4,373,998 | 48 | 48/48 | 0/0 | `5243fd42...` |
| 77 | `00000000000020803202000000002000` | 35,070 | 5,954,462 | 46 | 46/46 | 0/0 | `64616259...` |
| 120 | `01000000000000803202000000002000` | 41,969 | 12,289,825 | 51 | 51/51 | 0/0 | `3db43cd6...` |

- bit18 pushed as a single 1,208,076-byte file (commit `9983c533`), bit77 as a
  single 1,265,598-byte file (commit `787306d7`), bit120 as a line-boundary
  2-part split + README with joined md5 `3db43cd61598091d29f51417e6de9bf3`
  (commit `68ab3386`); all remote md5s verified identical after landing.
- Terminal ranges within [13,17] on all three.

## Frontier recompute after cost-58b

`recompute_frontier_cost58b_20261114.py` (direct runpy extension of the
published cost-56a script): every staged control through after-cost-56a
reproduced exactly (asserted 927 / 6,920 / 544,617 / 5,190/408,340), the
completed cost-58b sweep record, claim (status completed) and receipts record
are asserted, the child's demand (c1=0,c2=1,c4=1) is re-derived from the
frontier and matched, then the three receipts are added.

- cost-58b additions (covers / marginal / in-manifest):
  - bit 18: 7 / 6 / 3 (incl. the swept child's own orbit
    `00000000000000803202000000002000`)
  - bit 77: 7 / 6 / 3 (incl. the same orbit)
  - bit 120: 7 / 7 / 4 (incl. the same orbit and a cross-parent orbit
    `00000000020000003802000000000400`)
- **after cost-58b: solved 935 · unique remaining 6,912 · sum 544,040 ·
  open 5,182 / 407,763.**
- Second class-2 target S5 `00000000000000803202000000000000`: 39 -> 35 orbits
  (2,657 -> 2,383), now the best coverable class-2 target (the unclosable
  10-orbit S5 `00000000000000809082000000000000` stays best nominal class-2).
  Best class-4 unchanged (18 / 1,460; class4-lane parallel on cost-86e raw
  batches). Next class-2 after it: `00000000000000809102000000000000` (38 /
  2,721, parallel lane on cost-63a) and the third target
  `0000000000000080120a000000000000` (56 / 4,066).
- Two consecutive runs byte-identical (JSON + both CSVs).

## Operational notes

- The 58-candidate sweep (30.7M v16 nodes) plus three certificate extractions
  (22.6M nodes) and cross-checks all fit in well under an hour of compute on
  the v16/v15 pair; per-candidate sweep cost stayed in the low millions of
  nodes.
- push_files landed the bit18 and bit77 certificates byte-exact in single
  shots; the bit120 certificate (~1.5MB) hit MemoryLimitError mid-read but the
  push landed anyway — remote md5 verification after landing remains
  mandatory.
- Concurrent-main hygiene: main was re-fetched before every push; the parallel
  lanes' raw batches (cost-63a batch 1, cost-86e batches 1-2) touched different
  files and no conflict occurred.

## Status

11x11 empty board: UNKNOWN. Two-stone root {49,60}: UNKNOWN. S2 {59,60}:
UNKNOWN. class 2 / class 4 blockers: UNKNOWN. WIN7 certificates prove only
individual 7-stone roots within depth 10; REFUTED-D10 sweeps prove only the
absence of such receipts.
