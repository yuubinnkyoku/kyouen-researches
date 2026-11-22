# n11 central-reply closure: JOINT unconsumed-rows IF-ADOPTED decomposition of the nine WIN-HALT batches (Part AJ, 2026-11-22)

Read-only planning/audit experiment (no solver search, no new verdicts),
declared before any execution in the single-owner note as **Part AJ**
(note commit `8d5cb672`, observed HEAD-before-push `9a2b46f1`).
Batch / PR なし、main直接。

Scope: ALL unconsumed probed rows of the nine WIN-HALT batch experiments
(batches 1, 3, 4, 5, 6, 8, 9, 11, 12 = classes 16757 / 20421 / 16371 /
12264 / 5473 / 2634 / 1518 / 8785 / 8106), consolidated into one joint
what-if packet. Batch 13 (16930) is EXCLUDED (Part AI owns its own
decomposition, in flight at declaration time); batch 14 (23101, Part AF)
is untouched. Clean batches 2/7/10 are already inside the canonical BASE
cache. This extends the joint-adoption series Part H (joint 4-WIN) and
Part J (joint 5-WIN) with the five WINs they could not cover
(j033/h045/z003/n005/n006) plus all probed LOSS rows.

## Pinned inputs (fetch-time byte-verified)

* dependency-graph `54f9c364...` (16,001,318 bytes),
* canonical Part Y merged chain cache 6,027 rows `95e868d6...`,
* update8 plan `b658290a...`, Board source `954d3a10...`,
* evidence policy `78655e94...`, quarantine registry `81d23160...`,
* published raws / status.log / batch-keys.json of the nine batches
  (commit-pinned raw fetch, 312 raw files incl. batch-11 takeover passes),
* BASE control outputs: Part Y canonical `61943b85...` /
  `33f01a0c...` / `25987add...` (published
  `../n11-class8106-n005n006-base-control-20261122/`, not republished;
  byte-sha-verified on this host after fetch).
* pinned machinery: `refresh_19root_frontier.py` `88671526...` (4-hunk
  scenario adaptation like Part AH, diff-verified),
  `s5_union_merge.py` `90711961...` (byte-identical to the published
  merger), jsreplay pin `84585617...` (provenance of the raw rows only).

## What is executed (fail-closed)

1. `scripts/make_increments_joint10.py` builds three increments from the
   published raw rows (3-way p1/p2/status node-exact gates; batch-11
   z-keys are 4-way incl. takeover passes; legal/(lo,hi) against
   published batch-keys; 151 distinct keys; 0 hits in the 6,027-row BASE
   cache; quarantine 0):
   * `increment-joint-wins10-IFADOPTED-20261122.cache` (10 rows: the ten
     unconsumed closure WINs b018/d002/e002/f017/g018/j033/h045/z003/
     n005/n006),
   * `increment-joint-loss141-IFADOPTED-20261122.cache` (141 rows),
   * `increment-joint-all151-IFADOPTED-20261122.cache` (151 rows).
   h002 (batch-8 15M exhaustion, result 0) is excluded from all
   increments; its exhaustion shape is gate-checked (result 0, nodes
   15,000,000, 2-pass identical). Its 15M re-search stays forbidden.
2. `scripts/s5_union_merge.py` (pinned, selftest) merges BASE + each
   increment into three analysis-only scenario caches (fail-closed,
   WIN/LOSS conflict abort, duplicates 0):
   `jwin10/`, `jloss141/`, `jall151/` each with
   `output/cache-<scenario>-IFADOPTED.cache` + merge audit JSON.
3. Per scenario, the Part Y refresh script is adapted in exactly 4
   hunks (docstring / ROOT / CACHE / CACHE_SHA pin) and executed twice;
   run outputs must be byte-identical (determinism 2/2 per scenario).
4. `scripts/compare_deltas_joint10.py` re-executes the published refresh
   class-status semantics (graph + update8 + scenario cache, Board
   fail-closed free verification), asserts every recomputed
   class_status_count equals the published summaries for BASE + all
   three scenarios, machine-identifies the excluded_now flip set (the
   10-WIN holder union), the update8 newly-resolved indices gated to
   the increment rows (expected 10 / 141 / 151), per-batch-class
   unknown_now additivity, per-root free coverage gates (must equal BASE
   on every root; root first=27 keeps 119/119 free thirds), per-root and
   joint greedy scheduling tables, and emits
   `output/decomp-deltas-joint10.json`.

## Interpretation guard

Everything here is read-only IF-ADOPTED planning analysis; **no verdict is
consumed anywhere**. The ten WINs remain unconsumed closure WINs pending
the scrutiny owner (C++ second-implementation gate pin `9193f5b6...`;
all ten already carry third-implementation verdict-level cross-verification,
Parts G/H/K/O/P/T/W/AA/AD/AG). The still-unprobed children of the nine
batch classes, the 19 central-reply roots and the standard 11x11 empty
board remain UNKNOWN at every point of this experiment. Node counts are
bookkeeping, never verdicts.

## Result

(filled after execution)
