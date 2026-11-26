# Part SV declaration: sixthlossk38 LOSS-only canonical adoption (2026-11-26)

Canonical-chain adoption declaration (lineage: EM loss-only precedent,
SQ sixthwin3, SR cppgate, SS k38 C++ gate, ST sixthloss30, SU k38
third-impl). This Part consumes exactly the one standing unconsumed
loss-resolved row of the sixth-cost exclusive S5 batch: k38
(class 10376293541461626880:65536, s4 serving class 3077, probe kit
n11-sixthcost-class-s5-exclusive-probe-10376293541461626880-20261121,
exclusive_probe_order position 38, key 10376293541461626880:66048).
After this Part standing_unconsumed_parked_keys = 0: every k-row of
the batch is now either adopted into the canonical chain or adopted by
an earlier Part.  The third-impl corroboration vacancy recorded in the
Part ST declaration is closed by Part SU before this consumption.

## Claimed territory

Exactly 1 LOSS row consumed into the canonical merged exact-S5 chain:
the canonical head of record advances from the Part ST head
dade15780ce6625cc70d93ba77b1560145dd2b9f096a53dce556d2fccf7e312b
(6,831 rows, WIN 201 / LOSS 6,630) to
merged-exact-s5-chain-plus-sixthlossk38-20261126.cache
(42dbb58ffe8dd02a81f4a92993d08e3fbebdaeb4b4f7bf33e142120ff055bdc4,
6,832 rows, WIN 201 / LOSS 6,631, 285,776 B).  Adopted node total
21,839,049 (bookkeeping only).  NO root verdict, NO 11x11 outcome,
NO class freed, NO class excluded: LOSS-only adoption flips no status
(Part EM precedent), and this single-row adoption is measured
byte-identical to BASE on every planning surface: closure-classes.csv,
per-root-coverage.csv and probe-worklist.csv all unchanged; serving
class 3077 stays excluded_now with cost-unknown 61 -> 60 (measured).

## Eligibility (fail-closed, all machine-verified live during assembly)

- Source rows: the probe kit's published k38 stage raws, pinned
  directly per stage file (5 raws: at2m parked 2,000,000; at15m-run1
  and at15m-run2 parked 15,000,000 pair; at50m-run1 and at50m-run2
  resolved LOSS(2) at the 50,000,000 budget, node-exact 21,839,049
  across the pair), each payload-gated against the pinned
  key/legal/budget/result/nodes table.
- C++ second-implementation scrutiny: Part SS pinned gate kit
  (MANIFEST + gate-status.log byte-cloned into this kit's input/ and
  sha-pinned), k38 GATE-PASS line
  (100, 50000000, 2, 21839049) verified live.
- Third-implementation corroboration: Part SU kit (21/21 files
  MANIFEST-verified live) with verdict-level LOSS(2) agreement;
  audit_k38.py re-run live x2 by this lane's maker, both rc=0 31/31,
  stdout byte-identical across the pair.
- Freshness: k38 absent from the BASE head of record
  (base_cache_absent_hits_for_emitted 0); quarantine-free;
  canonical-safe per the pinned s5 evidence policy.
- Determinism: maker x2 byte-identical manifest; union merger
  byte-clone 3/3 byte-identical merged outputs; refresh x2
  byte-identical; measurer x2 byte-identical census json.

## Pre-registered pins (all byte-verified against the emitted files)

- BASE: dade15780ce6625cc70d93ba77b1560145dd2b9f096a53dce556d2fccf7e312b
  (6,831 rows, WIN 201 / LOSS 6,630; the Part ST published head).
- increment-sixthlossk38-adoption-20261126.cache (1 LOSS row):
  977780efc8cc447be8212c445c311e536f42e8a56bbb9ba2d06ec50e3b9ff6e5
  (2,254 B; adopted-table digest
  75a45f999795a170ba09f8522fdeaaf2bbece59b59b4d50025d42b6ef192bba5).
- increments-manifest.json (schema
  sixthlossk38-adoption-increments-manifest-v1):
  2619f1b345eec424bc8c8d2a7971cff1fe6004b107df84878dacf17dbdc99ce6
  (3,860 B; base_cache_absent_hits_for_emitted 0, quarantine_hits 0,
  loss_ties [], win_ids [], standing_unconsumed_parked_keys 0).
  Disclosure: this lane's maker initially emitted the manifest with
  merged_cache_bytes hardcoded 285,769, 7 B off the measured 285,776;
  caught by this lane before any publication and fixed to a
  live-measured byte size with fail-closed sha + size gates on the
  merged head of record; the merged cache sha 42dbb58f... was correct
  throughout.  The corrected manifest is the one pinned here.
- merged head of record:
  42dbb58ffe8dd02a81f4a92993d08e3fbebdaeb4b4f7bf33e142120ff055bdc4
  (285,776 B, 6,832 rows, WIN 201 / LOSS 6,631), reproduced by the
  fail-closed union merger byte-clone
  907119610034fb2aebfde012550a4129dfa3b086c6de11194e856747ac74606a
  (repo-relative invocation) 3/3 byte-identical runs; merge audits
  merge-audit-run1/2/3.json all sha256
  c5e03c951c984aea60d416d52bd82e71aa78810b9a8a733a42239361dcbf870a.
- census-deltas-sixthlossk38-adoption.json:
  dc3d4e3cb06d269b9b483df5a1209cb9b4865046b0d4571615eb496833bb8b59
  (3,644 B; all embedded expectations asserted live: census recount
  BASE/SCEN identical 34,405 unknown / 115 excluded_now / 39
  free_now / 390 excluded, status flips 0, serving class 3077 stays
  excluded_now with cost-unknown 61 -> 60, closure churn zero
  (804 rows, entered/left/unknown/rank churn all empty), per-root
  greedy delta empty and per-root-coverage.csv byte-identical,
  joint greedy 36,789 = 36,789, worklist_total 64,275 = 64,275,
  win_hit groups 25 identical, update8 resolved 281 / remaining
  31,445 identical, the adopted s5 index outside the baseline
  requirement, owner_class_count_hist {3: 1}).
- Kit scripts: maker
  15b1ed74ab8c7da9b7a447a4a1e57626652aa5189f82593ba9aafd39a408be15
  (fresh single-row fail-closed maker, NOT a byte-clone of the Part
  ST maker; disclosed: direct per-stage probe-raw pins, Part SS
  byte-clone pins, Part SU kit MANIFEST verification and live
  audit_k38.py re-run x2, dependency-graph s5_index/owner
  verification, fail-closed merged-head sha + live byte-size gates),
  measurer
  2695e6180532f42a11997002ce4d0eff53e5868039a6be814a422d04181e3f1f
  (disclosed structural adaptation of the Part ST measurer
  b43da34a..., fresh single-row expectations), merger byte-clone
  90711961... (above).
- Reaudit: runner refresh_adoption_sixthlossk38.py (3-region
  disclosed diff clone of the Part ST runner 02987d1c...: kit path,
  merged-cache name/pin, manifest schema):
  9500cc66389aa6c92b784e292baf8f0adb540a2f798ea176102e84194ac11b7b;
  refresh-summary.json
  451c1e3647b2a4431cb57a81c5c4b372ffd111638ef2f77bf95a295d2a36e19d,
  closure-classes.csv
  0eb19c8955e92c3e96c9a7d40f84a4d2c274489fb03b8d1266b850995ea818e9
  (byte-identical to the Part ST published closure ladder),
  per-root-coverage.csv
  1828d7f764015a2d319dd56fc19de666fef49a30843b4a6ec37187d14370f849
  (byte-identical to the Part ST published per-root coverage).
  probe-worklist.csv NOT published (size policy): SCEN regen pin
  b946ed062e84d0a14f84dd4db167d1b051bb1459bc3a8ff738eeda3d9c6d8c26
  (3,715,960 B), byte-identical to the BASE regen pin (measured
  zero worklist drift for this adoption); worklist_total 64,275
  unchanged.
- Kit path of record:
  research/experiments/n11-centralreply-sixthlossk38-adoption-reaudit-20261126/
  (README + MANIFEST-sha256 + scripts x3 + output x7 + reaudit
  scripts x1 + reaudit output x3; worklist excluded by size policy).

## Publication waves

A: this declaration.  B: kit scripts (merger byte-clone, maker,
measurer).  C: kit output (increment, increments-manifest,
census-deltas, merge-audit x3, merged head of record).  D: reaudit
script + 3 outputs + kit README.md + MANIFEST-sha256.txt.  F:
completion log.  Each wave re-fetches latest main before push
(hourly parallel-lane hazard); on any conflict, record and defer.

## Verdict scope

11x11 empty board UNKNOWN; all 19 central-reply roots UNKNOWN;
two-stone root {60,27} UNKNOWN; third-move pair {100,108} UNKNOWN;
every closure class UNKNOWN unless a published Part says otherwise.
Nodes are bookkeeping, never verdicts.
