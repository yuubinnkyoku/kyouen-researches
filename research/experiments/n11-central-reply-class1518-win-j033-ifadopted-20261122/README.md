# n11 central-reply: batch-9 (class 1518) j033 WIN if-adopted decomposition (2026-11-22)

IF-ADOPTED scenario analysis for the batch-9 WIN-HALT key **j033**
(s5_index 69347, key `[1153484455030030336, 0]`, legal 80, probe_order 364,
result 1 WIN, 4,718,280 nodes, 2-pass node-exact; see
`../n11-centralreply-closure-class1518-batch9-20261122/`, declaration Part Q).
At the halt 33/51 keys were probed (j001-j032 all exact LOSS + j033 WIN;
j034-j051 untouched). The lane does NOT consume the verdict (pre-registered
rule: WIN rows go to the verdict-scrutiny owner, as b018, d002, e002, f017,
g018). Following the Part H-bis / Part J methodology (machine-separated
WIN-only vs LOSS-only vs full scenario), this experiment answers,
fail-closed: **what would change if (a) only the j033 WIN row, (b) only the
32 batch-9 LOSS rows, or (c) all 33 probed rows were adopted**.

## Construction

- increments built fail-closed from the batch-9 raw 2-pass replay rows by
  `scripts/make_increments_batch9.py` (every row cross-checked pass-vs-pass
  node-exact at budget 15M, key/legal cross-checked against the batch-9
  worklist inputs; 33 rows = 32 exact LOSS + j033 WIN; sha256 in
  `output/`):
  `increment-batch9-probed-33rows-IFADOPTED-20261122.cache` (33 rows,
  sha256 `80c83c399ab28ab3769528374ba3dfd260ff555e3c9ef92fdc01085f0445edd8`),
  `increment-batch9-winj033-only-IFADOPTED-20261122.cache` (1 WIN row,
  sha256 `d7f4f48561d1b5b9c365bac1b8cb2630e1522cfc16131417e838e208886c383b`),
  `increment-batch9-loss32-only-IFADOPTED-20261122.cache` (32 LOSS rows,
  sha256 `c216005e1894a5dc8b1b81a44e0576fc72054a1f83978e16689127866ff24cdf`)
- fail-closed union merge onto the canonical 5,975-row merged cache
  (sha256 `a998f4c0...`, published merger, selftest PASS, conflicts 0,
  duplicates 0):
  `pwinj033/` 5,976 rows WIN 159 / LOSS 5,817 sha256
  `27da260497a66021323987330e07b2f840ef17fc6d1a8a991073be8c7c26037f`;
  `ploss32/` 6,007 rows WIN 158 / LOSS 5,849 sha256
  `f83825bb8bd5c097ee8d5e567ef9a7f38bac4543f6e65bc257e6d1b0bce09aab`;
  `pfull33/` 6,008 rows WIN 159 / LOSS 5,849 sha256
  `882fe1632a9ce2375aad8766e86885a5fbf3e9ee2359080f9140e2cc19345f69`;
  audits `*/output/merge-audit-ifadopted.json`
- `scripts/refresh_19root_frontier.py` (one byte-copy per scenario, only
  the depth line, merged-cache path and sha pin changed, 3 lines each,
  diff-verified against the pinned Part M re-audit script): run twice per
  scenario, all four outputs byte-identical each time (determinism 6/6
  runs); all other pins unchanged; baseline control holds (root first=27:
  119/119 free thirds)
- deltas gated through `scripts/compare_batch9_deltas.py` ->
  `output/decomp-deltas-batch9.json`

## Machine-verified decomposition (deltas vs the Part M canonical re-audit)

| metric | base | PWINJ033 (j033 only) | PLOSS32 (32 LOSS) | PFULL33 (33 rows) |
|---|---|---|---|---|
| excluded_now | 23 | **25** (+2) | 23 (0) | 25 (+2) |
| free_now | 34 | 34 | 34 | 34 |
| unknown classes | 34,502 | 34,500 (−2) | 34,502 (0) | 34,500 (−2) |
| update8 remaining | 31,836 | 31,836 (0) | 31,835 (−1) | 31,835 (−1) |
| update8 resolved | 23 | 23 (0) | 24 (+1) | 24 (+1) |
| win-hit groups | 0 | 0 | 0 | 0 |
| joint greedy size | 35,857 | 35,856 (−1) | **35,235 (−622)** | 35,235 (−622) |
| probe worklist | 65,155 | 65,153 (−2) | 65,111 (−44) | 65,109 (−46) |
| root {X,60,27} free thirds | 119 | 119 | 119 | 119 |

- **excluded flips (PWINJ033 = PFULL33): exactly 2 classes**,
  machine-identified from the frozen dependency graph as the S4 classes
  holding s5 69347 as a cost child: `1518` and `4843` (both base-unknown,
  cross-checked twice: the PWIN unknown-changed row set and the PFULL minus
  PLOSS per-class unknown delta both equal the graph holder set, and the
  batch-9 worklist membership_class_count of j033 was 2). Class 1518 itself
  joins the excluded set, same self-exclusion shape as 5473 under g018
  (Part J). Class 4843 is a peer holder (base closure rank 123, unknown 58
  -> 57, rank 123 -> 97 under PWIN).
- **update8: the j033 WIN carries NO win-hit groups and no
  baseline-requirement resolution** (remaining unchanged, resolved
  unchanged, win-hit 0), in deliberate contrast to the batch-6 g018 WIN
  (4 win-hit groups, remaining −51). The single LOSS-side resolution is
  `j016 -> s5 69330` (resolved 23 -> 24, remaining −1), additive and
  identical under PLOSS32 and PFULL33.
- **joint greedy: the 32 batch-9 LOSS rows reduce the joint 19-root plan
  cost by 622 (35,857 -> 35,235)** - the first measured greedy REDUCTION in
  the closure-grind lane (batch-5 f-LOSS packet raised it +1,372, batch-6
  was neutral, Part H-bis / Part J). Main per-root greedy movers under
  PLOSS32: root 15 (5,991 -> 5,916, −75) and root 26 (5,203 -> 5,131, −72).
  The WIN-only greedy effect is −1 (subsumed by the LOSS-side set in
  PFULL33; greedy is sub-additive by exactly 1). Worklist deltas are
  exactly additive: −2 (WIN) + −44 (LOSS) = −46 (FULL).
- **class-1518 scheduling after the packet**: PLOSS32 leaves class 1518
  unknown 51 -> 19 and moves it to closure-classes rank 1 (probe_order 1,
  next unresolved key j033; its 18 further class rows follow). PFULL33
  leaves unknown 18, also rank 1 (next key j034, s5 69348). Under any
  adoption scenario, finishing class 1518 becomes the single cheapest
  closable move in the ranking. The remaining 18 batch-9 keys (j034-j051)
  were NOT probed here.
- free_now 34, board verification 34/34 and rejected 0 are unchanged in
  every scenario; the 10324/23963 closures and all achieved coverage are
  unaffected. Per-root free coverage is identical to base in all three
  scenarios (machine gate).

## Caveats (honest)

- The lane environment still cannot run the C++ second-implementation
  adoption gate (no compiler; package installs forbidden), so the j033 WIN
  stays unconsumed and with the scrutiny owner. A third-implementation
  (`third_impl.js` pin `08ea958f...`) spot verification of j033 in the
  Part K/O/P style was NOT run in this session and remains open.
- Budget exhaustion would be an honest UNKNOWN; it never occurred (all 33
  rows settled within the 15M budget).
- The scenario caches (5,976 / 6,007 / 6,008 rows) are analysis-only
  artifacts; the canonical merged cache remains the 5,975-row
  `a998f4c0...`.

## Verdict for the scrutiny owner

Adopting the j033 WIN row (with or without the 32 batch-9 LOSS rows) would:
flip classes 1518 (itself) and 4843 excluded, reduce unknown classes by 2,
reduce the probe worklist by 2, reduce the joint greedy plan cost by at most
1, resolve no update8 requirement through the WIN itself (win-hit 0), and
leave free coverage and board verification unchanged. The 32 LOSS rows (a
separate adoption decision with the usual fail-closed merge rules) resolve
one baseline requirement (s5 69330), cut the worklist by 44 and cut the
joint greedy by 622. The adoption gate stays with the scrutiny owner
(C++ second implementation pin `9193f5b6...` or equivalent); nothing here
consumes the verdict.

Read-only planning computation. No verdict is consumed. No class, root,
coverage or closure claim is made. The standard 11x11 empty board and all 19
central-reply roots stay UNKNOWN. Nodes are not verdicts.
