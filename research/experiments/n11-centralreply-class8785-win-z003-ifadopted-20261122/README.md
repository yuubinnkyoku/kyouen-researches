# n11 central-reply: batch-11 (class 8785) z003 WIN if-adopted decomposition (2026-11-22)

IF-ADOPTED scenario analysis for the batch-11 WIN-HALT key **z003**
(s5_index 198530, key `[1225542323476103168, 1]`, legal 82, probe_order 334,
result 1 WIN, 11,601,265 nodes, 2-pass node-exact + 4-way cross-host
agreement; see `../n11-centralreply-closure-class8785-batch11-20261122/`,
takeover provenance Part Z, third-implementation cross-verification Part AA).
Batch 11 probed 4/51 (first wave z001-z004: 3 LOSS + the z003 WIN; z005-z051
untouched; no exhaustion rows exist). The lane does NOT consume the verdict
(pre-registered rule: WIN rows go to the verdict-scrutiny owner, as b018,
d002, e002, f017, g018, j033, h045). Following the Part H-bis / Part J /
Part R / Part V methodology (machine-separated WIN-only vs LOSS-only vs
full scenario), this experiment answers, fail-closed: **what would change
if (a) only the z003 WIN row, (b) only the 3 batch-11 LOSS rows
(z001/z002/z004), or (c) all 4 probed resolved rows were adopted.**

## Construction

- BASE = the Part Y canonical re-audit outputs, reproduced byte-exactly
  twice on this host:
  `../n11-class8785-z003-base-control-20261122/` (cross-host determinism: both
  runs byte-identical and the three published outputs byte-equal to
  `../n11-central-reply-8784-closure-reaudit-20261122/`).
- Increments built fail-closed from the published batch-11 raw replay rows
  of BOTH hosts by `scripts/make_increments_batch11.py` (every row
  cross-checked 4-way: declaring-host p1/p2 + takeover-host
  p1/p2 all identical; declaring-host status.log PASS rows agree on
  (budget,result,nodes); key/legal cross-checked against the published
  batch-keys.json sha256
  `8ef2206986a87f3859aa0a4b25f9936ffa82001d1fd3214013dc6351ecf8b08b`;
  exactly 4 keys, exactly one WIN row z003, 3 LOSS rows; verdicts
  byte-taken from the raws):
  `output/increment-batch11-probed-4rows-IFADOPTED-20261122.cache` (4 rows,
  sha256 `2778d392255827ec9705ba0dcf241baba12d4662ef369cd0c50e698ce31b7a46`),
  `output/increment-batch11-winz003-only-IFADOPTED-20261122.cache` (1 WIN
  row, sha256 `32c582c1c476ba5d737686f4d261b79612363ed13c39a7c3afc6753437a34377`),
  `output/increment-batch11-loss3-only-IFADOPTED-20261122.cache` (3 LOSS rows,
  sha256 `939f8deba2389fcf0cbd69a0c8e27f212ab967416770e3f5d0366ecf2bcb3096`).
- Fail-closed union merges onto the canonical 6,027-row merged cache
  (sha256 `95e868d6...`, published merger `scripts/s5_union_merge.py`,
  selftest PASS, WIN/LOSS conflicts 0, duplicates 0):
  `pwinz003/output/cache-pwinz003-IFADOPTED.cache` 6,028 rows WIN 159 /
  LOSS 5,869 sha256
  `3fcdbfd090e64144f458d3eb5f28086e6026e000c5f24aecca4a34f38173a882`;
  `ploss3/output/cache-ploss3-IFADOPTED.cache` 6,030 rows WIN 158 /
  LOSS 5,872 sha256
  `ba08f924153f19275b03137c943dde9edeb4b0a3afa45a9ef2755875d376ef75`;
  `pfull4/output/cache-pfull4-IFADOPTED.cache` 6,031 rows WIN 159 /
  LOSS 5,872 sha256
  `c5044be884211755c8b06cbc1b699fa51b5f7710192174f306e6b21550b88cae`;
  audits `p*/merge-audit-ifadopted.json`. The three scenario caches are
  analysis-only artifacts and are NOT canonical.
- `<scenario>/scripts/refresh_19root_frontier.py` (one byte-copy per
  scenario of the published Part Y script, only the docstring
  cache-series lines, the depth (`ROOT`) line, the CACHE path line and the
  sha pin line changed, diff-verified): run twice per scenario, all four
  outputs byte-identical per run (determinism 6/6 runs); all other pins
  unchanged; baseline control holds (root first=27: 119/119 free thirds,
  identical per-root free coverage in every scenario).
- Deltas gated through `scripts/compare_deltas_batch11.py` ->
  `output/decomp-deltas-batch11.json` (sha256
  `99c744b90f0ed9d024f7e644586e15d902055723cd8a622113cd2507eb812d75`).
  The compare script also re-executes the published refresh class-status
  semantics faithfully from the graph + update8 receipt + scenario cache
  (verdict-level statuses and the Board fail-closed verification for free
  candidates) and asserts every recomputed `class_status_count` equals the
  published summary for BASE and all three scenarios before any delta is
  reported. The scenario `probe-worklist.csv` outputs (3.8 MB each,
  regenerable byte-identically from the pinned inputs) are not published
  (lane convention; sha256 recorded here: BASE
  `1807e4d21f6fb757ea21850c6bda4d822cb76ac59abfa9bcd1cc7b53bd7055ef`,
  PWINZ003 `82dbd7750215e4f7b981691b4059478555774c88008dad9bb5418191bb1a5852`,
  PLOSS3 `ec123c7450ef1533bb5b78c68b43c4493beec6967c8fc95c58e98b36a2f75b64`,
  PFULL4 `2ac35775425b4e94c46860ade2380aa93491032fca90bf7c7f8a368878a7309a`).

## Machine-verified decomposition (deltas vs the Part Y canonical re-audit)

| metric | base | PWINZ003 (z003 WIN only) | PLOSS3 (3 LOSS) | PFULL4 (4 rows) |
|---|---|---|---|---|
| excluded_now | 23 | **26** (+3) | 23 (0) | 26 (+3) |
| free_now | 35 | 35 | 35 | 35 |
| unknown classes | 34,501 | 34,498 (-3) | 34,501 (0) | 34,498 (-3) |
| update8 remaining | 31,784 | **31,726 (-58)** | 31,783 (-1) | 31,726 (-58) |
| update8 resolved | 75 | 76 (+1) | 76 (+1) | 77 (+2) |
| win-hit groups | 0 | **5** | 0 | 5 |
| joint greedy size | 35,242 | 35,241 (-1) | 35,241 (-1) | **36,039 (+797)** |
| probe worklist | 65,154 | 65,152 (-2) | 65,150 (-4) | 65,148 (-6, additive) |
| root {X,60,27} free thirds | 119 | 119 | 119 | 119 |

- **excluded_now flips (PWINZ003 = PFULL4): exactly 3 classes =
  {5307, 5748, 8785}**, machine-identified from the frozen graph as the
  classes holding s5 198530 as a cost child (membership_class_count 3,
  three-way agreement). Class 8785 self-excludes (like 5473 for g018, 1518
  for j033, 2634 for h045); peers 5307 and 5748 exclude on this single WIN
  regardless of their remaining unknown children (published refresh
  semantics). PLOSS3 flips: empty (gate).
- **class 8785 unknown_now: 51 -> 50 / 48 / 47** (WIN-only -1, LOSS-only -3,
  full -4; additivity machine-gated). Renewed closure rank: class 8785
  remains a refutation-evidence holder (z003) in every scenario.
- **update8 (frozen joint plan refresh): the z003 WIN hits exactly 5
  groups, all served by class 5748** (s4_mask `[1225542048598196224, 1]`,
  groups first=16/third 59,61,104 and first=49/third 56,64 with reply 60,
  fourth swapped within each pair; each group's unknown_s5_children count
  58). Newly resolved baseline requirements: PWINZ003 `{198530}` (z003
  itself), PLOSS3 `{211089}` (z004), PFULL4 `{198530, 211089}`. Remaining
  delta is sub-additive by exactly 1 (PW -58, PL -1, full -58): s5 211089
  (z004) is also a cost child of class 5748 (machine-verified from the
  frozen graph), so its separate LOSS resolution is subsumed by the
  win-hit group unknown-set drops of the full scenario. z001/z002 (s5
  86114/100564) are not update8 baseline requirements (resolved update8
  count unchanged by the loss rows: 76 -> 76 there only via z004).
- **joint greedy is NOT additive for this packet**: WIN-only -1,
  LOSS-only -1, full **+797** (36,039). Per-root greedy_union_size changed
  only at root 49 (2,890 -> 2,899 in each single-row scenario, +9; 2,946
  in the full scenario, +56; every other root byte-identical, per-root
  free coverage identical everywhere). The joint-union growth beyond the
  root-49 per-root growth comes from greedy option re-selection cascades
  across roots (selection ordering shifts under the packet's exclusion and
  resolution changes); group_best_options_nonfree is 2,127 in all four
  runs. This is a scheduling-quantity effect of the frozen greedy
  pipeline, not a coverage or verdict claim: contrast Part V (h045:
  full == loss-only) and Part R (j033: full sub-additive by 1) - the joint
  greedy pipeline is sensitive to which classes are excluded and which
  options resolve jointly.
- Scheduling quantities only: `worklist_total` is fully additive
  (-2 -4 = -6). Unknown class count and excluded_now/class-status counts
  are WIN-only driven as in Part H-bis (LOSS rows move only the scheduling
  option pool: worklist; and the resolved/remaining bookkeeping).

## Honesty record

- Verdicts NOT consumed. z003 remains the 8th unconsumed closure WIN
  (b018/d002/e002/f017/g018/j033/h045/z003), scrutiny owner (C++
  second-implementation gate pin `9193f5b6...` precedent, unchanged).
  The scenario caches are analysis-only; adopting or discarding them is
  the scrutiny owner's decision; this lane does not rewrite the canonical
  cache. The standard 11x11 empty board, the 19 central-reply roots,
  class 8785 (unknown stays 51 in the canonical cache; 47 only under the
  full what-if) and class 8106 remain UNKNOWN throughout. Node counts are
  not verdicts. Win-hit groups, greedy sizes and worklist sizes are
  scheduling quantities and carry no class status.
