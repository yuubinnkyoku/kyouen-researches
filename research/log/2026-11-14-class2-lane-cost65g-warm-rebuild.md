# 2026-11-14 class2-lane: cost-65g warm rebuild — all 9 WIN7 bits certified (6 warm certificates), frontier 997 -> 1005

Long-term lane session 12, continuing directly from the cost-63e warm rebuild
(solved 997; commits `19b441b5` + `9392852e`). Target: the 6 unverified
WIN7-D10 bits of the cost-65g sweep of the child
`00000000000000803202000000000004` (second class-2 target S5
`00000000000000803202000000000000`), i.e. the warm certificate-rebuild
candidates listed in the cost-65i and cost-63e-warm logs (bits 0, 15, 44, 52,
75, 105). The original cost-65g sweep had 9 WIN7-D10 bits, of which 3 (bits
94, 1, 86) were already certified in the original sweep records.

## Warm certificates — all 6 verification PASS

Every warm candidate was extracted with `class4_child1_cert_extractor_exact.ts`
(repo-verbatim), blind (empty kill table), FBS=1<<20; every per-move extraction
ok and uncapped, fbt_drops=0 on all six; rows sorted unique; verified with
`verify_bit7_win7_cert.ts` (root-check + all sub-roots + consumed/rows union).
Extraction stdin recipe: `legal_candidates.py <root32hex> | sed -n 2p`.

| bit | root hex | rows | extraction nodes | mobility | sub-roots | union miss/extra | md5 |
|---:|---|---:|---:|---:|---:|---|---|
| 0 | `00000000000000803202000000000005` | 42,091 | 13,545,545 | 54 | 54/54 | 0/0 | `967a9275...` |
| 15 | `00000000000000803202000000008004` | 41,226 | 7,209,440 | 52 | 52/52 | 0/0 | `0cd7de22...` |
| 44 | `00000000000000803202100000000004` | 40,807 | 11,705,049 | 52 | 52/52 | 0/0 | `c09c0854...` |
| 52 | `00000000000000803212000000000004` | 37,706 | 9,427,271 | 51 | 51/51 | 0/0 | `9f2e448d...` |
| 75 | `00000000000008803202000000000004` | 39,625 | 7,380,455 | 52 | 52/52 | 0/0 | `d270c5df...` |
| 105 | `00000200000000803202000000000004` | 43,743 | 10,918,655 | 52 | 52/52 | 0/0 | `97d3c67b...` |

- v15 cross-engine anchors from the original sweep records carried over: bits
  0, 44 and 105 v15 loss=true at 9,114,880 / 7,286,939 / 7,366,826 nodes
  (verdicts identical to the v16 sweep).
- All six landed byte-exact with full paged reads (every push reported the 16
  MiB sandbox record limit AFTER the push call completed — verified landed and
  remote-md5-verified on all six).
- Root absence: GitHub code search for each root hex returns exactly 1 hit —
  the cost-65g sweep record `win7_roots` listing, no certificate existed;
  first publication on all six (the cost-61e bit-1 cross-child duplicate
  pattern does not occur here).
- Terminal ranges within [13,17] on all six.

## Warm-record format (original records untouched)

The cost-65g sweep/certificate records (3 certificates, bits 94/1/86) are
referenced with asserts by the published recompute chain and were NOT
modified. The 6 warm certificates were added to the same
`class2-lane-cost65g-certificates/` directory, and a NEW record
`class2-lane-cost65g-warm-certificates-20261114.json` (6 entries, recipe
documented) records their receipts — same pattern as the cost-63e warm record.

## Frontier recompute after cost-65g warm

`recompute_frontier_cost65g_warm_20261114.py` (direct runpy extension of the
published cost-63e-warm script): every staged control through
after-cost-63e-warm reproduced exactly (asserted 997 / 6,850 / 539,745 /
5,120/403,468), the original cost-65g sweep record's unverified bits are
asserted to be exactly [0,15,44,52,75,105], and the 6 warm receipts are added.

- Warm receipt marginals (covers / marginal / in-manifest): bits 0, 44, 75
  each 7/6/2, bits 15, 52 each 7/5/1, bit 105 7/4/0; net in-manifest +8.
- **after cost-65g-warm: solved 1005 · unique remaining 6,842 · sum 539,174 ·
  open 5,112 / 402,897**.
- Second class-2 target S5 `00000000000000803202000000000000`: **14 -> 10
  orbits (1,001 -> 721)** — the warm receipts removed 4 of its remaining
  child orbits; still the best coverable class-2 target. Best class-4
  unchanged (18 / 1,460).
- Records + recompute JSON + ranking CSVs + script pushed (single commit),
  remote md5 verified on all 5 files. Two consecutive recompute runs
  byte-identical (JSON + both CSVs).

## Operational notes

- All 9 cost-65g WIN7-D10 bits now have verified certificates (3 original +
  6 warm); cost-65g leaves zero unverified WIN7 bits, matching cost-65i and
  cost-63e. All-band warm candidates now: cost-60b 19 · cost-61d 11 ·
  cost-61e 9 · cost-61f 8 · cost-62a 10 · cost-63e 0 · cost-64b 17 ·
  cost-65g 0 · cost-65h 10 (parallel-lane sweep; coordinate before touching)
  · cost-65i 0.
- Next cheapest remaining children of the second class-2 target (per
  `class-frontier-top-candidates-s6-after-cost65g-warm-20261114.csv`):
  cost-67b `00000000000000803202000020000000` claimed by the parallel lane
  (raw sweep 67/67 complete at commit `3fa0fe7c`, records pending); then
  `00000000000000803202000400000000` (68) and `00000000000000803202000000008000`
  (69). Verify membership + demand from the latest main before claiming.
- The 6 warm extractions cost 60,186,415 nodes total (~24 s wall each), all
  well under the depth-10 caps; cheap relative to a new sweep.

## Status

11x11 empty board: UNKNOWN. Two-stone root {49,60}: UNKNOWN. S2 {59,60}:
UNKNOWN. class 2 / class 4 blockers: UNKNOWN. WIN7 certificates prove only
individual 7-stone roots within depth 10; REFUTED-D10 sweeps prove only the
absence of such receipts.
