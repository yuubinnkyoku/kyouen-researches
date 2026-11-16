# 2026-11-16：cost-64h の6証明書を第三の独立実装で再検証

開始時 main: `36f50af4c71987ea9b2de66a9d033969819caa90`。同mainのcost64h証明書ディレクトリに公開済みの6ファイルを取得し、既存の二検証器とは別実装で全戦略木を再生した。

## 検証方式

`verify_cost64h_certificate_bareiss_independent_20261116.mjs` を追加した。行列 `[x²+y²,x,y,1]` の4×4行列式をBigInt直接Bareiss消去で計算し、三点ごとの禁止点集合をキャッシュして合法手を再生成する。既存BigInt verifierの3×3余因子展開、既存TypeScript verifierのNumber Bareissをimportせず、証明書の全応手木を再走査する。

各証明書で、7石rootの安全性、root mobility、全strategy rowの整列・一意性、勝者手の合法性、敗者の全合法応手、終端の敗者手詰まり、消費行集合と証明書行集合の完全一致を検査した。

## 結果

**6 / 6 PASS**

| bit | root mobility / subroots | strategy rows | visited states | terminals |
|---:|---:|---:|---:|---:|
| 4 | 46 | 28,668 | 64,156 | 9,576 |
| 6 | 45 | 25,015 | 58,725 | 9,510 |
| 38 | 44 | 17,496 | 43,333 | 5,971 |
| 49 | 48 | 24,625 | 57,719 | 9,245 |
| 74 | 44 | 23,867 | 52,948 | 7,999 |
| 91 | 44 | 16,590 | 42,592 | 6,436 |
| **合計** | **271** | **136,261** | **319,473** | **48,737** |

- 6 rootすべて7石かつ安全。
- 271/271 subrootの全応手木を検査。
- 全証明書でstrategy行と消費行の差はmissing 0 / extra 0。
- 6証明書すべての終端石数範囲は[13,17]。
- 対象ファイルのGit blob SHAを固定し、取得した内容と照合した。

## 公開物

- 第三検証器: `research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/scripts/verify_cost64h_certificate_bareiss_independent_20261116.mjs`
- 結果JSON: `research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class2-lane-cost64h-certificate-third-verification-20261116.json`

同じ検証アルゴリズムをCode Mode上で実行して6件すべてPASSした。完全cloneがないため、公開したNode.jsファイルをローカルCLIから起動する試験とリポジトリ全体のCIは未実施。再現用スクリプトと入力blob pinはmainに保存した。

## 証明上の境界・次の作業

最新mainのcommit subjectはcost64h証明書進捗を7/23と報告している一方、対象ディレクトリに実在するファイルは6本だった。この監査は確認できた6本だけを数え、未掲載の第7ファイルを推定で加えていない。次回は最新mainを再確認し、追加ファイルの所在・hashを解決する。

6本はいずれも個別7石rootのWIN7証明書として検証できたが、head 1452へのreceipt foldは未着地。証明書の存在だけでS6 manifest行が閉じたとは扱わない。次は残りのWIN rootの証明書抽出、独立検証、marginalの再計算、head 1452へのfoldが必要。

**11×11空盤、二石root {49,60}/{59,60}、S2 {59,60}、class 1/2/4はUNKNOWNのまま。** REFUTED-D10もLOSS証明ではない。
