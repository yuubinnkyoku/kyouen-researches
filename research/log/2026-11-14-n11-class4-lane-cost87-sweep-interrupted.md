# 2026-11-14 n11 class4-lane cost-87 sweep: in flight, interrupted by execution-environment outage

Long-term lane session 11, continued. After completing the cost-86 band (86a-86e all sterile; 86e = 23rd sterile, record/log pushed and md5-verified at commit 2b64343), this session claimed the cost-87 child of the class-4 target `00000000020000003800000080000000`: S6 child `00000000020000003800000080000004` (cost 87, demand c1=0,c2=0,c4=3).

## Progress before the outage

- Claim: `class4-lane-cost87-inflight-20261114.json` pushed (status: in flight, 87 legal candidates via legal_candidates.py Bareiss enumeration, bit-exact with the published edge cost 87).
- Raw batch 1 (bits 0,3,4,5,6,10,11) and raw batch 2 (bits 12,14,15,16,17,18,19) completed and pushed: 14/14 REFUTED-D10, pilot d6 5,949 nodes in both invocations, 0 capped.
- Raw batch 3 (bits 21,25,26,27,28,29,30) completed locally with all 7 candidate lines present (last line: bit 30 REFUTED-D10, 2,738,352 nodes) but **could not be pushed**: the execution environment went unavailable (repeated "temporarily unavailable" failures on every bash/file operation, retried ~15 times over several minutes). The raw file is therefore trapped in a non-durable local state and is NOT evidence; batch 3 must be re-run for a durable raw record.

## Resume instructions for the next run

1. Pull latest main; confirm `class4-lane-cost87-inflight-20261114.json` is still status in-flight and owned by this lane (the parallel lane holds cost-84).
2. Re-run batch 3 (bits 21,25,26,27,28,29,30) and continue batches 4-13 (7 bits each, last batch 3 bits) with the identical v15 protocol (close-first AND at depth>=8, cap 1e9, depth 10), pushing each batch's raw JSONL immediately.
3. On completion: determinism rerun of the heaviest 3 candidates, record `class4-lane-cost87-sweep-20261114.json` (same schema as the cost-86 records), claim status update, log entry. If any WIN7 appears, run the certificate extractor + independent verifier flow before pushing any verdict.

Batches 1-2 and their md5s are durable on main (commit 8d890d2). Node counts observed so far are consistent with the cost-86 band's per-candidate cost profile (1M-20M nodes).

## Status

Cost-87 child: unsolved (in flight, 14/87 candidates REFUTED-D10 durably). 11x11 empty root, two-stone root {49,60}, S2 {59,60}, class 2, class 4: **UNKNOWN**.
