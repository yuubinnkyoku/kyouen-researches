# Part EV adoption pre-declaration dossier (evwin4 scenario) (2026-11-26)

STATUS: this is NOT a Part.  No declaration, no adoption, no verdict
consumption.  The canonical head stays merged-exact-s5-chain-plus-euwin2
(sha256 3ba48608... 6,767 rows WIN 188 / LOSS 6,579).  The standard 11x11
empty board, every root, S2, class 1/2/4 and every closure class stay
UNKNOWN.  nodes are bookkeeping.

PURPOSE: the Part EU lesson (its declaration pinned a scenario refresh fork
at a377eea0..., bytes that were never published, forcing the disclosed
repair fork 6dc24c15...) was that declaration pins must only reference
PUBLISHED bytes.  This dossier publishes, up front, every artifact a
future Part EV adoption declaration would pin, together with the measured
scenario deltas, so that Part EV can be declared from published material
only.

## Scenario

SCENARIO cache = the canonical BASE (Part EU head 3ba48608...) union-merged
with the 4 Part EV gate-verified UNCONSUMED closure-batch WIN rows
(b018 class 16757, d002 class 20421, e002 class 16371, f017 class 12264;
EV gate kit b2f54948..., declaration 666fefd3..., run wave C f6ab5c30...,
audit 0327dad8... G0-G4 PASS) -> merged-exact-s5-chain-plus-evwin4
(sha256 63f33c4f... 6,771 rows WIN 192 / LOSS 6,579).  Nothing is
consumed: the 4 rows stay gate-verified UNCONSUMED labels until a Part EV
declaration says otherwise.

## Published files

| file | sha256 | size |
|---|---|---|
| output/increment-evwin4-20261126.cache | 8d0e43ed... | 1,193 B |
| output/merged-exact-s5-chain-plus-evwin4-20261126.cache | 63f33c4f... | 282,733 B |
| output/merge-audit-run1.json (x3 identical) | 3f40ce90... | 1,542 B |
| output/census-deltas-evwin4-predecl.json | ab97fba9... | 9,469 B |
| reaudit/output/refresh-summary.json | 1fafd081... | 37,214 B |
| reaudit/output/closure-classes.csv | 6ba51faa... | 35,852 B |
| reaudit/output/per-root-coverage.csv | d9eee976... | 588 B |
| reaudit/scripts/refresh_adoption_evwin4.py | f2edac3e... | 26,147 B |
| scripts/measure_census_deltas_evwin4.py | 2c842b50... | 16,203 B |

UNPUBLISHED per the size policy: reaudit/output/probe-worklist.csv
(regen pin sha256 ca50cb68... 3,717,416 B; the BASE-side worklist regen pin
is the published Part EU pin 397a4379... 3,717,712 B).

## Measurements (script scripts/measure_census_deltas_evwin4.py, rc=0)

All numbers below are machine-derived (census-deltas-evwin4-predecl.json);
no hand transcription.

* Census (unknown/excluded_now/free_now/excluded):
  BASE 34,430/90/39/390 -> SCEN 34,417/103/39/390.  The independent
  recount (frozen graph s4_status/s4_cost + update8 receipts + cache
  verdicts) reproduces the published refresh-summary counts EXACTLY on
  both sides.
* EXACTLY 13 status flips, all unknown -> excluded_now:
  4864, 4903, 5255, 5282, 5613, 6030, 12264, 12327, 14776, 15640, 16371,
  16757, 20421 = exactly the BASE-unknown owner classes of the 4 keys.
  Owner arithmetic (owner classes of each key from the frozen graph):
  b018 3 owners (15640, 16757, 30345 - the last already excluded_now at
  Part EP, correctly NOT double-flipped), d002 4 owners (5255, 5282,
  6030, 20421), e002 4 owners (4864, 4903, 5613, 16371), f017 3 owners
  (12264, 12327, 14776).  2+4+4+3 = 13 exactly.
* Owner-class unknown_now churn (closure-classes.csv):
  16757: 3 -> 2, 30345: 5 -> 4, 20421: 6 -> 5, 16371: 2 -> 1,
  12264: 51 -> 50.  805 -> 805 rows, zero enter/leave.
* update8 refresh: resolved 260 -> 263, remaining 31,505 -> 31,445,
  groups_free_now 131 unchanged, win_hit groups 10 -> 25 (15 new, zero
  removed; the 15 new hits are quartet groups whose class is one of the
  4 target classes).
* Joint greedy static requirement 36,619 -> 36,618; worklist total
  64,307 -> 64,302.
* Class rank churn (7 rows): 16371 4->1, 23101 1->2, 1849 2->3,
  2251 3->4, 12264 13->11, 13342 11->12, 30118 12->13.
* Per-root coverage: free_now and uncovered columns IDENTICAL on all 20
  roots; the individual_greedy_union column drops on 6 roots
  (first=5: -1, 48: -2, 37: -1, 36: -54, 12: -2, 0: -191).

## Run record (all local, byte-pins above)

* Increment rows machine-verified before writing: all 4 keys fresh to BASE
  3ba48608..., absent from the active quarantine registry (81d23160...),
  canonical-safe per s5_evidence_policy, (lo,hi)/s5_index/class node-pinned
  to the EV gate SSOT gate-rows-ev.json (3ba154f2...).  Adopted node total
  26,544,863 (b018 3,549,602 / d002 5,359,994 / e002 14,112,632 /
  f017 3,522,635), agreeing with the gate-kit README target total.
* Merger = published byte-clone s5_union_merge.py (90711961...): selftest
  PASS; 3 merge runs, all outputs byte-identical, audits 3f40ce90... x3;
  MERGED unique=6771 dup_elided=0 WIN=192 LOSS=6579, zero conflicts.
* Refresh fork refresh_adoption_evwin4.py (f2edac3e...) = byte-clone of
  the published Part EU refresh 6dc24c15... (itself the disclosed repair
  clone of the Part ER refresh 6c91e0ce...) with EXACTLY three regions
  changed: the docstring, the CACHE path, the expected cache sha.  The
  computation region is byte-identical (asserted mechanically, only the
  two pin lines differ outside the docstring).
* Fork executed twice (63.8s / 65.8s, one process at a time): all four
  outputs byte-identical across the two runs.

## Integration path for the declaring Part EV session

The Part EV declaration may pin the dossier bytes above directly (they
are published by this commit).  The Part still owes, per the
EM/EP/ER/EU adoption pattern: the declared adopt-eligibility gates
(evwin2-style: EV gate SSOT verification, freshness of all 4 rows vs the
then-current head, quarantine check, third-impl gates), its own
fail-closed extractor recomputing the census deltas from published bytes
(structural clone of compare_deltas_eu_adoption.py 9bc5f06a...; the
dossier's measure_census_deltas_evwin4.py is the measurement reference,
not a substitute), and the log entry.  Consuming the 4 WIN labels asserts
NO root verdict and NO 11x11 outcome; a consumed WIN only marks classes
excluded as scheduling bookkeeping.  If the canonical head has moved
beyond 3ba48608... by then, this dossier's scenario pins must be
re-derived, not patched.

## Pins

* BASE: merged-exact-s5-chain-plus-euwin2 3ba48608...; EU reaudit outputs
  refresh-summary 2b70bb55... / closure-classes 59a4c85f... /
  per-root-coverage cfc2bfe1... / worklist regen 397a4379...
  (3,717,712 B); increment d9365d80...; audits 9f807c95... x3; EU fork
  6dc24c15...; ER refresh 6c91e0ce...; EU extractor 9bc5f06a...;
  EU merger byte-clone 90711961...
* Part EV gate provenance: SSOT gate-rows-ev.json 3ba154f2...; gate source
  kyouen_dfpn_root.cpp 9193f5b6... (commit 154f3b7a); gate kit b2f54948;
  declaration 666fefd3; run wave C f6ab5c30; audit 0327dad8; G0-G4 PASS.
* Frozen environment: dependency-graph 54f9c364..., update8 b658290a...,
  Board 954d3a10..., policy 78655e94..., quarantine 81d23160...,
  b38-keys 29807104...
