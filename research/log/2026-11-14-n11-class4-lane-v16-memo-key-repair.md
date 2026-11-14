# 2026-11-14 n11 class4 lane: repair signed transposition keys before the next sweep

Audit base: `main` = `fc536bc2d7c4ed9d6892de007cf61e7fde39ced6`.

The current `AGENTS.md`, `research/knowledge/README.md`, K0023, K0783, the milestone-5 experiment README, and the current class2/class4 claims and raw batches were checked before editing.

## Structural defect

The v15 search runner stores its four occupancy words in `Uint32Array` keys (`mK0..mK3`), but the live `M0..M3` words are JavaScript bitwise signed 32-bit integers. The memo lookup compared them with strict equality without converting the live values to unsigned.

The active class4 S6 child `00000000020000003800000280000000` contains bit 31. Thus its low word is `-2147483648` as a signed JavaScript number but `2147483648` in the `Uint32Array`. The hash still matches, but the key comparison fails. Instrumenting the v15 depth-9 run (bit 15, cap 200,000) gave 118,602 memo lookups and **zero hits**, despite 89,682 memo insertions. The transposition table was effectively disabled for these roots.

A second, independent cache defect was present: `mNoWin` and `mNoLose` are initialized to sentinel 255, but the update conditions required a depth greater than the current value. Since search depths are at most 10, neither negative bound could ever be stored.

## Repair

A separate `class4_child1_runner_v16.ts` was added; the original v15 file is deliberately unchanged so that already-running sweeps remain reproducible.

- Compare stored unsigned keys with `M0>>>0` through `M3>>>0` in both `memoFind` and `memoEntry`.
- Treat 255 as an empty negative-bound sentinel when writing `mNoWin` and `mNoLose`.
- Update the v16 pilot control from the v15 count 5,949 to the repaired count 3,402.
- Add `class4_child1_runner_v16.test.ts` as a Node 22 command-line regression.

## Measured comparison

Same child, candidate, depth, ordering, and cap:

- S6 child: `00000000020000003800000280000000`
- seventh-stone bit: 15
- depth 8, close-first AND, cap 200,000
- v15: `loss=false`, 146,514 nodes, terminal range [13,15]
- v16: `loss=false`, 56,791 nodes, terminal range [13,15]

That is 89,723 fewer nodes (**61.24% reduction**, 2.58x fewer nodes) on this regression. The instrumented v16 run recorded 31,513 memo lookups, 10,853 hits, 20,467 insertions, 5,458 no-WIN writes, 8,864 no-LOSS writes, 2,793 no-WIN hits, and 4,419 no-LOSS hits. The pilot changed from 5,949 to 3,402 nodes while retaining `loss=false`.

A second regression exercises the sign bit in word M1 using the claimed class2 cost-62a child `00000000000000809102000001000000` plus bit 0 at depth 8: v15 reached the 200,000-node cap, while v16 completed in 121,837 nodes with `loss=false` and terminal range [13,15]. This confirms the unsigned comparison is needed in every 32-bit word, not only M0.

These are finite depth-8 implementation measurements, not a depth-10 game verdict or a proof of the full search. The V8 tool runtime executed the transformed runner in this turn; the Node 22 CLI test file is committed for direct reproduction, but was not run inside the container.

## Do not mix active v15 sweeps

- Class4 cost-86c is still in flight on v15. Its 67/86 published candidates are all REFUTED-D10, uncapped, with 223,650,541 nodes; the 67 bit indices are unique and match the published candidate list with 19 not yet present. All 11 pilot controls are loss=false at 5,949 nodes. These partial raw records must remain v15 data.
- The class2 cost-62a claim for S5 `00000000000000809102000000000000` also names v15 and the 5,949-node pilot. It is left untouched; do not mix v16 batches into that claim.
- The earlier best class2 S5 `00000000000000809082000000000000` is receipt-unclosable within the WIN7-D10 receipt framework: all 10 remaining S6 children were fully swept and sterile. This is not a LOSS proof. The next class2 target has 40 remaining S6 orbits / edge cost 2,850, with the cost-62 child claimed above.

Other copies with the same signed-key pattern exist in the older sweep engine, chunk prover, certificate extractors, and FBT-saturation audit runners. They were not silently rewritten here. Before using those copies for a new sweep or certificate extraction, audit and repair them as separate versioned changes.

## Status

No new WIN7/LOSS7 certificate or game verdict was produced by this repair. The class4 cost-86c sweep remains in flight. Standard 11x11 empty root, two-stone root `{49,60}`, S2 `{59,60}`, class 2, and class 4 remain **UNKNOWN**.
