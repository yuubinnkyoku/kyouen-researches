# n11 central-reply class 2251 batch-29 remaining-37-LOSS canonical adoption + reaudit (Part DB, 2026-11-24)

Part DB single-owner canonical adoption of the batch-29 (class 2251)
takeover drive-2 remaining fresh LOSS evidence: the 37 resolved LOSS keys
ab017..ab027 + ab029..ab054 (2-pass node-exact at budget 15M, total nodes
159,325,566 per pass), merged into the canonical exact-S5 chain cache
behind the Part CU base (30ddad9d..., 6,317 rows) as BASE + 37 = 6,354
rows (158 WIN / 6,196 LOSS, sha256 04b0a239...). The 16 keys ab001..ab016
were already adopted by Part CU; the single probe-level WIN key ab028
(result 1, nodes 3,167,121, key (1297036830121656320, 131074), s5 93815)
is NOT adopted here, is emitted into no increment and no canonical cache,
and stays UNCONSUMED (WIN-row adoption remains the scrutiny-owner C++
second-implementation gate 9193f5b6... exclusive lane; three-implementation
corroboration for ab028 is the published Part CZ lane).

## Declaration (publish-then-execute)

Single-owner declaration published before the official run:
`research/log/2026-11-24-part-db-b29loss37-adoption-declaration.md`
(commit 3bf90f67, git blob sha 6ec9ad49...). Observed HEAD at
declaration time cca29581 (with 02:31Z re-check immediately before the
push): no counter-claim on this adoption lane in the last 40 commits.
Part letter: a concurrent session had taken "Part DA" (88ffdc92,
batch-29 b29d2loss15 third-implementation cross-verification, read-only,
verdict-non-consuming, declaring the canonical adoption itself to be a
separate adoption Part's exclusive domain) - this Part DB is that
adoption Part; no other adoption counter-claim existed.

## Contents

- `scripts/make_increments_b29loss37.py` - fail-closed adoption increment
  maker (kit MANIFEST 71-file sha verification, post-scaffold val-gate
  8-file double-host node-exact cross-check, raw 2-pass discipline over
  all 54 keys, status.log strict parse with the CU drive-1 16-line
  append-only prefix gate, BASE/quarantine absence gates, ab028
  WIN-unconsumed pin).
- `scripts/s5_union_merge.py` - byte-clone fail-closed union merger
  (selftest PASS; WIN/LOSS conflict abort).
- `reaudit/scripts/refresh_adoption_b29loss37.py` - post-adoption 19-root
  joint-plan refresh against the merged chain cache (read-only).
- `scripts/compare_deltas_b29loss37_adoption.py` - fail-closed delta
  extractor (pin pile: increment / manifest / scenario / BASE reaudit
  outputs / status.log drive-1 prefix / batch-keys / kit MANIFEST /
  val-gate 4-pattern x 4-host / ab028 WIN pin / class-2251 focus gates).
- `output/increment-b29loss37-20261124.cache` - 37 LOSS rows
  (sha256 85bd4469...).
- `output/increments-manifest.json` - b29loss37-increments-manifest-v1
  (sha256 1b51f30d...; full_packet_eq_loss_only=true ON THE PROBED SET,
  win_scenario_exists=false, no EXHAUSTED row, 16 already-adopted CU
  keys asserted present in BASE).
- `output/merge-audit-run{1,2,3}.json` - audits (sha256 2d7b4998... x3,
  identical; merged output sha256 04b0a239...; inputs 30ddad9d... +
  85bd4469...).
- `output/merged-exact-s5-chain-plus-b28loss1-plus-b28loss7-plus-b29loss16-plus-b29loss37-20261124.cache`
  - the canonical merged chain cache, 6,354 rows (262,326 B).
- `reaudit/output/refresh-summary.json` / `closure-classes.csv` /
  `per-root-coverage.csv` - post-adoption reaudit outputs
  (sha256 1fc531d3... / b37425d7... / 8f69d5bb...). probe-worklist.csv
  (sha256 4ecb9a0a... at generation time) is reproducible from the
  refresh script and is NOT committed for volume.
- `output/decomp-deltas-b29loss37-adoption.json` - base->scenario delta
  book (schema n11-b29loss37-adoption-decomp-deltas-v1,
  sha256 83536046...).

## Run record (official, publish-then-execute)

1. Pre-declaration work (all machine-computed): maker/merger/refresh/
   extractor finalized; all outputs pinned; refresh x3 + isolated rerun
   and extractor x4 + isolated rerun byte-identical; tamper battery
   15/15 (14 tamper probes captured rc=1, control rc=0); the full pin
   pile re-verified against the on-disk files by machine (two sha
   typos introduced by hand transcription into the extractor's
   VAL_GATES block were caught by that machine check and fixed -
   transcription of pins is machine-mediated only).
2. Declaration published (3bf90f67), then official rerun in a fresh
   scratch tree (cp -a, no hardlinks):
   - maker x4: increment 85bd4469... + manifest 1b51f30d... byte
     identical every run (PASS x4).
   - merger: selftest PASS + merge x3: merged cache 04b0a239... byte
     identical x3; merge-audit 2d7b4998... x3 identical when invoked
     with the same relative-path arguments as the declaration-era run
     (an absolute-path invocation produces f01b8626... whose only
     difference is the recorded input file path field - honest note).
   - refresh x3 (~58 s/run) + isolated rerun (second tree, env -i,
     PYTHONHASHSEED=random): all four outputs byte identical to pins
     every run (4ecb9a0a... for the worklist).
   - extractor x4 + isolated rerun: all gates PASS, decomp 83536046...
     byte identical x5.
3. Publication A-E (5 commits: A scripts 4 -> feb725c3, B increment +
   manifest + audits x3 -> c56f0706, C merged cache 262,326 B ->
   951f7bcb, D reaudit outputs + decomp -> 728bc400, E this README +
   MANIFEST-sha256.txt), each fetch-back verified byte-exactly against
   the local tree by commit-pinned raw fetch + cmp.

## Adoption effects (machine-observed, none misread as verdicts)

- class 2251: canonical unknown_now 38 -> 1 (closure rank 4 -> 3).
  The single remaining unknown child is the UNCONSUMED ab028 WIN row
  (s5 93815). class 2251 is NOT freed and NOT excluded: scenario status
  stays unknown (zero-WIN-consumed adoption).
- Class-status counts unchanged on both sides: excluded 390 /
  excluded_now 23 / free_now 38 / unknown 34,498; no excluded_now flip;
  no newly freed class.
- Holder union 107 (class 2251 own 37 fresh rows; 106 other classes
  own exactly 1 each). Closure unknown deltas: 2251 (38->1),
  2257 (97->96), 2299 (98->97), 5535 (56->55), 8583 (59->58),
  9001 (60->59), 11779 (60->59) - all stay UNKNOWN. Closure table
  808/808; churn stable-unknown 126 {excluded_now 2, unknown 124};
  tie-swap left {1035 (rank 486, unknown 98)} / entered {2261
  (rank 460, unknown 97)} (group 15/39 anchor re-selection
  bookkeeping). Anchors 23101 (1,1) and 1849 (2,1) unchanged; 16757
  (unknown 29) unchanged, rank 3 -> 4 (overtaken by 2251's unknown 1).
- update8 unchanged: resolved 141 / remaining 31,718, newly resolved
  empty (the 37 adopted s5 indices do NOT intersect the update8
  requirement set).
- Metrics: probe worklist 64,809 -> 64,765 (net -44; class 2251 serving
  rows 38 -> 1, the remaining 1 row being exactly the unconsumed ab028:
  s5 93815, class_unknown_now 1, closure (37,81), membership 3; the 37
  adopted keys leave 0 scenario rows; serving deltas 1035 (98->0),
  2261 (0->97), 2257/2299/5535/8583/9001/11779 -1 each; ab028 keeps
  both-side rows as schedule bookkeeping). joint greedy union
  35,691 -> 36,903 (+1,212; NON-monotone bookkeeping of the frozen
  greedy scheduler: per-root free/uncovered thirds are unchanged on
  every root; movers root 14 (4,439 -> 4,540, +101), 16 (-1),
  37 (-96), 38 (-2), 49 (-1)); roots summary unchanged (root 27
  119/119).
- batch-29 is probe-complete at probe level: all 54 keys carry two-pass
  labels (53 LOSS, of which 16 are the Part CU rows and 37 are adopted
  here; 1 WIN ab028 unconsumed; 0 EXHAUSTED). Probe-level labels are
  not root verdicts.

## Concurrent lanes (honest contact observation)

- Part DA (88ffdc92, 2026-11-24T02:22Z) declared third-implementation
  cross-verification of 15 of these keys (ab017..ab027+ab029..ab032),
  explicitly read-only and verdict-non-consuming, with the canonical
  adoption reserved to a pinned-merger adoption Part - this Part DB.
  No file overlap with its experiment dir; its outcome will corroborate
  or challenge the corresponding rows.
- Part CZ (68751f... completed): ab028 three-implementation
  corroboration (replica + third-impl, verdict WIN agreement) - ab028
  remains unconsumed pending the scrutiny-owner C++ gate.
- Part CP (batch-30, class 34269) and Part CY (batch-31, class 5804)
  and K1277 (strip z=9) are running on disjoint paths (no contact).

## Interpretation guard

Verdicts are consumed ONLY as exact LOSS rows of probed keys. Nodes and
budget are bookkeeping. Adopting 37 more keys does NOT free class 2251
(its last unknown child ab028 is an unconsumed WIN), does NOT decide
anything about the 19 central-reply roots or the standard 11x11 empty
board. **11x11 stays UNKNOWN.**

