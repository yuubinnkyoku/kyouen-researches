# seventh-cost k05 L50M escalation completion (2026-11-27)

Lane: long-term lane (11x11), autonomous session; the user's PC was
unreachable this session (GitHub API publishing only). Declaration
`research/log/2026-11-27-n11-seventhcost-k05-l50m-escalation-single-owner.md`
(commit e89e80aa) pre-registered this Part as publish-then-execute; no
concurrent lane pushed anything between the declaration and this completion.

## Result

k05 `1152921504607932416:536870912` (legal 90) is **resolved exact WIN(1) at
the 50,000,000-node stage, with a byte-identical cold determinism pair**:

- `output/raw/at50m-run1-k05.out.csv` and `at50m-run2-k05.out.csv`
  (both sha256 ff750cc63e3ead314a5c5a22b09cca5588f284a34dc08c5c4d1cc5716eda342c,
  byte-identical incl. wall_s=87 on this host):
  `replay,0,5,90,0,50000000,1,15763505,87,1152921504607932416,536870912`.

This is the **first WIN row of the seventh-cost batch** (previous checkpoint:
41 LOSS, 1 parked, 0 WIN). The batch is now 41 exact LOSS + 1 exact WIN, 0
parked - as raw rows only. Stage policy was satisfied: k05 had a published 2M
UNKNOWN and a published 15M UNKNOWN cold pair (nodes 15,000,000 both) before
this 50M stage. Host validation before the declaration: the published val-gate
reproduced 4/4 node-exact (2M x2 result 0 / nodes 2000000; 15M x2 result 2 /
nodes 3651923 and 5040200); jsreplay sha256 84585617... byte-verified;
k05 input sha256 a73a6c70... byte-verified (git blob db9a2753).

Nodes are bookkeeping only. Verdict NOT consumed: this is a
single-implementation (Node.js replica) result. Following the sixth-cost
precedent (k20/k33), a WIN row requires the pinned C++
second-implementation scrutiny gate and a third-implementation
corroboration before any canonical adoption Part; both remain open future
Parts, together with the C++ gate for the 41 LOSS rows.

## Pre-registered instrument interaction (disclosed, scratch run)

The published pre-audit instrument
(`n11-seventhcost-ladder-preaudit-20261126/scripts/audit_seventh_ladder.py`,
sha256 89e816dc...) was run on a scratch checkout BEFORE this push:

- clean control (124 published raws): rc=0, 8,699 gates, checkpoint=full,
  41 resolved / parked [5] / 0 WIN - byte-equivalent to the published first
  real run;
- with the two new at50m raws added (126 raws): **rc=0, 8,729 gates, all
  PASS** (per-file schema/provenance/budget/stage-order gates for the new
  rows all pass; the stage-order gate correctly sees the 2M UNKNOWN
  prerequisite).

Two honest findings for the instrument's owner lane (this lane did NOT
modify the instrument):

1. The instrument does not yet model 50M-stage resolution: at50m rows do not
   feed the resolved/parked/win bookkeeping, so it still reports k05 as
   parked at 15M and 0 WIN. No false failure occurs (fail-closed integrity is
   intact), but the coverage report is now incomplete until an
   escalation-aware revision adds a pair_50m determinism gate and 50M
   resolved/parked paths.
2. If such a revision naively maps the 50M WIN into `resolved`, the existing
   WIN stopping rule ("no raws beyond the first WIN key") would fail against
   the already-published k06..k42 raws. Those raws were published at the
   15M checkpoint BEFORE k05's WIN was known (the escalation is
   temporally later), so the rule needs an escalation-aware, temporal-order
   formulation rather than a pure key-order one.

## Honest disclosure

- Both 50M runs and the val-gate ran on this lane's host (vibe upgraded
  sandbox, Node.js v22.20.0); wall_s is host-specific and is not evidence.
- The 15M stage of k05 consumed the full budget twice (nodes 15,000,000 x2,
  UNKNOWN); the WIN(1) appears only at 50M with nodes 15,763,505 - i.e. the
  resolution is deeper than 15M but well inside the 50M budget.
- No cache increment, no manifest edit, no batch-summary edit was made by
  this lane: the owner lane's MANIFEST-raw-sha256.txt and batch-summary.json
  still describe the 15M checkpoint; integrating the two new raws into those
  bookkeeping files is the owner lane's integration step (this log is the
  record of the raws themselves).

## Status guard

Nothing here claims, implies or consumes any verdict. The standard 11x11
empty board: UNKNOWN. All 19 central-reply roots: UNKNOWN. Two-stone root
{60,27}: UNKNOWN. Third-move pair {100,108}: UNKNOWN. Every closure class:
UNKNOWN unless a published Part says otherwise. A WIN raw row is not a
class verdict and transfers nothing to any root.
