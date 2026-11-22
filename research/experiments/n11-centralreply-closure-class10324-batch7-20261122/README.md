# n11 central-reply closure class 10324 exact-S5 probe batch 7 (2026-11-22)

Batch 7 of the central-reply 19-root closure grind (K0415/K0417 line). Declared
as **Part L** amendment of
`research/log/2026-11-22-n11-centralreply-19root-refresh-closure-batch1-single-owner-note.md`.

Context: batches 1/3/4/5/6 all halted at pre-registered WINs (16757: b018;
20421: d002; 16371: e002; 12264: f017; 5473: g018 - all unconsumed, scrutiny
owner pending). The Part H-bis closure ranking therefore now carries
refutation evidence in ranks 1-6, and the first candidate without any is
re-audit closure-classes **rank 7 class 10324** (mask
`[1152921504607191040, 0]`), with 51 still-unknown canonical S5 children
serving the first=14/third=16 groups (4 groups). The measured WIN-dense cheap
end (5 WIN-HALTs in 6 batches) stays a scheduling observation only; batch
selection is never a verdict. If all 51 settle exact LOSS the class becomes
closable by the same machinery; **no coverage, closure or root claim is made by
this batch**: closure needs the independent merge + refresh re-audit.

## Protocol

- keys: `input/batch-keys.json` (51 keys h001-h051, inputs
  `input/h001..h051.input.csv`); the keys, legal counts and ordering are the
  canonical re-audit probe-worklist rows `serving_class=10324`
  (probe_order 281-331, worklist sha256 `cbea9e79...` byte-identical to the
  published re-audit output and the lane kit copies)
- fail-safe machine checks done before declaring: (1) canonical worklist and
  closure-classes files verified against the published re-audit bytes
  (sha256 match on both copies used); (2) all 51 keys absent from the
  canonical merged cache (5,924 rows, sha256 `8a721a18...`, 0 hits);
  (3) quarantine registry (sha256 `81d23160...`, 4 active entries)
  key-pair check 0 hits
- solver: pinned replica `scripts/jsreplay.js` (sha256
  `845856175d3c793a7eb4306f5902ecda3f1c046a8a53e8f34ed375e51febc3df`),
  identical bytes to batches 1-6
- per key: 2 fresh cold passes at budget 15,000,000, one solver per row, exact
  order=count, publish=ALL; runner `scripts/runbatch.sh` (HARD-STOP rc=42 on
  (result,nodes,legal) mismatch, WIN-HALT rc=45 on result 1)
- validation gate before the first row: the published two-target-design 4
  rows are reproduced node-exact on this host (see `output/val-gate/`; this
  host's fresh runs: at2m result 0/2,000,000 twice, 15m result 2/3,651,923 and
  result 2/5,040,200, 4/4 node-exact)
- honest negatives: budget exhaustion (result 0) is recorded as UNKNOWN; no
  15M same-condition re-search
- consumption: only 2-pass LOSS rows may later enter a fail-closed increment
  cache candidate; this batch alone consumes nothing

## Status

see `output/status.log`. The standard 11x11 empty board, the 19 central-reply
roots and class 10324 remain UNKNOWN throughout. Nodes are not verdicts.

## Status: COMPLETED - 51/51 all-LOSS (2026-11-22T05:59:50Z)

**No WIN-HALT fired.** All 51 keys h001-h051 are 2-pass node-exact
**LOSS (result 2)** at budget 15M (per-key nodes 2,133,491 - 7,430,631;
cumulative 203,517,761 nodes). Provenance note: rows h001-h010 and h011-h019
were run by two concurrent instances of this lane (the same hourly task);
every duplicated execution produced identical (result, nodes, legal) rows, and
the published status.log keeps each row once. The parallel-run collision is
recorded in the session log continuation.

Unlike batches 1/3/4/5/6, the all-children-LOSS closure route for class 10324
survives this batch. **Consumption is still not done by this batch alone**:
the class becomes closable only after the fail-closed increment merge into the
canonical cache plus the refresh re-audit (Board-verified, quarantine-free),
published as its own experiment. **The standard 11x11 empty board, the 19
central-reply roots and class 10324 remain UNKNOWN** until that re-audit
certifies the closure.
