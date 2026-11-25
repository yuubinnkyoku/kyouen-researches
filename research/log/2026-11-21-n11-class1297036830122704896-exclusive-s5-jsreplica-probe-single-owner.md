# 2026-11-21 n11 third-cost class 1297036830122704896:0 exclusive single-live-parent S5 probe (JS replica): single-owner declaration

- Declaration time: 2026-11-21T16:05Z. HEAD at declaration: `29857713052cbafb10898f13fa38d939a4fc9182`. This declaration claims the following 39 S5 keys so that no other agent starts the same exact searches.
- Respected concurrent lanes (their scoped keys, caches, raws, manifest and analysis outputs are not modified by this lane):
  1. reply27 two-target S5 candidate probe lane (`research/log/2026-11-21-n11-reply27-s5-probe-js-replica-single-owner.md`, commit `4e944105`): claims the supply's ranked candidates with `live_parents >= 2`. **This lane never starts a key with two or more live candidate parents** (every claimed key is machine-verified `live_parents == 1` with the single live parent exactly `{1297036830122704896:0}`).
  2. focus-class exclusive lane (commit `aa33434c`): claims the 35 exclusive keys of `1188950301626859520:536870912`. **Machine-checked disjoint from this lane's 39 keys.**
  3. certificate-class exclusive probe lane (commit `9e4e6f4c`, the ccp lane Part B): claims 38 exclusive keys of `1297036692683752448:0`. **Machine-checked disjoint.**
  4. S4 corpus fresh-regeneration lane (commit `0dd5773e`): claims the 99 corpus keys of `1297036692683752448:0` plus two extra backward-only rows. **Machine-checked disjoint from this lane's set.**
  5. n11 S5 frontier census / union-audit lane (commits `e4aae3b4`..`b03edff`): read-only, closed; its published measurement outputs are reused as pinned inputs (class-closure priority experiment `94223661`).
- Coordination observation (recorded transparently, no judgment, decision left to those lanes' owners): lanes 3 and 4 both claim, under different base-selection rules (ccp: exclusive single-live-parent unknowns; sbd: all chain-absent children of the class = 99), 38 keys that appear in both enumerations (the certificate class's exclusive children). This lane's machine selection asserts disjointness from the union of both claims, so the potential double-claim cannot consume this lane's compute.

## Claimed scope

The 39 five-stone keys that, under the frozen 3,384-class geometry
(`research/experiments/n11-strategy-redesign-20261010/output/geometry.json.gz`, sha256 `146be80b5794462c2444e983fc4c4a6e76d3b464bfd5e86fac14509024100b54`)
and the reply27 probe-13 merged exact cache
(`research/experiments/n11-reply27-s5-jsreplica-probe-10376293541461626880-40960-20261121/output/merged-exact-s5-after-js-probe-13.cache`, sha256 `60e0dc3476920d4e99043dd4f132398ea72e4dfdcd9f3dbb8fc686ba65bc28c6`),
satisfy all of:

1. child of the third-cost candidate class `1297036830122704896:0` (the two-target-design README's 費用3位 class; coverage {47, 51, 100, 108}; status UNKNOWN, 7 LOSS / 100 UNKNOWN children under the base cache; 107 children total),
2. absent from the base merged cache and from the active quarantine registry (`results/n11-s5-evidence-quarantine.json`, sha256 `81d231604d3a095c115135e05ca393d6be83e1aadde4f614d3b5a9cc67d17fe9`),
3. live candidate parent set exactly `{1297036830122704896:0}` (exclusive single-live-parent keys; deg-1 supply),
4. disjoint from every concurrent-lane claim listed above (machine-checked in the selector whose published output is authoritative).

Fail-closed clause: the authoritative key set is the machine-regenerated 39-key list computed from the pinned inputs and published in `research/experiments/n11-class1297036830122704896-exclusive-s5-jsreplica-probe-20261121/output/exclusive-selection.json` (`exclusive_probe_order`); any discrepancy between this prose enumeration and that machine list aborts the probe part. Execution order within the list is ascending truncated-cost proxy (band 5,041,585 then 5,234,938 then 5,932,112), then key. A key concurrently published by another developer before its run starts is skipped and reused from main instead.

Enumerated keys (ascending proxy band, then key):

proxy band 5,041,585 (7 keys):
`1153062242230468608:68719476736`, `1297036830122835968:0`, `1297036830139482112:0`, `1297037929634332672:0`, `1297177567611060224:0`, `3602879839336398848:0`, `10412322888236404736:0`;

proxy band 5,234,938 (29 keys):
`1152921504607895552:553648640`, `1152930300699873280:536870944`, `1161928703861592064:536870944`, `1297036830122704896:8`, `1297036830122704896:16`, `1297036830122704896:128`, `1297036830122704896:16384`, `1297036830122704896:65536`, `1297036830122704896:67108864`, `1297036830122704897:0`, `1297036830122704900:0`, `1297036830122704928:0`, `1297036830122705152:0`, `1297036830122708992:0`, `1297036830122713088:0`, `1297036830122737664:0`, `1297036830122770432:0`, `1297036830256922624:0`, `1297036830391140352:0`, `1297036831196446720:0`, `1297037105000611840:0`, `1369094424160632832:0`, `1585267206274416640:0`, `1873497582426128384:0`, `5908722848550092800:0`, `10376294091217440768:8`, `10376294091217440768:131072`, `10376294091217440768:33554432`, `10376294091217440768:67108864`;

proxy band 5,932,112 (3 keys):
`1152921504606851072:536870945`, `1297036830122704896:16777216`, `10376294091217440768:268435456`.

## Pre-registered stopping rules (fail-closed)

1. Any child verdict WIN(1): the class `1297036830122704896:0` is WIN-eliminated for its coverage; this lane stops that key's further chain immediately, records the raw evidence, publishes the WIN witness with its independent-geometry verification, and stops starting further claimed keys this session. No cache increment containing that row is published without an explicit machine-verified witness publication; the WIN is a finding, not a class-closure or root claim.
2. Any child UNKNOWN at the 15,000,000 budget: the key is parked (raw rows recorded for both stages and both runs), no cache row is emitted for it, no S6/S7 work is started this session, and the lane continues with the next key.
3. Node-exact validation gate failure, determinism (twice-run) mismatch on any 15M stage, or an independent-geometry gate failure: the lane stops and reports; no verdict is used or published.
4. Publication-time conflict (WIN/LOSS value difference) between this lane's increments and the then-latest main merged exact S5 cache: fail closed, no increment is published; the conflict is reported. A same-value duplicate row is elided (the earlier publication is the canonical evidence).

## Execution medium and acceptance conditions

Same evidence class as the reply27, focus-class and certificate-class lanes (replica solver-trusted exact, node-exact against the published C++ raw rows; NOT terminal-only minimax):

1. Node.js replica `jsreplay.js` (sha256 `845856175d3c793a7eb4306f5902ecda3f1c046a8a53e8f34ed375e51febc3df`, byte-identical to the reply27 probe-13 publication, replica of `cpp/solvers/kyouen_dfpn_root.cpp` at `154f3b7a67`, source sha256 `9193f5b6065e0fbcad2ef7c65f386187701cafa1f5b718cc35a5cbb0d138f92e`). In-session validation gate re-run PASSED before this declaration (fresh, this host): all four published two-target raw rows reproduce with identical stones/legal/is_or/budget/result/nodes, only wall_s differs (at2m x2 -> UNKNOWN 2,000,000 nodes; 15M rows -> LOSS 3,651,923 and LOSS 5,040,200).
2. Probes run cold: fresh 2^22-entry PnTT per row (fresh Solver per row), one row at a time, deadline 0, publish=ALL, exact order=count; budget ladder 2,000,000 first, then 15,000,000 only on UNKNOWN. CPU use: one worker at a time (host has 2 cores).
3. Determinism: the 15M resolution run is executed twice (independent fresh solvers); identical (result, nodes) required.
4. Every new verdict is independently geometry-verified before publication with the repo-independent integer implementation (`n11-independent-exact-audit-20261010/scripts/independent.py`, sha256 `954d3a104c1723ebb15b8c9bae63a4494f07f9eb73446a6d067c4fd6a4ba189f`): 5 stones, D4-canonical, safe (no forbidden quadruple), derived legal count equals the supply ledger's legal, membership as a child of the frozen-3,384-class parents of the key, absence from the base merged cache and the quarantine registry; canonical-safe policy (`n11-frontier-selection-20261005/scripts/s5_evidence_policy.py`, sha256 `78655e94480920de48a6fe8792e02e611513ddee7f685b422bbb2b08af5c95e2`) must accept the key.
5. Published increment (expected one publication for the batch): per-key raw in/out rows for both stages of both runs (plus the four validation-gate raw rows), batch input CSVs, selection JSON (fail-closed gates), verification audit JSON (fail-closed gates over the whole batch), SHA-256 manifest, one merged cache file = then-latest main merged exact S5 chain cache + this lane's new sorted rows (base file byte-preserved; byte comparison plus fail-closed WIN/LOSS conflict and duplicate handling on the union). The cache line format `s5verdict,<lo>,<hi>,5,<verdict>,<nodes>` matches the existing caches. Regenerated class statistics for `1297036830122704896:0` under the merged cache (unknown count decrease only, no status change claim unless the full 107-child all-children-LOSS condition is machine-checked). Fetch-back byte verification after push. Latest main re-fetched before every push.
6. No S4 class status change beyond machine-checked recomputation; no third-move coverage claim beyond a machine-checked class closure; no `{60,27}`, multi-root, or empty-board claim.

## Non-goals

No two-live-parent keys (reply27's band), no focus-class keys, no certificate-class keys, no S6/S7 enumeration, no df-pn lane work, no sweep restarts, no adoption or rejection of the backward-only rows (evidence owners keep that decision), no modification of any other lane's files or caches, no branch/PR.

## Status guard

The standard 11x11 empty board, the two-stone root {60,27}, and its remaining third moves 100/108 remain UNKNOWN throughout. Nodes, solver counts, and proxy values are never read as verdicts. A batch of LOSS decrements does not close the class (the class reaches 46/107 with all 39 LOSS; 61 shared children remain) unless the class-wide all-children-LOSS condition is machine-checked against the full 107-child set.
