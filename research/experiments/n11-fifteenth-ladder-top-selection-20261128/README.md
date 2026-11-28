# n11 fifteenth ladder-top selection 2026-11-28

Kit of the fifteenth closure-ladder top-candidate selection declared
single-owner publish-then-execute (declaration commit `8893fb2d`,
`research/log/2026-11-28-n11-fifteenth-ladder-top-selection-declaration.md`),
under the canonical head of record
`merged-exact-s5-chain-plus-fourteenth-k01-20261128.cache`
(sha256 `a66f636e...`, 6,897 rows WIN 215 / LOSS 6,682) and the
published fourteenth k01 adoption reaudit closure ladder
(`8fe6125f...`, 799 rows).

## Selected (closure-ladder rank 1 under the head a66f636e)

- class 5804 `6053400849139367936:0`, exactly **3 remaining
  unknown S5 keys** (the adopted fourteenth k01 WIN row resolved one
  of the four; resolving all three completes the class, a candidate
  free_now flip, Board-verified at adoption time)
- k01 `6053682324116078592:0` (s5_index 207094, legal 82)
- k02 `6052837899185946628:128` (s5_index 212115, legal 87)
- k03 `6053400849139367936:128` (s5_index 212536, legal 92)
- ladder basis: the published fourteenth k01 adoption reaudit
  closure ladder (`8fe6125f...`, 799 rows); all 799 rows'
  `unknown_now` recomputed from graph `54f9c364...` + head + update8
  receipts `b658290a...`: 799/799 exact match
- top-5 gated exactly as pre-registered: 5804 (3) / 20421 (5) /
  34269 (11) / 12264 (33) / 5343 (46); scanned ranks 1-12
- selector `select_fifteenth_ladder_top.py` sha256 `2ebdf573...`, a
  structural adaptation of the published fourteenth selection
  instrument `eb776f38...` (head/ladder pins, pre-registered top-5 +
  selection gates, claim machinery extended with the adopted
  fourteenth k01 `6053401124017274880:0` as `fourteenth_1`);
  44 fail-closed gates PASS; 3 cold runs byte-identical (run json
  sha256 `be310d04...`)
- all three keys' legal move counts derived independently (repo
  Board vs fresh integer 4x4-determinant concyclicity): 82/82, 87/87,
  92/92 agreement; no key is in the probe-13 supply (proxy null)
- input csvs byte-identical to the fourteenth kit's k02/k03/k04
  input files (`8568c7f5` / `fda5d01d` / `cad75b29`): the same
  three keys, cross-kit byte agreement
- claim status: all three keys UNCLAIMED vs focus_35 / cert_38 /
  third_39 / fourth_41 / fifth_44 / sixth_43 / seventh_42 / eighth_43 /
  ninth_45 / tenth_44 / eleventh_46 / twelfth_51 / sbd_101 / parked_6 /
  the adopted ultra-cheap 4 / the adopted thirteenth 2 / the adopted
  fourteenth 1; fresh vs head; quarantine absent
- tamper battery 5/5 fail-closed (T1 closure rank-1 unknown_now flip
  3->2 w/ pin patched -> P2 recomputation + top-5; T2 head row
  deletion w/ pin patched -> P1 head-shape; T3 claim duplicate
  (k01-key added to fourteenth_1 claim w/ pin patched) -> P3
  claim-sizes/adopted + P4 selection; T4 graph s4_cost UNKNOWN-child
  removal (k04 index 212536 removed from class 5804 w/ pin patched)
  -> P2 + P4; T5 update8 receipt deletion w/ pin patched -> P1
  update8-receipts + P2); clean control re-PASS byte-identical.
  Disclosure: the first T1 attempt hashed the tampered closure file
  before the writer was flushed, so the pin gate (P0) caught it
  instead of the intended P2 computation gate; redone with the file
  properly closed, P2 catches it with the pin patched as designed.

## Deviation from the pre-registered expectation

None. All pre-registered expectations (799/799 recomputation, top-5,
selection class 5804, the three keys, s5 indices, dual-legal counts)
matched the selector's machine output exactly; the pre-pass that
recorded them (one full-battery run, disclosed in the declaration)
agrees with the declared 3-run execution byte-for-byte.

## Claim status

Selection and scheduling bookkeeping only: NO verdict is claimed or
implied.  The standard 11x11 empty board: UNKNOWN.  All 19
central-reply roots: UNKNOWN.  Two-stone root {60,27}: UNKNOWN.
Third-move pair {100,108}: UNKNOWN.  Legal counts, proxy and nodes
are bookkeeping, never verdicts.
