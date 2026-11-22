# n11 e002 WIN row IF-ADOPTED analysis (2026-11-22)

IF-ADOPTED scenario analysis for the batch-4 WIN-HALT key **e002**
(s5_index 183566, key `[1153765929805414400, 16]`, legal 79, result 1 WIN,
14,112,632 nodes, 2-pass node-exact; see
`../n11-centralreply-closure-class16371-batch4-20261122/`, declaration Part E).
The lane does NOT consume the verdict (pre-registered rule: WIN rows go to the
verdict-scrutiny owner, as b018 and d002). This experiment answers,
machine-verified and fail-closed: **what would change if the batch-4 probed
rows (e001 exact LOSS + e002 WIN) were adopted**.

## Construction

- if-adopted increment: 2 rows = the two batch-4 probed keys
  (`output/increment-e001loss-plus-e002win-IFADOPTED-20261122.cache`):
  e001 LOSS 882,800 nodes; e002 WIN 14,112,632 nodes; keys/verdicts/nodes
  byte-taken from the published batch-4 raw replay rows.
- fail-closed union merge with the canonical 5,924-row merged cache (same
  published merger, selftest PASS, conflicts 0):
  `output/merged-exact-s5-chain-plus-closure-increment-PLUS-E002WIN-IFADOPTED-20261122.cache`,
  5,926 unique rows, WIN 159 / LOSS 5,767, sha256
  `cd3ad8d7074958776cd1580b1f33372ff9047fb92d8306f5ba26d780edc1ad2b`
  (published as its own single-file commit; audit
  `output/merge-audit-ifadopted.json`).
- `scripts/refresh_19root_frontier.py`: byte-copy of the published re-audit
  script with ONLY the merged-cache path and sha pins changed (2 lines); run
  twice, all four output files byte-identical (determinism 4/4); all other
  pins unchanged; baseline control holds (root first=27: 119/119).
- the full 65,211-row probe-worklist.csv is regenerated on any rerun; mirrored
  in the lane kit, not republished here (3.7 MB).

## If-adopted deltas vs the canonical re-audit (machine-verified)

- **class flips: exactly 4 S4 classes flip to excluded_now (27 vs 23), unknown
  34,503 -> 34,499**: the four classes that hold s5 183566 as a cost child,
  machine-identified from the frozen dependency graph:
  `4864` (mask `[1153765929805414400, 0]`), `4903`
  (mask `[1153484454828703744, 16]`), `5613`
  (mask `[1729663732155416576, 0]`), `16371`
  (mask `[1153202979851993088, 16]`).
- **update8 consequence: NONE.** win_hit_groups stays empty and remaining_now
  stays 31,838 (resolved_among_baseline_requirement 21 unchanged): unlike
  class 20421 (d002 analysis), class 16371 is not a selected class of the
  frozen update8 plan, and neither e001 nor e002 lies inside the 31,859-key
  baseline requirement.
- **free_now unchanged at 33, board verification 33/33, rejected 0**: the
  23963 closure and every achieved coverage are UNAFFECTED. Per-root
  free-third coverage unchanged on all 19 roots; joint greedy 35,617 ->
  35,616; per-root greedy root 26: 5,203 -> 5,202, root 48: 2,822 -> 2,820.
- worklist 65,213 -> 65,211 slots (exactly the 2 resolved s5 keys leave; no
  pair is added). closure-classes table: class 16371 drops to unknown_now 48
  but remains listed (rank 4) with a WIN cost child, joining 16757 (b018) and
  20421 (d002) in the refuted-conditional pool pending scrutiny.

## Verdict for the scrutiny owner

Adopting the e002 WIN row (with the e001 LOSS row) would: (a) kill the
all-LOSS closure route of class 16371 formally, (b) additionally exclude
classes 4864, 4903 and 5613 from any all-LOSS closure route, and (c) not
disturb any update8 record, any achieved free class (33), any achieved
coverage, or the 23963 closure. Nothing here adopts the rows: analysis only;
all batch-4 verdicts (1 LOSS + 1 WIN) remain unconsumed on main, and the
canonical refresh pins remain on the 5,924-row cache.

The standard 11x11 empty board, the 19 central-reply roots and all classes
remain UNKNOWN. Node counts are not verdicts; only the 2-pass rows cited
above carry their cited results.
