# n11 tenth-cost batch stage-1 sweep (2M cold pairs) + interleaved 15M escalation

Wave B of the tenth-cost long-lane Part declared in
research/log/2026-11-27-n11-tenthcost-batch-stage1-sweep-declaration.md
(commit 8e60224f). Class 1297036692683751424:131072 (rank 10), 44
exclusive keys fresh to the canonical head 47280073... (6,887 rows WIN
206 / LOSS 6,681), selected by the published kit
n11-tenthcost-class-s5-exclusive-probe-20261127 (commit 1ab5d6e1,
selector output sha256 3d0f791e..., jsreplay byte-clone 84585617...).

## What ran (single implementation: Node.js replica jsreplay 84585617)

- Stage-1: all 44 keys k01..k44 at budget 2,000,000, one cold pair per
  key (88 runs). Result: 44/44 UNKNOWN (result 0, nodes 2,000,000,
  budget exhausted). All 88 pairs are node-identical; 32 of 44 pairs
  are byte-identical, the other 12 differ only in wall_s.
- Interleaved 15M escalation in key order with the standing
  WIN-stopping rule:
  - k01 (1297036692683751424:131074): 2M UNKNOWN pair -> 15M cold pair
    resolved exact-LOSS(2), nodes 6,783,438, pair byte-identical.
  - k02 (1297036692683751424:131136): 2M UNKNOWN pair -> 15M cold pair
    resolved WIN(1), nodes 8,799,140, pair node-identical (wall_s 46
    vs 44 only). WIN-stopping rule FIRED: no new key is started after
    k02 resolved WIN(1).
- k03..k44: escalation suppressed (42 keys). Their stage-1 2M cold
  pairs were completed after the k02 WIN as bookkeeping only, so the
  stage-1 enumeration is complete and comparable with the ninth-cost
  precedent (fully enumerated stage-1, suppression applies to
  escalation only).

## Machine cross-checks performed on this host before publication

- jsreplay.js and tenth-cost-exclusive-keys.json byte-verified against
  the published kit sha256 pins; all 44 input CSVs sha256-verified
  against the published kit MANIFEST-sha256.txt (44/44 OK).
- For every key: raw replay row cross-checked against the input CSV and
  the selector keys JSON (key_lo, key_hi, legal all identical); stage-1
  budget/result/nodes gated (2000000/0/2000000); cold-pair equality
  gated (byte or wall-only).
- Escalated rows gated: k01 (result 2, nodes 6783438) and k02
  (result 1, nodes 8799140) cold pairs result+nodes identical.

## Honest disclosures

- Ordering: the escalation ladder is interleaved per key (k01's 15M
  pair ran before k02's stage-1 pair), which matches the literal
  per-key reading of the wave A plan; the stage-1 completion for
  k03..k44 postdates the k02 WIN. No k03..k44 escalation was run.
- One pre-declaration k01 2M sanity run (result 0, nodes 2,000,000)
  was disclosed in the declaration.
- The sweep ran in foreground chunks of this execution environment
  (background processes do not survive between tool invocations);
  scripts-chunk.sh / scripts-stage1.sh document the exact commands.
- All rows are single-implementation. The k02 WIN(1) row requires the
  C++ second-implementation scrutiny gate (expected quadruple
  84,15000000,1,8799140) and the third-implementation corroboration
  before any adoption; a WIN-side flip-census review at adoption
  follows the ninth-cost k12/k02/k07 precedent. The k01 LOSS row
  likewise requires both pillars before adoption.

## Meaning and non-meaning

Scheduling bookkeeping only; no verdict is claimed or implied. The
standard 11x11 empty board: UNKNOWN. All 19 central-reply roots:
UNKNOWN. Two-stone root {60,27}: UNKNOWN. Third-move pair {100,108}:
UNKNOWN. Every closure class: UNKNOWN unless a published Part says
otherwise. Nodes and proxy values are never evidence of WIN or LOSS.
