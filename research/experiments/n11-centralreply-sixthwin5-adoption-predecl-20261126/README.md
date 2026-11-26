# EM-pattern WIN-adoption pre-declaration dossier (sixthwin5 scenario) (2026-11-26)

STATUS: this is NOT a Part.  No declaration, no adoption, no verdict
consumption.  The canonical head stays merged-exact-s5-chain-plus-emloss21
(sha256 6e49dd84... 6,792 rows WIN 192 / LOSS 6,600).  The standard 11x11
empty board, every root, S2, the two-stone root {60,27}, its remaining third
moves {100,108} and every closure class stay UNKNOWN.  nodes are bookkeeping.

PURPOSE: the pre-declaration dossier pattern (Part EV euwin4, Part EU
euwin2-loss-side, Part EM emloss21) extended to the WIN side of the
sixth-cost class.  This dossier publishes, up front, every artifact a future
EV-pattern WIN-adoption Part would pin, together with the measured scenario
deltas, so the declaring Part can be declared from published bytes only.
The pool of record is exactly the 5 unconsumed exact-WIN rows of the
sixth-cost exclusive-probe program (class 3077, fifth-resumption batch)
whose verification chain is already complete.

## The 5 adopted WIN rows (unconsumed; all four-implementations verified)

Every row is a two-pass fresh-cold node-exact C++-gated exact WIN at the
single published condition (budget 15,000,000, order 0), third-implementation
corroborated; full per-row source pins are recorded in
output/increments-manifest.json (schema sixthwin5-increments-manifest-v1).

| row | (lo,hi) key | legal | nodes | s5_index | owner classes (graph) |
|---|---|---|---|---|---|
| k02 | 1297036692683751424:68157440 | 87 | 7,717,432 | 64872 | 1387, 3077, 30354 |
| k03 | 10376293541461626880:65792 | 81 | 9,255,414 | 96472 | 2339, 3077, 16734 |
| k04 | 10376293541461626888:65536 | 83 | 9,433,024 | 112201 | 3077, 30329 |
| k05 | 10376293610182157952:65536 | 88 | 13,397,611 | 91506 | 2169, 3077, 25845 |
| k08 | 10376293610182148096:68719476736 | 89 | 6,195,897 | 39127 | 774, 3077 |

Total adopted nodes 45,999,378 (bookkeeping).  Serving class for all five:
3077 (the sixth-cost class 10376293541461626880:65536).  The three standing
unconsumed LOSS rows of the same 18-row plan (k01, k06, k07) are recorded
and NOT adopted here (a WIN-only adoption scenario).  The later third-impl
batch WIN rows k13/k19 (parked4 L50M ladder) are out of this dossier's
scope and stay unconsumed.

Verification chain per row (gates in scripts/make_increments_sixthwin5.py,
all fail-closed, rc=0 twice, byte-identical outputs):

* exclusive-probe kit (n11-sixthcost-class-s5-exclusive-probe-
  10376293541461626880-20261121, no MANIFEST, direct pins): selection
  JSON d5e9b059, status.log SSOT 2a253d08, win-finding-ifadopted ladder
  be662d23, 20 raw sha256 pins; the 5 input CSVs are byte-identical to the
  C++-gate kit and third-impl kit inputs (cross-registration).
* C++ gate kit (n11-sixthcost-exclusive-cppgate-20261126): MANIFEST
  8d84b1a5 verified 46/46, 178 gates PASS, 11-row GATE-PASS, run1/2/3
  audits identical (ad139ece...).
* third-implementation kit (n11-sixthcost-k01-k03-thirdimpl...
  20261122): TI MANIFEST 538f8ec7 (344 lines), verdict-level WIN
  agreement on k03/k04/k05/k08, determinism triplets byte-identical;
  ea73c3e3 kit (20261121) k02 witness: 4 runs (a/b/g/v), 9,106,337
  expansions each, WIN(1) clean.
* freshness vs BASE 6e49dd84, absent from the active quarantine registry
  81d23160, canonical-safe per s5_evidence_policy 78655e94, s5_index
  round-trip against frozen dependency-graph 54f9c364.

## Scenario

SCENARIO cache = canonical BASE (Part EM head 6e49dd84...) union-merged
with the 5 unconsumed exact-WIN rows -> merged-exact-s5-chain-plus-sixthwin5
(sha256 16a12390... 6,797 rows WIN 197 / LOSS 6,600).  Nothing is consumed:
the 5 rows stay unconsumed honest WIN labels until a future Part declares
their adoption.

## Published files

| file | sha256 | size |
|---|---|---|
| scripts/make_increments_sixthwin5.py | 424edee4... | 48,060 B |
| scripts/s5_union_merge.py (byte-clone) | 90711961... | 10,887 B |
| scripts/measure_census_deltas_sixthwin5.py | 23869728... | 21,548 B |
| output/increment-sixthwin5-20261126.cache | 44c16a28... | 2,013 B |
| output/increments-manifest.json (schema sixthwin5-increments-manifest-v1) | 25defefa... | 13,486 B |
| output/merged-exact-s5-chain-plus-sixthwin5-20261126.cache | 16a12390... | 284,024 B |
| output/merge-audit-run1.json (x3 identical) | 2fcc1ce0... | 1,460 B |
| output/census-deltas-sixthwin5-predecl.json | fd684d83... | 4,480 B |
| reaudit/scripts/refresh_adoption_sixthwin5.py | 92a884c9... | 26,621 B |
| reaudit/output/refresh-summary.json | 295027cf... | 38,319 B |
| reaudit/output/closure-classes.csv | 350e269a... | 35,806 B |
| reaudit/output/per-root-coverage.csv | 9c5b2774... | 588 B |

UNPUBLISHED per the size policy: reaudit/output/probe-worklist.csv (regen
pin sha256 82f9e517... 3,715,904 B, recorded in the census json; the
BASE-side worklist regen pin is the published Part EM dossier census json
scen pin 147b62d6... 3,715,963 B).

## Measurements (scripts/measure_census_deltas_sixthwin5.py, rc=0 twice, byte-identical)

All numbers below are machine-derived
(census-deltas-sixthwin5-predecl.json); no hand transcription.

* Census (unknown/excluded_now/free_now/excluded): BASE 34,417/103/39/390
  -> SCEN 34,409/111/39/390.  Exactly 8 status flips, ALL of them
  unknown -> excluded_now (the WIN-side win-hit mechanism; no class is
  freed): classes 774, 1387, 2169, 2339, 3077, 16734, 25845, 30329 =
  EXACTLY the owner classes of the 5 adopted keys that were unknown at
  BASE (measured set equality, not asserted from theory).  The
  independent recount reproduces the published refresh-summary counts
  EXACTLY on both sides.
* Serving-class unknown children (graph-derived): class 3077 100 -> 95
  (exactly the 5 adopted keys, all owned there; its status flips
  unknown -> excluded_now).
* update8 refresh: resolved 280 -> 281 (+1: exactly k02 / s5_index
  64872, the only adopted key that sits in the frozen update8 baseline
  requirement; k03/k04/k05/k08 were first probed after the baseline froze
  and are correctly outside it - measured, disclosed); remaining 31,445
  unchanged; groups_free_now 131 and win_hit 25 groups IDENTICAL
  (set-equal by group key on both sides).
* Joint greedy static requirement 35,155 -> 35,155 UNCHANGED.  Worklist
  total 64,277 -> 64,276 (-1 = exactly the one newly resolved
  in-requirement key).
* Per-root coverage (free_now/uncovered columns, all 20 roots):
  BYTE-IDENTICAL to BASE.
* Closure-classes ranking: 804 -> 804 rows, no row enters or leaves, NO
  rank churn; the only unknown_now churn is class 16734 (92 -> 91; the
  other 7 flipped owner classes are not in the ranked closure table).
  NET reading: a WIN-only adoption moves no scheduling quantity EXCEPT
  the 8 owner classes leaving live status and the one
  in-baseline-requirement resolution.

## Run record (local, byte-pins above)

* Increment rows machine-verified before writing (make_increments_
  sixthwin5.py, fail-closed, rc=0 twice, byte-identical outputs): probe
  kit pinned directly (no MANIFEST, it predates the convention), C++
  gate kit verified against its published MANIFEST 8d84b1a5 (46/46),
  TI kit audits and ea73c3e3 k02 witness parsed and pinned, all 5 rows
  fresh to BASE, quarantine-free, canonical-safe, s5_index/serving/donor
  tables rebuilt from frozen graph bytes.
* Merger = published byte-clone s5_union_merge.py (90711961...): 3
  merge runs, all outputs byte-identical, audits 2fcc1ce0... x3; MERGED
  unique=6,797 dup_elided=0 WIN=197 LOSS=6,600, zero conflicts.
* Refresh fork refresh_adoption_sixthwin5.py (92a884c9...) = byte-clone
  of the published Part EM dossier fork cc01b3d8... differing in
  EXACTLY the three regions (docstring, the CACHE path, the expected
  cache sha); the computation region is byte-identical.  Executed twice
  (~58s each, one process at a time): all outputs byte-identical across
  runs.
* Measurer (this kit's measurement reference) rc=0 twice, byte-identical
  census json fd684d83...; every measured expectation is derived from
  published bytes, and the one hand-transcribed assumption it disagreed
  with (all-5-in-baseline-requirement) was corrected to the measured
  truth before freezing (see the session log).

## Integration path for the declaring Part session

A future Part may declare the sixthwin5 WIN adoption pinning the dossier
bytes above directly.  The declaring Part still owes, per the EM/EP/ER/
EU/EV adoption pattern: declared adopt-eligibility gates (all 5 rows fresh
vs the then-current head, quarantine check, kit re-verification against
published bytes), its own fail-closed extractor recomputing the census
deltas from published bytes (structural clone of compare_deltas_em_
adoption.py; the dossier's measure_census_deltas_sixthwin5.py is the
measurement reference, not a substitute), and the log entry.  Consuming
the 5 WIN labels asserts NO root verdict and NO 11x11 outcome; it moves
no per-root coverage and no joint-greedy quantity.  If the canonical head
has moved beyond 6e49dd84... by then, this dossier's scenario pins must
be re-derived, not patched.

## Pins

* BASE: merged-exact-s5-chain-plus-emloss21 6e49dd84... (6,792 rows WIN
  192 / LOSS 6,600); EM dossier reaudit outputs refresh-summary
  7f379b71... / closure-classes 68628134... / per-root-coverage
  9c5b2774... / worklist regen 147b62d6... (3,715,963 B, in the EM
  census json d67b6e9b...).
* Source kits: probe selection d5e9b059... / status SSOT 2a253d08... /
  win-finding ladder be662d23...; C++ gate MANIFEST 8d84b1a5... (46
  files, audit ad139ece...); TI MANIFEST 538f8ec7... (audits c24da5cd /
  5116045c / 15373d06 / 6cb112f8); ea73c3e3 kit README 1a3ddd07 /
  third_impl.js 08ea958f / k02 witness raws bbce3433, a0eec80f, 98e9427f,
  7a490ad4 (4 runs, 9,106,337 expansions).
* Frozen environment: dependency-graph 54f9c364..., update8 b658290a...,
  policy 78655e94..., quarantine 81d23160....
