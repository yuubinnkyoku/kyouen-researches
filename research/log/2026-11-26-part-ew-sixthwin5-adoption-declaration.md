# Part EW declaration: sixthwin5 WIN-only canonical adoption (publish-then-execute)

Date: 2026-11-26 (long-term lane session)
Scope: the 5 UNCONSUMED sixth-cost exclusive-probe exact-WIN rows
k02 / k03 / k04 / k05 / k08 of the sixthwin5 pre-declaration dossier
kit (commits 02aa442b, 83711340, 622fb365, 52826b45), probe kit
n11-sixthcost-class-s5-exclusive-probe-10376293541461626880-20261121,
class 10376293541461626880:65536 (s4 class 3077, coverage
{80,84,100,108}), budget 15,000,000 order 0 (first stage 2,000,000),
two-pass fresh-cold node-exact plus a voluntary third cold verify run
each; k02 7,717,432 / k03 9,255,414 / k04 9,433,024 / k05 13,397,611 /
k08 6,195,897 nodes.  Adopted node total 45,999,378 (bookkeeping, never
verdicts).  This is a WIN-only canonical adoption: NO LOSS row is
adopted.  NOT consumed and NOT emitted: the 3 standing honest LOSS
labels of the same ladder (k01 15M 10,369,650, k06 15M 8,182,231,
k07 2M 1,419,823) and every later third-impl batch WIN row (k13/k19
etc., parked4 L50M ladder) stays in NO cache.

## Pre-registered kit shas (published in this Part's kit after this log)

Increment (5 s5verdict rows, verdict=1; header supersedes the dossier
increment with the Part EW adoption header; row region byte-identical
to the dossier increment
44c16a28f944e255d3968f49a16cc61e06f70269ada833fe976f1607b7d40b03):
- output/increment-sixthwin5-adoption-20261126.cache =
  efee7b9e3b377aabbd5cb3606b84739be7f87aff8ddd4bffafc9d22fa557e6be

Manifest (schema sixthwin5-adoption-increments-manifest-v1):
- output/increments-manifest.json =
  a7376780687fbacb0a9a958a94de0df4634d4512bb08d1631b36772a9c78ba86

Merge audits (3 byte-identical runs; BASE 6e49dd84 6,792 rows + Part
increment 5 rows -> merged 6,797 rows WIN 197 / LOSS 6,600, output
byte-identical to the published dossier merged cache
16a12390c0c3f046f0ae537b2a9940e15661263fc5034ce1b155c138bb9043cd,
which stays the merged cache of record and is NOT republished here):
- output/merge-audit-run{1,2,3}.json =
  b404c2483988daac71c88de54f29962cfea90ab5b4c85fbf81697d5dab4e720a (x3)

Decomp (fail-closed extractor output, schema
sixthwin5-decomp-deltas-v1; 2 runs rc=0 with byte-identical stdout):
- output/decomp-deltas-sixthwin5-adoption.json =
  48913dc4cb09aeebceb9e158dda02b913b12e0534f05b3e1639225576786ccc5

Kit scripts (structural clones; byte-clone for the merger):
- scripts/compare_deltas_sixthwin5_adoption.py (own fail-closed
  extractor; fork of the published Part EM extractor
  b9a74915d0aa5690898f64b6fae5eeba8c87ebcb761dd7cdc680bdeb8c8f228c) =
  cfefe839fcebfc89155e3fa9232f962174930a4ec9aaa07277ef2abdff7b3ee3
- scripts/make_increments_sixthwin5_adoption.py (structural clone of
  the published dossier maker
  424edee4116ab785376d5fe5d197599b1574b71a46cf847d90a291dd27f99558;
  computation region byte-identical) =
  9e6bf99249339e94aa85257a0e74e2b102a03c8b2a2d3f11904c960de45f80f5
- scripts/s5_union_merge.py (byte-clone of the published merger,
  identical to the Part EM kit pin) =
  907119610034fb2aebfde012550a4129dfa3b086c6de11194e856747ac74606a

## Base / scenario identity

- BASE (head of record at declaration) = the Part EM merged exact-S5
  chain cache
  6e49dd841b7bfcb335d86ef2479c95f47ab7acbcf41ace389a8b8eb95c778c9d
  (6,792 rows WIN 192 / LOSS 6,600), published at the Part EM
  pre-declaration dossier path.  Unchanged by this Part.
- SCEN (canonical head after Part EW) = byte-identical to the published
  dossier merged cache 16a12390... above: BASE rows + exactly the 5
  Part increment rows, verdict agreement everywhere, NO
  base-cache-absent hits, quarantine 0.  All 5 adopted keys are fresh
  to BASE: no WIN regression ties this time (unlike emloss21's
  f017/ai007/ai040), recorded win_ties = [].

## Adopt-eligibility gates (all declared, all re-verified live twice)

All 5 rows were re-verified against published bytes by the Part maker
(live re-check) AND again during the extractor run by the
byte-verbatim re-execution of the published dossier maker
(424edee4..., rc=0, increment + manifest reproduced byte-identically),
which re-encodes: probe-kit direct sha pins (README, selection JSON,
the k08 win-finding JSON, status.log, 5 target input CSVs and all 20
raw CSV files), the Part SK C++ second-implementation gate kit
(MANIFEST 8d84b1a5..., 46/46 files, gate table 178 rows / 11 GATE-PASS
for the adopted targets), the TI third-implementation verdict
re-verification kit (MANIFEST 538f8ec7..., verdict-level WIN agreement
for k03/k04/k05/k08 with determinism triplets and replica-unanimous
rows incl. the k08 first-stage 2M incomplete marker), the ea73c3e3
fixed third implementation's 4-run k02 witness, the fresh-to-BASE /
quarantine / canonical-safety gates and the adopted-table digest
b6ea1bcc...; every adopted row's replica raw bytes are byte-identical
across the probe kit and the TI audits.  The Part increment is
row-for-row disjoint from the prior Part EM kit increment
3e6e9bf0a5f410a1d584889832f21352dd01a97aef5a899de06a28373fcaef82
(no re-adoption of any consumed row).

## Measurements (declared, verified fail-closed by the extractor)

- Census flips: EXACTLY 8, ALL unknown -> excluded_now, win-hit only,
  and exactly the owner classes of the 5 adopted keys that were
  status-unknown at BASE: {774, 1387, 2169, 2339, 3077, 16734, 25845,
  30329}; the remaining owner class 30354 (k02) was already
  excluded_now and keeps its status.  Census 34,417/103/39/390 ->
  34,409/111/39/390.  NO class is freed (none moves to free_now).  The
  published dossier census measurement
  fd684d83c689452f0da7dca2ec2cb5b6501f03b9f5d2b30c30fbcf0590f5ba5f is
  cross-checked field-by-field (agreement exact).
- Serving class 3077: cost-unknown 100 -> 95 (exactly the 5 adopted
  keys, all owned there; raw Board boundary 108, cost size 100); its
  status flips unknown -> excluded_now (the win-hit mechanism,
  measured dossier-side).
- Closure-classes.csv: 804 -> 804, ZERO rows enter or leave; the only
  unknown_now churn is {16734: 92 -> 91}; rank churn EMPTY (0
  re-ranked rows); groups_served churn 0.
- Frozen update8 refresh: resolved 280 -> 281 (newly resolved =
  exactly k02's s5 index 64872; the other 4 adopted keys - s5 39127 /
  91506 / 96472 / 112201 - sit OUTSIDE the frozen baseline requirement
  and are correctly not counted, measured, disclosed), remaining
  31,445 unchanged, groups_free_now 131, union baseline 31,859,
  win_hit groups 25 -> 25 IDENTICAL sets.
- Per-root: free_now/uncovered identical at all 20 roots (per-root
  coverage byte-identical on both sides); individual greedy union
  UNCHANGED at all 20 roots; joint greedy 35,155 -> 35,155 UNCHANGED;
  unique groups 2,115 -> 2,115; group_best_options_nonfree 2,101 ->
  2,101; worklist 64,277 -> 64,276 (-1, exactly the one newly resolved
  in-requirement key).  All scheduling bookkeeping, no coverage claim.
- Extractor battery: 2 runs rc=0 with byte-identical stdout + decomp;
  3-mode tamper battery (increment row / merge-audit / manifest
  mutations) all fail-closed rc=1 with byte-verified restore (recorded
  here, not published as kit files).

## Session honesty note

The Part maker and extractor were prepared inside this session as
staged structural forks of the published Part EM kit scripts; a
context compaction hit mid-fork (a draft-stage loss).  Every final kit
byte was re-staged from the published EM kit files and re-verified
against all published pins before the recorded runs; nothing in the
kit depends on the lost draft.  The staged transformation files are
not part of the kit.

## Verdict scope and status

Consuming the 5 exact-WIN labels asserts NO root verdict, frees no
class and makes no coverage claim; owner classes leave live status by
the win-hit mechanism only.  The standard 11x11 empty board and every
central-reply root stay UNKNOWN.  k01/k06/k07 LOSS rows and every
unconsumed probe-level WIN (k13/k19 etc.) stay in NO cache.  Nodes are
bookkeeping, never verdicts.

Next waves (B scripts, C outputs, D kit README + MANIFEST-sha256,
F completion log advancing the head of record
6e49dd84 -> 16a12390 at the published dossier path) follow
publish-then-execute with fetch-back byte verification per wave.
