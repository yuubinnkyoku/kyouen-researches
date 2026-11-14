# 2026-11-14 class2-lane: cost-61e sweep — 13 WIN7-D10 (3 certificates verified), frontier 951 -> 954, claim demand bookkeeping corrected

Long-term lane session 12, continuing directly from the cost-61d result on the
same lane (after-cost-61d frontier solved 951; commits `63e0dbe4` + `8d7a9e2a`).
Sweep target: the cost-61 child `00000000000000803202000040000000` of the
second class-2 target S5 `00000000000000803202000000000000`, named cost-61e
because the cost-61 band names are already occupied by the published cost-61 /
cost-61b / cost-61c / cost-61d sweeps.

## Claim and candidate enumeration

- Claim pushed before any sweep batch (commit `bd4ec1df`):
  `class2-lane-cost61e-inflight-20261114.json`, 61 candidates bit-exact with
  the published edge cost 61 (independent `legal_candidates.py` Bareiss
  enumeration).
- Engine: the v16 runner, agreement-gated in cost-56a and the sweep engine for
  cost-58b / cost-60b / cost-61d. Pilot d6 control loss=false at exactly 3,402
  nodes in all 8 batch invocations.

## Sweep result

**61/61 candidates: 13 WIN7-D10 + 48 REFUTED, 0 capped, 32,935,423 v16
nodes** (8 batches, raw JSONL pushed per batch, commit `9c969f05`; terminal
range [13,17] on every candidate).

- WIN7 bits: 1, 4, 17, 40, 74, 87, 89, 92, 102, 105, 109, 114, 120.
- Heaviest candidates: bit 102 (2,241,701), bit 3 (1,932,707, REFUTED), bit 4
  (1,594,068), bit 8 (1,496,203), bit 14 (1,392,905), bit 114 (1,230,688).
- Determinism: bits 102, 3 and 4 re-solved fresh in a separate process,
  node-exact identical
  (`class2-lane-cost61e-v16-determinism-rerun-20261114.jsonl`).
- v15 cross-engine anchors (pilot 5,949 PASS): bits 102/4/109 all loss=true
  at 5,705,537 / 4,993,271 / 702,145 nodes and bit 3 loss=false at 6,411,106
  nodes — verdicts identical to v16
  (`class2-lane-cost61e-v15-crosscheck-20261114.jsonl`).

## Three WIN7 certificates — all verification PASS

The three cheapest WIN7 candidates were extracted with
`class4_child1_cert_extractor_exact.ts` (repo-verbatim), blind, FBS=1<<20;
every per-move extraction ok and uncapped, fbt_drops=0 on all three; rows
sorted unique; verified with `verify_bit7_win7_cert.ts` (root-check + all
sub-roots + consumed/rows union); root hexes absent from all published
win7-certificates records (GitHub code search: 0 hits each).

| bit | root hex | rows | extraction nodes | mobility | sub-roots | union miss/extra | md5 |
|---:|---|---:|---:|---:|---:|---|---|
| 109 | `00002000000000803202000040000000` | 15,534 | 1,141,887 | 43 | 43/43 | 0/0 | `ada3f6a1...` |
| 17 | `00000000000000803202000040020000` | 22,590 | 2,901,988 | 47 | 47/47 | 0/0 | `25b81adb...` |
| 40 | `00000000000000803202010040000000` | 25,428 | 2,129,491 | 44 | 44/44 | 0/0 | `6cf359c9...` |

- All three landed byte-exact with full paged reads (commits `6bfdd1db` /
  `905936d3` / `df51253f`); remote md5 verified.
- **Duplicate root discovered**: WIN7 bit 1's root
  `00000000000000803202000040000002` is the identical 7-stone position as the
  published cost-61d bit-30 receipt (reached via a different child). The fresh
  extraction reproduced the published certificate bit-exact (md5
  `93bc0a6a...`, 23,348 rows); it is NOT re-pushed and the duplicate is
  recorded in the sweep and receipts records.
- The remaining 9 WIN7-D10 bits (4,74,87,89,92,102,105,114,120) stay warm
  certificate-rebuild candidates; bits 102/4 carry v15 loss=true
  cross-engine anchors.
- Terminal ranges within [13,17] on all three.

## CORRECTION: the claim's demand bookkeeping was wrong

Found during frontier integration: the claim described the S6 child
`00000000000000803202000040000000` as "the cheapest remaining unswept child"
of the second class-2 target with demand classes c1=0, c2=2, c4=0
"(after-cost61d frontier)". Neither part holds:

- The child was **already solved in the published after-cost-60b baseline**
  (its canon is among the covered positions of published receipts, including
  the cost-61d bit-30 cover); its open-class demand is empty in every frontier
  state since cost-60b, and it is not among the remaining children of the
  second class-2 target in any of those states (29 after cost-60b, 27 after
  cost-61d).
- The demand line was inherited from the cost-61d claim without
  re-verification.

The claim and sweep records were corrected in place with a transparent
`demand_classes_correction` note (commit `d2c2244b`); the correction is also
asserted and documented in the recompute controls. The sweep itself and all
certificates remain valid research: the 61 swept 7-stone positions were never
solved before, and the receipts add genuinely new coverage. Lesson recorded
for future claims: re-derive the child's demand from the current frontier
state and assert the child is actually among the parent's remaining children
before claiming.

## Frontier recompute after cost-61e

`recompute_frontier_cost61e_20261114.py` (direct runpy extension of the
published cost-61d script): every staged control through after-cost-61d
reproduced exactly (asserted 951 / 6,896 / 542,952 / 5,166/406,675), the
completed cost-61e sweep record, claim (status completed) and receipts record
are asserted, the duplicate bit-1 root is asserted already-covered in the
baseline, the (empty) demand of the child in the after-cost-61d state is
asserted with the claim correction documented, then the three receipts are
added.

- cost-61e additions (covers / marginal / in-manifest): bit 109: 7/0/0,
  bit 17: 7/5/1, bit 40: 7/6/2 (net in-manifest +3; one of bit 40's new
  manifest positions is a remaining child of the second class-2 target).
- **after cost-61e: solved 954 · unique remaining 6,893 · sum 542,756 ·
  open 5,163 / 406,479.**
- Second class-2 target S5 `00000000000000803202000000000000`: 27 -> 26 orbits
  (1,876 -> 1,809), still the best coverable class-2 target. Best class-4
  unchanged (18 / 1,460).
- Records completed and pushed (commit `709bcca1`: sweep record, receipts
  record, completed claim, v15-crosscheck and determinism JSONL; remote md5
  verified). Frontier recompute + script + rankings pushed in commit
  `d2c2244b`. Two consecutive recompute runs byte-identical (JSON + both
  CSVs).

## Operational notes

- Parallel-run push conflicts ("Reference cannot be updated" / "Update is
  not a fast forward" / a tree-creation timeout) occurred three times while
  the hourly parallel lane was pushing cost-65e batches; re-fetching main and
  re-pushing the identical content resolved all of them. Raw CDN staleness
  can show old bytes for updated files right after a push — verify against
  the commit's file listing / contents API in that case.
- Session-12 lane totals so far: cost-56a (1 WIN7), cost-58b (3 WIN7),
  cost-60b (25 WIN7), cost-61d (14 WIN7), cost-61e (13 WIN7) on the second
  class-2 target's children; frontier 924 -> 954 across the session's
  receipts.

## Status

11x11 empty board: UNKNOWN. Two-stone root {49,60}: UNKNOWN. S2 {59,60}:
UNKNOWN. class 2 / class 4 blockers: UNKNOWN. WIN7 certificates prove only
individual 7-stone roots within depth 10; REFUTED-D10 sweeps prove only the
absence of such receipts.
