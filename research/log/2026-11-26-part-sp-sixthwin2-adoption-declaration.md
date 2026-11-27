# Part SP declaration: sixthwin2 WIN-only canonical adoption (publish-then-execute)

Date: 2026-11-26 (long-term lane session)
Scope: the 2 unconsumed parked4 L50M ladder exact-WIN rows k13
(1152921573327376384:536870912, s5 index 112203, nodes 16,402,480)
and k19 (10376293541461626880:65664, s5 index 103319, nodes
15,379,062) of the sixth-cost class 10376293541461626880:65536
(exclusive_probe_order positions 13/19 of the published selection JSON
d5e9b059611849f7b7e69c7370a0e66cd7535c43b3a043ce9f5bfc0e5ff72e87),
resolved by the parked4 L50M ladder kit
n11-sixthcost-class10376293541461626880-parked4-s5-l50m-ladder-20261126
(budget 50,000,000 over the pinned 15,000,000 park-at-UNKNOWN
baselines; per key a cold two-pass node-exact 50M battery, a 32M
budget-margin re-proof and a voluntary third cold 50M verify run, plus
4 validation-anchor honesty replays).  Adopted node total 31,781,542
(bookkeeping, never verdicts).  This is a WIN-only canonical adoption:
NO LOSS row is adopted.  NOT consumed and NOT emitted (standing
unconsumed, disclosed): the parked4rest2 L50M WIN rows k20/k33
(third-implementation corroboration absent at SP build time; their
C++ gate kit Part SN was in flight) and the 30 fifth-resumption
verified LOSS rows of the Part SL batch.

No pre-declaration dossier exists for sixthwin2 (unlike EW's
sixthwin5): this Part SP publishes the merged head of record itself at
its kit path.  Merger = byte-clone of the pinned s5_union_merge.py
907119610034fb2aebfde012550a4129dfa3b086c6de11194e856747ac74606a.

## Pre-registered kit shas (published in this Part's kit after this log)

Increment (39-line Part SP header + exactly 2 s5verdict WIN rows):
- output/increment-sixthwin2-adoption-20261126.cache =
  89bff217885ef89ae7a86d9580657818bdf4c7619ef24da7efd6392169aa1694

Manifest (schema sixthwin2-adoption-increments-manifest-v1; includes
the canonical_head_published_by_this_part block):
- output/increments-manifest.json =
  d97f1d5d6b37814cd130fc7519e211b2405f327b9af5e0b7f5bfe9a422c31e07

Merged cache of record (BASE 16a12390 6,797 rows + exactly the 2
increment rows -> merged 6,799 rows WIN 199 / LOSS 6,600, 284,127
bytes; verdict agreement everywhere, WIN/LOSS conflict abort armed, no
base-cache-absent hits):
- output/merged-exact-s5-chain-plus-sixthwin2-20261126.cache =
  cc3694bbe871ccf27bdf4dbcf5e93586da440164fd75c02c15dc2a0ae46d11b8

Merge audits (3 byte-identical runs; inputs recorded with the
kit-relative path strings of record):
- output/merge-audit-run{1,2,3}.json =
  5904693ec6836515c2523d5a5b8744e4f515e56400e3288a07dff30e6875f9cf (x3)

Census measurement (measurer output, cross-checked field-by-field by
the extractor's independent recount):
- output/census-deltas-sixthwin2-adoption.json =
  030e36eddc042da500e568f3076352461f008d5625009a5b3814c2f6ae8e38d3

Decomp (fail-closed extractor output, schema
sixthwin2-decomp-deltas-v1; 2 runs rc=0 with byte-identical stdout +
decomp):
- output/decomp-deltas-sixthwin2-adoption.json =
  16bb56a02942e97ebc5e18a3c840fc300d1fd27354d8295993670dd797ab0d43

Reaudit refresh outputs (SP fork byte-clone chain; regenerated
byte-verbatim from scratch by the extractor):
- reaudit/output/refresh-summary.json =
  7a500a032f997307defb37f28ce65f93ce935f2feca9ca6281c5474775ef4bc7
- reaudit/output/closure-classes.csv =
  350e269a9d4e0827274aff7c587cdb389f070eade0ff54c220c7c14f9197bc6d
- reaudit/output/per-root-coverage.csv =
  9c5b277429f99157ff2e65323b5912b9ce957f1d2008f8ac8fc1e03b49f91ad1
- reaudit/output/probe-worklist.csv: NOT published per the size policy;
  regen pin 0818da81ba01259945d7fb0051b07221582cd4dc68d55d9edb61aa447e4628ac,
  3,715,904 bytes

Kit scripts:
- scripts/s5_union_merge.py (byte-clone of the published union
  merger) =
  907119610034fb2aebfde012550a4129dfa3b086c6de11194e856747ac74606a
- scripts/make_increments_sixthwin2_adoption.py (structural clone of
  the Part EW maker 9e6bf992...; sources replaced: parked4 ladder /
  SM gate / SL batch; the merged head and its 3 audits additionally
  gated) =
  6e95f467fb3074242cc513b7513bd50ddadc67ee472151ad4e5daf42666541fb
- scripts/measure_census_deltas_sixthwin2.py (structural clone of the
  sixthwin5 dossier measurer 23869728...) =
  062a071c92e485825bd65de5aef19ddeafe1223ba21bf43f162052352d318fe9
- scripts/compare_deltas_sixthwin2_adoption.py (own fail-closed
  extractor: re-executes both published refreshes byte-verbatim,
  re-executes the maker byte-verbatim, re-runs the merger 3x with the
  recorded input path strings, republishes the independent census
  recount and cross-checks the census json field-by-field) =
  9feb2cbe58e612fddeabe34c5169baba2e0b2cf4b30374f3894c46bba4351b65
- reaudit/scripts/refresh_adoption_sixthwin2.py (byte-clone of the
  published sixthwin5 dossier refresh 92a884c9... differing in exactly
  the docstring / CACHE path / expected-cache-sha regions) =
  82ddb89c279f6221cd6d5aa8e89f5f316eba56592fbb7201550b2478da00852e

## Base / scenario identity

- BASE (head of record at declaration) = the Part EW merged exact-S5
  chain cache
  16a12390c0c3f046f0ae537b2a9940e15661263fc5034ce1b155c138bb9043cd
  (6,797 rows WIN 197 / LOSS 6,600), published at the sixthwin5 dossier
  kit path.  Unchanged by this Part.
- SCEN (canonical head after Part SP) = BASE rows + exactly the 2
  Part increment rows, verdict agreement everywhere, NO
  base-cache-absent hits, quarantine 0.  Both adopted keys are fresh
  to BASE: win_ties = [] (no consumed-WIN regression ties).
- Downstream lanes must re-anchor against the advanced head of
  record cc3694bb... at this kit's output path (freshness vs BASE
  16a12390 is superseded by freshness vs cc3694bb for any later
  adoption).

## Adopt-eligibility gates (all declared, all re-verified live twice)

Both rows were re-verified against published bytes by the Part maker
(live re-check) AND again during the extractor run (byte-verbatim
re-execution of the maker from a scratch tree, increment + manifest
reproduced byte-identically), which re-encodes: parked4 ladder direct
sha pins (README, jsreplay.js, halt-audit.json
9baeb8be..., status.log, 8 input CSVs and all 14 raw CSVs incl. the 4
validation-anchor honesty replays; halt-audit gates_passed_count 77,
parked baselines, halt-on-WIN stop rule 1, k20/k33 never-started
disclosure), the probe selection JSON d5e9b059... (positions 13/19 of
the 43-key exclusive_probe_order), the Part SM C++
second-implementation scrutiny gate kit (MANIFEST-sha256
976e079c... verified file-by-file 28/28, gate table 66/66 PASS, 5
GATE-PASS rows incl. the 3 anchors, audit_gate x4 byte-identical
a11983dd..., C++ solver 9193f5b6... @ 154f3b7a..., batch-input
cross-registration and raw/margin/run3 sha cross-registration back to
the parked4 raws), the Part SL third-implementation batch audit
(summary 300c8c0a...: row_results k13/k19 with verdict-level WIN
agreement, determinism triplets identical, replica 4-run unanimity
and park-baseline rows, cold a/b/v witness rows with pinned
tt-overwrites 15,238,891 / 13,761,643, fail-closed negative battery
legal96/stones6), the fresh-to-BASE / quarantine / canonical-safety
gates and the adopted-table digest
e7e2b30d5e5ee504f299ec1e64ecf2c252d9d3ca412299d38932628e8844bd83.
The Part increment is row-for-row disjoint from the Part EW kit
increment efee7b9e... and the sixthwin5 dossier increment
44c16a28... (no re-adoption of any consumed row).

## Measurements (declared, verified fail-closed by the extractor)

- Census flips: EXACTLY 2, BOTH unknown -> excluded_now, win-hit only,
  and exactly the owner classes of the adopted keys that were
  status-unknown at BASE: {2624 (1297600742147751936:0, owner of k19),
  30136 (1152921573327376384:0, owner of k13)}.  The other owner
  classes 3077 (both keys; already excluded_now since Part EW) and
  5184 (k19) keep their status.  Census 34,409/111/39/390 ->
  34,407/113/39/390.  NO class is freed.
- Serving class 3077: cost-unknown 95 -> 93 (exactly the 2 adopted
  keys, both owned there); its status stays excluded_now on both
  sides (Part EW's earlier win-hit; the SP adoption is not its
  first).
- Lane-era prediction superseded (disclosed): the parked4 halt-audit's
  if-adopted global-status prediction was computed against the
  6e49dd84 head (pre-EW) and is not the measurement of record; the
  full recount against the current 16a12390 head additionally
  discovers class 30136.
- Closure-classes.csv: 804 -> 804, ZERO rows enter or leave; ZERO
  unknown_now churn; rank churn EMPTY (0 re-ranked rows);
  groups_served churn 0.
- Frozen update8 refresh: resolved 281 -> 281 (BOTH adopted s5
  indices 103319 / 112203 sit OUTSIDE the frozen baseline
  requirement: nothing newly resolves, measured, disclosed),
  remaining 31,445 unchanged, groups_free_now 131, union baseline
  31,859, win_hit groups 25 -> 25 IDENTICAL sets.
- Per-root: free_now/uncovered identical at all 20 roots (per-root
  coverage byte-identical on both sides); individual greedy union
  UNCHANGED at all 20 roots; joint greedy 35,155 -> 35,155
  UNCHANGED; unique groups 2,115 -> 2,115;
  group_best_options_nonfree 2,101 -> 2,101; worklist 64,276 ->
  64,276 (delta 0: the 2 adopted keys are probe-worklist members but
  sit outside the frozen baseline requirement row set that drives the
  worklist delta accounting).  All scheduling bookkeeping, no
  coverage claim.
- Determinism: maker 2 runs rc=0, byte-identical stdout + increment +
  manifest; extractor 2 runs rc=0, byte-identical stdout + decomp;
  merger 3 runs byte-identical (cache + audit); refresh forks
  byte-verbatim re-executed on both sides from scratch trees.
- Tamper battery (recorded here, not published as kit files):
  increment-row WIN->LOSS flip, merge-audit unique_rows mutation and
  manifest adopted_nodes_total mutation all fail closed rc=1 with
  byte-verified restore; clean control rc=0.

## Session honesty note

This session continued after a context compaction mid-kit.  All kit
bytes were re-staged from the published repo tree and re-verified
against the published pins listed above before the recorded runs; the
merged-cache sha was re-derived by machine (an earlier hand-noted
transcription differed; the maker/extractor/README/manifest pins all
carry the machine-derived cc3694bb... value, re-verified by sha256sum
round trip).  Staged working files outside the kit path are not part
of the kit.

## Verdict scope and status

Consuming the 2 exact-WIN labels asserts NO root verdict, frees no
class and makes no coverage claim; owner classes leave live status by
the win-hit mechanism only.  The standard 11x11 empty board and every
central-reply root stay UNKNOWN.  k20/k33 WIN rows and the 30 SL
batch LOSS rows stay in NO cache.  Nodes are bookkeeping, never
verdicts.

Next waves (B kit scripts, C outputs, D kit README + MANIFEST-sha256,
F completion log advancing the head of record 16a12390 -> cc3694bb at
this kit's output path) follow publish-then-execute with fetch-back
byte verification per wave.
