# n11 central-reply closure: JOINT unconsumed-rows IF-ADOPTED decomposition of the nine WIN-HALT batches (Part AJ, 2026-11-22)

Read-only planning/audit experiment (no solver search, no new verdicts),
declared before any execution in the single-owner note as **Part AJ**
(note commit `8d5cb672`, observed HEAD-before-push `9a2b46f1`).
No branch / PR; published directly to main.

Scope: ALL unconsumed probed rows of the nine WIN-HALT batch experiments
(batches 1, 3, 4, 5, 6, 8, 9, 11, 12 = classes 16757 / 20421 / 16371 /
12264 / 5473 / 2634 / 1518 / 8785 / 8106), consolidated into one joint
what-if packet. Batch 13 (16930) is EXCLUDED (Part AI owns its own
decomposition, in flight at declaration time); batch 14 (23101, Part AF)
is untouched. Clean batches 2/7/10 are already inside the canonical BASE
cache. This extends the joint-adoption series Part H (joint 4-WIN) and
Part J (joint 5-WIN) with the five WINs they could not cover
(j033/h045/z003/n005/n006) plus all probed LOSS rows.

## HONEST CORRECTION (published by the maker's own fail-closed gate)

The first run of `scripts/make_increments_joint10.py` ABORTed at
`ABORT b001: key already in canonical BASE cache`. Precise re-measurement
of every batch key against the 6,027-row BASE found that exactly **19
batch-1 LOSS rows (b001..b017, b019, b020) are ALREADY inside canonical
BASE with identical verdicts AND identical node counts** (the canonical
batch-2/7/10 increments reached their membership classes); batch-1's WIN
b018 is NOT in BASE; the other eight batches have ZERO BASE overlap; no
verdict conflicts exist anywhere. Those 19 rows are therefore excluded
from every increment as pre-consumed duplicates, under a stricter gate
(verdict AND node count must both match BASE exactly, else ABORT). The
packet shrank from 151 probed rows to **132 unique-new rows
(10 WIN + 122 LOSS)**. No previously published verdict is re-claimed.

## Pinned inputs (fetch-time byte-verified)

* dependency-graph `54f9c364...` (16,001,318 bytes),
* canonical Part Y merged chain cache 6,027 rows `95e868d6...`,
* update8 plan `b658290a...`, Board source `954d3a10...`,
* evidence policy `78655e94...`, quarantine registry `81d23160...`,
* published raws / status.log / batch-keys.json of the nine batches
  (commit-pinned raw fetch `8c9d943a`, 312 raw files incl. batch-11
  takeover passes),
* BASE control outputs: Part Y canonical `61943b85...` /
  `33f01a0c...` / `25987add...` (published
  `../n11-class8106-n005n006-base-control-20261122/`, not republished;
  byte-sha-verified on the analysis host after fetch).
* pinned machinery: `refresh_19root_frontier.py` `88671526...` (4-hunk
  scenario adaptation like Part AH, diff-verified),
  `s5_union_merge.py` `90711961...` (byte-identical to the published
  merger), jsreplay pin `84585617...` (provenance of the raw rows only).

## What is executed (fail-closed)

1. `scripts/make_increments_joint10.py` builds three increments from the
   published raw rows (3-way p1/p2/status node-exact gates; batch-11
   z-keys are 4-way incl. takeover passes; legal/(lo,hi) against
   published batch-keys; 151 distinct keys total of which 19 pre-consumed
   BASE duplicates are excluded under the verdict+node-identity gate;
   quarantine 0):
   * `increment-joint-wins10-IFADOPTED-20261122.cache` (10 rows: the ten
     unconsumed closure WINs b018/d002/e002/f017/g018/j033/h045/z003/
     n005/n006; none of them is in BASE),
   * `increment-joint-loss122-IFADOPTED-20261122.cache` (122 rows),
   * `increment-joint-all132-IFADOPTED-20261122.cache` (132 rows).
   h002 (batch-8 15M exhaustion, result 0) is excluded from all
   increments; its exhaustion shape is gate-checked (result 0, nodes
   15,000,000, 2-pass identical). Its 15M re-search stays forbidden.
   Increment shas: wins10 `fe2c6f68...`, loss122 `e5fe80af...`,
   all132 `cc841d6e...` (see `output/increments-manifest.json`).
2. `scripts/s5_union_merge.py` (pinned, selftest) merges BASE + each
   increment into three analysis-only scenario caches (fail-closed,
   WIN/LOSS conflict abort, duplicates 0, 6,027+N unique rows):
   `output/merged-joint-wins10-scenario-20261122.cache` (6,037 rows,
   `7881724a...`), `output/merged-joint-loss122-scenario-20261122.cache`
   (6,149 rows, `d80ee94b...`) and
   `output/merged-joint-all132-scenario-20261122.cache` (6,159 rows,
   `13bfec6e...`), each with a merge audit JSON.
3. Per scenario (`wins10/`, `loss122/`, `all132/`), the Part Y refresh
   script is adapted in exactly 4 hunks (docstring / ROOT / CACHE /
   CACHE_SHA pin, diff-verified against the pinned base script
   `88671526...`) and executed twice; run outputs are byte-identical
   (determinism 2/2 per scenario, all four outputs compared).
4. `scripts/compare_deltas_joint10.py` re-executes the published refresh
   class-status semantics (graph + update8 + scenario cache, Board
   fail-closed free verification), asserts every recomputed
   class_status_count equals the published summaries for BASE + all
   three scenarios, machine-identifies the excluded_now flip set (the
   10-WIN eligible holder union), the update8 newly-resolved indices
   gated to the increment rows, per-batch-class unknown_now additivity
   (measured via actual s4_cost membership, not batch ownership), per-root
   free coverage gates (must equal BASE on every root; root first=27 keeps
   119/119 free thirds), per-root and joint greedy scheduling tables, and
   emits `output/decomp-deltas-joint10.json`. All gates PASS.

## Interpretation guard

Everything here is read-only IF-ADOPTED planning analysis; **no verdict is
consumed anywhere**. The ten WINs are HYPOTHETICAL adoptions (unconsumed
closure WINs pending the scrutiny owner; C++ second-implementation gate
pin `9193f5b6...`; all ten already carry third-implementation
verdict-level cross-verification, Parts G/H/K/O/P/T/W/AA/AD/AG). The 122
LOSS rows are published evidence not yet inside the canonical cache.
The still-unprobed children of the nine batch classes, the 19
central-reply roots and the standard 11x11 empty board remain UNKNOWN at
every point of this experiment. Node counts are bookkeeping, never
verdicts.

## Result

All fail-closed gates PASS. Published outputs: three increments with
manifest, three merged scenario caches with merge audits, three scenario
refresh output sets (refresh-summary / per-root-coverage /
closure-classes; the 3.7MB probe worklists are regenerable from the
published scripts and are not republished), and
`output/decomp-deltas-joint10.json`.

* **JWIN10** (adopt the ten hypothetical WINs): excluded_now
  23 -> **53** (+30 flips), unknown 34,501 -> 34,471. Machine-measured
  flip set == the frozen-graph valid holder union of the 10 WIN S5
  children exactly (30 classes, all baseline UNKNOWN, none already
  excluded_now at BASE): each WIN flips its own batch class plus its peer
  cost-child holders; only class 8106 is a multi-WIN holder
  (n005+n006); update8 win_hit_groups 0 -> 29; free_now stays 35 and
  root27 stays 119/119.
* **JLOSS122** (adopt the 122 unconsumed published LOSS rows):
  excluded_now stays 23 (empty flip set), free_now stays 35,
  unknown stays 34,501, root27 stays 119/119; update8 resolved 75 -> 163
  (+88 of the 122 rows are in the frozen update8 baseline requirement),
  update8 remaining 31,784 -> 31,696, joint greedy 35,242 -> 36,201,
  probe worklist 65,154 -> 65,011.
* **JALL132**: excluded_now 53 and unknown 34,471 (identical to JWIN10;
  the LOSS rows flip nothing), update8 resolved 75 -> 171 (+96),
  remaining 31,784 -> 31,442, joint greedy 35,242 -> 36,193, probe
  worklist 65,154 -> 64,996. Per-class membership additivity holds for
  all nine batch classes (full delta == WIN delta + LOSS delta); the
  update8 remaining_now and joint greedy deltas are honestly
  nonadditive because WIN hits remove whole planned groups while LOSS
  rows resolve individual requirements; greedy nonadditive roots (0, 14,
  49) are recorded in the delta JSON, not gated away.

Scheduling reading (not a verdict): the 122 LOSS rows are incremental
resolved evidence that would shrink the frozen update8 requirement by
88 rows and the worklist by 143 with zero status flips; the ten WINs are
worth 30 excluded classes but are still hypothetical. The 11x11 empty
board remains UNKNOWN.
