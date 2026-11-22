# n11 central-reply closure class 5473 exact-S5 probe batch 6 (2026-11-22)

Batch 6 of the central-reply 19-root closure grind (K0415/K0417 line). Declared
as Part I amendment of
`research/log/2026-11-22-n11-centralreply-19root-refresh-closure-batch1-single-owner-note.md`.

Context: batches 1/3/4/5 halted at pre-registered WINs (16757: b018; 20421:
d002; 16371: e002; 12264: f017 - all unconsumed, scrutiny owner pending; class
30345 additionally holds b018's s5 528497 as a cost child). Batch 2 closed class
23963 (48/48 LOSS, re-audit certified free, free_now 32 -> 33). Part H-bis
confirmed that closure ranks 1-5 carry refutation evidence in every adoption
scenario, so the first candidate with none is S4 graph class index
`5473` (mask `[1158058422931816448, 0]`), re-audit closure rank 6 with 51
still-unknown canonical S5 children, serving 4 (first, third) groups, cheapest
at first=26/third=59. The measured 4-of-5 WIN-dense cheap end stays a
scheduling observation only; batch selection is never a verdict. If all 51
settle exact LOSS, the class becomes closable by the same machinery; **no
coverage, closure or root claim is made by this batch**: closure needs the
independent merge + refresh re-audit.

## Protocol

- keys: `input/batch-keys.json` (51 keys g001-g051, inputs
  `input/g001..g051.input.csv`); the keys, legal counts (72..92) and ordering
  are the canonical re-audit probe-worklist rows `serving_class=5473` in
  probe_order (230-280)
- fail-safe machine checks done before declaring: (1) the re-audit
  `probe-worklist.csv` (65,213 rows) and all three re-audit summaries
  (`closure-classes.csv`, `per-root-coverage.csv`, `refresh-summary.json`)
  regenerate byte-identically on this host from the pinned
  `refresh_19root_frontier.py` + pinned inputs (dependency-graph.json.gz,
  merged chain cache sha256 `8a721a18...`, update8 plan, independent.py,
  s5_evidence_policy.py, quarantine registry); (2) all 51 keys absent from
  the canonical merged cache (5,924 rows, 0 hits); (3) quarantine registry
  key-pair check 0 hits
- solver: pinned replica `scripts/jsreplay.js` (sha256
  `845856175d3c793a7eb4306f5902ecda3f1c046a8a53e8f34ed375e51febc3df`),
  identical bytes to batches 1-5
- per key: 2 fresh cold passes at budget 15,000,000, one solver per row, exact
  order=count, publish=ALL; runner `scripts/runbatch.sh` (HARD-STOP rc=42 on
  (result,nodes,legal) mismatch, WIN-HALT rc=45 on result 1)
- validation gate before the first row: the published two-target-design 4
  rows are reproduced node-exact on this host (see `output/val-gate/`; this
  host's runs: at2m result 0/2,000,000 twice, 15m result 2/3,651,923 and
  result 2/5,040,200, 4/4 node-exact)
- honest negatives: budget exhaustion (result 0) is recorded as UNKNOWN; no
  15M same-condition re-search
- consumption: only 2-pass LOSS rows may later enter a fail-closed increment
  cache candidate; this batch alone consumes nothing

## Status

see `output/status.log`. The standard 11x11 empty board, the 19 central-reply
roots and class 5473 remain UNKNOWN throughout. Nodes are not verdicts.
