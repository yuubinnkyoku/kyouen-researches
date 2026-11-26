# Part EM declaration: emloss21 loss-only canonical adoption (publish-then-execute)

Date: 2026-11-26 (long-term lane session)
Scope: the 21 UNCONSUMED closure-batch exact-LOSS rows of the emloss21
pre-declaration dossier kit (commit c77e79ab) - 17 batch-5 class-12264
rows (f001..f016, f018, budget 15M, nodes 58,253,401) and 4 Part ES
class-30345 reprobe30m rows (ai024/ai030/ai038/ai041, budget 30M,
nodes 71,265,013).  Adopted node total 129,518,414 (bookkeeping kinds,
not a work claim).  This is a LOSS-only canonical adoption: NO WIN row
is adopted, no source-batch WIN is re-readopted.

## Pre-registered kit shas (published in this Part's kit after this log)

Increment (21 s5verdict rows, header supersedes the dossier increment
with the Part EM adoption header; row region byte-identical to the
dossier increment 47443dc143c157ab972de0f39f2cf3afb5d062e209da9dcd8e486f0a57c8ebca):
- output/increment-emloss21-adoption-20261126.cache =
  3e6e9bf0a5f410a1d584889832f21352dd01a97aef5a899de06a28373fcaef82

Manifest (schema emloss21-adoption-increments-manifest-v1):
- output/increments-manifest.json =
  bd4b9e766d0806f60a6df1ec4e91076fa7564486caeadfc222a16baabca6c01d

Merge audits (3 byte-identical runs; BASE 63f33c4f 6,771 rows + Part
increment 21 rows -> merged 6,792 rows WIN 192 / LOSS 6,600, output
byte-identical to the published dossier merged cache
6e49dd841b7bfcb335d86ef2479c95f47ab7acbcf41ace389a8b8eb95c778c9d,
which stays the merged cache of record and is NOT republished here):
- output/merge-audit-run{1,2,3}.json =
  17a390e78f603de0bc20577f9f1f75b5016fd818af1acb58db835f5add49801f (x3)

Decomp (fail-closed extractor output, schema
emloss21-decomp-deltas-v1; 2 runs byte-identical stdout):
- output/decomp-deltas-emloss21-adoption.json =
  c1bf58814cfc5d65ecbe6130c996aa060c3715f918c97a4ee33f583bc74cf02e

Kit scripts (structural clones; byte-clone for the merger):
- scripts/compare_deltas_em_adoption.py (own fail-closed extractor;
  fork of the published EV extractor 70a5b207...) =
  b9a74915d0aa5690898f64b6fae5eeba8c87ebcb761dd7cdc680bdeb8c8f228c
- scripts/make_increments_emloss21_adoption.py (structural clone of the
  published dossier maker 74fbbfd9a206a28e1bcdf2d52ceb884bf71c5aee62ec0eefe520a41cd33d8035;
  computation region byte-identical) =
  cd603627520fc5115fd0a9002b5595e70d0c0770ea76ad75e7d07cd60f7dc423
- scripts/s5_union_merge.py (byte-clone of the published merger,
  identical to EV kit pin) =
  907119610034fb2aebfde012550a4129dfa3b086c6de11194e856747ac74606a

## Base / scenario identity

- BASE (head of record at declaration) = the Part EV head merged exact-S5
  chain cache 63f33c4f620583449641102026b261c559ae5ecc29713cd6445d6fe9369858f0
  (6,771 rows WIN 192 / LOSS 6,579), published at the Part EV pre-declaration
  dossier path.  Unchanged by this Part.
- SCEN (canonical head after Part EM) = byte-identical to the published
  dossier merged cache 6e49dd84... above: BASE rows + exactly the 21
  Part increment rows, verdict agreement everywhere, NO
  base-cache-absent hits, quarantine 0.

## Adopt-eligibility gates (all declared, all re-verified live twice)

All 21 rows were re-verified against published bytes by the Part maker
(live re-check) AND again during the extractor run by the
byte-verbatim re-execution of the published dossier maker
(74fbbfd9..., rc=0, increment + manifest reproduced byte-identically),
which re-encodes: batch-5 kit direct sha pins (39/39 consumed files),
Part ES kit MANIFEST cc987739... 38/38, the b38 batch-keys SSOT
29807104... cross-gate with the prior 15M EXHAUSTED honest-label pins
for all 6 ES targets, the f017/ai007/ai040 WIN regression ties against
BASE (identical nodes, consumed by Parts EV/EU, NOT re-adopted here),
the fresh-to-BASE / quarantine / canonical-safety gates and the
adopted-table digest 4fd8723e....
The Part increment is row-for-row disjoint from the Part EV kit
increment 7f1256108d697bd96d473e55a5509dea35f4c0b1be45893cac3f667c4b3f55c4
(no re-adoption of any consumed row).

## Measurements (declared, verified fail-closed by the extractor)

- Census flips: ZERO.  Class statuses identical on both sides
  (34,417 unknown / 103 excluded_now / 39 free_now / 390 excluded);
  the published dossier census measurement
  d67b6e9bcf55a601afdc177aa804f2be2b8d4fd6ec9d76ac6389fa5b913edcd3
  cross-checked field-by-field (agreement exact).
- Serving classes: class 12264 cost-unknown 50 -> 33 (the 17 batch-5
  keys consumed; closure rank 11 -> 9), class 30345 cost-unknown 4 -> 0
  (its 4 remaining unknown closure children consumed; the class EXITS
  the closure-classes ranking 805 -> 804, exited=[30345], entered=[];
  both classes KEEP their excluded_now status from the EP/EU/EV chain - NOT flipped).
- Frozen update8 refresh: resolved 263 -> 280 (newly resolved = exactly
  the 17 batch-5 s5 indices), remaining 31,445 unchanged, win_hit groups
  25 -> 25 IDENTICAL sets.
- Closure-classes churn: unknown_now {6518: 61->60, 6547: 58->57,
  9478: 61->60, 12235: 61->60, 12264: 50->33}; 763 rows re-ranked
  (dense-rank bookkeeping); groups_served churn 0.
- Per-root: free_now/uncovered identical at all 20 roots; greedy union
  changes only at 6 roots {49, 38, 16, 5, 36, 12}; joint greedy
  36,618 -> 35,155 (-1,463, the largest single scheduling reduction of
  any pending adoption pool measured so far); worklist 64,302 -> 64,277
  (-25).  All scheduling bookkeeping, no coverage claim.
- Extractor battery: 2 runs rc=0 with byte-identical stdout + decomp;
  3-mode tamper battery (increment row / merge-audit / manifest) all
  fail-closed rc=1 (recorded here, not published as kit files).

## Verdict scope and status

Consuming the 21 exact-LOSS labels asserts NO root verdict, NO free
class, and NO 11x11 outcome.  The standard 11x11 empty board and every
central-reply root stay UNKNOWN.  k04 (sixth-cost WIN) and every other
unconsumed probe-level WIN stay in NO cache.  Nodes are bookkeeping.

Next waves (B scripts, C outputs, D kit README + MANIFEST-sha256,
F completion log advancing the head of record
63f33c4f -> 6e49dd84) follow publish-then-execute with fetch-back byte
verification per wave.
