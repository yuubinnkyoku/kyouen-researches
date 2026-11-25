# n11 class2-lane: merged frontier recompute after cost-69e v2 (70c + 60b-warm 17 + 71b = 23 receipts); chain-break repair; frontier 1023 → 1045; second target S5 down to 3 children / 222

Long-term lane session (2026-11-15 JST), continuing after the cost-71b sweep
(frontier 1026 published pre-v2) and the parallel lane's cost-69e v2 update
(baseline 1019 → 1023, all ten 69e receipts folded).

## Warm rebuild verification completed earlier in this session

- cost-60b band unverified_win7_bits 19 → 0: **17 warm certificates rebuilt
  and fully verified** (bits 40/77/26/74/44/28/8/88/95/106/87/22/100/108/
  32/114/43; bits 15/34 cross-child duplicates already in the manifest, not
  re-added), rows/sub-roots/union/md5/extraction-nodes asserted; remote md5
  byte-exact verified. The **parallel lane's independent BigInt audit passed
  17/17** on the same certificates — an unplanned two-implementation
  verification of the whole warm set.
- cost-70c / cost-71b control JSONL repair (commit 86bbe2ef): the v16
  determinism-rerun and v15 crosscheck JSONLs for 70c and 71b were found
  never pushed to main; both pairs were regenerated deterministically
  (node-exact against the published sweep records) and re-published.
- 71b chain byte-exact reproduction verified: the 71b script + sweep + raw
  batches + control JSONLs + certificates pulled from remote reproduce the
  published branch-B endpoint outputs byte-identically.

## Chain break discovered and repaired

The parallel lane's cost-69e v2 update folded all ten 69e receipts into the
recompute and moved the after-cost-69e endpoint 1019 → 1023 **without
rebasing the downstream scripts**: `recompute_frontier_cost70c_20261115.py`
(asserts 1019 → 1022), `recompute_frontier_cost60b_warm_20261115.py`
(1022 → 1040) and `recompute_frontier_cost71b_20261115.py` (1022 → 1026) all
runpy the 69e script and now **fail their baseline asserts against current
main** (verified locally: the 70c script raises AssertionError at line 47).
The historical endpoints 1022/1040/1026 were therefore no longer reproducible
from main as-is — a bookkeeping break, not a game-theoretic claim change.

The merged recompute
`recompute_frontier_merged_after69ev2_70c_60bwarm_71b_20261115.py` (commit
73f8b5d8) is the repair and the canonical chain head from the 69e v2
baseline onward:

- reproduces the 69e v2 baseline by runpy (assert 1023/6824/537833/5094/
  401556);
- re-derives the pre-v2 six-receipt state (1019) and from it **all three
  superseded endpoints exactly from raw records** — after-70c 1022,
  after-60b-warm 1040, after-71b 1026 — without runpy-ing the now-failing
  scripts, so the historical endpoints stay independently verifiable;
- asserts every input group from published records: the 70c sweep (70
  candidates, 13 WIN7 + 57 REFUTED, 100,935,666 nodes, raw batches
  re-summed, det 86/66 node-exact, v15 anchors 13/13) and receipts 94/20/23
  (rows/subs/union/md5/roots); the 60b sweep record (25 WIN7, unverified 19)
  and the 17 warm certificates; the 71b sweep (71 candidates, 9 WIN7 + 62
  REFUTED, 87,586,636 nodes, det 32/113 node-exact, v15 anchors 9/9) and
  receipts 109/21/105;
- re-adds all **23 receipts** in canonical chronological order (70c →
  60b-warm → 71b) with per-bit marginals re-derived from the growing union
  and compared with their published stage marginals. Duplicate-fold cases
  confirmed: 71b bits 109/21 marginal 0 (already covered by the warm set;
  bit-21 root = 60b-warm bit-22 root, md5-identical), 60b-warm bits 95/100
  marginal 0 (cross-child duplicates).
- final controls: sequential replay == baseline ∪ all 23 covers; every
  superseded endpoint's solved set ⊆ merged solved set.

Two runs **byte-identical** (md5 b1576b72… / cac000de… / fdd96e88…).

## Merged frontier

Stage frontiers (solved / unique remaining / sum cost / open s6 / open cost):

- baseline (69e v2): 1023 / 6824 / 537833 / 5094 / 401556
- after 70c: 1026 / 6821 / 537611 / 5091 / 401334
- after 60b-warm: 1044 / 6803 / 536212 / 5073 / 399935
- after 71b (merged): **1045 / 6802 / 536131 / 5072 / 399854**

The +22 over the 1023 baseline (23 receipts, one duplicate-fold) closes the
cost-70c child, the cost-60b child (closed mid-flight by the earlier warm
set), and the cost-71b child within one canonical recompute.

## Ranking effect / next targets

The second class-2 target S5 `00000000000000803202000000000000` drops to
**3 remaining S6 children / 222 edge cost**:

- `00000000000000803202000000000200` (cost 72) — parallel lane sweeping now
  (raw batches 1–9 + audit published: 2 WIN7-D10 bits 52/111, bit-111
  certificate published, sweep record not yet completed → **not folded
  here**; certificates without records are not receipts)
- `00000000000000803202000000000008` (cost 75)
- `00000000000000803202000000004000` (cost 75)

The audit-blocked S5 `00000000000000809082000000000000` holds at 10/698.
Best class-4 unchanged: `00000000020000003800000080000000` at 18/1,460.
The target remains receipt-coverable — no uncoverability change.

Outstanding warm-rebuild candidates without records (not folded): cost-61d
bit-22 (= cost-71b bit-1 root), cost-71b remaining WIN7 bits
1/14/32/74/94/117, and other unverified WIN7 bits of earlier bands.

## Status

- 11×11 empty board, two-stone root {49,60}, S2 {59,60}, class 2, class 4:
  **UNKNOWN**. WIN7 certificates prove a win within depth 10 from the
  individual 7-stone roots only; REFUTED-D10 sweeps prove only the absence
  of such a win in that subtree; this recompute is bookkeeping over
  published receipts and proves no new game outcome.
