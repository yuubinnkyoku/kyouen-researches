# Part SP kit: n11-centralreply-sixthwin2-adoption-reaudit-20261126

Part SP sixthwin2 canonical WIN-only adoption (declared 2026-11-26 by
the long-term lane session; publish-then-execute waves A-F on main).
This kit declares, measures and publishes the sixthwin2 canonical
WIN adoption:

- the canonical head of record advances from the Part EW head
  merged-exact-s5-chain-plus-sixthwin5 (sha256 16a12390c0c3f046f0ae537b
  2a9940e15661263fc5034ce1b155c138bb9043cd, 6,797 rows WIN 197 /
  LOSS 6,600) to
  merged-exact-s5-chain-plus-sixthwin2 (sha256 cc3694bbe871ccf27bdf4dbc
  f5e93586da440164fd75c02c15dc2a0ae46d11b8, 6,799 rows WIN 199 /
  LOSS 6,600, 284,127 bytes) published HERE (this Part publishes the
  merged head of record itself: unlike EW's sixthwin5, NO
  pre-declaration dossier exists for sixthwin2);
- consumed: exactly the 2 unconsumed parked4 L50M ladder exact-WIN rows
  of the sixth-cost class 10376293541461626880:65536: k13
  1152921573327376384:536870912 (s5 index 112203, nodes 16,402,480)
  and k19 10376293541461626880:65664 (s5 index 103319, nodes
  15,379,062); adopted node total 31,781,542 (bookkeeping, never
  verdicts); adopted-table digest
  e7e2b30d5e5ee504f299ec1e64ecf2c252d9d3ca412299d38932628e8844bd83;
- NOT consumed and NOT emitted (standing unconsumed, recorded only):
  the parked4rest2 L50M WIN rows k20/k33 (third-implementation
  corroboration absent at SP build time; their C++ gate kit Part SN
  was in flight - disclosed) and the 30 fifth-resumption verified
  LOSS rows of the Part SL batch.  No LOSS row is adopted.

## Adopt-eligibility (all re-verified live by the maker and again by the extractor)

1. parked4 ladder kit
   n11-sixthcost-class10376293541461626880-parked4-s5-l50m-ladder-20261126
   (no MANIFEST: every consumed byte direct-pinned): README/jsreplay/
   halt-audit/status.log, 8 input CSVs, 14 raw CSVs; per key the
   15,000,000 park-at-UNKNOWN baseline + the 50M cold two-pass
   node-exact battery + the 32M budget-margin re-proof + the voluntary
   third cold 50M verify run, plus 4 validation-anchor honesty
   replays (2M park-UNKNOWN / 15M honest LOSS);
2. Part SM pinned C++ second-implementation scrutiny gate kit
   n11-sixthcost-parked4-l50m-cppgate-20261126: MANIFEST-sha256
   976e079c069379d51efb2a36d3b7d8919ef30aae577764615d73468ebc6f4abe
   verified file-by-file (28/28), gate table 66/66 PASS, 5 GATE-PASS
   rows (3 anchors + k13/k19), audit_gate.run1/run2/run3 byte-identical
   (a11983dd...), C++ solver pinned
   cpp/solvers/kyouen_dfpn_root.cpp 9193f5b6... @ commit 154f3b7a...;
   the pre-registered adoption requirement the halt-audit delegates;
3. Part SL third-implementation batch audit (published kit
   n11-sixthcost-k01-k03-thirdimpl-verdict-reverification-20261122,
   out/audit-k09k43-summary.json
   300c8c0a61e4e5fe5fb1a8a5a1fe32aaebd391ec767dc2783f3b87cfd943728e):
   verdict-level WIN agreement, 3 identical cold runs each (k13
   expansions 19,433,195 / tt-hits 10,181,270 / tt-overwrites
   15,238,891; k19 17,955,947 / 9,504,863 / 13,761,643), replica
   4-run unanimity + park-baseline rows, cold a/b/v witness rows, and
   the fail-closed negative battery (legal96/stones6 GATE_FAIL);
   expansions legitimately differ from replica node counts (different
   implementations);
4. probe kit selection JSON
   d5e9b059611849f7b7e69c7370a0e66cd7535c43b3a043ce9f5bfc0e5ff72e87:
   k13/k19 are exactly exclusive_probe_order positions 13/19 of the
   same sixth-cost class selection of record;
5. freshness: both keys fresh to BASE (win_ties = [], no
   base-cache-absent hits), quarantine 0, canonical-safe per
   s5_evidence_policy 78655e94...; frozen graph 54f9c364... round trip.

## Files

- scripts/s5_union_merge.py: byte-clone of the published union merger
  (907119610034fb2aebfde012550a4129dfa3b086c6de11194e856747ac74606a);
- scripts/make_increments_sixthwin2_adoption.py: fail-closed Part
  maker (structural clone of the Part EW maker 9e6bf992...; source
  pools replaced: parked4 ladder / SM gate / SL batch; the merged head
  of record and its 3 byte-identical merge audits are additionally
  gated here);
- scripts/measure_census_deltas_sixthwin2.py: census-delta measurer
  (structural clone of the published sixthwin5 dossier measurer
  23869728... with the declared-adoption verdict fields and the
  Part SP expectations);
- scripts/compare_deltas_sixthwin2_adoption.py: fail-closed
  extractor: re-executes both published refreshes (BASE 92a884c9...
  and the SP fork 82ddb89c...) byte-verbatim from scratch trees,
  re-executes the maker byte-verbatim, re-runs the merger 3x with the
  recorded input path strings, republishes the independent census
  recount and cross-checks the published census json field-by-field;
- reaudit/scripts/refresh_adoption_sixthwin2.py: the SP refresh fork
  (byte-clone chain of the published refreshes; exactly the
  docstring / CACHE path / expected-cache-sha regions differ from
  92a884c9...);
- output/increment-sixthwin2-adoption-20261126.cache
  (89bff217885ef89ae7a86d9580657818bdf4c7619ef24da7efd6392169aa1694:
  39-line Part SP header + exactly 2 s5verdict WIN rows);
- output/increments-manifest.json
  (d97f1d5d6b37814cd130fc7519e211b2405f327b9af5e0b7f5bfe9a422c31e07,
  schema sixthwin2-adoption-increments-manifest-v1);
- output/merged-exact-s5-chain-plus-sixthwin2-20261126.cache: the
  merged head of record (BASE 16a12390 + 2 increment rows; 6,799 rows
  WIN 199 / LOSS 6,600);
- output/merge-audit-run{1,2,3}.json
  (5904693ec6836515c2523d5a5b8744e4f515e56400e3288a07dff30e6875f9cf
  x3 byte-identical; inputs recorded with the kit-relative path
  strings of record);
- output/census-deltas-sixthwin2-adoption.json
  (030e36eddc042da500e568f3076352461f008d5625009a5b3814c2f6ae8e38d3);
- output/decomp-deltas-sixthwin2-adoption.json
  (16bb56a02942e97ebc5e18a3c840fc300d1fd27354d8295993670dd797ab0d43,
  schema sixthwin2-decomp-deltas-v1);
- reaudit/output/{refresh-summary.json, closure-classes.csv,
  per-root-coverage.csv}
  (7a500a03... / 350e269a... / 9c5b2774...; the regenerated
  probe-worklist.csv is NOT published per the size policy: regen pin
  0818da81ba01259945d7fb0051b07221582cd4dc68d55d9edb61aa447e4628ac,
  3,715,904 bytes).

## Measured adoption effects (fail-closed verified)

Census 34,409/111/39/390 -> 34,407/113/39/390; EXACTLY 2 win-hit
flips, both unknown -> excluded_now: class 2624 (1297600742147751936:0,
owner of k19) and class 30136 (1152921573327376384:0, owner of k13).
The serving class 3077 was ALREADY excluded_now (Part EW) and stays
so with cost-unknown 95 -> 93; owner classes 5184 (k19) and 3077 keep
their status.  NO class is freed.  Closure classes 804 -> 804 with
zero enter/leave, zero unknown_now churn and zero rank churn.
Per-root coverage byte-identical; joint greedy 35,155 unchanged;
worklist 64,276 -> 64,276 (delta 0).  Frozen update8 refresh: resolved
281 -> 281 (both adopted s5 indices 103319/112203 sit OUTSIDE the
frozen baseline requirement: no baseline-requirement scheduling
change at all), remaining 31,445, groups_free_now 131, win_hit groups
25 -> 25 IDENTICAL.

Note on the lane-era prediction: the parked4 halt-audit's if-adopted
prediction was computed against the older 6e49dd84 head (pre-EW) and
is superseded; the authoritative measurement is against the current
16a12390 head above (the full recount additionally discovers class
30136, and 3077 is already flipped by Part EW).

## Determinism and battery

Maker: 2 runs rc=0 with byte-identical stdout and byte-identical
increment + manifest.  Extractor: 2 runs rc=0 with byte-identical
stdout and byte-identical decomp json.  Merger: 3 runs byte-identical
(cache + audit).  Tamper battery (recorded in the declaration log;
not published as kit files): increment-row WIN->LOSS flip, merge-audit
mutation and manifest mutation each fail-closed rc=1 with
byte-verified restore; clean control rc=0.

## Verdict scope

WIN-only canonical adoption asserts NO root verdict, frees no class
and makes no coverage claim; owner classes leave live status by the
win-hit mechanism only.  The standard 11x11 empty board and every
central-reply root stay UNKNOWN.  k20/k33 WIN rows and the 30 SL
batch LOSS rows stay in NO cache.  Nodes are bookkeeping, never
verdicts.
