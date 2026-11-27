# 2026-11-27 n11 ninth-cost wave C stage-1/first-escalation scratch observations and execution-environment loss (honest record)

Host-local scratch record of the ninth-cost lane (kit published at 4e8d2c7a,
fetch-back verified). NOT an official ladder publication: all raws below were
lost when the upgraded execution environment reset mid-session, before any
wave C publication. The runs are deterministic (pinned jsreplay 84585617,
published single-row inputs), so the official wave C re-execution on a fresh
host must reproduce them node-exactly; per policy these values are disclosed
observations only and no row is consumed by them.

## Stage-1 2M cold-pair sweep (all 45 keys, executed, raws lost)

All 45 keys k01..k45: result 0 / nodes 2,000,000 on both passes of the cold
pair (90 replay rows). All pairs node-identical (the only a/b byte differences
were wall_s: k04/k09/k15/k16/k19/k27/k32). Every key therefore eligible for
15M escalation. Total 90 x 2,000,000 = 180,000,000 nodes.

## 15M escalation, k01..k10 (executed, raws lost; k11 never started)

- k01 (1297036692683751424:134283264): **LOSS(2), nodes 2,163,556**, cold
  pair node-identical.
- k02 (1297036692683751424:201326592): UNKNOWN, nodes 15,000,000 x2 (L50M
  escalation candidate).
- k03 (1297036761403228160:134217728): **LOSS(2), nodes 7,753,840**, pair
  node-identical.
- k04 (1152921504607903744:536903680): UNKNOWN, 15,000,000 x2.
- k05 (1152921504624672768:536903680): **LOSS(2), nodes 8,687,533**, pair
  node-identical.
- k06 (1152923703764321280:68719476736): **LOSS(2), nodes 8,130,387**, pair
  node-identical.
- k07 (1152923703765368832:68719476736): UNKNOWN, 15,000,000 x2.
- k08 (1152921513197830144:536903680 is k28; k08 = 1152923703764321280-family
  band member; exact key per published k08.input.csv): **LOSS(2), nodes
  3,306,768**, pair node-identical.
- k09: **LOSS(2), nodes 4,711,230**, pair node-identical.
- k10: **LOSS(2), nodes 5,542,083**, pair node-identical.
- k11..k45: never started (WIN stopping rule never fired; no WIN observed).

Scratch tally (unofficial): 7 LOSS-resolved candidates (k01, k03, k05, k06,
k08, k09, k10), 3 parked candidates (k02, k04, k07), 35 unprobed.

## What was lost / what survives

Lost: /home/user/work/eighthcensus (ninth kit mirror incl. all ladder raws),
/home/user/repo (pinned dependency tree, all byte-verified against published
pins this session). Survives: the complete published kit (65 files, commit
4e8d2c7a, fetch-back 64/64 byte-identical) including the selector, the
independent cross-check, the keys JSON and all 45 inputs; the wave A
declaration log (ac4d7432). The dependency tree is fully reconstructible from
the published pins (every pin path + sha256 is recorded in the selector and
cross-check sources).

## Next-session resume

1. Re-fetch latest main; rebuild the dependency tree from the published pins
   (all paths + shas are inside select_ninth_exclusive.py).
2. Re-run the official wave C: stage-1 2M cold pair for all 45 keys, then
   15M escalation from k01 in ascending order, publishing the raws and a
   batch-summary checkpoint (schema n11-ninthcost-batch-checkpoint-summary-v1)
   before any further lane action. Expect node-exact reproduction of the
   disclosed observations above; any deviation is a fail-closed event to be
   reported, not merged.
3. The k08 band note above is corrected by the published k08.input.csv, which
   is authoritative (prose is secondary).

## Guards

Scratch observations only; no verdict is consumed or claimed. All rows are
single-implementation (Node.js replica). The standard 11x11 empty board:
UNKNOWN. All 19 central-reply roots: UNKNOWN. Two-stone root {60,27}:
UNKNOWN. Third-move pair {100,108}: UNKNOWN. Every closure class: UNKNOWN
unless a published Part says otherwise. Nodes are never evidence of WIN or
LOSS beyond the fail-closed replay semantics.
