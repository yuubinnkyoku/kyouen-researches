# 2026-11-14 class2-lane: cost-63e warm rebuild — all 8 WIN7 bits certified (5 warm certificates), frontier 991 -> 997

Long-term lane session 12, continuing directly from the merged cost-65h+65i
frontier (solved 991; commits `e8f5037a` + `25754db8`). Target: the 5
unverified WIN7-D10 bits of the cost-63e sweep of the child
`00000000000000803202200000000000` (second class-2 target S5
`00000000000000803202000000000000`), i.e. the warm certificate-rebuild
candidates listed in the cost-65i log (bits 42, 73, 100, 116, 120). The
original cost-63e sweep had 8 WIN7-D10 bits, of which 3 (bits 28, 90, 97) were
already certified in the original sweep records.

## Warm certificates — all 5 verification PASS

Every warm candidate was extracted with `class4_child1_cert_extractor_exact.ts`
(repo-verbatim), blind (empty kill table), FBS=1<<20; every per-move extraction
ok and uncapped, fbt_drops=0 on all five; rows sorted unique; verified with
`verify_bit7_win7_cert.ts` (root-check + all sub-roots + consumed/rows union).
Extraction stdin recipe: `legal_candidates.py <root32hex> | sed -n 2p` — the
`sed -n 2p` replacement for the historical `head -2 | LC_ALL=C sort -u` recipe
(fixed in the cost-65i sweep after the bit-43 line-order failure; the
candidate-bits line is always line 2).

| bit | root hex | rows | extraction nodes | mobility | sub-roots | union miss/extra | md5 |
|---:|---|---:|---:|---:|---:|---|---|
| 42 | `00000000000000803202240000000000` | 45,348 | 6,853,938 | 54 | 54/54 | 0/0 | `d5f9bf43...` |
| 73 | `00000000000002803202200000000000` | 40,313 | 8,122,453 | 50 | 50/50 | 0/0 | `19f1ace0...` |
| 100 | `00000010000000803202200000000000` | 33,856 | 8,274,380 | 49 | 49/49 | 0/0 | `ba80e653...` |
| 116 | `00100000000000803202200000000000` | 48,268 | 13,532,545 | 53 | 53/53 | 0/0 | `aac6e20a...` |
| 120 | `01000000000000803202200000000000` | 44,172 | 11,429,678 | 55 | 55/55 | 0/0 | `9dbba316...` |

- v15 cross-engine anchors from the original sweep records carried over: bits
  116 and 120 v15 loss=true at 7,081,266 / 5,199,573 nodes (plus the sweep's
  earlier anchors on other bits).
- All five landed byte-exact with full paged reads (commits `afdb1109` /
  `1fa74c58` / `3c391a0a` / `065c467a` / `708b689b`); remote md5 verified on
  every file (the bit-42 and bit-120 pushes hit the 16 MiB sandbox record
  limit AFTER the push call completed — verified landed).
- Root absence: GitHub code search 0 hits each (all 5 warm roots checked; the
  cost-61e bit-1 cross-child duplicate pattern does not occur here — that
  root's 2 hits were both sweep/win7_roots listings, not certificates).
- Terminal ranges within [13,17] on all five.

## New warm-record format (original records untouched)

The cost-63e sweep/certificate records (3 certificates, bits 28/90/97) are
referenced with asserts by the published recompute chain and were NOT
modified. The 5 warm certificates were added to the same
`class2-lane-cost63e-certificates/` directory, and a NEW record
`class2-lane-cost63e-warm-certificates-20261114.json` (5 entries, recipe
documented) records their receipts. This keeps the public recompute chain
intact while extending the manifest.

## Frontier recompute after cost-63e warm

`recompute_frontier_cost63e_warm_20261114.py` (direct runpy extension of the
published cost-65h+65i merged script): every staged control through
after-cost-65h+65i reproduced exactly (asserted 991 / 6,856 / 540,177 /
5,126/403,900), the original cost-63e sweep record's unverified bits are
asserted to be exactly [42,73,100,116,120], and the 5 warm receipts are added.

- Warm receipt marginals (covers / marginal / in-manifest): bits 42, 73, 100,
  120 each 5/1/... and bit 116 6/2; net in-manifest +6.
- **after cost-63e-warm: solved 997 · unique remaining 6,850 · sum 539,745 ·
  open 5,120 / 403,468**.
- Second class-2 target S5 `00000000000000803202000000000000`: 15 -> 14 orbits
  (1,072 -> 1,001), still the best coverable class-2 target. Best class-4
  unchanged (18 / 1,460).
- Records + recompute JSON + ranking CSVs + script pushed in commit
  `19b441b5` (a first attempt did not land — the re-push of identical local
  files landed cleanly), remote md5 verified on all 5 files. Two consecutive
  recompute runs byte-identical (JSON + both CSVs).

## Operational notes

- All 8 cost-63e WIN7-D10 bits now have verified certificates (3 original + 5
  warm); cost-63e leaves zero unverified WIN7 bits, matching cost-65i.
- Warm candidates remaining: cost-60b 19 · cost-61d 11 · cost-61e 9 ·
  cost-61f 8 · cost-63e 0 · cost-64b 17 · cost-62a 10 · cost-65g 6 (bits
  0,15,44,52,75,105) · cost-65h 10 (bits 4,14,33,40,43,67,99,102,117,118 —
  parallel-lane sweep; coordinate before touching) · cost-65i 0.
- Next cheapest remaining children of the second class-2 target (per
  `class-frontier-top-candidates-s6-after-cost63e-warm-20261114.csv`):
  cost-67b `00000000000000803202000020000000` claimed by the parallel lane
  (raw sweep 67/67 complete at commit `3fa0fe7c`, records pending); then
  `00000000000000803202000400000000` (68) and `00000000000000803202000000008000`
  (69). Verify membership + demand from the latest main before claiming.

## Status

11x11 empty board: UNKNOWN. Two-stone root {49,60}: UNKNOWN. S2 {59,60}:
UNKNOWN. class 2 / class 4 blockers: UNKNOWN. WIN7 certificates prove only
individual 7-stone roots within depth 10; REFUTED-D10 sweeps prove only the
absence of such receipts.
