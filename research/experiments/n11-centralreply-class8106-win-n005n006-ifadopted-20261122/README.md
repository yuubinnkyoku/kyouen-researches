# n11 central-reply: batch-12 (class 8106) n005/n006 WIN if-adopted decomposition (2026-11-22)

IF-ADOPTED scenario analysis for the batch-12 WIN-HALT keys **n005 and n006**
(n005: s5_index 188395, key `[1153489144664555520, 0]`, legal 82, probe_order
438, result 1 WIN, 12,863,268 nodes; n006: s5_index 219608, key
`[1152926194711134208, 128]`, legal 78, probe_order 439, result 1 WIN,
3,695,373 nodes; both 2-pass node-exact and third-implementation
cross-verified at verdict level, Part AD scratch / Part AG completion record;
see `../n11-centralreply-closure-class8106-batch12-20261122/`, wave-1 raw
chunk `eca35f3c`, wave-2 chunk `ace92d84`). Batch 12 probed 8/52 (two waves
n001-n004 and n005-n008: 6 LOSS + the n005/n006 WIN-HALT x2; n009-n052
untouched; no exhaustion rows exist). The lane does NOT consume the verdicts
(pre-registered rule: WIN rows go to the verdict-scrutiny owner). Following
the Part H-bis / Part J / Part R / Part V / Part AB methodology
(machine-separated WIN-only vs LOSS-only vs full scenario), this experiment
answers, fail-closed: **what would change if (a) only the 2 WIN rows
(n005/n006), (b) only the 6 LOSS rows (n001-n004/n007/n008), or (c) all 8
probed resolved rows were adopted.** This is the closure grind's first
decomposition packet with a multi-WIN increment (batch-11 z003 was 1 WIN).

## Construction

- BASE = the Part Y canonical re-audit outputs, reproduced byte-exactly
  twice on this host:
  `../n11-class8106-n005n006-base-control-20261122/` (cross-host determinism:
  both runs byte-identical and the three published outputs byte-equal to
  `../n11-central-reply-8784-closure-reaudit-20261122/`).
- Increments built fail-closed from the published batch-12 raw replay rows
  of the declaring host by `scripts/make_increments_batch12.py` (every row
  cross-checked 3-way: declaring-host p1/p2 passes identical +
  declaring-host status.log PASS rows agree on (budget,result,nodes); batch-12
  was executed entirely on the declaring host, so no takeover-host passes
  exist for this batch - unlike batch-11's 4-way cross-host; key/legal
  cross-checked against the published batch-keys.json sha256
  `de55df83483663e31b1c1db0fb8a1239079e7152bddef9bd893439b7b2fdbdc2`
  (52 keys); exactly 8 keys, exactly the n005/n006 WIN pair, 6 LOSS rows;
  verdicts byte-taken from the raws; determinism 2/2 runs byte-identical):
  `output/increment-batch12-probed-8rows-IFADOPTED-20261122.cache` (8 rows,
  sha256 `d1954280f21b16bca20b4da42570e576e41b64cb3fe6e19de05c537658012def`),
  `output/increment-batch12-winn005n006-only-IFADOPTED-20261122.cache`
  (2 WIN rows, sha256
  `dd5fc998af17c3c3acdf89f3bbbbbf2d9e94280baff70ee6ff54d3b0759eef5d`),
  `output/increment-batch12-loss6-only-IFADOPTED-20261122.cache` (6 LOSS rows,
  sha256 `d18ddaf8d5f12b425591597faab3f728e6cea5478b69288ff295ce2cd5f166b6`).
- Fail-closed union merges onto the canonical 6,027-row merged cache
  (sha256 `95e868d6...`, published merger `scripts/s5_union_merge.py`,
  selftest PASS, WIN/LOSS conflicts 0, duplicates 0):
  `pwin2/output/cache-pwin2-IFADOPTED.cache` 6,029 rows WIN 160 /
  LOSS 5,869 sha256
  `c13f81d75f3837b1331f05742d046fac9ae3b3821c24ec26a311833ae4bbf986`;
  `ploss6/output/cache-ploss6-IFADOPTED.cache` 6,033 rows WIN 158 /
  LOSS 5,875 sha256
  `898ca5f48d78f2eaf628e45bea8d1454278d95e54c34c7c5a68325cba7b6e883`;
  `pfull8/output/cache-pfull8-IFADOPTED.cache` 6,035 rows WIN 160 /
  LOSS 5,875 sha256
  `21bbef33b8b8fa575217397d81a9366b9788b6c336337dae6f71e9ac6fe64c6f`;
  audits `p*/merge-audit-ifadopted.json` (rows additivity 2+6 = 8,
  verdict counts additive WIN 158+2 / LOSS 5,869+6). The three scenario
  caches are analysis-only artifacts and are NOT canonical.
- `<scenario>/scripts/refresh_19root_frontier.py` (one byte-copy per
  scenario of the published Part Y script, only the docstring
  cache-series lines, the depth (`ROOT`) line, the CACHE path line and the
  sha pin line changed, diff-verified against the base-control copy): run
  twice per scenario, all outputs byte-identical per run (determinism 6/6
  runs); all other pins unchanged; baseline control holds (root first=27:
  119/119 free thirds and identical per-root free coverage
  (free_now/uncovered) in every scenario).
- Deltas gated through `scripts/compare_deltas_batch12.py` ->
  `output/decomp-deltas-batch12.json` (sha256
  `a4152995259ac996215aad5ba4364ccefc8a43063d9b4adfaf251be15d46dee4`).
  The compare script also re-executes the published refresh class-status
  semantics faithfully from the graph + update8 receipt + scenario cache
  (verdict-level statuses and the Board fail-closed verification for free
  candidates) and asserts every recomputed `class_status_count` equals the
  published summary for BASE and all three scenarios before any delta is
  reported. The scenario `probe-worklist.csv` outputs (3.8 MB each,
  regenerable byte-identically from the pinned inputs) are not published
  (lane convention; sha256 recorded here: BASE
  `1807e4d21f6fb757ea21850c6bda4d822cb76ac59abfa9bcd1cc7b53bd7055ef`,
  PWIN2 `aea3536346caa67ef686bf44e4672ca184df86d635cbb6c13cb8b9ca33510a23`,
  PLOSS6 `f9687992470c6613cb8b1fa4ea4ca6654cd26cbdd3dbd8ee8b53777f116eb010`,
  PFULL8 `fbf65fe3cc28ab405ee8e29abfff00efbf6c5bda0aef8f18c2275cf0d5d93bee`).

## Machine-verified decomposition (deltas vs the Part Y canonical re-audit)

| metric | base | PWIN2 (2 WIN only) | PLOSS6 (6 LOSS) | PFULL8 (8 rows) |
|---|---|---|---|---|
| excluded_now | 23 | **28** (+5) | 23 (0) | 28 (+5) |
| free_now | 35 | 35 | 35 | 35 |
| unknown classes | 34,501 | 34,496 (-5) | 34,501 (0) | 34,496 (-5) |
| update8 remaining | 31,784 | **31,732** (-52) | 31,778 (-6) | 31,732 (-52) |
| update8 resolved | 75 | 77 (+2) | 81 (+6) | 83 (+8) |
| win-hit groups | 0 | **4** | 0 | 4 |
| joint greedy size | 35,242 | 35,294 (+52) | 35,242 (0) | 35,294 (+52) |
| probe worklist | 65,154 | 65,150 (-4) | 65,147 (-7) | 65,143 (-11, additive) |
| root {X,60,27} free thirds | 119 | 119 | 119 | 119 |

- **excluded_now flips: exactly 5 classes = {5007, 5011, 6147, 6166, 8106}**
  (same set in PWIN2 and PFULL8, as in Part AB where PWINZ003 = PFULL4), machine-identified from the
  frozen graph as the union of the holder sets of BOTH WIN S5 children
  (n005 188395: {5007, 5011, 8106}; n006 219608: {6147, 6166, 8106};
  membership_class_count 3 each; the two triples overlap in exactly one
  class: batch class 8106 itself, hence union 5). Class 8106 self-excludes
  (like 8785 for z003, 5473 for g018, 1518 for j033, 2634 for h045); peers
  5007/5011 (n005) and 6147/6166 (n006) exclude on a single WIN regardless
  of their remaining unknown children (published refresh semantics). All
  five holders were baseline UNKNOWN at the frozen graph (machine-gated).
  PLOSS6 flips: empty (gate). This is the first multi-WIN flip set: it is
  the union, not the sum, of per-WIN flips (3+3 with overlap 1 = 5).
- **class 8106 unknown_now: 52 -> 50 / 46 / 44** (WIN-only -2, LOSS-only -6,
  full -8; additivity machine-gated). Renewed closure rank: class 8106
  remains a refutation-evidence holder under the full what-if only (44
  unknown children left); in the canonical cache the 52-row universe is
  untouched.
- **update8 (frozen joint plan refresh): ALL EIGHT batch-12 probed rows are
  update8 baseline requirements** (unlike batch-11, where only z003/z004
  were): newly-resolved PWIN2 `{188395, 219608}` (n005/n006 themselves),
  PLOSS6 `{48210, 75387, 110810, 161205, 232022, 237227}` (n001-n004,
  n007/n008), PFULL8 all eight. Remaining delta is sub-additive by exactly
  6 (PW -52, PL -6, full -52): the class-8106 excluded_now flip drops the
  class's full 52-member remaining baseline-requirement set at once,
  subsuming the 6 separately LOSS-resolved indices. The z003 batch-11
  analogue dropped 58 (class 5748); here the dropped set belongs to the
  batch class itself.
- **update8 win-hit groups (PWIN2 = PFULL8): exactly 4 groups, all served
  by class 8106** (s4_mask `[1152926194711134208, 0]`, reply 60): two for
  root first=14 (thirds 58/102, fourths 102/58) and two for root first=38
  (thirds 42/34, fourths 34/42); each group's unknown_s5_children count 52
  (the class-8106 universe). Batch-11's z003 pattern served 5 groups via
  peer 5748; the batch-12 pattern hits through the batch class itself, so
  the win-hit holder doubles as an excluded_now flip.
- **joint greedy is additive for this packet at the joint level**
  (WIN-only +52, LOSS-only 0, full +52 - contrast batch-11's +797
  non-additive cascade in Part AB), but the **per-root greedy_union_size
  column is non-additive at root 14**: central first=14 moves +1 (PWIN2),
  +7 (PLOSS6), +5 (PFULL8) - win+loss = 8 != 5, sub-additive by 3;
  first=38 moves -2/-6/-8 (additive) and first=49 moves -2/0/-2 (additive);
  every other root and every free-coverage column is byte-identical.
  group_best_options_nonfree is 2,127 in all four runs. Batch class 8106
  covers central-reply receipt classes for roots 14 and 38 (reply 60),
  which is where the greedy re-selection shows first. These are
  scheduling-quantity effects of the frozen greedy pipeline, not coverage
  or verdict claims.
- Scheduling quantities only: `worklist_total` is fully additive
  (-4 -7 = -11). Unknown class count and excluded_now/class-status counts
  are WIN-only driven as in Part H-bis / Part AB (LOSS rows move only the
  scheduling option pool: worklist; and the resolved/remaining bookkeeping).

## Honesty record

- Verdicts NOT consumed. n005/n006 remain unconsumed closure WINs (with
  b018/d002/e002/f017/g018/j033/h045/z003/p002/p003 all 12 closure WINs are
  third-implementation cross-verified at verdict level, Part AG), scrutiny
  owner (C++ second-implementation gate pin `9193f5b6...` precedent,
  unchanged). The scenario caches are analysis-only; adopting or discarding
  them is the scrutiny owner's decision; this lane does not rewrite the
  canonical cache. The standard 11x11 empty board, the 19 central-reply
  roots, class 8106 (52-row universe untouched in the canonical cache; 44
  unknown only under the full what-if) and every other class remain
  UNKNOWN throughout. Node counts are not verdicts. Win-hit groups, greedy
  sizes and worklist sizes are scheduling quantities and carry no class
  status.
