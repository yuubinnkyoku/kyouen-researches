# 2026-11-19 n11: 49-root two-ply frontier reproduction repair

## 発見した不整合

最新 main `45bc836d631b2733ef3922a45e737829c5210b8d` の二手先frontier再現器を監査したところ、公開済みの結果JSONは正しい数値を含む一方、同じmainに置かれたスクリプトはそのままでは実行不能だった。

- 検査配列の `per.every(...)` に閉じ括弧が欠け、JavaScript構文エラーになる。
- 出力先は `OP` と定義されているのに、書き込み時に未定義の `OUTPUT_PATH` を参照する。
- スクリプトと結果JSONの間で、summaryのキー名・行列式メタデータ・検査名が一致していなかった。

したがって、以前の「公開スクリプトをそのまま再実行すれば結果JSONを再現できる」という扱いは誤り。結果JSONの数値自体を直ちに否定するものではないが、再現器の実行可能性と出力由来は別途修復が必要だった。

## 固定入力からの再計算

mobility入力 `b35d54a0ced182153802247452a593096a0acf81`、residual witness `a8eaf00bd6494eda50a68e7d06498bed833a7688`、規則K0001、候補規約K0868を固定して、接続JavaScript実行環境で独立に全49 rootを再計算した。

- 7石root: 49本（48 pair + 1 singleton）
- 異なる3点組: 28,553
- 各3点組×121点の判定: 3,454,913件。三項余因子展開と六項Leibniz展開が全件一致
- 8石子: 2,985。合法応手28〜73、終局子0
- 順序付き二手目: 146,118
- 9石局面: 73,059
- root内D4重複: 0
- 全root横断D4類: 72,756
- root間共有: 303類、213 root pair、最大47類

既存JSONと、全rootの明細・応手数分布・pairwise overlap集合・最大共有状態一覧・集計値を照合し、一致した。pairwise overlapは並び順に依存しない集合比較で確認した。

## 修復

- 再現スクリプトblob: `8b27743bf7fb99aca7ba6eeb61b175b0dedcd505`
- 再計算JSON blob: `429553bae0511f3753af408024563fb4c6898121`
- 分析基準main: `45bc836d631b2733ef3922a45e737829c5210b8d`
- 入力側source main: `317f6af8c9810941bda38b5cf355a8f27ce3aa65`

修正内容は構文、出力先、JSON schemaの一致に限定した。探索器・verdict・certificate・receiptは変更していない。

スクリプト本文は構文検査を通し、同じ固定入力に対する独立再計算で全数値を照合した。ただし、この実行環境にはGitHub checkoutもNode.js実行環境もなく、修正後のNodeスクリプト自体をcheckout上で起動したとは主張しない。GitHub Actionsの結果も未確認である。

## 意味と限界

これは49候補rootの浅い二手先構造の再現性修復であり、DFPN探索ではない。303共有類（0.414733%）は9石層だけの重複で、深い探索での共有cache利得や実測費用を示さない。49本は依然として候補rootであり、WIN7-D10証明書ではない。

新しいWIN/LOSS verdict、certificate、receipt、manifest閉鎖は0。REFUTED-D10はLOSS証明ではない。標準11×11空盤、二石root `{49,60}`/`{59,60}`、S2 `{59,60}`、class 1/2/4は **UNKNOWN** のまま。
