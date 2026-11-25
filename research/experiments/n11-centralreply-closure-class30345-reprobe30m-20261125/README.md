# n11-centralreply-closure-class30345-reprobe30m-20261125 (Part ES, 2026-11-25)

Part ES: re-probe of the 6 batch-38 honest-EXHAUSTED keys of closure class
30345 at the 30M DIFFERENT condition.  Declared at
`research/log/2026-11-25-part-es-class30345-reprobe30m-declaration.md`
(commit `de2e8bf3`) under the publish-then-execute convention; kit published
at `e84ab297`; results below were produced AFTER publication, entirely in
this single session (2026-11-25 UTC).

Nothing here consumes any verdict.  Probe-level honest labels only: the 2
WIN rows are UNCONSUMED probe-level WINs (canonical adoption is the
scrutiny-owner C++ second-implementation gate's exclusive right); the 4
LOSS rows are Part-EM loss-only adoption territory, equally unconsumed.
The standard 11x11 empty board stays UNKNOWN.  All 19 central-reply roots
stay UNKNOWN.  nodes are bookkeeping, never verdicts.

## Result: all 6 targets RESOLVED at 30M (no exhaustion)

| key_id | s5_index | lo | hi | label @30M | nodes (2-pass node-exact) | 15M label (Part EF) |
|---|---|---|---|---|---|---|
| ai007 | 441292 | 1152922604118478880 | 65536 | WIN (unconsumed) | 16,090,493 | EXHAUSTED |
| ai024 | 889534 | 1152922604118479104 | 65536 | LOSS (unconsumed) | 19,127,057 | EXHAUSTED |
| ai030 | 894456 | 1152921573327372288 | 17825792 | LOSS (unconsumed) | 16,504,156 | EXHAUSTED |
| ai038 | 898436 | 1152927002164989952 | 65536 | LOSS (unconsumed) | 19,851,840 | EXHAUSTED |
| ai040 | 899584 | 1152922604118487040 | 65536 | WIN (unconsumed) | 20,711,023 | EXHAUSTED |
| ai041 | 900170 | 1152921573327372288 | 34603008 | LOSS (unconsumed) | 15,781,960 | EXHAUSTED |

Every resolution node count (15,781,960 .. 20,711,023) lies strictly above
the 15M condition and below the 30M budget - the batch-38 EXHAUSTED
dispositions at 15M were budget artifacts, as the different-condition
route anticipated.  Honest first-observation note: all six resolve inside
the (15M, 30M] window, so the 15M condition could not have decided any
of them, and this Part retired the unknowns without a single new
exhaustion.

Drive accounting: per-pass node sum 108,066,529; two-pass total 216,133,058
expansions; status.log exactly 8 lines (6 PASS + 2 WIN rows logged under
WIN-CONTINUE); zero MISMATCH, zero truncation events, zero runner
failures; every raw carries its terminal `# replay_done` line.

## Val-gate (before any target run): 8/8 PASS

The four published batch-38 val-gate molecules byte-cloned into
`val-gate/` were run first, two fresh runs each, and EVERY replay row
equaled its published baseline byte-for-byte except wall_s: the two
at-2M exhaustion molecules (nodes 2,000,000, result 0) and the two 15M
molecules resolving LOSS at 3,651,923 / 5,040,200 nodes.  Two of the
eight run files came out sha256-identical to the published baseline file
itself (matching wall_s by coincidence: 9 s and 9 s).  This environment
measured ~190-210K nodes/s foreground (single pass); the 30M worst-case
pass estimate ~157 s drove the split-call schedule (below).

## Honest drive design disclosure

The pinned runner semantics are unchanged: every pass runs the exact
published command
`node scripts/jsreplay.js --exact-replay=input/<k>.input.csv
--exact-replay-budget=30000000` fresh-cold, and the pinned runbatch30m.sh
per-key invocation re-verified both passes' `replay_done` completion and
performed the two-pass MISMATCH comparison itself, writing status.log.
The only deviation from a single whole-batch invocation is the scheduling
imposed by the 300-second tool cap: passes were issued in foreground
split calls (ai007's two passes in a 2-worker parallel call; the
remaining keys one pass per call), after measuring that a 30M-budget
pass worst case exceeds the cap at the observed throughput.  A pre-kit
timing smoke of the at-2M molecule (disclosed in the declaration write-up
window) ran to /tmp and was discarded - it produced no evidence and
touched no kit path.  No pass was ever re-run after carrying a
`replay_done` line; the truncation guard never fired.

## Provenance pins

* targets: `input/targets-30m.json` (sha256 1c27a238...) machine-extracted
  from the published batch-38 SSOT batch-keys-b38.json (29807104...,
  Part EF kit); the 6 input CSVs are byte-clones of the b38 kit inputs;
* engine: `scripts/jsreplay.js` byte-clone 84585617... (the Node replica
  of the C++ exact-replay path, source pin 9193f5b6... at 154f3b7a);
* runner: `scripts/runbatch30m.sh` (44674932...), disclosed fork of the
  pinned batch-38 runbatch.sh (f591f8c2...): BUDGET 15M -> 30M and
  WIN-HALT -> WIN-CONTINUE; guard/MISMATCH/fail/rc semantics identical;
* freshness: all six (lo,hi) pairs are absent from the canonical chain
  head `9c4dd94e...` (Part ER head, verified this same session) and from
  the quarantine registry `81d23160...`; b018 (the 7th class-30345
  unknown) stays excluded and untouched;
* the same-condition re-probe ban is untouched: no completed exhaustion
  row was ever re-probed at its own condition; the 15M EXHAUSTED
  dispositions remain a permanent historical record of the 15M condition.

All 38 published kit files are sha256-pinned in MANIFEST-sha256.txt.

## What this changes (and does not change)

Class 30345's 7 probe-level unknown members reduce to 5 resolvable
members + b018 by these honest labels - but NOTHING is consumed: the
class census, closure CSV, worklist and canonical chain head `9c4dd94e`
are untouched by this Part (no merge, no refresh, no adoption).  The
natural successors, each in its owner lane: the scrutiny C++ gate on the
2 WIN rows (ai007/ai040) and any EM-pattern loss-only adoption of the 4
LOSS rows.  nodes are bookkeeping; no coverage, secured-coverage or root
resolution claim is made anywhere in this Part.  The standard 11x11
empty board stays UNKNOWN.
