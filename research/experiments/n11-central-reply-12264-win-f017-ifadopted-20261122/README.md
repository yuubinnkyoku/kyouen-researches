# n11 f017 WIN row IF-ADOPTED analysis (2026-11-22)

IF-ADOPTED scenario analysis for the batch-5 WIN-HALT key **f017**
(s5_index 415095, key `[1188950301625810945, 70368744177666]`, legal 82,
result 1 WIN, 3,522,635 nodes, 2-pass node-exact; see
`../n11-centralreply-closure-class12264-batch5-20261122/`, declaration Part F).
The lane does NOT consume the verdict (pre-registered rule: WIN rows go to the
verdict-scrutiny owner, as b018, d002, e002). This experiment answers,
machine-verified and fail-closed: **what would change if all eighteen
batch-5 probed rows (f001-f018: 17 exact LOSS + f017 WIN) were adopted**.

## Construction

- if-adopted increment: 18 rows = all batch-5 probed keys
  (`output/increment-batch5-probed-18rows-IFADOPTED-20261122.cache`); keys,
  verdicts and nodes byte-taken from the published batch-5 raw replay rows
  (f017 WIN 3,522,635 nodes; the other 17 LOSS, nodes in the raws).
- fail-closed union merge with the canonical 5,924-row merged cache (same
  published merger, selftest PASS, conflicts 0):
  `output/merged-exact-s5-chain-plus-closure-increment-PLUS-BATCH5PROBED-IFADOPTED-20261122.cache`,
  5,942 unique rows, WIN 159 / LOSS 5,783, sha256
  `f7c7c960c7387161f8f335cf3f22fdecb90380f301d810fdff80d3bee7416c98`
  (published as its own single-file commit; audit
  `output/merge-audit-ifadopted.json`).
- `scripts/refresh_19root_frontier.py`: byte-copy of the published re-audit
  script with ONLY the merged-cache path and sha pins changed (2 lines); run
  twice, all four output files byte-identical (determinism 4/4); all other
  pins unchanged; baseline control holds (root first=27: 119/119).
- the full 65,191-row probe-worklist.csv is regenerated on any rerun;
  mirrored in the lane kit, not republished here (3.7 MB).

## If-adopted deltas vs the canonical re-audit (machine-verified)

- **class flips: exactly 3 S4 classes flip to excluded_now (26 vs 23), unknown
  34,503 -> 34,500**: the three classes that hold s5 415095 as a cost child,
  machine-identified from the frozen dependency graph:
  `12264` (mask `[1152921504606848033, 0]`), `12327`
  (mask `[1188950301625810945, 2]`), `14776`
  (mask `[1152921504606846977, 70368744177666]`).
- **update8 consequence: 6 group records flip to win-hit-blocked**, all via
  s4 class 12264 (a frozen-plan selected class): root first=0 (thirds 5 and 10
  paired with fourths 10/5, thirds 55 and 110 paired with 110/55) and root
  first=5 (thirds 0 and 10 paired with fourths 10/0).
  resolved_among_baseline_requirement 21 -> 39 (all 18 batch-5 keys lie inside
  the 31,859-key baseline requirement); remaining_now 31,838 -> 31,787
  (root 0: 11,726 -> 11,522, root 5: 10,699 -> 10,597, all others unchanged);
  groups_free_now 122 unchanged; worklist 65,213 -> 65,191.
- **free_now unchanged at 33, board verification 33/33, rejected 0**: the
  23963 closure and every achieved coverage are UNAFFECTED. Per-root
  free-third coverage unchanged on all 19 roots.
- **joint greedy INCREASES 35,617 -> 36,989** (roots 0/5 lose their cheap
  option and re-plan to higher-cost classes; per-root greedy: root 0
  2,785 -> 2,829, root 5 2,974 -> 2,956, root 38 3,066 -> 2,922, root 49
  2,893 -> 2,896): adopting the WIN row makes the joint 19-root plan MORE
  expensive, the first measured instance of an adoption raising the greedy
  requirement.

## Verdict for the scrutiny owner

Adopting the f017 WIN row (with the 17 batch-5 LOSS rows) would:
(a) kill the all-LOSS closure route of class 12264 formally, (b)
additionally exclude classes 12327 and 14776 from any all-LOSS closure route,
(c) block 6 update8 groups on roots 0 and 5 as win-hit, (d) resolve 18 keys
inside the frozen baseline requirement (largest single adoption delta so
far), and (e) raise the joint greedy requirement by 1,372 while leaving all
achieved free classes (33), coverage and the 23963 closure untouched. Nothing
here adopts any row: analysis only; all batch-5 verdicts (17 LOSS + 1 WIN)
remain unconsumed on main, and the canonical refresh pins remain on the
5,924-row cache.

The standard 11x11 empty board, the 19 central-reply roots (including 0 and 5)
and all classes remain UNKNOWN. Node counts are not verdicts; only the
2-pass rows cited above carry their cited results.
