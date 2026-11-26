# Part SQ kit: n11-centralreply-sixthwin3-adoption-reaudit-20261126

Part SQ sixthwin3 canonical WIN-only adoption (declared 2026-11-26 by
the long-term lane session; publish-then-execute waves on main).  This
kit declares, measures and publishes the sixthwin3 canonical WIN
adoption:

- the canonical head of record advances from the Part SP head
  merged-exact-s5-chain-plus-sixthwin2 (sha256 cc3694bbe871ccf27bdf4dbc
  f5e93586da440164fd75c02c15dc2a0ae46d11b8, 6,799 rows WIN 199 /
  LOSS 6,600) to
  merged-exact-s5-chain-plus-sixthwin3 (sha256 02db5ab35b8ad71dfd069921
  7756291c6bc896c78e9fd7c609b5e25177f6b25c, 6,801 rows WIN 201 /
  LOSS 6,600, 284,230 bytes) published HERE (this Part publishes the
  merged head of record itself: no pre-declaration dossier exists for
  sixthwin3);
- consumed: exactly the 2 unconsumed parked4rest2 L50M ladder
  exact-WIN rows of the sixth-cost class 10376293541461626880:65536:
  k20 10376293541461626880:33619968 (s5 index 111843, nodes
  16,196,331) and k33 12682136550675320832:65536 (s5 index 97791,
  nodes 15,842,649); exclusive_probe_order positions 20/33 of the
  published probe selection; adopted node total 32,038,980
  (bookkeeping, never verdicts); adopted-table digest
  d89ccfbb53078359fb650b2ac7fec5d94fe2b7bfb0038b54ce476d7b01f6dd28;
- NOT consumed and NOT emitted (standing unconsumed, recorded only):
  the still-parked key k38 of the same probe selection
  (15,000,000 park-at-UNKNOWN, NO L50M follow-up claimed - the
  coverage asymmetry the k20/k33 third-impl completion
  pre-registered) and the 30 fifth-resumption verified LOSS rows of
  the Part SL batch, which remain WITHOUT a delegated C++
  second-implementation gate (coverage asymmetry disclosed).  No LOSS
  row is adopted.

## Adopt-eligibility (all re-verified live by the maker and again by the extractor)

1. parked4rest2 ladder kit
   n11-sixthcost-class10376293541461626880-parked4rest2-s5-l50m-ladder-
   20261126 (MANIFEST-sha256
   fa4b2615c1edce655e94a4be7cdc765e2d68015b68f323a0df7f8c4169b76fed
   verified file-by-file, 26/26): per key the 15,000,000
   park-at-UNKNOWN baseline + the 50M cold two-pass node-exact
   battery + the 32M budget-margin re-proof + the voluntary third
   cold 50M verify run, plus 4 validation-anchor honesty replays;
   the consumed bytes are additionally direct-pinned (README,
   jsreplay, halt-audit, status.log, 6 input CSVs, 14 raw CSVs);
2. Part SN pinned C++ second-implementation scrutiny gate kit
   n11-sixthcost-parked4rest2-l50m-cppgate-20261126: MANIFEST-sha256
   9853b8616949cbfb9b64b23ce7b97e053303a0d9183ddb0873a36d2fd35a853d
   verified file-by-file (28/28), gate table 67/67 PASS, 5 GATE-PASS
   rows (3 anchors + k20/k33), audit_gate.run1/run2/run3
   byte-identical (3fbb449d...), C++ solver pinned
   cpp/solvers/kyouen_dfpn_root.cpp 9193f5b6... @ commit 154f3b7a...;
   the pre-registered adoption requirement the halt-audit delegates;
   its gate-rows input CSVs are byte-equal to the ladder batch
   inputs (cross-registration gated);
3. k20/k33 third-implementation verdict re-verification addendum
   (published inside the kit
   n11-sixthcost-k01-k03-thirdimpl-verdict-reverification-20261122,
   auditor audit_k20k33.py
   32893172386f002b551b6380b71d44ba0bc18ef8f2ab6bbcaf78228e4de2c172,
   re-run LIVE by the Part maker, rc=0, 49/49 gates, deterministic
   stdout x2): verdict-level WIN agreement, 3 identical cold runs
   each (k20 expansions 19,455,330 / tt-hits 10,071,309 /
   tt-overwrites 15,261,026; k33 18,829,006 / 10,066,094 /
   14,634,702), replica 4-run unanimity + park-baseline rows (the
   addendum's replica-raw copies are byte-equal to the ladder raws,
   gated), cold a/b/v witness rows, C1 fresh-calibration raws and
   the fail-closed negative battery (legal+1 / stones=6 GATE_FAIL);
   expansions legitimately differ from replica node counts (different
   implementations);
4. probe kit selection JSON
   d5e9b059611849f7b7e69c7370a0e66cd7535c43b3a043ce9f5bfc0e5ff72e87:
   k20/k33 are exactly exclusive_probe_order positions 20/33 of the
   same sixth-cost class selection of record;
5. freshness: both keys fresh to BASE (win_ties = [], no
   base-cache-absent hits), quarantine 0, canonical-safe per
   s5_evidence_policy 78655e94...; frozen graph 54f9c364... round
   trip.  Note: the lane-time pins of the halt-audit and the SN
   gate-rows (canonical head 16a12390..., pre-SP) are disclosed as
   lane-era records; freshness vs the current cc3694bb head is what
   this Part gates and measures.

## Files

- scripts/s5_union_merge.py: byte-clone of the published union merger
  (907119610034fb2aebfde012550a4129dfa3b086c6de11194e856747ac74606a);
- scripts/make_increments_sixthwin3_adoption.py: fail-closed Part
  maker (structural clone of the published Part SP maker
  6e95f467...; source pools replaced: parked4rest2 ladder / SN gate /
  k20-k33 third-impl addendum; the merged head of record and its 3
  byte-identical merge audits are additionally gated here);
- scripts/measure_census_deltas_sixthwin3.py: census-delta measurer
  (structural clone of the published Part SP measurer
  062a071c... with the Part SQ expectations);
- scripts/compare_deltas_sixthwin3_adoption.py: fail-closed
  extractor (structural clone of the published Part SP extractor
  9feb2cbe...): re-executes both published refreshes (BASE
  82ddb89c... and the SQ fork 60dfb1a1...) byte-verbatim from
  scratch trees, re-executes the maker byte-verbatim, re-runs the
  merger 3x with the recorded input path strings, republishes the
  independent census recount and cross-checks the published census
  json field-by-field;
- reaudit/scripts/refresh_adoption_sixthwin3.py: the SQ refresh fork
  (byte-clone chain of the published refreshes; exactly the
  docstring / CACHE path / expected-cache-sha regions differ from
  82ddb89c...);
- output/increment-sixthwin3-adoption-20261126.cache
  (47f7dfb02489a960184b5c83bd3ed36e33936bd40067c7cc97299ab1f740ecc6:
  44-line Part SQ header + exactly 2 s5verdict WIN rows, emit order
  k33 then k20);
- output/increments-manifest.json
  (07181de7e74b619be876fdfff907f452a294cec20705258314560327e12eeb27,
  schema sixthwin3-adoption-increments-manifest-v1);
- output/merged-exact-s5-chain-plus-sixthwin3-20261126.cache: the
  merged head of record (BASE cc3694bb + 2 increment rows; 6,801
  rows WIN 201 / LOSS 6,600, 284,230 bytes);
- output/merge-audit-run{1,2,3}.json
  (622ac17f72c9ad2a7b9e9714b3274c6bcba1df34910365268db16f3c76e0c368
  x3 byte-identical; inputs recorded with the kit-relative path
  strings of record);
- output/census-deltas-sixthwin3-adoption.json
  (8d8329d092557933300c3b7297c3fe532ce157a62b7694308aadf716a56e6fcc);
- output/decomp-deltas-sixthwin3-adoption.json
  (88cf53386ce66d5a2ffbcef4d622f9de54240e0fd7fbde6c343864d4037d1015,
  schema sixthwin3-decomp-deltas-v1);
- reaudit/output/{refresh-summary.json, closure-classes.csv,
  per-root-coverage.csv}
  (de205c31... / 350e269a... / 9c5b2774...; the regenerated
  probe-worklist.csv is NOT published per the size policy: regen pin
  24301312e1e7cfd904da085723144bbbaef15e272c2d430979410520672dcd33,
  3,715,904 bytes).

Provenance note: this kit's scripts and outputs were rebuilt after a
full local environment loss (session timeout) by deterministic
reconstruction from the published-byte-verbatim inputs; the maker
reproduced the pinned increment (47f7dfb0...) and manifest
(07181de7...) bytes exactly, the refresh fork reproduced all pinned
reaudit outputs exactly, and the measurer/extractor were rebuilt as
structural clones of the published SP originals with the Part SQ
expectations.  The census and decomp measurement jsons were
regenerated by the rebuilt measurer/extractor (all measured fields
identical to the pre-loss recorded values; the json shas
8d8329d0.../88cf5338... are the authoritative ones of record).

## Measured adoption effects (fail-closed verified)

Census 34,407/113/39/390 -> 34,405/115/39/390; EXACTLY 2 win-hit
flips, both unknown -> excluded_now: class 3054
(1297037794341814272:0, owner of k20) and class 2402
(1873498544497754112:0, owner of k33).  The serving class 3077 was
ALREADY excluded_now (Part EW) and stays so with cost-unknown
93 -> 91; owner classes 30156 (k20) and 6233 (k33) were already
excluded_now at BASE and keep their status.  NO class is freed.
Closure classes 804 -> 804 with zero enter/leave, zero unknown_now
churn and zero rank churn.  Per-root coverage byte-identical; joint
greedy 35,155 unchanged; worklist 64,276 -> 64,276 (delta 0).  Frozen
update8 refresh: resolved 281 -> 281 (both adopted s5 indices
97791/111843 sit OUTSIDE the frozen baseline requirement: no
baseline-requirement scheduling change at all), remaining 31,445,
groups_free_now 131, win_hit groups 25 -> 25 IDENTICAL.  Owner-class
histogram: both adopted keys have exactly 3 owner classes.

## Determinism and battery

Maker: 2 runs rc=0 with byte-identical increment + manifest.
Extractor: 2 runs rc=0 with byte-identical decomp json.
Merger: 3 runs byte-identical (cache + audit).  Tamper battery
(recorded in the declaration log; not published as kit files):
increment-row WIN->LOSS flip, merge-audit mutation and manifest
mutation each fail-closed rc=1 with byte-verified restore; clean
control rc=0.

## Verdict scope

WIN-only canonical adoption asserts NO root verdict, frees no class
and makes no coverage claim; owner classes leave live status by the
win-hit mechanism only.  The standard 11x11 empty board and every
central-reply root stay UNKNOWN.  The still-parked k38 and the 30 SL
batch LOSS rows stay in NO cache.  Nodes are bookkeeping, never
verdicts.
