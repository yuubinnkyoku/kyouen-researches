# n11 central-reply closure batch 7 increment merge + class 10324 free re-audit (2026-11-22)

Fail-closed consumption + independent re-verification audit closing the loop of
batch 7 (`../n11-centralreply-closure-class10324-batch7-20261122/`):
51/51 keys h001-h051 2-pass node-exact LOSS at budget 15M, no WIN-HALT.

This experiment merges ONLY the 51 2-pass LOSS rows of batch 7 (the six
unconsumed WIN rows b018/d002/e002/f017/g018 of batches 1/3/4/5/6 stay
deliberately unconsumed - verdict-scrutiny owner pending) into the canonical
chain cache (5,924 rows, sha256 `8a721a18...`) and re-runs the 19-root frontier
refresh against the merged cache.

## Steps (all fail-closed, machine-derived)

1. increment `output/increment-51loss-20261122.cache` (sha256
   `39b975e80b4a8c3a2371f440dfada12ae2dfec74f9b82aa6f303742bda2e5e7b`, 51 rows
   `s5verdict,<lo>,<hi>,5,2,<nodes>`, built only from the published raws with
   per-row 2-pass (result,nodes,legal) identity and key/lo/hi equality asserts)
2. merge `scripts/s5_union_merge.py` (published bytes, sha256 `90711961...`,
   selftest PASS) - inputs pinned: canonical 5,924 (`8a721a18...`) + 51-row
   increment (`39b975e8...`) -> `output/merged-exact-s5-chain-plus-closure-increment-plus-batch7-20261122.cache`:
   **5,975 unique rows (WIN 158 / LOSS 5,817), 0 duplicates elided, 0 WIN/LOSS
   conflicts, audit `output/merge-audit-20261122.json`, output sha256
   `a998f4c0b13383cb50bbbdb60761182722ba45280fd585739ad5d08bc182ed1b`**
3. refresh `scripts/refresh_19root_frontier.py` - published bytes (from the
   23963 closure re-audit) with ONLY the two cache-pin lines changed (path +
   expected sha; diff-verified against the published base), all other pinned
   inputs byte-identical (dependency graph `54f9c364...`, update8 plan
   `b658290a...`, board source `954d3a10...`, evidence policy `78655e94...`,
   quarantine registry `81d23160...`), run **twice, all four outputs
   byte-identical**

## Result (machine-verified against the canonical 5,924 baseline)

- **class 10324 is Board-verified free**: `free_now` 33 -> **34** (34th free
  class), `board_verification` 34/34 free candidates verified by the
  independent integer-geometry Board, 0 rejected; `unknown` 34,503 -> 34,502;
  `excluded`/`excluded_now` unchanged (no new WIN entered the corpus)
- root third coverage improved: total `free_thirds_now` 244 -> **248**
  (root 14: 6 -> 8, root 16: 10 -> 12); all 19 roots' covered/free structure
  otherwise unchanged, baseline roots {60,27} stay 119/119
- update8 frozen plan: `remaining_now` 31,838 -> **31,836** (-2),
  `resolved_among_baseline_requirement` 21 -> 23 (new: S5 indices ~362082
  = batch-7 h043 and ~362090 = batch-7 h051), `win_hit_groups` still empty
- scheduling quantities: joint greedy 35,617 -> 35,857 (+240: the LOSS-side
  option-pool effect, same direction as the f-batch of Part H-bis); closure
  ranking's first candidate without refutation evidence is now **rank 7 class
  2634** (`[4035225266258182144, 0]`, unknown 51) - 10324 left the
  closure-classes ranking entirely; probe worklist 65,213 -> 65,155 (-58)

## Rules

WIN rows were never consumed; no verdict was created or asserted here; nodes
are bookkeeping, never verdicts. **The standard 11x11 empty board and the 19
central-reply roots remain UNKNOWN.** Class 10324's free status is a derived
class status from the merged cache - it feeds coverage scheduling, it is NOT a
claim about the empty board.

## Transport

`probe-worklist.csv` (3,7MB) is deliberately not re-published: it regenerates
byte-identically from the pinned inputs + this script (total in
`refresh-summary.json`).
