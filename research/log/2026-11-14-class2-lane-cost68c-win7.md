# 2026-11-14 class2-lane: cost-68c sweep — 5 WIN7-D10 (3 certificates verified, all 5 WIN7 bits v15-anchored), frontier 993 -> 998

Long-term lane parallel execution, continuing after the cost-67b frontier
recompute (after-cost-67b solved 993; cost-67b receipts by this lane, commit
`9116a60d`). Sweep target: the cost-68 child
`00000000000000803202000400000000` of the second class-2 target S5
`00000000000000803202000000000000`, named cost-68c (cost-68 / cost-68b
occupied by earlier lanes; this child is the parent's only cost-68 child and
the cheapest remaining unswept child after cost-67b).

## Claim and candidate enumeration

- Claim pushed before any sweep batch (commit `ee1d0591`):
  `class2-lane-cost68c-inflight-20261114.json`, 68 candidates bit-exact with
  the published edge cost 68 (independent `legal_candidates.py` Bareiss
  enumeration).
- **Per the cost-61e correction lesson**, the child's membership among the
  parent's remaining children (14 orbits / 1,005 after cost-67b) and its
  non-empty demand (c1=0, c2=1, c4=0) were re-verified from
  `class-frontier-top-candidates-s6-after-cost67b-20261114.csv` BEFORE the
  claim.
- Engine: the v16 runner (`class4_child1_runner_v16.ts`, repo-verbatim), depth
  10, andclose=1, cap 1e9; pilot d6 control loss=false at exactly 3,402 nodes
  in all 9 batch invocations.

## Sweep result

**68/68 candidates: 5 WIN7-D10 + 63 REFUTED, 0 capped, 104,482,623 v16
nodes** (9 batches 8x8+4, raw JSONL pushed as completed — commits `cf872e3b`
/ `0b9e53d4`; terminal range [13,17] on every candidate).

- WIN7 bits: 11, 21, 24, 53, 118.
- Heaviest candidates: bit 75 (7,717,013, REFUTED), bit 113 (4,620,886,
  REFUTED), bit 74 (4,394,457, REFUTED), bit 28 (4,386,248, REFUTED), bit
  103 (4,303,685, REFUTED), bit 87 (4,058,225, REFUTED).
- Determinism: bit 24 (WIN7, 2,738,947 nodes) and bit 75 (REFUTED, 7,717,013
  nodes — the heaviest overall candidate) re-solved fresh in a separate
  process, node-exact identical
  (`class2-lane-cost68c-v16-determinism-rerun-20261114.jsonl`, commit
  `f94d18aa`).
- v15 cross-engine anchors (pilot 5,949 PASS): **all 5 WIN7 bits** loss=true
  at 1,662,130 (21) / 4,310,842 (11) / 2,163,356 (118) / 7,811,750 (24) /
  4,957,133 (53) nodes — verdicts identical to v16
  (`class2-lane-cost68c-v15-crosscheck-20261114.jsonl`, same commit).
- Duplicate-root check: all 5 WIN7 root hexes code-searched over
  yuubinnkyoku/kyouen-researches before pushing certificates. 4 roots 0 hits.
  The bit-21 root `00000000000000803202000400200000` is a **cross-child
  duplicate** of the cost-60b bit-34 win7_roots listing (cost-61e bit-1 /
  cost-65g bit-1 / cost-67b bit-20 pattern: the same 7-stone root is
  reachable from two S6 children, here `00000000000000803202000000000000`'s
  children `00000000000000803202000000000000`-side and
  `00000000000000803202000400000000`); it had NO prior published certificate
  (cost-60b certified bits 117/96/94/105/73/23 only), so this certificate is
  new coverage and also closes the cost-60b bit-34 warm entry.

## Three WIN7 certificates — all verification PASS

Three WIN7 candidates were extracted with
`class4_child1_cert_extractor_exact.ts` (repo-verbatim), blind, FBS=1<<20;
fbt_drops=0 on all three; rows sorted unique; verified with
`verify_bit7_win7_cert.ts` (root-check + all sub-roots + consumed/rows
union).

| bit | root hex | rows | extraction nodes | mobility | sub-roots | union miss/extra | md5 |
|---:|---|---:|---:|---:|---:|---|---|
| 21 | `00000000000000803202000400200000` | 23,096 | 2,955,284 | 47 | 47/47 | 0/0 | `933f5b5a...` |
| 11 | `00000000000000803202000400000800` | 40,600 | 8,468,317 | 50 | 50/50 | 0/0 | `70bf8e05...` |
| 118 | `00400000000000803202000400000000` | 31,576 | 4,236,453 | 56 | 56/56 | 0/0 | `70ce9f70...` |

- All three landed byte-exact with full paged reads (commits `3b1b8aca` /
  `b0eb8087` / `04acce4b`); remote md5 verified (bit 21
  `933f5b5a08f23159a447848d54409d91`, bit 11
  `70bf8e0578bd31321fd1b5e6640eb540`, bit 118
  `70ce9f70f613923402d74454aa87062f`). Operational note: the bit-11 push hit
  the sandbox memory limit AFTER the push call completed; the remote file was
  verified byte-exact afterwards.
- Certificates: `class2-lane-cost68c-certificates/bit{21,11,118}-root-<hex>.cert`.
- 2 WIN7-D10 bits remain without extracted certificates (24, 53): warm
  certificate-rebuild candidates; they change no frontier number.
- Records pushed (commit `66c98b25`): sweep record + win7-certificates record
  (schema-consistent with the cost-65h/67b records: per-certificate verdict /
  sub_roots_verified / root_check object) + inflight updated to completed.

## Frontier recompute after cost-68c

`recompute_frontier_cost68c_20261114.py` (direct runpy extension of the
published `recompute_frontier_cost67b_20261114.py`; commit `368e2b1f`): every
staged control through after-cost-67b reproduced exactly (asserted
993/6,854/540,035/5,124/403,758), the completed cost-68c
sweep/claim/demand/receipts are asserted, and the child remaining-membership
and demand (c1=0,c2=1,c4=0) are re-derived from the frontier and asserted.

- cost-68c additions (covers / marginal / in-manifest): bit 21: 7/6/2, bit
  11: 7/5/2, bit 118: 7/6/3.
- **after cost-68c: solved 998 · unique remaining 6,849 · sum 539,673 ·
  open 5,119 / 403,396** (net in-manifest +5 from 993).
- Second class-2 target S5 `00000000000000803202000000000000`:
  14 -> 12 orbits (1,005 -> 864), still the best coverable class-2 target.
  Next cheapest remaining children: two cost-69 children
  `00000000000000803202000000008000` and `00000000000000803222000000000000`
  (both c1=0,c2=2,c4=0) — band names cost-69a/-69b/-69c/-69d occupied, a
  future sweep would be cost-69e+. Best class-4 unchanged (18 / 1,460).
- Two consecutive recompute runs byte-identical (JSON + both CSVs); remote
  md5 verified for the recompute JSON, ranking CSV, top-candidates CSV and
  the script.

## Status

11x11 empty board: UNKNOWN. Two-stone root {49,60}: UNKNOWN. S2 {59,60}:
UNKNOWN. class 2 / class 4 blockers: UNKNOWN. WIN7 certificates prove only
individual 7-stone roots within depth 10; REFUTED-D10 sweeps prove only the
absence of such receipts.
