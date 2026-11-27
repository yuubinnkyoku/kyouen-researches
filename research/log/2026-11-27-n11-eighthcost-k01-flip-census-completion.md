# 2026-11-27 n11 eighth-cost k01 WIN adoption flip-census completion

Completion log of the FOLLOW-UP Part declared in the eighth-cost k01
WIN row canonical adoption (completion log of d108bae0, adoption
manifest `follow_up_declared`): the class-status flip census
measurement (win-hit mechanism) of the serving class
1297036692750860288:0 owner set, BASE 5b6e77f7 (6,874 rows WIN 202 /
LOSS 6,672) vs SCEN 0935c94c (6,875 rows WIN 203 / LOSS 6,672), with
the reaudit refresh of the new canonical head of record.

Kit: research/experiments/n11-eighthcost-k01-win-adoption-reaudit-20261127
(README, MANIFEST-sha256.txt, measurer + 3-region byte-clone refresh,
refresh outputs, census json).  Publication waves: kit scripts+README+
MANIFEST first, outputs second; execution preceded publication
(disclosed; the Part was pre-declared before any run, Part SZ wave E
precedent).

## Measured results

- Census BASE -> SCEN: unknown 34,403 -> 34,400; excluded_now
  117 -> 120; free_now 39 -> 39 (Board-verified both sides);
  excluded 390 -> 390.  Recount reproduces both published/refreshed
  summaries exactly.
- WIN-side flips: exactly 3 classes, all graph-time owner classes of
  the adopted k01 WIN row 1297036692750860288:64 (s5 index 91779):
  2182 (1154117773392084992:0), 2197 (the eighth-cost serving class
  1297036692750860288:0, cost-unknown 100 -> 99) and 16914
  (1152921504675004416:64), each unknown -> excluded_now.  Flip list
  == owner set exactly; no other flip direction; owner histogram
  {"3": 1}.
- update8: adopted index 91779 (WIN) is OUTSIDE the frozen baseline
  requirement; resolved 282 -> 282, remaining_now 31,444 -> 31,444;
  win-hit group set unchanged (25).
- Closure ladder 804 -> 804: entered/left/unknown_now/rank churn ALL
  empty, and closure-classes.csv is BYTE-IDENTICAL to the BASE side
  (unlike the seventh-cost 42-row adoption, nothing re-ranks).
- Per-root coverage byte-identical on all 20 roots (no greedy
  re-route); joint greedy 37,398 -> 37,398; worklist total
  64,273 -> 64,273 (regen sha 76b77442..., same size as the BASE pin
  2987300a...; unpublishable per size policy, pin only).

## Verification

- Refresh: 3 runs, 4 outputs byte-identical each (summary ff5c1586,
  closure ae1d0a7f, per-root 81b17904, worklist 76b77442; stdout
  d96dbef4 x3).  3-region clone verified against the published SZ
  wave E refresh d8b14697 (only docstring / CACHE path / expected
  cache sha differ).
- Measurer: 2 runs byte-identical (census json 9f25fd99 x2), all
  fail-closed gates PASS (pin gates for both caches, increment,
  manifest, merger, graph, BASE reaudit outputs; census recount both
  sides; flip == owner set; closure/per-root byte-identity; update8
  arithmetic; worklist pins).
- Tamper battery 5/5 fail-closed (T1 scen census value flip / T2
  increment WIN->LOSS / T3 scen closure unknown_now flip / T4 phantom
  excluded_now / T5 phantom closure row 805) + restored clean control
  rc=0 byte-identical.

## Non-meaning

The k01 S5 WIN row is consumed as cache bookkeeping only.  The flips
are scheduling bookkeeping: no root verdict, no root freed, no root
excluded, no coverage claim.  The standard 11x11 empty board, all 19
central-reply roots, the two-stone root {60,27}, its remaining third
moves {100,108}, S2 and all closure classes stay UNKNOWN.  Nodes are
bookkeeping, never verdicts.

## Resume notes

- Next eighth-cost selection must be a fresh selector run (mold:
  select_eighth_exclusive.py sha ac896d94, head basis now 0935c94c,
  6,875 rows); the 42 WIN-stopping-rule suppressed keys stay
  UNKNOWN-pair-at-2M and fresh vs BASE.
- The four remaining one-verdict-from-completion classes
  (16371/23101/1849/2251) measured in the Part SZ wave E refresh are
  unchanged by this Part (closure ladder byte-identical).
