# 2026-11-16 n11 class2-lane cost-66c fold receipt independent agreement (12/12 PASS vs the pre-registration)

## Start state

- Start main for this check: `96e2dbac` (cost-66c fold receipt landed 11:19:20Z;
  follow-ups `42788a0d` this lane's sweep re-run verification, `e795cdce` fold log,
  `fcbd795d` claim v4 field correction).
- The pre-registration `class2-lane-cost66c-fold-preregistration-20261116.json`
  (git blob `809ad05e`, commit `aca9d762`, published 11:10:03Z) was pinned locally by
  this lane BEFORE the fold receipt landed (fetched at 11:11Z from main).

## Check

- `scripts/verify_cost66c_fold_receipt_independent_agreement_20261116.py`: an
  independent field-by-field comparison written from the pre-registration semantics
  only (this lane had not read the fold arm's own check script
  `check_cost66c_fold_receipt_vs_preregistration_20261116.py` when writing it).
- **12/12 checks PASS**: projected head 6-numbers (1450/174/6398/506297/4671/370211),
  basis head 1444 + 764 receipt roots, demand histogram deltas
  (c2=1,c4=0: -4 / c2=1,c4=2: -1 / c2=2,c4=0: -1), all 7 per-receipt records in
  publication order (bit / root hex / D4 canon / covers / marginals /
  marginal-in-manifest), totals (7 receipts / marginal 35 / mim 6), the 6 closed
  manifest rows, all 6 affected parents (rows/edge-cost before-and-after and lost-row
  hexes), empty conflict census, parent edge-cost delta 596, the child closed exactly
  by bit 73, sweep nodes 84180263, and the receipt_bits mapping.
- Output: `output/class2-lane-cost66c-fold-receipt-independent-agreement-20261116.json`
  (byte-identical on re-run).

## Position

- The landed fold receipt agrees completely with the pre-registered independent
  projection: **new canonical head 1450/174/6398/506297/4671/370211** is confirmed by
  two independent projections (the pre-registration arm's and this check).
- Together with this lane's sweep re-run verification (`42788a0d`) and the certificate
  blind re-extraction verification published in the companion commit, the entire
  cost-66c evidence chain (sweep verdicts -> certificates -> fold) now has third-party
  verification at every layer.

## Interpretation guard

- Bookkeeping agreement only. A fold changes manifest coverage bookkeeping, not the
  game-theoretic value of any position. WIN7 certificates prove a first-player win
  within depth 10 from individual 7-stone roots only. REFUTED-D10 is not a LOSS
  proof. The 11x11 empty board, the two-stone roots {49,60} and {59,60}, S2 {59,60},
  and classes 1/2/4 all remain **UNKNOWN**.
