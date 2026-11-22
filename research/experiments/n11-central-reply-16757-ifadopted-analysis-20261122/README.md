# n11 b018 WIN row IF-ADOPTED analysis (2026-11-22)

IF-ADOPTED scenario analysis for the batch-1 WIN-HALT key **b018**
(s5_index 528497, key `[1153204079095189504, 65536]`, legal 60, result 1 WIN,
3,549,602 nodes, 2-pass node-exact; see
`../n11-centralreply-closure-class16757-batch-20261122/`). The lane does NOT
consume the verdict (pre-registered rule: WIN rows go to the verdict-scrutiny
owner). This experiment answers, machine-verified and fail-closed: **what would
change if the row were adopted**.

## Construction

- if-adopted increment: canonical 67-row increment + the single b018 WIN row =
  68 rows (`../n11-central-reply-23963-closure-reaudit-20261122/output/increment-67loss-plus-b018win-IFADOPTED-20261122.cache`)
- fail-closed union merge with the 5,857-row base cache (same published
  merger, sha-gated: `output/merge-audit-ifadopted.json`, 5,925 unique rows,
  WIN 159 / LOSS 5,766, conflicts 0)
- merged if-adopted cache
  `../n11-central-reply-23963-closure-reaudit-20261122/output/merged-exact-s5-chain-plus-closure-increment-PLUS-B018WIN-IFADOPTED-20261122.cache`
  (sha256 `062ff64d1b8eac70c21d469c35ce16aaea8f4e6f4ff00cb1877cacaef4bdd76f`,
  published as its own single-file commit)
- `scripts/refresh_19root_frontier.py`: byte-copy of the re-audit script with
  only the cache pin changed; run twice, byte-identical (determinism), all
  other pins unchanged; baseline control holds (root first=27: 119/119)

## If-adopted deltas vs the canonical re-audit (machine-verified)

- **class flips: exactly 3 S4 classes flip to excluded_now (26 vs 23), unknown
  34,500 vs 34,503**: the three classes that hold s5 528497 as a cost child,
  machine-identified from the frozen dependency graph:
  `16757` (mask `[1153204079095185408, 65536]`), `30345` (mask
  `[1152922604118478848, 65536]`), `15640` (mask `[1153204079095189504, 0]`).
  Classes 16757 and 30345 additionally lose their worklist slots for 528497
  (29 and 50 total slots respectively before adoption).
- **free_now unchanged at 33**: the class 23963 closure achieved by the
  canonical re-audit is UNAFFECTED by adopting the row.
- **update8 consequence: 5 group records flip to win-hit-blocked**, all via
  s4 class 16757 (see `output/refresh-summary.json` frozen_update8_refresh.
  win_hit_groups): roots first=36 (thirds 50/70/84 permutations with fourth
  84/50/70) and first=48 (thirds 40/80 with fourth 80/40). PLUS
  resolved_among_baseline_requirement grows 21 -> 22 (s5 528497 itself).
  remaining_now 31,838 -> 31,809 (root 36: 11,256 -> 11,169; root 48:
  10,963 -> 10,905; all other roots unchanged); per-root free-third coverage
  and free counts unchanged everywhere; groups_free_now 122 unchanged;
  worklist 65,213 -> 65,211 slots.

## Verdict for the scrutiny owner

Adopting the b018 WIN row would: (a) kill the (already dead) all-LOSS closure
route of class 16757 formally, (b) additionally exclude classes 30345 and
15640 from any all-LOSS closure route, (c) block 5 update8 groups on roots 36
and 48 as win-hit, and (d) not disturb any achieved free class (33) or any
achieved coverage. Nothing here adopts the row: this is analysis only, the
verdict remains unconsumed on main.

The standard 11x11 empty board, the 19 central-reply roots (including 36 and
48) and all classes remain UNKNOWN. Node counts are not verdicts; only the
2-pass rows cited above carry their cited results.
