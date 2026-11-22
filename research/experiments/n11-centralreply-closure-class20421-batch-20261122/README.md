# n11 central-reply closure class 20421 exact-S5 probe batch 3 (2026-11-22)

Batch 3 of the central-reply 19-root closure grind (K0415/K0417 line). Declared
as Part D amendment of
`research/log/2026-11-22-n11-centralreply-19root-refresh-closure-batch1-single-owner-note.md`.

Context: batch 1 (class 16757, refresh closure rank 1) halted at the
pre-registered WIN-HALT (b018 result 1 double-pass node-exact; all-LOSS route
refuted). Batch 2 (class 23963) completed 48/48 2-pass node-exact LOSS and the
class was certified free by the fail-closed merge + re-audit
(`../n11-central-reply-23963-closure-reaudit-20261122/`, free_now 32 -> 33).
The genuine next all-LOSS candidate in the re-audit
`closure-classes.csv` is S4 graph class index `20421` (mask
`[1155173304420536320, 131072]`) with 49 still-unknown canonical S5 children,
serving 4 (first, third) groups, cheapest at first=12/third=51 (class_rank 2,
after the 16757 remnant at rank 1, which is permanently non-closable once its
WIN child is consumed). If all 49 settle exact LOSS, the class becomes
closable by the same machinery; **no coverage, closure or root claim is made by
this batch**: closure needs the independent merge + refresh re-audit.

## Protocol

- keys: `input/batch-keys.json` (49 keys d001-d049, inputs
  `input/d001..d049.input.csv`, `target,0,5,lo,hi,legal,0,0,0,0,0`; legal
  counts are the Board-recomputed values from the re-audit worklist
  `probe-worklist.csv` rows `serving_class=20421`, ordering by probe_order)
- fail-safe machine checks done before declaring: all 49 keys absent from the
  canonical merged cache (5,924 rows, 0 hits); worklist built through the
  refresh's quarantine-registry policy
- solver: pinned replica `scripts/jsreplay.js` (sha256
  `845856175d3c793a7eb4306f5902ecda3f1c046a8a53e8f34ed375e51febc3df`),
  identical bytes to batches 1/2
- per key: 2 fresh cold passes at budget 15,000,000, one solver per row, exact
  order=count, publish=ALL; runner `scripts/runbatch.sh` (HARD-STOP rc=42 on
  (result,nodes,legal) mismatch, WIN-HALT rc=45 on result 1)
- validation gate before the first row: the published two-target-design 4 rows
  are reproduced node-exact on this host (see `output/val-gate/`)
- honest negatives: budget exhaustion (result 0) is recorded as UNKNOWN; no
  15M same-condition re-search
- consumption: only 2-pass LOSS rows may later enter a fail-closed increment
  cache candidate; this batch alone consumes nothing

## Status

see `output/status.log` and the final README section. The standard 11x11
empty board, the 19 central-reply roots and class 20421 remain UNKNOWN
throughout.
