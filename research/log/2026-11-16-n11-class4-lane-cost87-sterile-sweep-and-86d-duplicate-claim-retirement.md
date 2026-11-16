# 2026-11-16 n11 class4-lane cost-87 sweep: sterile - the best class-4 blocker S5 is now fully swept (18/18 rows REFUTED-D10); duplicate 2026-11-15 cost-86d claim retired

Long-term class4 frontier lane, continued (cost-87 claim resumed after the 2026-11-14/15 execution-environment failures, recorded as experimental facts). S5 parent `00000000020000003800000080000000` (the best class-4 blocker-candidate S5, 18 rows / 1460 at head 1407), S6 child `00000000020000003800000080000004` (cost 87, demand c1=0,c2=0,c4=3, stones [2,31,59,60,61,89]).

## Sweep

- Candidates: 87 legal seventh moves re-enumerated independently via `legal_candidates.py` (Bareiss 4x4, script blob sha 8e97082c42838c7a4a4b6d2dd235276c8d43ab9a), bit-exact with the claim candidate_bits and the published head-1407 top-candidates CSV row (edge cost 87).
- Engine: v16 (`class4_child1_runner_v16.ts`, git blob sha 0a4a86f6828dc010c89ff17596054336a6b6091f), depth 10, cap 1e9, close-first AND (andclose=1), per-candidate fresh process (Node v22 native).
- Pilot d6 control: `loss=false` at exactly 3,402 nodes in all 87 per-candidate invocations (one control line per candidate in the raw batches).
- Demand re-verified at the head-1407 state before running: D4 one-stone deletions give exactly three open class-4 parents - stone 2 -> the blocker S5 (18/1460), stone 31 -> `00000000000000801002000000480000` (89/7577), stone 89 -> `00000000000000003800000000800100` (90/7775); stones 59/60/61 deletions are closed rows.
- Result: **87 REFUTED-D10, 0 WIN7-D10, 0 capped, 142,614,947 candidate nodes**, terminal stone range [13,17] on all 87 candidates, andclose=true throughout.
- Determinism control: batch 5 (bits 43,44,45,46,48,49,50,51) re-run in a separate process - verdicts/nodes/capped/terminal node-exact identical.
- v15 cross-engine control: pilot 5,949 loss=false; the 3 heaviest REFUTED anchors (bits 6 / 28 / 110, 11,064,041 / 7,015,253 / 6,612,283 v16 nodes) re-solved with the v15 engine (14,292,036 / 11,734,720 / 5,004,960 v15 nodes) - all loss=false agreement.
- Independent audit: `audit_cost87_raw_sweep_20261116.py` (stdlib-only re-derivation of the aggregate, batch bits, demand, parent rows against the head-1407 CSVs, plus the duplicate-claim check below) - all checks pass; audit JSON byte-identical across two runs.

## Blocker S5 fully swept

With this sweep all 18 open S6 rows of the best class-4 blocker-candidate S5 `00000000020000003800000080000000` are REFUTED-D10 (73f, 74f, 74c, 75, 79, 79b, 80, 80c, 81, 82, 82b, 84, 86a, 86b, 86c, 86d, 86e, 87). **The S5 is unclosable by depth-10 WIN7 receipts**: no 7-stone root extending any of its rows admits a first-player win within depth 10, so its c4 demand can only be met through cross-child certificate reuse or evidence beyond depth 10. This is a negative structural fact only - NOT a LOSS proof for the S5, its rows, or any parent; the S5 remains an open row of the class-4 frontier at head 1407. No fold material is produced; the canonical head is unchanged (the parallel cost-60c WIN7-D10 receipt fold and the cost-76d/77e folds are separate lanes and do not touch this child or its parents).

Next class-4 candidates by the head-1407 ranking: `000000000000003800002000800000` (60 rows / 4216), `00000000020000003800000000080000` (61 rows / 4351), `00000000000000801802000000080000` (64 rows / 4390).

## Duplicate 2026-11-15 cost-86d claim retired

The 2026-11-15 claim `class4-lane-cost86d-inflight-20261115.json` (child `00000000020000003800100080000000`) was a **duplicate**: the child had already been swept and published STERILE on 2026-11-14 (`class4-lane-cost86d-sweep-20261114.json`, 86/86 REFUTED-D10, 315,578,134 nodes). Child hex, 86-candidate list and edge cost are bit-exact identical between the two files (verified programmatically; the audit script re-enumerates the 86d child independently). The claim's no_prior_sweep_note was wrong - the claiming session scanned only inflight/claim files and missed the published sweep JSON. No raw batches ran under the duplicate claim, so no computation was wasted and no evidence conflict exists. The claim is retired to status `superseded_duplicate` in this push.

Coordination lesson for all lanes: before claiming a child, grep the output directory for the child hex across ALL schemas (sweep JSONs and raw batches included), not only the inflight/claim files.

## Records

Raw batches: `../experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class4-lane-cost87-raw-batch1..11-20261116.jsonl`. Controls: `class4-lane-cost87-v16-determinism-rerun-20261116.jsonl`, `class4-lane-cost87-v15-crosscheck-20261116.jsonl`. Claim: `class4-lane-cost87-inflight-20261114.json` (status updated to completed). Audit: `class4-lane-cost87-raw-sweep-audit-20261116.json`, script `../scripts/audit_cost87_raw_sweep_20261116.py`. Knowledge: K0783 appended in the same push.

## Status

11x11 empty board, two-stone roots {49,60}/{59,60}, S2 {59,60}, class 1, class 2, class 4: **UNKNOWN**. REFUTED-D10 is only the negation of a winner win within depth 10 from the 7-stone root; it is NOT a statement about deeper play, the S5/S6 orbits, or the empty board.
