# 2026-11-14 class2-lane: cost-67b sweep — 7 WIN7-D10 (3 certificates verified, all 7 WIN7 bits v15-anchored), frontier 991 -> 993

Long-term lane parallel execution, continuing after the merged cost-65h+65i
frontier recompute (after-cost-65h-65i solved 991; the cost-65h receipts by this
lane, the cost-65i receipts by session 12, merged recompute commit `e8f5037a`).
Sweep target: the cost-67 child `00000000000000803202000020000000` of the
second class-2 target S5 `00000000000000803202000000000000`, named cost-67b
(cost-67 occupied by the child `00000000000000809082020000000000` of the
receipt-unclosable S5 `00000000000000809082000000000000`).

## Claim and candidate enumeration

- Claim pushed before any sweep batch (commit `88885656`):
  `class2-lane-cost67b-inflight-20261114.json`, 67 candidates bit-exact with
  the published edge cost 67 (independent `legal_candidates.py` Bareiss
  enumeration).
- **Per the cost-61e correction lesson**, the child's membership among the
  parent's remaining children (15 orbits / 1,072 after cost-65h-65i; cheapest
  remaining unswept child) and its non-empty demand (c1=0, c2=2, c4=0) were
  re-verified from
  `class-frontier-top-candidates-s6-after-cost65h-65i-20261114.csv` BEFORE the
  claim.
- Engine: the v16 runner (`class4_child1_runner_v16.ts`, repo-verbatim), depth
  10, andclose=1, cap 1e9; pilot d6 control loss=false at exactly 3,402 nodes
  in all 9 batch invocations.

## Sweep result

**67/67 candidates: 7 WIN7-D10 + 60 REFUTED, 0 capped, 64,859,548 v16
nodes** (9 batches 8x8+3, raw JSONL pushed per batch — commits `2e406598` /
`2cc2e96d` / `3fa0fe7c`; terminal range [13,17] on every candidate).

- WIN7 bits: 11, 17, 20, 33, 99, 109, 117.
- Heaviest candidates: bit 42 (8,712,578, REFUTED), bit 32 (7,060,598,
  REFUTED), bit 76 (3,742,029, REFUTED), bit 33 (3,299,841, WIN7), bit 6
  (3,214,046, REFUTED), bit 118 (2,456,089, REFUTED).
- Determinism: bits 33 (WIN7), 6 (REFUTED) and 99 (WIN7) re-solved fresh in a
  separate process, node-exact identical
  (`class2-lane-cost67b-v16-determinism-rerun-20261114.jsonl`, commit
  `5e5bd313`).
- v15 cross-engine anchors (pilot 5,949 PASS): **all 7 WIN7 bits** loss=true
  at 3,201,038 (11) / 1,775,234 (17) / 2,055,608 (20) / 6,238,220 (33) /
  2,176,741 (99) / 2,011,805 (109) / 1,840,199 (117) nodes — verdicts
  identical to v16 (`class2-lane-cost67b-v15-crosscheck-20261114.jsonl`, same
  commit).
- Duplicate-root check: all 7 WIN7 root hexes code-searched over
  yuubinnkyoku/kyouen-researches before pushing certificates. 6 roots 0 hits.
  The bit-20 root `00000000000000803202000020100000` is a **cross-child
  duplicate** of the cost-64b bit-29 win7_roots listing (cost-61e bit-1 /
  cost-65g bit-1 pattern: the same 7-stone root is reachable from two S6
  children, here `00000000000000803202000000100000` and
  `00000000000000803202000020000000`); it had NO prior published certificate
  (cost-64b certified bits 73/7/99 only), so a future certificate for it is new
  coverage.

## Three WIN7 certificates — all verification PASS

Three WIN7 candidates (the cheapest per certificate) were extracted with
`class4_child1_cert_extractor_exact.ts` (repo-verbatim), blind, FBS=1<<20;
fbt_drops=0 on all three; rows sorted unique; verified with
`verify_bit7_win7_cert.ts` (root-check + all sub-roots + consumed/rows union).

| bit | root hex | rows | extraction nodes | mobility | sub-roots | union miss/extra | md5 |
|---:|---|---:|---:|---:|---:|---|---|
| 17 | `00000000000000803202000020020000` | 34,860 | 2,884,412 | 47 | 47/47 | 0/0 | `6a75b5f7...` |
| 117 | `00200000000000803202000020000000` | 32,441 | 3,212,680 | 50 | 50/50 | 0/0 | `1989bfd4...` |
| 109 | `00002000000000803202000020000000` | 27,559 | 3,211,752 | 47 | 47/47 | 0/0 | `4812896a...` |

- All three landed byte-exact with full paged reads (commits `57d052aa` /
  `fa184c80` / `e9280223`); remote md5 verified (bit 17
  `6a75b5f707ca9686bdc0653549c72d4e`, bit 117
  `1989bfd4fb2113737529def5055fa48d`, bit 109
  `4812896aa31933cd61b8116bb95ca449`).
- Certificates: `class2-lane-cost67b-certificates/bit{17,117,109}-root-<hex>.cert`.
- 4 WIN7-D10 bits remain without extracted certificates (11, 20, 33, 99):
  warm certificate-rebuild candidates (bit 20 is the cross-child duplicate of
  the cost-64b bit-29 warm root); they change no frontier number.
- Records pushed (commit `90248fe3`): sweep record + win7-certificates record
  (schema-consistent with the cost-65h records: per-certificate verdict /
  sub_roots_verified / root_check object) + inflight updated to completed.

## Frontier recompute after cost-67b

`recompute_frontier_cost67b_20261114.py` (direct runpy extension of the
published `recompute_frontier_cost65h_65i_20261114.py`; commit `9116a60d`):
every staged control through after-cost-65h-65i reproduced exactly (asserted
991/6,856/540,177/5,124/403,900), the completed cost-67b
sweep/claim/demand/receipts are asserted, and the child remaining-membership
and demand (c1=0,c2=2,c4=0) are re-derived from the frontier and asserted.

- cost-67b additions (covers / marginal / in-manifest): bit 17: 7/5/1, bit
  117: 7/5/1, bit 109: 7/6/2 (the bit-109 extra parent
  `00000000080000809002000000000800` is a class-2 position outside this
  target).
- **after cost-67b: solved 993 · unique remaining 6,854 · sum 540,035 ·
  open 5,124 / 403,758** (net in-manifest +2 from 991).
- Second class-2 target S5 `00000000000000803202000000000000`:
  15 -> 14 orbits (1,072 -> 1,005), still the best coverable class-2 target.
  Next cheapest remaining child: `00000000000000803202000400000000` (cost 68,
  c1=0,c2=1,c4=0) — band names cost-68/cost-68b are occupied (a future sweep
  would be cost-68c). Best class-4 unchanged (18 / 1,460).
- Two consecutive recompute runs byte-identical (JSON + both CSVs); remote
  md5 verified for the recompute JSON, ranking CSV, top-candidates CSV and
  the script.

## Status

11x11 empty board: UNKNOWN. Two-stone root {49,60}: UNKNOWN. S2 {59,60}:
UNKNOWN. class 2 / class 4 blockers: UNKNOWN. WIN7 certificates prove only
individual 7-stone roots within depth 10; REFUTED-D10 sweeps prove only the
absence of such receipts.
