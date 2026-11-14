# N11 class2 cost-69a raw batches 1–3: duplicate candidate audit (2026-11-14)

Source: commit `87099ca175efdfc4936e6433d59063a8ca313b9e`, three `class2-lane-cost69a-raw-batch{1,2,3}-20261114.jsonl` files under `research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/`.

## Independent aggregation

- Candidate records: **20** (4 + 8 + 8); separate `pilot_d6` control record: 1.
- **Distinct candidate bit indices: 17**, not 20. Bits **0, 1, 2** occur in both batch1 and batch2.
- The duplicated bits have identical `nodes`, `loss`, `capped`, `terminalStoneRange`, and `andclose` fields, but different wall times (`ms`). They are repeated measurements, not 3 additional covered candidates.
- Sum of all 20 candidate-record node counts: **86,460,390**; sum after deduplicating by bit: **75,270,843**. Difference: **11,189,547**. These are reported node visits, not unique search states.
- Among these 17 distinct bits, none reports `loss:true` or `capped:true`; this is **not** a game-theoretic verdict for the six-stone parent or the two-stone root.

## Consequence

The commit message's “20/69 candidates” counts records rather than distinct candidates. For coverage accounting, use **17/69 distinct bits** until additional records appear. Do not sum repeated candidate records into unique coverage, and do not count the pilot as a candidate.

This audit only checks raw-record consistency; it does not independently execute the search or validate a game certificate. Standard N11 empty-board and two-stone roots remain **UNKNOWN**.
