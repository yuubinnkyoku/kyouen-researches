# 2026-11-28 n11 fifteenth ladder-top selection

Completion log of the selection declared in
`research/log/2026-11-28-n11-fifteenth-ladder-top-selection-declaration.md`
(declaration commit `8893fb2d`, single owner, publish-then-execute;
kit `n11-fifteenth-ladder-top-selection-20261128` at commit
`6f6deac0`, fetch-back 12/12 byte-identical via git blob sha).

## Selected (closure-ladder rank 1 under the head a66f636e)

- class 5804 `6053400849139367936:0`, exactly **3 remaining
  unknown S5 keys** (the adopted fourteenth k01 WIN row
  `6053401124017274880:0` resolved the first of the four);
  resolving all three completes the class (a candidate free_now
  flip, Board-verified at adoption time)
- k01 `6053682324116078592:0` (s5_index 207094, legal 82)
- k02 `6052837899185946628:128` (s5_index 212115, legal 87)
- k03 `6053400849139367936:128` (s5_index 212536, legal 92)
- head basis `a66f636e...` (6,897 rows WIN 215 / LOSS 6,682,
  fourteenth k01 adoption); ladder basis the published fourteenth
  k01 adoption reaudit closure ladder `8fe6125f...` (799 rows);
  all 799 rows' unknown_now recomputed from graph `54f9c364...`
  + head + update8 receipts `b658290a...`: 799/799 exact match
- top-5 gated exactly as pre-registered: 5804 (3) / 20421 (5) /
  34269 (11) / 12264 (33) / 5343 (46)
- selector `select_fifteenth_ladder_top.py` sha256 `2ebdf573...`,
  structural adaptation of the published fourteenth selection
  instrument `eb776f38...` (claim machinery extended with the
  adopted fourteenth k01); 44 fail-closed gates PASS; 3 cold runs
  byte-identical (run json sha256 `be310d04...`); dual-implementation
  legal 82/82, 87/87, 92/92; none of the three keys is in the
  probe-13 supply (proxy null); all UNCLAIMED vs every standing
  claim set including the adopted fourteenth 1; fresh vs head;
  quarantine absent
- input csvs byte-identical to the fourteenth selection kit's
  k02/k03/k04 input files (`8568c7f5` / `fda5d01d` /
  `cad75b29`): cross-kit byte agreement on the same three keys
- tamper battery 5/5 fail-closed (T1 closure rank-1 unknown_now
  flip w/ pin patched -> P2 recomputation + top-5; T2 head row
  deletion w/ pin patched -> P1 head-shape; T3 claim duplicate
  w/ pin patched -> P3 + P4; T4 graph s4_cost UNKNOWN-child removal
  (class 5804, index 212536) w/ pin patched -> P2 + P4; T5 update8
  receipt deletion w/ pin patched -> P1 + P2); clean control
  re-PASS byte-identical.  Disclosure: the first T1 attempt hashed
  the tampered file before the writer flushed (the pin gate caught
  it); redone with the file closed so the P2 computation gate
  catches it with the pin patched as designed.

## Deviation from the pre-registered expectation

None. The pre-pass (one full-battery run, disclosed in the
declaration) and the declared 3-run execution agree byte-for-byte;
all pre-registered expectations matched.

## Next work

- A separate single-owner escalation declaration for the three
  selected keys (cold 2M pair sweep, then 15M escalation; WIN-stop
  rule; any WIN needs the C++-gate + third-implementation pillars
  before adoption), then the flip-census/reaudit follow-up.

## Guards

Selection and scheduling only: NO verdict is claimed or implied.
The standard 11x11 empty board: UNKNOWN. All 19 central-reply
roots: UNKNOWN. Two-stone root {60,27}: UNKNOWN. Third-move pair
{100,108}: UNKNOWN. Legal counts, proxy and nodes are bookkeeping,
never verdicts. (kit commit `6f6deac0`, log commit below)
