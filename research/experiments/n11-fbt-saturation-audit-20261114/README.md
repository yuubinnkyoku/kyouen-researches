# n11 sweep-engine fbt cache saturation audit (2026-11-14)

## Why

The canonical class2-lane sweep engine (`class4_child1_runner.ts`, shared verbatim with
the v15 sandbox sweep engine) carries a 3-stone blocked-mask cache `fbtOR` with
`FBS = 1<<17` slots, open-addressing linear probing, and a hard 48-probe limit.
When a key's probe walk finds neither the key nor an empty slot within 48 steps, the
function **silently returns** and contributes nothing to the blocked mask. Under
saturation this can (a) mark squares legal that are actually blocked, and (b) skip
OR contributions, in the worst case flipping a verdict. Nothing in the canonical
engine detects or records this. This audit measures whether saturation actually
occurs on the published class2-lane sweep rows, and whether any published verdict
is compromised.

## Method

Two variants of the canonical runner, both behavior-identical to the canonical
engine (search order, memo, wscore, caps untouched; verified: pilot d6 control
`loss=false` at exactly 5,949 nodes in every invocation, and node-exact reproduction
of all 20 audited published rows):

- `scripts/runner_instr.ts` — adds `fbtDrops` / `fbtInserts` / `fbtMaxProbe` counters
  to `fbtOR` (canonical `FBS=1<<17`).
- `scripts/runner_fbs20.ts` — same counters with `FBS=1<<20` (drop-free; every row
  below reports `fbtDrops=0`).

Insert-counting convention: `fbtInserts` counts search-time insertions only;
`setRoot` pre-inserts `C(7,3)=35` root-triple entries into the empty cache before
the search starts (not counted). Total occupancy = `fbtInserts + 35`.

Row set (20 rows): all 8 published WIN7 rows of the target's swept children
(cost-67 bits 18/34/101/118, cost-71 bits 9/70, cost-73a bit 81, cost-73d bit 48),
the 6 heaviest REFUTED rows where saturation was found, and 6 heavy clean rows
(cost-73e bit 48, cost-71 bits 94/100, cost-73b bit 53, cost-74 bits 15/20).
All 20 rows are node-exact / verdict-exact / capped-exact / terminal-range-exact
against the published raw batches (see `output/runs-manifest.json`).

## Findings

1. **All eight audited WIN7 rows have `fbtDrops = 0`.** No published WIN7
   certificate is affected by saturation.
2. **Saturation is real: 6 of 20 rows dropped queries** (all REFUTED-D10 rows):

   | sweep | bit | drops | inserts+35 (occ.) | canonical nodes | drop-free nodes | verdict |
   |-------|-----|-------|-------------------|----------------|-----------------|---------|
   | cost-73c | 32 | **834,047** | 116,510 (88.9%) | 19,876,385 | 19,910,958 | survives |
   | cost-73b | 18 | **646,356** | 110,723 (84.4%) | 19,812,446 | 19,632,308 | survives |
   | cost-73c | 120 | 58,092 | 102,597 (78.3%) | 26,150,087 | 26,220,909 | survives |
   | cost-74 | 70 | 16,034 | 90,616 (69.1%) | 19,146,135 | 19,178,789 | survives |
   | cost-71 | 110 | 10,298 | 96,272 (73.5%) | 21,014,908 | 21,014,094 | survives |
   | cost-70 | 112 | 9,046 | 96,305 (73.5%) | 24,933,747 | 24,937,173 | survives |

3. **Every saturated verdict survived a drop-free re-solve** (`FBS=1<<20`,
   `fbtDrops=0`): all six rows remain `loss=false` (REFUTED-D10). No verdict flips,
   no WIN7 appears or disappears. Published records, frontier numbers and
   certificates are unchanged.
4. **Saturation onset**: the least-occupied saturated row is cost-74 bit70 at
   90,616 total inserts (69.1% of 131,072 slots); the most-occupied clean row is
   cost-74 bit20 at 87,159 (66.5%). `fbtMaxProbe` hits the 47/48 ceiling exactly on
   the saturated rows.
5. The **certificate layer is separately drop-guarded**: the exact extractor
   already runs `FBS=1<<20` and requires `fbt_drops=0` on every published
   certificate, so published certificates never inherit this risk.

## Provenance note

Session 10 (2026-11-14) ran this audit first, but its local raw outputs were lost
to an execution-environment reset before they could be pushed. Session 11
regenerated every row from scratch with a rebuilt instrumented variant; all
previously recorded `fbtDrops` values and drop-free node counts reproduced
**bit-exact** — an unplanned but welcome determinism confirmation of the engine
across independent runs on independent machines. Only `fbtInserts` conventions
differ by the documented constant 35.

## Recommendation

- Sweep candidates expected above ~19M nodes (~90k fbt inserts) should run with
  the drop counter; any saturated verdict must be confirmed with the `FBS=1<<20`
  re-solve before reuse as evidence.
- The canonical runner stays byte-identical for raw comparability.
- Remaining unaudited ≥19M-node rows from earlier sweeps (e.g. cost-65b/66a/66b/
  68/68b/70b heaviest rows) are cheap follow-ups.


## Follow-up (same day): full class2-lane closure

The first pass covered this S5 target's swept children. The follow-up scanned all 19
published class2-lane sweep records (cost-65b through cost-74), listed every raw
candidate row with >= 19M nodes (6 unaudited) plus every remaining WIN7 row (11
unaudited), and re-solved all 17 deduplicated rows instrumented. All 17 are
node-exact / verdict-exact against the published raw batches.

- **Every WIN7 row of the entire class2 lane is now audited: 19/19 with fbtDrops=0**
  (first pass 8 + follow-up 11, including the parallel-lane cost-73a bit81).
- **3 new saturated rows** (all REFUTED-D10, all confirmed surviving drop-free):

  | sweep | bit | drops | occupancy | canonical nodes | drop-free nodes | verdict |
  |-------|-----|-------|-----------|-----------------|-----------------|---------|
  | cost-69c | 68 | **208,479** | 106,411 (81.2%) | 22,139,194 | 21,821,889 | survives |
  | cost-69c | 110 | 13,151 | 95,315 (72.7%) | 23,731,323 | 23,850,131 | survives |
  | cost-70 | 86 | 5,703 | 94,547 (72.1%) | 20,457,811 | 20,458,227 | survives |

- Clean heavy REFUTED rows at 28.8M / 24.8M / 22.3M nodes with only 75,510 /
  84,596 / 71,620 occupancy show that node count alone does not predict saturation;
  occupancy (fbtInserts) does. Every saturated row across both phases sits above
  ~90.6k occupancy, every clean row below ~87.2k.
- **Combined totals: 37 rows audited, 9 saturated, 9/9 confirmed drop-free, 0
  verdict flips, 0 WIN7 rows affected.** No published verdict, frontier number, or
  certificate changes.


## Follow-up 2 (same day): cost-73a rows from the parallel-lane record

The parallel lane completed the cost-73a sweep (1 WIN7-D10 bit81 + 72 REFUTED, 0 capped, 383,290,602 nodes; sweep record first published at c6d4aa78 and re-pushed with the bit81 certificate at ff417b0f). This follow-up re-solved the record's two heaviest REFUTED rows and the WIN7 row with the instrumented runner; all three rows are node-exact / verdict-exact against the record:

| sweep | bit | verdict | nodes (record = run) | fbtDrops | inserts+35 (occ.) | fbtMaxProbe |
|-------|-----|---------|----------------------|----------|--------------------|-------------|
| cost-73a | 92 | REFUTED-D10 | 20,603,022 exact | **1,384** | 87,984 (67.1%) | 43 |
| cost-73a | 23 | REFUTED-D10 | 18,497,705 exact | **1,761** | 97,145 (74.1%) | 47 |
| cost-73a | 81 | WIN7-D10 | 5,530,773 exact | 0 | 55,402 | 16 |

- **Both new saturated rows are now confirmed drop-free.** The parallel lane published `class2-lane-cost73a-runner-fbs20-crosscheck-20261114.jsonl` (runner_fbs20, FBS=1<<20): bits 92/23/48/81 all `fbtDrops=0`, verdicts unchanged, and node counts bit-exact identical to the canonical v15 rows (20,603,022 / 18,497,705 / 16,806,863 / 5,530,773; `fbtMaxProbe<=6`). Combined audit state: 11 rows with observed drops, 11/11 confirmed drop-free, 0 verdict flips. Notably these two rows' drop-free node counts equal the saturated canonical counts (unlike the six first-pass saturated rows, whose drop-free counts differed) — at 67.1%/74.1% occupancy the ~1.4k/1.8k dropped queries did not alter the search.
- **Onset bracket tightened to [87,159 clean; 87,984 saturated]** (66.5%-67.1% of 131,072 slots): cost-73a bit92 saturates at 67.1% occupancy, below the previous least-occupied saturated row (cost-74 bit70 at 69.1%).
- **Correction to the first-pass reading of fbtMaxProbe**: it is *not* a saturation indicator. The counter records only probe walks that end in a find-or-insert; a dropped query stops at the 48-step limit without updating the counter, so bit92 shows maxProbe=43 while dropping 1,384 queries. The 47/48 ceiling on earlier saturated rows was a successful-walk artifact.
- WIN7 coverage: cost-73a bit81 re-confirmed clean — a third independent node-exact reproduction (session-9 inflight, parallel-lane fresh rerun, this audit). Distinct class2-lane WIN7 rows audited remain 19/19, all fbtDrops=0.
- v15 context: the parallel lane's v16 runner repairs signed TT keys and the negative-bound sentinel that v15 stores ineffectively. The instrumented and drop-free variants here are deliberately v15-derived for raw comparability (node counts reproduce v15 exactly). Under v16 the memo actually hits, which changes search-time fbt insert patterns — the occupancy-onset figures above are v15-specific and must be re-measured before reuse for v16 sweeps.

## Files

- `scripts/runner_instr.ts` — instrumented canonical (FBS=1<<17 + counters)
- `scripts/runner_fbs20.ts` — drop-free variant (FBS=1<<20 + counters)
- `output/instrumented-runs.jsonl` — 20 audited rows with counters
- `output/drop-free-reresolve.jsonl` — 6 saturated rows re-solved drop-free
- `output/instrumented-runs-followup.jsonl` — 17 follow-up rows (>=19M + remaining WIN7)
- `output/drop-free-reresolve-followup.jsonl` — 3 follow-up saturated rows re-solved drop-free
- `output/runs-manifest.json` — structured summary, cross-checks, conclusions (both phases)
- `output/instrumented-runs-followup2.jsonl` — 3 cost-73a rows (2 heaviest REFUTED + WIN7 re-check)
- `output/runs-manifest-followup2.json` — structured follow-up-2 data

## Interpretation guard

`loss=false` (REFUTED-D10) is the absence of a winner-win-within-depth-10 in a
7-stone subtree; it is **not** a refutation of the child. This audit changes no
verdicts and proves no game-theoretic claim beyond the audited rows.

**11x11 empty board, two-stone root {49,60}, S2 {59,60}, class 2, class 4:
UNKNOWN.**
