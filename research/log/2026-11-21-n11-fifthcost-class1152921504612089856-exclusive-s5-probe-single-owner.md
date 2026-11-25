# 2026-11-21 n11 fifth-cost class 1152921504612089856:536870912 exclusive single-live-parent S5 probe (JS replica): single-owner declaration

- Declaration time: 2026-11-21T17:13Z. HEAD at declaration: `a336a5586e6acd84b8f7b813e1d88c1e732060c2`. This declaration claims the following 44 S5 keys so that no other agent starts the same exact searches.
- Lane: the 11x11 long-term (weak-solution) lane's next coordinator-picked exclusive class target, following the class-closure priority measurement (`research/experiments/n11-s5-class-closure-priority-20261121`) and the wave-2 claim allocation: the top-4 cheapest classes' exclusive keys are all claimed by concurrent lanes, and this class is the proxy_total rank-5 class with unclaimed exclusive keys (the bin-prior 0.972136 is the highest of the 62 live classes).
- Respected concurrent lanes (their scoped keys, caches, raws, manifest and analysis outputs are not modified by this lane):
  1. reply27 two-target S5 candidate probe lane (commit `4e944105`): claims the supply's ranked candidates with `live_parents >= 2`. **This lane never starts a key with two or more live candidate parents** (every claimed key is machine-verified `live_parents == 1` with the single live parent exactly `{1152921504612089856:536870912}`).
  2. focus-class exclusive lane (commit `aa33434c`): 35 exclusive keys of `1188950301626859520:536870912`. **Machine-checked disjoint from this lane's 44 keys.**
  3. certificate-class exclusive probe lane (commit `9e4e6f4c`, ccp Part B): 38 exclusive keys of `1297036692683752448:0`. **Machine-checked disjoint.**
  4. S4 corpus fresh-regeneration lane (commit `0dd5773e`): the 99 corpus keys of `1297036692683752448:0` plus two extra backward-only rows (keymap 101 targets). **Machine-checked disjoint.**
  5. third-cost class exclusive S5 probe lane (commit `5ec015a0`): 39 exclusive keys of `1297036830122704896:0`. **Machine-checked disjoint.**
  6. wave-2 coordination refresh / fourth-cost class exclusive S5 probe lane (commit `1f94f501`): 41 exclusive keys of `1297107061427929088:0`, plus its measurement/tooling parts A/B (its `wave2-priority.json` scenarios are static all-LOSS IF-scenarios; if they were computed before this declaration they will not include this lane's claim - a stale-scenario observation, not a conflict, and this lane does not modify them).
  7. n11 S5 frontier census / union-audit lane (commits `e4aae3b4`..`b03edff`): read-only, closed; its published measurement outputs are reused as pinned inputs.

## Claimed scope

The 44 five-stone keys that, under the frozen 3,384-class geometry (`research/experiments/n11-strategy-redesign-20261010/output/geometry.json.gz`, sha256 `146be80b5794462c2444e983fc4c4a6e76d3b464bfd5e86fac14509024100b54`) and the reply27 probe-13 merged exact cache (sha256 `60e0dc3476920d4e99043dd4f132398ea72e4dfdcd9f3dbb8fc686ba65bc28c6`), satisfy all of:

1. child of the fifth-cost candidate class `1152921504612089856:536870912` (coverage {88, 98, 100, 108}; class-closure-priority proxy_total rank 5 = 559,112,936; status UNKNOWN, 15 LOSS / 99 UNKNOWN children under the probe-13 cache; 114 children total),
2. absent from the base merged cache and from the active quarantine registry (`results/n11-s5-evidence-quarantine.json`, sha256 `81d231604d3a095c115135e05ca393d6be83e1aadde4f614d3b5a9cc67d17fe9`),
3. live candidate parent set exactly `{1152921504612089856:536870912}` (exclusive single-live-parent keys; deg-1 supply),
4. disjoint from every concurrent-lane claim listed above (machine-checked in the selector whose published output is authoritative; the claim sets are embedded in that selector with their provenance).

Fail-closed clause: the authoritative key set is the machine-regenerated 44-key list computed from the pinned inputs and published in `research/experiments/n11-fifthcost-class-s5-exclusive-probe-1152921504612089856-20261121/output/fifth-cost-exclusive-keys.json` (field `exclusive_probe_order`); any discrepancy between this prose enumeration and that machine list aborts the probe part. Execution order within the list is ascending truncated-cost proxy (band 5,069,670 then 5,234,938 then 5,932,112), then key. A key concurrently published by another developer before its run starts is skipped and reused from main instead.

Enumerated keys (ascending proxy band, then key):

proxy band 5,069,670 (1 keys):

`1152991873356267520:536870912`;

proxy band 5,234,938 (7 keys):

`1152921504612089856:536870976`, `1152921504612089856:536936448`, `1152921504612089888:536870912`, `1152921779489996800:536870912`, `1152956693273907200:536870912`, `10376293541461623812:68719476736`, `10376293541462671364:68719476736`;

proxy band 5,932,112 (36 keys):

`1152921504612089856:537001984`, `1152921504612089856:537133056`, `1152921504612089856:553648128`, `1152921504612089856:603979776`, `1152921504612089856:805306368`, `1152921504612093952:536870912`, `1152921504612098048:536870912`, `1152921504612122624:536870912`, `1152921504628867072:536870912`, `1152921504741064705:85899345920`, `1152921505685831680:536870912`, `1152921508901818368:536870920`, `1152921508901818368:536870976`, `1152921508901818368:536936448`, `1152921508901818368:537001984`, `1152921508901818368:553648128`, `1152921508901818368:570425344`, `1152921508901818368:603979776`, `1152921508901818368:69256347648`, `1152921508906012672:536870912`, `1152921513202024448:536870912`, `1152921517491752960:536870912`, `1152956688984178688:536870912`, `1152991877645996032:536870912`, `1153062242100445184:536870912`, `1188950305920782336:536870912`, `1224979098650017792:536870912`, `1224979102939746304:536870912`, `1297036696977674240:536870912`, `1441151885053530112:536870912`, `1729382256915513344:536870912`, `1729382261205241856:536870912`, `10376293541461622788:68719476737`, `10376293545756590084:68719476736`, `10376297939508133892:68719476736`, `10385300740716363780:68719476736`;

## Pre-registered stopping rules (fail-closed)

1. Any child verdict WIN(1): the class `1152921504612089856:536870912` is WIN-eliminated for its coverage; this lane stops that key's further chain immediately, records the raw evidence, publishes the WIN witness with its independent-geometry verification, and stops starting further claimed keys this session. No cache increment containing that row is published without an explicit machine-verified witness publication; the WIN is a finding, not a class-closure or root claim.
2. Any child UNKNOWN at the 15,000,000 budget: the key is parked (raw rows recorded for both stages and both runs), no cache row is emitted for it, no S6/S7 work is started this session, and the lane continues with the next key.
3. Node-exact validation gate failure, determinism (twice-run) mismatch on any 15M stage, or an independent-geometry gate failure: the lane stops and reports; no verdict is used or published.
4. Publication-time conflict (WIN/LOSS value difference) between this lane's increments and the then-latest main merged exact S5 cache: fail closed, no increment is published; the conflict is reported. A same-value duplicate row is elided (the earlier publication is the canonical evidence).

## Execution medium and acceptance conditions

Same evidence class as the reply27, focus-class, certificate-class, third-cost, fourth-cost and sbd lanes (replica solver-trusted exact, node-exact against the published C++ raw rows; NOT terminal-only minimax):

1. Node.js replica `jsreplay.js` (sha256 `845856175d3c793a7eb4306f5902ecda3f1c046a8a53e8f34ed375e51febc3df`, byte-identical to the reply27 probe-13 publication, replica of `cpp/solvers/kyouen_dfpn_root.cpp` at `154f3b7a67`, source sha256 `9193f5b6065e0fbcad2ef7c65f386187701cafa1f5b5c0d138f92e`). In-session validation gate re-run PASSED before this declaration (fresh, this host): all four published two-target raw rows reproduce with identical stones/legal/is_or/budget/result/nodes (at2m x2 -> UNKNOWN 2,000,000 nodes; 15M rows -> LOSS 3,651,923 and LOSS 5,040,200), only wall_s differs. Geometry pre-check over all 44 keys PASSED before this declaration (5 stones, D4-canonical, quadruple-free, canonical-safe, derived legal == supply ledger legal, live parent exactly the fifth class, absent from the base cache and the quarantine registry, disjoint from all six concurrent fixed claims).
2. Probes run cold: fresh 2^22-entry PnTT per row (fresh Solver per row), one row at a time, deadline 0, publish=ALL, exact order=count; budget ladder 2,000,000 first, then 15,000,000 only on UNKNOWN. CPU use: at most 2 worker processes (2-core host).
3. Determinism: every 15,000,000-budget resolution run is executed twice (independent fresh solvers); identical (result, nodes) required.
4. Every new verdict is independently geometry-verified before publication with the repo-independent integer implementation (`n11-independent-exact-audit-20261010/scripts/independent.py`, sha256 `954d3a104c1723ebb15b8c9bae63a4494f07f9eb73446a6d067c4fd6a4ba189f`): 5 stones, D4-canonical, safe, legal count match, membership as an exclusive child of the fifth-cost class in the frozen 3,384-class geometry, absence from the base merged cache and the quarantine registry; canonical-safe policy (`n11-frontier-selection-20261005/scripts/s5_evidence_policy.py`, sha256 `78655e94480920de48a6fe8792e02e611513ddee7f685b422bbb2b08af5c95e2`) must accept the key.
5. Published increment (expected per-session checkpoint publications plus a final batch publication): per-key raw in/out rows for both stages of both runs (plus the four validation-gate raw rows), batch input CSVs, selection JSON (fail-closed gates), verification audit JSON (fail-closed gates over the whole batch), SHA-256 manifest, one merged cache file = then-latest main merged exact S5 chain cache + this lane's new sorted rows (base byte-preserved; fail-closed WIN/LOSS conflict and duplicate handling on the union; removing this lane's rows must reproduce the base byte-exactly). The cache line format `s5verdict,<lo>,<hi>,5,<verdict>,<nodes>` matches the existing caches. Regenerated class statistics for `1152921504612089856:536870912` under the merged cache (unknown count decrease only, no status change claim unless the full 114-child all-children-LOSS condition is machine-checked against the full child set). Fetch-back byte verification after push. Latest main re-fetched before every push.
6. No S4 class status change beyond machine-checked recomputation; no third-move coverage claim beyond a machine-checked class closure; no `{60,27}`, multi-root, or empty-board claim. No K item is created for this batch (verdicts stay at solver-trusted cache increment level, following the reply27/focus/certificate/third-cost lane precedent).

## Non-goals

No two-live-parent keys (reply27's band), no focus/certificate/sbd/third-cost/fourth-cost keys, no S6/S7 enumeration, no df-pn lane work, no sweep restarts, no adoption or rejection of any backward-only row (evidence owners keep that decision), no modification of any other lane's files or caches, no branch/PR, no class closure claim for the fifth-cost class even if all 44 keys resolve LOSS (55 shared children remain unclaimed under this declaration).

## Status guard

The standard 11x11 empty board, the two-stone root {60,27}, and its remaining third moves 100/108 remain UNKNOWN throughout. Nodes, solver counts, and proxy values are never read as verdicts. A batch of LOSS decrements does not close the class (the class reaches 44/99 exclusive progress at best in this declaration, all-LOSS scenario) unless the class-wide all-children-LOSS condition is machine-checked against the full 114-child set, which this lane does not claim.
