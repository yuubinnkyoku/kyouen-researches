# n11 central-reply: batch-6 (class 5473) g018 WIN if-adopted decomposition (2026-11-22)

IF-ADOPTED scenario analysis for the batch-6 WIN-HALT key **g018**
(s5_index 184684, key `[1734519175235239936, 0]`, legal 78, result 1 WIN,
5,936,863 nodes, 2-pass node-exact; see
`../n11-centralreply-closure-class5473-batch6-20261122/`, declaration Part I).
The lane does NOT consume the verdict (pre-registered rule: WIN rows go to the
verdict-scrutiny owner, as b018, d002, e002, f017). Following the Part H-bis
methodology (machine-separated WIN-only vs LOSS-only vs full scenario), this
experiment answers, fail-closed: **what would change if (a) only the g018 WIN
row, (b) only the 17 batch-6 LOSS rows, or (c) all 18 probed rows were
adopted**.

## Construction

- increments built fail-closed from the batch-6 raw 2-pass replay rows by
  `scripts/make_increments_batch6.py` (every row cross-checked pass-vs-pass
  node-exact, key/legal cross-checked against the batch-6 worklist inputs;
  18 rows = 17 exact LOSS + g018 WIN; sha256 in `output/`):
  `increment-batch6-probed-18rows-IFADOPTED-20261122.cache` (18 rows),
  `increment-batch6-wing018-only-IFADOPTED-20261122.cache` (1 WIN row),
  `increment-batch6-gloss17-only-IFADOPTED-20261122.cache` (17 LOSS rows)
- fail-closed union merge onto the canonical 5,924-row merged cache
  (published merger, selftest PASS, conflicts 0):
  `pwing018/` 5,925 rows WIN 159 / LOSS 5,766 sha256
  `3e77daae...`; `pgloss17/` 5,941 rows WIN 158 / LOSS 5,783 sha256
  `d97a307e...`; `pfull18/` 5,942 rows WIN 159 / LOSS 5,783 sha256
  `b839abfc...`; audits `*/output/merge-audit-ifadopted.json`
- `scripts/refresh_19root_frontier.py` (one byte-copy per scenario with only
  the depth line, merged-cache path and sha pin changed, 3 lines each): run
  twice per scenario, all four outputs byte-identical each time
  (determinism 2/2 per scenario, 6/6 runs); all other pins unchanged;
  baseline control holds (root first=27: 119/119 free thirds)
- deltas gated through `scripts/compare_batch6_deltas.py` ->
  `output/decomp-deltas-batch6.json`

## Machine-verified decomposition (deltas vs the canonical re-audit)

| metric | base | PWIN18 (g018 only) | PLOSS17 (17 LOSS) | PFULL18 (18 rows) |
|---|---|---|---|---|
| excluded_now | 23 | **27** (+4) | 23 (0) | 27 (+4) |
| free_now | 33 | 33 | 33 | 33 |
| unknown classes | 34,503 | 34,499 (−4) | 34,503 (0) | 34,499 (−4) |
| update8 remaining | 31,838 | **31,787** (−51) | 31,821 (−17) | 31,787 (−51) |
| update8 resolved | 21 | 22 (+1) | 38 (+17) | 39 (+18) |
| win-hit groups | 0 | 4 | 0 | 4 |
| joint greedy size | 35,617 | **35,617 (0)** | 35,617 (0) | 35,617 (0) |
| probe worklist | 65,213 | 65,212 (−1) | 65,194 (−19) | 65,193 (−20) |
| root {X,60,27} free thirds | 119 | 119 | 119 | 119 |

- **excluded flips (PWIN18 = PFULL18): exactly 4 classes**, machine-identified
  from the frozen dependency graph as the S4 classes holding s5 184684 as a
  cost child: `4889`, `4892`, `5473`, `5501`. Class 5473 itself joins the
  excluded set (its own child is the WIN).
- **update8 win-hit: 4 groups, all via class 5473** (root first=26:
  thirds 59/92-kernel with fourth 92/59 and the mirrored record; root first=49:
  thirds 46/52 with fourth 52/46 and the mirrored record; reply 60), inside
  the machine-checked frozen-plan selection; per-root remaining drops on
  root 26 (11,689 -> 11,587, −102) and root 49 (10,918 -> 10,816, −102),
  union remaining_now −51.
- **WIN-vs-LOSS attribution (Part H-bis methodology)**: the WIN-only scenario
  delivers ALL class-status benefit (excluded +4, unknown −4, remaining −51).
  The 17 LOSS rows add only resolved_among_baseline_requirement (+17,
  additive: 1+17=18) and worklist reduction (−19, additive −1−19=−20).
  update8 remaining is NOT additive here either: −51 (WIN) + −17 (LOSS) vs
  −51 (full) - the WIN-side resolution subsumes the LOSS-side keys, the same
  subsumption shape Part H-bis measured for the packet (P4+P21==P25 except
  WIN-side containment).
- **joint greedy is UNCHANGED in all three scenarios (35,617)** - unlike the
  batch-5 packet adoption (+1,367), adopting g018 (with or without the batch-6
  LOSS rows) does not raise the joint 19-root plan cost on this host at these
  inputs. The f017 greedy increase was measured (Part H-bis) to be a property
  of the f-batch's LOSS completeness; no such effect occurs in batch 6.
- **class-5473 scheduling after the batch**: with only the 17 LOSS rows
  adopted (PLOSS17), class 5473's unknown count falls 51 -> 34 and it becomes
  closure rank 2 (after the 16757 remnant); with the full 18 rows (PFULL18),
  unknown 33 and also rank 2. If the g018 WIN is adopted, class 5473 leaves
  the closable set entirely (excluded) and the first clean candidates beyond
  the refuted quartet + 5473 are rank 7 class `10324` and rank 8 class `2634`
  (both 51 unknown, no evidence either way - untouched scheduling quantities).
- free_now 33, board verification 33/33 and rejected 0 are unchanged in every
  scenario; the 23963 closure and all achieved coverage are unaffected.

## Caveats (honest)

- The batch-6 raw rows g011-g018 were computed after the repository's public
  endpoints returned 404 mid-session (2026-11-22 ~04:52Z); rows g001-g010 and
  the scaffold/declaration were published before (commits `09f24c62`,
  `729be22c`). The remaining publish payloads are staged in the lane kit and
  this experiment ships together with them.
- Budget exhaustion would be an honest UNKNOWN; it never occurred (all 18
  rows settled within the 15M budget).

## Verdict for the scrutiny owner

Adopting the g018 WIN row (with or without the 17 batch-6 LOSS rows) would:
flip classes 4889/4892/5473/5501 excluded, reduce update8 remaining to
31,787, leave free coverage, board verification and the joint greedy plan
cost unchanged, and remove class 5473 from the closable set. The adoption
gate stays with the scrutiny owner (C++ second implementation pin
`9193f5b6...` or equivalent); nothing here consumes the verdict.

Read-only planning computation. No verdict is consumed. No class, root,
coverage or closure claim is made. The standard 11x11 empty board and all 19
central-reply roots stay UNKNOWN. Nodes are not verdicts.
