# 2026-11-27 n11 ninth-cost parked-3 L50M escalation: single-owner declaration (wave A)

## Claim

This lane claims the L50M (budget 50,000,000) escalation of the three
ninth-cost parked keys k02 / k04 / k07 of the batch declared in
`research/log/2026-11-27-n11-ninthcost-class1297036692683751424-exclusive-s5-probe-single-owner.md`
and closed at 15M in `output/batch-summary-15m.json` (schema
n11-ninthcost-batch-checkpoint-summary-v1, commit 7332d958) of the kit
`research/experiments/n11-ninthcost-class-s5-exclusive-probe-1297036692683751424-20261127/`.

Publish-then-execute: this declaration is pushed before any 50M run starts
on this host. No 50M invocation of k02/k04/k07 has been made by this lane
before this push. Pre-declaration host sanity runs (disclosed below) used
already-published budgets only.

## Targets (parked UNKNOWN@15M, official status before this wave)

| key | s5 state (lo,hi) | legal | 15M status |
| --- | --- | --- | --- |
| k02 | 1297036692683751424, 201326592 | 87 | UNKNOWN, nodes 15,000,000 (pair identical) |
| k04 | 1152921504607903744, 536903680 | 98 | UNKNOWN, nodes 15,000,000 (pair identical) |
| k07 | 1152923703765368832, 68719476736 | 96 | UNKNOWN, nodes 15,000,000 (pair identical) |

## Pre-registered execution policy

- Engine: the published Node.js replica `scripts/jsreplay.js` (sha256
  845856175d3c793a7eb4306f5902ecda3f1c046a8a53e8f34ed375e51febc3df),
  byte-verified against the kit MANIFEST-sha256.txt before this declaration.
- Inputs: `input/k02.input.csv` (8c2a0438...), `input/k04.input.csv`
  (dc3bfeb4...), `input/k07.input.csv` (928a1b98...), each byte-verified
  against the kit MANIFEST-sha256.txt.
- Per key: two cold invocations (run1, run2, fresh solver each) at
  `--exact-replay-budget=50000000`. Both runs are executed regardless of
  the run1 outcome (all three keys are pre-declared targets of this wave;
  the seventh-cost k05 L50M and sixth-cost parked-4 precedents).
- Key order: ascending truncated-cost proxy order k02, k04, k07 (the
  batch order). No stopping rule: the wave-C WIN stopping rule does not
  apply to parked rows (they were parked before the k12 WIN determination;
  k02 precedent of the eighth-cost batch).
- Acceptance per key: result 1 (WIN) or result 2 (LOSS) with
  pair-node-identical runs => resolved row (single-implementation,
  adoption-gated); result 0 with nodes 50,000,000 in both runs =>
  parked UNKNOWN@50M.
- Honest-negative rule: any discarded/failed pass is disclosed, not
  silently rerun.

## Freshness basis

Canonical head of record at declaration time: 0935c94c... (6,875 rows WIN
203 / LOSS 6,672, `merged-exact-s5-chain-plus-eighthcost-k01-20261127.cache`,
287,808 bytes), byte-verified (sha256 match) after fetching at commit
7e6943e3. Machine-checked: all three (lo,hi) pairs are ABSENT from the head
cache (3/3). No ninth-cost adoption Part has been published on main (HEAD
at push time 03487c4b, commit list machine-checked), so the head basis of
the batch is still the current head.

## Disclosed pre-declaration host sanity runs (published budgets only)

- k02 @2M: result 0, nodes 2,000,000, forbidden quadruples 95,670 - node-exact
  vs the published at2m raw.
- k02 @15M: result 0, nodes 15,000,000 - node-exact vs the published
  `at15m-run1/k02.out.csv` raw (wall_s differs; wall is bookkeeping).

No other runs of these keys were made by this lane before this declaration.

## Guards

Verdict NOT consumed. Any WIN(1)/LOSS(2) rows produced by this wave are
single-implementation cache-bookkeeping rows only: they transfer nothing to
any root or class verdict. Per the k20/k33/k05/k01 precedent, a resolved row
from this wave requires a C++ second-implementation scrutiny gate and a
third-implementation corroboration before any adoption Part. Standard 11x11
empty board: UNKNOWN. All 19 central-reply roots: UNKNOWN. Two-stone root
{60,27}: UNKNOWN. Third-move pair {100,108}: UNKNOWN. Every closure class:
UNKNOWN unless a published Part says otherwise. Nodes are never evidence of
WIN or LOSS. This lane runs without access to the user's computer (scheduled
task); publication is via the GitHub API only; the latest main is re-fetched
before each push and concurrent-lane conflicts are recorded, not forced.
