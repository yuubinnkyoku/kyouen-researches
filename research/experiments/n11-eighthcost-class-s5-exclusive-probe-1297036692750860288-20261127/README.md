# n11-eighthcost-class-s5-exclusive-probe-1297036692750860288-20261127

Exclusive single-live-parent S5 probe batch for the eighth-cost candidate
class `1297036692750860288:0` (coverage {46, 52, 100, 108}), the adaptive-coordinator next
selection after the Part SZ canonical adoption closed the seventh-cost batch
(canonical head of record 5b6e77f7..., 6,874 rows WIN 202 / LOSS 6,672,
Part SZ reaudit census published). Declared in
`research/log/2026-11-27-n11-eighthcost-class1297036692750860288-exclusive-s5-probe-single-owner.md`
(wave A).

## Status

Selection and validation-gate stage published (2026-11-27). The ladder probe
(wave C raws) follows under the pre-registered stopping rules: per key a
2M-budget cold pair first; a key whose 2M pair resolves exact LOSS with
node-identical cold passes stops; a key whose 2M pair stays UNKNOWN
(result 0, nodes 2,000,000 both passes) escalates to a 15M-budget cold pair;
a key still UNKNOWN at 15M parks (L50M escalation candidate). The WIN
stopping rule applies: no new key is started after a key resolves WIN(1).
All rows are single-implementation (Node.js replica) results: a C++
second-implementation scrutiny gate and a third-implementation corroboration
are separate future Parts before any adoption (the seventh-cost precedent).
No verdict of this table may be consumed before the full batch audit, the
merged cache increment and the SHA-256 manifest are published by the closing
commit of this lane.

## Contents

- `scripts/select_eighth_exclusive.py`: fail-closed batch selector (fresh
  structural descendant of the published seventh-cost selector 581cb045...;
  freshness basis = the CURRENT canonical head 5b6e77f7 (Part SZ merged
  seventhcost42 cache); adds the seventh-42 claim set (seventh-cost-exclusive-
  keys.json pin c395fe03...) so the coordinator scan starts at rank 8;
  220 gates, deterministic 2x byte-identical).
- `scripts/jsreplay.js`: byte-clone of the pinned published Node.js replica
  (sha256 84585617...) of the standalone exact replay path of
  `cpp/solvers/kyouen_dfpn_root.cpp` at commit 154f3b7a.
- `input/k01..k43.input.csv`: per-key batch inputs (ascending truncated-cost
  proxy, then key).
- `input/val-gate/`: the published two-target-design validation rows
  (byte-clone of the seventh-cost kit val-gate inputs).
- `output/eighth-cost-exclusive-keys.json`: the authoritative machine list
  (schema n11-eighthcost-exclusive-selection-v1).
- `output/val-gate-summary.json` + `output/val-gate-raw/`: validation gate
  4/4 node-exact x2 on this execution host (Node.js v22.20.0).

## Selection summary (head basis, authoritative)

108 S5 children; 100 unknown under the head; 43 exclusive unknown children;
57 shared; proxy_exclusive_sum 233,896,005; bands 5,041,585 x5 / 5,234,938
x24 / 5,932,112 x14. The published probe-13-basis priority row (s5_unknown
101 / unknown_exclusive 41 / proxy_exclusive_sum 222,728,955) is retained
inside the selection JSON as the historical basis and is superseded by the
head-basis recomputation.

## Independent cross-check (same session, pre-publication)

A fresh reimplementation (selector source not used; live classes, unknown
children and exclusivity recomputed from the pinned geometry + head; ranking
from the published CCP table; all nine concurrent-lane claim sources
re-derived) reproduced the class, all 43 keys, the probe order, the bands,
the proxy sums and the disjointness gates exactly (CROSSCHECK-PASS).
Disclosed: both selector runs, the val-gate runs and this cross-check were
executed on this host before the wave A/B publication (publish-then-execute
covers the wave C ladder raws); the selector adaptation defect below was
caught by its own fail-closed pin gate before any selection output existed.

## Honest disclosures

- Selector adaptation defect: one string replacement corrupted the
  SEVENTHKEYS pin path (`eighth-cost-...` instead of `seventh-cost-...`);
  the selector's own fail-closed pin gate caught it (rc=1, no output
  written) and it was fixed before the first passing run.
- The canonical head basis (5b6e77f7, 6,874 rows) and all 16 pinned inputs
  were byte-verified against the published sha256 pins before the run;
  the two selector runs are byte-identical (stdout + keys JSON + all 43
  input CSVs).
- This lane runs without access to the user's computer (scheduled task);
  publication is via the GitHub API only.

## Guards

Selection and scheduling only; no verdict is claimed or implied. The
standard 11x11 empty board: UNKNOWN. All 19 central-reply roots: UNKNOWN.
Two-stone root {60,27}: UNKNOWN. Third-move pair {100,108}: UNKNOWN.
Every closure class: UNKNOWN unless a published Part says otherwise.
