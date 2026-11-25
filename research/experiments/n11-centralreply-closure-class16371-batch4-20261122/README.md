# n11 central-reply closure class 16371 exact-S5 probe batch 4 (2026-11-22)

Batch 4 of the central-reply 19-root closure grind (K0415/K0417 line). Declared
as Part E amendment of
`research/log/2026-11-22-n11-centralreply-19root-refresh-closure-batch1-single-owner-note.md`.

Context: batch 1 (class 16757) halted at the pre-registered WIN-HALT (b018);
batch 2 (class 23963) closed 48/48 LOSS and the class was certified free by the
fail-closed merge + re-audit (free_now 32 -> 33); batch 3 (class 20421) halted
at the WIN-HALT (d002 result 1, 2-pass node-exact; if-adopted analysis
published as
`../n11-central-reply-20421-win-d002-ifadopted-20261122/`). With the closure
ranking's top candidates now holding WIN children (16757: b018; 20421: d002;
30345: holds b018's s5 528497 as a cost child), the first ranked class with
no refutation evidence is S4 graph class index `16371` (mask
`[1153202979851993088, 16]`), re-audit closure rank 4 with 50 still-unknown
canonical S5 children, serving the root first=26 / third=50 group. If all 50
settle exact LOSS, the class becomes closable by the same machinery;
**no coverage, closure or root claim is made by this batch**: closure needs
the independent merge + refresh re-audit.

## Protocol

- keys: `input/batch-keys.json` (50 keys e001-e050, inputs
  `input/e001..e050.input.csv`, `target,0,5,lo,hi,legal,0,0,0,0,0`; the keys,
  legal counts (74..94) and ordering are the canonical re-audit probe-worklist
  rows `serving_class=16371` in probe_order)
- fail-safe machine checks done before declaring: all 50 keys absent from the
  canonical merged cache (5,924 rows, sha256 `8a721a18...`, 0 hits);
  quarantine registration through the refresh's policy as for batches 2/3
- solver: pinned replica `scripts/jsreplay.js` (sha256
  `845856175d3c793a7eb4306f5902ecda3f1c046a8a53e8f34ed375e51febc3df`),
  identical bytes to batches 1-3
- per key: 2 fresh cold passes at budget 15,000,000, one solver per row, exact
  order=count, publish=ALL; runner `scripts/runbatch.sh` (HARD-STOP rc=42 on
  (result,nodes,legal) mismatch, WIN-HALT rc=45 on result 1)
- validation gate before the first row: the published two-target-design 4 rows
  are reproduced node-exact on this host (see `output/val-gate/`; this host's
  runs: at2m result 0/2,000,000 twice, 15m result 2/3,651,923 and
  result 2/5,040,200, 4/4 node-exact)
- honest negatives: budget exhaustion (result 0) is recorded as UNKNOWN; no
  15M same-condition re-search
- consumption: only 2-pass LOSS rows may later enter a fail-closed increment
  cache candidate; this batch alone consumes nothing

## Status

see `output/status.log`. The standard 11x11 empty board, the 19 central-reply
roots and class 16371 remain UNKNOWN throughout. Nodes are not verdicts.

## Status: WIN-HALT at e002 (2026-11-22T03:26:03Z)

Pre-registered WIN-HALT fired on key e002 (s5_index 183566, key
`[1153765929805414400, 16]`, legal 79): 2-pass node-exact
**result 1 (WIN), 14,112,632 nodes** at budget 15,000,000.
Probed before the halt (both 2-pass node-exact):

- e001 LOSS 882,800 nodes
- e002 **WIN** 14,112,632 nodes (HALT)

Consequences (honest, no speculation): with e002 a WIN child, the
all-children-LOSS closure route for class 16371 is refuted. e003-e050
remain unprobed (48 keys, no 15M same-condition re-search consumed).
e002's WIN is NOT adopted by this lane (verdict unconsumed, scrutiny owner
pending), exactly as b018 (batch 1) and d002 (batch 3). The batch is stopped
per the pre-registered rule.

Empirical note (scheduling-relevant, not a claim): of the four closure
batches so far, three halted on a pre-registered WIN (16757: b018; 20421:
d002; 16371: e002) and only 23963 closed 48/48 LOSS. The cheap end of the
closure-classes ranking appears WIN-dense; candidate selection may benefit
from more scrutiny-owner verdict consumption before further full batches.
No WIN row is consumed here and no inference is drawn beyond the refuted
closure routes.

The standard 11x11 empty board, the 19 central-reply roots, class 16371
and all remaining S5 keys remain UNKNOWN. Nodes are not verdicts.
