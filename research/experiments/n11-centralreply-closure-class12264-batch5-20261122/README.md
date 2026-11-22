# n11 central-reply closure class 12264 exact-S5 probe batch 5 (2026-11-22)

Batch 5 of the central-reply 19-root closure grind (K0415/K0417 line). Declared
as Part F amendment of
`research/log/2026-11-22-n11-centralreply-19root-refresh-closure-batch1-single-owner-note.md`.

Context: batches 1/3/4 halted at pre-registered WINs (16757: b018; 20421:
d002; 16371: e002 - all unconsumed, scrutiny owner pending; class 30345
additionally holds b018's s5 528497 as a cost child). Batch 2 closed class
23963 (48/48 LOSS, re-audit certified free, free_now 32 -> 33). With closure
ranks 1-4 all carrying refutation evidence, the next candidate with none is
S4 graph class index `12264` (mask `[1152921504606848033, 0]`), re-audit
closure rank 5 with 51 still-unknown canonical S5 children (graph cost size
52: 51 unknown + 1 already-known non-WIN cost child), serving groups that
include root first=0 / third=5. If all 51 settle exact LOSS, the class becomes
closable by the same machinery; **no coverage, closure or root claim is made
by this batch**: closure needs the independent merge + refresh re-audit.

## Protocol

- keys: `input/batch-keys.json` (51 keys f001-f051, inputs
  `input/f001..f051.input.csv`); the keys, legal counts (76..92) and ordering
  are the canonical re-audit probe-worklist rows `serving_class=12264` in
  probe_order
- fail-safe machine checks done before declaring: all 51 keys absent from
  the canonical merged cache (5,924 rows, sha256 `8a721a18...`, 0 hits)
- solver: pinned replica `scripts/jsreplay.js` (sha256
  `845856175d3c793a7eb4306f5902ecda3f1c046a8a53e8f34ed375e51febc3df`),
  identical bytes to batches 1-4
- per key: 2 fresh cold passes at budget 15,000,000, one solver per row, exact
  order=count, publish=ALL; runner `scripts/runbatch.sh` (HARD-STOP rc=42 on
  (result,nodes,legal) mismatch, WIN-HALT rc=45 on result 1)
- validation gate before the first row: the published two-target-design 4
  rows are reproduced node-exact on this host (see `output/val-gate/`; this
  host's runs: at2m result 0/2,000,000 twice, 15m result 2/3,651,923 and
  result 2/5,040,200, 4/4 node-exact; same host as batch 3 runs)
- honest negatives: budget exhaustion (result 0) is recorded as UNKNOWN; no
  15M same-condition re-search
- consumption: only 2-pass LOSS rows may later enter a fail-closed increment
  cache candidate; this batch alone consumes nothing

## Status

see `output/status.log`. The standard 11x11 empty board, the 19 central-reply
roots and class 12264 remain UNKNOWN throughout. Nodes are not verdicts.

## Status: WIN-HALT at f017 (2026-11-22T03:41:36Z)

Pre-registered WIN-HALT fired on key f017 (s5_index 415095, key
`[1188950301625810945, 70368744177666]`, legal 82): 2-pass node-exact
**result 1 (WIN), 3,522,635 nodes** at budget 15,000,000. Probed total:
18/51 (all 2-pass node-exact; 17 LOSS + f017 WIN):

- f001-f016 LOSS (cumulative nodes in status.log: 23,693,764 + f009-016
  chunk; see the published raws)
- f017 **WIN 3,522,635 nodes (HALT)**
- f018 LOSS 3,598,340 nodes (completed in-flight before the halt observer
  stopped the batch; published as-is, 2-pass node-exact)

Consequences (honest): with f017 a WIN child, the all-children-LOSS closure
route for class 12264 is refuted. f019-f051 remain unprobed (33 keys, no 15M
same-condition re-search consumed). f017's WIN is NOT adopted (verdict
unconsumed, scrutiny owner pending), exactly as b018, d002, e002.

Empirical update: 4 of 5 closure batches have now WIN-halted (16757: b018,
20421: d002, 16371: e002, 12264: f017); only 23963 closed 48/48 LOSS. 5 of
the 5 batches' halt keys or refutations sit at closure rank 1-5, all chosen
by ascending unknown-count: the cheap end of the ranking is measured to be
WIN-dense, and candidate scoring for future batches should account for it
(the ranking itself stays a scheduling quantity, never a verdict).

The standard 11x11 empty board, the 19 central-reply roots, class 12264 and
all remaining S5 keys remain UNKNOWN. Nodes are not verdicts.
