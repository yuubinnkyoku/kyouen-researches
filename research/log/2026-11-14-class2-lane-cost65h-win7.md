# 2026-11-14 class2-lane: cost-65h sweep — 13 WIN7-D10 (3 certificates verified), second of the cost-65 band pair

Long-term lane parallel execution (running alongside session 12, which had
completed cost-65g). Sweep target: the cost-65 child
`00000000000000803202000000001000` of the second class-2 target S5
`00000000000000803202000000000000`, named cost-65h (cost-65 / -65b (sterile) /
-65c / -65d / -65e / -65f / -65g occupied; the sibling
`00000000000000803202000000080000` was subsequently claimed by session 12 as
cost-65i, closing the band pair).

## Claim and candidate enumeration

- Claim pushed before any sweep batch (commit `42bb27ec`):
  `class2-lane-cost65h-inflight-20261114.json`, 65 candidates bit-exact with
  the published edge cost 65 (independent `legal_candidates.py` Bareiss
  enumeration).
- **Per the cost-61e correction lesson**, the child's membership among the
  parent's remaining children (18 orbits / 1,277 after cost-65g; cost-65 band
  pair) and its non-empty demand (c1=0, c2=2, c4=0) were re-verified from
  `class-frontier-top-candidates-s6-after-cost65g-20261114.csv` BEFORE the
  claim.
- Engine: the v16 runner (`class4_child1_runner_v16.ts`, repo-verbatim), depth
  10, andclose=1, cap 1e9; pilot d6 control loss=false at exactly 3,402 nodes in
  all 9 batch invocations.

## Sweep result

**65/65 candidates: 13 WIN7-D10 + 52 REFUTED, 0 capped, 57,639,642 v16
nodes** (9 batches 8x8+1, raw JSONL pushed per batch as completed; terminal
range [13,17] on every candidate).

- WIN7 bits: 4, 7, 14, 24, 33, 40, 43, 67, 99, 102, 109, 117, 118.
- Heaviest candidates: bit 102 (3,354,664, WIN7), bit 14 (3,338,467, WIN7),
  bit 43 (3,269,824, WIN7), bit 4 (2,875,171, WIN7), bit 114 (2,361,961,
  REFUTED), bit 118 (2,307,338, WIN7).
- Determinism: bits 43 (WIN7), 102 (WIN7) and 87 (REFUTED) re-solved fresh in
  a separate process, node-exact identical
  (`class2-lane-cost65h-v16-determinism-rerun-20261114.jsonl`).
- v15 cross-engine anchors (pilot 5,949 PASS): bits 7/109/24 all loss=true at
  2,354,374 / 3,048,755 / 4,038,657 nodes and bit 87 loss=false at 1,492,948
  nodes — verdicts identical to v16
  (`class2-lane-cost65h-v15-crosscheck-20261114.jsonl`).
- Duplicate-root check: all 13 WIN7 root hexes code-searched over
  yuubinnkyoku/kyouen-researches before pushing certificates: 0 hits each
  (no cost-61e bit-1 / cost-65g bit-1 cross-child duplicate pattern).

## Three WIN7 certificates — all verification PASS

Three WIN7 candidates were extracted with
`class4_child1_cert_extractor_exact.ts` (repo-verbatim), blind, FBS=1<<20;
every per-move extraction ok and uncapped, fbt_drops=0 on all three; rows
sorted unique; verified with `verify_bit7_win7_cert.ts` (root-check + all
sub-roots + consumed/rows union).

| bit | root hex | rows | extraction nodes | mobility | sub-roots | union miss/extra | md5 |
|---:|---|---:|---:|---:|---:|---|---|
| 7 | `00000000000000803202000000001080` | 28,375 | 4,165,959 | 51 | 51/51 | 0/0 | `db2f1980...` |
| 109 | `00002000000000803202000000001000` | 26,774 | 5,149,589 | 50 | 50/50 | 0/0 | `74bbb79c...` |
| 24 | `00000000000000803202000001001000` | 38,440 | 6,109,915 | 50 | 50/50 | 0/0 | `e8ade711...` |

- All three landed byte-exact with full paged reads; remote md5 verified
  (bit 7 `db2f1980229cd95c3d46d9722f65b84a`, bit 109
  `74bbb79c486ae249606ce3b04096c422`, bit 24
  `e8ade711a7867b01255db657697af731`). Operational note: the bit-24 push hit
  the sandbox memory limit AFTER the push call completed; the remote file was
  verified byte-exact afterwards.
- Certificates: `class2-lane-cost65h-certificates/bit{7,109,24}-root-<hex>.cert`.
- 10 WIN7-D10 bits remain without extracted certificates (4, 14, 33, 40, 43,
  67, 99, 102, 117, 118): warm certificate-rebuild candidates; they change no
  frontier number.
- Records pushed (commit `0c772f2c`): `class2-lane-cost65h-sweep-20261114.json`
  + `class2-lane-cost65h-win7-certificates-20261114.json` + inflight updated
  to status completed.

## Frontier accounting (merged recompute after cost-65h + cost-65i)

Session 12 continued with the sibling child (cost-65i) and merged both lanes'
receipts in a single recompute (`recompute_frontier_cost65h_65i_20261114.py`,
commit `e8f5037a`; see the cost-65i log entry):

- after-cost-65h intermediate: solved 983 · unique remaining 6,864 ·
  sum 540,758 · open 5,134/404,481 (65h receipts marginal: bits 7/109/24 each
  6 marginal / 2 in-manifest).
- after cost-65h+65i: solved 991 · unique remaining 6,856 · sum 540,177 ·
  open 5,126/403,900.
- Second class-2 target S5 `00000000000000803202000000000000`:
  18 -> 15 orbits (1,277 -> 1,072), still the best coverable class-2 target.

## Status

11x11 empty board: UNKNOWN. Two-stone root {49,60}: UNKNOWN. S2 {59,60}:
UNKNOWN. class 2 / class 4 blockers: UNKNOWN. WIN7 certificates prove only
individual 7-stone roots within depth 10; REFUTED-D10 sweeps prove only the
absence of such receipts.
