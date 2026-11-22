# n11 central-reply closure class 8784 re-audit: increment merge + refresh (Part Y, 2026-11-22)

Consumption of batch 10 (Part X): the 52 two-pass node-exact LOSS rows of
`research/experiments/n11-centralreply-closure-class8784-batch10-20261122`
(class 8784, mask `[6052837899186012160, 0]`, probe_order 383-434) are merged
into the canonical chain cache and the 19-root joint plan refresh is re-run,
under the same fail-closed mechanism as Part C (23963, 33rd free class) and
Part M (10324, 34th free class). Declared as **Part Y** of
`research/log/2026-11-22-n11-centralreply-19root-refresh-closure-batch1-single-owner-note.md`.

## Inputs (all sha-pinned, re-downloaded from the published repo)

- canonical merged cache: 5,975 rows
  `merged-exact-s5-chain-plus-closure-increment-plus-batch7-20261122.cache`
  sha256 `a998f4c0b13383cb50bbbdb60761182722ba45280fd585739ad5d08bc182ed1b`
  (published Part M output)
- batch-10 published raws: 104 files (chunk commits `7b8790ab` / `736a4f11` /
  `354524de`), re-downloaded for the increment build and byte-compared 104/104
  against the execution-host copies
- `input/batch-keys.json` of the batch-10 experiment
  sha256 `a1401ee2769f3943f993527dd4934ce82e99c6d55ee27a13cf74b1b417148ebf`
- refresh pinned inputs (unchanged from Part M): dependency-graph
  `54f9c364...`, update8 plan `b658290a...`, board source `954d3a10...`,
  evidence policy `78655e94...`, quarantine registry `81d23160...`

## Pipeline (fail-closed)

1. increment: `scripts/make_increment_batch10.py` validates every batch-10
   raw fail-closed (rule gate `forbidden quadruples: 95670` in both passes,
   row schema stones==5 / is_or==0 / budget==15,000,000, 2-pass
   (budget,result,nodes) equality, result==2 LOSS only, legal and (lo,hi)
   matching the published batch-keys.json) and emits
   `output/increment-52loss-20261122.cache` (52 rows,
   sha256 `f500610a55802e7f67eecb06d9d31e3462761cbb61a746bbd46a4e63ad2cc652`).
   Any gate violation aborts with no output.
2. merge: published `scripts/s5_union_merge.py` (selftest PASS on this host)
   merges canonical 5,975 rows + the 52-row increment: unique rows **6,027**,
   duplicates elided 0, verdicts WIN 158 / LOSS 5,869,
   **conflicts 0, node mismatches 0** (see `output/merge-audit-20261122.json`);
   new merged cache
   `output/merged-exact-s5-chain-plus-closure-increment-plus-batch10-20261122.cache`
   sha256 `95e868d6762925b9a27ad963a825a9ad4fd5131a864eb82fac0db77d7acdb326`
   (247,267 bytes). Re-running the merge from the canonical input path
   reproduced the output sha byte-identically.
3. refresh: `scripts/refresh_19root_frontier.py` is the published Part M
   script (sha256 `0bc10a05...`) byte-copied with exactly 3 changed lines
   (docstring cache-lineage line, CACHE path line, CACHE_SHA_EXPECTED line;
   scenario-script sha256
   `8867152695245aa23f3cd6849b3050e5bfec9365276d3da7998a0d607469a31c`),
   run twice: **all 4 outputs byte-identical across the two runs**
   (`closure-classes.csv` `61943b85...`, `per-root-coverage.csv`
   `33f01a0c...`, `refresh-summary.json` `25987add...`, `probe-worklist.csv`
   `1807e4d2...`; the 65,154-row worklist is regenerable and not republished,
   total recorded in refresh-summary.json).

## Machine-verified results (vs published Part M base)

Pre-registered judgement gates (all PASS):

- **class 8784 disappears from the unknown closure ranking and becomes the
  35th Board-verified free class**: `free_now` 34 -> **35**,
  `board_verification` 35/35 verified, rejected 0.
- `unknown` class count 34,502 -> **34,501** (exactly one class flipped
  unknown -> free; `excluded_now` **unchanged 23** as machine-required for a
  zero-WIN increment).
- frozen update8 plan: `remaining_now` 31,836 -> **31,784** (-52),
  `resolved_count` 23 -> **75** (all 52 consumed s5 indices are baseline
  requirements), `groups_free_now` 122 -> **127** (+5);
  per-root remaining: root 16 -104, root 38 -156.
- real per-root free-third coverage gains: root 38 free thirds
  **10 -> 13** (+3), root 16 **12 -> 14** (+2) (see `per-root-coverage.csv`).
- scheduling quantities: joint greedy union 35,857 -> **35,242** (-615,
  the third-largest greedy reduction in the lane's history after the batch-8
  LOSS-43 -951 and batch-9 LOSS-32 -622), probe worklist 65,155 -> 65,154,
  nonfree best-option groups 2,132 -> 2,127.
- next first clean candidate in the refreshed closure ranking: rank 9 is
  class 8784 no more; ranks 1-8 are unchanged and all carry refutation
  evidence (16757: b018, 20421: d002, 30345: 528497, 16371: e002,
  12264: f017, 5473: g018, 2634: h045, 1518: j033), so the first clean
  candidate becomes rank 9 **class 8106** `[1152926194711134208, 0]`
  (unknown 52, first=14/third=58, 4 groups).

## Claims and consumption

Consumed: only the 52 batch-10 LOSS rows. The seven closure WINs
(b018/d002/e002/f017/g018/j033/h045) remain unconsumed, third-implementation
spot-verified, and pending the scrutiny owner (C++ second-implementation gate
pin `9193f5b6...` precedent). The free status of class 8784 is a derived class
status of this merged cache; **no coverage/closure/root game-outcome claim is
made beyond it. The standard 11x11 empty board and the 19 central-reply roots
remain UNKNOWN.** Nodes are bookkeeping, never verdicts.
