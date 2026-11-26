# n11-centralreply-emloss21-adoption-reaudit-20261126 (Part EM, 2026-11-26)

Part EM: the emloss21 LOSS-ONLY canonical adoption in the central-reply
chain.  The 21 gate-verified unconsumed closure-batch exact-LOSS rows of
the EM-pattern loss-adoption territory are consumed into the canonical
merged exact-S5 chain cache as LOSS labels:

* 17 rows f001-f016 and f018 of the published batch-5 kit (closure class
  12264, 2026-11-22, budget 15,000,000, order 0, two-pass fresh-cold
  node-exact; f018 published as-is after the f017 WIN-HALT), adopted
  nodes 58,253,401;
* 4 rows ai024/ai030/ai038/ai041 of the published Part ES reprobe30m kit
  (closure class 30345, 2026-11-25, budget 30,000,000, order 0, two-pass
  fresh-cold node-exact; the batch-38 honest-EXHAUSTED keys resolved
  exact at the first next-highest condition), adopted nodes 71,265,013.

Adopted node total: 129,518,414 (bookkeeping only; nodes are never
verdicts).  NO new solver pass runs in this Part.

Nothing here asserts any root verdict and no 11x11 outcome: a LOSS
canonical adoption transfers NO verdict to any central-reply root.
The class-status census is IDENTICAL on both sides (34,417 unknown /
103 excluded_now / 39 free_now / 390 excluded; exactly ZERO flips:
loss-only adoption frees no class and excludes no class).  34,417 S4
classes remain status-unknown.  The standard 11x11 empty board and every
central-reply root stay UNKNOWN.

## chain position

* BASE = the Part EV canonical merged chain head 63f33c4f...
  (6,771 rows, WIN 192 / LOSS 6,579), published in the Part EV dossier
  kit output/merged-exact-s5-chain-plus-evwin4-20261126.cache.
* increment = `output/increment-emloss21-adoption-20261126.cache` (21
  LOSS rows, sha256 3e6e9bf0a5f410a1d584889832f21352dd01a97aef5a899de06a28373fcaef82),
  row region byte-identical to the pre-declaration dossier increment
  47443dc1...; the Part increment supersedes the dossier "PREDECL
  DOSSIER" header (disclosed; the header comment block is the only
  differing region).  SSOT-extracted per-row pins in
  `output/increments-manifest.json` (schema
  emloss21-adoption-increments-manifest-v1, sha256 bd4b9e76...).
* merged head of record = the PUBLISHED dossier file
  `research/experiments/n11-centralreply-emloss21-adoption-predecl-20261126/output/merged-exact-s5-chain-plus-emloss21-20261126.cache`
  (6,792 rows, WIN 192 / LOSS 6,600, sha256 6e49dd84...).  This Part
  does NOT republish that file; the fail-closed union merger
  byte-clone (90711961...) reproduces it deterministically from BASE +
  the Part increment (3/3 byte-identical runs, audits
  merge-audit-run1/2/3.json all sha256 17a390e7..., unique_rows 6,792,
  WIN 192 / LOSS 6,600, conflict-free).

## LOSS label eligibility (fail-closed, machine-verified)

The maker `scripts/make_increments_emloss21_adoption.py` (sha256
cd603627...; structural clone of the published pre-declaration dossier
maker 74fbbfd9..., computation region byte-identical logic, disclosed
diff: docstring, emitted header, output names, manifest Part/
supersession fields and the added dossier-supersession byte gates)
re-verifies every gate before emitting a single row (fail-closed; rc=1
on ANY drift):

1. batch-5 kit consumed bytes pinned directly by sha256 (the kit
   predates the repo MANIFEST convention): README 1f69bfb1...,
   batch-keys.json 57da4702..., status.log c473e32c..., all 36 raw
   files (raw_file_sha256_pins in the manifest) and the solver replica
   pin 84585617... (39/39 consumed files re-anchored byte-identical to
   the published repo tree);
2. Part ES kit verified file-by-file against its published
   MANIFEST-sha256 cc987739... (38/38 files); the ES targets-30m SSOT
   cross-gated field-by-field against the published batch-38
   batch-keys SSOT 29807104... with the prior 15M EXHAUSTED
   honest-label pins;
3. all 24 probed rows' two-pass pairs payload-gated
   (stones/legal/is_or/budget/result/nodes/lo/hi identical across
   passes, '# replay_done' completeness guard); both status logs
   pinned and line-class accounted;
4. the f017/ai007/ai040 WIN regression ties carried and NOT
   re-adopted: each sits in BASE 63f33c4f as a consumed WIN with
   identical nodes (f017 Part EV 15M 3,522,635; ai007 and ai040 Part
   EU euwin2 30M 16,090,493 / 20,711,023);
5. all 21 adopted (lo,hi) pairs proven fresh to BASE (unique_new 21,
   base_cache_absent_hits_for_emitted 0), absent from the active
   quarantine registry 81d23160... and canonical-safe per
   s5_evidence_policy 78655e94...; the adopted-table digest 4fd8723e...
   and the emitted increment sha self-pinned;
6. the published dossier kit bytes re-pinned (increment 47443dc1...,
   manifest 94815c34..., maker 74fbbfd9..., merged 6e49dd84...) and
   the emitted rows cross-gated row-for-row against the dossier rows.

NOT consumed (each stays in NO cache): k04 (sixth-cost WIN) and every
other unconsumed probe-level WIN.  No batch key was re-searched at any
condition.

## reaudit (Board fail-closed child verification + census cross-check)

The kit extractor `scripts/compare_deltas_em_adoption.py` (sha256
b9a74915...; structural clone of the published Part EV extractor
70a5b207...) recomputes from published bytes only, fail-closed:

* BOTH published refresh forks re-executed byte-verbatim in isolated
  scratch trees: the Part EV dossier refresh fork f2edac3e...
  (refresh_adoption_evwin4.py) against BASE, and the emloss21 dossier
  refresh fork cc01b3d8... (refresh_adoption_emloss21.py; byte-clone of
  f2edac3e... differing in EXACTLY docstring, CACHE path and expected
  cache sha) against SCEN; all eight outputs byte-identical to the
  published / regenerated pins (BASE refresh-summary 1fafd081...,
  closure-classes 6ba51faa..., per-root-coverage d9eee976...; SCEN
  refresh-summary 7f379b71..., closure-classes 68628134...,
  per-root-coverage 9c5b2774...); the probe-worklists stay UNPUBLISHED
  per the size policy, entering only as regen pins (BASE ca50cb68...
  3,717,416 B / SCEN 147b62d6... 3,715,963 B) re-verified by the
  byte-verbatim re-execution;
* the published dossier maker make_increments_emloss21.py (74fbbfd9...)
  is RE-EXECUTED byte-verbatim in an isolated scratch tree (rc=0,
  byte-identical increment 47443dc1... and manifest 94815c34...),
  re-proving live, from published bytes only, the entire Part EM
  adopt-eligibility evidence chain the dossier maker encodes;
* SCEN == BASE rows + exactly the 21 Part increment rows (6,792 rows
  WIN 192 / LOSS 6,600, verdict agreement everywhere); no adopted key
  intersects the Part EV increment 7f125610... (no re-adoption);
* the independent full-class census reproduces the published class
  status counts EXACTLY on both sides (34,417 / 103 / 39 / 390
  IDENTICAL) with EXACTLY ZERO status flips;
* serving-class Board arithmetic recomputed from the frozen graph:
  class 12264 cost-unknown 50 -> 33 (the 17 batch-5 keys consumed;
  closure rank 11 -> 9) and class 30345 cost-unknown 4 -> 0 (its 4
  remaining unknown closure children consumed); class 30345 EXITS the
  closure-classes ranking 805 -> 804 (exited=[30345], entered=[]), its
  status staying excluded_now - flipped by the Part EP/EU chain, NOT
  re-flipped here; 763-row dense-rank bookkeeping at the cheap end;
* the published dossier census measurement
  census-deltas-emloss21-predecl.json d67b6e9b... is machine
  cross-compared field-by-field against the extractor's own independent
  recount: EXACT agreement on both cache identities, census counts, the
  zero-flip set, closure churn incl. the 763-row rank table, per-root
  greedy deltas, joint greedy, worklist totals, update8 numbers, the
  17-key newly-resolved set, win_hit identity (25 -> 25 IDENTICAL sets),
  serving-class records, the owner histogram and the 21-row adopted
  table (its dossier-time verdict-scope fields are superseded by this
  Part declaration; disclosed, not asserted here).

Scheduling bookkeeping measured by the extractor (no coverage claim):
joint greedy 36,618 -> 35,155 (-1,463, the largest single scheduling
reduction of any pending adoption pool measured so far), worklist
64,302 -> 64,277 (-25), group_best_options_nonfree 2,105 -> 2,101,
update8 resolved 263 -> 280 with the newly_resolved set exactly the 17
batch-5 adopted s5 indices (the 4 Part ES keys were first probed in
batch-38 AFTER the update8 baseline froze and are correctly not in it;
measured, disclosed).  Per-root free_now/uncovered identical at all 20
rows + baseline; per-root greedy-union changes only at roots
{5, 12, 16, 36, 38, 49}.

The extractor's full battery output is
`output/decomp-deltas-emloss21-adoption.json` (sha256 c1bf5881...,
schema emloss21-decomp-deltas-v1).

## Publication record (publish-then-execute; fetch-back byte-verified)

* declaration c5793256: pre-registered every kit byte pin;
* wave B1 3fc406da: scripts/s5_union_merge.py byte-clone;
* wave B2 8e570d0e: scripts/make_increments_emloss21_adoption.py +
  scripts/compare_deltas_em_adoption.py;
* wave C-1 ff942502: the six output files (published stepwise via the
  upload-verify-promote scratch protocol; the intermediate push 5f107ca1
  accidentally stripped trailing LFs and was repaired byte-exact by
  ff942502, disclosed);
* wave C-2 66badee4: the increment and manifest promote (assembled from
  the published dossier bytes + op-line scratch, blob-sha-gated at
  every step, scratch deleted);
* each wave fetch-back byte-verified against the pre-registered pins
  (sha256 sums listed in MANIFEST-sha256.txt are the exact published
  bytes).

## Interpretation guard

Consuming the 21 LOSS labels asserts NO root verdict, NO root-class
verdict and NO 11x11 outcome.  No class is freed or excluded by this
Part; the class census is identical on both sides.  k04 and every other
unconsumed probe-level WIN stay in NO cache.  No free-coverage,
secured-coverage or root-resolution claim is made anywhere in this Part.
Nodes are bookkeeping, never verdicts.  The standard 11x11 empty board
and every central-reply root stay UNKNOWN.
