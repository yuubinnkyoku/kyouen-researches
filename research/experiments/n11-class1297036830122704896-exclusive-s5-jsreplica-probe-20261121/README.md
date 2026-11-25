# n11 third-cost class 1297036830122704896:0 exclusive S5 probe (JS replica) — 2026-11-21

Single-owner lane declared in `research/log/2026-11-21-n11-class1297036830122704896-exclusive-s5-jsreplica-probe-single-owner.md` (commit `5ec015a033aa6499a9d77bfe53258d3a4cc60b09`, declared at HEAD `29857713`): 39 exclusive single-live-parent keys of the third-cost class `1297036830122704896:0` (coverage {47,51,100,108}, 100 unknown children at claim time, 39 exclusive unclaimed keys, lowest average truncated-cost proxy among then-unclaimed classes). The 39-key set is machine-verified disjoint from every concurrent fixed claim (focus-class 35 keys `aa33434c`, certificate-class Part B 38 keys `9e4e6f4c`, sbd corpus 99+2 keys `0dd5773e`, fourth-cost wave-2 41 keys `1f94f501`) and from the S5 quarantine registry.

## What this is

Evidence increment toward the weak solution of the standard 11x11 empty board: exact S5 verdicts for the claimed 39 exclusive children, probed so that a later LOSS closure of the parent class would sit on independently verifiable raw rows. This is NOT a class-closure, root, or empty-board claim.

## Method

- Node.js replica `jsreplay.js` (sha256 `845856175d3c793a7eb4306f5902ecda3f1c046a8a53e8f34ed375e51febc3df`, byte-identical to the reply27 probe-13 publication; replica of `cpp/solvers/kyouen_dfpn_root.cpp` at `154f3b7a67`, source sha256 `9193f5b6065e0fbcad2ef7c65f386187701cafa1f5b718cc35a5cbb0d138f92e`), exact replay mode: 0 UNKNOWN (budget exhausted) / 1 WIN / 2 LOSS, exact order=count, deadline 0, publish=ALL, fresh 2^22-entry PnTT per row, cold per-row solver, at most 2 worker processes on a 2-core host.
- Validation gate re-run fresh this session: all four published two-target raw rows reproduce with identical stones/legal/is_or/budget/result/nodes (only wall_s may differ).
- Budget ladder per key: 2,000,000 first; only on UNKNOWN, 15,000,000, run twice (independent fresh solvers); identical (result, nodes) required. 2 keys resolved at the 2M stage; 35 at the 15M stage; 2 parked; see `output/probe-audit.json` per_key stages.
- Stopping rules as declared: no WIN occurred (0 of 39); parked keys emit no cache row.

## Results (all machine-checked in `output/probe-audit.json`, fail-closed audit, ALL 641 GATES PASS)

- 37 LOSS / 2 UNKNOWN@15M parked (`1297036830122704896:67108864`, `10376294091217440768:33554432`) / 0 WIN of the 39 claimed keys.
- Merged cache increment `output/merged-exact-s5-after-class-excl-1.cache`: base = the then-latest main chain cache `research/experiments/n11-reply27-s5-jsreplica-probe-10376293541461626880-40960-20261121/output/merged-exact-s5-after-js-probe-13.cache` (sha256 `60e0dc3476920d4e99043dd4f132398ea72e4dfdcd9f3dbb8fc686ba65bc28c6`), base rows byte-preserved verbatim (original nodes fields included), + exactly 37 new sorted rows, no WIN/LOSS conflict, no duplicates. sha256 `bb4495e0586404876db05856c5b8573c62361dadd826b6f68f6f8cae611190b0`.
- Class recomputation on the frozen 3,384-class geometry: `1297036830122704896:0` goes 7 -> 44 LOSS, 100 -> 63 unknown, still UNKNOWN (not closed; 63 children remain unproven). Global status_changes = [] (no class opens or closes); candidate classes touching remaining third moves are unchanged; secured coverage is unchanged; the two-stone root {60,27} third-move picture {100, 108} is unchanged.
- Determinism: the audit and the merged cache regenerate byte-identically on re-run and in a fresh published-layout clone simulation (kit and repo layouts both exercised via `scripts/pub_paths.py`).

## Reproduction (from a repo clone)

```
python3 research/experiments/n11-class1297036830122704896-exclusive-s5-jsreplica-probe-20261121/scripts/exclusive_select.py
# byte-identical output/exclusive-selection.json
node research/experiments/n11-reply27-s5-jsreplica-probe-10376293541461626880-40960-20261121/scripts/jsreplay.js \
  --exact-replay=research/experiments/n11-class1297036830122704896-exclusive-s5-jsreplica-probe-20261121/input/batch-s5-<lo>-<hi>.input.csv \
  --exact-replay-budget=<2000000|15000000>
# raw rows recorded under output/raw/ (two runs per resolved stage)
python3 research/experiments/n11-class1297036830122704896-exclusive-s5-jsreplica-probe-20261121/scripts/audit_class_excl.py
# expected: ALL 641 GATES PASS; byte-identical probe-audit.json and merged cache
```

`scripts/audit_class_excl.py` re-derives everything from the published raw rows, the pinned inputs (geometry sha `146be80b...100b54`, base cache sha `60e0dc34...bc28c6`, supply sha `31f0d29b...ea954`, quarantine sha `81d23160...`, independent.py sha `954d3a10...`, s5_evidence_policy.py sha `78655e94...`), and the frozen geometry; it fails closed on any gate failure and writes no OK audit.

## Status guard

The standard 11x11 empty board remains UNKNOWN. The two-stone root {60,27} and both remaining third moves 100/108 remain UNKNOWN. Nodes, solver counts, and proxy values are never verdicts. A batch of LOSS decrements does not close the class: `1297036830122704896:0` is not closed and remains UNKNOWN with 63 unproven children.

## Non-goals

No S6/S7 enumeration, no df-pn lane work, no modification of any other lane's files or claims, no adoption or rejection of backward-only rows, no class closure claim for this class even though 37 keys resolved LOSS (2 parked, and 61 shared children were never claimed), no branch/PR, no K item (addressable cache-increment verdicts follow the reply27/focus/wave-2 lane precedent).
