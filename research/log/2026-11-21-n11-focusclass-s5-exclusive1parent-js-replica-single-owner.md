# 2026-11-21 n11 focus-class exclusive single-live-parent S5 probe (JS replica): single-owner declaration

- Declaration time: 2026-11-21T13:38Z (planned). HEAD at declaration: `81e6d802c48f23991038b4e4550ad00088da71de`.
- Respected concurrent lane: `2026-11-21-n11-reply27-s5-probe-js-replica-single-owner.md` (commit `4e944105`) claims the two-target supply's ranked candidates with `live_parents >= 2`. **This lane never starts a key with two or more live candidate parents.** The reply27 lane's caches, raws, manifest and analysis outputs are not modified.

## Claimed scope

The 35 five-stone keys that, under the frozen 3,384-class geometry
(`research/experiments/n11-strategy-redesign-20261010/output/geometry.json.gz`, sha256 `146be80b5794462c2444e983fc4c4a6e76d3b464bfd5e86fac14509024100b54`)
and the reply27 probe-12 merged exact cache
(`research/experiments/n11-reply27-s5-jsreplica-probe-10376293541461626880-34359742464-20261121/output/merged-exact-s5-after-js-probe-12.cache`, sha256 `0e4016aea0feea2c1eaa6dbc8ba56af1e54c1d02d8cba5338ecd8ddd0804f3a8`),
satisfy all of:

1. child of the focus class `1188950301626859520:536870912` (the two-target README's designated continuation class; coverage {55, 65, 100, 108}; status UNKNOWN, 16 LOSS / 93 UNKNOWN children under the base cache),
2. absent from the base merged cache and from the active quarantine registry (`results/n11-s5-evidence-quarantine.json`, sha256 `81d231604d3a095c115135e05ca393d6be83e1aadde4f614d3b5a9cc67d17fe9`),
3. live candidate parent set (candidate classes covering third moves 100/108 that remain UNKNOWN) exactly `{1188950301626859520:536870912}`.

Enumerated keys (ascending truncated-cost proxy, per the probe-12 supply `shared-s5-tasks.csv`, sha256 `fd51bc3c12b5220743bf1e26e96907fb9fb41aa518dc15b06082dc4434c71601`):

proxy band 5,234,938 (23 keys):
`1152921504606851072:536870922`, `1152921504606851072:536870978`, `1152921504606851072:536936450`, `1152921504606851072:537001986`, `1152921504606851072:570425346`, `1188950301626859520:536870913`, `1188950301626859520:536870976`, `1188950301626859520:537133056`, `1188950301626859520:603979776`, `1188950301626863616:536870912`, `1188950301626892288:536870912`, `1188950301643636736:536870912`, `1188950310216794112:536870912`, `1188950576504766464:536870912`, `1188951401138487296:536870912`, `1189091039115214848:536870912`, `1197957500881600512:536870912`, `1261007895664787456:536870912`, `1765411053930283008:536870912`, `5800636320054247424:536870912`, `10376293541461622816:68719476737`, `10412322338481635328:536870912`, `1152921504606851072:553648130`;

proxy band 5,932,112 (12 keys):
`1152921504606851072:603979778`, `1152921504741064705:68719476738`, `1152921504741068800:68719476738`, `1188950301626859520:537001984`, `1188950301626859520:805306368`, `1188950301626867712:536870912`, `1188950302700601344:536870912`, `1188950305921826816:536870912`, `1188959097719881728:536870912`, `1189020670371037184:536870912`, `1193453901254230016:536870912`, `10376293545756590112:68719476736`.

Execution order is ascending proxy, then key. A key concurrently published by another developer before its run starts is skipped and reused from main instead.

## Pre-registered stopping rules (fail-closed)

1. Any child verdict WIN(1): the focus class is eliminated (WIN) and this lane stops; the outcome is recorded with the raw evidence; no further focus-class child of this list is started.
2. Any child UNKNOWN at the 15M budget: the key is parked (recorded with raw rows), no cache row is emitted for it, no S6/S7 work is started this session, and the lane continues with the next key.
3. Node-exact validation gate failure, determinism (twice-run) mismatch on the 15M stage, or any independent-geometry gate failure: the lane stops and reports; no verdict is used or published.
4. Publication-time conflict (WIN/LOSS) between this lane's increments and the then-latest main merged cache: fail closed, no increment is published; the conflict is reported.

## Execution medium and acceptance conditions

Same evidence class as the reply27 lane (replica solver-trusted exact, node-exact against the published C++ raw rows; NOT terminal-only minimax):

1. Node.js replica of the pinned exact-replay path: `jsreplay.js` (sha256 `845856175d3c793a7eb4306f5902ecda3f1c046a8a53e8f34ed375e51febc3df`, byte-identical to the reply27 probe-11 published script, replica of `cpp/solvers/kyouen_dfpn_root.cpp` at `154f3b7a67`, file sha256 `9193f5b6065e0fbcad2ef7c65f386187701cafa1f5b718cc35a5cbb0d138f92e`). In-session validation gate re-run PASSED before this declaration: all four published two-target raw rows reproduce with identical stones/legal/is_or/budget/result/nodes (at2m 98/99 -> UNKNOWN 2,000,000; first-15m 98 -> LOSS 3,651,923; second-15m 99 -> LOSS 5,040,200); only wall_s differs.
2. Probes run cold: fresh 2^22-entry PnTT per row, one row at a time, deadline 0, publish=ALL, exact order=count; budget ladder 2,000,000 first, then 15,000,000 only on UNKNOWN. Rows may be batched inside one process for the completion-table build; each row still constructs a fresh Solver/TT, so each row is byte-equivalent to a standalone run (spot-checked against the standalone driver for at least one key).
3. Determinism: the 15M resolution run is executed twice (independent fresh solvers); identical (result, nodes) required.
4. Every new verdict is independently geometry-verified before publication with the repo-independent integer implementation (`n11-independent-exact-audit-20261010/scripts/independent.py`, sha256 `954d3a104c1723ebb15b8c9bae63a4494f07f9eb73446a6d067c4fd6a4ba189f`): 5 stones, D4-canonical, safe, legal count match, frozen-3,384-class parent membership; absence from the base merged cache and the quarantine registry; canonical-safe policy (`n11-frontier-selection-20261005/scripts/s5_evidence_policy.py`, sha256 `78655e94480920de48a6fe8792e02e611513ddee7f685b422bbb2b08af5c95e2`) must accept the key.
5. Published increment (expected one publication for the batch): per-key raw in/out rows for both stages of both runs, batch input CSVs, verification audit JSON (fail-closed gates), SHA-256 manifest, one merged cache file = then-latest main merged exact S5 cache + this lane's new sorted rows (base byte-preserved as a file; byte comparison plus fail-closed WIN/LOSS conflict check on the union), regenerated class-ledger analysis for the focus class and candidates. Fetch-back byte verification after push. The increment cache line format `s5verdict,<lo>,<hi>,5,<verdict>,<nodes>` matches the existing caches.
6. No S4 class status is changed by this lane's own claim other than what a machine-checked recomputation of the frozen geometry against the merged cache shows; no third-move coverage beyond a machine-checked class closure; no `{60,27}`, multi-root or empty-board claim.

## Non-goals

No two-live-parent keys (reply27's band), no S6/S7 enumeration, no df-pn lane work, no sweep restarts, no modification of any other lane's files or caches, no branch/PR.

## Status guard

The standard 11x11 empty board, the two-stone root {60,27}, and its remaining third moves 100/108 remain UNKNOWN throughout. Nodes, solver counts, and proxy values are never read as verdicts. A batch of LOSS decrements does not close the class unless the class-wide all-children-LOSS condition is machine-checked against the full 109-child set.
