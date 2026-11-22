# n11 central-reply closure class 5830 exact-S5 probe batch 15 (2026-11-22)

Batch 15 of the central-reply 19-root closure grind (K0415/K0417 line). Declared
as **Part AK** amendment of
`research/log/2026-11-22-n11-centralreply-19root-refresh-closure-batch1-single-owner-note.md`
(note blob sha `deea536f...` after the declaration commit `0f57eef7`).

Context: 14 batches at declaration time, 11 WIN-HALT + 3 clean
(23963/10324/8784, the 33rd/34th/35th Board-verified free classes); batch 13
(class 16930) halted at p002/p003, batch 14 (class 23101) in flight by another
operator (Part AF). Twelve unconsumed closure WINs are third-implementation
verdict-level cross-verified (Part G/H/K/O/P/T/W/AA/AD/AG) and adoption remains
with the scrutiny owner (C++ second implementation gate pin `9193f5b6...`).

Selection: under the pre-registered rule (first clean candidate = neither in
flight nor WIN-halted, no refutation evidence), renewed closure ranks 1-12 are
all evidence-carrying, WIN-halted or in flight (16757: b018, 20421: d002,
30345: b018 cost child, 16371: e002, 12264: f017, 5473: g018, 2634: h045,
8785: z003, 1518: j033, 8106: n005/n006, 16930: p002/p003, 23101: batch-14 in
flight), so the first clean candidate is **renewed rank 13 class 5830**
(mask `[4035788216077385728, 0]`, unknown 52, groups 2 served: root 49
third 59 and root 49 third 61; all 52 still-unknown canonical S5 children sit
in those closure groups). Batch selection is a scheduling quantity and never
a verdict.

## Protocol

- keys: `input/batch-keys.json` (52 keys r001-r052, sha256
  `af3e4c46af0d84bcb248c350283b07e26b901f6e0d196038e24bd1292b133727`,
  inputs `input/r001..r052.input.csv`); the keys, legal counts and ordering
  are the Part Y re-audit probe-worklist rows `serving_class=5830`
  (probe_order 590-641 of the 65,154-row worklist, sha256
  `1807e4d21f6fb757ea21850c6bda4d822cb76ac59abfa9bcd1cc7b53bd7055ef`).
  The worklist is regenerable and not republished; the 52 class rows are
  published here in full via batch-keys.json, so the selection is
  independently checkable against the canonical cache and the update8
  machinery. Key prefix note: `r` continues the batch 1-14 prefixes
  (b/c/d/e/f/g/h/j/m/z/n/p/q) and avoids the third-implementation anchor ids
  (k02a/l1a); the prefix is bookkeeping only.
- worklist re-derivation: this declaring session regenerated the workspace
  from the six pinned inputs exactly as documented in the Part AC/AE/AF
  scaffold READMEs: published Part Y refresh script (sha256 `88671526...`)
  run against the pinned dependency graph (`54f9c364...`), merged cache
  (6,027 data rows, `95e868d6...`), repaired update8 plan, independent Board
  source (`954d3a10...`), evidence policy and quarantine registry
  (`81d23160...`). Three runs on this host were byte-identical; the three
  outputs (closure-classes.csv `61943b85...`, per-root-coverage.csv
  `33f01a0c...`, refresh-summary.json `25987add...`) and the regenerated
  probe-worklist.csv (`1807e4d2...`) match the published Part Y canonical
  bytes; the published closure-classes.csv copy on main was also cmp-verified
  byte-equal (rank 13 row = class 5830, mask `[4035788216077385728, 0]`,
  unknown 52, first group root 49 third 59, groups 2). Fresh
  class_status_counts reproduction: excluded 390 / excluded_now 23 / free_now
  35 / unknown 34501, joint greedy 35,242, update8 remaining_now 31,784.
- fail-safe machine checks done before declaring: (1) all 52 keys absent
  from the canonical merged cache (52/52 misses, 0 hits); (2) quarantine
  registry (sha256 `81d23160...`, 2 active entries) key-pair cross-check
  0 hits, both directions; (3) the 52 keys are duplicate free; (4) the
  renewed closure-classes.csv rank 13 row matches class 5830 against the
  published Part Y output; (5) none of the twelve unconsumed WIN keys
  (b018/d002/e002/f017/g018/j033/h045/z003/n005/n006/p002/p003, machine-
  extracted from the ten published batch-keys.json files) is among the 52
  unknown children of class 5830 (0 hits); (6) probe_order contiguity
  590-641 with class_unknown_now = 52 on every row;
  membership_class_count distribution {1: 7, 2: 15, 3: 30}.
- solver: pinned replica `scripts/jsreplay.js` (sha256
  `845856175d3c793a7eb4306f5902ecda3f1c046a8a53e8f34ed375e51febc3df`),
  identical bytes to batches 1-14
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
board, the 19 central-reply roots and class 5830 remain UNKNOWN throughout.
Nodes are not verdicts.
