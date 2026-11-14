# 2026-11-15 N11 class2-lane: unified merge 1154 endpointの第三独立検証（solved set不要の帳簿法）とmarginal 6 hexの親・需要構造

## 背景

- unified merge foldが2つの並走レーンで独立実行され、同一endpoint **1,154 / 6,693 / 527,949 / 4,963 / 391,672（残りS5 175）** に到達した（7aaa7d83 20:47:56Z、625b0e0c 20:51:40Z）。両者ともrunpyでsolved setを再構成してfoldを再実行する同種の手法である。
- 本セッションは実行環境（bash/filesystem）が終終利用不能で、全計算をsandbox + GitHubコネクタで実施した。gz入力3種（win7-reuse-hits.csv.gz、s5-remaining-after-reuse.csv.gz、s5-s6-remaining-incidences.csv.gz）は取得不能だったため、solved setを一切使わない検証手法を設計した。

## 手法: solved set不要の帳簿法

入力4種のみ:

1. 6分割S6 manifest `ms5_s6_manifest_part1..6.csv`（7,867行: hex, cost, classes）
2. merged-1148 ranking CSV `class-frontier-s5-ranking-after-merged-multiband2-68dhyg-20261115.csv`（175 open S5のper-S5残数・残費用）
3. merged-1148 top-candidates CSV（77行: 子hex, manifest cost, 需要文字列 c1/c2/c4）
4. 50-receipt和解監査の6 marginal C hex（同監査でBigInt独立検証済み）

子incidenceの再生成: children(X) = {canon(X | 1<<m) : 0<=m<=120} ∩ manifest。canonは121-bit BigInt maskのD4 8変換最小（bit index 11*b+a、変換 (x,y),(y,10-x),(10-x,10-y),(10-y,x),(10-x,y),(x,10-y),(y,x),(10-y,10-x)）。175 S5 × 121手 = 21,175回のcanon呼び出し。

鍵定理: 6 C hexはすべてmerged-1148時点で未解決ゆえ、任意のopen S5 Xについて h ∈ rem(X) ⟺ h ∈ children(X) が成り立つ。unsolved軌道の需要（open 175 S5に対するc1/c2/c4計数）はrem行全体の計数と正確に一致し、非C軌道の需要はserving S5が閉じない限り不変、閉じるS5の残り軌道はすべてCに含まれる。よってfold後endpointは帳簿差分で厳密に確定する: new_rem(X) = rem1148(X) − |C ∩ children(X)|、unique = 6,699 − |C ∩ unique|、sum = 528,423 − Σcost(C ∩ unique)、ヒストグラム差分はc1=0（open_only）のC hexのみから生じる。

## 制御（全て通過）

- manifest 7,867行: 検証器実装のD4 canonで全行不変、重複0。
- 175 open S5: 全行canon不変。
- top-candidates 77行（4対象S5: 18+10+8+41行）: 子hexが再生成childrenに存在、manifest cost一致、需要文字列c1/c2/c4が再生成結果と完全一致（公開行の正否判定器として機能）。
- |children(X)| >= rem(X): 175/175。closing ⟺ cost差分0の整合: 175/175。
- 再生child edges合計 14,896。

## 結果: endpoint全数値が権威unified merge JSONと一致

- solved 1,154 / remaining_s5 175 / unique_uncovered 6,693 / sum_uncovered_cost 527,949 / open_demand 4,963 / open_demand_cost 391,672 — 6数値すべて完全一致。
- 需要ヒストグラム（open_only）9バケット完全一致: {c2=0,c4=1: 527, c2=0,c4=2: 3,021, c2=0,c4=3: 12, c2=1,c4=0: 239, c2=1,c4=1: 60, c2=1,c4=2: 9, c2=2,c4=0: 1,034, c2=2,c4=1: 6, c2=2,c4=2: 55}。c2=2,c4=0バケットは1,040→1,034（−6）、他は不変、総和4,963。
- 候補ランキング一致: best coverable class2 `00000000000000809102000000000000` 8軌道/588、audit-blocked class2 `00000000000000809082000000000000` 10/698、best class4 `00000000020000003800000080000000` 18/1,460、いずれも不変。

## marginal 6 hexの親・需要構造（新規の厳密な成果）

全6 hexがmanifest所属・D4 canon不変、costは bit105=`00000000000000849002000000008000` 76 / bit92=`00000000000000849002000010000000` 80 / bit40=`00000000000000801242010000000000` 75 / bit24=`00000000000000801242000001000000` 80 / bit11=`00000000000000801242000000000800` 78 / bit8=`00000000000000801242000000000100` 85（和474）。需要は全員 **c1=0, c2=2, c4=0**（open_only、バケットc2=2,c4=0）。

各hexはちょうど2個のclass-2 S5親に共有され、親の全体は7個:

- `00000000000000801242000000000000`: **全6 hexの共通親**。rem 70→64、cost 5,517→5,043（−474）。
- `00000000000003800000008000002`: 51→50、3,837→3,759（bit11 hex）。
- `00000000000083800000008000000`: 57→56、4,257→4,181（bit105 hex）。
- `00000000000003800000009000000`: 63→62、4,778→4,698（bit24 hex）。
- `00000000000000801202010000000000`: 65→64、4,708→4,633（bit40 hex）。
- `00000000000000403800000080000000`: 69→68、5,590→5,510（bit92 hex）。
- `00000000000000801202000000000100`: 71→70、5,796→5,711（bit8 hex）。

closersは0（remaining_s5は175のまま）。best/next候補の行はこのfoldで一切変化しない。共通親 `...801242000000000000` はclass-2 ranking中位（39番目）だが、cost-70c bandの6 receiptがこのS5の残り子を6個閉じる構造になっている。

## 限界

- 公開receiptに対する帳簿検証であり、証明書本体の再実行ではない。
- 6 marginal hexは和解監査（BigInt独立検証済み）から引用した。
- 需要構造はmerged-1148公開per-S5集計から導出するため、ranking CSVとfoldの両方に同種の誤りがあれば検出できない。
- gz入力3種を本環境で取得できず、solved set経路の再実行はしていない（並走レーンが二重実行済み）。
- 帳簿法はsolved setを要求しないため、今後のfold予測・endpoint検証に再利用可能である。

## push時点の並走状況（併記）

cost-70c warm batch-3が完了し、残りbits 3/42/86/103の4証明書が公開・claim closure済み（並走のgain-0予測: 6751e21e）。cost-69fは証明書5/9（bits 20/44/68/69/118）まで公開済み。これらは次回unified merge foldの材料であり、本検証の1154 endpointには含まれない。

## 解釈上の注意

解消計数はmanifest被覆の前進であり、盤全体の勝敗ではない。WIN7証明書は個別7石rootの深さ10以内のWINのみを証明する。**標準11×11空盤、二石root `{49,60}`・`{59,60}`、S2 `{59,60}`、class2・class4は引き続き UNKNOWN。**

成果物: [検証記録JSON](../experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class2-lane-unified-merge-endpoint-third-verification-20261115.json)
