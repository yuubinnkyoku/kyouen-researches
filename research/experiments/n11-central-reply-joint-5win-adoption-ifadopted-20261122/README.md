# n11 central-reply: joint 5-WIN adoption IF-ADOPTED (2026-11-22)

Joint IF-ADOPTED extension of the Part H / Part H-bis packet analyses to the
**current five unconsumed closure WINs** (b018, d002, e002, f017 from batches
1/3/4/5 and **g018 from batch 6**, all 2-pass node-exact pinned-jsreplay
@15M, all verdict-unconsumed, scrutiny owner pending). Read-only planning
computation; no verdict is consumed; 11x11 stays UNKNOWN.

## Construction

- `PJ5WIN`: canonical 5,924-row cache + the published 4-WIN increment
  (`increment-wins-only-4rows-IFADOPTED-20261122.cache`, Part H-bis P4) + the
  batch-6 WIN-only increment (g018). Fail-closed union merge (published
  merger, selftest PASS, conflicts 0): 5,929 rows, WIN 163 / LOSS 5,766,
  sha256 `653dfb07...` (`pj5win/output/`).
- `PJ5FULL`: published packet-25 merged cache (P25, sha `88ef4388...`,
  5,949 rows) + the batch-6 18-row increment (17 LOSS + g018 WIN). Merge:
  5,967 rows, WIN 163 / LOSS 5,804, sha256 `a31e093b...` (`pj5full/output/`).
- per-scenario refresh byte-copies (3 pinned lines changed each, selftest
  n/a - same published script): run twice per scenario, all outputs
  byte-identical (determinism 2/2 per scenario, 4/4 runs); root {X,60,27}
  control 119/119 free thirds in every scenario.
- delta artifact: `output/decomp-deltas-joint5.json` (pinned input shas
  included).

## Machine-verified deltas (vs the canonical re-audit baseline)

| metric | base | P4 (4 WINs) | PJ5WIN (5 WINs) | PJ5FULL (43 rows: 25 + 18) |
|---|---|---|---|---|
| excluded_now | 23 | 37 (+14) | **41 (+18)** | 41 (+18) |
| free_now | 33 | 33 | 33 | 33 |
| unknown classes | 34,503 | 34,489 | 34,485 (−18) | 34,485 (−18) |
| update8 remaining | 31,838 | 31,709 (−129) | **31,658 (−180)** | 31,658 (−180) |
| update8 resolved | 21 | 24 | 25 (+4) | 62 (+41) |
| win-hit groups | 0 | 15 | **19 = 15 + 4** | 19 |
| joint greedy | 35,617 | 35,616 (−1) | **35,616 (−1)** | **36,984 (+1,367)** |
| probe worklist | 65,213 | 65,208 | 65,207 | 65,163 (−50) |
| root {X,60,27} free thirds | 119 | 119 | 119 | 119 |

- excluded flips decompose additively: 14 classes via the 4 packet WINs
  (Part H) + 4 classes via g018 (4889/4892/5473/5501, batch-6 experiment);
  win-hit groups decompose additively per class: `16757`: 5, `20421`: 4,
  `12264`: 6, `5473`: 4.
- update8 remaining is additive on the WIN side: −129 (P4) + −51 (g018) =
  −180; the per-root reductions union on roots 0/12/36/37/48 (packet) and
  roots 26/49 (g018, −102 each).
- **joint greedy: the five WINs alone keep the plan greedy-neutral
  (35,617 -> 35,616, same as P4); the full 43-row adoption lands exactly on
  the Part-H packet value 36,984 (+1,367) with ZERO additional increase from
  the batch-6 rows** - confirming the Part H-bis attribution (the increase is
  driven by the f-batch/12264 LOSS completeness property, not by WIN
  adoptions) in the joint setting.
- free_now 33, board verification 33/33, rejected 0 unchanged everywhere;
  the 23963 closure and all achieved per-root coverage are unaffected.

## Verdict for the scrutiny owner

The five unconsumed WINs remain adoption-gated individually; jointly, their
WIN-side benefit is now machine-measured at excluded 23 -> 41,
update8 remaining 31,838 -> 31,658, win-hit 19 groups, greedy-neutral
(35,616). The batch-6 rows (g018 + 17 LOSS) are measured to be planning-cost
neutral in every scenario combination tested (solo LOSS-only, solo-full,
joint five-WIN, joint 43-row). 11x11 and every root/class stay UNKNOWN.
