# Part EM completion log: emloss21 loss-only canonical adoption (2026-11-26)

All waves landed.  Part EM closes complete; the canonical merged exact-S5
chain head of record formally advances to the EM merged cache
`research/experiments/n11-centralreply-emloss21-adoption-predecl-20261126/output/merged-exact-s5-chain-plus-emloss21-20261126.cache`
(sha256 6e49dd841b7bfcb335d86ef2479c95f47ab7acbcf41ace389a8b8eb95c778c9d,
6,792 rows, WIN 192 / LOSS 6,600), already published dossier-side and
byte-reproduced here by the fail-closed merger from BASE + the Part
increment; it is the new BASE for every later adoption / reaudit /
extractor.

## Wave chain (each push preceded by a fresh main refetch; each verified by
blob-sha-gated fetch-back against the regenerated local bytes)

* A  declaration c5793256: all kit byte pins pre-registered before any
  kit byte was published;
* B  kit scripts 3/3: 3fc406da (merger 90711961 byte-clone) then 8e570d0e
  (maker cd603627 + extractor b9a74915, each published via op-line
  scratch steps blob-gated at every promote);
* C  adoption outputs: ff942502 (6 files - merge-audit-run1/2/3 all
  17a390e7, decomp-deltas c1bf5881) after the intermediate push 5f107ca1
  accidentally stripped trailing LFs (tool-transport behavior of the
  upload path, disclosed and repaired byte-exact by ff942502); then
  66badee4 the increment promote (3e6e9bf0) + manifest (bd4b9e76,
  schema emloss21-adoption-increments-manifest-v1), assembled from the
  published dossier bytes + op-line scratch, candidate blob 438956ed
  gated before promote;
* D  close-out 5c8ed34f: kit README + MANIFEST-sha256 (9 published kit
  members byte-pinned sha+size, README/MANIFEST self-excluded per
  convention);
* F  completion log = this commit.

All temp upload-verify-promote scratch files (payloads, candidates,
op-line parts) were deleted from main after each promote; no scratch
bytes remain.

NOT republished in this Part (deliberate, recorded in the kit MANIFEST
header): the merged scenario cache copy (byte-identical to the published
dossier file 6e49dd84; regenerable from BASE pin 63f33c4f via the kit
merger + increment), the probe-worklists (BASE regen pin ca50cb68,
3,717,416 B; SCEN regen pin 147b62d6, 3,715,963 B; size policy), the
dossier census json (published dossier-side).  All Part kit bytes were
published from the declaration-pinned local artifacts; every wave was
blob-sha-verified against the pre-registered pins (increment
f39c087d.../3e6e9bf0, manifest 9eff8dd1.../bd4b9e76, audits
47cbaa20.../17a390e7 x3, decomp c969b262.../c1bf5881; blob = git blob
sha1 over the exact published bytes).

## Execution record (this Part, all from published bytes; NO new solver
pass ran)

The kit extractor b9a74915 ran its full battery fail-closed over
published bytes only: BOTH published refresh forks (Part EV dossier
refresh f2edac3e against BASE, emloss21 dossier refresh cc01b3d8
against SCEN, itself a byte-clone of f2edac3e differing in exactly
docstring / CACHE path / expected sha) re-executed byte-verbatim in
isolated scratch trees reproducing all 8 published / regen-pinned
outputs (1fafd081 / 6ba51faa / d9eee976 / ca50cb68 and 7f379b71 /
68628134 / 9c5b2774 / 147b62d6); the published dossier maker
74fbbfd9 re-executed byte-verbatim (rc=0, byte-identical increment
47443dc1 + manifest 94815c34), re-proving the entire adopt-eligibility
chain live from published bytes.  The merger reproduced the dossier
merged head 6e49dd84 3/3 byte-identical conflict-free runs (audits
17a390e7 x3, unique_rows 6,792, WIN 192 / LOSS 6,600).  The decomp
c1bf5881 records the extractor's independent recount agreeing EXACT
with the published dossier census measurement d67b6e9b on both cache
identities, census counts, the zero-flip set, closure churn incl. the
763-row rank table, per-root greedy deltas, joint greedy, worklist
totals, update8 numbers, win_hit identity, serving-class records, the
owner histogram and the 21-row adopted table with owner sets.

## State after the Part (all machine-verified by the extractor battery)

* canonical BASE of record: 6e49dd84... (6,792 rows WIN 192 /
  LOSS 6,600); the Part EV head 63f33c4f... remains published history
  and is the merge BASE of this Part;
* census: class_status_counts 34,417/103/39/390 -> 34,417/103/39/390
  IDENTICAL with EXACTLY ZERO flips (loss-only adoption frees no class
  and excludes no class; every owner class of the 21 keys keeps its
  BASE status);
* closure-classes.csv 805 -> 804: class 30345 EXITS the ranking
  (exited=[30345], entered=[]) because its 4 remaining unknown closure
  children (the Part ES reprobe30m keys) are consumed - its status
  stays excluded_now (Part EP/EU chain state, NOT re-flipped); class
  12264 cost-unknown 50 -> 33 (the 17 batch-5 keys consumed), closure
  rank 11 -> 9; 763-row dense-rank bookkeeping at the cheap end
  (unknown_now churn {6518: 61->60, 6547: 58->57, 9478: 61->60,
  12235: 61->60, 12264: 50->33});
* update8 frozen baseline: resolved_count 263 -> 280 (newly_resolved
  exactly the 17 batch-5 adopted s5 indices; the 4 Part ES keys were
  first probed in batch-38 AFTER the baseline froze and are correctly
  not in it - measured, disclosed), remaining_now 31,445 -> 31,445,
  groups_free_now 131 static, union baseline 31,859 stale-equal;
  win_hit_groups 25 -> 25 IDENTICAL sets (loss-only adoption adds no
  win_hit group and removes none);
* per-root free_now/uncovered identical at all 20 roots + baseline
  (no coverage claim); individual greedy-union changes only at roots
  {5: 2883->2866, 12: 2846->2842, 16: 2969->2982, 36: 2951->3001,
  38: 3014->2879, 49: 2697->2696}; joint greedy 36,618 -> 35,155
  (-1,463, the largest single scheduling reduction of any pending
  adoption pool measured so far); group_best_options_nonfree 2,105 ->
  2,101; worklist 64,302 -> 64,277 (-25).  All scheduling bookkeeping;
  no coverage claim anywhere.

## Verdict scope and guarantees (unchanged)

Consumed in this Part: exactly the 21 gate-verified unconsumed
closure-batch exact-LOSS rows of the EM-pattern loss-adoption territory
- 17 rows f001-f016,f018 (batch-5 kit, closure class 12264, 2026-11-22,
budget 15,000,000, order 0, two-pass fresh-cold node-exact, adopted
nodes 58,253,401) and 4 rows ai024/ai030/ai038/ai041 (Part ES
reprobe30m kit, closure class 30345, 2026-11-25, budget 30,000,000,
order 0, two-pass fresh-cold node-exact, adopted nodes 71,265,013);
adopted node total 129,518,414.  Consuming a LOSS label asserts NO
root verdict, frees no class and excludes no class.  NOT consumed
(regression ties, each sits in BASE as a consumed WIN with identical
nodes): f017 (Part EV, 15M, 3,522,635), ai007 and ai040 (Part EU
euwin2, 30M, 16,090,493 / 20,711,023).  NOT consumed and NOT emitted:
k04 (sixth-cost WIN) and every other unconsumed probe-level WIN.  No
batch key was re-searched at any condition.  The standard 11x11 empty
board and every central-reply root stay UNKNOWN; nodes are bookkeeping,
never verdicts; no free/secured-coverage or root-resolution claim is
made anywhere.  Next natural steps recorded by the lanes: the k04
sixth-cost WIN lane remains, and any later adoption Part takes
6e49dd84 as its BASE.
