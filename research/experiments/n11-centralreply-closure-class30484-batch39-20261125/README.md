# n11 central-reply closure class 30484 batch-39: fresh 50-key probe (2026-11-25, Part EH)

Declared in
`research/log/2026-11-25-part-eh-batch39-class30484-declaration.md`
(observed HEAD `e8ff04e3`, opposing declarations 0; sibling lanes Part EF
batch-38 / Part EG third-impl were already in flight and were neither touched
nor re-probed).

Batch-39 of the central-reply 19-root closure grind (K0415/K0417 line).
The ranks-13..20 freshness scan (machine-verified in this kit) shows
ranks 13-19 all-children prior-probed (fresh 0), so the highest-ranked
closure class with clean (never-probed) unknown children available is
**class 30484** (rank 20, mask `[1152922604135251968, 65536]`,
unknown_now 52) in the refreshed closure table
(`refresh 01937f23` regen reproduced all four outputs byte-identically:
worklist `b4933810`, closure-classes `27e00b0d`,
refresh-summary `6af660a1`, per-root `6974299b`).

## Class accounting (machine-verified, no closure claim)

- 52 unknown_now = **2 dual-class claim-reserved** children + **50 clean
  fresh targets**. The claim-reserved pair (probe_order 585/586) is
  identical to two batch-38 targets of the in-flight Part EF drive
  (ai044 = 30345/30484 dual-class, legal 72;
  ai048 = 30345/30484 dual-class, legal 68); same-condition re-probe is
  prohibited, so batch-39 = the other 50 children
  aj001..aj050 (worklist probe_order 540..584, 587..591).
- Prior-probe universe `6deee846` (2,104 pairs), canonical cache
  `fc3e4ac9` (6,666 rows) and quarantine `81d23160` all exclude the
  50 targets (maker gates G4/G5/G7); `freshness-ranks13to20.csv`
  (`deea05b8`) pins the ranks-13..19 fresh-0 frontier.

## Protocol (publish-then-execute, single owner)

- kit: scripts 5 (`jsreplay.js` `84585617` + `runbatch.sh` `f591f8c2`
  byte-clones of the batch-37/38 kits; fail-closed maker
  `make_batch39_keys.py` `425329c0`; drive wrapper
  `drive39_local_step.sh` `49ec1dd5`; machine audit `audit_b39.py`),
  sources 8 (batch-38 packet keys `29807104`; canonical cache
  `fc3e4ac9`; closure-classes `27e00b0d`; freshness `deea05b8`;
  universe `6deee846`; quarantine `81d23160`; refresh-summary
  `6af660a1`; worklist-class30484-extract `feda8c72`, probe_order
  540..591, 52 rows), input 51 (50 target CSV +
  `batch-keys-b39.json` `5e25b550`), val-gate 12 (4 molecules x
  input/published-baseline byte-clones identical to the batch-37/38
  kit sha set) + 4 fresh host sidecars (published under
  `output/val-gate-host/`).
- maker gates G1-G7 (G1 pin layer incl. batch-38 keys, G2 b38
  claim-reserved provenance, G3 closure rank-20 anchor 52 = 2 + 50,
  G3b freshness ranks 13..19, G4 pair absence in canonical cache,
  G5 quarantine absence, G6 extract 52-row field match with 585/586
  reserved rows in place, G7 universe absence). Maker run 3x
  byte-identical; tamper battery 10/10 fail-closed + control PASS.
- val-gate: 4 fresh b39-host runs, node-exact on all replay fields vs
  the published baselines except wall_s (2M x2 EXHAUSTED-style
  budget-halt rows, 15M x2 LOSS rows).
- drive: 2-pass fresh-cold exact replay, budget 15,000,000,
  1 solver / row / process, single drive39 invocation
  (2 keys x 2 workers, 2-core host, ~200k nodes/s);
  increments inc1 `e68f25e4` (aj001-008) / inc2 `0d9ad71b` (aj009-016) /
  inc3 `988b9789` (aj017-024) / inc4 `b356d3b1` (aj025-032) /
  inc5 `f1a42582` (aj033-040) / inc6+inc7 `46dd06a7` (aj041-050 +
  final status); every pushed file fetch-back byte-verified.

## Results (honest labels; verdicts NOT consumed anywhere by this batch)

- **50/50 keys probe-complete**: **46 LOSS + 2 EXHAUSTED + 2 WIN +
  0 determinism mismatch**. Total nodes 177,032,132 per pass
  (p1 wall 1692s / p2 wall 1339s on 2 workers).
- aj030 / aj039 EXHAUSTED: 15,000,000-node budget halts on both
  passes, deterministic; honest UNKNOWN. No same-condition re-probe.
- aj049 WIN (1,871,594) / aj050 WIN (4,998,452): pre-registered
  WIN-HALT markers, 2-pass node-exact; the WIN verdicts are
  **unconsumed**: adoption only through the scrutiny-owner C++
  second-implementation gate (`9193f5b6...`), which this environment
  cannot run (no C++ compiler).
- status.log sha256 `08d70bb7` (50 PASS + 2 EXHAUSTED + 2 WIN-HALT,
  54 lines total);
  batch-audit.json (machine audit, sha256 `5a2b67cb`, schema
  `n11-centralreply-closure-batch39-audit-v1`) aggregates per-key
  (probe_order, budget, result, nodes, ts) with gates A1-A9:
  3x byte-identical, tamper battery 8/8 fail-closed
  (A2/A3/A4/A5/A6/A7x2/A9) and a publish-then-execute re-run from the
  published tree reproduction (115-file reconstruction, AUDIT-OK,
  identical output sha).

**No closure, coverage, secured-coverage, or root-outcome claim is made
anywhere in this batch. The standard 11x11 empty board, all 19
central-reply roots, the two-stone roots {49,60}/{59,60}, S2 {59,60},
classes 1/2/4, and class 30484 itself remain UNKNOWN at every point.
Nodes counts are bookkeeping, not outcomes or distances.**
