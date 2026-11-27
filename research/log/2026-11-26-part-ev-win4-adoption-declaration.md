# Part EV declaration: evwin4 canonical WIN adoption (fourth WIN row group), 2026-11-26

Publish-then-execute Part declaration, following the Part EU (euwin2) pattern
(A declaration, B kit scripts, C outputs, D close-out, F completion log).
This declaration pre-registers the bytes this Part will publish and the exact
measurable post-conditions of the adoption.  It pins only already-published
bytes plus the bytes this Part publishes in its own follow-up waves; the
completion log may only close after fetch-back byte verification of every
pinned Part artifact.

## What is adopted

The 4 Part EV gate-verified UNCONSUMED closure-batch WIN rows
(2026-11-22 closure batches 1/3/4/5, 15M two-pass fresh-cold node-exact
replica raws, third-impl a/b verdict-level corroboration, C++ second
implementation scrutiny gate 2026-11-25).  NO new solver pass runs in this
Part.

| key | class | s5_index | lo | hi | legal | budget | result | nodes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| b018 | 16757 (batch-1, dual-class) | 528497 | 1153204079095189504 | 65536 | 60 | 15000000 | WIN(1) | 3549602 |
| d002 | 20421 (batch-3) | 197253 | 3461016313634230272 | 131072 | 73 | 15000000 | WIN(1) | 5359994 |
| e002 | 16371 (batch-4) | 183566 | 1153765929805414400 | 16 | 79 | 15000000 | WIN(1) | 14112632 |
| f017 | 12264 (batch-5) | 415095 | 1188950301625810945 | 70368744177666 | 82 | 15000000 | WIN(1) | 3522635 |

Adopted node total: 26,544,863 (bookkeeping only; nodes are never verdicts).

Provenance pins re-verified live by the maker from published bytes only:
EV gate kit MANIFEST 34d7768b..., SSOT registry gate-rows-ev.json 3ba154f2...
(targets quadruples equal the batch-keys SSOT, batch raws, gate raws and the
ADOPTED table), audit 0327dad8... (schema
n11-centralreply-cppgate-wins41164-audit-v1, overall PASS, 7/7 GATE-PASS,
4/4 byte-identical audit re-runs), gate source kyouen_dfpn_root.cpp
9193f5b6... at commit 154f3b7a67b97e13acbaee8b04dc74ddca728d19; the 4
closure-batch kits re-hashed file-by-file against the registry
batch_source_pins (20 files); the thirdimpl kit re-hashed 96/96 against
MANIFEST c5ed4414...; the EU regression tie is carried: both Part-EU rows
(increment d9365d80...) already sit WIN in BASE with identical nodes and are
NOT re-adopted.

## Canonical chain and scenario of record

* BASE canonical cache (Part EU output, published):
  `research/experiments/n11-centralreply-euwin2-adoption-reaudit-20261125/output/merged-exact-s5-chain-plus-euwin2-20261125.cache`
  sha256 3ba486086703b9f44a0c685d7d5b45fab80f86760f2cd032a8dc18a2690233d6,
  6,767 rows WIN 188 / LOSS 6,579.
* SCEN scenario merged cache of record = the PUBLISHED dossier file
  `research/experiments/n11-centralreply-evwin4-adoption-predecl-20261126/output/merged-exact-s5-chain-plus-evwin4-20261126.cache`
  sha256 63f33c4f620583449641102026b261c559ae5ecc29713cd6445d6fe9369858f0,
  6,771 rows WIN 192 / LOSS 6,579.  This Part does NOT re-publish that file;
  the Part merge audits reproduce it deterministically.
* Dossier supersession (disclosed): the dossier predecl increment
  8d0e43ed... carries a "PREDECL DOSSIER STATUS" header that is measurement
  material only.  The Part-emitted increment supersedes it with the Part EV
  adoption header; the 4 s5verdict rows are byte-identical between the two
  files, and the Part increment is the adoption of record.
* BASE-side reaudit outputs (published Part EU kit, re-executed here
  byte-verbatim by the published refresh fork 6dc24c15...):
  refresh-summary 2b70bb55..., closure-classes 59a4c85f...,
  per-root-coverage cfc2bfe1..., probe-worklist regen pin
  397a43794be60442725825371a5cfba9c2744a69b8f5d32cb3a3f313ced29ba6
  (3,717,712 B; NOT published, size policy).
* SCEN-side reaudit outputs (published dossier kit, re-executed here
  byte-verbatim by the published dossier refresh fork f2edac3e..., itself a
  byte-clone of 6dc24c15... differing only in docstring/CACHE path/expected
  sha): refresh-summary 1fafd081..., closure-classes 6ba51faa...,
  per-root-coverage d9eee976..., probe-worklist regen pin
  ca50cb68c10827e7e24e02c02e0166813b57ad646eb169bf8bd2c827fcdd09df
  (3,717,416 B; NOT published, size policy).
* Census measurement cross-check source: the published dossier
  `census-deltas-evwin4-predecl.json` ab97fba9... is machine cross-compared
  field-by-field by the Part extractor against its own independent recount;
  its dossier-time verdict-scope fields (consumed NOTHING,
  part_ev_declared false) are superseded by this declaration (disclosed, not
  asserted by the extractor).

## Part artifacts this Part will publish (pre-registered)

Kit `research/experiments/n11-centralreply-evwin4-adoption-reaudit-20261126/`:

* `scripts/make_increments_ev_win4_adoption.py`
  sha256 4ddbc83176e079d803f5a86f16d39cae470f9fec663ecbfd2474c7070aa372cc
  (structural clone of the published Part EU maker f2ae97a1...).
* `scripts/compare_deltas_ev_adoption.py`
  sha256 70a5b2077f5774742464d189baa348297c3fbb5c715d327ce8706bfbfbcf2b5b
  (structural clone of the published Part EU extractor 9bc5f06a...).
* `scripts/s5_union_merge.py`
  sha256 907119610034fb2aebfde012550a4129dfa3b086c6de11194e856747ac74606a
  (byte-clone of the published union merger).
* `output/increment-evwin4-20261126.cache`
  sha256 7f1256108d697bd96d473e55a5509dea35f4c0b1be45893cac3f667c4b3f55c4
  (4 WIN rows, nodes 26,544,863; row region byte-identical to the dossier
  increment 8d0e43ed...).
* `output/increments-manifest.json`
  sha256 f013a8f54807297c649538958bbc19b156eab7d469019a1d1dbf7bc31a4726b9
  (schema evwin4-increments-manifest-v1).
* `output/merge-audit-run1.json`,
  `output/merge-audit-run2.json`, `output/merge-audit-run3.json`:
  all sha256
  d9713aed5c0679605bb3e10e0198e1c15fd7b5b3867f3a253f5251b8a0dc667f
  (three byte-identical deterministic runs; unique_rows 6,771,
  verdict_counts WIN(1) 192 / LOSS(2) 6,579, output_sha256 63f33c4f...,
  conflict-free).
* `output/decomp-deltas-evwin4-adoption.json`
  sha256 c05f11cdc7841b3b2b2f86a880ffa548cf34f9be2a48fac09b00c6685f5bdf96
  (schema evwin4-decomp-deltas-v1).
* NOT published (regenerable / superseded / size policy): the merged
  scenario cache copy (byte-identical to the published dossier file
  63f33c4f...), the probe-worklists (enter only as regen pins), the scratch
  refresh re-execution trees.

## Pre-registered measurable post-conditions (fail-closed in the extractor)

1. Cache relation: SCEN == BASE rows + exactly the 4 increment rows;
   every increment row is a fresh exact-WIN row absent from BASE; no key
   outside the adopted set; verdict counts WIN 192 / LOSS 6,579;
   adopted node total 26,544,863.
2. Independent full-class census (replicating the refresh status logic):
   BASE {unknown 34,430, excluded_now 90, free_now 39, excluded 390} ->
   SCEN {unknown 34,417, excluded_now 103, free_now 39, excluded 390};
   EXACTLY 13 status flips, all UNKNOWN -> excluded_now, exactly the
   BASE-unknown owner classes of the adopted keys:
   4864, 4903, 5255, 5282, 5613, 6030, 12264, 12327, 14776, 15640, 16371,
   16757, 20421.  The further owner class 30345 (b018) stays excluded_now
   on both sides (Part EP/EU chain flipped it; no double-flip).  The
   no-member class 30354 also stays excluded_now (EP flip, no EV member).
3. Per-class Board boundary arithmetic (independent regenerations):
   4864 (101/101, 101->100), 4903 (105/103, 102->101),
   5255 (104/104, 104->103), 5282 (95/95, 95->94),
   5613 (105/105, 105->104), 6030 (103/102, 102->101),
   12264 (52/52, 51->50), 12327 (99/99, 99->98), 14776 (59/59, 59->58),
   15640 (96/93, 93->92), 16371 (52/52, 2->1), 16757 (49/49, 3->2),
   20421 (50/49, 6->5), 30345 (51/50, 5->4), 30354 (97/97, 96->96),
   as (raw boundary / cost size, cost-unknown before -> after).
4. closure-classes.csv: rows 805 -> 805, ZERO left, ZERO entered; the
   unknown_now churn is exactly {16371: 2->1, 16757: 3->2, 30345: 5->4,
   20421: 6->5, 12264: 51->50} and the class_rank churn is exactly the
   7-row set {23101: 1->2, 1849: 2->3, 2251: 3->4, 16371: 4->1,
   13342: 11->12, 30118: 12->13, 12264: 13->11}; groups_served_count churn
   empty; every other field of every common row byte-identical.
5. Frozen update8 refresh: resolved_count 260 -> 263, remaining_now
   31,505 -> 31,445, groups_free_now 131 -> 131, union baseline 31,859;
   win_hit_groups 10 -> 25: the 10 BASE class-30354 quartets (recorded
   unknown_s5_children 97) stay IDENTICAL and exactly 15 new groups join,
   the quartets of classes 12264 (6, recorded 51), 16757 (5, recorded 48),
   20421 (4, recorded 49); zero groups removed.
6. per-root coverage: free_now/uncovered identical at all 20 roots +
   baseline; Board verification 39/39, zero rejections on both sides;
   individual greedy union changes only at 6 roots
   {0: 2980->2789, 36: 3005->2951, 12: 2848->2846, 48: 2895->2893,
   5: 2884->2883, 37: 3620->3619}; joint greedy 36,619 -> 36,618;
   group_best_options_nonfree 2,105 -> 2,105; worklist total
   64,307 -> 64,302.  All scheduling bookkeeping, no coverage claim.
7. Determinism: the extractor re-executes BOTH published refresh forks
   byte-verbatim in isolated scratch trees and all 8 outputs (3 published
   + 1 regen pin per side) must be byte-identical to the pins; extractor
   re-runs byte-identical (2 clean runs observed at declaration time); the
   merger reproduces 63f33c4f... in 3/3 byte-identical audits.
8. Tamper battery at declaration time (recorded): extractor pin mutation
   -> ABORT sha drift; adopted-node expectation mutation -> ABORT manifest
   adopted row drift; census count expectation mutation -> ABORT
   independent census after-drift; all fail-closed, clean rerun restored.

## Honesty guards

Consuming the 4 WIN labels asserts NO root verdict, NO root-class verdict
and NO 11x11 outcome.  13 classes become excluded_now (a known WIN cost
child ends free all-LOSS coverage); 34,417 S4 classes remain
status-unknown.  The 21 unconsumed closure-batch LOSS rows, k04 and every
other unconsumed probe-level WIN stay in NO cache.  No batch key was
re-searched at any condition.  The standard 11x11 empty board and every
central-reply root stay UNKNOWN.
