# n11 central-reply closure class 16930 exact-S5 probe batch 13 (2026-11-22)

Batch 13 of the central-reply 19-root closure grind (K0415/K0417 line). Declared
as **Part AE** amendment of
`research/log/2026-11-22-n11-centralreply-19root-refresh-closure-batch1-single-owner-note.md`.

Context: batch 12 (class 8106, Part AC) WIN-HALTED at n006/n005 (9th and 10th
unconsumed closure WINs; third-implementation cross-verification of the 8
probed rows is declared by another owner as Part AD and is NOT touched by this
batch). Batch record: 12 batches, 9 WIN-HALT + 3 clean (23963/10324/8784, the
33rd/34th/35th Board-verified free classes).

Selection: under the pre-registered rule (first clean candidate = neither in
flight nor WIN-halted, no refutation evidence), renewed closure ranks 1-9 all
carry refutation evidence (16757: b018, 20421: d002, 30345: b018 cost child
s5 528497, 16371: e002, 12264: f017, 5473: g018, 2634: h045, 8785: z003,
1518: j033) and rank 10 (8106) WIN-HALTed in Part AC, so the first clean
candidate is **renewed rank 11 class 16930** (mask
`[1152921504875282432, 272]`, unknown 52, first 26 / third 70, 3 groups
served; all 52 still-unknown canonical S5 children sit in the closure group
first=26/third=70). Batch selection is a scheduling quantity and never a
verdict.

## Protocol

- keys: `input/batch-keys.json` (52 keys p001-p052, sha256
  `c6c56a1a0552b8a87d1e1f5f9e0d6c3955cf1f58a85ef6726317d17846a0a2c7`,
  inputs `input/p001..p052.input.csv`); the keys, legal counts and ordering
  are the Part Y re-audit probe-worklist rows `serving_class=16930`
  (probe_order 486-537 of the 65,154-row worklist, sha256
  `1807e4d21f6fb757ea21850c6bda4d822cb76ac59abfa9bcd1cc7b53bd7055ef`).
  The worklist is regenerable and not republished; the 52 class rows are
  published here in full via batch-keys.json, so the selection is
  independently checkable against the canonical cache and the update8
  machinery. Key prefix note: `p` skips the batch 1-12 prefixes
  (b/c/d/e/f/g/h/j/m/z/n) and the third-implementation anchor ids (k02a/l1a);
  the prefix is bookkeeping only.
- worklist re-derivation: the declaring session reuses the Part Y regeneration
  already re-verified in this workspace lineage (pinned inputs 6 re-fetched
  byte-exact from the repo canonical copies, published Part Y scenario script
  `refresh_19root_frontier.py` sha256 `88671526...` run twice: all outputs
  byte-identical, cross-host byte-equal to the published Part Y canonical
  outputs; documented in the batch-12 Part AC scaffold README). This session
  re-verified: worklist run1 == run2 (both sha256 `1807e4d2...`) and
  closure-classes.csv / per-root-coverage.csv / refresh-summary.json
  byte-equal to the published canonical copies on main (checked at commit
  `7eb9ab70`).
- fail-safe machine checks done before declaring: (1) all 52 keys absent
  from the canonical merged cache (6,027 data rows, sha256 `95e868d6...`,
  52/52 misses, 0 hits); (2) quarantine registry (sha256 `81d23160...`, 2
  active entries) key-pair cross-check 0 hits, both directions; (3) the 52
  keys are duplicate free; (4) the renewed closure-classes.csv rank 11 row
  matches class 16930 (mask `[1152921504875282432, 272]`, unknown 52, first
  26 / third 70, groups 3) byte-against the published Part Y output; (5) none
  of the ten unconsumed WIN keys
  (b018/d002/e002/f017/g018/j033/h045/z003/n005/n006) is among the 52 unknown
  children of class 16930 (cost-child cross-check, 0 hits); (6) probe_order
  contiguity 486-537 with class_unknown_now = 52 on every row.
- solver: pinned replica `scripts/jsreplay.js` (sha256
  `845856175d3c793a7eb4306f5902ecda3f1c046a8a53e8f34ed375e51febc3df`),
  identical bytes to batches 1-12
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

Result section below (this README was amended after the batch stop; per-row
honest records land in `output/status.log` and `output/raw/`). The standard
11x11 empty board, the 19 central-reply roots and class 16930 remain UNKNOWN
throughout. Nodes are not verdicts.

## Result (2026-11-22, amending this README after batch stop)

Batch halted under the pre-registered WIN-HALT rule at **4/52 probed**
(p001-p004; one probe_order wave; p005-p052 = 48 keys unprobed). Executed on
this host (`8c50fb9e...`, 2 cores, up to 4 workers), runner started
2026-11-22T12:16:52Z, stopped 2026-11-22T12:21:20Z. Every completed key is
2-pass fresh cold node-exact at budget 15,000,000:

- wave 1 (in-flight completion disclosed honestly, batch-5 f018 precedent;
  the WIN-HALT fired on p003 first and p002 completed in flight):
  **p003 WIN (result 1, 2-pass node-exact, 7,489,274 nodes, key
  `[3458764514088976384, 272]`, legal 81, s5_index 203419, probe_order 488)**
  and **p002 WIN (result 1, 2-pass node-exact, 10,770,254 nodes, key
  `[1153484454828703744, 272]`, legal 85, s5_index 185003, probe_order 487)**;
  p001 LOSS 4,631,275 nodes / p004 LOSS 2,291,059 nodes. Second closure
  batch in a row to surface two WIN rows in the same wave.
- no determinism mismatch (rc=42) and no budget exhaustion (result 0)
  anywhere; the runner stopped launching new waves after the rc=45
  WIN-HALT (in-flight wave members completed).

p002 and p003 are the **11th and 12th unconsumed closure WINs**
(b018/d002/e002/f017/g018/j033/h045/z003/n005/n006/p002/p003). Their
verdicts are NOT consumed on this lane: adoption remains with the scrutiny
owner (C++ second-implementation gate precedent, pinned replica verdicts
only corroborate the batch record). Batch record: 13 batches, 11 WIN-HALT +
3 clean (23963/10324/8784, the 33rd/34th/35th Board-verified free classes).

Consequences recorded without interpretation: the two WINs are refutation
evidence against the all-LOSS closure route of class 16930 (the class status
itself remains UNKNOWN and derived only from the refresh machinery);
third-implementation cross-verification of p002/p003 (plus the 2 LOSS rows)
and the if-adopted decomposition are open items for future declarations.
Next first-clean candidate in the renewed ranking: rank 12 class 23101
(`[1152921504892059648, 16]`, unknown 52; final declaration-time fail-safes
will be re-run before declaring).

Raws are published in a chunk commit (`output/raw/p001..p004.p1/.p2.out`,
`output/status.log`). The standard 11x11 empty board, the 19 central-reply
roots and class 16930 remain UNKNOWN throughout. Node counts are not
verdicts.
