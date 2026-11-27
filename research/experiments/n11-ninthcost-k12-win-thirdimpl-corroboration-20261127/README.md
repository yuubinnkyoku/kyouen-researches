# n11-ninthcost-k12-win-thirdimpl-corroboration-20261127

Third-implementation corroboration pillar for the ninth-cost k12 WIN row
(key `1297036692683751424:134217792`, legal 92, replica stage-2 15M WIN(1)
nodes 14,521,862, published ninth-cost kit raws, wave C7).

## Result: CORROBORATION-PASS (verdict-level)

- third_impl.js (pinned standing implementation, sha256 08ea958f...,
  byte-clone of the eighth-cost k01 corroboration kit copy) reported
  **result 1 (WIN)** for k12 in both fresh cold passes, expansions
  17,247,041 mutually identical (ttHits 9,122,930, quads 95670,
  memoPower 22, legal derived 92 = legalIn 92, reason clean, cap 400,000,000
  wallcap 260).
- Replica (jsreplay 84585617) had reported WIN(1) nodes 14,521,862, cold
  pair node-identical (published wave C7 raws).
- Verdict-level agreement: the third implementation agrees with the replica
  that k12 is WIN(1). Node and expansion counts are bookkeeping and are not
  expected to match across implementations.

## Honest disclosures

- A first pass pair at cap 15,000,000 ended runlimit:cap (result 0,
  expansions 15,000,001, disclosed INDET, not part of the corroboration);
  the cap was then raised to 400,000,000 as in the seventh-cost batch
  precedent and both cold passes resolved clean.
- A total of three clean passes were executed across the session (one
  exploratory + the published pair); all three are expansions-identical
  (17,247,041). Only the two published p1/p2 raws are the official pair.
- The node_rc=0 trailer line records the node process exit code captured
  directly by the shell in the same command (`echo "node_rc=$?"`).
- The wall_s field differs per pass (49.06 / 48.44); timing is not evidence.
- This is one of the two pillars required before any adoption of the k12
  WIN row. The C++ second-implementation scrutiny gate (Part SR/SW/SX
  pattern) remains pending.
- The verdict is NOT consumed: no cache increment, no class-status change,
  no coverage claim, no adoption.
- This lane runs without access to the user's computer (scheduled task);
  publication is via the GitHub API only.

## Files

- `scripts/third_impl.js`: byte-clone of the pinned third implementation.
- `output/raw/k12.p1.txt`, `output/raw/k12.p2.txt`: the two cold-pass raws.
- `MANIFEST-sha256.txt`: kit manifest.

## Guards

The standard 11x11 empty board: UNKNOWN. All 19 central-reply roots:
UNKNOWN. Two-stone root {60,27}: UNKNOWN. Third-move pair {100,108}:
UNKNOWN. Every closure class: UNKNOWN unless a published Part says
otherwise. A third-implementation WIN(1) agreement is not a class closure
claim, not a root verdict, and transfers nothing.
