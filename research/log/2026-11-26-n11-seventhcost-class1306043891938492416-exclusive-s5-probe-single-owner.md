# n11 seventh-cost class exclusive S5 probe: single-owner declaration (2026-11-26)

The Part SV completion log closed the sixth-cost exclusive S5 batch
(standing_unconsumed_parked_keys = 0, canonical head of record
42dbb58ffe8dd02a81f4a92993d08e3fbebdaeb4b4f7bf33e142120ff055bdc4, 6,832 rows
WIN 201 / LOSS 6,631) and returned the lane to the adaptive coordinator for
the next certificate/probe selection. This lane executes that selection.

## Selection (fail-closed, all gates machine-checked)

- Selector: `scripts/select_seventh_exclusive.py` (sha256 581cb045ff67d04219d13ee073c9b328fe78d47130e184e51e125759a719f620), a fresh
  implementation of the published sixth-cost selector structure with the
  canonical head of record as the freshness basis (disclosed difference: the
  sixth selector cross-checked probe-13 + the then-latest third-cost
  increment; this selector recomputes live classes, unknown children and
  exclusivity against the CURRENT head 42dbb58f, which supersedes both).
- Output: `output/seventh-cost-exclusive-keys.json` (sha256 c395fe032f87ee6764ee24777b90140ca0eaa05002abe9038a7c67d6ca12e627, schema
  n11-seventhcost-exclusive-selection-v1), 214 gates PASS, selector
  deterministic across two runs.
- Selected class: `1306043891938492416:0` (coverage {100, 103, 105, 108}),
  the next unclaimed rank (rank 7) of the published class-closure-priority
  proxy_total ordering after the six claimed classes (focus-35
  1188950301626859520:536870912, cert-38 1297036692683752448:0, third-39
  1297036830122704896:0, fourth-41 1297107061427929088:0, fifth-44
  1152921504612089856:536870912, sixth-43 10376293541461626880:65536).
- Head-basis measurements (authoritative): 108 S5 children, 100 unknown
  under the head, 42 exclusive (single-live-parent) unknown children,
  58 shared; proxy_exclusive_sum 226,065,724; bands 5,041,585 x4 /
  5,234,938 x28 / 5,932,112 x10. The published probe-13-basis priority row
  (s5_unknown 101 / unknown_exclusive 41) is recorded inside the selection
  JSON as the historical basis and is NOT the selection basis; the head-basis
  recomputation supersedes it (one key that was shared at probe-13 time has
  become exclusive because another of its live parents is no longer a live
  class under the head).
- Disjointness: the 42 selected keys are disjoint from all machine-read
  concurrent-lane claim sets (focus_35, cert_38, third_39, fourth_41,
  fifth_44, sbd_101, parked_2, parked_4, sixth_43), absent from the canonical
  head, and absent from the active quarantine registry. Every selected key:
  5 stones, D4-canonical, safe (no forbidden quadruple), independent
  integer-geometry legal count equals the supply ledger.
- Validation gate: the pinned Node.js replica (jsreplay.js sha256
  845856175d3c793a7eb4306f5902ecda3f1c046a8a53e8f34ed375e51febc3df,
  byte-clone of the published sixth-cost replica) reproduces all four
  published two-target-design replay rows exactly on this execution host
  (at2m x2: result 0 / nodes 2,000,000; 15M x2: result 2 / nodes 3,651,923
  and 5,040,200), see output/val-gate-summary.json (sha256 d9c0203a2cb7a6d82ac59f4c6d49062b93ad824819cbb67ef622c60854588960).

## Pre-registered stopping rules (identical to the sixth-cost lane)

1. The ladder runs the claimed keys k01..k42 in ascending (proxy, key)
   order. Stage 1 is a fresh cold 2,000,000-budget replay per key.
2. A key that resolves at the 2M stage gets a second independent cold 2M
   run; identical (result, nodes) records the key resolved (determinism
   pair).
3. A key UNKNOWN at 2M proceeds to a 15,000,000-budget cold pair (run1,
   run2). LOSS/LOSS with identical (result, nodes) records the key
   resolved; UNKNOWN/UNKNOWN parks the key (both runs recorded, no cache
   row) and the ladder continues.
4. Any WIN at any stage stops further claimed-key starts in this session
   (WIN stopping rule); the witness rows are published and no further
   claimed key is started. Verdicts are NOT consumed by this lane: no cache
   increment, no class-status change, no coverage claim.
5. Raw rows are pushed incrementally as checkpoints; no verdict of this
   table may be consumed before a full batch audit, a merged cache increment
   and a SHA-256 manifest are published.

## Status guard

This is selection and scheduling only. No verdict is claimed or implied;
nodes and proxy values are never evidence of WIN or LOSS. The standard 11x11
empty board: UNKNOWN. All 19 central-reply roots: UNKNOWN. Two-stone root
{60,27}: UNKNOWN. Third-move pair {100,108}: UNKNOWN. Every closure class:
UNKNOWN unless a published Part says otherwise.
