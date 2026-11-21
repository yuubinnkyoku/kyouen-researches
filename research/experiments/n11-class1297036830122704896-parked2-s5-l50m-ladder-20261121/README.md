# n11 third-cost class 1297036830122704896:0 parked-2-keys S5 L50M ladder - HALTED ON WIN (2026-11-21)

Single-owner lane declared in
`research/log/2026-11-21-n11-class1297036830122704896-parked2-s5-l50m-ladder-single-owner.md`
(commit `b1a3814445e9bf3a30566b08cc9f3a718570ee9f`, declared at HEAD `d23f57fa01ab1807f51dbe7296d6e500429e6139`).
Scope: the two exclusive single-live-parent keys that the completed third-cost exclusive S5 probe parked at
UNKNOWN@15M - the minimal blockers for any future attempt to close the class `1297036830122704896:0`
(44 LOSS / 63 unknown of 107 children at claim time; the remaining 61 unknown children are shared with
other live classes and out of this lane's scope).

## What this is

The budget ladder 15,000,000 -> 50,000,000 on the identical exact-replay protocol RESOLVED BOTH KEYS, and
one of the two resolved as **WIN**, halting the batch under stopping rule 1. Consequence, exactly as
declared in advance: this lane consumes NO verdict, publishes NO cache row for either key, makes NO
class/root/board claim, and hands the two raw rows to scrutiny owners for the mandatory
second-implementation re-verification. `output/halt-audit.json` is the machine record of the halted state
(51 pre-WIN gates PASS, gate list fail-closed); there is no probe-audit.json and no cache file because
the batch never reached consumption.

The standard 11x11 empty board remains UNKNOWN. A WIN raw for one S5 child is not a root claim and not a
class-closure claim; if adopted it would turn the class WIN, the opposite of the LOSS closure this ladder
was aimed at.

## Method (identical exact-replay protocol, budget raised)

- Node.js replica `jsreplay.js` (sha256 `845856175d3c793a7eb4306f5902ecda3f1c046a8a53e8f34ed375e51febc3df`,
  byte-identical to the reply27 probe-13 publication and the parent probe pins; replica of
  `cpp/solvers/kyouen_dfpn_root.cpp` at `154f3b7a67`, source sha256
  `9193f5b6065e0fbcad2ef7c65f386187701cafa1f5b718cc35a5cbb0d138f92e`), exact replay mode: order=count-asc,
  share_tt=0, fresh 2^22-entry PnTT per row, cold per-row solver, budget 50,000,000, run TWICE per key with
  independent fresh solvers, plus one budget-margin re-proof at 32,000,000 per key.
- Fresh-session gates before any ladder row was trusted: the four published two-target validation rows
  reproduce node-exact (val-at2m-first/second at 2M, val-first/second-15m at 15M), and both keys
  re-reproduce the parent probe's parked baseline at 15M (result UNKNOWN, nodes exactly 15,000,000).
- 2 worker processes max on a 2-core host; wall_s is environment-dependent and never a verdict.

## Results (machine-checked in output/halt-audit.json)

- `1297036830122704896:67108864` (stones (9,1),(4,3),(2,5),(5,5),(2,8); legal 91): **LOSS in 22,388,336
  nodes** - identical in both 50M runs and in the 32M margin re-proof. The 15M park is explained: the proof
  needs ~1.49x the 15M budget.
- `10376294091217440768:33554432` (stones (1,1),(6,3),(5,5),(8,5),(1,8); legal 94): **WIN in 31,799,580
  nodes** - identical in both 50M runs and in the 32M margin re-proof; the proof completes ~2.12x the 15M
  budget, which is why the parent probe parked it. This is the first WIN verdict recorded in the
  exclusive-probe lanes (reply27 13-probe, focus 35, certificate Part B 38, sbd 99+2, third-cost 39,
  fourth-cost 41 pass1 so far: all 0 WIN). The chain cache contains 158 historical WIN rows from earlier
  corpora, so result-1 semantics is an exercised verdict class; no published C++ validation row has
  result WIN, which is exactly why the second-implementation re-verification below is mandatory.
- Semantics: 1 = the fixed proposition "the player who moved FIRST on this line eventually wins" holds
  with a full df-pn proof; at 5 stones the node is an AND node, so WIN means the first player of this
  line wins against every second-player reply, not that the side to move wins.
- If-adopted scenario (recorded in `output/halt-audit.json`, NOT adopted, NOT judged by this lane):
  adopting both raw rows would flip TWO classes in the frozen 3,384-class geometry:
  `1297036830122704896:0` -> WIN (1 WIN + 45 LOSS + 61 unknown of 107; coverage {47,51,100,108} includes
  both remaining third moves 100/108 of the two-stone root {60,27}) and `1297036694830186496:131072` ->
  WIN (coverage {47,51,101,107}, does not touch 100/108). The root impact through the depth-2/depth-1
  chain is NOT computed by this lane and belongs to the K0414/K0416-lineage owners.
- Determinism: every stage ran with identical (result, nodes) across runs; the audit re-derives everything
  from the published raws and regenerates `halt-audit.json` byte-identically in kit and published layouts
  (both exercised; sha256 pinned in manifest-sha256.json).

## Mandatory scrutiny before any consumption (handed to scrutiny owners)

1. Second-implementation re-verification: compile the pinned C++ `cpp/solvers/kyouen_dfpn_root.cpp`
   (source sha256 `9193f5b6065e0fbcad2ef7c65f386187701cafa1f5b718cc35a5cbb0d138f92e`) and run the same
   `target,0,5,10376294091217440768,33554432,94,0,0,0,0,0` at budget 50,000,000; expect result 1,
   nodes 31,799,580. This lane's sandbox has no C++ compiler and package installation is forbidden by the
   sandbox policy (recorded as an environment fact), so the step could not be executed here. The replica
   is node-exact against all four published C++ raw rows, but none of them is a WIN row.
2. Game-theoretic consistency review against the 158 historical WIN rows in the chain cache and the
   class-vs-root backward chain (K0414/K0416 lineage owners).
3. Only after (1)+(2): emit the cache rows for BOTH keys (WIN row for `10376294091217440768:33554432`,
   LOSS row for `1297036830122704896:67108864`) through the chain merge policy with the WIN/LOSS conflict
   gate. Until then, both raw rows stay unconsumed.

## Tamper battery (fail-closed controls, run pre-publication)

- WIN-run1 result 1->2: `GATE FAIL ...determinism`, rc=1, no halt-audit written.
- Base chain cache byte tampered: `GATE FAIL base_chain_cache_sha`, rc=1.
- Baseline 15M nodes 15000000->14999999: `GATE FAIL ...base15m_parked_reproduced`, rc=1.
- Untouched control: 51 pre-WIN gates PASS, halt, byte-identical `halt-audit.json`.

## Reproduction (from a repo clone)

```
node research/experiments/n11-reply27-s5-jsreplica-probe-10376293541461626880-40960-20261121/scripts/jsreplay.js \
  --exact-replay=research/experiments/n11-class1297036830122704896-parked2-s5-l50m-ladder-20261121/input/batch-s5-<lo>-<hi>.input.csv \
  --exact-replay-budget=<15000000|32000000|50000000>
# validation rows: input/val-*.input.csv (budgets 2000000 and 15000000)
# raw rows recorded under output/raw/ (two 50M runs + one 32M margin run per key)
python3 research/experiments/n11-class1297036830122704896-parked2-s5-l50m-ladder-20261121/scripts/audit_parked2_l50m.py
# expected: "ALL 51 PRE-WIN GATES PASS -> HALTED ON WIN 10376294091217440768:33554432", rc=2,
# byte-identical output/halt-audit.json, and NO probe-audit.json / cache file
```

`scripts/audit_parked2_l50m.py` re-derives everything from the published raw rows, the pinned inputs
(geometry sha `146be80b...100b54`, chain cache sha `bb4495e0...19b90b`, parent probe audit sha
`950a716b...93fd2`, supply sha `31f0d29b...ea954`, quarantine sha `81d23160...`, independent.py sha
`954d3a10...89f`, s5_evidence_policy.py sha `78655e94...5c95e2`, jsreplay sha `84585617...3df`), and the
frozen 3,384-class geometry; it fails closed on any gate failure, and on the WIN branch exits rc=2
after writing the halt record, without writing any OK audit or cache file.

## Status guard

The standard 11x11 empty board remains UNKNOWN. The two-stone root {60,27} and both remaining third moves
100/108 remain UNKNOWN. This experiment claims no verdict-consuming result: the WIN raw is a
solver-trusted evidence row pending two-implementation scrutiny, and the LOSS raw is published alongside
it so the scrutiny owner can adopt both under one merge. Nodes, solver counts, budgets, and proxy values
are never verdicts. The class `1297036830122704896:0` is untouched by this lane: it stays UNKNOWN with
44 LOSS / 63 unknown until the rows are consumed by the scrutiny owners.

## Non-goals

No verdict consumption, no class/root/empty-board claim, no adoption or rejection of backward-only
reconciliation rows, no S6/S7 enumeration, no modification of any other lane's files or claims, no
branch/PR, no K item until the second-implementation verification exists.
