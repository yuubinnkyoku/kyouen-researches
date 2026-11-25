# n11-s4bd-fresh-corpus-regen-20261121 (final commit: corpus merged, S4 closed LOSS, 119/119 coverage, root {60,27} certificate regenerated)

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

### Resume checkpoint addendum: merge-layout byte-copies (s6w.p1/s6w.p2)

- `output/raw/s6w.p1.out` and `output/raw/s6w.p2.out` are byte-copies of
  `output/raw/s6w.run1.p1.out` and `output/raw/s6w.run2.p1.out`
  respectively (the two cold determinism runs of this session, sha-identical
  to their source files), published only so that
  `scripts/build_merged_cache.py` can find the S6-witness pair under its
  expected pass1/pass2 filenames. Content and provenance remain the run1 /
  run2 files; the copies carry no new computation.

## Final commit (2026-11-22): merge run (decided-class corpus re-established on the chain lineage)

Executed and published by the merge run declared in
`research/log/2026-11-22-n11-sbd-corpus-regen-merge-run-single-owner-note.md`
(session log `research/log/2026-11-22-n11-sbd-corpus-regen-merge-run-session-log.md`),
under the parent 15:39Z declaration's acceptance conditions, unchanged.

- Preflight on the merge-run host: jsreplay and every consumed pin sha-verified
  (base cache `60e0dc34...`, geometry `146be80b...`, independent.py
  `954d3a10...`, s5_evidence_policy `78655e94...`, quarantine `81d23160...`,
  Oct 12 S6 raw `78672ab3...`); all 205 raws + 104 inputs re-fetched and
  blob-sha-verified (309/309); node-exact validation gate 4/4 reproduced
  fresh this session.
- k012 (TARGET_S5) pass 2: fresh cold 15M replay, honest result 0,
  nodes 15,000,000 (exact budget exhaustion), identical to pass 1, so the
  two-pass determinism matrix over all 101 declared keys + the S6 witness
  pair is complete (`output/raw/k012.p2.out`).
- One-line, path-only repoints (logic identical, pre/post sha256 recorded in
  the session log): `RAWS2` in `scripts/build_merged_cache.py`
  (`output/raw-pass2/` -> `output/raw/`; `e4e7ca9e...` -> `114dad4e...`) and
  `WITNESS2` in `scripts/gen_s6_witness_audit.py` (`6eb0f8b0...` ->
  `03426685...`), exactly the two deviations pre-registered by the resume
  session's addenda.
- `output/s6-witness-fresh-audit.json`: the single canonical LOSS witness
  `(1152921504675009536,536870912)` settles at 5,859,060 nodes in both fresh
  passes; canonical 6-stone child of TARGET_S5 with odd-stone AND polarity;
  cross-checked against the published Oct 12 raw.
- `output/merged-exact-s5-after-js-probe-13-plus-freshregen-20261121.cache`:
  5,857 rows = base probe-13 cache (byte-preserved, 5,756) + 101 increment
  rows (100 direct two-pass settled exact LOSS + 1 S6-witness-derived
  TARGET_S5 row, verdict 2, nodes 0, per the Oct 12 precedent). sha256
  `4fee9d5ec78a825b487cc4706bc303b6828ea3be162268c307acb448f6c91e12`,
  byte-identical to the scratch pre-verification candidate of the resume
  addenda. Every fail-closed gate of `output/merge-manifest.json` passed
  (101/101 determinism incl. the fresh k012 pair, 0 fresh WIN,
  100/100 fresh-vs-history agreement, quarantine-free, base-conflict-free).
- Class and coverage statements, published only from the machine audits over
  this cache (`output/frontier-after-fresh-regen.json`):
  - all 3,384 frozen S4 child boundaries independently regenerated from the
    repo-independent integer Board; cache verdict counts LOSS 5,699 / WIN 158;
    all-S4 class status counts {LOSS 32, WIN 272, UNKNOWN 3080};
  - third-move coverage from root {60,27}: 119/119 secured, remaining []
    (the historical residual {100,108} is closed);
  - target S4 `(1297036692683752448,0)`: all 106 canonical S5 children exact
    LOSS, so the class is closed LOSS on the chain-native cache.
- `output/root-60-27-loss-proof-freshregen.json`: the move-by-move root
  {60,27} LOSS certificate regenerated for the live chain lineage: 119/119
  legal root moves each assigned an S4 LOSS response whose full S5 child
  boundary is exact LOSS; moves 100 and 108 are witnessed through the target
  S4 (replies 110 and 120); 32 distinct S4 LOSS classes used; AND/OR
  propagation solver-trusted, not a terminal-only proof. Per the parent
  declaration this adds chain-native evidence to K0414, which keeps its
  existing status and scope.
- Analyses over the new cache: `scripts/reclassify_115_candidates.py`
  (adapted copy, path-only diffs from the Oct 12 published script)
  reclassifies the 115 historical {100,108}-covering classes to
  {LOSS 1 (the target S4), WIN 53, UNKNOWN 61} (retrospective queue only;
  `output/candidate-classes-after-fresh-regen.csv`,
  `output/candidate-ranking-after-fresh-regen.json`). The published
  `analyze.py` (two-target-design) is state-gated: its pre-registered
  assertions hard-require the residual set {100,108}, which this
  119/119-secured cache empties by design; the attempt is published as an
  honest negative log (`output/analyze-two-target-attempt-state-gate.log`).
  The published `cache_aware_reply27_cardinality.py` is environment-blocked
  on this host (numpy/scipy unavailable and installs forbidden; delegated
  to the scrutiny owner; with zero unsecured third-move vertices the minimum
  additional class cover is vacuously 0 classes, recorded, not asserted as a
  run; `output/cardinality-attempt-env-block.log`).
- `output/manifest-sha256.json` pins the 13 final-commit machine files.
- Status: the corpus verdicts are now consumed per the parent declaration's
  acceptance conditions 6/7 (this is the final commit of the lane). The
  standard 11x11 EMPTY BOARD remains UNKNOWN. The two-stone root {60,27}
  statement is unchanged in scope: LOSS for the original first player,
  `{60,27}` only, solver-trusted, no empty-board claim. Nodes, pass counts
  and solved counts are never verdicts.
