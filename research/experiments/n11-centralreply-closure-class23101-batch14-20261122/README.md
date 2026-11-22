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


## Takeover (Part AQ, 2026-11-22)

The declaring host (Part AF) published the scaffold at 2026-11-22T12:26:47Z
(commit `54b7453d`) and never published a probe row or a status line. After
3h40m of silence, far beyond the 20-minute takeover criterion used for
batches 8/11, the remaining work was completed by the takeover host as
declared in Part AQ of the lane note (commit `398a96ae`, observed
HEAD-before-push `ede3eb42`). No declaring-host rows existed in any mirror,
so there was nothing to rescue; all 52 rows in this experiment were produced
by the takeover host.

Takeover-host verification re-run before the first row (all PASS):

- published scaffold 65 files byte-identical to the kit mirror
  (MANIFEST-sha256 cross-check); `scripts/jsreplay.js` sha256
  `845856175d3c793a7eb4306f5902ecda3f1c046a8a53e8f34ed375e51febc3df`
- fail-safes (1)-(6) of the Part AF declaration re-run on this host: 52/52
  keys absent from the then-canonical 6,027-row exact-S5 cache (sha256
  `95e868d6...`), quarantine cross-check 0 hits both directions,
  duplicate-free keys, closure-classes rank-12 row byte-agreement, 12
  unconsumed WIN keys 0 hits (lo/hi re-extracted from the published batch
  raws), probe_order 538-589 with class_unknown_now 52 on every worklist
  row and lo/hi/legal/s5_index agreement with batch-keys
- val-gate 4/4 node-exact fresh on this host: at2m twice result 0 /
  nodes 2,000,000; 15m result 2 / 3,651,923 and result 2 / 5,040,200
  (`output/val-gate/*.takeover-aq.out`; the wall_s diagnostic field is
  host-dependent and outside the gate)
- runner: per-key semantics identical to the declared `scripts/runbatch.sh`
  (2-pass fresh cold, budget 15M, mismatch HARD-STOP rc=42, WIN-HALT rc=45,
  in-flight wave members complete and are disclosed); the takeover wrapper
  `scripts/runwave-aq.sh` adds WAVE-START/WAVE-END logging and a
  `# replay_done` completeness guard that discards any truncated file
  (no truncation occurred on this host: all 84 raws carry the replay_done
  trailer; per-wave stdout logs are retained in the knowledge-kit mirror
  only and are not part of the publication)

Honest record: after the WIN-HALT, the full 52-key batch-key set was
re-checked against the new canonical 6,079-row exact-S5 cache published by
the parallel Part AP adoption reaudit (sha256 `342e8683...`): 0 hits (all
52 batch-14 keys remain outside the canonical cache, including the 42
probed rows and the WIN key q042).

## Result (Part AQ takeover: WIN-HALT at q042, verdict not consumed)

42/52 keys probed (probe_order 538-579), the batch halting under the
pre-registered WIN-HALT rule at the first WIN:

- **q042: result 1 (WIN), 9,149,084 nodes, 2-pass fresh-cold node-exact**
  (s5_index 745184, key `[1152921505747697664, 1032]`, legal 85,
  probe_order 579)
- same-wave in-flight q039/q040/q041 completed and disclosed: result 2 LOSS
  (2-pass node-exact)
- 41 LOSS rows total (all 2-pass node-exact); budget-exhausted rows 0;
  determinism mismatches 0; total 88,338,850 nodes per pass
- q043-q052 (10 keys) not started (halt rule)
- machine row audit `output/row-audit.json` (schema
  `n11-centralreply-closure-class23101-batch14-rowaudit-takeover-v1`,
  sha256 `cc22a1c8...`): every row re-checked for p1/p2
  (budget,result,nodes) equality, legal and key agreement with
  batch-keys.json, probe_order contiguity, the 95,670 forbidden-quadruple
  gate in both passes, replay_done completeness, and status.log
  cross-agreement; problems list empty

Interpretation guards (unchanged): the WIN is not consumed by this lane;
q042 joins the unconsumed closure WIN set as the 15th member
(b018/d002/e002/f017/g018/j033/h045/z003/n005/n006/p002/p003/r001/r002/q042),
adoption pending with the scrutiny owner (C++ second implementation gate
pin `9193f5b6...`). The all-52-children-LOSS closure route for class 23101
is refuted by a verified WIN child (verdict-level claim about this route
only, not a game-theoretic value). Batch tally: 15 batches to date:
12 WIN-HALT + 3 clean (23963/10324/8784, the 33rd/34th/35th Board-verified
free classes; class 10687 became closure-qualified during this takeover via
the parallel Part AP, outside this experiment's scope). The standard 11x11
empty board, the 19 central-reply roots, class 23101 and its S5 children
remain UNKNOWN throughout; nodes are not verdicts and the batch selection
is a scheduling quantity.
