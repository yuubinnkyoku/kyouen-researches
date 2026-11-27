# 2026-11-27 n11 tenth-cost k01/k02 third-impl corroboration: wave A declaration

Single-owner declaration of the third-implementation corroboration
Part for the two resolved tenth-cost batch rows (published in kit
n11-tenthcost-batch-stage1-2m-20261127, commits b8049d8b / 3485348c).
Publish-then-execute: the raw passes below are the wave B payload.

## Targets and pre-registered verdicts (machine-derived from the published replica raws)

- k01 `1297036692683751424:131074` (legal 86): replica 15M cold pair
  exact-LOSS(2), nodes 6,783,438, pair byte-identical. Pre-registered
  third-impl expected result: 2 (LOSS).
- k02 `1297036692683751424:131136` (legal 84): replica 15M cold pair
  WIN(1), nodes 8,799,140, pair node-identical. Pre-registered
  third-impl expected result: 1 (WIN).

## Standing implementation and parameters

- third_impl.js, the pinned standing third implementation, sha256
  08ea958f... (byte-clone published in the ninth-cost corroboration
  kits), fetched from main and byte-verified on this host.
- Two fresh cold passes per key at cap 400,000,000, wallcap 260,
  memo-power 22 (ninth-cost k12 precedent: the 15M cap ends
  runlimit:cap INDET, so the cap is 400M from the start; no 15M
  passes will be run).
- Acceptance (verdict-level): per key, both passes report the
  pre-registered result with reason clean, mutually identical
  expansions, and legal derived == legal declared. Honest-negative
  rule: any disagreement is reported as CORROBORATION-FAIL and
  nothing is adopted.
- node_rc trailer: the shell captures the node exit code in the same
  command (`echo "node_rc=$?"`).

## Honest disclosures

- The stage-1/15M replica runs these keys corroborate were executed
  and published earlier this session by this same lane (declaration
  8e60224f, kit b8049d8b, completion 3485348c). The third
  implementation is independent of the replica code path (non-df-pn
  AND/OR minimax with completion-memo, canonical D4 keys).
- A single-implementation WIN row never adopts on its own; this Part
  plus the C++ second-implementation scrutiny gate (expected
  quadruples 86,15000000,2,6783438 for k01 and 84,15000000,1,8799140
  for k02, gate source 9193f5b6 @154f3b7a) are both required before
  any adoption Part; WIN-side flip-census review at adoption follows
  the ninth-cost precedent.
- This lane runs without access to the user's computer (scheduled
  task); publication is via the GitHub API only. Before each push the
  latest main is re-fetched; concurrent-lane conflicts are recorded,
  not forced.

## Guards

Corroboration bookkeeping only; no verdict is claimed or implied
beyond reporting what the third implementation outputs. The standard
11x11 empty board: UNKNOWN. All 19 central-reply roots: UNKNOWN.
Two-stone root {60,27}: UNKNOWN. Third-move pair {100,108}: UNKNOWN.
Every closure class: UNKNOWN unless a published Part says otherwise.
Expansions and nodes are never evidence of WIN or LOSS.
