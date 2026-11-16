# class2-lane: head-chain linearity audit 1398 -> 1419 (2026-11-16)

## What was done

- Re-read the published fold recompute records covering branch D (cost-62a / 58c / 63i / 63j / 65m / 67d), the fork reconciliation (63h cover vs 70g fold on branch D head 1398), and the subsequent chain (75e / 60c / 65j).
- Arithmetic delta checks at every step (solved counts, unique_remaining_s6, sum_remaining_cost, needed, cost_needed) plus demand-histogram sum checks.
- No new sweeps, no verdicts: bookkeeping chain verification only.

## Results

- The chain is fully linear and arithmetically consistent at every step: 1318 -> 62a -> 1326 -> 58c -> 1360 -> 63i -> 1367 -> 63j -> 1394 -> 65m -> 1396 -> 67d -> **1398 (branch D head)**; fork: 70g-on-D = 1403 (superseded) vs 63h-cover-on-D = 1400 (canonical), reconciled by set-equality + reverse-order replay at **1405**; then 75e -> **1407** -> 60c -> **1410** -> 65j -> **1419 (current head)**.
- Every in-manifest marginal matches its head delta (e.g. 63j: 1367+27=1394; 65j: 1410+9=1419, 6438-9=6429, 509109-635=508474); demand histograms sum exactly to 'needed' at every checked head.
- Citation hygiene finding (documentation-level): the cost-63j/65m/67d baseline_main strings cite the 58c recompute filename with cumulative head numbers (1367 / 1394) that do not match that file's own frontier_after (1360), and 63j/67d quote the same git blob sha (db0288f1) for two different claimed heads. The quoted numbers match the intended cumulative baselines and all delta checks pass, so fold arithmetic is unaffected; the citations should simply have named the actual upstream fold records.
- 13 of the 17 folded cost-65j receipts (the cost-65f set) have no published certificates; they are folded on blob-pinned raw sweep records (the 65j record itself notes certificate extraction as optional follow-up).

## Observations for the parallel lane

- Current canonical head is **1419/174/6429/508474/4702/372388**; all inflight claims must re-base onto it: cost-76c still references 1407, and the cost-76d / 77e lanes pinned 1405.
- P (00000000000000403800000008000000, 24 rows / 1704) and Q (00000000000000821082000000000000, 18 rows / 1238) are unchanged at 1419 - no fold in the 1405->1419 chain lists their S5s among affected parents. The Q/P pre-sweep orbit-dedup measurements published earlier today (be91d324, 665cc6e1) therefore still apply at the current head.
- Future folds should cite the specific upstream fold record rather than reusing the 58c filename for cumulative heads; no retroactive rewrite is needed.

## Status

- 11x11 empty board, S2 {59,60}, class1/class2/class4 roots: **UNKNOWN** (unchanged).
- head 1419 counts are manifest coverage bookkeeping only.

Output: `research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class2-lane-head-chain-linearity-audit-20261116.json`
