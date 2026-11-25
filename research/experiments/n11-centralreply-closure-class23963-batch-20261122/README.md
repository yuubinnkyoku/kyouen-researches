# n11 central-reply closure class 23963 exact-S5 probe batch 2 (2026-11-22)

Batch 2 of the central-reply 19-root closure grind (K0415/K0417 line). Declared
as Part C amendment of
`research/log/2026-11-22-n11-centralreply-19root-refresh-closure-batch1-single-owner-note.md`.

Context: batch 1 (class 16757, the frontier-refresh closure rank #1) halted at
its pre-registered WIN-HALT rule on key b018 (2-pass node-exact result 1), which
refutes the all-48-LOSS closure route for class 16757 (see
`../n11-centralreply-closure-class16757-batch-20261122/README.md`). The next
ranked candidate from the same 2026-11-22 frontier refresh is S4 graph class
index `23963` (mask `[1152921504673955840, 67109888]`) with 48 still-unknown
canonical S5 children, serving 3 (first, third) groups, cheapest at
first=24/third=52 (`closure-classes.csv` class_rank 2). If all 48 settle exact
LOSS, the class becomes closable; **no coverage, closure or root claim is made by
this batch**: the class closes only after an independent re-verification audit
(rerun of the refresh with the new cache), which this batch does not perform.

## Protocol

- keys: `input/batch-keys.json` (48 keys, inputs `input/c001..c048.input.csv`,
  `target,0,5,lo,hi,legal,0,0,0,0,0`, legal counts are the Board-recomputed
  values from the refresh worklist `probe-worklist.csv`, ordering by
  probe_order)
- solver: pinned replica `scripts/jsreplay.js` (sha256
  `845856175d3c793a7eb4306f5902ecda3f1c046a8a53e8f34ed375e51febc3df`),
  identical bytes to batch 1 and to the reply27 probe publications
- fail-safe machine checks done before declaring: all 48 keys absent from the
  merged chain cache (`4fee9d5e...`, 5,857 rows, 0 hits); worklist built through
  the refresh's quarantine-registry policy
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

## Status (batch complete 2026-11-22T02:56:54Z)

- **all 48 keys (c001-c048): 2-pass node-exact, result 2 (LOSS), budget 15M**
  (no WIN, no budget exhaustion, no mismatch; status.log 48 PASS rows, rc=0)
- independent row audit `output/batch-audit.json`: 48/48 keys 2-pass agree,
  key/lo/hi and legal counts machine-verified against `input/batch-keys.json`,
  all input csv rows regenerate byte-exact; total nodes 76,504,609 per pass,
  153,009,218 for both passes
- consequence: the all-48-LOSS closure route for S4 class 23963 SURVIVES this
  batch. The class becomes closable only after the independent re-verification
  audit (rerun of the frontier refresh with a fail-closed merged cache that
  includes these 48 rows, with the Board fail-safe boundary regeneration);
  that audit is a separate publication. **No closure or coverage claim is made
  by this batch alone.**
- consumption: the 48 LOSS rows are increment-cache candidates via the
  fail-closed union merger with a WIN/LOSS conflict gate (separate publication);
  this batch consumes nothing
- the standard 11x11 empty board, the 19 central-reply roots and class 23963
  remain UNKNOWN throughout
