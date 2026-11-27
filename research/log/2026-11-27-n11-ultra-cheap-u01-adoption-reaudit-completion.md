# n11 ultra-cheap u01 adoption flip-census/reaudit: completion log

**Part completed (declared, then executed).** The follow-up Part
declared in
`research/experiments/n11-ultra-cheap-u01-adoption-reaudit-20261127/DECLARATION.md`
(declaration commit `740c980b`, publish-then-execute) is complete:
the BASE (`1e2eeda2...`, eleventh-cost k01 head of record, 6,890
rows WIN 208 / LOSS 6,682) vs SCENARIO (`0ec4080d...`, the adopted
ultra-cheap u01 head of record, 6,891 rows WIN 209 / LOSS 6,682)
class-status census measurement and the reaudit refresh of the new
canonical head.

## What ran

- Refresh `refresh_adoption_ultra_cheap_u01.py` (`d0fa1762...`,
  byte-clone of the published eleventh refresh `0355d7fb...`,
  three-region-only transform machine-verified): three sequential
  fresh-cold runs against sha-pinned inputs (graph `54f9c364`,
  update8 `b658290a`, Board `954d3a10`, policy `78655e94`,
  quarantine `81d23160`, SCEN cache `0ec4080d`); all output sets
  byte-identical (`refresh-summary.json` `2e27ad1a`,
  `closure-classes.csv` `e97ab986`, `per-root-coverage.csv`
  `d2d36539`, worklist regen `5feaba28`/3,715,117 bytes).
- Measurer `measurer_adoption_ultra_cheap_u01.py` (`c5ff4883...`,
  structural adaptation of the eleventh measurer `f286f165...`,
  fail-closed sha gates on every BASE input, independent census
  replication exact on both sides, tamper battery 4/4): three runs
  byte-identical (`census-deltas-ultra-cheap-u01-adoption.json`
  `a1a84a3e`).

## Measured result

- Census unknown 34,388 -> 34,385, excluded_now 132 -> 135, free_now
  39 -> 39 (Board-verified both sides), excluded 390 -> 390.
- The adopted WIN row u01 (`1153485622925590528:0`, s5 index
  81011, serving class 1849) flips exactly its THREE owner classes
  unknown -> excluded_now: 1849 (cost-unknown 1 -> 0; LEAVES the
  closure ladder 804 -> 803 rows, 785 rank-churn cells), 1858
  (96 -> 95) and 5160 (56 -> 55; the ladder's single unknown_now
  churn cell; six added win-hit groups, 25 -> 31).
- Per-root: root 36 individual greedy 3,001 -> 3,029, root 49
  2,696 -> 2,693 (free_now/uncovered identical on all 20 roots);
  joint greedy 37,398 -> 43,776 (scheduling quantity, NOT a
  coverage claim); probing worklist 64,272 -> 64,270 rows.
- update8: the adopted s5 index 81011 sits INSIDE the frozen
  baseline requirement (resolved 282 -> 283, remaining_now 31,444
  -> 31,388, groups_free_now 131 -> 131).

## Deviation from the pre-registered expectation (experimental fact)

The declaration pre-registered ONE flip (unknown 34,387 /
excluded_now 133).  Measured: THREE flips (unknown 34,385 /
excluded_now 135).  Cause: the WIN key has three owner classes, the
same three-owner pattern the eleventh-cost k01 WIN measured.  The
measured values supersede the prediction; nothing was adjusted.

## Next

- Next selection under the new head `0ec4080d...` (ultra-cheap
  wave-B raws remain unpublished pending pre-audit Stage B; u02-u04
  stay 2M UNKNOWN, re-escalation needs a fresh declaration).
- Kit: `research/experiments/n11-ultra-cheap-u01-adoption-reaudit-20261127`
  (MANIFEST `8ccb7150...`).

## Guards

Adoption bookkeeping only: NO root verdict consumed, NO class freed,
NO root excluded.  Nodes are bookkeeping.  The standard 11x11 empty
board, every central-reply root, the two-stone root {60,27} and its
remaining third moves {100,108} stay UNKNOWN.
