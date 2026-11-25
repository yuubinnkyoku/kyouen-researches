# 2026-11-15：cost-71c receipts fold — canonical head 1233 → 1235・bit112 md5誤記の検出と訂正

開始時main: HEAD `02eefc8d`（前セッションの71c sweep/証明書push列の最終コミット）。canonical head 1233（`class-frontier-cost70e-receipts-recompute-20261115.json`・blob `a0171d4bb839aeb813d231c7d879d6a89452359f`）。fold直前に最新mainを再取得し、65l/70f/70gいずれのfoldも着地していないことを確認（fork不要）。

## 成果1：cost-71c receipts fold（head 1233 → 1235）

`recompute_frontier_cost71c_receipts_20261115.py`（70e fold scriptと同じ構成・122公開入力をgit blob shaでbyte-exact検証）を書いて実行した。すべての統制がPASS:

- **baseline再構成**: 29 base inputs + 52 pre-70e head JSONs（402 chain roots）から純幾何で1227 merged headを再構成し、staged controls（638/7208/565500・657/7189/564070・665/7181/563509・814/7032/552811/5256/413283）とmerged CSV（blob `4eeca615`/`0f9905fc`）のbyte-identical再生成を確認。
- **70e fold再現**: 70e head JSONの5 addition records（bits [0,8,24,66,79]）を公開順にfoldし、per-record marginal（5/5/6/6/4・in-manifest 1/1/2/2/0）が公開記録と完全一致、1233/6614/522131/4884/385854に到達、70e head CSV（blob `33fe27c1`/`4561af13`）がbyte-identical再生成されることを確認。
- **71c childの残存確認**: parent1 `00000000000000801202000000200000` 28行/2119・第2親 `00000000000000801202000080000000` 43行/3268がchild `00000000000000801202000080200000`（edge cost 71・需要 c1=0,c2=2,c4=0）を行として持ち、holderはこの2開親のみ。D4 lift: del31=parent1 bit-exact・del21=parent2 bit-exact・残り4削除は閉行。
- **sweep再導出**: 9 raw batch JSONLsから71候補を一度ずつ（claim列挙と一致）・**2 WIN7-D10（bits 24/112・win nodes 457,250/3,985,676）・69 REFUTED・0 capped・総nodes 94,128,613**・pilot 3402×9・batch5 determinism rerun node-exact・v15 cross-engine（WIN 2,695,796/14,334,967・アンカー75/113/116 loss=false・pilot 5949）・D4 duplicate scan（49 manifests/126 roots・0重複）。
- **証明書検証**: bit24単一ファイル（blob `8d9b4459`）・bit112 2分割（part blobs `494ed053`/`c84955f6`・join md5 = 全体md5）・rows sorted-unique（32-hex key + move）・sub-roots == loser mobility == 47/56・BigInt/Bareiss両verify記録の再読み込み（union 0/0）・各rootから自身の追加石を削除するとD4正規化でchildに一致・manifest totals再総和（82,602 rows / 24,639,331 extraction nodes / 2 roots）。
- **root disjointness**: 2新root vs 497 fold済みroot（baseline 12ファイル + class4 batch1/2/3 + 8 laneファイル + 402 chain roots + 70e 5 receipts）をraw-hex・D4両方で確認。2 distinct D4 orbits。
- **fold**: 公開順 [24, 112]でper-record marginalを拡張unionから再導出（bit24: marginal 5・in-manifest 1〔child〕/ bit112: marginal 5・in-manifest 1〔`00000000210000003800000000000200`〕・総marginal 10・総in-manifest 2）・child orbit closure（bit24）・両開親のchild行喪失・set等式・逆順replay。

**fold後 frontier: solved 1235 / unique 6612 / cost 521,988 / open 4,882 / open_cost 385,711**（hist c2=2,c4=0: 957）。parent1 26行/1976（child 71 + `00000000210000003800000000000200` 72を喪失）・第2親42行/3197（child 71を喪失）。次のcoverable class-2候補は third target `00000000000000809102000000000000`（2行/143）が不変最安。

## 成果2：bit112全体md5誤記の検出と訂正

fold中の証明書検証で、**公開済み記録のbit112全体md5が33文字（正しい32-hex md5 `e38d80cfd89ccc8e48264c36a9e7701a` に末尾の余分な `5` が付いた `…7701a5`）**であることを検出した。影響範囲: certificate manifest・claim v2・sweep audit・certificates README・前セッションlog・K0783セクションの6文書。**part md5・join・証明書バイト・両独立検証のPASS・fold算術には一切影響なし**（検証器はバイト列を検証しており、誤記文字列は検証していない）。

対応: fold scriptは真値をassertしつつ誤記を明示検出し、fold head JSONのcontrols（`bit112_join_md5_typo_detected`）に記録。履歴文書はprovenanceのためbyte-unmodifiedとし、[md5 erratum](../experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class2-lane-cost71c-md5-erratum-20261115.json)と[claim v3](../experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class2-lane-cost71c-inflight-20261115.json)のfoldレコードで訂正した。

## 解釈境界（重要）

- solved数はmanifest被覆の簿記であり、いかなる局面のgame-theoretic値も意味しない。
- **REFUTED-D10はLOSS証明ではない**（depth-10以内の先手勝ちが無いことのみ）。
- 2つのWIN7証明書は個別7石rootからdepth-10以内の先手勝ちのみを証明する。child orbitの閉鎖は両開class-2親の残行を減らすが、どちらのS5親も解決せず、class 2・class 4も決定しない。
- **標準11×11空盤・二石root {49,60}/{59,60}・S2 {59,60}・class1・class2・class4は引き続きUNKNOWN**。

## 今後

- 次のfold baselineは本head 1235（`class-frontier-cost71c-receipts-recompute-20261115.json`）。fold前に必ず最新mainを再取得し、並走lane（65l/70f/70g）のfold着地をチェックすること。
- 未着地のreceipts: cost-65l（bits 21/48・証明書本体はmainに無し）・cost-70f（証明書着地済み・fold未）・class4-82b等のin-flight。

詳細: [fold head JSON](../experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class-frontier-cost71c-receipts-recompute-20261115.json)、[ranking CSV](../experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class-frontier-s5-ranking-after-cost71c-receipts-20261115.csv)、[top-candidates CSV](../experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class-frontier-top-candidates-s6-after-cost71c-receipts-20261115.csv)、[fold script](../experiments/n11-s2-5960-ms5-s7-reuse-20261113/scripts/recompute_frontier_cost71c_receipts_20261115.py)、[claim v3](../experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class2-lane-cost71c-inflight-20261115.json)、[md5 erratum](../experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class2-lane-cost71c-md5-erratum-20261115.json)。
