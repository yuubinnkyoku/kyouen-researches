# EM-pattern loss-adoption pre-declaration dossier (emloss21 scenario) (2026-11-26)

STATUS: this is NOT a Part.  No declaration, no adoption, no verdict
consumption.  The canonical head stays merged-exact-s5-chain-plus-evwin4
(sha256 63f33c4f... 6,771 rows WIN 192 / LOSS 6,579).  The standard 11x11
empty board, every root, S2, class 1/2/4 and every closure class stay
UNKNOWN.  nodes are bookkeeping.

PURPOSE: the Part EU lesson (declaration pins must only reference
PUBLISHED bytes) applied to the loss side.  This dossier publishes, up
front, every artifact a future EM-pattern loss-adoption Part would pin,
together with the measured scenario deltas, so that the declaring Part
can be declared from published material only.  The pool of record is
exactly the 21 unconsumed closure-batch LOSS rows named by the published
Part EV adoption territory ("the 21 unconsumed closure-batch LOSS rows
(EM-pattern loss-adoption territory)").

## Scenario

SCENARIO cache = the canonical BASE (Part EV head 63f33c4f...) union-
merged with the 21 unconsumed closure-batch exact-LOSS rows -> merged-
exact-s5-chain-plus-emloss21 (sha256 6e49dd84... 6,792 rows WIN 192 /
LOSS 6,600).  Nothing is consumed: the 21 rows stay unconsumed honest
LOSS labels until a future Part declares their adoption.

| pool | class | budget | rows | adopted nodes |
|---|---|---|---|---|
| batch-5 (2026-11-22, two-pass fresh-cold node-exact) | 12264 | 15,000,000 | f001-f016, f018 (17) | 58,253,401 |
| Part ES reprobe30m (2026-11-25, two-pass fresh-cold node-exact) | 30345 | 30,000,000 | ai024, ai030, ai038, ai041 (4) | 71,265,013 |
| total adopted |  |  | 21 | 129,518,414 |

The 3 source-batch WIN rows f017 (Part EV, 15M, 3,522,635), ai007 and
ai040 (Part EU euwin2, 30M, 16,090,493 / 20,711,023) sit in BASE already
as WIN with identical nodes: regression ties, machine-verified, NOT
re-adopted, NOT emitted.

## Published files

| file | sha256 | size |
|---|---|---|
| scripts/make_increments_emloss21.py | 74fbbfd9... | 39,350 B |
| scripts/s5_union_merge.py (byte-clone) | 90711961... | 10,887 B |
| scripts/measure_census_deltas_emloss21.py | a6979d1a... | 19,462 B |
| output/increment-emloss21-20261126.cache | 47443dc1... | 2,728 B |
| output/increments-manifest.json (schema emloss21-increments-manifest-v1) | 94815c34... | 13,020 B |
| output/merged-exact-s5-chain-plus-emloss21-20261126.cache | 6e49dd84... | 283,770 B |
| output/merge-audit-run1.json (x3 identical) | f4304731... | 1,548 B |
| output/census-deltas-emloss21-predecl.json | d67b6e9b... | 62,156 B |
| reaudit/scripts/refresh_adoption_emloss21.py | cc01b3d8... | 26,221 B |
| reaudit/output/refresh-summary.json | 7f379b71... | 38,307 B |
| reaudit/output/closure-classes.csv | 68628134... | 35,806 B |
| reaudit/output/per-root-coverage.csv | 9c5b2774... | 588 B |

UNPUBLISHED per the size policy: reaudit/output/probe-worklist.csv
(regen pin sha256 147b62d6... 3,715,963 B; the BASE-side worklist regen
pin is the published Part EV dossier pin ca50cb68... 3,717,416 B).

## Measurements (script scripts/measure_census_deltas_emloss21.py, rc=0)

All numbers below are machine-derived
(census-deltas-emloss21-predecl.json); no hand transcription.

* Census (unknown/excluded_now/free_now/excluded): BASE 34,417/103/39/390
  -> SCEN 34,417/103/39/390, IDENTICAL.  EXACTLY ZERO status flips:
  loss-only adoption frees no class and excludes no class (every owner
  class of the 21 keys keeps its BASE status; the independent recount
  reproduces the published refresh-summary counts EXACTLY on both sides).
* Serving-class unknown_now arithmetic (graph-derived): class 12264
  50 -> 33 (exactly the 17 batch-5 keys consumed; closure rank 11 -> 9);
  class 30345 4 -> 0 (the 4 Part ES keys exhausted its remaining unknown
  closure children; the class EXITS the closure-classes ranking, rows
  805 -> 804, exited=[30345], entered=[]; its status stays excluded_now
  already excluded at Part EP - no flip).  Rank churn across the
  remaining ranking: 763 rows re-ranked (huge mass only because the 21
  keys' owner classes, 3-owner x7 / 4-owner x14, shifted by 1-2 counts
  each and the ranking is dense at the cheap end).
* update8 refresh: resolved 263 -> 280 (+17: exactly the 17 batch-5
  keys that sit in the frozen update8 baseline requirement; the 4 Part
  ES keys were first probed in batch-38 AFTER the baseline froze and
  are correctly not in it - measured, disclosed); remaining 31,445
  unchanged; groups_free_now 131 and win_hit 25 unchanged (loss-only
  adds no win-hit group).
* Joint greedy static requirement 36,618 -> 35,155 (MINUS 1,463,
  -4.0%: the largest single scheduling reduction of any pending
  adoption pool measured so far; pure re-routing after class 30345
  leaves the cheap end of the ranking).  Worklist total 64,302 ->
  64,277 (-25).
* Per-root coverage: free_now and uncovered columns IDENTICAL on all 20
  roots; the individual_greedy_union column changes on 6 roots (49 -1,
  38 -135, 5 -17, 12 -4, 16 +13, 36 +50 - four drops and two rises;
  the greedy heuristic is a scheduling quantity, disclosed as-is).

## Run record (all local, byte-pins above)

* Increment rows machine-verified before writing (make_increments_
  emloss21.py, fail-closed, rc=0 twice with byte-identical outputs):
  the batch-5 kit kit has no MANIFEST (2026-11-22, it predates the
  convention) so every consumed byte is pinned directly (README, keys,
  status and all 36 raws; re-anchored 39/39 file-by-file against the
  published repo tree at dossier construction time); the Part ES kit is
  verified file-by-file against its published MANIFEST cc987739 (38/38);
  targets-30m cross-gated field-by-field against the b38 batch-keys
  SSOT 29807104 with the prior 15M EXHAUSTED honest-label pins; all 24
  probed rows two-pass payload-gated; the 3 WIN ties regression-gated
  against BASE; all 21 adopted (lo,hi) fresh to BASE, absent from the
  active quarantine registry 81d23160, canonical-safe per
  s5_evidence_policy.
* Merger = published byte-clone s5_union_merge.py (90711961...): 3
  merge runs, all outputs byte-identical, audits f4304731... x3; MERGED
  unique=6,792 dup_elided=0 WIN=192 LOSS=6,600, zero conflicts.
* Refresh fork refresh_adoption_emloss21.py (cc01b3d8...) = byte-clone
  of the published Part EV dossier fork f2edac3e... differing in
  EXACTLY the three regions (docstring, the CACHE path, the expected
  cache sha); the computation region is byte-identical (asserted
  mechanically).  Executed twice (58.1s / 58.3s, one process at a
  time): all four outputs byte-identical across the two runs.

## Integration path for the declaring Part session

A future Part may declare the emloss21 loss adoption pinning the
dossier bytes above directly.  The declaring Part still owes, per the
EM/EP/ER/EU/EV adoption pattern: declared adopt-eligibility gates (all
21 rows fresh vs the then-current head, quarantine check, kit
re-verification against published bytes), its own fail-closed
extractor recomputing the census deltas from published bytes
(structural clone of compare_deltas_em_adoption.py; the dossier's
measure_census_deltas_emloss21.py is the measurement reference, not a
substitute), and the log entry.  Consuming the 21 LOSS labels asserts NO
root verdict and NO 11x11 outcome; the census flips NOTHING (zero
status flips measured).  If the canonical head has moved beyond
63f33c4f... by then, this dossier's scenario pins must be re-derived,
not patched.

## Pins

* BASE: merged-exact-s5-chain-plus-evwin4 63f33c4f... (6,771 rows WIN
  192 / LOSS 6,579); EV dossier reaudit outputs refresh-summary
  1fafd081... / closure-classes 6ba51faa... / per-root-coverage
  d9eee976... / worklist regen ca50cb68... (3,717,416 B).
* Source kits: batch-5 README 1f69bfb1... / keys 57da4702... / status
  c473e32c... / 36 raw pins in the manifest; Part ES MANIFEST
  cc987739... (38 files) / README 67ab379d... / targets-30m 1c27a238...
  / status 4b597320...; b38 SSOT keys 29807104....
* Frozen environment: dependency-graph 54f9c364..., update8 b658290a...,
  Board 954d3a10..., policy 78655e94..., quarantine 81d23160....
