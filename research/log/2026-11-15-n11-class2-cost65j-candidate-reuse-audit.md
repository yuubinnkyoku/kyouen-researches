# n11 class2 cost65j: one of 65 S7 candidates is already covered by a WIN7 certificate

2026-11-15 JST. This is a reuse audit only; no new search was launched and no S6 frontier count was changed.

## Candidate set

The published cost65j claim targets S5 `00000000000000809102000000000000` and its S6 child `00000000000000809102000080000000`, with 65 legal seventh moves. An independent exact 4x4 determinant enumeration over all 121 cells reproduced all 65 candidate bits exactly. The 65 resulting seven-stone roots occupy 65 distinct D4 orbits.

## Reused certificate

The candidate at bit 79 is

`00000000000080809102000080000000`.

It is the D4 image under transform 5, `(x,y) -> (x,10-y)`, of the already-published WIN7 certificate root

`00000002000000809102000800000000`.

The transform sends source added bit 35 to target bit 79, and sends source parent `00000002000000809102000000000000` exactly to the cost65j S6 child. Thus this is not merely a seven-stone orbit match: the parent-child lift also matches exactly.

The two certificate parts were fetched from main and checked by Git blob SHA:

- part 1: 707,361 bytes, `a33afbaba4c99511872108223b70c1f15e786db1`
- part 2: 707,359 bytes, `af1545ee1ebd70ab7f48274732678c15c286fa12`

The joined certificate was independently replayed using BigInt exact geometry, without the search engine, verdict cache, or repository verifier:

| Check | Result |
|---|---:|
| Root stones / safety | 7 / PASS |
| Root legal replies | 49 |
| Strategy rows | 39,159 |
| Subroots verified | 49 / 49 |
| Visited states across subroots | 88,265 |
| Terminal visits | 13,150 |
| Opponent reply edges | 82,167 |
| Terminal stone range | 13–17 |
| Consumed strategy rows | 39,159 |
| Missing / extra rows | 0 / 0 |

## Effect and boundary

At least one of the 65 cost65j candidate roots is already certified. The number requiring new WIN7 evidence therefore falls from 65 to at most 64 before accounting for any other newly published receipts. The concurrent batch2 lane is still publishing certificates, so this is not claimed to be the final reuse count.

This does **not** close the six-stone parent. A single WIN7 child only certifies that child; all legal seven-stone children are needed to classify the S6 parent. No S6 frontier count was changed, and the cost65j sweep is not marked complete.

Standard 11×11 empty board, two-stone roots `{49,60}` and `{59,60}`, S2 `{59,60}`, and class2/class4 remain **UNKNOWN**.

Reproduction: `node research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/scripts/audit_cost65j_candidate_reuse_20261115.mjs`.

Machine-readable result: [class2-lane-cost65j-candidate-reuse-audit-20261115.json](../experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class2-lane-cost65j-candidate-reuse-audit-20261115.json).
Verifier: [audit_cost65j_candidate_reuse_20261115.mjs](../experiments/n11-s2-5960-ms5-s7-reuse-20261113/scripts/audit_cost65j_candidate_reuse_20261115.mjs).
