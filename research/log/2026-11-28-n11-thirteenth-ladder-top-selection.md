# 2026-11-28 n11 thirteenth ladder-top selection

Completion log of the selection declared in
`2026-11-28-n11-thirteenth-ladder-top-selection-declaration.md`
(declaration commit `7583169d`, single owner, publish-then-execute).
Kit:
`research/experiments/n11-thirteenth-ladder-top-selection-20261128/`
(11 files, fetch-back 10/10 byte-identical vs MANIFEST).

## Selected (closure-ladder rank 1 under the head beecb024)

- class 16757 `1153204079095185408:65536`, exactly **2 remaining
  unknown S5 keys** (the cheapest closure-ladder class; resolving both
  completes the class, a candidate free_now flip, Board-verified at
  adoption time)
- k01 `1153204147814662144:65536` (s5_index 556117, legal 72)
- k02 `1152922672837951488:65792` (s5_index 558553, legal 72)
- head basis: merged-exact-s5-chain-plus-ultra-cheap-u04
  (`beecb024...`, 6,894 rows WIN 212 / LOSS 6,682)
- ladder basis: the published ultra-cheap u04 adoption reaudit
  closure ladder (`ef344748...`, 800 rows); all 800 rows'
  `unknown_now` recomputed from graph `54f9c364...` + head + update8
  receipts `b658290a...`: 800/800 exact match
- top-5 gated exactly as pre-registered: 16757 (2) / 5804 (4) /
  20421 (5) / 34269 (11) / 12264 (33); scanned ranks 1-12 all fully
  available (no blocked keys)
- selector `select_thirteenth_ladder_top.py` sha256 `e2986020...`, a
  structural adaptation of the ultra-cheap census instrument
  `c5e7b88e...` (head/ladder pins, pre-registered top-5 + selection
  gates, claim machinery, dual-implementation legal derivation
  added); 42 fail-closed gates PASS; 3 cold runs byte-identical
  (run json sha256 `fd9e21d7...`)
- both keys' legal move counts derived independently (repo Board vs
  fresh integer 4x4-determinant concyclicity): 72/72 agreement;
  neither key is in the probe-13 supply (proxy null)
- claim status: both keys UNCLAIMED vs focus_35 / cert_38 / third_39
  / fourth_41 / fifth_44 / sixth_43 / seventh_42 / eighth_43 /
  ninth_45 / tenth_44 / eleventh_46 / twelfth_51 (incl. the concurrent
  twelfth-cost takeover lane `768d2e5a`) / sbd_101 / parked_6 and the
  adopted ultra-cheap 4; fresh vs head; quarantine absent
- tamper battery 5/5 fail-closed (T1 closure rank-1 flip w/ pin
  patched -> P2 recomputation + top-5; T2 head row deletion ->
  P0 head-sha + P1 shape; T3 claim duplicate w/ pin patched ->
  P3 claim-sizes; T4 graph s4_cost edit w/ pin patched -> P2 + P4;
  T5 update8 receipt deletion -> P0 + P1 + P2); clean control re-PASS
  byte-identical

## Next work

- A separate single-owner escalation declaration for k01/k02 (cold
  2M pair sweep, then 15M escalation; WIN-stop rule; any WIN needs
  the C++-gate + third-implementation pillars before adoption), then
  the flip-census/reaudit follow-up.

## Guards

Selection and scheduling only: NO verdict is claimed or implied. The
standard 11x11 empty board: UNKNOWN. All 19 central-reply roots:
UNKNOWN. Two-stone root {60,27}: UNKNOWN. Third-move pair {100,108}:
UNKNOWN. Nodes, proxy and legal counts are bookkeeping, never
verdicts. (kit commit `fa4e6cb2`, log commit below)
