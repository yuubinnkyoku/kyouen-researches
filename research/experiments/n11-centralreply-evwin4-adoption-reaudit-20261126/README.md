# n11-centralreply-evwin4-adoption-reaudit-20261126 (Part EV, 2026-11-26)

Part EV: the FOURTH WIN canonical adoption in the central-reply chain.  The
4 gate-verified closure-batch WIN rows (2026-11-22 closure batches 1/3/4/5;
15M two-pass fresh-cold node-exact replica raws; third-impl a/b verdict-level
corroboration; C++ second-implementation scrutiny gate 2026-11-25) are
consumed into the canonical merged exact-S5 chain cache as WIN verdicts:

| key | class | s5_index | hi | legal | result | nodes |
| --- | --- | --- | --- | --- | --- | --- | --- |
| b018 | 16757 (batch-1, dual-class) | 528497 | 65536 | 60 | WIN(1) | 3,549,602 |
| d002 | 20421 (batch-3) | 197253 | 131072 | 73 | WIN(1) | 5,359,994 |
| e002 | 16371 (batch-4) | 183566 | 16 | 79 | WIN(1) | 14,112,632 |
| f017 | 12264 (batch-5) | 415095 | 70368744177666 | 82 | WIN(1) | 3,522,635 |

Adopted node total: 26,544,863 (bookkeeping only; nodes are never
verdicts).  NO new solver pass runs in this Part.

Nothing here asserts any root verdict and no 11x11 outcome: a WIN
canonical adoption transfers NO verdict to any central-reply root.
Exactly 13 classes flip UNKNOWN -> excluded_now (a known WIN cost child
ends free all-LOSS coverage); 34,417 S4 classes remain status-unknown.
The standard 11x11 empty board and every central-reply root stay
UNKNOWN.

## chain position

* BASE = the Part EU canonical merged chain head 3ba48608...
  (6,767 rows, WIN 188 / LOSS 6,579), published in the Part EU kit
  output/merged-exact-s5-chain-plus-euwin2-20261125.cache.
* increment = `output/increment-evwin4-20261126.cache` (4 WIN rows,
  sha256 7f125610...), row region byte-identical to the dossier predecl
  increment 8d0e43ed...; the Part increment supersedes the dossier
  "PREDECL DOSSIER STATUS" header (disclosed).  SSOT-extracted per-row
  pins in `output/increments-manifest.json` (schema
  evwin4-increments-manifest-v1, sha256 f013a8f5...).
* merged head of record = the PUBLISHED dossier file
  `research/experiments/n11-centralreply-evwin4-adoption-predecl-20261126/output/merged-exact-s5-chain-plus-evwin4-20261126.cache`
  (6,771 rows, WIN 192 / LOSS 6,579, sha256 63f33c4f...).  This Part does
  NOT republish that file; the fail-closed union merger byte-clone
  (90711961...) reproduces it deterministically from BASE + the Part
  increment (3/3 byte-identical runs, audits merge-audit-run1/2/3.json all
  sha256 d9713aed..., unique_rows 6,771, conflict-free).

## WIN label eligibility (fail-closed, machine-verified)

The maker `scripts/make_increments_ev_win4_adoption.py` re-verifies every
gate before emitting a single row (fail-closed; rc=1 on ANY drift):

1. EV gate kit MANIFEST 34d7768b... verified file-by-file; SSOT registry
   gate-rows-ev.json 3ba154f2... whose target quadruples equal the
   batch-keys SSOT, the batch raws, the gate raws and the ADOPTED table;
2. audit 0327dad8... (schema n11-centralreply-cppgate-wins41164-audit-v1,
   overall PASS, 7/7 GATE-PASS, 4/4 byte-identical audit re-runs), gate
   source kyouen_dfpn_root.cpp 9193f5b6... at commit
   154f3b7a67b97e13acbaee8b04dc74ddca728d19;
3. the 4 closure-batch kits re-hashed file-by-file against the registry
   batch_source_pins (20 files); the thirdimpl kit re-hashed 96/96
   against MANIFEST c5ed4414...;
4. the EU regression tie is carried: both Part-EU rows (increment
   d9365d80...) already sit WIN in BASE with identical nodes and are NOT
   re-adopted; every adopted (lo,hi) is absent from BASE (fresh
   exact-WIN rows, no key outside the adopted set) and from the
   quarantine registry 81d23160....

NOT consumed (each stays in NO cache): the 21 unconsumed closure-batch
LOSS rows (EM-pattern loss-adoption territory), the k04 sixth-cost WIN
and every other unconsumed probe-level WIN.  No batch key was
re-searched at any condition.

## reaudit (Board fail-closed child verification + census cross-check)

The kit extractor `scripts/compare_deltas_ev_adoption.py` (sha256
70a5b207...; structural clone of the published Part EU extractor
9bc5f06a...) re-executed BOTH published refresh forks byte-verbatim in
isolated scratch trees: the Part EU kit fork
`research/experiments/n11-centralreply-euwin2-adoption-reaudit-20261125/reaudit/scripts/refresh_adoption_eu.py`
(6dc24c15...) against BASE, and the dossier kit fork
`n11-centralreply-evwin4-adoption-predecl-20261126/reaudit/scripts/refresh_adoption_evwin4.py`
(f2edac3e..., byte-clone of 6dc24c15... differing only in docstring/CACHE
path/expected sha) against SCEN.  All EIGHT outputs byte-identical to
the declaration pins: BASE side refresh-summary 2b70bb55...,
closure-classes 59a4c85f..., per-root-coverage cfc2bfe1... plus
probe-worklist regen pin 397a4379... (3,717,712 B, NOT published, size
policy); SCEN side refresh-summary 1fafd081..., closure-classes
6ba51faa..., per-root-coverage d9eee976... plus probe-worklist regen
pin ca50cb68... (3,717,416 B, NOT published, size policy).  The
published dossier census-deltas-evwin4-predecl.json ab97fba9... is
machine cross-compared field-by-field against the extractor's own
independent recount (its dossier-time verdict-scope fields are
superseded by the Part declaration; disclosed, not asserted here).

Run records (this Part, all from published bytes):

* extractor full battery rc=0 TWICE consecutively (wall about 2m04s
  each), stdout byte-identical, decomp-deltas-evwin4-adoption.json sha256
  c05f11cd... byte-identical across both runs;
* merger reproduces the dossier merged head 63f33c4f... 3/3
  byte-identical runs with conflict-free audits;
* tamper battery (recorded): extractor increment-sha pin mutation ->
  ABORT "sha drift" (increment); b018 adopted-node expectation mutation ->
  ABORT "manifest adopted row drift: b018"; census after-count
  expectation mutation (34,417 -> 34,418) -> ABORT "independent census
  after-drift vs the published SCEN counts"; all fail-closed, clean rerun
  restored the byte-identical decomp.

The battery re-derived from published bytes: SCEN == BASE rows + exactly
the 4 increment rows (WIN 192 / LOSS 6,579); census 34,430/90/39/390 ->
34,417/103/39/390 with EXACTLY 13 UNKNOWN -> excluded_now flips
{4864, 4903, 5255, 5282, 5613, 6030, 12264, 12327, 14776, 15640, 16371,
16757, 20421} and no double-flip at 30345/30354; closure 805 -> 805 zero
rows left/entered, unknown_now churn {16371: 2->1, 16757: 3->2,
30345: 5->4, 20421: 6->5, 12264: 51->50} and the exact 7-row rank churn
{23101: 1->2, 1849: 2->3, 2251: 3->4, 16371: 4->1, 13342: 11->12,
30118: 12->13, 12264: 13->11}; update8 resolved_count 260 -> 263,
remaining_now 31,505 -> 31,445, groups_free_now 131 static, union
baseline 31,859; win_hit_groups 10 -> 25 (the 10 BASE class-30354
quartets identical, exactly 15 new groups joining: classes 12264 x 6,
16757 x 5, 20421 x 4; zero removed); Board verification 39/39 both
sides, zero rejections; per-root free_now/uncovered identical at all 20
roots + baseline, individual greedy changes only at roots
{0: 2980->2789, 36: 3005->2951, 12: 2848->2846, 48: 2895->2893,
5: 2884->2883, 37: 3620->3619}; joint greedy 36,619 -> 36,618;
group_best_options_nonfree 2,105 static; worklist 64,307 -> 64,302.
Pure scheduling bookkeeping; no coverage claim.

## Publication record (publish-then-execute; fetch-back byte-verified)

* declaration 10fea2ee: pre-registered every kit byte pin below;
* wave B1 511e0feb: scripts/s5_union_merge.py byte-clone;
* wave B2 06df8b0e: scripts/make_increments_ev_win4_adoption.py +
  scripts/compare_deltas_ev_adoption.py;
* wave C a46c3a14: the 6 output files;
* each wave fetch-back byte-verified against the pre-registered pins
  (sha256 sums listed in MANIFEST-sha256.txt are the exact published
  bytes).

## Interpretation guard

Consuming the 4 WIN labels asserts NO root verdict, NO root-class
verdict and NO 11x11 outcome.  34,417 S4 classes remain status-unknown.
The 21 unconsumed closure-batch LOSS rows, k04 and every other
unconsumed probe-level WIN stay in NO cache.  No free-coverage,
secured-coverage or root-resolution claim is made anywhere in this Part.
The standard 11x11 empty board and every central-reply root stay
UNKNOWN.
