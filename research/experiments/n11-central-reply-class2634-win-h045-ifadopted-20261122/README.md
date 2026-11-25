# n11 central-reply: batch-8 (class 2634) h045 WIN if-adopted decomposition (2026-11-22)

IF-ADOPTED scenario analysis for the batch-8 WIN-HALT key **h045**
(s5_index 103558, key `[4035225266258182144, 64]`, legal 85, probe_order 325,
result 1 WIN, 6,366,900 nodes, 2-pass node-exact; see
`../n11-centralreply-closure-class2634-batch8-20261122/`, takeover provenance
Part U). At the halt 45/51 keys were probed (h001-h044 + h045: 43 exact LOSS
+ h002 (a 15M budget-exhaustion UNKNOWN, s5 11390, honest UNKNOWN, not
re-searchable under the same condition) + the h045 WIN; h046-h051
untouched). The lane does NOT consume the verdict (pre-registered rule: WIN
rows go to the verdict-scrutiny owner, as b018, d002, e002, f017, g018,
j033). Following the Part H-bis / Part J / Part R methodology
(machine-separated WIN-only vs LOSS-only vs full scenario), this experiment
answers, fail-closed: **what would change if (a) only the h045 WIN row,
(b) only the 43 batch-8 LOSS rows, or (c) all 44 probed resolved rows were
adopted.**

## Construction

- BASE = the pinned Part M canonical re-audit outputs, reproduced
  byte-exactly twice on this (takeover) host:
  `../n11-class2634-base-control-20261122/` (cross-host determinism: both
  runs byte-identical and the three published outputs
  `refresh-summary.json` / `closure-classes.csv` / `per-root-coverage.csv`
  byte-equal to `../n11-central-reply-10324-closure-reaudit-20261122/`).
- increments built fail-closed from the batch-8 raw 2-pass replay rows by
  `scripts/make_increments_batch8.py` (every row cross-checked pass-vs-pass
  node-exact at budget 15M, fresh cold, pinned jsreplay.js sha256
  `845856175d3c793a7eb4306f5902ecda3f1c046a8a53e8f34ed375e51febc3df`;
  exactly 45 keys h001-h045 read; h002 result-0 exhaustion dropped from
  every increment; exactly one WIN row and it must be h045; shas in
  `output/`):
  `increment-batch8-probed-44rows-IFADOPTED-20261122.cache` (44 rows,
  sha256 `356b62a71d62ea77e4071d687eca794c835b9dbcea58143e18355e39203827f3`),
  `increment-batch8-winh045-only-IFADOPTED-20261122.cache` (1 WIN row,
  sha256 `7a5e05499027efa76cf507e06f99f6b3adcbe2adbf450212a1cd92632a3217f2`),
  `increment-batch8-loss43-only-IFADOPTED-20261122.cache` (43 LOSS rows,
  sha256 `73f01e74b4cdf3fe5029c3a0011f323bf4ba35758c12c9755e2a628c8ef891f8`)
- fail-closed union merge onto the canonical 5,975-row merged cache
  (sha256 `a998f4c0...`, published merger `scripts/s5_union_merge.py`,
  selftest PASS, WIN/LOSS conflicts 0, duplicates 0):
  `pwinh045/` 5,976 rows WIN 159 / LOSS 5,817 sha256
  `1b84db115bfc68fde9f9e9000ff3250d3ed2b279d508174f38e979a40ce9b2b1`;
  `ploss43/` 6,018 rows WIN 158 / LOSS 5,860 sha256
  `0020b89d8a77e2a5350fca78442eec3eea6969056c91177e4d87c661cbc8ecfe`;
  `pfull44/` 6,019 rows WIN 159 / LOSS 5,860 sha256
  `9235e54786a895c37e42076089a675a93d27adc5af3c2aa326f698408ca0a6cd`;
  audits `*/output/merge-audit-ifadopted.json`
- `scripts/refresh_19root_frontier.py` (one byte-copy per scenario, only
  the depth line, merged-cache path and sha pin changed, 3 lines each,
  diff-verified against the pinned Part M script): run twice per scenario,
  all four outputs byte-identical per run (determinism 6/6 runs); all other
  pins unchanged; baseline control holds (root first=27: 119/119 free
  thirds)
- deltas gated through `scripts/compare_deltas_batch8.py` ->
  `output/decomp-deltas-batch8.json` (sha256
  `d4a02c299425f095f4c66b6a2a3f4230c486e574493c0945dbc0fb54134a3873`).
  The compare script also re-executes the published refresh class-status
  semantics faithfully from the graph + update8 receipt + scenario cache
  (verdict-level statuses and the Board fail-closed verification for free
  candidates) and asserts every recomputed `class_status_count` equals the
  published summary for BASE and all three scenarios before any delta is
  reported. The three scenario `probe-worklist.csv` outputs (3.77 MB each)
  are not published (lane convention).

## Machine-verified decomposition (deltas vs the Part M canonical re-audit)

| metric | base | PW045 (h045 WIN only) | PLOSS43 (43 LOSS) | PFULL44 (44 rows) |
|---|---|---|---|---|
| excluded_now | 23 | **25** (+2) | 23 (0) | 25 (+2) |
| free_now | 34 | 34 | 34 | 34 |
| unknown classes | 34,502 | 34,500 (-2) | 34,502 (0) | 34,500 (-2) |
| update8 remaining | 31,836 | **31,786 (-50)** | 31,793 (-43) | 31,785 (-51) |
| update8 resolved | 23 | 24 (+1) | 66 (+43) | 67 (+44) |
| win-hit groups | 0 | **1** | 0 | 1 |
| joint greedy size | 35,857 | 35,856 (-1) | **34,906 (-951)** | 34,906 (-951) |
| probe worklist | 65,155 | 65,154 (-1) | 65,110 (-45) | 65,109 (-46) |
| root {X,60,27} free thirds | 119 | 119 | 119 | 119 |

- **excluded flips (PW045 = PFULL44): exactly 2 classes**, machine-identified
  from the frozen dependency graph as the S4 classes holding s5 103558 as a
  cost child: `2634` and `5632` (both base-UNKNOWN, membership_class_count 2,
  cross-checked by three independent routes: the faithful verdict-level
  recompute flip set, the PFULL44-minus-PLOSS43 excluded_now set difference,
  and the graph holder scan). Class 2634 itself joins the excluded set
  despite still having 50 unresolved cost children - the same
  self-exclusion shape as 5473 under g018 (Part J) and 1518 under j033
  (Part R); per the published refresh semantics a baseline-UNKNOWN class
  with any WIN cost child becomes excluded_now regardless of its remaining
  unknown children. Class 5632 is a peer holder with 102 base-unknown cost
  children that is likewise excluded by this single WIN (it is not one of
  the 811 ranked closure classes, i.e. it serves no open coverage group;
  its base remaining set is recorded in
  `output/decomp-deltas-batch8.json`).
- **update8 (frozen joint plan refresh): unlike the batch-9 j033 WIN
  (0 win-hit groups), the h045 WIN DOES hit the frozen plan** - exactly 1
  group, the root-49 group `{first 49, reply 60, third 71, fourth 57}`
  served by class 2634 with 51 unknown children. The win-hit group drops
  out of the requirement refresh, removing class 2634's 50 still-unknown
  batch-8 keys from the remaining set; with s5 103558 itself newly resolved,
  `remaining_now` falls 31,836 -> 31,786 (-50) while `resolved_count` rises
  only 23 -> 24. The 43 LOSS rows are purely additive on the requirement
  side (+43 resolved, -43 remaining, all 43 indices inside the baseline
  requirement); PFULL44 (-51, +44) is NOT the sum of the two scenario
  effects (-50 -43 = -93 would double-count the win-hit group drop), which
  is the expected non-additivity of a group-level requirement refresh.
- **joint greedy: the 43 batch-8 LOSS rows reduce the joint 19-root plan
  cost by 951 (35,857 -> 34,906)** - the largest measured greedy reduction
  in the closure-grind lane so far (batch-9's loss-32 packet measured
  -622, Part R; batch-5 raised it +1,372; batch-6 was neutral). Biggest
  per-root greedy mover under PLOSS43: root 49 (2,891 -> 2,803, -88), the
  root whose group class 2634 serves. The WIN-only greedy effect is -1,
  fully subsumed by the LOSS-side effect in PFULL44 (greedy is sub-additive
  by exactly 1, same shape as Part R). Worklist deltas are exactly
  additive: -1 (WIN) + -45 (LOSS) = -46 (FULL); the WIN-only -1 is exactly
  the h045 key leaving class 2634's unresolved set; PW045 still lists
  class 2634's other 50 keys (h002 + h046-h051 + the 43 not-yet-adopted
  LOSS keys) because the worklist does not prune excluded classes - those
  rows can no longer produce free coverage and are listed for scheduling
  bookkeeping only.
- **class-2634 scheduling after the packet** (all class-2634 cost children:
  the 51 batch keys): PLOSS43 leaves class 2634 unknown 51 -> 8 and rank 7
  -> 1 (next unresolved key h002, then h046-h051); PFULL44 leaves unknown
  7, rank 1 (next key h046, s5 103559). Additivity of the class-level
  unknown set is exact: (51-50) + (51-8) = 51-7 = 44 resolved rows, all 44
  machine-tagged to the batch-8 increments. The remaining 6 batch-8 keys
  (h046-h051, s5 103559-103564) were NOT probed here; h002 (s5 11390,
  15M-budget exhaustion) stays an honest UNKNOWN and is not re-searched
  under the same condition.
- free_now 34, board verification 34/34 and rejected 0 are unchanged in
  every scenario; the 10324/23963 closures and all achieved coverage are
  unaffected. Per-root free coverage is identical to base in all three
  scenarios (machine gate).

## Caveats (honest)

- The lane environment still cannot run the C++ second-implementation
  adoption gate, so the h045 WIN stays unconsumed and with the scrutiny
  owner. A third-implementation spot verification of h045 in the
  Part K/O/P/T style was NOT run in this session and remains open.
- Budget exhaustion never occurred among the 44 increment rows (h002 was
  the only exhaustion and is excluded from every increment).
- The scenario caches (5,976 / 6,018 / 6,019 rows) are analysis-only
  artifacts; the canonical merged cache remains the 5,975-row
  `a998f4c0...`.
- This experiment is a what-if decomposition of a single batch's probed
  rows; it does not search any new key and does not advance the unprobed
  h046-h051 keys.

## Verdict for the scrutiny owner

Adopting the h045 WIN row (with or without the 43 batch-8 LOSS rows) would:
flip classes 2634 (itself) and 5632 excluded, reduce unknown classes by 2,
hit exactly one frozen-plan group (root 49), reduce the frozen remaining
requirement by 50 (1 resolution + the win-hit group drop), reduce the probe
worklist by 1, and leave free coverage and board verification unchanged.
Adopting the 43 LOSS rows (a separate adoption decision with the usual
fail-closed merge rules) resolves 43 baseline requirements, cuts the
worklist by 45 and cuts the joint greedy plan cost by 951. The adoption
gate stays with the scrutiny owner (C++ second implementation
pin `9193f5b6...` or equivalent); nothing here consumes the verdict.

Read-only planning computation. No verdict is consumed. No class, root,
coverage or closure claim is made. The standard 11x11 empty board and all 19
central-reply roots stay UNKNOWN. Nodes are not verdicts.
