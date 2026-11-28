# 2026-11-28 n11 fourteenth ladder-top selection

Completion log of the selection declared in
`2026-11-28-n11-fourteenth-ladder-top-selection-declaration.md`
(declaration commit `235b7056`, single owner, publish-then-execute).
Kit:
`research/experiments/n11-fourteenth-ladder-top-selection-20261128/`
(13 files, fetch-back 13/13 byte-identical vs local at kit commit
`a85f9c20`).

## Selected (closure-ladder rank 1 under the head d772f73c)

- class 5804 `6053400849139367936:0`, exactly **4 remaining
  unknown S5 keys** (the cheapest closure-ladder class; resolving all
  four completes the class, a candidate free_now flip, Board-verified
  at adoption time)
- k01 `6053401124017274880:0` (s5_index 198576, legal 86)
- k02 `6053682324116078592:0` (s5_index 207094, legal 82)
- k03 `6052837899185946628:128` (s5_index 212115, legal 87)
- k04 `6053400849139367936:128` (s5_index 212536, legal 92)
- head basis: merged-exact-s5-chain-plus-thirteenth-k01k02
  (`d772f73c...`, 6,896 rows WIN 214 / LOSS 6,682)
- ladder basis: the published thirteenth k01k02 adoption reaudit
  closure ladder (`be8bcff1...`, 799 rows); all 799 rows'
  `unknown_now` recomputed from graph `54f9c364...` + head + update8
  receipts `b658290a...`: 799/799 exact match
- top-5 gated exactly as pre-registered: 5804 (4) / 20421 (5) /
  34269 (11) / 12264 (33) / 5343 (46); scanned ranks 1-12 all fully
  available (no blocked keys)
- selector `select_fourteenth_ladder_top.py` sha256 `eb776f38...`, a
  structural adaptation of the thirteenth selection instrument
  `e2986020...` (head/ladder pins, pre-registered top-5 + selection
  gates, claim machinery extended with the adopted thirteenth_2,
  dual-implementation legal derivation kept); 43 fail-closed gates
  PASS; 3 cold runs byte-identical (run json sha256 `40d50b7d...`)
- all four keys' legal move counts derived independently (repo Board
  vs fresh integer 4x4-determinant concyclicity): 86/86, 82/82, 87/87,
  92/92 agreement; no key is in the probe-13 supply (proxy null)
- claim status: all four keys UNCLAIMED vs focus_35 / cert_38 /
  third_39 / fourth_41 / fifth_44 / sixth_43 / seventh_42 / eighth_43 /
  ninth_45 / tenth_44 / eleventh_46 / twelfth_51 / sbd_101 / parked_6 /
  the adopted ultra-cheap 4 / the adopted thirteenth 2; fresh vs head;
  quarantine absent
- tamper battery 5/5 fail-closed (T1 closure rank-1 unknown_now flip
  w/ pin patched -> P2 recomputation + top-5; T2 head row deletion w/
  pin patched -> P1 head-shape; T3 claim duplicate w/ pin patched ->
  P3 claim-sizes; T4 graph s4_cost UNKNOWN-child removal w/ pin
  patched -> P2 + P4; T5 update8 receipt deletion w/ pin patched ->
  P1 + P2); clean control re-PASS byte-identical.  Disclosure: a
  first T4 attempt removing a KNOWN child of class 5804 legitimately
  passed (rc=0) - the unknown-count recomputation is invariant to
  known-child edits - recorded as a calibration fact and replaced by
  the UNKNOWN-child removal.

## Deviation from the pre-registered expectation

None. All pre-registered expectations (799/799 recomputation, top-5,
selection class 5804, the four keys, s5 indices, dual-legal counts)
matched the selector's machine output exactly; the pre-pass that
recorded them (3 cold runs byte-identical, selection gates
neutralised) is disclosed in the declaration.

## Next work

- A separate single-owner escalation declaration for k01-k04 (cold
  2M pair sweep, then 15M escalation; WIN-stop rule; any WIN needs
  the C++-gate + third-implementation pillars before adoption), then
  the flip-census/reaudit follow-up.

## Guards

Selection and scheduling only: NO verdict is claimed or implied. The
standard 11x11 empty board: UNKNOWN. All 19 central-reply roots:
UNKNOWN. Two-stone root {60,27}: UNKNOWN. Third-move pair {100,108}:
UNKNOWN. Nodes, proxy and legal counts are bookkeeping, never
verdicts. (kit commit `a85f9c20`, log commit below)
