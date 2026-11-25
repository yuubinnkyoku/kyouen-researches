# 2026-11-14 class2-lane: cost-64b sweep — 20 WIN7-D10 (3 certificates verified), frontier 970 -> 974

Long-term lane session 12, continuing directly from the cost-63e result on the
same lane (after-cost-63e frontier solved 970; commits `e4f735c8` + `b268a9fb`).
Sweep target: the cost-64 child `00000000000000803202000000100000` of the
second class-2 target S5 `00000000000000803202000000000000`, named cost-64b
because the cost-64 band name is already occupied by another target's child
(the published cost-64 sweep).

## Claim and candidate enumeration

- Claim pushed before any sweep batch (commit `05a53c9f`):
  `class2-lane-cost64b-inflight-20261114.json`, 64 candidates bit-exact with
  the published edge cost 64 (independent `legal_candidates.py` Bareiss
  enumeration).
- **Per the cost-61e correction lesson**, the child's membership among the
  parent's remaining children (21 orbits / 1,482 after cost-63e, cheapest at
  cost 64) and its non-empty demand (c1=0, c2=2, c4=0) were re-verified from
  `class-frontier-top-candidates-s6-after-cost63e-20261114.csv` BEFORE the
  claim.
- Engine: the v16 runner, agreement-gated in cost-56a and the sweep engine for
  cost-58b / cost-60b / cost-61d / cost-61e / cost-61f / cost-63e. Pilot d6
  control loss=false at exactly 3,402 nodes in all 8 batch invocations.

## Sweep result

**64/64 candidates: 20 WIN7-D10 + 44 REFUTED, 0 capped, 50,655,645 v16
nodes** (8 batches, raw JSONL pushed per batch, commit `1ae7872c`; terminal
range [13,17] on every candidate). 20/64 = 31% WIN7 — the second most
WIN7-rich class-2 child after cost-60b (25/60).

- WIN7 bits: 7, 8, 29, 33, 40, 42, 43, 53, 54, 73, 84, 86, 92, 94, 99, 102,
  103, 109, 116, 117.
- Heaviest candidates: bit 77 (2,446,820, REFUTED), bit 43 (2,441,923), bit 92
  (2,318,162), bit 98 (2,256,840, REFUTED), bit 42 (2,150,846), bit 102
  (2,054,074).
- Determinism: bits 43, 77 and 92 re-solved fresh in a separate process,
  node-exact identical
  (`class2-lane-cost64b-v16-determinism-rerun-20261114.jsonl`, commit `0c7a376b`).
- v15 cross-engine anchors (pilot 5,949 PASS): bits 73/43/92 all loss=true at
  1,793,234 / 6,507,741 / 4,535,899 nodes and bit 77 loss=false at 6,995,995
  nodes — verdicts identical to v16
  (`class2-lane-cost64b-v15-crosscheck-20261114.jsonl`).

## Three WIN7 certificates — all verification PASS

The three cheapest WIN7 candidates were extracted with
`class4_child1_cert_extractor_exact.ts` (repo-verbatim), blind, FBS=1<<20;
every per-move extraction ok and uncapped, fbt_drops=0 on all three; rows
sorted unique; verified with `verify_bit7_win7_cert.ts` (root-check + all
sub-roots + consumed/rows union).

| bit | root hex | rows | extraction nodes | mobility | sub-roots | union miss/extra | md5 |
|---:|---|---:|---:|---:|---:|---|---|
| 73 | `00000000000002803202000000100000` | 28,046 | 2,771,892 | 49 | 49/49 | 0/0 | `aa6bd5f2...` |
| 7 | `00000000000000803202000000100080` | 21,382 | 2,133,560 | 48 | 48/48 | 0/0 | `6751a92c...` |
| 99 | `00000008000000803202000000100000` | 26,812 | 2,569,053 | 48 | 48/48 | 0/0 | `71fe98be...` |

- All three landed byte-exact with full paged reads (commits `06c2a019` /
  `d2ab99f4` / `7340e679`); remote md5 verified.
- Root absence: GitHub code search 0 hits each (all 20 WIN7 roots checked);
  the 3 certificate roots were also matched against the published WIN7
  receipt roots — no duplicates (the cost-61e bit-1 cross-child duplicate
  pattern does not occur here).
- The remaining 17 WIN7-D10 bits (8, 29, 33, 40, 42, 43, 53, 54, 84, 86, 92,
  94, 102, 103, 109, 116, 117) stay warm certificate-rebuild candidates; bits
  43/92 carry v15 loss=true cross-engine anchors.
- Terminal ranges within [13,17] on all three.

## Frontier recompute after cost-64b

`recompute_frontier_cost64b_20261114.py` (direct runpy extension of the
published cost-63e script): every staged control through after-cost-63e
reproduced exactly (asserted 970 / 6,877 / 541,680 / 5,147/405,403), the
completed cost-64b sweep record, claim (status completed) and receipts record
are asserted, the child's remaining-membership and demand (c1=0,c2=2,c4=0)
are re-derived from the frontier and asserted, then the three receipts are
added.

- cost-64b additions (covers / marginal / in-manifest): bit 73: 7/6/2,
  bit 7: 7/6/2, bit 99: 7/6/2 (net in-manifest +4).
- **after cost-64b: solved 974 · unique remaining 6,873 · sum 541,401 ·
  open 5,143 / 405,124.**
- Second class-2 target S5 `00000000000000803202000000000000`: 21 -> 20 orbits
  (1,482 -> 1,418), still the best coverable class-2 target. Best class-4
  unchanged (18 / 1,460).
- Records completed and pushed (commit `9e51f9e6`: sweep record, receipts
  record, completed claim). Frontier recompute + script + rankings pushed in
  commit `5f2de248`, remote md5 verified. Two consecutive recompute runs
  byte-identical (JSON + both CSVs).

## Operational notes

- Next cheapest remaining children of the second class-2 target after
  cost-64b: the cost-65 band triple — `00000000000000803202000000000004`
  (c1=0,c2=2,c4=0), `00000000000000803202000000001000` (c1=0,c2=2,c4=0),
  `00000000000000803202000000080000` (c1=0,c2=2,c4=2) (per
  `class-frontier-top-candidates-s6-after-cost64b-20261114.csv`; verify
  membership + demand again before claiming).
- Session-12 lane totals: cost-56a (1 WIN7), cost-58b (3 WIN7), cost-60b
  (25 WIN7), cost-61d (14 WIN7), cost-61e (13 WIN7), cost-61f (11 WIN7),
  cost-63e (8 WIN7), cost-64b (20 WIN7) on the second class-2 target's
  children; frontier 924 -> 974 across the session's receipts (95 WIN7-D10
  verdicts, 27 certificates verified).

## Status

11x11 empty board: UNKNOWN. Two-stone root {49,60}: UNKNOWN. S2 {59,60}:
UNKNOWN. class 2 / class 4 blockers: UNKNOWN. WIN7 certificates prove only
individual 7-stone roots within depth 10; REFUTED-D10 sweeps prove only the
absence of such receipts.
