# n11 sixth-cost class 10376293541461626880:65536 parked4-rest2 (k20/k33) S5 L50M ladder - single-owner declaration (2026-11-26)

Single-owner lane, publish-then-execute. Scope: the two exclusive
single-live-parent keys that the parked4 L50M ladder
(`research/experiments/n11-sixthcost-class10376293541461626880-parked4-s5-l50m-ladder-20261126/`,
single-owner declaration `research/log/2026-11-26-n11-sixthcost-class10376293541461626880-parked4-s5-l50m-ladder-single-owner.md`,
commit `9e042a5f`) left NEVER STARTED under its stopping rule 1 and that lane's
halt-audit records as still parked@15M, claimable by a later lane - this one:

- k20 `10376293541461626880:33619968` (legal 95; machine-order position 20 of the
  parent batch's published selection; published parent parked rows: 2M / 15M x2
  all result 0 / nodes = budget exactly)
- k33 `12682136550675320832:65536` (legal 91; position 33; published parent parked
  rows: 2M / 15M x2 all result 0 / nodes = budget exactly)

k13/k19 are NOT claimed here: they are the parked4 lane's WIN evidence with its
Part SM delegated pinned C++ gate (`n11-sixthcost-exclusive-cppgate-20261126/`),
still unconsumed, untouched by this lane.

Class state on the chain head of record at lane time, machine-recomputed this
session from the published files BEFORE drafting (frozen 3,384-class geometry +
`merged-exact-s5-chain-plus-sixthwin5-20261126.cache`, the Part EW head, sha256
`16a12390c0c3f046f0ae537b2a9940e15661263fc5034ce1b155c138bb9043cd`; 6,797 rows, WIN 197 / LOSS 6,600): the class's 108 S5 children stand at
5 WIN / 8 LOSS / 95 UNKNOWN, i.e. under the audit's local status rule the class
reads WIN, exactly the canonical win-hit flip unknown -> excluded_now of serving
class 3077 recorded by the Part EW completion log (NO class freed, NO coverage
claim, NO root verdict; 11x11 stays UNKNOWN). This lane claims no class status:
probing k20/k33 at a raised budget narrows the unknown-children set of the
class and reserves nothing else.

## Ladder

Budget raise 15,000,000 -> 50,000,000 on the identical exact-replay protocol:
Node replica `jsreplay.js` (sha256
`845856175d3c793a7eb4306f5902ecda3f1c046a8a53e8f34ed375e51febc3df`,
byte-identical to every published pin of this engine, re-verified this session),
exact replay mode (order=count-asc, share_tt=0, fresh 2^22-entry PnTT per row,
cold per-row solver), budget 50,000,000, run TWICE per key with independent
fresh solvers; identical (result, nodes) required. Semantics unchanged:
0 UNKNOWN (budget exhausted), 1 WIN, 2 LOSS (fixed first player). One
budget-margin re-proof at 32,000,000 per resolved key. A voluntary third cold
50,000,000 verification run for every WIN key (honestly labeled beyond the
declared pair, the k02/k03/k04/k05/k08 precedent).

- Both claimed keys' fresh 15M baseline runs START together immediately after
  this note is pushed, before any 50M result exists; therefore both are STARTED
  keys under stopping rule 1 and both complete their full pre-registered stages
  (base15m -> 50M pair -> 32M margin if resolved -> voluntary 50M run3-verify
  if WIN). A WIN (result 1) at any key still stops further claimed-key STARTS
  at once; this lane has no other claimed key.
- A key that still exhausts 50M nodes is parked again (UNKNOWN@50M, no cache row).
- NO merged cache increment is published by this lane under ANY outcome
  (declared no-consumption rule, identical to the parked4 lane): the sixth-cost
  parent batch's consumption gate reserves any increment for the full batch
  audit under the WIN/LOSS conflict policy; this lane records raw evidence and
  a fail-closed machine audit only.

## Fresh-session gates before any ladder row is trusted

1. Validation gate: all four published two-target raw rows must reproduce
   node-exact on this host BEFORE this note is pushed - DONE: (at2m x2:
   result 0 / nodes 2,000,000 / legal 98, 99; 15M rows: result 2 / nodes
   3,651,923 and 5,040,200 / legal 98, 99); this host's wall_s 20/21/40/49
   (published prior hosts 9/9/17/25 and others).
2. Baseline parked reproduction: one fresh 15M run per key must reproduce the
   parent probe's published parked baseline exactly (result 0, nodes
   15,000,000) before that key's 50M ladder runs.

## Claim hygiene (machine-checked this session on latest main, HEAD `9d9be4b6` 2026-11-26T11:52:47Z)

- Both keys are members of the published machine selection
  `n11-sixthcost-exclusive-selection-v1` (selection JSON sha256 `d5e9b059...`
  byte-identical re-download verified; positions 20/33 of the authoritative
  `exclusive_probe_order`) and exclusive single-live-parent S5 children of the
  declared class per the frozen geometry (child-of-class membership
   machine-verified; 5 stones; d4-canonical; canonical-safe under the pinned
  2policy; legal counts 95/91 agree with the reply27 supply ledger).
- Both exact (key_lo, key_hi) pairs are ABSENT from the chain head of record
  `16a12390` (machine scan over the published 6,797 rows) and from the S5
  quarantine registry (2 active entries, neither touching these keys).
- Counter-probe: no parked4rest2 / k20-k33 escalation lane, experiment
  directory, or declaration exists on main before this note (probes over the
  main tree and the 2026-11-26 log set at HEAD `9d9be4b6`: zero hits; the only
  sixth-cost L50M lane is the parked4 parent of this lane; no Part SN
  adoption exists).
- Territory-disjoint from the parked4 lane (its artifacts stay in its
  experiment dir; this lane never modifies them) and from every other
  concurrent lane's claims (this lane claims no key outside k20/k33).

## Machine audit (fail-closed, kit-pinned)

Scripts are structural clones of the parked4 kit (commit `73dfd4a7`):
`jsreplay.js` byte-identical (sha above), `pub_paths.py` identical except the
BASE pin retarget 6e49dd84 -> 16a12390 (6,797 rows) declared in its docstring,
`audit_parked4rest2_l50m.py` identical except: LANE_KEYS confined to k20/k33
(the MY_KEYS table and selection position gates stay, re-deriving parent-JSON
facts only), the BASE_CLASS_BEFORE constant recomputed mechanically (WIN-status
under the local rule = the Part EW win-hit/excluded_now state, 5/8/95,
annotated in-source), parked4rest2 schema strings, claimed-keys lists following
LANE_KEYS, and the second-implementation language updated to the Part SM
precedent. Full delta list disclosed in the audit script docstring; no gate
added, removed, or weakened vs the clone source. Audit outputs regenerate
byte-identically on two runs; a tamper battery must fail closed.

## Second-implementation scrutiny before any consumption

Identical contract to the parked4 lane: every resolved key requires
re-verification with the pinned C++ `cpp/solvers/kyouen_dfpn_root.cpp` (source
sha256 `9193f5b6065e0fbcad2ef7c65f386187701cafa1f5b718cc35a5cbb0d138f92e`)
before any row may be consumed. Unlike that lane's sandbox, this environment
CAN build that source (zig 0.13.0, Part SM precedent, binary sha non-pinned).
Per Part SM precedent the gate still runs as a publish-then-execute kit with
all expected quadruples pre-registered in this lane's audit JSON and fails
closed on any disagreement; whether it runs in this session or a successor is
an execution detail, never a consumption event. Consumption itself stays with
the parent batch's full audit, which this lane does not perform.

## Compute discipline

At most 2 concurrent jsreplay worker processes on this shared host; per-key
stages serial; no other long-running loads launched; failures and timeouts
recorded as experimental facts.

## Non-goals

No class-closure claim (the class already sits in the win-hit/excluded_now
state and this lane does not even record that as adopted), no two-stone-root
or empty-board claim, no adoption or rejection of any verdict, no S6/S7
enumeration, no modification of any other lane's files or claims, no branch/PR,
no K slot (verdict-unconsumed evidence kit per precedent).

## Status guard

The standard 11x11 empty board remains UNKNOWN. The two-stone root {60,27}
and its remaining third moves 100/108 remain UNKNOWN. Nodes, solver counts,
budgets, and proxy values are never verdicts. A LOSS or WIN at 50M is evidence
for one child only. This lane consumes nothing.
