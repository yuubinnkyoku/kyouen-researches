# 2026-11-18 n11 class2-lane: cost78c / cost79c combined receipt fold — first S5 parent fully closed

## 開始時点と判断

開始時の最新mainは 62279f626e5f11f58b136861c4c8662e146c3c21。AGENTS.md と research/knowledge/README.md は現行mainで再確認し、K0023、K0863、K0865、および直近のglobal-fold・78c・79c・82d関連claim/logを確認した。

head-1589 global foldはhead-1476のopen S6行6,372から113行を閉じていた。一方、cost78c（11 WIN7-D10証明書）とcost79c（19新規WIN7-D10証明書）は全件出版・独立検証済みなのに、receipt foldは旧66i/66j/69j/71e/72d/73i/73j/73k/73l依存の後ろでpendingだった。これらの旧foldはglobal foldに取り込まれているため、78c/79cの証明書をまとめてfoldするのが最優先と判断した。

v20 presweepはcost78cの子 00000000000000403800000008000008（cost 78）を再びsweep targetに選んでいたが、この子は既にsweep完了・証明書11件出版済みだった。再sweepせずreceiptをfoldした。v20の歴史記録は変更せず、本foldで選定状態を解消した。

## 成果

30本のWIN7-D10証明書rootを、head-1589の未閉鎖6,259行へ照合した。

- cost78c: 11証明書、BigInt独立検査11/11、cross-lane照合7/7
- cost79c: 19証明書、第三実装BigInt検査19/19（3+16分割）、raw監査19/19、v15 cross-engine 14/14
- 30 rootはすべて7石、manifestのD4正準形と一致、child | (1 << bit) と一致。D4正準形の重複0
- v13の16 verdict map内部衝突0、harvestとの衝突0

D4照合は二方向で独立に実装した。rootを8通りに変換して1石ずつ削除しS6軌道を作る方法と、各open S6行から全rootの8変換を直接調べる方法で、19行・29組の(root,row)対応が一致した。変換番号と追加石番号は正準化の向きに依存するため、比較対象はroot-row対応であり、変換番号そのものではない。

| 出所 | 新たに閉じたS6行 | edge cost減少 | root-row対応数 |
|---|---:|---:|---:|
| cost78c | 5 | 387 | 15 |
| cost79c | 14 | 1,155 | 14 |
| 合計 | 19 | 1,542 | 29 |

cost78cの子行は最後の1行（cost 78）として残っており、このfoldで親S5 00000000000000403800000008000000 が1行/78から0行/0になった。head-1589から初めて完全receipt-closedになったS5親である。

cost79cの子行 00000000000000c09002000200000000 自体は既存global foldですでに閉鎖済みだった。19証明書のうち5本は今回の新規open行を増やさず、残る14本が別の14行をcross-coverした。bit 110は既存cost73k bit87の同一D4軌道なので重複計上していない。

## frontier

| 指標 | head-1589 | 今回後 |
|---|---:|---:|
| solved S6 manifest rows | 1,589 | 1,608 |
| remaining S5 orbits | 174 | 173 |
| unique remaining S6 | 6,259 | 6,240 |
| remaining edge cost | 495,507 | 493,965 |
| open-class S6 demand | 4,543 | 4,524 |
| open-class edge-cost demand | 360,227 | 358,685 |

新規receiptは16親に影響し、parent-row incidenceは32。完全閉鎖した親は1件。

## 再現・反映

- 開始main: 62279f626e5f11f58b136861c4c8662e146c3c21
- 再現スクリプト: research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/scripts/fold_cost78c_79c_receipts_20261118.mjs（blob 17f543a11b74bf88f3c4234fcb4c93c5199dbba9）
- fold record: research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class-frontier-cost78c-79c-receipts-recompute-20261118.json（blob 7e6144a6a...）
- cost78c claim: receipt_fold を COMPLETED に更新。commit e5793e4b26d57eb28fb3e2a6fe5b8db62e535f68 の直前に反映
- cost79c claim: receipt_fold を COMPLETED に更新。commit e5793e4b26d57eb28fb3e2a6fe5b8db62e535f68 の直前に反映

この実行では固定blobの内容をV8のJavaScript整数実装で再計算した。公開Nodeスクリプトは通常のcheckoutで再実行するためのものだが、この実行環境ではcheckout上で同スクリプト自体は起動していない。計算結果は二方向のD4照合、既存の独立証明書検査、head-1589の基準値再計算で照合した。

今回、新しいengine verdictは作っていない。証明書のreceipt/manifest簿記のみである。

## 次の判断

- cost78c/79cはsweep・証明書・receipt foldまで完了。再探索しない。
- v20のcost78c再sweep選択は旧状態に基づくため、次回はhead-1608から21 sweep mapとSTERILE-parent除外を反映してcoordinatorを再構築する。
- cost82dは82/82 REFUTED-D10の再検証であり、対象は全残行STERILEのclass-4親。LOSS証明ではなく、receipt閉鎖対象として再実行しない。

標準11×11空盤、二石root {49,60}/{59,60}、S2 {59,60}、class 1/2/4は引き続きUNKNOWN。REFUTED-D10をLOSSと解釈しない。
