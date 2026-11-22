# n11 central-reply closure class 8106 exact-S5 probe batch 12 (2026-11-22)

Batch 12 of the central-reply 19-root closure grind (K0415/K0417 line). Declared
as **Part AC** amendment of
`research/log/2026-11-22-n11-centralreply-19root-refresh-closure-batch1-single-owner-note.md`.

Context: batch 11 (class 8785, Part Z) WIN-HALTED at z003 (8th unconsumed
closure WIN, now third-implementation cross-verified in Part AA and
decomposed, WIN-only / LOSS-only / full, in Part AB). Batch record: 8
WIN-HALT + 3 clean in 11 batches (23963/10324/8784, the 33rd/34th/35th
Board-verified free classes).

Selection: under the pre-registered rule (first clean candidate = neither in
flight nor WIN-halted, no refutation evidence), renewed closure ranks 1-8 all
carry refutation evidence (16757: b018, 20421: d002, 30345: b018's cost child
s5 528497, 16371: e002, 12264: f017, 5473: g018, 2634: h045, 8785: z003) and
rank 9 (1518: j033) too, so the first clean candidate is **renewed rank 10
class 8106** (mask `[1152926194711134208, 0]`, unknown 52, first 14 / third 58,
4 groups served; all 52 still-unknown canonical S5 children sit in the
closure group first=14/third=58). Batch selection is a scheduling quantity
and never a verdict.

## Protocol

- keys: `input/batch-keys.json` (52 keys n001-n052, sha256
  `de55df83483663e31b1c1db0fb8a1239079e7152bddef9bd893439b7b2fdbdc2`,
  inputs `input/n001..n052.input.csv`); the keys, legal counts and ordering
  are the Part Y re-audit probe-worklist rows `serving_class=8106`
  (probe_order 434-485 of the 65,154-row worklist, sha256
  `1807e4d21f6fb757ea21850c6bda4d822cb76ac59abfa9bcd1cc7b53bd7055ef`).
  The worklist is regenerable and not republished; the 52 class rows are
  published here in full via batch-keys.json, so the selection is
  independently checkable against the canonical cache and the update8
  machinery. Key prefix note: `n` skips the batch 1-11 prefixes
  (b/c/d/e/f/g/h/j/m/z) and the third-implementation anchor ids (k02a/l1a);
  the prefix is bookkeeping only.
- worklist re-derivation (this session): the declaring session lost its local
  workspace to an execution-environment reset, so the Part Y pinned inputs 6
  (dependency-graph `54f9c364...`, merged canonical cache 6,027 rows
  `95e868d6...`, update8 plan `b658290a...`, Board source `954d3a10...`,
  evidence policy `78655e94...`, quarantine registry `81d23160...`) were
  re-fetched byte-exact from the repo canonical copies (commit `0a369d6c`
  pinned raw) and the published Part Y scenario script
  (`refresh_19root_frontier.py`, sha256 `88671526...`) was re-run twice on
  this host: all four outputs byte-identical between the runs, and
  closure-classes.csv / per-root-coverage.csv / refresh-summary.json
  byte-equal to the published Part Y canonical outputs (cross-host
  byte-exact reproduction, same as the published Part AB base control).
  All 52 batch keys were then machine-extracted from the regenerated
  worklist.
- fail-safe machine checks done before declaring: (1) all 52 keys absent
  from the canonical merged cache (6,027 rows, sha256 `95e868d6...`, 52/52
  misses, 0 hits); (2) quarantine registry (sha256 `81d23160...`, 2 active
  entries) key-pair cross-check 0 hits, both directions; (3) the 52 keys are
  duplicate free; (4) the renewed closure-classes.csv rank 10 row matches
  class 8106 (mask `[1152926194711134208, 0]`, unknown 52, first 14 /
  third 58, groups 4) byte-against the published Part Y output; (5) none of
  the eight unconsumed WIN keys (b018/d002/e002/f017/g018/j033/h045/z003)
  is among the 52 unknown children of class 8106 (cost-child cross-check,
  0 hits).
- solver: pinned replica `scripts/jsreplay.js` (sha256
  `845856175d3c793a7eb4306f5902ecda3f1c046a8a53e8f34ed375e51febc3df`),
  identical bytes to batches 1-11
- per key: 2 fresh cold passes at budget 15,000,000, one solver per row, exact
  order=count, publish=ALL; runner `scripts/runbatch.sh` (HARD-STOP rc=42 on
  (result,nodes,legal) mismatch, WIN-HALT rc=45 on result 1; this host runs
  up to 4 single-key runner invocations concurrently, which does not affect
  determinism because every pass is a fresh cold share_tt=0 process)
- validation gate before the first row: the published two-target-design 4
  rows are reproduced node-exact on this host (see `output/val-gate/`; this
  host's fresh runs: at2m result 0/2,000,000 twice, 15m result 2/3,651,923
  and result 2/5,040,200, 4/4 node-exact on (result, nodes, legal))
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
board, the 19 central-reply roots and class 8106 remain UNKNOWN throughout.
Nodes are not verdicts.

## Result (2026-11-22, amending this README after batch stop)

Batch halted under the pre-registered WIN-HALT rule at **8/52 probed**
(n001-n008; two probe_order waves; n009-n052 = 44 keys unprobed). Executed on
this host (`8c50fb9e...`, 2 cores, up to 4 workers), runner started
2026-11-22T11:48:32Z, stopped 2026-11-22T11:55:49Z. Every completed key is
2-pass fresh cold node-exact at budget 15,000,000:

- wave 1 (all LOSS): n001 6,471,615 / n002 3,083,301 / n003 4,560,719 /
  n004 3,710,926 nodes
- wave 2 (in-flight completion disclosed honestly, batch-5 f018
  precedent): n007 LOSS 2,905,330 / n008 LOSS 3,442,689 nodes;
  **n006 WIN (result 1, 2-pass node-exact, 3,695,373 nodes, key
  `[1152926194711134208, 128]`, legal 78, s5_index per batch-keys.json)**
  and **n005 WIN (result 1, 2-pass node-exact, 12,863,268 nodes, key
  `[1153489144664555520, 0]`, legal 82)**. First closure batch to surface
  two WIN rows, both in the same wave.
- no determinism mismatch (rc=42) and no budget exhaustion (result 0)
  anywhere; the runner stopped launching new waves after the rc=45
  WIN-HALT (in-flight wave members completed).

n005 and n006 are the **9th and 10th unconsumed closure WINs**
(b018/d002/e002/f017/g018/j033/h045/z003/n005/n006). Their verdicts are NOT
consumed on this lane: adoption remains with the scrutiny owner (C++
second-implementation gate precedent, pinned replica verdicts only
corroborated here). Batch record: 12 batches, 9 WIN-HALT + 3 clean
(23963/10324/8784 = 33rd/34th/35th Board-verified free classes).

Consequences recorded without interpretation: the two WINs are refutation
evidence against the all-LOSS closure route of class 8106 (the class status
itself remains UNKNOWN and derived only from the refresh machinery);
third-implementation cross-verification of n005/n006 and the if-adopted
decomposition (WIN-only / LOSS-only / full over the 8 probed rows) are open
items for future declarations. Next first-clean candidate in the renewed
ranking: **rank 11 class 16930** (`[1152921504875282432, 272]`, unknown 52;
nothing in flight, 10-WIN-key cross-check against its 52 worklist children
0 hits; final declaration-time fail-safes will be re-run before declaring).

Raws are published in chunk commits (`output/raw/n001..n008.p1/.p2.out`,
`output/status.log`, 15 lines). The standard 11x11 empty board, the 19
central-reply roots and class 8106 remain UNKNOWN throughout. Node counts
are not verdicts.
