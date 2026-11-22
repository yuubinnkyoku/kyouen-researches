# n11 central-reply closure class 23101 exact-S5 probe batch 14 (2026-11-22)

Batch 14 of the central-reply 19-root closure grind (K0415/K0417 line). Declared
as **Part AF** amendment of
`research/log/2026-11-22-n11-centralreply-19root-refresh-closure-batch1-single-owner-note.md`.

Context: batch 13 (class 16930, Part AE) WIN-HALTED at p003/p002 (11th and
12th unconsumed closure WINs; their third-implementation cross-verification
and the if-adopted decomposition remain open future declarations). Batch
record entering this batch: 13 batches, 11 WIN-HALT + 3 clean
(23963/10324/8784, the 33rd/34th/35th Board-verified free classes).

Selection: under the pre-registered rule (first clean candidate = neither in
flight nor WIN-halted, no refutation evidence), renewed closure ranks 1-9 all
carry refutation evidence (16757: b018, 20421: d002, 30345: b018 cost child
s5 528497, 16371: e002, 12264: f017, 5473: g018, 2634: h045, 8785: z003,
1518: j033), rank 10 (8106) WIN-HALTed in Part AC and rank 11 (16930)
WIN-HALTed in Part AE, so the first clean candidate is **renewed rank 12
class 23101** (mask `[1152921504892059648, 16]`, unknown 52, first 24 /
third 28, 3 groups served; all 52 still-unknown canonical S5 children sit in
the closure group first=24/third=28). Batch selection is a scheduling
quantity and never a verdict.

## Protocol

- keys: `input/batch-keys.json` (52 keys q001-q052, sha256
  `dfde0e90b75fd261b51ef746fe69a16eb182a99f5d2f8e1ff8bfa6efe936d71f`,
  inputs `input/q001..q052.input.csv`); the keys, legal counts and ordering
  are the Part Y re-audit probe-worklist rows `serving_class=23101`
  (probe_order 538-589 of the 65,154-row worklist, sha256
  `1807e4d21f6fb757ea21850c6bda4d822cb76ac59abfa9bcd1cc7b53bd7055ef`).
  The worklist is regenerable and not republished; the 52 class rows are
  published here in full via batch-keys.json, so the selection is
  independently checkable against the canonical cache and the update8
  machinery. Key prefix note: `q` skips the batch 1-13 prefixes
  (b/c/d/e/f/g/h/j/m/z/n/p) and the third-implementation anchor ids
  (k02a/l1a); the prefix is bookkeeping only.
- worklist re-derivation: this declaring session reuses the same
  workspace regeneration as batches 12-13 (documented in the Part AC and
  Part AE scaffold READMEs): published Part Y scenario script (sha256
  `88671526...`) run twice from the re-fetched pinned inputs 6, all outputs
  byte-identical and byte-equal to the published Part Y canonical outputs
  (this session re-verified worklist run1 == run2, sha256 `1807e4d2...`,
  and closure-classes.csv / per-root-coverage.csv / refresh-summary.json
  byte-equal to the published canonical copies on main).
- fail-safe machine checks done before declaring: (1) all 52 keys absent
  from the canonical merged cache (6,027 data rows, sha256 `95e868d6...`,
  52/52 misses, 0 hits); (2) quarantine registry (sha256 `81d23160...`, 2
  active entries) key-pair cross-check 0 hits, both directions; (3) the 52
  keys are duplicate free; (4) the renewed closure-classes.csv rank 12 row
  matches class 23101 (mask `[1152921504892059648, 16]`, unknown 52, first
  24 / third 28, groups 3) byte-against the published Part Y output; (5)
  none of the twelve unconsumed WIN keys
  (b018/d002/e002/f017/g018/j033/h045/z003/n005/n006/p002/p003) is among
  the 52 unknown children of class 23101 (cost-child cross-check, 0 hits);
  (6) probe_order contiguity 538-589 with class_unknown_now = 52 on every
  row.
- solver: pinned replica `scripts/jsreplay.js` (sha256
  `845856175d3c793a7eb4306f5902ecda3f1c046a8a53e8f34ed375e51febc3df`),
  identical bytes to batches 1-13
- per key: 2 fresh cold passes at budget 15,000,000, one solver per row, exact
  order=count, publish=ALL; runner `scripts/runbatch.sh` (HARD-STOP rc=42 on
  (result,nodes,legal) mismatch, WIN-HALT rc=45 on result 1; this host runs
  up to 4 single-key runner invocations concurrently, which does not affect
  determinism because every pass is a fresh cold share_tt=0 process)
- validation gate before the first row: the published two-target-design 4
  rows are reproduced node-exact on this host (see `output/val-gate/`; this
  host's fresh runs: at2m result 0/2,000,000 twice, 15m result 2/3,651,923
  and result 2/5,040,200, 4/4 node-exact on (result, nodes, legal); the 9th
  diagnostic field of the replay line is host-dependent and outside the
  pre-registered gate)
- parallelism: this host runs at most 4 workers, keys processed in
  probe_order waves (`scripts/runner-all.sh`, resume-safe); after a WIN is
  reported no new key is started, and keys already in flight in the same
  wave complete and are disclosed honestly (batch-5 f018 precedent)
- honest negatives: budget exhaustion (result 0) is recorded as UNKNOWN; no
  15M same-condition re-search
- consumption: only 2-pass LOSS rows may later enter a fail-closed increment
  cache candidate (future verifier declaration, Part C/M/Y mechanism);
  this batch alone consumes nothing

## Status

Declared and scaffold published before the first probe row (this README will
be amended with the result section in a later commit; per-row honest records
land in `output/status.log` and `output/raw/`). The standard 11x11 empty
board, the 19 central-reply roots and class 23101 remain UNKNOWN throughout.
Nodes are not verdicts.
