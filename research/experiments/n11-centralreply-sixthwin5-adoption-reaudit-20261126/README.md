# n11-centralreply-sixthwin5-adoption-reaudit-20261126 (Part EW, 2026-11-26)

Part EW: the sixthwin5 WIN-ONLY canonical adoption in the central-reply
chain.  The 5 unconsumed sixth-cost exclusive-probe exact-WIN rows of
the probe kit
n11-sixthcost-class-s5-exclusive-probe-10376293541461626880-20261121
(class 10376293541461626880:65536, s4 class 3077, coverage
{80,84,100,108}, budget 15,000,000 order 0, first stage 2,000,000) are
consumed into the canonical merged exact-S5 chain cache as WIN labels:

* k02 (34 stones, s5 index 64872, key 1297036692683751424:68157440,
  7,717,432 nodes) - corroborated by the ea73c3e3 fixed third
  implementation's 4-run witness;
* k03 (9,255,414 nodes), k04 (9,433,024), k05 (13,397,611) and k08
  (6,195,897) - corroborated by the TI third-implementation audits'
  verdict-level WIN agreement (the TI replicas' raws byte-identical to
  the probe kit's).

Every row is two-pass fresh-cold node-exact at 15M plus a voluntary
third cold verify run.  Adopted node total: 45,999,378 (bookkeeping
only; nodes are never verdicts).  NO new solver pass runs in this
Part.

Nothing here asserts any root verdict and no 11x11 outcome: a WIN
canonical adoption transfers NO verdict to any central-reply root;
owner classes of the adopted keys leave live status by the win-hit
mechanism only (exactly 8 classes flip unknown -> excluded_now; NO
class is freed).  After the adoption 34,409 S4 classes remain
status-unknown.  The standard 11x11 empty board and every
central-reply root stay UNKNOWN.

## chain position

* BASE = the Part EM merged chain head 6e49dd84... (6,792 rows, WIN
  192 / LOSS 6,600), published at the Part EM pre-declaration dossier
  kit path.
* increment = `output/increment-sixthwin5-adoption-20261126.cache` (5
  WIN rows, sha256
  efee7b9e3b377aabbd5cb3606b84739be7f87aff8ddd4bffafc9d22fa557e6be),
  row region byte-identical to the pre-declaration dossier increment
  44c16a28...; the Part increment supersedes the dossier "PREDECL
  DOSSIER" header (disclosed; the header comment block is the only
  differing region).  SSOT-extracted per-row pins in
  `output/increments-manifest.json` (schema
  sixthwin5-adoption-increments-manifest-v1, sha256 a7376780...).
* merged head of record = the PUBLISHED dossier file
  `research/experiments/n11-centralreply-sixthwin5-adoption-predecl-20261126/output/merged-exact-s5-chain-plus-sixthwin5-20261126.cache`
  (6,797 rows, WIN 197 / LOSS 6,600, sha256 16a12390...).  This Part
  does NOT republish that file; the fail-closed union merger
  byte-clone (90711961...) reproduces it deterministically from BASE +
  the Part increment (3/3 byte-identical runs, audits
  merge-audit-run1/2/3.json all sha256 b404c248..., unique_rows 6,797,
  WIN 197 / LOSS 6,600, conflict-free).

## WIN label eligibility (fail-closed, machine-verified)

The maker `scripts/make_increments_sixthwin5_adoption.py` (sha256
9e6bf992...; structural clone of the published pre-declaration dossier
maker 424edee4..., computation region byte-identical logic, disclosed
diff: docstring, emitted header, output names, manifest Part /
supersession fields and the added dossier-supersession byte gates)
re-verifies every gate before emitting a single row (fail-closed; rc=1
on ANY drift):

1. the probe kit (which predates the repo MANIFEST convention) is
   consumed via direct sha256 pins: README, the selection JSON, the
   k08 win-finding JSON, status.log, the 5 target input CSVs and all
   20 raw CSV files (raw_file_sha256_pins / input_csv_sha256_pins in
   the manifest; each target input CSV is byte-equal to the Part SK
   kit's MANIFEST-pinned gate input and to the TI kit's
   MANIFEST-pinned input);
2. the Part SK C++ second-implementation gate kit verified
   file-by-file against its published MANIFEST-sha256 8d84b1a5...
   (46/46 files; the gate table 178 rows with 11 GATE-PASS rows;
   any C++ disagreement fails closed in favor of discarding the row);
3. the TI third-implementation verdict re-verification kit pinned by
   its MANIFEST 538f8ec7... (344 lines): verdict-level WIN(1)
   agreement for k03/k04/k05/k08 with determinism triplets and
   replica-unanimous rows (k08's replica raw records the first-stage
   2M incomplete marker before the three full-budget WIN replays);
   the TI audits' replica raws are byte-identical to the probe kit's;
4. the ea73c3e3 fixed third implementation re-verifies k02's WIN(1)
   on 4 witness runs (a/b/g/v, 9,106,337 expansions each;
   expansions legitimately differ from the replica's node count -
   verdict-level agreement, the same rule the TI audits apply);
5. all 5 adopted pairs proven fresh to BASE (unique_new 5,
   base_cache_absent_hits_for_emitted 0; NO WIN regression ties this
   time, win_ties = [] - unlike emloss21's f017/ai007/ai040), absent
   from the active quarantine registry 81d23160... and canonical-safe
   per s5_evidence_policy 78655e94...; the adopted-table digest
   b6ea1bcc... and the emitted increment sha self-pinned;
6. the published dossier kit bytes re-pinned (increment 44c16a28...,
   manifest 25defefa..., maker 424edee4..., merged 16a12390...) and
   the emitted rows cross-gated row-for-row against the dossier rows.

NOT consumed and NOT emitted: the 3 standing honest LOSS labels of the
same ladder (k01 15M 10,369,650; k06 15M 8,182,231; k07 2M
1,419,823) and every later third-impl batch WIN row (k13/k19 etc.,
parked4 L50M ladder).  No batch key was re-searched at any condition.

## reaudit (Board fail-closed child verification + census cross-check)

The kit extractor `scripts/compare_deltas_sixthwin5_adoption.py`
(sha256 cfefe839...; fork of the published Part EM extractor
b9a74915..., structural clone, disclosed diff: docstring, adopted
table, both refresh sides, manifest decomposition fields, the
win-hit flip expectations replacing the loss-only zero-flip
assertion, serving-class status expectations, dossier-supersession /
dossier-maker re-execution sections and pinned expectations)
recomputes from published bytes only, fail-closed:

* BOTH published refresh forks re-executed byte-verbatim in isolated
  scratch trees: the emloss21 dossier refresh fork cc01b3d8...
  (refresh_adoption_emloss21.py) against BASE, and the sixthwin5
  dossier refresh fork 92a884c9... (refresh_adoption_sixthwin5.py;
  byte-clone of cc01b3d8... differing in EXACTLY docstring, CACHE
  path and expected cache sha) against SCEN; all eight outputs
  byte-identical to the published / regenerated pins (BASE
  refresh-summary 7f379b71..., closure-classes 68628134...,
  per-root-coverage 9c5b2774...; SCEN refresh-summary 295027cf...,
  closure-classes 350e269a..., per-root-coverage 9c5b2774... - the
  latter byte-identical to BASE's, measured); the probe-worklists
  stay UNPUBLISHED per the size policy, entering only as regen pins
  (BASE 147b62d6... 3,715,963 B / SCEN 82f9e517... 3,715,904 B)
  re-verified by the byte-verbatim re-execution;
* the published dossier maker make_increments_sixthwin5.py
  (424edee4...) is RE-EXECUTED byte-verbatim in an isolated scratch
  tree (rc=0, byte-identical increment 44c16a28... and manifest
  25defefa...), re-proving live, from published bytes only, the
  entire Part EW adopt-eligibility evidence chain the dossier maker
  encodes;
* SCEN == BASE rows + exactly the 5 Part increment rows (6,797 rows
  WIN 197 / LOSS 6,600, verdict agreement everywhere); no adopted key
  intersects the prior Part EM kit increment 3e6e9bf0... (no
  re-adoption);
* the independent full-class census reproduces the published class
  status counts EXACTLY on both sides (BASE 34,417/103/39/390 ->
  SCEN 34,409/111/39/390) with EXACTLY 8 status flips, ALL unknown ->
  excluded_now by the win-hit mechanism, and the flipped set is
  EXACTLY the owner classes of the 5 adopted keys that were unknown
  at BASE {774, 1387, 2169, 2339, 3077, 16734, 25845, 30329}; the
  remaining owner class 30354 was already excluded_now and keeps its
  status; NO class is freed and NO class moves in any other
  direction;
* serving-class Board arithmetic recomputed from the frozen graph:
  class 3077 (raw boundary 108, cost size 100) cost-unknown 100 -> 95
  (exactly the 5 adopted keys, all owned there); its status flips
  unknown -> excluded_now, the dossier-measured serving transition;
* closure-classes.csv 804 -> 804: ZERO rows leave, ZERO rows enter;
  the unknown_now churn is exactly {16734: 92 -> 91} and the rank
  churn is EMPTY (0 re-ranked rows); NO groups_served churn; every
  other field of every common row is byte-identical;
* update8 refresh: resolved 280 -> 281 (the newly resolved set is
  EXACTLY the single adopted s5 index k02/64872, the only adopted key
  inside the frozen update8 baseline requirement; the other four
  adopted keys - 39127, 91506, 96472, 112201 - were first probed
  AFTER the baseline froze and are correctly not in it; measured,
  disclosed), remaining 31,445 unchanged, groups_free_now stays 131,
  union baseline stays 31,859, win_hit groups 25 -> 25 IDENTICAL
  sets;
* per-root coverage byte-identical on both sides (free_now/uncovered
  identical at all 20 roots; individual greedy union UNCHANGED at all
  20 roots); Board verification 39/39 with zero rejections on both
  sides;
* the published dossier census measurement
  census-deltas-sixthwin5-predecl.json fd684d83... is machine
  cross-compared field-by-field against the extractor's own
  independent recount: EXACT agreement on both cache identities,
  census counts, the 8-flip set, closure churn, per-root greedy
  deltas (none), joint greedy, worklist totals, update8 numbers
  incl. the single-key newly-resolved set and the 4 out-of-baseline
  keys, win_hit identity, serving-class records, the owner histogram
  and the 5-row adopted table with owner sets (its dossier-time
  verdict-scope fields part_declared=false / consumed=NOTHING are
  superseded by this Part declaration; disclosed, not asserted
  here).

Scheduling bookkeeping measured by the extractor (no coverage claim):
joint greedy 35,155 -> 35,155 UNCHANGED, worklist 64,277 -> 64,276
(-1 = exactly the one newly resolved in-requirement key),
group_best_options_nonfree 2,101 static, unique_groups 2,115 static,
update8 resolved 280 -> 281.

The extractor's full battery output is
`output/decomp-deltas-sixthwin5-adoption.json` (sha256 48913dc4...,
schema sixthwin5-decomp-deltas-v1).  The extractor ran twice with
byte-identical stdout and decomp; a 3-mode tamper battery (increment
row / merge-audit / manifest mutations, each restored and re-verified)
all failed closed rc=1 (recorded in the declaration log, not
published as kit files).

## Session honesty note

The maker and extractor were prepared inside this session as staged
structural forks of the published Part EM kit scripts; a context
compaction hit mid-fork (a draft-stage loss).  Every final kit byte
was re-staged from the published EM kit files and re-verified against
all published pins before the recorded runs; nothing in the kit
depends on the lost draft.  The staged transformation files are not
part of the kit.

## Publication record (publish-then-execute; fetch-back byte-verified)

* declaration 7fcf9dde: pre-registered every kit byte pin;
* wave B 9bd8d586: scripts/s5_union_merge.py byte-clone +
  scripts/make_increments_sixthwin5_adoption.py +
  scripts/compare_deltas_sixthwin5_adoption.py (one commit, 3 files);
* wave C 5f05a14a: the six output files (increment, manifest,
  merge-audit-run1/2/3, decomp; one commit);
* wave D (this commit): kit README + MANIFEST-sha256;
* each wave fetch-back byte-verified against the pre-registered pins
  (sha256 sums listed in MANIFEST-sha256.txt are the exact published
  bytes; no trailing-LF repair was needed this time, unlike the Part
  EM wave-C incident).

## Interpretation guard

Consuming the 5 WIN labels asserts NO root verdict, NO root-class
verdict and NO 11x11 outcome.  No class is freed; 8 owner classes
flip unknown -> excluded_now by the win-hit mechanism only.  The
k01/k06/k07 standing LOSS rows, the k13/k19 parked4 WIN rows and every
other unconsumed probe-level label stay in NO cache.  No
free-coverage, secured-coverage or root-resolution claim is made
anywhere in this Part.  Nodes are bookkeeping, never verdicts.  The
standard 11x11 empty board and every central-reply root stay UNKNOWN.
