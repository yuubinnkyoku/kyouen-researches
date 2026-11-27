# 2026-11-27 n11 eighth-cost class 1297036692750860288:0 probe checkpoint (k01 WIN, ladder stopped)

Checkpoint of the eighth-cost long-lane Part declared in wave A
(`research/log/2026-11-27-n11-eighthcost-class1297036692750860288-exclusive-s5-probe-single-owner.md`,
commit 8e76eaf6; kit wave B commit 16bd63ad, fetch-back 61/61 git blob sha
identical).

## Ladder outcome (single-implementation, NOT consumed)

- Stage-1 2M sweep: all 43 claimed keys ran the 2M cold pair; every pair
  UNKNOWN (result 0 / nodes 2,000,000, node-identical). 86 raws published in
  wave C1 (commit 60b76de9).
- 15M escalation: k01 (pos 1, key `1297036692750860288:64`, legal 84)
  resolved **WIN(1), nodes 8,514,427, cold pair node-identical** (both raw
  files byte-identical, sha256 3be9db9b... each). The pre-registered WIN
  stopping rule fired: no further key was officially started at any stage.
- Official tally: 1 resolved WIN row, 0 LOSS rows, 0 parked keys, 42 keys
  stopped at the 2M UNKNOWN pair with escalation suppressed.
- Machine summary `output/batch-summary.json` (schema
  n11-eighthcost-batch-checkpoint-summary-v1), raw manifest
  `MANIFEST-raw-sha256.txt` (88 official raws), kit README and kit
  MANIFEST updated in this wave.

## Honest disclosures

1. **Overreach execution (post-WIN k02 15M pair)**: the 15M escalation was
   batched two keys per shell command; k02 (pos 2, key
   `1297036692750868480:0`) therefore executed its 15M cold pair in the same
   command AFTER k01 had already resolved WIN(1). Observed values (NOT
   official, NOT published as a raw, host-local scratch only): UNKNOWN,
   nodes 15,000,000, pair identical. Officially k02 is stopped at its 2M
   UNKNOWN pair with the escalation suppressed; the batch summary carries
   this disclosure and the observed values so the record is complete.
2. The k01 WIN(1) row is single-implementation (Node.js replica jsreplay
   84585617, val-gate 4/4 node-exact on this host). Per the k20/k33/k05
   precedent it may NOT be adopted before a C++ second-implementation
   scrutiny gate and a third-implementation corroboration. No cache
   increment, no class-status change, no coverage claim was made.
3. The WIN-side reading of the batch is bookkeeping only: a WIN(1) S5 raw
   is not a class closure claim, not a root verdict, and transfers nothing.
4. This lane runs without access to the user's computer (scheduled task);
   publication is via the GitHub API only. Latest main was re-fetched before
   each push; no concurrent-lane conflict occurred in this window.

## Resume notes (next runs: re-fetch latest main first; hourly lanes run in parallel)

- The eighth-cost k01 WIN row is the pending corroboration target: the next
  Parts are (a) the C++ scrutiny gate for the k01 WIN quadruple
  (k01 = 84,15000000,1,8514427; Part SR/SW/SX pattern, gate-rows schema
  n11-eighthcost-...-rows-v1), then (b) a third-implementation
  corroboration, then (c) only if both agree, an adoption Part with the
  WIN/LOSS conflict review (BASE 5b6e77f7, fresh declaration; a WIN row
  triggers the win-hit class-status flip review exactly as in Part SZ
  wave E).
- The pre-audit ladder instrument (audit_seventh_ladder.py rev2 lineage)
  needs the eighth-cost batch-summary ledger pin plus WIN-stopping modeling
  for a 1-WIN batch where 42 keys never escalated; the overreach disclosure
  above is the input for that modeling.
- The 42 suppressed keys remain claimed by this lane's selection (class
  1297036692750860288:0 is WIN-side pending corroboration); the coordinator
  should not re-select them elsewhere until the k01 WIN is corroborated or
  refuted.

## Guards

The standard 11x11 empty board: UNKNOWN. All 19 central-reply roots:
UNKNOWN. Two-stone root {60,27}: UNKNOWN. Third-move pair {100,108}:
UNKNOWN. Every closure class: UNKNOWN unless a published Part says
otherwise. Nodes are bookkeeping, never verdicts.
