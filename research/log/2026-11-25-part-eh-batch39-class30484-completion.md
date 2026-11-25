# Part EH: class 30484 batch-39 probe complete (2026-11-25)

Complement to the declaration `research/log/2026-11-25-part-eh-batch39-class30484-declaration.md`
(commit `20d17137`, observed HEAD `e8ff04e3`, opposing declarations 0).
Full protocol, kit pins and per-file hashes:
`research/experiments/n11-centralreply-closure-class30484-batch39-20261125/README.md`
and `MANIFEST-sha256.txt` in the same directory (178 published files).

## Outcome

- 50/50 fresh targets of class 30484 (rank 20 closure, mask
  `[1152922604135251968, 65536]`) probe-complete: **46 LOSS + 2 EXHAUSTED
  (aj030 / aj039) + 2 WIN (aj049 / aj050), 0 determinism mismatch**.
  Total nodes 177,032,132/pass (2-pass fresh-cold exact replay,
  budget 15,000,000, single drive39 invocation = 2 keys x 2 workers).
- aj030 / aj039 EXHAUSTED: budget-halt `15000000,0,15000000` node-exact on
  both passes; **honest UNKNOWN**, no same-condition re-probe permitted.
- aj049 WIN `15000000,1,4998452` / aj050 WIN `15000000,1,1871594` are
  node-exact across passes with pre-registered WIN-HALT markers; verdicts
  are **unconsumed** (adoption only via the scrutiny-owner C++ gate
  `9193f5b6...`; this environment has no C++ compiler).
- The 2 dual-class claim-reserved children (probe_order 585/586 =
  batch-38 ai044/ai048, Part EF in-flight) were NOT probed here;
  same-condition re-probe prohibition stands.

## Publish chain (all push-then-fetch-back byte-verified)

`20d17137` declaration -> `ecc3961b` kit scripts (maker
`425329c0`, runbatch `f591f8c2`, jsreplay `84585617`, drive39 `49ec1dd5`)
-> `0191cec1` sources (8, incl. canonical cache `fc3e4ac9`,
freshness-ranks13to20 `deea05b8`) -> `dc86a313` input (51,
batch-keys `5e25b550`) -> `49c985b1` val-gate (12 + 4 fresh
b39-host sidecars under `output/val-gate-host/`, node-exact vs published
baselines) -> increments `e68f25e4` / `0d9ad71b` / `988b9789` /
`b356d3b1` / `f1a42582` (aj001-aj040) -> `46dd06a7` inc6+inc7
(aj041-aj050 + final status.log `08d70bb7`, 54 lines) -> `0840a5d1`
machine audit (`audit_b39.py` + `batch-audit.json` `5a2b67cb`) ->
`4e2efd49` README + MANIFEST-sha256 -> this completion log.

Machine audit `audit_b39.py` (gates A1-A9): batch-keys pin, 10
source/script pin recompute, exact 100-raw set, replay field +
legal/lo/hi check, p1/p2 node-exactness, 54-line status.log
accountability, honest-label aggregation, 52-pair canonical-cache
absence (port of maker G4). 3x byte-identical output; tamper battery
8/8 fail-closed (A2/A3/A4/A5/A6/A7x2/A9) with control AUDIT-OK;
publish-then-execute re-run from a 115-file published-tree
reconstruction reproduced AUDIT-OK byte-identically.

## Honest-label accounting for class 30484 after this batch

52 unknown_now = 2 dual-class claim-reserved (Part EF ai044/ai048, their
verdicts belong to the EF lane) + 50 fresh probed here (46 LOSS honest
unconsumed, 2 EXHAUSTED honest UNKNOWN, 2 WIN honest unconsumed behind the
scrutiny gate). Class 30484 itself remains UNKNOWN: honest labels are not
merged verdicts. The 46 LOSS rows become adoptable raw for the next
adoption Part via the pinned merger `90711961` (BASE `fc3e4ac9`, 6,666
rows) with WIN/LOSS conflict checks against the canonical cache; any
adoption requires a fresh publication + declaration per house rules.

11x11 empty board: UNKNOWN - no outcome claim, no closure claim, no
coverage claim, nothing consumed. The standard 11x11 empty board, all 19
central-reply roots, the two-stone roots {49,60}/{59,60}, S2 {59,60} and
classes 1/2/4 remain UNKNOWN at every point.

## Resume notes (next runs)

1. Adoption Part candidate material: batch-39's 46 LOSS rows (this
   lane's raw is published and manifest-pinned), plus batch-38's
   published LOSS rows once the EF lane finishes its increments; merge
   via the pinned merger with declaration, never silently.
2. The 2 EXHAUSTED keys (aj030/aj039) stay honest UNKNOWN: re-probing
   them at the same conditions (15M, order=0, fresh-cold) is prohibited;
   only a materially different certified configuration (higher budget /
   different order policy) may re-ask them, as a new declared part.
3. WIN rows aj049/aj050: only the scrutiny-owner C++ gate `9193f5b6`
   may consume them; until then class 30484 cannot close even if every
   other child were adopted.
4. Next fresh frontier after class 30484 (post-adoption rescans will
   shift ranks): rank 22 class 23964 (fresh 51 + prior 1) and rank 24
   class 8811 (fresh 51 + prior 1) per the freshness scan in this kit;
   selecting them needs a fresh maker fork (worklist extract per class)
   and a new declaration, and must re-check latest main for concurrent
   lane claims (Part EF inc6/ai044-ai049 were still unpublished at this
   batch's drive time; do not touch EF-owned keys).
