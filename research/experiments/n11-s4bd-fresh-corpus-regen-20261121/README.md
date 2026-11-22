# n11-s4bd-fresh-corpus-regen-20261121 (checkpoint state: pass 1 in progress)

Fresh, chain-native regeneration of the decided-class corpus for
S4 `(1297036692683752448,0)` (plus the 2 unclaimed backward-only rows),
declared in
`research/log/2026-11-21-n11-sbd-fresh-corpus-regen-single-owner-note.md`
(single-owner declaration, HEAD at declaration `904e7b40b2f8...`, corrected at
commit `29857713052c`).

Status at this checkpoint commit:
- Validation gate 4/4 reproduced on this execution host (see `output/val/`):
  the pinned Node.js replica reproduces all four published two-target-design
  replay rows exactly (at2m x2: result 0 / nodes 2,000,000 / legal 98,99;
  15M x2: result 2 / nodes 3,651,923 and 5,040,200 / legal 98,99).
- Pass 1 (fresh 15M-budget replays): the keys pushed so far are in
  `output/raw/*.p1.out`. Pass 2 (determinism gate) has NOT run yet for most
  keys. No verdict of this table may be consumed before the full two-pass
  merge manifest (`output/merge-manifest.json`), the frontier audit and the
  root-loss audit are published by the final commit of this lane.
- Expected final state (if all gates pass): 100 of the 101 declared S5 keys
  settle exact LOSS (the 99 corpus keys carry canonical children of the S4;
  the 2 unclaimed rows settle LOSS; TARGET_S5
  `(1152921504607899649,536870912)` is budget-exhausted UNKNOWN at 15M, so its
  row is derived LOSS (nodes=0) from the fresh S6 witness
  `(1152921504675009536,536870912)` re-execution, Oct 12 precedent), the S4
  class closes LOSS on the 106-child boundary, third-move coverage becomes
  119/119 and the root {60,27} LOSS certificate is regenerated for the live
  chain lineage. The empty 11x11 board is NOT solved by this lane and remains
  UNKNOWN.

Inputs and recipes:
- `input/corpus-def.json`: machine-checkable corpus definition (frozen
  geometry children, probe-13 chain keys, the 99+2 corpus, legals recomputed
  from the independent Board, audited historical verdicts).
- `input/kNNN.input.csv`, `input/s6w.input.csv`: per-key exact-replay inputs
  `target,0,stones,lo,hi,legal,0,0,0,0,0`.
- `scripts/jsreplay.js`: pinned replica (sha256
  `845856175d3c793a7eb4306f5902ecda3f1c046a8a53e8f34ed375e51febc3df`),
  identical bytes to the reply27 probe publications.
- Consumed pins (not re-published here, sha-verified):
  - base cache `merged-exact-s5-after-js-probe-13.cache` (sha256 `60e0dc34...`)
    at `research/experiments/n11-reply27-s5-jsreplica-probe-10376293541461626880-40960-20261121/output/`;
  - geometry `geometry.json.gz` (sha256 `146be80b...`) and
    `historical-cost-profile.json` at
    `research/experiments/n11-strategy-redesign-20261010/output/`;
  - `independent.py` (sha256 `954d3a10...`) at
    `research/experiments/n11-independent-exact-audit-20261010/scripts/`;
  - `s5_evidence_policy.py` (sha256 `78655e94...`) at
    `research/experiments/n11-frontier-selection-20261005/scripts/`;
  - quarantine registry `results/n11-s5-evidence-quarantine.json`
    (sha256 `81d23160...`);
  - union-audit `global-union-audit.json` (sha256 `7280376d...`) at
    `research/experiments/n11-s5-frontier-census-20261121/output/`;
  - published S6 witness raw `s6-211.csv` (sha256 `78672ab3...`) at
    `research/experiments/n11-s4-boundary-direct-20261012/output/raw/`.
- `scripts/audit_frontier.py` and `scripts/audit_root_loss.py` are adapted
  copies (paths re-pointed, logic identical) of the Oct 12 audits in
  `research/experiments/n11-s4-boundary-direct-20261012/scripts/`.

Execution constraints honored: at most 2 workers (2-core host), fresh 2^22 PnTT
per row, one solver per row, publish=ALL, exact-order=count, <= 15,000,000 node
budget, cold runs only.

## Resume checkpoint (2026-11-22, pass 1 + pass 2 complete for the whole corpus)

- Resumed by the session declared in
  `research/log/2026-11-21-n11-sbd-corpus-regen-resume-pass1-single-owner-note.md`
  (no new keys claimed; every acceptance condition of the 15:39Z declaration
  unchanged). The parent session had stalled after the k061-k084 checkpoint
  (`93ceaab9c3`, 17:22Z).
- Validation gate re-reproduced on the resume host (4/4 node-exact before any
  row start: at2m x2 result 0 / 2,000,000 / legal 98,99; 15M rows result 2 /
  3,651,923 and 5,040,200).
- Pass 1 completed: k085-k101 executed fresh cold this session (17 rows,
  78,590,859 nodes, all result 2 exact LOSS within budget, 0 WIN, 0 unexpected
  exhaustion, every row agreeing with the audited historical verdict), pushed
  at `99becad0f9` (fetch-back 17/17 byte-identical). Pass 1 is now complete
  for the whole declared corpus k001-k101.
- S6 witness: cold determinism pair executed (`s6w.run1/run2.p1.out`, both
  result 2, nodes 5,859,060, identical to the published historical witness
  row), pushed at `32d436ae9`.
- Pass 2 completed: all 100 settled rows re-run fresh cold this session,
  (result, nodes) identical to pass 1 row-for-row (546,428,673 nodes each
  pass, 0 determinism mismatches; k012 TARGET_S5 stays honest result 0 at
  15M). Pushed at `d8575d50a8` / `67ae97a243` / `51d4fa7155` /
  `378a98f592`; cumulative fetch-back all byte-identical.
- Read-only consistency table published: `output/pass-consistency-table.json`
  (fail-closed: determinism 100/100, 0 fresh WIN, 0 fresh/history
  disagreement, k012 the only result-0 row, s6w pair identical; includes
  provenance per row and the standard UNKNOWN guard).
- Layout note for the merge run: pass-2 raws are published as
  `output/raw/kNNN.p2.out` (execution-time checkpoint layout, this lane's
  naming), while `scripts/build_merged_cache.py` (never executed yet) points
  its `RAWS2` at `output/raw-pass2/`. The merge run must repoint that one
  path constant or mirror the raws, and must record the one-line diff in its
  session log and manifest (logic must stay identical to the published Oct 12
  norms).
- Verdicts remain unconsumed: no cache increment, no merge, no class-status
  change, no coverage or third-move statement this session. The remaining
  final-commit pipeline (build_merged_cache.py + gen_s6_witness_audit.py +
  audit_frontier.py + audit_root_loss.py + reclassify/cardinality/analyze,
  merge manifest and SHA-256 manifest) is left to the next run(s) of this lane
  with the two-pass evidence now fully in hand. The standard 11x11 empty
  board, the two-stone root {60,27}, and the third moves {100,108} remain
  UNKNOWN throughout. Nodes and pass counts are never verdicts.
