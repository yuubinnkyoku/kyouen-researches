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

## 修復と実行確認

修正版スクリプトblob: `1ac095ee7e6378d6520cb360a58a1797ea86b90a`  
再計算JSON blob: `f631574b5701bd8f441d2c552ba001814246ef69`  
分析基準main: `55e87206340e87c2bb4e5214dc3d8943fe3b948d`  
入力側source main: `317f6af8c9810941bda38b5cf355a8f27ce3aa65`

修正したのは構文、出力先、Git blobのNUL区切り、JSON schema、検査名、分析基準headである。Git blob headerの区切りは実際のNUL byteでなければならない。二重エスケープされた `\\0` は文字列の「\0」であり、Git blob SHA-1とは一致しない。最初のNode実行で入力SHA検査が失敗したため、この点も修正した。

接続Proxmoxの専用runner `kyouen-80f-runner`（1 vCPU・4 GiB RAM、Node v22.23.5）に、GitHubの固定commitからスクリプトと6入力を取得した。Pythonで6/6のGit blob SHA-1を確認し、`node --check` の後にNodeスクリプトを2回実行した。両回とも15/15 checks PASS。2回目は7.297秒で、生成JSONは保存済みJSONとbyte-identicalだった。生成物のGit blob SHA-1は `f631574b5701bd8f441d2c552ba001814246ef69`、SHA-256は `2e50e310936ba4ac5aa0adc9a11f4fbc579b8ce4828e79ead649348cff7ad646`。

runnerの空き容量は実行前後とも約403 MiB。1 CPUのみ使用し、重い探索は起動していない。GitHub Actionsの状態は別途確認できておらず、この検証は専用runner上のNode実行である。

## 意味と限界

これは49候補rootの浅い二手先構造の再現性修復であり、DFPN探索ではない。303共有類（0.414733%）は9石層だけの重複で、深い探索での共有cache利得や実測費用を示さない。49本は依然として候補rootであり、WIN7-D10証明書ではない。

新しいWIN/LOSS verdict、certificate、receipt、manifest閉鎖は0。REFUTED-D10はLOSS証明ではない。標準11×11空盤、二石root `{49,60}`/`{59,60}`、S2 `{59,60}`、class 1/2/4は **UNKNOWN** のまま。
