# n11 central-reply closure: JOINT 4-WIN adoption IF-ADOPTED analysis (2026-11-22)

Part H of the central-reply 19-root closure grind lane (K0415/K0417 line),
declared as an amendment of
`research/log/2026-11-22-n11-centralreply-19root-refresh-closure-batch1-single-owner-note.md`.

## What this is

The closure batches 1/3/4/5 left an unconsumed packet of **25 rows**: four
two-pass node-exact WINs (b018, d002, e002, f017) and 21 two-pass LOSS rows.
The four single-WIN IF-ADOPTED analyses are published separately; this
experiment computes the **joint scenario** - what happens if the scrutiny
owner adopts the entire packet at once. The packet now also carries a
second, independent implementation's verdict-level agreement on all 25 rows
(Part G, `research/experiments/n11-centralreply-closure-wins-thirdimpl-reverify-20261122/`,
281/281 audit gates PASS).

**Read-only what-if computation. No verdict is consumed or changed. The
canonical merged chain cache stays at 5,924 rows (sha256 `8a721a18...`).
The standard 11x11 empty board, the 19 central-reply roots and all classes
remain UNKNOWN. Nodes/expansions are not verdicts.**

## Pipeline (all fail-closed)

1. `scripts/make_joint_increment.py`: machine-derives the 25-row increment
   from the published batch raws (source rows must themselves be 2-pass
   node-exact pinned-replica rows; results cross-checked against the
   batch expectations before emission).
2. `scripts/s5_union_merge.py` (published tool, sha256
   `907119610034fb2aebfde012550a4129dfa3b086c6de11194e856747ac74606a`,
   selftest PASS incl. negative probes and double-run determinism):
   canonical 5,924-row cache (sha256 `8a721a18...`, the published
   `n11-central-reply-23963-closure-reaudit-20261122` output) + 25-row
   increment -> **5,949 unique rows, WIN 162 / LOSS 5,787, 0 conflicts,
   0 duplicate elisions**, sha256
   `88ef4388d727bf1b1da8a9a1be350479ab481870ff2dae2d34f6f70c6d892a9a`
   (`output/merge-audit-ifadopted.json`).
3. `scripts/refresh_19root_frontier.py`: byte-copy of the published refresh
   script with ONLY the 2 cache pins changed (CACHE path and
   CACHE_SHA_EXPECTED; diff-verified). Run twice, outputs byte-identical
   (determinism). Baseline root {60,27} control: 119/119 free thirds
   (fails closed otherwise). All other inputs (dependency graph, update8
   plan, Board source `954d3a10...`, evidence policy `78655e94...`,
   quarantine `81d23160...`) are the pinned published files.
4. `scripts/compare_joint_deltas.py`: fail-closed delta extraction against
   the baseline re-audit summary and the four single-adoption summaries;
   writes `output/joint-deltas.json` and gates on:
   - **additivity**: for all 11 metrics, the joint delta must equal the
     sum of the single-adoption deltas (gate passed, 0 failures),
   - win-hit class set equality: joint == union of singles
     ({12264, 16757, 20421}: b018 -> 16757, d002 -> 20421, e002 -> none,
     f017 -> 12264),
   - per-root free coverage identical to baseline in every scenario.

## Joint-scenario results (machine-verified)

| metric | baseline | JOINT (if all 25 rows adopted) |
|---|---|---|
| excluded_now classes | 23 | **37** (+14 = the union of the four singles, no overlap) |
| free_now classes | 33 | 33 (unchanged; board-verified 33/33, rejected 0) |
| unknown classes | 34,503 | 34,489 (-14) |
| update8 remaining | 31,838 | **31,709** (-129 = b018 -29 + d002 -49 + e002 0 + f017 -51) |
| update8 resolved | 21 | 44 (+23 = +5 +4 +0 +18... machine sum: 5+4+0+14 single deltas) |
| win-hit groups | 0 | 15 (16757: 5 groups roots 36/48; 20421: 4 groups roots 12/37; 12264: 6 groups roots 0/5) |
| joint greedy size | 35,617 | **36,984** (+1,367; f017 alone was +1,372 -> the joint packet is 5 CHEAPER than adopting f017 alone) |
| probe worklist total | 65,213 | 65,183 (-30) |
| per-root free coverage | as published | identical (no root gains or loses free coverage) |

Headline planning facts:

- The joint adoption **raises the joint plan cost by 1,367** (f017's
  expensive flip of roots 0/5 dominates; b018/d002/e002 adoptions claw
  back 5 net via their own exclusions). Adoption of the full packet is
  therefore measured to make the frozen 19root plan HARDER at the
  scheduling level, not easier - a decision-relevant planning cost.
- All other deltas are favorable and compose additively across the four
  single adoptions (0 additivity gate failures).
- **Constraint on the closure ranking**: `output/closure-classes.csv` is a
  scheduling quantity and does NOT carry class status. Under joint adoption
  the ranked top is exactly the refuted quartet + 30345 (rank1 16757
  unknown 28, rank2 12264 unknown 33, rank3 20421 unknown 45, rank4 16371
  unknown 48, rank5 30345 unknown 49 - all excluded_now or holding an
  adopted WIN's cost child). **The first clean closure candidate under
  joint adoption is rank 6: class 5473** (`1158058422931816448:0`,
  51 unknown, serving the root first=26/third=59 group, 4 groups): the
  cheap end of the closure ranking is fully exhausted by the refuted
  quartet, and further blind batches should expect the WIN-dense behavior
  measured in batches 1/3/4/5 to continue at the 51-unknown scale.

## Not republished (transport constraint, honest note)

`output/probe-worklist.csv` (65,183 rows, ~3.7MB) is not re-published: it
regenerates deterministically from the pinned inputs by the published
refresh script, and its total is recorded in `output/refresh-summary.json`.
All other outputs are published. The merged 5,949-row if-adopted cache is
pushed as a separate single-file commit per repo convention and is an
analysis-only artifact, NOT the canonical chain cache.

## Status

Verdicts NOT consumed; scrutiny owner / C++ second-implementation gate
precedent unchanged; free_now 33 unchanged; no closure, coverage or root
claim is made. Standard 11x11 empty board, the 19 central-reply roots and
all classes remain UNKNOWN.
