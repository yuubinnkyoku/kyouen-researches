# 2026-11-16：cost-71d（第二候補S5のcost-71行）sweep完走 — STERILE（71/71 REFUTED-D10・証明書なし・foldなし・head 1400不変）

開始時main: `41dcba1c`（本laneのcost-71d IN FLIGHT claim着地直後・canonical headは本laneの統合fold **1400/6448/509842/4718/373565**）。並走laneはcost-70g（同一S5・child `00000000000000801202000040000001`）in flightのため、本laneは第二候補S5 `00000000000000801202000040000000`（head 1400で7行/509）の次の安い未sweep行 **cost-71 child `00000000000000801202000040000400`**（stones [10,30,49,57,60,71]・需要 c1=0,c2=2,c4=0・二開親: 第二候補7行/509〔lift 10〕とclass-2 S5 `00000000000000801202000000000400` 69行/5666〔lift 30〕・他4削除は閉行）をclaimしてsweepした。

## claim（`41dcba1c`）

`class2-lane-cost71d-inflight-20261116.json`: `legal_candidates.py`独立列挙71候補がmanifest edge cost 71とbit-exact・head 1400での需要・開親・lift stonesを`prep_claim_cost71_20261116.py`（統合fold scriptをrunpyして1400 headのrem/demから導出）で再導出してから着地。baselineは**1400**（1398'系ではなく）。

## sweep結果 — STERILE

- v16 engine（blob `0a4a86f6`・depth 10・cap 1e9・andclose 1）・9バッチ4並列・pilots 3402×9全PASS。
- **71/71 REFUTED-D10・0 WIN7-D10・0 capped・総nodes 97,476,178**（最大単一候補 7,590,056 nodes）・terminal全件 [13,17]・andclose全件 true・候補bitはclaim列挙と完全一致（each exactly once）。
- **determinism rerun**: batch5（8候補）を再実行し**node-exact**（nodes/loss/capped全一致）。
- **v15 cross-engine**: pilot d6 loss=false nodes=5949・反証アンカー3件（bits 0/1/3）すべてloss=falseでv16 rawとverdict一致（nodes 2,855,745 / 2,042,176 / 4,196,243 vs v16 1,423,531 / 1,084,822 / 2,170,270）。

## 結論と信頼境界

- このchildのどの7石rootも深さ10以内の先手勝ちを認めない（v16で全候補・v15でアンカー交叉確認）。**WIN7-D10 receiptではこの行を閉鎖できず、head 1400は不変**（証明書0件・foldなし・solved不変）。
- REFUTED-D10はいかなる局面のLOSS証明でもない。11×11空盤、二石root `{49,60}`・`{59,60}`、S2 `{59,60}`、class 1/2/4は引き続き **UNKNOWN**。
- 第二候補S5の残7行のうち、これでcost-64（64a STERILE）とcost-71（71d STERILE）がreceipt閉鎖不能と確定。残る閉鎖可能性はcost-70（70g in flight・並走）・cost-75 `00000000040000809002000000000002`・cost-76 2行・cost-77 `00000000040000809002000000004000`。
