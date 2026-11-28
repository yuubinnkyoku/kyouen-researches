# n11 sixteenth ladder-top selection 2026-11-28

Kit of the sixteenth closure-ladder top-candidate selection declared
single-owner publish-then-execute (declaration commit `a178dd64`,
`research/log/2026-11-28-n11-sixteenth-ladder-top-selection-declaration.md`),
under the canonical head of record
`merged-exact-s5-chain-plus-fifteenth-k02-20261128.cache`
(sha256 `58110025...`, 6,900 rows WIN 218 / LOSS 6,682) and the
published fifteenth k02 adoption reaudit closure ladder
(`e10b5765...`, 798 rows).

## Selected (closure-ladder rank 1 under the head 58110025)

- class 20421 `1155173304420536320:131072`, exactly **5 remaining
  unknown S5 keys** (resolving all five completes the class, a
  candidate free_now flip, Board-verified at adoption time)
- k01 `1155454779397246976:131072` (s5_index 528689, legal 76)
- k02 `1156299204327378944:131072` (s5_index 543795, legal 73)
- k03 `1155173441859489792:131072` (s5_index 605961, legal 73)
- k04 `1153062242096250880:540672` (s5_index 620742, legal 83)
- k05 `1152921642046849024:68719477248` (s5_index 625899, legal 78)
- ladder basis: the published fifteenth k02 adoption reaudit
  closure ladder (`e10b5765...`, 798 rows; the serving class 5804
  exited the ladder 799 -> 798 in that reaudit); all 798 rows'
  `unknown_now` recomputed from graph `54f9c364...` + head + update8
  receipts `b658290a...`: 798/798 exact match
- top-5 gated exactly as pre-registered: 20421 (5) / 34269 (11) /
  12264 (33) / 5343 (46) / 13342 (50); scanned ranks 1-12
- selector `select_sixteenth_ladder_top.py` sha256 `040a7440...`, a
  structural adaptation of the published fifteenth selection
  instrument `2ebdf573...` (head/ladder pins, pre-registered top-5 +
  selection gates, claim machinery extended with the adopted
  fifteenth k01/k02/k03 `6053682324116078592:0`,
  `6052837899185946628:128`, `6053400849139367936:128` as
  `fifteenth_3`); 45 fail-closed gates PASS; 3 cold runs
  byte-identical (run json sha256 `17c8765d...`)
- all five keys' legal move counts derived independently (repo
  Board vs fresh integer 4x4-determinant concyclicity): 76/76, 73/73,
  73/73, 83/83, 78/78 agreement; no key is in the probe-13 supply
  (proxy null)
- input csvs follow the published fifteenth kit's input csv format
  (one per selected key, legal from the dual derivation)
- claim status: all five keys UNCLAIMED vs focus_35 / cert_38 /
  third_39 / fourth_41 / fifth_44 / sixth_43 / seventh_42 / eighth_43 /
  ninth_45 / tenth_44 / eleventh_46 / twelfth_51 / sbd_101 / parked_6 /
  the adopted ultra-cheap 4 / the adopted thirteenth 2 / the adopted
  fourteenth 1 / the adopted fifteenth 3; fresh vs head; quarantine
  absent
- tamper battery 5/5 fail-closed (T1 closure rank-1 unknown_now flip
  5->4 w/ pin patched -> P2 recomputation + top-5; T2 head row
  deletion w/ pin patched -> P1 head-shape + P3 fifteenth-adopted;
  T3 claim duplicate (k01 selection key added to fourteenth_1 claim
  w/ sizes pin patched) -> P3 fourteenth-adopted + P4 selection
  (selection displaced to class 34269); T4 graph s4_cost UNKNOWN-child
  removal (k05 index 625899 removed from class 20421 w/ pin patched)
  -> P2 + P4; T5 update8 receipt deletion w/ pin patched -> P1
  update8-receipts + P2); clean control re-PASS byte-identical
  (`17c8765d`), all tampered inputs restored byte-identical to their
  pins.

## Deviation from the pre-registered expectation

None. All pre-registered expectations (798/798 recomputation, top-5,
selection class 20421, the five keys, s5 indices, dual-legal counts)
matched the selector's machine output exactly; the pre-pass that
recorded them (one full-battery run, disclosed in the declaration)
agrees with the declared 3-run execution byte-for-byte.

## Claim status

Selection and scheduling bookkeeping only: NO verdict is claimed or
implied.  The standard 11x11 empty board: UNKNOWN.  All 19
central-reply roots: UNKNOWN.  Two-stone root {60,27}: UNKNOWN.
Third-move pair {100,108}: UNKNOWN.  Legal counts, proxy and nodes
are bookkeeping, never verdicts.
