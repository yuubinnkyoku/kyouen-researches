# n11 sixth-cost WIN row third-implementation verdict re-verification: single-owner note (2026-11-21)

Declared: 2026-11-21T20:45Z (lane: the n11 long-term lane that published the sixth-cost
exclusive probe batch `30e694a6`/`1b262355`/`e0a30fab`/`f348343e` and the third-cost
class probe/L50M ladder). HEAD at the moment of this note's composition: `f44ec967`
(latest observed main; re-fetched immediately before push).

## What this lane will do

Re-verify the published, still-unconsumed replica verdict rows of this lane's own
claimed keys with a third implementation written from the game rules and a different
software structure (own BigInt geometry, own canonicalization, own memo design, own
move ordering; a plain deterministic AND/OR minimax with complete-position memo, not
df-pn, not a line port of `jsreplay.js`):

1. Validation pair (published two-target design rows, LOSS at 15M):
   `1152921504606851072:536870946` (legal 98), `1188950301626860544:536870912`
   (legal 99). Definitive re-runs must return LOSS(2).
2. Sixth-cost exclusive probe k01 `1297036692683751424:1114112` (legal 87),
   published LOSS(2) at 15M, nodes 10,369,650 x2 cold runs; and k02
   `1297036692683751424:68157440` (legal 87), published WIN(1) at 15M,
   nodes 7,717,432 x2 cold runs + voluntary third cold run. Verdict-level agreement
   (result only; node counts are implementation-specific and are expected to differ).
3. Third-cost parked pair (L50M ladder, published unconsumed): 
   `1297036830122704896:67108864` LOSS 22,388,336 /
   `10376294091217440768:33554432` WIN 31,799,580.
4. Stretch (only if wall-clock allows): the 37 third-cost exclusive LOSS rows of
   `merged-exact-s5-after-class-excl-1.cache` (sha256 `bb4495e0...`, 5,793 rows =
   probe-13 base `60e0dc34...` + 37 rows), verdict-level.

## What this lane will NOT do

- No cache increment, no chain merge, no verdict consumption, no class-status change,
  no coverage statement, no third-move statement. The 11x11 empty board, the two-stone
  root {60,27}, and third moves {100,108} remain UNKNOWN throughout.
- Nodes, budgets and proxy values are never read as verdicts.
- The pre-registered adoption gate for the WIN rows is unchanged: second-implementation
  verification of the raw rows by the pinned C++ solver
  (`cpp/solvers/kyouen_dfpn_root.cpp`, sha256 `9193f5b6...`) at 15M (k02 expected
  result 1, nodes 7,717,432; k01 expected result 2, nodes 10,369,650). That check
  remains delegated (no C++ toolchain in this sandbox; verified again this session;
  package installation is forbidden by the sandbox). This third-implementation
  verdict agreement is additional evidence only; it neither replaces the delegated
  C++ gate nor consumes the rows. Adoption/judgment stays with the scrutiny owner.

## Acceptance conditions (fail-closed)

- A1 The third implementation derives its own forbidden-quadruple geometry (BigInt
  determinant of [x^2+y^2, x, y, 1]) and its own legality; its forbidden-quadruple
  count must equal the replica's published table count, and its derived root legal
  counts must equal the published ledger legal values for every row it runs
  (98 / 99 / 87 / 87 and the parked pair's ledger values).
- A2 Every definitive re-run is executed twice on this host; (result) must be
  identical across its own pair (own determinism gate).
- A3 Any verdict DISagreement with a published row is a hard stop: no interpretation,
  no divergence analysis in the same batch; record the fact, publish the raw outputs,
  and hand the divergence investigation to the next run.
- A4 Negative control recorded once: for one agreed row, a deliberately misparsed
  input (stones/geometry off) must fail the input gates, not produce a verdict.
- A5 Budgets: per-row node cap 300,000,000 expansions and per-row wall cap 45
  minutes; exhausted rows are recorded as RUNLIMIT (not UNKNOWN-as-verdict) and are
  never reported as agreement. Serial execution on a 2-core host.

## Claims and disjointness

k01/k02 are exclusive keys already claimed by this lane's sixth-cost declaration; the
parked pair and the 37 rows belong to this lane's third-cost batch; the validation pair
is published artifact re-execution. No new keys are claimed. No other lane's claim set
is touched; no chain cache file is written. Concurrent lanes active at declaration time
(non-n11 topics per `research/log` since 19:42Z: seven-row q4 m69+, six-row q4 m47,
s12/s13 layer-3, four-row q6) are disjoint from these inputs.

## Environment facts (recorded for the next runs)

- Between 20:33Z and 20:36Z the repository stopped answering unauthenticated
  requests (raw / api / codeload / website all 404) while the GitHub app tools keep
  working; all unauthenticated curl routes were re-tested three times and failed
  consistently. Push/fetch-back must therefore go through the authenticated app tool
  path for the remainder of this session; this environment fact is re-verified at
  publication time and recorded in the session log.
- No C++ toolchain; package installation forbidden (re-verified today).
- 2 cores; Node.js v22.20.0; Python 3.12.14.
