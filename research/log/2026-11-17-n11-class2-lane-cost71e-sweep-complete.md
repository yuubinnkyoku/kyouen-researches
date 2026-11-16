# 2026-11-17 n11 class2-lane: cost71e fresh 71-bit sweep complete (13 WIN7-D10 + 58 REFUTED-D10, 0 capped)

## Summary

The head-1472 presweep census v5 (blob `ea85c023`, commit `723e8c2d`)
selected the next target of the primary pure class-2 family:
S6 child `00000000000000c09002000000002000` (parent
`00000000000000403800000008000000`, cost 71, demand c2=2/c4=2, stones
[13, 49, 60, 63, 70, 71]). After publishing the preregistered claim v1
(blob `f6439474`), the full 71-bit fresh v17 sweep ran to completion
(8 sweep batches + 1 confirmation batch):

* **13 WIN7-D10 bits**: [3, 4, 8, 41, 54, 58, 76, 79, 94, 96, 100,
  116, 119] (per-bit nodes recorded in the claim v2 and the raw
  batches; heaviest WIN bit 8 at 2,675,348 nodes)
* **58 REFUTED-D10** bits, **0 capped**
* candidate nodes 88,919,559 (88,950,177 node lines including 9 pilots)
* terminal stone range [13, 17] on every line, andclose=1, depth 10,
  cap 1e9, engine v17 (blob `c132cc6425eee3feaeef1d697dd74f968cfedb59`)

## Controls (all passed, all published)

1. **Pilots**: 9/9 batches, pilot d6 exactly {loss=false, nodes=3402}.
2. **Confirmation bits 20/67/97**: all three REFUTED-D10, exactly as
   preregistered by the census v5 overlay. Bit 20 = cost64h bit 97
   transfer (104,475 nodes), bit 67 = cost66i bit 107 transfer
   (269,982 nodes), bit 97 = pre-64h harvest transfer via cost64d bit
   97 canon equivalence (92,932 nodes): fresh verdicts agree with all
   cross-source records.
3. **Determinism**: batch 1 (contains WIN bits 3/4/8) and batch 6
   (heaviest batch, bit 88 at 9,928,319 nodes) re-run field-identical
   on every non-ms field.
4. **v15 cross-engine** (blob `8744fc65b6b7...`): pilot exactly 5949,
   all 13 WIN bits loss=true (13/13), 0 capped.
5. **Independent stdlib-only audit**
   (`audit_cost71e_raw_batches_20261117.py` ->
   `class2-lane-cost71e-raw-sweep-audit-20261117.json`, blob
   `9f56bdb7`): recomputed legal set 71/71 equals the raw bit records,
   pilot/andclose/terminal-stone checks 9/9, 13/13 WIN agreement,
   v15 node counts recorded, audit JSON byte-identical across the two
   repo/output and cost71/ layouts.

## Erratum: claim v1 legal_candidates field (corrected in claim v2)

The claim v1 (blob `f6439474`) carried a defective `legal_candidates`
field: it contained the 78-bit candidate list of the cost78a child
(`00000000000000809102000000400000`), a template carry-over in the
claim generator. Unaffected: `candidate_count` (71),
`engine_candidate_bits` (68 open + 3 confirmation), the transfers,
and every executed bit - the raw sweep bits equal the freshly
recomputed legal candidates of the cost71e child, and the published
stdlib audit recomputes `legal_candidates` itself and passed all
checks. Claim v2 (blob `3299f80f`) replaces the field with the
recomputed 71-bit list and records the erratum in
`erratum_v1_legal_candidates`. A systemic re-verification of all 34
published inflight claims that carry a `legal_candidates` field found
0 further mismatches (the 14 older claims predate the field).

## Interpretation guard

The sweep proves WIN7-within-depth-10 for the individual 7-stone roots
of this child only; REFUTED-D10 is not a LOSS proof of any position.
No manifest row is closed by the sweep. Certificate extraction for the
13 WIN roots is the next step (driver duplicated from cert_driver69j
with root defenses via legal_candidates, blind re-extraction, manifest
publication); the receipt fold of this row must wait behind the
pending cost-76c, cost-66i, cost-66j and cost-69j folds, which are
managed by their own lanes.

**The 11x11 empty board remains UNKNOWN. The two-stone roots {49,60}
and {59,60}, S2 {59,60} and classes 1/2/4 all remain UNKNOWN.**

## Files pushed

* `output/class2-lane-cost71e-inflight-20261117.json` (claim v2,
  sweep-complete + erratum; `update_claim71e_v2_20261117.py`)
* `output/class2-lane-cost71e-raw-batch{1..9}-20261117.jsonl`
* `output/class2-lane-cost71e-det-batch{1,6}-20261117.jsonl`
* `output/class2-lane-cost71e-v15-crosscheck-{a,b,c}-20261117.jsonl`
* `output/class2-lane-cost71e-raw-sweep-audit-20261117.json`
* `scripts/audit_cost71e_raw_batches_20261117.py`
* `scripts/update_claim71e_v2_20261117.py`
