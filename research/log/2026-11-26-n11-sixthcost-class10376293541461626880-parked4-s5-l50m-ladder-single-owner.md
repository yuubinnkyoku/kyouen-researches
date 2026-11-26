# n11 sixth-cost class 10376293541461626880:65536 parked-4-keys S5 L50M ladder - single-owner declaration (2026-11-26)

Single-owner lane. Scope: the four exclusive single-live-parent keys that the
fifth-resumption batch parked at UNKNOWN@15M (parent experiment
`research/experiments/n11-sixthcost-class-s5-exclusive-probe-10376293541461626880-20261121/`,
fifth-resumption declaration
`research/log/2026-11-26-n11-sixthcost-class10376293541461626880-exclusive-s5-probe-resume-k09-k43-single-owner-note.md`,
commit `cb0736ef`):

- k13 `1152921573327376384:536870912` (legal 95; machine-order position 13; published
  15M pair both result 0 / nodes 15,000,000, walls 81/81 s; checkpoint `2af0d7f2`)
- k19 `10376293541461626880:65664` (legal 95; position 19; published 15M pair both
  result 0 / nodes 15,000,000, walls 81/83 s; checkpoint `e0be4063`)
- k20 `10376293541461626880:33619968` (legal 95; position 20; published 15M pair both
  result 0 / nodes 15,000,000, walls 80/80 s; checkpoint `5ba9b673`)
- k33 `12682136550675320832:65536` (legal 91; position 33; published 15M pair both
  result 0 / nodes 15,000,000, walls 78/78 s; checkpoint `948f1f1c`)

These four keys are minimal blockers for any future attempt to close the sixth-cost
class `10376293541461626880:65536` (coverage {80, 84, 100, 108}): on the canonical
chain head of record `6e49dd84` (merged-exact-s5-chain-plus-emloss21-20261126.cache,
6,792 rows) the class's 108 S5 children stand at 0 WIN / 8 LOSS / 100 UNKNOWN
(machine-recomputed on the frozen 3,384-class geometry this session from the published
cache and geometry files; the parent batch's unconsumed raw verdicts are not in the
cache and are not consumed by this lane). 58 shared unknown children remain outside
this lane's declaration in any case.

## Ladder

Budget raise 15,000,000 -> 50,000,000 on the identical exact-replay protocol (third-cost
parked2 L50M ladder precedent
`research/experiments/n11-class1297036830122704896-parked2-s5-l50m-ladder-20261121/`):
Node replica `jsreplay.js` (sha256
`845856175d3c793a7eb4306f5902ecda3f1c046a8a53e8f34ed375e51febc3df`, byte-identical to
every published pin of this engine, re-verified this session), exact replay mode
(order=count-asc, share_tt=0, fresh 2^22-entry PnTT per row, cold per-row solver),
budget 50,000,000, run TWICE per key with independent fresh solvers; identical
(result, nodes) required. Semantics unchanged: 0 UNKNOWN (budget exhausted), 1 WIN,
2 LOSS (fixed first player). One budget-margin re-proof at 32,000,000 per resolved key
(different budget, same deterministic search: for a resolved key any budget >= the
proof-completion node count must return the exact same (result, nodes)).

- A WIN (result 1) at any key stops further claimed-key starts in this lane at once
  (stopping rule 1, identical to the parent batch and the L50M precedent); no cache
  row is emitted before scrutiny.
- A key that still exhausts 50M nodes is parked again (UNKNOWN@50M, no cache row).
- NO merged cache increment is published by this session under ANY outcome: the
  sixth-cost parent batch is mid-flight (its fifth resumption is running k38..k43 as
  this note is declared; HEAD immediately before this push `a8c830ec`, k42 checkpoint,
  2026-11-26T07:37:39Z) and its consumption gate reserves any increment for the full
  batch audit under the WIN/LOSS conflict policy; this lane records raw evidence and
  a fail-closed machine audit only.

## Fresh-session gates before any ladder row is trusted

1. Validation gate: all four published two-target raw rows reproduce node-exact -
   DONE on this host BEFORE this note was pushed: (at2m x2: result 0 / nodes
   2,000,000 / legal 98, 99; 15M rows: result 2 / nodes 3,651,923 and 5,040,200 /
   legal 98, 99); this host's wall_s 9/9/17/25 s (published prior hosts 9/9/18/25,
   9/9/17/24, 9/9/17/25).
2. Baseline parked reproduction: one fresh 15M run per key must reproduce the parent
   probe's published parked baseline exactly (result 0, nodes 15,000,000) before that
   key's 50M ladder runs.

## Claim hygiene (machine-checked on latest main; snapshot fetched via codeload
tarball at HEAD `238fa09c`, 2026-11-26T07:26:42Z)

- All four keys are members of the published machine selection
  `n11-sixthcost-exclusive-selection-v1` (selection JSON sha256 `d5e9b059...`
  re-verified byte-identical this session; positions 13/19/20/33 of the authoritative
  `exclusive_probe_order`; proxy band 5,234,938) and exclusive single-live-parent
  children of the declared class per the parent probe's 229-fail-closed-gate selector
  (re-executed today on the fifth-resumption host with byte-identical selection JSON
  and 43/43 batch inputs, as recorded in that resumption's declaration).
- All four exact (key_lo, key_hi) pairs are ABSENT from the chain head of record
  `6e49dd84` (machine scan over the 6,792 published rows; the cache's row with
  key_lo `10376293541461626880` and key_hi `131072` is a different position) and
  from the S5 quarantine registry (`results/n11-s5-evidence-quarantine.json`, 2
  active entries, neither touching these keys).
- Territory-disjoint from the concurrently running fifth-resumption session (its
  claimed keys are k09..k43 of the same machine list; the four parked keys were
  completed by that session as PARKED rows and are outside its remaining claimed-key
  starts; its raws and status.log live in the parent experiment dir, which this lane
  never modifies), and from every other concurrent lane's machine claim sets (the
  parent selector's disjointness gates; this lane claims no new key outside the four
  parked keys).
- Repo probe (run this session before this push): no parked-4 / sixth-cost parked
  escalation lane, experiment directory, or declaration exists on main before this
  note (search probes "parked4", "L50M" within sixth-cost territory: 0 hits; the only
  L50M lanes precede this one as the third-cost parked2 precedent).

## Compute discipline

At most 2 concurrent worker processes on this 2-core host; the ladder itself runs
serially (one jsreplay process per run); no other long-running loads launched by this
lane; failures and timeouts recorded as experimental facts.

## Acceptance conditions

1. Validation gate 4/4 node-exact in this session (done and recorded above).
2. Baseline parked reproduction 4/4 (per key, result 0, nodes exactly 15,000,000).
3. Ladder determinism: both 50M runs of each key identical (result, nodes); a
   resolved key additionally margin-proven at 32,000,000.
4. Machine audit: a fail-closed audit script re-derives every claim from the
   published raws and the pinned corpora (jsreplay sha, head-of-record cache sha,
   selection JSON sha, quarantine sha, frozen geometry sha, independent.py sha,
   canonical-safe policy sha), regenerating the audit JSON byte-identically on two
   audit runs; a tamper battery fails closed.
5. NO cache file published this session; every verdict stays unconsumed; any class
   recomputation is recorded as NOT-ADOPTED only; the class status continues to be
   decided by the canonical chain, not by this lane.

## Mandatory scrutiny before any consumption (handed to scrutiny owners)

Second-implementation re-verification with the pinned C++
`cpp/solvers/kyouen_dfpn_root.cpp` (source sha256
`9193f5b6065e0fbcad2ef7c65f386187701cafa1f5b718cc35a5cbb0d138f92e`) for every key
resolved here (target rows identical to the batch inputs, expected (result, nodes)
recorded in this lane's audit JSON); no C++ toolchain exists in this sandbox
(re-verified this session: no gcc/g++/clang/zig/cc on PATH), so the step is
delegated and recorded. Any later C++ disagreement fails closed in favor of
discarding the row.

## Non-goals

No class-closure claim, no two-stone-root or empty-board claim, no adoption or
rejection of any verdict, no S6/S7 enumeration, no modification of any other lane's
files or claims, no branch/PR, no K item (verdict-unconsumed evidence batch per
precedent).

## Status guard

The standard 11x11 empty board remains UNKNOWN. The two-stone root {60,27} and its
remaining third moves 100/108 remain UNKNOWN. Nodes, solver counts, budgets, and
proxy values are never verdicts. A LOSS at 50M is evidence for one child only and
does not close the class.
