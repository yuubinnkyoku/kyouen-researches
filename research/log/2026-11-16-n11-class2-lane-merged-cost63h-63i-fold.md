# 2026-11-16：cost-63h/63iチェーン分岐の統合fold — head 1367+63h receipt → 1369（新canonical head）

開始時main: `a8137dc4`。**並走laneのcost-63i fold（`12b71971`）がcost-58c chain head 1360/6488/512785/4758/376508に18 receiptをfoldしてhead 1367/6481/512295/4751/376018を宣言した一方、本laneのcost-63h foldは同じ1360 baselineからhead 1362/6486/512653/4756/376376に1 receipt（bit 89）をfold済み**であり、receipts chainが1360から二枝に分岐していた。本セッションは両枝を統合し、単一のcanonical headを確定した。

## 統合fold（`recompute_frontier_merged_cost63h_63i_20261116.py`）

1. **両枝の再現**: 63i fold script（runpy）で1360→1367を、63h fold script（runpy）で1360→1362を再現。両head JSONともblob-identical（63i `db0288f1…`・63h `647498b9…`）。各scriptは58c chain head 1360のbyte-identical再現とcompleted claim fold recordの照合まで含む。
2. **分岐の集合等式**: `s_1362 == s_1360 ∪ cov(63h root)`・`s_1367 == s_1360 ∪ cov(18×63i roots)` をassert。**枝間のcover重複は0**（|cov(63h root)|=7・|cov(18×63i)|=109・overlap=0）。
3. **root disjointness**: 63h bit-89 root `00000000020000801202000040080000` は667 folded roots（58cまで649+63iの18）とraw-hex・D4ともdisjoint。
4. **63h childの1367 headでの残存確認**: child `00000000000000801202000040080000` は三開親の残行（第二候補17行/1185・dual class-2+4 69行/5265・class-4 77行/5548）で需要 c1=0,c2=2,c4=2・lift stones {19, 30, 57} を再導出。
5. **証明書の再assert**: bit-89証明書（26,070行・941,299 bytes・md5 `b721d428…`）を公開bytesと照合し、BigInt+tsverify union 0/0・terminal [13,17]・rows sorted-uniqueを再確認。
6. **fold**: bit-89 receiptを1367 headにfold。**marginal 5・in-manifest 2**（child `00000000000000801202000040080000` + bonus orbit `00000000020000801002000040080000`）・child orbitはbit 89で閉鎖。
7. **reverse-order replay**: 1362 headに18×63i coversをfoldする逆順でも**同一のmerged setとsummary**が再現されることをassert（順序独立性）。63i coversのmarginalは1360/1362のいずれでも80、63h coversのmarginalは1360/1367のいずれでも5。

## 新canonical head: **1369/6479/512163/4749/375886**

- solved 1367→1369（in-manifest +2）・unique_remaining_s6 6481→6479・sum_remaining_cost 512295→512163。
- **第二候補S5: 17行/1185 → 16行/1122**（63h childのみ喪失）。
- dual class-2+4 S5 `00000000000000801202000000080000`: 69行/5265 → 68行/5202。class-4 S5 `00000000000000003800000001800000`: 77行/5548 → 75行/5416（bonus orbit閉鎖込み）。63i第2開親 `00000000000000403800000008000000`: 24行/1704（不変）。
- best coverable class-2は `00000000000000801202000000200000` 3行/209（全残行REFUTED-D10でdepth-10 receipt閉鎖不能・従来通り）。best class-4 blocker S5は18行/1460。
- 出力: head JSON（blob `c3ff5036…`・6,135 B）・ranking CSV（`d065e54f…`・7,537 B）・top-candidates CSV（`34067a18…`・4,663 B）。**2回実行で3出力ともbyte-identical**。
- cost-63h claimに`reconciliation`欄を追記（分岐状況・解消手順・merged headを記録。既存fold recordは1362枝の歴史記録として保持）。
- gap-fill: 並走laneが公開していなかった `reconstruct_tmp_cost63i_20261116.py`（18証明書648,506行のtsverify+BigInt再実行・全PASS）を執筆・公開。63i fold scriptのruntime入力（tmp-cost63i中間体）を誰でも再構成可能。

## 信頼境界

- foldは公開済みreceiptの帳簿更新であり、いかなる局面の勝敗判定でもない。solved数はmanifest被覆のみを測る。
- WIN7証明書はbit-89 rootから深さ10以内の先手勝ちのみを証明する。REFUTED-D10はLOSS証明ではない。
- 統合は既存の19 receiptの被覆集合の和に過ぎず、新たな探索結果は含まない。
- 標準11×11空盤、二石root `{49,60}`・`{59,60}`、S2 `{59,60}`、class 1/2/4は引き続き **UNKNOWN**。

## 再現

```sh
python research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/scripts/reconstruct_tmp_cost63i_20261116.py
python research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/scripts/recompute_frontier_merged_cost63h_63i_20261116.py
```

(tmp-cost58c・tmp-cost63h・tmp-cost83c等の他の中間体は既存のreconstruct script群で再構成済みの前提。実行時間は約2〜3分。)

## 次の一手

- **以後のfoldはmerged head 1369/6479/512163/4749/375886へのre-baseが必須**（両branch head 1362・1367は superseded）。
- **並走laneがcost-63jのIN FLIGHT claim（`4e3fcf00`・child `00000000040000003800000048000000`・1367 baseline）を着地済み** — 本laneは着手禁止。本セッションの1362 headでの独立導出（二開親: del 30 → 第二候補・del 90 → class-2 S5 `00000000000000003800000009000000`、他4削除は閉鎖行・c1=0,c2=2,c4=0）は並走claimの1367 head導出と一致しており、claimの数値を独立に裏付ける。**63j foldはmerged head 1369へのre-baseが必須**。
- 第二候補S5（16行/1122）の次の安い未sweep・未claim行: cost-64 `00000000000000801202000050000000`（c1=0,c2=2,c4=0）・ `00000000000000801282000040000000`（c1=1,c2=1,c4=0）。cost-64既存laneは64bまで。
- 次回定型: 監査v10両実装とagreement v7は1362 headまでのpinであるため、63i foldとmerged fold 1369を組み込むv11拡張（両実装+agreement v8）を機械的に行う。
