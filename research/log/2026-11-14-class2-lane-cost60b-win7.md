# 2026-11-14 class2-lane: cost-60b sweep — 25 WIN7-D10 (6 certificates verified), frontier 935 -> 946

Long-term lane session 12, continuing directly from the cost-58b result on the
same lane (after-cost-58b frontier solved 935; commits `d6d68a6d` +
`6b8ff79e`). The cheapest remaining unswept child of the second class-2 target
S5 `00000000000000803202000000000000` (35 orbits / 2,383 after cost-58b, best
coverable class-2 target) was the cost-60 child
`00000000000000803202000000200000`. Named cost-60b because the cost-60 band
name is already occupied by the published sweep of child
`00000000000000801a02000020000000` (`class2-lane-cost60-sweep-20261114.json`,
a different S5 target). While this sweep ran, the parallel lanes advanced raw
batches of cost-63a (class-2) and cost-86e (class-4, 73/86 candidates all
REFUTED so far); no new certificates from those lanes landed before this
recompute.

## Claim and candidate enumeration

- Claim pushed before any sweep batch (commit `32f0035b`):
  `class2-lane-cost60b-inflight-20261114.json`, 60 candidates bit-exact with the
  published edge cost 60 (independent `legal_candidates.py` Bareiss
  enumeration); demand classes c1=0, c2=2, c4=0.
- Engine: the v16 runner (`class4_child1_runner_v16.ts`), validated this
  session by the depth-10 verdict-agreement gate and already the sweep engine
  for cost-56a and cost-58b. Pilot d6 control loss=false at exactly 3,402 nodes
  in all 8 batch invocations.

## Sweep result

**60/60 candidates: 25 WIN7-D10 + 35 REFUTED, 0 capped, 24,832,895 v16 nodes**
(8 batches, raw JSONL pushed per batch, commit `1684b3ec`; terminal range
[13,17] on every candidate). This is the most WIN7-rich class-2 child swept so
far (25/60 = 42%, vs 19/60 on the cost-60 band of the other target and 11/62
on cost-62a).

- WIN7 bits: 8, 15, 22, 23, 26, 28, 32, 34, 40, 43, 44, 73, 74, 77, 87, 88,
  94, 95, 96, 100, 105, 106, 108, 114, 117 (roots = child | bit, listed in the
  sweep record).
- Heaviest candidates: bit 43 (1,521,565), bit 114 (1,427,777), bit 32
  (1,199,043), bit 108 (1,006,969), bit 100 (846,028), bit 22 (801,126).
- Determinism: bits 43, 114 and 117 re-solved fresh in a separate process,
  node-exact identical
  (`class2-lane-cost60b-v16-determinism-rerun-20261114.jsonl`).
- v15 cross-engine anchors (pilot 5,949 PASS): bits 43/114/32/117 all loss=true
  at 3,882,328 / 3,898,429 / 3,192,492 / 664,210 nodes — verdicts identical to
  v16 (`class2-lane-cost60b-v15-crosscheck-20261114.jsonl`).

## Six WIN7 certificates — all verification PASS

The six cheapest WIN7 candidates were extracted with
`class4_child1_cert_extractor_exact.ts` (repo-verbatim), blind (empty kill
table), FBS=1<<20; every per-move extraction ok and uncapped, fbt_drops=0 on
all six; rows sorted with no duplicates; verified with the independent
`verify_bit7_win7_cert.ts` (root-check + all sub-roots + consumed/rows union);
root hex absent from all published win7-certificates records (GitHub code
search: 0 hits each).

| bit | root hex | rows | extraction nodes | mobility | sub-roots | union miss/extra | md5 |
|---:|---|---:|---:|---:|---:|---|---|
| 117 | `00200000000000803202000000200000` | 10,145 | 1,102,035 | 37 | 37/37 | 0/0 | `94f9411a...` |
| 96 | `00000001000000803202000000200000` | 15,654 | 734,068 | 43 | 43/43 | 0/0 | `f60bfdad...` |
| 94 | `00000000400000803202000000200000` | 17,637 | 1,145,298 | 40 | 40/40 | 0/0 | `9d05d9d1...` |
| 105 | `00000200000000803202000000200000` | 15,804 | 1,130,428 | 45 | 45/45 | 0/0 | `8544bb5d...` |
| 73 | `00000000000002803202000000200000` | 19,986 | 1,711,622 | 43 | 43/43 | 0/0 | `79c7d729...` |
| 23 | `00000000000000803202000000a00000` | 18,570 | 1,696,945 | 45 | 45/45 | 0/0 | `458fe88d...` |

- The remaining 19 WIN7-D10 bits (8,15,22,26,28,32,34,40,43,44,74,77,87,88,95,
  100,106,108,114) stay warm certificate-rebuild candidates per the cost-62a
  precedent; bits 43/114/32 carry v15 loss=true cross-engine anchors.
- Terminal ranges within [13,17] on all six.

## Frontier recompute after cost-60b

`recompute_frontier_cost60b_20261114.py` (direct runpy extension of the
published cost-58b script): every staged control through after-cost-58b
reproduced exactly (asserted 935 / 6,912 / 544,040 / 5,182/407,763), the
completed cost-60b sweep record, claim (status completed) and receipts record
are asserted, the child's demand (c1=0,c2=2,c4=0) is re-derived from the
frontier and matched, then the six receipts are added.

- cost-60b additions (covers / marginal / in-manifest): bit 117: 7/7/3,
  bit 96: 7/7/3, bit 94: 7/7/3, bit 105: 7/7/3, bit 73: 7/6/2, bit 23: 7/6/2
  (each includes the swept child's own orbit
  `00000000000000803202000000200000`; the additions overlap across receipts,
  net in-manifest +11).
- **after cost-60b: solved 946 · unique remaining 6,901 · sum 543,316 ·
  open 5,171 / 407,039.**
- Second class-2 target S5 `00000000000000803202000000000000`: 35 -> 29 orbits
  (2,383 -> 2,005), still the best coverable class-2 target (unclosable
  10-orbit S5 `00000000000000809082000000000000` stays nominal best class-2).
  Third class-2 target `0000000000000080120a000000000000`: 56 -> 55 orbits
  (4,066 -> 4,001) — one of the six receipts covered an orbit of that target
  as well. Best class-4 unchanged (18 / 1,460).
- Two consecutive runs byte-identical (JSON + both CSVs).

## Operational notes

- **push_files read truncation re-confirmed the hard way**: reading a
  certificate without an explicit offset/limit pages returns only the first
  ~64KB page, and push_files lands that truncated content silently (all six
  certificates initially landed at ~64KB). With full paged reads
  (limit=2000-4000 lines, offset/next_offset loop, join-length asserted
  against the local byte count) every re-push landed byte-exact; remote md5
  re-verified for all six. MemoryLimitError can fire mid-block and the push
  may or may not have landed — always re-fetch and md5-verify.
- The 25-WIN7 sweep plus 6 extractions (~7.5M extraction nodes) plus
  cross-checks ran in a few minutes of compute; the remaining 19 warm
  certificate candidates cost roughly 3-5x that to extract if wanted.
- Concurrent-main hygiene: main was re-fetched before every push; two
  fast-forward rejections (parallel cost-86e batch pushes) were resolved by
  re-pushing unchanged content on the new HEAD; no file conflicts.

## Status

11x11 empty board: UNKNOWN. Two-stone root {49,60}: UNKNOWN. S2 {59,60}:
UNKNOWN. class 2 / class 4 blockers: UNKNOWN. WIN7 certificates prove only
individual 7-stone roots within depth 10; REFUTED-D10 sweeps prove only the
absence of such receipts.
