# 2026-11-26 n11 seventh-cost class 1306043891938492416:0 exclusive S5 probe — ladder checkpoint (41 LOSS / 1 parked / 0 WIN)

## Scope

Checkpoint record for the adaptive-coordinator seventh-cost selection and its
exclusive single-live-parent S5 probe batch for class `1306043891938492416:0`
(coverage {100, 103, 105, 108}), executed after the Part SV canonical adoption
closed the sixth-cost batch.

## Selection (head basis, authoritative)

- Fresh fail-closed selector `select_seventh_exclusive.py` (214 gates,
  deterministic, byte-reproducible on a fresh host). Freshness basis = the
  CURRENT canonical head
  `42dbb58ffe8dd02a81f4a92993d08e3fbebdaeb4b4f7bf33e142120ff055bdc4`
  (6,832 rows WIN 201 / LOSS 6,631), NOT probe-13 plus the third-cost
  increment. Consequence: 42 exclusive unknown keys (not the probe-13-basis
  41); one key is promoted because its parent class is already consumed under
  the head. The probe-13-basis priority row is retained inside the selection
  JSON as the historical basis and is superseded.
- Machine list: `output/seventh-cost-exclusive-keys.json`
  (schema n11-seventhcost-exclusive-selection-v1, sha256
  c395fe032f87ee6764ee24777b90140ca0eaa05002abe9038a7c67d6ca12e627).
- Replay implementation: byte-clone of the pinned published Node.js replica
  (jsreplay sha256 845856175d3c793a7eb4306f5902ecda3f1c046a8a53e8f34ed375e51febc3df).
- Validation gate: 4/4 node-exact against the published two-target-design rows.

## Results (pre-registered stopping rules)

- All 42 claimed keys executed. 41 keys resolved EXACT LOSS with cold
  two-pass node-identical determinism pairs (k16/k17 resolved at the 2M
  stage, nodes 1,228,696 / 1,831,284; the other 39 keys at the 15M stage,
  15M nodes sum 208,729,439 bookkeeping).
- 1 key parked UNKNOWN at 15M: k05 `1152921504607932416:536870912`
  (both cold runs 15,000,000 nodes, no row emitted). Candidate for a future
  L50M escalation; not a verdict.
- WIN stopping rule never fired (0 WIN rows).
- Machine summary: `output/batch-summary.json`
  (schema n11-seventhcost-batch-checkpoint-summary-v1, sha256
  6881eaaf48e900c96d8816017a5d052054d5ebbf4f0b3dc9e621df732ce01c2b).
  Raw manifest: `MANIFEST-raw-sha256.txt` (124 raw files).

## Verification state

- Single implementation only: every row is the Node.js replica (jsreplay
  84585617) cold two-pass on this execution host. The pinned C++
  second-implementation scrutiny gate (Part SR/SS pattern, gate-rows schema
  n11-seventhcost-...-rows-v1, 3 anchors + 41 targets) and a third-implementation
  corroboration are separate future Parts before any adoption (sixth-cost
  precedent).
- Verdicts NOT consumed: no cache increment, no class-status change, no
  coverage claim, no two-stone-root progress. Nothing in this batch may be
  read as a board outcome.
- All deliverables were published to GitHub before the two sandbox resets
  occurred; post-reset recovery used the published kit and raws, and the
  2M sweep was re-confirmed identical across three executions on two hosts
  (cross-host determinism).

## Publication chain

- wave A (declaration): 8d8c3c5c
- wave B (selection kit, 50 files): 2098c3ea
- wave C1 (2M sweep raws + k16/k17 pair): 928dc19b
- wave C2 (k01..k09 15M pairs): 64a46b4c
- wave C3 (k10..k42 pairs, batch-summary, raw manifest, README): 24f40b8b
- wave D (this checkpoint): this commit

Post-publication fetch-back verification: all 124 raw file blob SHAs and the
3 kit-root files (batch-summary.json, MANIFEST-raw-sha256.txt, README.md)
match the local computed blob SHAs byte-for-byte.

## Status guard

The standard 11x11 empty board: UNKNOWN. All 19 central-reply roots: UNKNOWN.
Two-stone root {60,27}: UNKNOWN. Third-move pair {100,108}: UNKNOWN. Every
closure class: UNKNOWN unless a published Part says otherwise. Nodes are
bookkeeping, never verdicts.
