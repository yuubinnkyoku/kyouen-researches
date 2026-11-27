# 2026-11-27 n11 tenth-cost batch stage-1 sweep completion

Wave C completion log of the tenth-cost batch declared in
research/log/2026-11-27-n11-tenthcost-batch-stage1-sweep-declaration.md
(commit 8e60224f, pinned to HEAD e61acf82). Kit published in commit
b8049d8b (research/experiments/n11-tenthcost-batch-stage1-2m-20261127/,
97 files, fetch-back 97/97 byte-identical via raw CDN pinned to the
publishing commit).

## Results (single implementation: Node.js replica jsreplay 84585617)

- Stage-1 2M sweep: all 44 exclusive keys of class
  1297036692683751424:131072 UNKNOWN at budget 2,000,000 (result 0 /
  nodes 2,000,000, budget exhausted). 88 cold runs; every pair
  node-identical; 32 of 44 pairs byte-identical, 12 differ only in
  wall_s.
- Interleaved 15M escalation in key order, WIN-stopping rule active:
  - k01 (1297036692683751424:131074): exact-LOSS(2), nodes 6,783,438,
    cold pair byte-identical.
  - k02 (1297036692683751424:131136): WIN(1), nodes 8,799,140, cold
    pair node-identical (wall_s 46 vs 44 only). WIN-stopping rule
    FIRED at k02.
  - k03..k44 (42 keys): escalation suppressed by the rule. Their 2M
    stage-1 pairs were completed after the k02 WIN, as bookkeeping
    only, so the stage-1 enumeration is complete (44/44) and
    comparable with the ninth-cost precedent.
- Resolved this batch: 1 LOSS row (k01) + 1 WIN row (k02), both
  single-implementation, both adoption-blocked pending the C++
  second-implementation scrutiny gate and the third-implementation
  corroboration pillars. A WIN-side flip-census review at adoption
  follows the ninth-cost k12/k02/k07 precedent.

## Machine verification performed before publication

- jsreplay.js (84585617...), selector output keys JSON (3d0f791e...)
  and all 44 input CSVs byte/sha256-verified against the published
  selection kit (commit 1ab5d6e1) on this host.
- Per-key raw replay rows cross-checked against input CSV and selector
  keys (key_lo, key_hi, legal identical); stage-1 budget/result/nodes
  gated; cold-pair equality gated (byte or wall-only).
- Escalated rows gated (result+nodes pair-identical).
- MANIFEST-sha256.txt (96 entries, sha256sum -c compatible) verified
  ALL-OK locally before publication; fetch-back after publication
  97/97 byte-identical.

## Honest disclosures

- Ordering: escalation is interleaved per key (k01's 15M pair ran
  before k02's stage-1 pair), matching the literal per-key reading of
  the wave A plan; the stage-1 completion for k03..k44 postdates the
  k02 WIN (no k03..k44 escalation was run). Disclosed in the kit
  README and batch-summary.json ordering_disclosure.
- One pre-declaration k01 2M sanity run (result 0, nodes 2,000,000)
  was disclosed in the wave A declaration; it is reproduced exactly
  by the official at2m-k01-p1/p2 raws.
- Harness note: background processes do not survive between tool
  invocations in this execution environment, so the sweep ran in
  foreground chunks (scripts-chunk.sh / scripts-stage1.sh in the kit
  document the exact commands; a first nohup attempt died silently and
  produced no official raw).
- No concurrent-lane conflict was observed: main HEAD was 8e60224f
  (this lane's declaration) immediately before the kit push.

## Guards

Scheduling bookkeeping only; no verdict is claimed or implied. The
standard 11x11 empty board: UNKNOWN. All 19 central-reply roots:
UNKNOWN. Two-stone root {60,27}: UNKNOWN. Third-move pair {100,108}:
UNKNOWN. Every closure class: UNKNOWN unless a published Part says
otherwise. Nodes and proxy values are never evidence of WIN or LOSS.
