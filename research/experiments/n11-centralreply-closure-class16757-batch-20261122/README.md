# n11 central-reply closure class 16757 exact-S5 probe batch 1 (2026-11-22)

Declared in
`research/log/2026-11-22-n11-centralreply-19root-refresh-closure-batch1-single-owner-note.md`
(commit `1596a630`, observed HEAD-before-push `216752f7`).

Batch 1 of the central-reply 19-root closure grind (K0415/K0417 line): the ranked
closure-certificate candidate #1 from the 2026-11-22 frontier refresh
(`../n11-central-reply-19root-frontier-refresh-20261122/output/closure-classes.csv`)
is S4 graph class index `16757` (mask `[1153204079095185408, 65536]`) with 48
still-unknown canonical S5 children. If all 48 settle exact LOSS, the class
becomes closable; it serves 5 (first, third) groups across the 19 roots, cheapest
at first=36/third=50. **No coverage, closure or root claim is made by this
batch**: the class closes only after an independent re-verification audit
(rerun of the refresh with the new cache), which this batch does not perform.

## Protocol

- keys: `input/batch-keys.json` (48 keys, inputs `input/b001..b048.input.csv`,
  `target,0,5,lo,hi,legal,0,0,0,0,0` with Board-recomputed legal counts)
- solver: pinned replica `scripts/jsreplay.js`
  (sha256 `845856175d3c793a7eb4306f5902ecda3f1c046a8a53e8f34ed375e51febc3df`),
  identical bytes to the reply27 probe publications
- per key: 2 fresh cold passes at budget 15,000,000, one solver per row, exact
  order=count, publish=ALL; runner `scripts/runbatch.sh` (HARD-STOP rc=42 on
  (result,nodes,legal) mismatch, WIN-HALT rc=45 on result 1)
- validation gate before the first row: the published two-target-design 4 rows
  are reproduced node-exact on this host (see `output/val-gate/`)
- honest negatives: budget exhaustion (result 0) is recorded as UNKNOWN; no
  15M same-condition re-search
- consumption: only 2-pass LOSS rows may later enter a fail-closed increment
  cache candidate (published separately with a WIN/LOSS conflict gate); this
  batch alone consumes nothing

## Status (batch halted 2026-11-22T02:39:43Z, pre-registered WIN-HALT)

- b001-b017, b019, b020: 2-pass node-exact, result 2 (LOSS), 15M budget, raw in
  `output/raw/` (published, raw URLs byte-verified against the pinned commit)
- **b018: 2-pass node-exact result 1 (WIN), 3,549,602 nodes both passes** ->
  pre-registered WIN-HALT fired (status.log). Consequence: the all-48-LOSS
  closure route for S4 class 16757 is refuted by a verified WIN child; the class
  drops out of the all-LOSS certificate candidate ranking from the 2026-11-22
  frontier refresh. No class-resolved claim of any kind is made from a WIN
  child on its own.
- b021-b048: not probed in this batch (halt honored), UNKNOWN. A future batch
  may resume them for cache completeness; they no longer serve certificate
  closure.
- All verdict rows are available as increment-cache candidates only through the
  separate fail-closed merge gate (not performed here).
- The standard 11x11 empty board, the 19 central-reply roots and class 16757
  remain UNKNOWN throughout.
