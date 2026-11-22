# 2026-11-22 n11 S4BD fresh-corpus regeneration merge run session log

Lane: the n11 long-term lane. Declaration:
`research/log/2026-11-22-n11-sbd-corpus-regen-merge-run-single-owner-note.md`
(`0e858300e7`, HEAD-before-push `073b4bd72f`). Parent declaration
(`research/log/2026-11-21-n11-sbd-fresh-corpus-regen-single-owner-note.md`,
15:39Z) and resume declaration (`6273b13fe67`, 23:50Z) in force unchanged;
the merge-run checklist executed is the one pre-registered by the resume
session log addenda 1 and 2. This is the final commit of the parent lane.

## Preflight (all before any pipeline stage)

- Host: 2 cores, Node v22.20.0, Python 3.12.14, stdlib only (no C++
  toolchain; package installation forbidden).
- jsreplay pin sha256 `84585617...` byte-verified. Consumed pins re-fetched
  commit-pinned (`073b4bd72f`) and sha-verified: base probe-13 cache
  `60e0dc34...`, geometry.json.gz `146be80b...`, independent.py
  `954d3a10...`, s5_evidence_policy.py `78655e94...`, quarantine registry
  `81d23160...`, Oct 12 S6 raw `s6-211.csv` `78672ab3...`.
- All 205 raws + 104 inputs of this experiment re-fetched and verified by
  local git-blob-sha1 recomputation: 309/309 byte-identical, 0 mismatches.
- Node-exact validation gate 4/4 reproduced fresh cold this session:
  at2m x2 -> result 0, nodes 2,000,000, legal 98 and 99; 15M rows ->
  result 2, nodes 3,651,923 and 5,040,200; byte-stable against the published
  val outputs except wall_s.

## Execution

1. k012 (TARGET_S5, input `target,0,5,1152921504607899649,536870912,98,...`)
   pass 2, fresh cold 15M, serial foreground: honest result 0, nodes
   15,000,000 (exact budget exhaustion), wall 83s; identical (result, nodes)
   to the published pass-1 raw (wall 126s there). The full two-pass
   determinism matrix (101 keys + s6w pair) is thereby complete.
2. One-line, path-only repoints documented before execution (logic
   identical; both pre/post sha256 recorded here):
   - `scripts/build_merged_cache.py` `RAWS2`: `output/raw-pass2/` ->
     `output/raw/` (`e4e7ca9e3b4e...` -> `114dad4e8bbe...`);
   - `scripts/gen_s6_witness_audit.py` `WITNESS2`: `output/raw-pass2/s6w.p2.out`
     -> `output/raw/s6w.p2.out` (`6eb0f8b09332...` -> `034266857dce...`).
   Exactly the two deviations pre-registered by the resume addenda.
3. `gen_s6_witness_audit.py` PASS: single canonical LOSS witness
   `(1152921504675009536,536870912)` (6 stones, legal 87, is_or 1, budget
   15M), both fresh passes result 2 / nodes 5,859,060 = the published Oct 12
   witness row; membership of the witness in the TARGET_S5 child boundary
   and the odd-stone AND derivation machine-checked by the independent
   Board. -> `output/s6-witness-fresh-audit.json`.
4. `build_merged_cache.py` PASS (all fail-closed gates): merge of the base
   probe-13 cache (byte-preserved, 5,756 rows, pin verified inside the
   script) + 101 fresh increment rows (100 direct two-pass settled exact
   LOSS + 1 S6-witness-derived TARGET_S5 row, verdict 2, nodes 0). Output
   `merged-exact-s5-after-js-probe-13-plus-freshregen-20261121.cache`:
   5,857 rows, strictly sorted, 0 duplicates, 0 quarantined keys, 0 base
   conflicts, 0 fresh WIN, 0 fresh/history disagreements, k012 the only
   declared exhaustion. sha256
   `4fee9d5ec78a825b487cc4706bc303b6828ea3be162268c307acb448f6c91e12`,
   **byte-identical to the scratch pre-verification candidate `4fee9d5e...`
   of resume addendum 1** (the k012 cache row is derived and independent of
   the pass-2 raw; only the determinism gate newly ran). ->
   `output/merge-manifest.json` (per-key two-pass rows, s6 witness pair,
   gate list).
5. `audit_frontier.py` PASS: every one of the 3,384 frozen S4 child
   boundaries regenerated from the independent integer Board and matched to
   the frozen geometry; over the merged cache: cache rows 5,857
   (LOSS 5,699 / WIN 158), all-S4 class status counts {LOSS 32, WIN 272,
   UNKNOWN 3080}, third-move universe 119, **secured 119/119, remaining []**
   (the historical residual {100,108} is closed), target S4
   `(1297036692683752448,0)` children 106, **child counts LOSS 106 /
   WIN 0 / UNKNOWN 0 => class status LOSS**. -> `output/frontier-after-fresh-regen.json`.
6. `audit_root_loss.py` PASS: the move-by-move root {60,27} LOSS certificate
   regenerated on the published cache: 119/119 legal root moves, each with
   an S4 LOSS response whose full canonical S5 child boundary is exact LOSS;
   moves 100 and 108 forced to and witnessed through the target S4 (reply
   moves 110 and 120); 32 distinct S4 LOSS classes used; root_outcome LOSS
   (solver-trusted AND/OR propagation; not a terminal-only proof). ->
   `output/root-60-27-loss-proof-freshregen.json`.
7. `reclassify_115_candidates.py` (adapted copy of the Oct 12 published
   script; path-only diffs: cache/frontier/output paths re-pointed to this
   experiment, output files renamed to the fresh-regen names; sha
   `7064efd6...`): the 115 historical {100,108}-covering classes
   reclassify to {LOSS 1 (the target S4), WIN 53, UNKNOWN 61}; the script's
   own gates pass (119 third moves, 115 candidates, target class complete
   LOSS 106/106). -> `output/candidate-classes-after-fresh-regen.csv`,
   `output/candidate-ranking-after-fresh-regen.json`.
8. Honest negatives (published as logs in run A, not as pipeline PASS):
   - `analyze.py` (published two-target-design script, run with
     --cache <merged cache> --out <this experiment>) is STATE-GATED: its
     pre-registered assertion `third_moves - secured == {100,108}` fires with
     the actual residual `set()`; the script encodes the pre-119/119 state
     and its prospective rankings are void over this closed cache. No
     analyze output is asserted.
   - `cache_aware_reply27_cardinality.py` is ENV-BLOCKED on this host:
     `ModuleNotFoundError: numpy` at import (before any load or solve);
     sandbox installs are forbidden and no substitute may be invented; the
     run is delegated. With the machine-checked 119/119 secured coverage of
     step 5 there is no unsecured third-move vertex, so the minimum
     additional UNKNOWN-class cover is vacuously 0; recorded, not asserted
     as a run of the script.

All audit values match the resume session's pre-verification expected-value
anchors exactly (kit `preverification-expected-values.json`), item by item.

## Publication (all fetch-back byte-verified)

- `0e858300e7` declaration (HEAD-before-push `073b4bd72f`).
- `861e6df534` run A: k012 pass-2 raw + repointed scripts (3) + honest
  negative logs (2). (A sibling six-row q7 (6,7) lane addendum `445e6a7812`
  landed between the declaration and run A; path-disjoint, no conflict.)
- `fa46b6f9db` run B: the merged cache (239,164 B).
- `00604a511ff` run C: `merge-manifest.json` + `s6-witness-fresh-audit.json`.
- `15746087ac` run D: `frontier-after-fresh-regen.json` +
  `root-60-27-loss-proof-freshregen.json` (the statements commit).
- `b947210263` run E: reclassify CSV + ranking JSON + `manifest-sha256.json`
  (13 final-commit machine files pinned).
- `2cf23087ee` run F: README final section (title state marker updated, all
  prior sections preserved verbatim).
- This commit: session log.
- Follow-up: K0414 chain-native evidence addendum (status and scope
  unchanged).

Each push was preceded by a latest-main re-fetch; every file was verified
post-push against the commit-pinned raw URL / git blob sha (sha256sum /
blob sha1 recomputation); 0 mismatches.

## Session totals

- Fresh exact replay nodes executed this session: validation gate 12,691,923
  + k012 pass 2 15,000,000 = 27,691,923, serial single process.
- 0 WIN rows, 0 determinism mismatches, 0 fresh/history disagreements, 0
  base/quarantine conflicts, 0 audit failures.

## Status

- The decided-class corpus verdicts are now consumed per the parent
  declaration's acceptance conditions 6/7 (this is the final commit of the
  lane): S4 `(1297036692683752448,0)` closed LOSS on the chain-native cache;
  third-move coverage from root {60,27} is 119/119 secured, remaining [];
  the root {60,27} LOSS certificate is regenerated for the live chain
  lineage and adds chain-native evidence to K0414 (existing status and
  scope unchanged: fixed original first player, solver-trusted leaves,
  `{60,27}` only).
- The standard 11x11 EMPTY BOARD remains UNKNOWN. Nodes, pass counts, solved
  counts and budget exhausted rows are never verdicts. The C++ reference
  implementation gate for the replica rows remains with the scrutiny owner as
  before (this lane's fresh corpus produced only exact LOSS and one honest
  exhaustion; the k02-era WIN rows belong to the disjoint sixth-cost lane and
  are untouched here).
