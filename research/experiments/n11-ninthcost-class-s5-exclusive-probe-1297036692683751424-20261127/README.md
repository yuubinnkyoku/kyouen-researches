# n11-ninthcost-class-s5-exclusive-probe-1297036692683751424-20261127

Exclusive single-live-parent S5 probe batch for the ninth-cost candidate
class `1297036692683751424:134217728` (coverage {35, 41, 100, 108}), the
adaptive-coordinator next selection after the eighth-cost k01 WIN-row
canonical adoption closed the eighth-cost batch (canonical head of record
0935c94c..., 6,875 rows WIN 203 / LOSS 6,672; flip-census + reaudit refresh
published in n11-eighthcost-k01-win-adoption-reaudit-20261127). Declared in
`research/log/2026-11-27-n11-ninthcost-class1297036692683751424-exclusive-s5-probe-single-owner.md`
(wave A).

## Status

Selection complete; ladder NOT started. The 45 exclusive keys are declared
as the ninth-cost lane's claim; no key has been probed at any budget. All
rows in the future ladder will be single-implementation (Node.js replica);
per the k20/k33/k05/k01 precedent, a C++ second-implementation scrutiny gate
and a third-implementation corroboration are required before any adoption.

Under the CURRENT canonical head (0935c94c, 6,875 rows) there are 58 live
active classes (115 active; the head resolves one further class to
LOSS-stage - 1297036692683752448:0 - and the sixth/seventh/eighth-cost
serving classes to WIN-stage), 112 S5 children of the selected class, 99
unknown, 45 exclusive (single-live-parent) and 54 shared. The selected class
is rank 9 of the published class-closure-priority table; ranks 1-8 are the
eight lane-claimed classes.

## Contents

- `scripts/select_ninth_exclusive.py`: fail-closed batch selector (fresh
  structural descendant of the published eighth-cost selector ac896d94...;
  freshness basis = the CURRENT canonical head 0935c94c (eighth-cost k01
  merged cache); adds the eighth-43 claim set (eighth-cost-exclusive-keys
  pin 691dcd80...) so the coordinator scan starts at rank 9; 234 gates,
  deterministic 2x byte-identical).
- `scripts/crosscheck_ninth.py`: independent fresh-reimplementation
  cross-check (does not read the selector source; re-derives live classes,
  unknown children and exclusivity from the pinned geometry + head, the
  ranking from the published CCP table, and all eleven lane claim sources).
  CROSSCHECK-PASS, deterministic 2x.
- `scripts/jsreplay.js`: byte-clone of the pinned published Node.js replica
  (sha256 84585617...) of the standalone exact replay path of
  `cpp/solvers/kyouen_dfpn_root.cpp` at commit 154f3b7a.
- `input/k01..k45.input.csv`: per-key batch inputs (ascending truncated-cost
  proxy, then key); single-row inputs, cold pair = two invocations.
- `input/val-gate/`: the published two-target-design validation rows
  (byte-clone of the seventh/eighth-cost kit val-gate inputs).
- `output/ninth-cost-exclusive-keys.json`: the authoritative machine list
  (schema n11-ninthcost-exclusive-selection-v1).
- `output/crosscheck-summary.json`: cross-check record (schema
  n11-ninthcost-crosscheck-v1).
- `output/val-gate-summary.json` + `output/val-gate-raw/`: validation gate
  8/8 node-exact x2 on this execution host (Node.js v22.20.0).

## Selection summary (head basis, authoritative)

112 S5 children; 99 unknown under the head; 45 exclusive unknown children;
54 shared; proxy_exclusive_sum 247,541,283; bands 5,041,585 x3 /
5,234,938 x24 / 5,932,112 x18. The published probe-13-basis priority row
(s5_unknown 100 / unknown_exclusive 42 / proxy_exclusive_sum 229,744,947)
is retained inside the selection JSON as the historical basis and is
superseded by the head-basis recomputation. Concurrent claims respected
(11 lanes): focus-35, cert-38, third-39, fourth-41, fifth-44, sixth-43,
seventh-42, eighth-43, sbd-101, parked-2, parked-4; claim-union size 388,
disjoint from the 45 selected keys.

## Independent cross-check (same session, pre-publication)

A fresh reimplementation (selector source not used; live classes, unknown
children and exclusivity recomputed from the pinned geometry + head under
the stage rule - WIN if any child verdict is WIN, LOSS if all children are
LOSS, else UNKNOWN; ranking from the published CCP table; all eleven lane
claim sources re-derived) reproduced the class, all 45 keys, the probe
order, the bands, the proxy sums, the 58-live-class count, the head-basis
counts and all 45 input rows exactly (CROSSCHECK-PASS; deterministic 2x;
`output/crosscheck-summary.json`). Disclosed: the selector runs, the
cross-check and the val-gate runs all happened on this host before the
wave A/B publication; the future ladder (wave C) is the publish-then-execute
payload.

## Honest disclosures

- Selector adaptation defects (both caught before the first passing run):
  (1) a hand-transcribed EIGHTHKEYS pin sha256 typo (the true published
  eighth-cost-exclusive-keys.json sha is 691dcd807d52b9b9dbe0118f...), caught
  by comparing against the pinned file; the selector's own fail-closed pin
  gate would have refused the wrong pin. (2) a head_basis output-path field
  that pointed at a nonexistent `output/merged/` subdirectory; the actual
  published head cache is `output/merged-exact-s5-chain-plus-eighthcost-
  k01-20261127.cache`. No output existed before both were fixed.
- The canonical head basis (0935c94c, 6,875 rows WIN 203 / LOSS 6672) and all
  pinned inputs were byte-verified against the published sha256 pins before
  the runs; the two selector runs are byte-identical (stdout + keys JSON +
  all 45 input CSVs).
- This lane runs without access to the user's computer (scheduled task);
  publication is via the GitHub API only. Before each push the latest main
  is re-fetched; concurrent-lane conflicts are recorded, not forced.

## Guards

Selection and scheduling only; no verdict is claimed or implied. The
standard 11x11 empty board: UNKNOWN. All 19 central-reply roots: UNKNOWN.
Two-stone root {60,27}: UNKNOWN. Third-move pair {100,108}: UNKNOWN.
Every closure class: UNKNOWN unless a published Part says otherwise.
Nodes and proxy values are never evidence of WIN or LOSS.
