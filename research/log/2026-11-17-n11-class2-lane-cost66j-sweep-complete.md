# 2026-11-17 n11 class2-lane: cost66j fresh 66-bit sweep complete (9 WIN7-D10 + 57 REFUTED-D10, 0 capped)

## Summary

The head-1472 presweep census v3 (blob `3ee5703c`) selected the next
target of the primary pure class-2 family:
S6 child `00000000000000c09002000000001000` (parent
`00000000000000403800000008000000`, cost 66, demand c2=2, stones
[12, 49, 60, 63, 70, 71]). After publishing the preregistered claim v1
(blob `68d8f8f2`), the full 66-bit fresh v17 sweep ran to completion:

* **9 WIN7-D10 bits**: [7, 9, 30, 66, 78, 79, 92, 96, 114]
* **57 REFUTED-D10** bits, **0 capped**
* candidate nodes 65,981,633 (66,020,133 node lines including 9 pilots)
* terminal stone range [13, 17] on every line, andclose=1, depth 10,
  cap 1e9, engine v17 (blob `c132cc6425eee3feaeef1d697dd74f968cfedb59`)
* wall time ~2 minutes, two background streams (2 concurrent node
  processes; nproc=2, cgroup quota 1 CPU)

## Controls (all passed, all published)

1. **Pilots**: 9/9 batches, pilot d6 exactly {loss=false, nodes=3402}.
2. **Confirmation bits 20/97**: both REFUTED-D10, as preregistered.
   Bit 20 = cost-64h orbit transfer (64h bit 108): cross-engine canon
   agreement, engine verdict agrees with the v16-era 64h map. Bit 97 =
   v1 harvest transfer, confirmed fresh. The standalone pre-batch bit-20
   test (518,569 nodes) matches the batch-9 line exactly.
3. **Determinism**: batch 5 (heaviest, 14.6M nodes, contains WIN bits
   66/78/79) and batch 8 (contains WIN bit 114) re-run field-identical
   on all non-ms fields.
4. **v15 cross-engine** (blob `8744fc65b6b7...`): pilot exactly 5949,
   all 9 WIN bits loss=true (9/9), 0 capped.
5. **Independent stdlib-only audit**
   (`audit_cost66j_raw_batches_20261117.py` ->
   `class2-lane-cost66j-raw-audit-20261117.json`): legal set 66/66 equal
   to the claim, bit coverage exact, canon recompute 66/66 matches the
   head-1452 census v1 bit table, transfer canons 2/2 match the claim,
   internal canon collisions 0, **cross-source conflict scan vs the
   64h/76c/66i verdict maps: 0 conflicts**, and no 66j WIN canon is
   already folded in the landed 64h receipts.

## Interpretation guard

The sweep proves WIN7-within-depth-10 for the individual 7-stone roots
of this child only; REFUTED-D10 is not a LOSS proof of any position. No
manifest row is closed by the sweep. Certificate extraction for the 9
WIN roots is the next step; the receipt fold of this row must wait
behind the pending cost-76c fold (parallel lane, bit 61 certificate in
flight) and the cost-66i receipt fold.

**The 11x11 empty board remains UNKNOWN. The two-stone roots {49,60}
and {59,60}, S2 {59,60} and classes 1/2/4 all remain UNKNOWN.**

## Files pushed

* `output/class2-lane-cost66j-inflight-20261117.json` (claim v2,
  sweep-complete)
* `output/class2-lane-cost66j-raw-batch{1..9}-20261117.jsonl`
* `output/class2-lane-cost66j-det-batch{5,8}-20261117.jsonl`
* `output/class2-lane-cost66j-v15-crosscheck-20261117.jsonl`
* `output/class2-lane-cost66j-raw-audit-20261117.json`
* `scripts/audit_cost66j_raw_batches_20261117.py`
