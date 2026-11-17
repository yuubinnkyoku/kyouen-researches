# 2026-11-18：cost66i bit19 receipt fold（head 1473 → 1476）

## 結果

cost66iの9本のWIN7-D10証明書のうち、head1473で最大の正味marginalを持つbit19を1本だけfoldした。証明書は7個のS6 D4 orbitを覆い、そのうちhead1473で新たにmanifestへ追加できる行は3件。残る8本は未foldのまま保持する。

- bit19 root: `00000000000000801226000000080000`（7石）
- 証明書: 40,935 strategy rows、52/52 subroots、BigInt独立検証PASS、union missing/extra 0/0、終端石数13〜17
- 公開済み分割証明書: 739,395 + 739,348 = 1,478,743 bytes。part1/part2/READMEのGit blob SHAは既存BigInt再検証記録のpinと一致
- marginal: 7 D4 S6 orbits、うち新規manifest行3件、S6→S7 edge cost 207
- S5親: 5 parent orbits、7 parent-row incidences。親行残数はすべて正で、S5 parentは1つも閉じない
- 親行edge-cost差分: 489。cost76cの既知foldで同じ計算法を再構成し、6 incidence・458と既存receiptに一致することを較正した
- 既存cost64h/cost76cとのD4重複・WIN/LOSS conflict censusは0

## frontier

| 指標 | head1473 | bit19 fold後 |
|---|---:|---:|
| solved S6 manifest rows | 1473 | 1476 |
| remaining S5 orbits | 174 | 174 |
| unique remaining S6 | 6375 | 6372 |
| sum remaining edge cost | 504596 | 504389 |
| open-class S6 demand | 4648 | 4645 |
| open-class edge-cost demand | 368510 | 368303 |

## 監査・再現

- 入力スナップショット: `output/class2-lane-cost66i-bit19-parent-incidence-input-20261118.json`（Git blob `24a750eb2967930b92023f556b14797b661678b9`）
- 再現スクリプト: `scripts/audit_cost66i_bit19_receipt_fold_20261118.py`
- fold: `output/class-frontier-cost66i-bit19-receipts-recompute-20261118.json`
- audit: `output/class2-lane-cost66i-bit19-receipt-fold-audit-20261118.json`

入力CSV・receipt JSON・証明書manifest・BigInt監査・証明書分割partのGit blob SHAを固定した。今回の計算値は取得した固定入力からJavaScript整数実装で再計算した。Python再現スクリプトは追加したが、この実行環境のcheckout上では未実行である。

## 解釈の境界

これは既存WIN7-D10証明書の簿記foldであり、新しい探索結果ではない。bit19の7石rootだけが深さ10以内の先手勝ちとして証明される。REFUTED-D10はLOSS証明ではない。S5 parentは未閉鎖で、標準11×11空盤、二石root `{49,60}`・`{59,60}`、S2 `{59,60}`、class 1/2/4はすべてUNKNOWNのまま。

次は残る8本のmarginalとconflict censusをhead1476で再計算する。
