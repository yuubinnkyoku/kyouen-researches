# 2026-11-27 n11 eleventh-cost k01 adoption flip-census + reaudit completion

Completion log of the follow-up Part declared in the eleventh-cost k01
canonical adoption completion log and in the adoption kit README ("the
flip-census/reaudit review of the serving class 1297036696978718720:0
owner set is the next follow-up Part").  Kit:
`research/experiments/n11-eleventhcost-k01-adoption-reaudit-20261127/`
(8 published files; the probe-worklist.csv regen is sha-pinned but
unpublished per size policy).

## Refresh (byte-clone lineage, 3 runs byte-identical)

- refresh_adoption_eleventhcost_k01.py sha256 0355d7fb... is a
  byte-clone of the published tenth-cost k01/k02 refresh 280d7062...
  differing in EXACTLY the three regions (docstring, CACHE path,
  expected cache sha); verified by machine diff of the code region
  (exactly 2 changed lines: CACHE, CACHE_SHA_EXPECTED).
- Refreshed census against the adopted head 1e2eeda2 (6,890 rows
  WIN 208 / LOSS 6,682): unknown 34,388 / excluded_now 132 /
  free_now 39 (Board-verified, rejected 0) / excluded 390.
- refresh-summary.json sha256 abaf62aad...; closure-classes.csv
  sha256 d7ae77dd... (byte-identical to the tenth-cost BASE side;
  804 rows, no churn); per-root-coverage.csv sha256 03fd32f2...;
  probe-worklist regen sha256 407a340f... (64,272 rows,
  3,715,222 bytes).

## Flip-census measurement (measurer f286f165..., 3 runs
byte-identical; census json e1811434...)

- The adopted WIN row k01 `1297036696978718720:64` (s5 index 97250)
  flips exactly its THREE owner classes unknown -> excluded_now
  (win-hit, the Part EW/EM mechanism): 2376
  `1297036696977670144:64` (cost-unknown 109 -> 108), 3288 (the
  eleventh-cost serving class `1297036696978718720:0`, cost-unknown
  102 -> 101), 17116 `1152921504607895808:64` (99 -> 98).
- Census: BASE 34,391/129/39/390 -> SCEN 34,388/132/39/390; no class
  flips to free_now; free_now stays 39 both sides.
- MEASURED individual greedy re-route: root 2's individual greedy
  union drops 6,132 -> 6,131 (the only per-root CSV difference;
  free_now/uncovered identical on all 20 roots).
- Joint greedy 37,398 -> 37,398; worklist 64,272 -> 64,272 rows;
  update8 resolved 282 -> 282, remaining_now 31,444 -> 31,444,
  groups_free_now 131 -> 131; the adopted s5 index sits outside the
  frozen baseline requirement; the win-hit group set is unchanged
  (25 groups; the flipped classes are disjoint from every update8
  plan group class).
- All measurer inputs re-fetched from main and sha-verified before
  the run (BASE cache 16b34014, SCEN cache 1e2eeda2, increment
  0f627887, manifest 6442d01d, tenth reaudit BASE side
  40268a5e/d7ae77dd/8cc804bb, graph 54f9c364, update8 b658290a,
  board 954d3a10, policy 78655e94, quarantine 81d23160, merger
  90711961).

## Honest disclosures

- The refresh is memory-heavy; the three determinism runs of the
  refresh and of the measurer were executed strictly sequentially
  (no parallel launch).
- The measurer's pre-registered expectations (flip list, greedy
  re-route, worklist pins) were machine-measured before publication
  of the kit; every expectation is asserted against the graph-derived
  recomputation, not taken from the measurement alone.
- This lane runs without access to the user's computer (scheduled
  task); publication is via the GitHub API only.

## Next work

- Twelfth-cost class selection under the new head 1e2eeda2 (fresh
  selector, template = eleventh selector 431e3f55; the eleventh
  serving class 1297036696978718720:0 is excluded_now under the new
  head and cannot be re-selected).
- The 45 suppressed keys (k02..k46) stay 2M-UNKNOWN bookkeeping.

## Guards

Class-status bookkeeping only: NO root verdict is consumed, NO class
freed, NO coverage claim made or changed.  The standard 11x11 empty
board: UNKNOWN.  All 19 central-reply roots: UNKNOWN.  Two-stone root
{60,27}: UNKNOWN.  Third-move pair {100,108}: UNKNOWN.  Nodes are
bookkeeping, never verdicts.
