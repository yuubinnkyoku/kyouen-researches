# Part EU wave-D repair feasibility diagnostic (2026-11-26, same session as the resumption log)

This NOTE records a THROWAWAY LOCAL DIAGNOSTIC only.  No official Part EU
artifact, kit member, or output was produced or modified by it; published
bytes are untouched (verified below).  It is evidence FOR the wave-D repair
decision that the resumption log (commit baa8a0c0) explicitly deferred, so
the next owner session can act on proven facts.

## Setup (single disclosed substitutions, throwaway copies)

* The published extractor `compare_deltas_eu_adoption.py` (pin aaf13bdc)
  was copied to a scratch location inside the local verification tree with
  EXACTLY TWO byte substitutions, both disclosed:
  1. `SCEN_REFRESH_SHA`: `a377eea0...` (the declaring session's fork,
     bytes never published and not recoverable - see the resumption log
     section 3) -> `353f15d3...`, the regenerated disclosed-diff fork
     of this session (diff vs the published Part ER refresh `6c91e0ce`
     verified to hold exactly the 3 declared regions: CACHE path,
     expected cache sha, docstring; every computation byte identical).
  2. `DECOMP_OUT` rerouted to a /tmp diagnostic path so no official
     `output/decomp-deltas-euwin2-adoption.json` is produced.
* The diagnostic copy is not published and not placed on main; the
  published extractor is byte-unchanged (sha re-verified after the run).

## Result: the full battery PASSES under the single-pin substitution

`python3 <diag extractor>` -> rc=0, wall ~126 s (the two refresh
re-execution double-runs included).  Final line:

```
EU decomp OK: flips=6 caches=6765->6767 win=186->188 closure_left=[]
greedy=36619->36619 decomp_sha=8d4a5743...
```

That means, with the substitution and NOTHING ELSE changed, the extractor
verified ALL of: the 25-object pin list (BASE/SCEN caches, increment,
manifest, maker, ER increment, b38 SSOT, both published refresh-output
trios, the published ER refresh script, the merger, the 3 merge-audits,
graph/update8/board/policy/quarantine); the manifest decomposition
(every row, provenance, out-of-scope declarations); the SCEN==BASE+2-rows
decomposition (6,767 rows WIN 188 / LOSS 6,579); BOTH refresh forks
re-executed byte-verbatim in isolated scratch trees reproducing all
EIGHT outputs byte-identically to the published/regenerated pins
(including the worklist regen pins 78e499dd / 397a4379); the independent
full census with EXACTLY 6 UNKNOWN->excluded_now flips, exactly the
declared owner classes {12846, 12875, 13801, 30282, 30308, 30326} with
30345 NOT double-flipping; the Board-recomputed class boundary arithmetic
for 30345 (51 raw / 50 cost, unknown 7->5), the six flipped owner classes,
and 30354 (97/97, 96 static); closure-classes churn only
{30345: unknown 7->5; rank 8->7} + {20421: rank 7->8}, zero rows
left/entered; the win_hit groups unchanged; the per-root coverage deltas
only at roots 12 (2850->2848) and 36 (3007->3005); update8 static
(31,859 / 260 / 131); joint greedy 36,619 static;
group_best_options_nonfree 2,105 static; worklist 64,309 -> 64,307.

## What this proves and what remains open

* The wave-D repair option (resumption log section 3, option 2) is
  PROVEN viable end-to-end: substituting the one unrecoverable pin with
  the disclosed-diff fork (whose outputs are bit-identical to all four
  declared refresh output pins) lets the published-battery logic run to
  full PASS.
* Non-official diagnostic decomp: sha256
  `8d4a574359dd8f5c8e1bc140fbd4fefc533fcf71049bc80f9d06a9fdc8dcba00`
  (produced by the substituted extractor; NOT the official wave-D
  artifact and not published as one).
* Still open (owner decision, NOT taken here): whether to publish the
  wave-D repair (wave D with the fork `353f15d3` + a disclosed
  single-pin repair of the kit extractor pin `a377eea0` -> `353f15d3`,
  then waves E/F), or hold for exact `a377eea0` byte recovery.  Until
  the Part closes, the canonical BASE stays the Part ER head `9c4dd94e`.
* 11x11 stays UNKNOWN; every root stays UNKNOWN; nodes are bookkeeping;
  no verdict is consumed anywhere by this diagnostic.
