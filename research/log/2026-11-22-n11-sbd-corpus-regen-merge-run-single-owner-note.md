# 2026-11-22 n11 S4BD fresh-corpus regeneration: merge run (final-commit pipeline): single-owner declaration

- Declaration time: 2026-11-22T01:2xZ (exact time carried by this commit's
  author timestamp; HEAD at declaration `073b4bd72f`, re-fetched immediately
  before this push). Lane identity: the n11 long-term lane. This note declares
  the merge run of the S4BD fresh-corpus regeneration experiment
  (`research/experiments/n11-s4bd-fresh-corpus-regen-20261121/`), i.e. the
  final-commit stage of the parent single-owner declaration
  (`research/log/2026-11-21-n11-sbd-fresh-corpus-regen-single-owner-note.md`,
  15:39Z) and its resumed execution
  (`research/log/2026-11-21-n11-sbd-corpus-regen-resume-pass1-single-owner-note.md`,
  23:50Z; session log `research/log/2026-11-22-n11-sbd-corpus-regen-resume-pass1-pass2-session-log.md`
  incl. the two scratch pre-verification addenda). No new S5 key is claimed
  anywhere: every key of this run is already inside the parent lane's 101-key
  claim, and the only fresh solver execution is `k012`'s pass-2 determinism
  re-run at the parent-declared 15M budget (the sole gap the resume session
  left to this run). Every acceptance condition of the parent declaration
  remains in force unchanged.
- Preconditions re-verified on this execution host before this declaration:
  - jsreplay pin byte-verified (sha256
    `845856175d3c793a7eb4306f5902ecda3f1c046a8a53e8f34ed375e51febc3df`).
  - All consumed pins re-fetched commit-pinned and sha-verified: base
    probe-13 cache `60e0dc34...` (5,756 rows), geometry.json.gz `146be80b...`,
    independent.py `954d3a10...`, s5_evidence_policy.py `78655e94...`,
    quarantine registry `81d23160...`, published Oct 12 S6 witness raw
    `s6-211.csv` (`78672ab3...`).
  - All 205 raws and all 104 input files of this experiment re-fetched
    commit-pinned and verified byte-identical (git blob sha1 recomputation,
    309/309).
  - Node-exact validation gate 4/4 reproduced fresh on this host this session
    (at2m x2: result 0, nodes 2,000,000, legal 98/99; 15M rows: result 2,
    nodes 3,651,923 and 5,040,200; byte-stable against the published val
    outputs except wall_s).
  - Corpus raw state check: `output/raw/kNNN.p2.out` present for 100 settled
    rows plus `s6w.p1.out`/`s6w.p2.out` byte-copies; `k012.p2.out` absent
    (this run executes it).
- Declared scope, in the order of the merge-run checklist (session log
  addendum 1 item-by-item, addendum 2 for the audit stages):
  1. `k012` pass-2 fresh cold (budget 15,000,000; expected honest
     result 0, nodes 15,000,000 = exact budget exhaustion, matching
     `k012.p1.out`; any other outcome is a publication blocker), published
     as `output/raw/k012.p2.out`.
  2. The two one-line, path-only repoints documented by the resume session
     (logic identical, both pre/post shas recorded in this run's outputs):
     `RAWS2` in `scripts/build_merged_cache.py` and `WITNESS2` in
     `scripts/gen_s6_witness_audit.py`, repointed from
     `output/raw-pass2/` to the actual checkpoint layout `output/raw/`.
  3. `scripts/gen_s6_witness_audit.py` (S6-witness membership/parity machine
     check for the TARGET_S5 derived row).
  4. The unpatched merge (`scripts/build_merged_cache.py`, with only the
     documented RAWS2 path repoint): merged cache
     `merged-exact-s5-after-js-probe-13-plus-freshregen-20261121.cache`
     (new file; base probe-13 cache byte-preserved) + `merge-manifest.json`.
     The merged-cache sha256 is compared against the scratch pre-verification
     candidate `4fee9d5e...`: byte-identical is expected (the k012 cache row
     is derived and independent of the pass-2 raw; only the determinism gate
     newly runs); any divergence is a publication blocker to investigate
     before anything else is published.
  5. Only if 1-4 pass: `scripts/audit_frontier.py` (all 3,384 frozen S4 child
     boundaries independently regenerated; residual third-move set must be
     {100,108} or empty; expected-if-published values per the pre-verification
     anchors: cache rows 5,857 (LOSS 5,699 / WIN 158), all-S4 class counts
     {LOSS 32, WIN 272, UNKNOWN 3080}, third-move coverage 119/119 secured,
     remaining [], target S4 `(1297036692683752448,0)` 106/106 children LOSS)
     and `scripts/audit_root_loss.py` (move-by-move root {60,27} certificate,
     moves 100/108 forced through the target S4). The class-closure,
     119/119-coverage and root-{60,27} statements are published only from
     these machine audits. The root statement adds chain-native evidence to
     K0414 (which keeps its existing status) and does not touch the empty
     board.
  6. The remaining published-pipeline analyses over the new cache, as
     path-repointed adapted copies in this experiment's `scripts/` (no logic
     changes): `reclassify_115_candidates.py` and `analyze.py`.
     `cache_aware_reply27_cardinality.py` cannot run on this host (its
     numpy/scipy imports; package installation is forbidden in this sandbox
     and no substitute implementation may be invented): it is honestly
     delegated, with its outputs void given the machine-checked 119/119
     secured coverage of step 5 (no unsecured third-move vertex remains, so
     the minimum UNKNOWN-class cover is vacuously 0; recorded, not asserted
     as run).
  7. Publication: `output/raw/k012.p2.out`, repointed scripts, merged cache,
     `merge-manifest.json`, `s6-witness-fresh-audit.json`,
     `frontier-after-fresh-regen.json`, `root-60-27-loss-proof-freshregen.json`,
     reclassify/analyze outputs, a SHA-256 manifest for the final-commit
     files, README final section, session log, and the K0414 evidence
     addendum; latest `main` re-fetched before every push; fetch-back byte
     verification on every publish.
- Fail-closed rules (unchanged in force): any k012 pass-2 outcome other than
  honest 15M exhaustion; any determinism mismatch anywhere in the merge
  input; any fresh WIN row; any fresh/history verdict disagreement; any
  quarantined-key entry; any merged-cache sha divergence from the scratch
  candidate; any audit failure (residual set, boundary mismatch, non-LOSS
  target child, missing witness) -> the corresponding statements are NOT
  published, raws and the failure are published honestly instead, and the
  lane hands over to the scrutiny owner. Verdict consumption happens exactly
  as pre-registered by the parent declaration's acceptance condition 6/7
  (this is the final commit of the parent lane).
- Disjointness (machine-checked on latest main at declaration): the
  sixth-cost k05..k43 batch stays halted under its own stop rule and is
  path/key-disjoint from this corpus; the bank recalibration lane is complete
  and uses its own paths; the six-row (6,5)/(6,7)/(6,6) lanes are non-n11-S4
  topics; no other active lane writes into this experiment dir, these log
  paths, or K0414.
- Status guard: the standard 11x11 empty board remains UNKNOWN. Until the
  canonical publication of steps 1-5 passes every gate, the two-stone root
  {60,27} keeps its guarded treatment in lane documentation. Nodes, pass
  counts, and solved counts are never verdicts.
