# n11-centralreply-sixthlossk38-adoption-reaudit-20261126 (Part SV, 2026-11-26)

Part SV: the sixthlossk38 LOSS-ONLY canonical adoption in the
central-reply chain.  The one standing unconsumed resolved exact-LOSS
row of the sixth-cost probe kit
n11-sixthcost-class-s5-exclusive-probe-10376293541461626880-20261121
(class 10376293541461626880:65536, s4 serving class 3077,
exclusive_probe_order position 38, s5_index 85024,
key 10376293541461626880:66048) is consumed into the canonical
merged exact-S5 chain cache as a LOSS label.  After this adoption the
probe kit's sixth-cost batch has zero standing unconsumed
loss-resolved rows (standing_unconsumed_parked_keys = 0).

The adopted row is cold two-pass node-exact at the pinned 50,000,000
resolution budget (nodes 21,839,049, bookkeeping only; nodes are
never verdicts), C++-gated by the Part SS pinned second-implementation
scrutiny gate (GATE-PASS target quadruple 100,50000000,2,21839049)
and third-implementation-corroborated by the Part SU L50M third-impl
kit (verdict-level LOSS(2) agreement, auditor re-run live 31/31 x2
byte-identical).  NO new solver pass runs in this Part.

Nothing here asserts any root verdict and no 11x11 outcome: a
LOSS-only canonical adoption transfers NO verdict to any
central-reply root, frees NO class, excludes NO class and changes NO
coverage claim (the Part EM precedent; status_flip_count = 0,
verified).  After the adoption the S4 census is unchanged at
34,405 unknown / 115 excluded_now / 39 free_now / 390 excluded; the
serving class 3077 stays excluded_now with cost-unknown 61 -> 60.
Closure-ladder churn, per-root coverage and the probe worklist are
measured byte-identical to BASE (zero churn, zero re-routing; joint
greedy 36,789 unchanged, worklist_total 64,275 unchanged).  The
standard 11x11 empty board, all 19 central-reply roots, the two-stone
root {60,27} and the third-move pair {100,108} stay UNKNOWN.

## chain position

* BASE = the published Part ST adoption head of record
  merged-exact-s5-chain-plus-sixthloss30-20261126.cache (sha256
  dade15780ce6625cc70d93ba77b1560145dd2b9f096a53dce556d2fccf7e312b,
  6,831 rows, WIN 201 / LOSS 6,630) at the Part ST kit path.
* increment = `output/increment-sixthlossk38-adoption-20261126.cache`
  (1 LOSS row, sha256
  977780efc8cc447be8212c445c311e536f42e8a56bbb9ba2d06ec50e3b9ff6e5;
  adopted-table digest sha256
  75a45f999795a170ba09f8522fdeaaf2bbece59b59b4d50025d42b6ef192bba5).
  SSOT per-row pins in `output/increments-manifest.json` (schema
  sixthlossk38-adoption-increments-manifest-v1, sha256
  2619f1b345eec424bc8c8d2a7971cff1fe6004b107df84878dacf17dbdc99ce6;
  base_cache_absent_hits_for_emitted 0, quarantine_hits 0,
  loss_ties 0, win_ids 0).
* merged head of record = `output/merged-exact-s5-chain-plus-sixthlossk38-20261126.cache`
  (6,832 rows, WIN 201 / LOSS 6,631, sha256
  42dbb58ffe8dd02a81f4a92993d08e3fbebdaeb4b4f7bf33e142120ff055bdc4,
  285,776 B), published by this Part: reproduced by the fail-closed
  union merger byte-clone (`scripts/s5_union_merge.py`, sha256
  907119610034fb2aebfde012550a4129dfa3b086c6de11194e856747ac74606a)
  from BASE + the Part increment, 3/3 byte-identical runs
  (merge-audit-run1/2/3.json all sha256
  c5e03c951c984aea60d416d52bd82e71aa78810b9a8a733a42239361dcbf870a,
  unique_rows 6,832, WIN 201 / LOSS 6,631, conflict-free).

## LOSS label eligibility (fail-closed, machine-verified)

The maker `scripts/make_increments_sixthlossk38_adoption.py` (sha256
15b1ed74ab8c7da9b7a447a4a1e57626652aa5189f82593ba9aafd39a408be15)
is a structural clone of the published Part ST maker
make_increments_sixthloss30_adoption.py (sha256 d4949f71...): the
computation region (source-kit byte gates, multi-pass payload gates,
gate-kit MANIFEST verification, third-impl gates, freshness/
quarantine/canonical-safety gates, adopted-table digest,
self-publication gates, increment emit) is identical logic; the
disclosed diffs are the docstring, the source pools (the probe kit's
published k38 stage raws pinned per stage file; the Part SU kit
manifest verified 21 files; the Part SU auditor re-run live x2), the
emitted header block, output names and manifest fields.  The
published census/manifest are byte-identical re-publications of the
local generator output (fetch-back verified by git blob sha in
wave C2: the first wave C publication had corrupted the 20-digit key
10376293541461626880 to 10376293541461627000 through a JSON
round-trip in the publishing step; the sha256 pins of record were
never wrong and are now byte-exact on main).  The maker measures
merged_cache_bytes live with a fail-closed gate (no hardcoded
byte counts).

## measurement (census deltas) and reaudit

* `output/census-deltas-sixthlossk38-adoption.json` (sha256
  dc3d4e3cb06d269b9b483df5a1209cb9b4865046b0d4571615eb496833bb8b59)
  from `scripts/measure_census_deltas_sixthlossk38.py` (sha256
  2695e6180532f42a11997002ce4d0eff53e5868039a6be814a422d04181e3f1f):
  all embedded expectations asserted live (BASE/SCEN census recount
  identical 34,405/115/39/390, status flips 0, closure churn all
  empty, per-root byte-identical, joint greedy 36,789 = 36,789,
  worklist_total 64,275 = 64,275, update8 resolved 281 /
  remaining 31,445 identical, win_hit groups 25 identical, the one
  adopted s5_index 85024 outside the baseline requirement,
  owner_class_count_hist {3: 1}).
* reaudit (refresh of the published closure/per-root/worklist state
  against the SCEN head): runner
  `reaudit/scripts/refresh_adoption_sixthlossk38.py` (sha256
  9500cc66389aa6c92b784e292baf8f0adb540a2f798ea176102e84194ac11b7b),
  outputs `reaudit/output/refresh-summary.json` (sha256
  451c1e3647b2a4431cb57a81c5c4b372ffd111638ef2f77bf95a295d2a36e19d),
  `reaudit/output/closure-classes.csv` (sha256
  0eb19c8955e92c3e96c9a7d40f84a4d2c274489fb03b8d1266b850995ea818e9),
  `reaudit/output/per-root-coverage.csv` (sha256
  1828d7f764015a2d319dd56fc19de666fef49a30843b4a6ec37187d14370f849).
  The probe worklist is NOT published (size policy): BASE and SCEN
  regen pins are byte-identical sha256
  b946ed062e84d0a14f84dd4db167d1b051bb1459bc3a8ff738eeda3d9c6d8c26
  (3,715,960 B, worklist_total 64,275 unchanged); regenerable from
  the published refresh forks against the pinned cache heads.

## verdict status

11x11 empty board: UNKNOWN.  All 19 central-reply roots: UNKNOWN.
Two-stone root {60,27}: UNKNOWN.  Third-move pair {100,108}: UNKNOWN.
Every closure class: UNKNOWN unless a published Part says otherwise.
This Part consumes exactly 1 exact-LOSS leaf row and nothing else;
no partial, pn/dn or node-count value is read as a verdict.
