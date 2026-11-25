# 2026-11-14 class2-lane: cost-65g sweep — 9 WIN7-D10 (3 certificates verified, first certificate for the cost-61d cross-child duplicate root), frontier 974 -> 979

Long-term lane session 12, continuing directly from the cost-64b result on the
same lane (after-cost-64b frontier solved 974; commits `5f2de248` + `eac93109`).
Sweep target: the cost-65 child `00000000000000803202000000000004` of the
second class-2 target S5 `00000000000000803202000000000000`, named cost-65g
because the cost-65 band names are already occupied (cost-65 / -65b (sterile) /
-65c / -65d / -65e / -65f).

## Claim and candidate enumeration

- Claim pushed before any sweep batch (commit `e987ca50`):
  `class2-lane-cost65g-inflight-20261114.json`, 65 candidates bit-exact with
  the published edge cost 65 (independent `legal_candidates.py` Bareiss
  enumeration).
- **Per the cost-61e correction lesson**, the child's membership among the
  parent's remaining children (20 orbits / 1,418 after cost-64b; cheapest
  remaining band = the cost-65 triple, this child first) and its non-empty
  demand (c1=0, c2=2, c4=0) were re-verified from
  `class-frontier-top-candidates-s6-after-cost64b-20261114.csv` BEFORE the
  claim.
- Engine: the v16 runner, agreement-gated in cost-56a and the sweep engine for
  cost-58b / cost-60b / cost-61d / cost-61e / cost-61f / cost-63e / cost-64b.
  Pilot d6 control loss=false at exactly 3,402 nodes in all 9 batch
  invocations.

## Sweep result

**65/65 candidates: 9 WIN7-D10 + 56 REFUTED, 0 capped, 69,332,778 v16
nodes** (9 batches 8x8+1, raw JSONL pushed per batch, commit `ef8d6e20`;
terminal range [13,17] on every candidate).

- WIN7 bits: 0, 1, 15, 44, 52, 75, 86, 94, 105.
- Heaviest candidates: bit 0 (3,695,463), bit 77 (3,163,335, REFUTED), bit 105
  (3,132,696), bit 44 (3,056,671), bit 95 (2,639,694, REFUTED), bit 66
  (2,471,273, REFUTED).
- Determinism: bits 0, 77 and 105 re-solved fresh in a separate process,
  node-exact identical
  (`class2-lane-cost65g-v16-determinism-rerun-20261114.jsonl`, commit
  `ba8f69ef`).
- v15 cross-engine anchors (pilot 5,949 PASS): bits 0/105/44/94 all loss=true
  at 9,114,880 / 7,366,826 / 7,286,939 / 2,570,221 nodes and bit 77 loss=false
  at 6,422,042 nodes — verdicts identical to v16
  (`class2-lane-cost65g-v15-crosscheck-20261114.jsonl`, same commit).

## Three WIN7 certificates — all verification PASS

Three WIN7 candidates were extracted with
`class4_child1_cert_extractor_exact.ts` (repo-verbatim), blind, FBS=1<<20;
every per-move extraction ok and uncapped, fbt_drops=0 on all three; rows
sorted unique; verified with `verify_bit7_win7_cert.ts` (root-check + all
sub-roots + consumed/rows union).

| bit | root hex | rows | extraction nodes | mobility | sub-roots | union miss/extra | md5 |
|---:|---|---:|---:|---:|---:|---|---|
| 94 | `00000000400000803202000000000004` | 30,777 | 3,768,221 | 48 | 48/48 | 0/0 | `089406dd...` |
| 1 | `00000000000000803202000000000006` | 29,005 | 4,475,807 | 45 | 45/45 | 0/0 | `ad9894f2...` |
| 86 | `00000000004000803202000000000004` | 39,834 | 7,681,155 | 57 | 57/57 | 0/0 | `74fda987...` |

- All three landed byte-exact with full paged reads (commits `d96c9453` /
  `86ff4ea1` / `f9feffea`); remote md5 verified.
- **Bit-1 cross-child duplicate, resolved as a first publication**: the root
  `00000000000000803202000000000006` code-searched at exactly 2 hits before
  pushing — both are `win7_roots` array listings in the cost-61d sweep/inflight
  records (cost-61d proved the same 7-stone root WIN7-D10 from a different
  parent edge; the cost-61e bit-1 pattern recurring). No prior certificate
  file existed anywhere in the repo, so the bit-1 certificate pushed here is
  the FIRST published certificate for this root — recorded as
  duplicate_root_cross_child, not a duplicate certificate. The frontier
  recompute confirms its marginal coverage is new (6/2), not double counted.
- The other 8 WIN7 roots: GitHub code search 0 hits each.
- The remaining 6 WIN7-D10 bits (0, 15, 44, 52, 75, 105) stay warm
  certificate-rebuild candidates; bits 0/105/44 carry v15 loss=true
  cross-engine anchors.
- Terminal ranges within [13,17] on all three.

## Frontier recompute after cost-65g

`recompute_frontier_cost65g_20261114.py` (direct runpy extension of the
published cost-64b script): every staged control through after-cost-64b
reproduced exactly (asserted 974 / 6,873 / 541,401 / 5,143/405,124), the
completed cost-65g sweep record, claim (status completed) and receipts record
are asserted, the child's remaining-membership and demand (c1=0,c2=2,c4=0)
are re-derived from the frontier and asserted, then the three receipts are
added.

- cost-65g additions (covers / marginal / in-manifest): bit 94: 7/6/2,
  bit 1: 7/6/2, bit 86: 7/7/3 (net in-manifest +5).
- **after cost-65g: solved 979 · unique remaining 6,868 · sum 541,041 ·
  open 5,138 / 404,764.**
- Second class-2 target S5 `00000000000000803202000000000000`: 20 -> 18 orbits
  (1,418 -> 1,277), still the best coverable class-2 target. Best class-4
  unchanged (18 / 1,460).
- Records completed and pushed (commit `0297862c`: sweep record, receipts
  record, completed claim). Frontier recompute + script + rankings pushed in
  commit `c5bcedf9`, remote md5 verified. Two consecutive recompute runs
  byte-identical (JSON + both CSVs).

## Operational notes

- Next cheapest remaining children of the second class-2 target after
  cost-65g: the cost-65 band pair — `00000000000000803202000000001000`
  (c1=0,c2=2,c4=0), `00000000000000803202000000080000` (c1=0,c2=2,c4=2),
  then `00000000000000803202000020000000` (67, c1=0,c2=2,c4=0) (per
  `class-frontier-top-candidates-s6-after-cost65g-20261114.csv`; verify
  membership + demand again before claiming).
- Session-12 lane totals: cost-56a (1 WIN7), cost-58b (3 WIN7), cost-60b
  (25 WIN7), cost-61d (14 WIN7), cost-61e (13 WIN7), cost-61f (11 WIN7),
  cost-63e (8 WIN7), cost-64b (20 WIN7), cost-65g (9 WIN7) on the second
  class-2 target's children; frontier 924 -> 979 across the session's
  receipts (104 WIN7-D10 verdicts, 30 certificates verified).

## Status

11x11 empty board: UNKNOWN. Two-stone root {49,60}: UNKNOWN. S2 {59,60}:
UNKNOWN. class 2 / class 4 blockers: UNKNOWN. WIN7 certificates prove only
individual 7-stone roots within depth 10; REFUTED-D10 sweeps prove only the
absence of such receipts.
